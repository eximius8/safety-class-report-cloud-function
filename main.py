#import base64
import json
import random
import string
import os
from flask import abort

# Settings
PROJECT_NAME = os.environ.get('PROJECT_NAME')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def get_random_string(length):
    """
    Generate random string of length = length    
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))    
    return result_str


# gcloud functions deploy safety-report --runtime python38 --trigger-topic generate_waste_rep
# gcloud functions deploy safety-report --runtime python38  --trigger-http --allow-unauthenticated
# functions-framework --target=generate_waste_rep --debug

def generate_latex(data_dict, path_filename):
    """
    Generates tex file in path_filename location
    data_dict - python dictionary to generate WasteReport object instance
    """
    # local
    from wastereport import WasteReport
    doc = WasteReport(data_dict=data_dict)
    doc.create_preamble()
    doc.fill_document() 
    doc.generate_tex(path_filename)


def upload_to_storage(filename, path_filename):
    """
    Upload tex to cloud storage
    filename - name of file on storage
    path_filename - file to upload
    """
    from google.cloud import storage
    
    client = storage.Client(project=PROJECT_NAME)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_filename(path_filename+'.tex')



def generate_waste_rep(request): 

    if request.method == 'OPTIONS':        
        headers = {
            'Access-Control-Allow-Origin': 'https://ma34.ru',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers) 

    headers = {
        'Access-Control-Allow-Origin': 'https://ma34.ru'
    }
    
    try:
        data_dict = request.get_json()
    except:
        return abort(500)
  
   

    filename = get_random_string(10)
    path_filename = f"/tmp/{filename}"

    
    try:
        generate_latex(data_dict['data'], path_filename)
    except:
        return abort(500)
    
    upload_to_storage(filename, path_filename)  
    
    
    return (json.dumps({"url": f'https://latexonline.cc/compile?url=https://storage.googleapis.com/{BUCKET_NAME}/{filename}&force=True'}), 200, headers)  


