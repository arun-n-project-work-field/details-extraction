from flask import Flask, render_template, Response,redirect,url_for,jsonify,request
import os
import Scanner

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image_gatway',methods=['POST'])
def image_gatway():
        f=request.files['file']
        f1=request.files['file1']
        UPLOAD_FOLDER = '.'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],"sample.jpg"))
        f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"sample1.jpg"))
        s=Scanner.AdharExtract()
        d=s.getData("sample.jpg","sample1.jpg")
        # s1=Scanner.AdharExtract()
        # d=s1.getaddress("sample1.jpg")
        
        return jsonify(d)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=7000)