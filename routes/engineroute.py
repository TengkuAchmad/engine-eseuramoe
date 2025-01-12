# LIBRARIES
from utilities.utility import *

engine_blueprint = Blueprint('model_scan', __name__)

@engine_blueprint.route('/engine-scan', methods=['POST'])
def scan():
    if request.method == 'POST':
        if 'multipart/form-data' not in request.content_type:
            return jsonify({'status': 'Missing form-data in request'}), 400
        else :
            model_id = request.form.get('model_id')
            if not model_id:
                return jsonify({'status': 'No Model ID in the request'}), 400
            
            token = request.form.get('token')
            if not token:
                return jsonify({'status': 'No token in the request'}), 403
            
            if 'file' not in request.files:
                return jsonify({'status': 'No file part in the request'}), 400

            file = request.files['file']

            if file.filename == '':
                return jsonify({'status': 'No file selected'}), 400

            return enginecontroller.model_scan(model_id, file, token)

    else:
        return jsonify({"Bad Request" : "Invalid Method"}), 400