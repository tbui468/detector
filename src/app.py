from flask import Flask, request, render_template_string
from PIL import Image
import os, shutil
import time
import torch
import detect
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.files)
    out_path = ''
    if request.files:
        img = request.files['image']
        #img = Image.open(image)
        result = detect.predict(img)
        folder = 'static'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            os.unlink(file_path)

        ts = time.time()
        out_path = 'static/output' + str(ts) + '.png'
        result.save(out_path)

    #render template is reading from same directory as __init__.py, 
    #but img.save is reading from src directory
    return render_template_string(
            '''
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="image"/>
                <button type="submit">Submit</button>
            </form>
            <img src="{{output}}" alt="test output">
            <h1>Nope</h1>
            ''', output=out_path)



    if __name__ == '__main__':
        app.run()
