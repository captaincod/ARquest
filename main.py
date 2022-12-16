import os
import glob
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'assets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    for path in glob.glob("assets/*"):
        os.remove(path)
    return render_template('index.html')


@app.route('/get_quest', methods=['GET', 'POST'])
def get_quest():
    lats = []
    lons = []
    assets = []
    if request.method == 'POST':
        for key in list(request.form.keys()):
            if key[:3] == 'lat':
                lats.append(request.form[key])
            elif key[:3] == 'lon':
                lons.append(request.form[key])
        for key in list(request.files.keys()):
            file = request.files[key]
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                asset_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(asset_path)
                assets.append(asset_path)
    print('Lats: ', lats)
    print('Lons: ', lons)
    print('Assets: ', assets)
    return render_template('quest.html', lats=lats, lons=lons, assets=assets)


if __name__ == '__main__':
    app.run('0.0.0.0')
