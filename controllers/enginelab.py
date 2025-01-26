# LIBRARIES
from utilities.utility import *

# VARIABLES DECLARATION BEGIN
scaler = joblib.load('./docs/scaler_iseuramoe.pkl')

le = joblib.load('./docs/label_encoder_iseuramoe.pkl')

# VARIABLES DECLARATION END 

# SUPPORT FUNCTIONS FOR RAPID TEST BEGIN
def download_model(model_url, save_path='downloaded_model.keras'):
    response = requests.get(model_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f'Model successfully downloaded and saved to {save_path}')
    else:
        raise ValueError(f'Failed to download the model from {model_url}')

def get_model_from_api(token, model_id):
    api_url = f"http://128.199.122.162:3000/model-management/get/{model_id}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        model_url = data['data']['Url_MD']
        print(f"Model URL retrieved: {model_url}")

        model_path = 'downloaded_model.keras'
        download_model(model_url, model_path)
        return model_path
    else:
        raise ValueError(f"Error fetching model data: {response.json()['message']}")
    
def model_scan(model_id, file, token):
    try :
        scanresult = perform_scan(token, model_id, file)

        return jsonify({"status" : "Request success!", "result" : scanresult }), 200
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 404  
    
def parseKeys(file_path):
    try:
        restored_list = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                restored_list.append(row[0]) 
        return restored_list
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def get_features_from_input(input_features, all_keys, scaler):
    if not all_keys or not scaler:
        raise ValueError("Feature keys (all_keys) or scaler are not defined.")
    feature_values = {key: input_features.get(key, 0) for key in all_keys}
    
    feature_vector = np.array(list(feature_values.values())).reshape(1, -1)
    
    return scaler.transform(feature_vector) 

@tf.function
def predict_with_model(model, image, features):
    return model([image, features])
# SUPPORT FUNCTIONS FOR RAPID TEST END

# PERFORM SCAN BEGIN
def perform_scan(token, input_features, model_id, image_file, img_size=(96, 96)):
    
    # LOAD MODEL BEGIN
    model_path = get_model_from_api(token, model_id)    
    model = tf.keras.models.load_model(model_path)
    # LOAD MODEL END
    
    try:
        
        # IMAGE PROCESSING BEGIN
        img_array = np.frombuffer(image_file.read(), np.uint8)
        
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image decoding failed. Ensure the uploaded file is a valid image format.")

        img = cv2.resize(img, img_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        # IMAGE PROCESSING END
        
        # READ ALL KEYS BEGIN
        all_keys = parseKeys('./docs/all_keys.csv');
        # READ ALL KEYS END
        
        # PROCESS ADDITIONAL FEATURES BEGIN
        features = get_features_from_input(input_features, all_keys, scaler)
        # PROCESS ADDITIONAL FEATURES END
        
        # PERFORM PREDICTION BEGIN
        prediction = predict_with_model(model, img, features)
        # PERFORM PREDICTION END
        
        # EXTRACT SCORES BEGIN
        scores = prediction.numpy()[0] 
        # EXTRACT SCORES END
        
        # FILTER AND SORT BEGIN
        threshold = 1e-4 
        non_zero_scores = [(i, score) for i, score in enumerate(scores) if score > threshold]
        non_zero_scores.sort(key=lambda x: x[1], reverse=True)
        # FILTER AND SORT END
        
        # EXTRACT PREDICTED CLASS AND CONFIDENCE BEGIN
        predicted_class_index = np.argmax(scores)
        predicted_class = le.inverse_transform([predicted_class_index])[0]
        confidence = scores[predicted_class_index]
        confidence_percent = f"{confidence:.2%}"
        # EXTRACT PREDICTED CLASS AND CONFIDENCE END
        
        print(f"\nPredicted Class: {predicted_class} with Confidence: {confidence:.2%}")
        
        return [predicted_class, confidence_percent]
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if os.path.exists(model_path):
            os.remove(model_path)
            print(f"Model file {model_path} has been deleted.")
# PERFORM SCAN END

def model_lab(model_id, input_features, file, token):
    try :
        scanresult = perform_scan(token, input_features, model_id, file)

        return jsonify({"status" : "Request success!", "result" : scanresult }), 200
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 404