def seg(name):
    import torchvision
    from PIL import Image
    import torch
    import matplotlib.pyplot as plt
    import pandas as pd
    import os
    import numpy as np
    import warnings
    from torchvision import transforms
    from PIL import Image
    from pathlib import Path
    from torch.utils.data import Dataset, DataLoader
    from torchvision import models


    class Mydataset(Dataset):
        """
        Датасет с картинками, который паралельно подгружает их из папок
        производит скалирование и превращение в торчевые тензоры
        """

        def __init__(self, files):
            super().__init__()
            # список файлов для загрузки
            self.files = sorted(files)

        def load_sample(self, file):
            image = Image.open(file)
            image.load()
            return image

        def len(self):
            return len(self.files)

        def getitem(self, index):
            transform = transforms.Compose([
                transforms.Resize(256),
                #transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
            ])

            x = self.load_sample(self.files[index])
            x = transform(x)
            return x


    def decode_segmap(image,
                      nc=21):  # С помощью данной функции мы сможем отрисовывать различными цветами различные изображения

        label_colors = np.array([(0, 0, 0),  # 0=background
                                 # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                                 (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                                 # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                                 (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                                 # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                                 (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                                 # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                                 (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

        r = np.zeros_like(image).astype(np.uint8)
        g = np.zeros_like(image).astype(np.uint8)
        b = np.zeros_like(image).astype(np.uint8)

        for l in range(0, nc):
            idx = image == l
            r[idx] = label_colors[l, 0]
            g[idx] = label_colors[l, 1]
            b[idx] = label_colors[l, 2]

        rgb = np.stack([r, g, b], axis=2)
        return rgb


    fcb = models.segmentation.deeplabv3_resnet101(pretrained=4, progress=True, num_classes=21,
                                                  aux_loss=None).eval()  # Скачиваем модель
    result = []
    from PIL import Image, ImageFile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    TRAIN_DIR = Path('instance/uploads/')
    train_files = sorted(list(TRAIN_DIR.rglob(name)))
    print(train_files)

    train_dataset = Mydataset(train_files)
    for i in range(train_dataset.len()):
        ing = train_dataset.getitem(i)
        ing = ing.unsqueeze(0)
        out = fcb(ing)['out']
        out = out.squeeze(0)
        out = torch.argmax(out, dim=0).detach().numpy()
        ii = decode_segmap(out)
        result.append(ii)

    result = np.array(result)
    q = Image.fromarray(result[0], 'RGB')
    print('СЕТЬ ОТРАБОТАЛА')
    q.save('static/result.jpg')
    return