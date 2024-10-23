from flask import Flask, render_template, request, jsonify, g
app = Flask(__name__)
import base64
import asyncio



def get_default_base64_image():
    with open("uploads/parking-lot-facebook.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

@app.before_request
def before_request():
    g.base64_image = None
    g.description = None
    
@app.route('/')
def home():
    base64_image = g.base64_image or "default_base64_image"
    description = g.description or get_default_base64_image()
    print("home endpoint: " + base64_image[:10])
    
    return render_template('index.html', base64_image =g.base64_image, description =g.description)



@app.route('/submit', methods=['POST'])
async def submit():
 
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
    

    g.base64_image = base64_image
    g.description = description
    # Send a response indicating success
    response = {
        'status': 'success',
        'description': description,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')