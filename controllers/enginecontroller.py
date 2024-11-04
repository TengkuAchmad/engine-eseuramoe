# LIBRARIES
from utilities.utility import *

model = tf.keras.models.load_model('model/palm_kernel_classifier.keras')

# TESTING THE MODEL
def perform_scan(image_file, img_size=(96, 96)):
    img_array = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Image decoding failed. Ensure the uploaded file is a valid image format.")

    img = cv2.resize(img, img_size)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    predicted_class = class_names[np.argmax(prediction)]
    print(prediction)
    print(predicted_class)
    return predicted_class

def model_scan(file):
    try :
        scanresult = perform_scan(file)

        return jsonify({"status" : "Request success!", "result" : scanresult }), 200
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 404