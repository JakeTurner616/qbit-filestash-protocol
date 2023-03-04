import os
from flask import Flask, redirect, url_for
from flask import send_from_directory

app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
