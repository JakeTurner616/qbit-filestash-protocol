import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './mnt'
ALLOWED_EXTENSIONS = set(['torrent'])

app = Flask(__name__)
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
            <title>Web UI</title>
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
                    background-color: #4CAF50;
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
                    background-color: #3e8e41;
                }

                .login {
                    border: 1px solid #ccc;
                    padding: 20px;
                    margin-top: 20px;
                }

                .login p {
                    margin: 0;
                    padding: 0;
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <h1>Upload new .torrent</h1>
            <form action="" method="post" enctype="multipart/form-data">
                <label>Select a file to upload:</label>
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
            <div class="login">
                <p>Sign in to start packing:</p>
                <p>Username: guest</p>
                <p>Password: adminadmin</p>
                <form target="iframe1" action="https://guac.serverboi.org/guacamole/#/">
                    <input type="submit" value="Launch Packer">
                </form>
            </div>
            <p></p>
            <iframe name="iframe1" src="" style="width:500px; height:500px; bottom:0; right:0;"></iframe>
            <p><b>currently in memory:</b> %s</p>
        </body>
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

