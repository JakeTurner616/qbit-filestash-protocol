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
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('display_iframe'))
    return """
    <!doctype html>
    <html>
        <head>
            <title>Uploader</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                }

                h1 {
                    font-size: 24px;
                    margin-bottom: 20px;
                }

                label {
                    display: block;
                    margin-bottom: 10px;
                }

                input[type=file] {
                    margin-bottom: 10px;
                }

                input[type=submit] {
                    background-color: #f44336;
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin-top: 20px;
                    cursor: pointer;
                }

                input[type=submit]:hover {
                    background-color: #d32f2f;
                    text-decoration: underline;
                }

                .login p {
                    margin: 0;
                    padding: 0;
                    margin-bottom: 10px;
                }
                #content, href {
                max-width: max-content;
                max-width: min-content;
                padding: 100px;
                border: 2px solid #ccc;
                }
                html,  body > center:nth-child(3) > a:nth-child(2) {
                background-color: #303030;
                color: #fff;
                }
            </style>
        </head>
<body>
<br></br>

<center>
<h1>.torrent upload</h1>
<div id="content">
  
<form action="" method="post" enctype="multipart/form-data">
    <label>Select a file to upload:</label>
    <input type="file" name="file">
    <input type="submit" value="Upload">
  </form>
<br></br>
  <p><b>currently in memory:</b> %s</p>
  </div>
  
<a href="/webui">torrent ui</a>
  </center>
</body>

<style>
.container {
  display: flex;
}

.login, .viewer {
  margin-right: 20px;
}
</style>

    </html>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

    
    

@app.route("/webui")
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
