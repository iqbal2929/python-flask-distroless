from crypt import methods
from flask import Flask, request, send_file
import json
import os
import yaml

os.mkdir("/files")

api = Flask(__name__)

@api.route('/list-env', methods = ['GET'])
def list_env():

    json_response= []

    for env in os.environ:
        json_response.append({
           "Env variable": env,
            "Env value": os.getenv(env),
        })
    
    return json.dumps(json_response)

@api.route('/set-env', methods = ['PUT'])
def set_env():
    
    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_data = request.json
        os.environ[json_data['Env variable']] = json_data['Env value']

        json_response = {
            "success": "true"
        }
    else:

        json_response = {
            "success": "false",
            "message": "content-Type not supported"
        }

    return json.dumps(json_response)

@api.route('/unset-env', methods = ['DELETE'])
def unset_env():

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_data = request.json

        if json_data['Env variable'] in os.environ:
            del os.environ[json_data['Env variable']]
            
            json_response = {
                "success": "true"
            }

        else:
            json_response = {
                "success": "false",
                "message": "no env variable"
            }

    else:
        json_response = {
            "success": "false",
            "message": "content-Type not supported"
        }
    
    return json.dumps(json_response)

@api.route('/file-env', methods = ['PUT'])
def file_env():
    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        
        json_data = request.json
        
        if json_data['Type'] == "json":
            
            json_array = []
            
            for env in os.environ:
                
                json_array.append({
                    env: os.getenv(env)
                })

            with open('/files/'+ json_data['File name'] + "." + json_data['Type'],'w') as json_file:
                json.dump(json_array, json_file)
            
            json_response = {
                "success": "true",
                "message": json_data['Type'] + " file created file at /files/" + json_data['File name'] + "." + json_data['Type']
            }
            

        elif json_data['Type'] == "env":
            
            with open('/files/'+ json_data['File name'] + "." + json_data['Type'],'w') as env_file:
                for env in os.environ:
                    env_file.write(env + "=" + os.getenv(env) + "\n")
            
            json_response = {
                "success": "true",
                "message": json_data['Type'] + " file created file at /files/" + json_data['File name'] + "." + json_data['Type']
            }

        elif  json_data['Type'] == "yaml":
            
            yaml_array = []
            
            for env in os.environ: 
                
                yaml_array.append({
                    env : os.getenv(env)
                })
            
            with open('/files/'+ json_data['File name'] + "." + json_data['Type'],'w') as yaml_file:
                yaml.dump(yaml_array, yaml_file)
            
            json_response = {
                "success": "true",
                "message": json_data['Type'] + " file created file at /files/" + json_data['File name'] + "." + json_data['Type']
            }
        else:
            json_response = {
                "success": "false",
                "message": "wrong json parameter"
            }

    else:
        json_response = {
            "success": "false",
            "message": "content-Type not supported"
        }
    return json.dumps(json_response)

@api.route('/list-file', methods = ['GET'])
def list_file():

    json_array= []

    for file in os.listdir("/files/"):

        extension = os.path.splitext("/files/" + file)[1]

        json_array.append({
            "File name": file,
            "File type": extension[1:]
        })

    return json.dumps(json_array)

@api.route('/download-file/<filename>', methods = ['GET'])
def download_env(filename):
    return send_file('/files/' + filename, as_attachment=True)