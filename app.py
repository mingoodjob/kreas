from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os

db = client.vip


model = tf.keras.models.load_model('static/model/model.h5') 

app = Flask(__name__)

def dbsave(img,label):
    col = db.image_class

    doc = {

        'img': img,
        'label': label,

    }

    col.insert_one(doc)    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fileupload', methods=['POST'])
def file_upload():
    global save_to
    file = request.files['file_give']
    
    extension = file.filename.split('.')[-1]
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'
    
    save_to = f'static/img/catdog/{filename}.{extension}'
    
    file.save(save_to)

		
    return jsonify({'result':'success'})

@app.route('/result')
def result():
	 
    test_datagen = ImageDataGenerator(rescale = 1./255)
    test_dir = 'static/img'
    test_generator = test_datagen.flow_from_directory(
            test_dir,
            
            target_size =(256, 256),
            color_mode ="rgb",
            shuffle = False,
            
            class_mode = None,
            batch_size = 1)
    pred = model.predict(test_generator)
    
    if pred[-1] > 0.5:
        result = '강아지'
        dbsave(save_to,'result')
    else:
        result = '고양이'
        dbsave(save_to,'result')
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)