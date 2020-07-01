from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from forms import LoginForm
import os
from werkzeug.utils import secure_filename
from model_for_seg import seg

app = Flask(__name__)
app.config.from_object('config')
UPLOAD_FOLDER = './home/Загрузки'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png,jpg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
MAX_FILE_SIZE = 10240 * 1024 + 1
uploads_dir = app.static_folder

global name


def allowed_file(filename):
    s = str(filename)
    if (s[-3:] == 'jpg') or (s[-3:] == 'png'):
        return True
    else:
        return False


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        names = os.listdir('static')
        for i in names:
            if (os.path.isfile(i)) and (i != 'picture.jpg'):
                os.remove(f'static/{i}')
        file = request.files["file"]
        print(file.filename)
        print(allowed_file(file.filename))
        if allowed_file(file.filename):
            file.save(os.path.join(uploads_dir, 'picture.jpg'))
            name = 'picture.jpg'
            print('пересохранение изображения')
            seg('picture.jpg')
        return redirect('/result')
    return render_template("loading.html")


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Roma'}
    posts = [
        {
            'author': {'nickname': 'Susan'},
            'body': 'Nice day'
        },
        {
            'author': {'nickname': 'Petya'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', user=user, posts=posts)


if __name__ == '__main__':
    app.run()
