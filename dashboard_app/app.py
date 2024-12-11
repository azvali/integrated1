from flask import Flask, render_template, request, jsonify
from google.cloud import firestore
from datetime import datetime
import base64
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
IMAGE_FILE_PATH = os.path.join(UPLOAD_FOLDER, "latest_image.txt")
DESCRIPTION_FILE_PATH = os.path.join(UPLOAD_FOLDER, "latest_description.txt")
db = firestore.Client()

def get_default_base64_image():
    with open(os.path.join(UPLOAD_FOLDER, "parking-lot-facebook.jpg"), "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_current_image_data():
    if os.path.exists(IMAGE_FILE_PATH):
        with open(IMAGE_FILE_PATH, "r") as image_file:
            return image_file.read()
    return get_default_base64_image()

def get_current_description_data():
    if os.path.exists(DESCRIPTION_FILE_PATH):
        with open(DESCRIPTION_FILE_PATH, "r") as description_file:
            return description_file.read()
    return "Fake parking lot"

def save_image_data(image_data):
    with open(IMAGE_FILE_PATH, "w") as image_file:
        image_file.write(image_data)

def save_description_data(image_data):
    with open(DESCRIPTION_FILE_PATH, "w") as description_file:
        description_file.write(image_data)

# Initialize with default image
if not os.path.exists(IMAGE_FILE_PATH):
    save_image_data(get_default_base64_image())

@app.route('/')
def home():
    base64_image = get_current_image_data()
    description = get_current_description_data() 
    history = fetch_entities()

    print("db things ", history)

    # print("home endpoint: " + base64_image[:10])
    return render_template('index.html', base64_image=base64_image, description=description, history=history)

@app.route('/submit', methods=['POST'])
async def submit():
    # Ensure the request contains JSON
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400
    
    # Get the data from the request
    data = request.get_json()

    description = data.get('description', None)
    base64_image = data.get('image', None)
    
    if not description or not base64_image:
        return jsonify({'status': 'error', 'message': 'Missing description or image data'}), 400

    # Save the image data to a file
    save_image_data(base64_image)
    save_description_data(description)

    current_time = datetime.now().time().strftime("%H:%M:%S")

    pklot_ref = db.collection('pkinglot')
    pklot_ref.add({
        'availability': description,
        'time': current_time,
    })

    # Send a response indicating success
    response = {
        'status': 'success',
        'description': description,
    }
    return jsonify(response)


def fetch_entities():
    try:
        pklot_ref = db.collection('pkinglot')
        docs = pklot_ref.stream()
        entities = []
        for doc in docs:
            data = doc.to_dict()
            entities.append(data)
        return entities
    except Exception as e:
        raise e


@app.route('/get-entities', methods=['GET'])
def get_entities():
    print("dogdogdodgodgodgo")
    try:
        
        print("get-entities endpoint")
        pklot_ref = db.collection('pkinglot')
        docs = pklot_ref.stream()  
        print(pklot_ref)
        
        entities = [{doc.id: doc.to_dict()} for doc in docs]
    
        return jsonify(entities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
