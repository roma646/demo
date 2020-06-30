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
uploads_dir = os.path.join(app.instance_path, 'uploads')

global name


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        names = os.listdir('static')
        for i in names:
            os.remove(f'static/{i}')
        file = request.files["file"]
        file.save(os.path.join(uploads_dir, 'picture.jpg'))
        name = str(file.filename)
        seg(name)
        return redirect('/result')
    return render_template("loading.html")


@app.route('/result')
def result():
    return render_template('result.html', name=name)


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
