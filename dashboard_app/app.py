from flask import Flask, render_template, request, jsonify, g
app = Flask(__name__)
import base64
import asyncio



def get_default_base64_image():
    with open("uploads/parking-lot-facebook.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    


base64_image = get_default_base64_image()
description = "Fake parking lot"
    
@app.route('/')
def home():
    global base64_image 
    global description 
    print("home endpoint: " + base64_image[:10])
    
    return render_template('index.html', base64_image = base64_image, description = description)



@app.route('/submit', methods=['POST'])
async def submit():
 
    global base64_image
    global description
    print("dog")
    # Ensure the request contains JSON
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400
    
    # Get the data from the request
    data = request.get_json()

    description = data.get('description', None)
    base64_image = data.get('image', None)
    
    print("submit endpoint: " + base64_image[:10])
    if not description or not base64_image:
        return jsonify({'status': 'error', 'message': 'Missing description or image data'}), 400

    # Send a response indicating success
    response = {
        'status': 'success',
        'description': description,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')