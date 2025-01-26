# LIBRARIES
from utilities.utility import *

# SUPPORT FUNCTIONS FOR RAPID TEST
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
    
def perform_scan(token, model_id, image_file, img_size=(96, 96)):
    
    model_path = get_model_from_api(token, model_id)    
    model = tf.keras.models.load_model(model_path)
    
    try:
        img_array = np.frombuffer(image_file.read(), np.uint8)
        
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image decoding failed. Ensure the uploaded file is a valid image format.")

        img = cv2.resize(img, img_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        
        prediction = model.predict(img)
        confidence = np.max(prediction)
        confidence_percent = f"{confidence:.2%}"
        predicted_class = class_names[np.argmax(prediction)]
        
        return [predicted_class, confidence_percent]
    
    finally:
        if os.path.exists(model_path):
            os.remove(model_path)
            print(f"Model file {model_path} has been deleted.")