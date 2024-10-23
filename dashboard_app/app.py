from flask import Flask, rendertemplate, request, jsonify, g
app = Flask(name)
import base64
import asyncio

def getdefaultbase64image():
    with open("uploads/parking-lot-facebook.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = get_default_base64_image()
description = "Fake parking lot"

@app.route('/')
def home():
    global base64_image 
    global description 
    print("home endpoint: " + base64_image[:10])

    return render_template('index.html', base64_image=base64_image, description=description)

@app.route('/submit', methods=['POST'])
async def submit():
    global base64_image
    global description

    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400

    data = request.get_json()
    description = data.get('description', None)
    base64_image = data.get('image', None)

    if not description or not base64_image:
        return jsonify({'status': 'error', 'message': 'Missing description or image data'}), 400

    response = {
        'status': 'success',
        'description': description,
        'image': base64_image
    }
    return jsonify(response)

if __name == '__main':
    app.run(debug=True, host='0.0.0.0')