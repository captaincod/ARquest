import os
import glob
import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'assets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    # Очищаем ассеты перед каждой сессией
    for path in glob.glob("assets/*"):
        os.remove(path)
    return render_template('index.html')


@app.route('/get_quest', methods=['GET', 'POST'])
def get_quest():
    lats = []
    lons = []
    assets = []
    errors = ""
    if request.method == 'POST':
        for key in list(request.form.keys()):
            if key[:3] == 'lat':
                if request.form[key] == '':
                    errors += f"Не задана широта на номере {int(key[3:])+1}; "
                else:
                    try:
                        a = float(request.form[key])
                    except ValueError:
                        errors += f"Широта номер {int(key[3:]) + 1} не является координатой; "
                lats.append(request.form[key])
            elif key[:3] == 'lon':
                if request.form[key] == '':
                    errors += f"Не задана долгота на номере {int(key[3:])+1}; "
                else:
                    try:
                        a = float(request.form[key])
                    except ValueError:
                        errors += f"Долгота номер {int(key[3:]) + 1} не является координатой; "
                lons.append(request.form[key])
        for key in list(request.files.keys()):
            file = request.files[key]
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                asset_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(asset_path)
                size = os.stat(asset_path).st_size / 1000000
                if size > 15:
                    errors += f"Файл {filename} больше 15 мегабайт; "
                assets.append(asset_path)
        maximum = lambda a, b: a if a > b else b
        if len(assets) < maximum(len(lats), len(lons)):
            errors += f"Не на всех точках прикреплены изображения; "
    if errors:
        for path in glob.glob("assets/*"):
            os.remove(path)
        return render_template("index.html", errors=errors)
    else:
        data = ""
        for i in range(len(lats)):
            data += f"<a-image \n src=\"{assets[i]}\" \n look-at=\"[gps-camera]\" \n" \
                    f"scale=\"1 1 1\" \n gps-entity-place=\"latitude: {lats[i]}; longitude: {lons[i]};\"></a-image> \n"
        return render_template("quest.html", data=data)


if __name__ == '__main__':
    app.run('0.0.0.0')
