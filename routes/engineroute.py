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

            return enginerapid.model_scan(model_id, file, token)

    else:
        return jsonify({"Bad Request" : "Invalid Method"}), 400

@engine_blueprint.route('/engine-lab', methods=['POST'])
def lab():
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
            
            input_features = request.form.get('input_features')
            if input_features:
                try:
                    input_features = json.loads(input_features)
                except json.JSONDecodeError:
                    return jsonify({'status': 'Invalid input_features JSON format'}), 400
            else:
                input_features = {
                    'Age': 35.333333333333336, 
                    'Years of Oil Palm Farming': 9.0, 
                    'Age of Plants (Years)': 6.666666666666667, 
                    'Land Area (Ha)': 1.1666666666666667, 
                    'Production (Ton/Month)': 1.4333333333333333, 
                    'Productivity (Ton/ha/Year)': 12.666666666666666, 
                    'TBS Price': 1633.3333333333333,
                    'P-av': 1.4, 
                    'KB': 36.8, 
                    'KTK': 20.0,
                    'SPEKT 1238,3': 25.242376, 
                    'SPEKT 1672,3': 41.152858, 
                    'SPEKT 1718,6': 13.673046, 
                    'SPEKT 1840,1': 74.598919, 
                    'SPEKT 2416,8': 71.74209, 
                    'SPEKT 2870,1': 9.868589, 
                    'SPEKT 3115': 54.357821
                }
                
            if 'file' not in request.files:
                return jsonify({'status': 'No file part in the request'}), 400

            file = request.files['file']

            if file.filename == '':
                return jsonify({'status': 'No file selected'}), 400

            return enginelab.model_lab(model_id, input_features, file, token)

    else:
        return jsonify({"Bad Request" : "Invalid Method"}), 400