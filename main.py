# LIBRARIES
from flask import Flask
from flask_cors import CORS
from utilities.utility import *

# PROJECT CONFIG
import os
import sys
sys.dont_write_bytecode = True

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)


# CORS DECLARATOR
CORS(app, origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(engine_blueprint)

@app.route('/')
def health_check():
    return {"status": "running", "message": "Welcome to the Flask app!"}, 200

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=8000)