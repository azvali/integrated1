from flask import Flask, render_template, request, jsonify
import base64
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
IMAGE_FILE_PATH = os.path.join(UPLOAD_FOLDER, "latest_image.txt")

def get_default_base64_image():
    with open(os.path.join(UPLOAD_FOLDER, "parking-lot-facebook.jpg"), "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_current_image_data():
    if os.path.exists(IMAGE_FILE_PATH):
        with open(IMAGE_FILE_PATH, "r") as image_file:
            return image_file.read()
    return get_default_base64_image()

def save_image_data(image_data):
    with open(IMAGE_FILE_PATH, "w") as image_file:
        image_file.write(image_data)

# Initialize with default image
if not os.path.exists(IMAGE_FILE_PATH):
    save_image_data(get_default_base64_image())

@app.route('/')
def home():
    base64_image = get_current_image_data()
    description = "Fake parking lot"  # You may also store this in a file if it needs to be dynamic

    print("home endpoint: " + base64_image[:10])
    return render_template('index.html', base64_image=base64_image, description=description)

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

    # Send a response indicating success
    response = {
        'status': 'success',
        'description': description,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
