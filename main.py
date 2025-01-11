# LIBRARIES
from utilities.utility import *

# PROJECT CONFIG
import sys
sys.dont_write_bytecode = True

app = Flask(__name__)

# CORS DECLARATOR
CORS(app, origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(engine_blueprint)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=8000)