import boto3
import urllib.request
import os
from flask import Flask, flash, request, redirect, render_template
import base64
import boto3



def detect_text(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    return len(textDetections)


app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return render_template('form.html', message="hello")

@app.route('/', methods=['POST'])
def upload_file():
    image_in_base_64 = base64_to_file(request.data)
	
    client = boto3.client('rekognition')

    response = client.detect_text(Image={'Bytes': image_in_base_64 })  
    
    return {"status":"ok", "detection": response}
    

def base64_to_file(img_data):
    img_data = img_data.decode("utf-8")
    img_data = img_data.replace("data:image/png;base64,", "")
    #return bytes(img_data, 'utf-8')
    return base64.decodebytes(bytes(img_data, 'utf-8'))
    # with open("imageToSave.png", "wb") as fh:
    #     fh.write(base64.decodebytes(bytes(img_data, 'utf-8')))  
        
    
    
# @app.route("/")
# def hello():
#     return "Hello World!"

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
# bucket='edx-ricardodps'
# photo='sample-image-2.jpg'
# text_count=detect_text(photo,bucket)
# print("Text detected: " + str(text_count))

