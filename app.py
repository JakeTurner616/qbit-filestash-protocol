import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
UPLOAD_FOLDER = './mnt'
ALLOWED_EXTENSIONS = set(['torrent'])

app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def clear_folder():
    # Removes all files from the UPLOAD_FOLDER directory
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

@app.route("/", methods=['GET', 'POST'])
def display_iframe():
    return """
    <!doctype html>
    <title>Web UI</title>
    <iframe src="http://127.0.0.1:8080/" style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;">
    
<a href="http://127.0.0.1:8080/">Click to go to torrent web UI</a>

</iframe>

    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
