from flask import Flask, render_template, request, jsonify, g, session
import base64
import asyncio

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session encryption

def get_default_base64_image():
    with open("uploads/parking-lot-facebook.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.before_request
def load_defaults():
    # Set defaults in the session if they are not already there
    if 'base64_image' not in session:
        session['base64_image'] = get_default_base64_image()
    if 'description' not in session:
        session['description'] = "Fake parking lot"

@app.route('/')
def home():
    base64_image = session.get('base64_image')
    description = session.get('description')
    print("home endpoint: " + base64_image[:10])
    return render_template('index.html', base64_image=base64_image, description=description)

@app.route('/submit', methods=['POST'])
async def submit():
    # Ensure the request contains JSON
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400
    
    # Get the data from the request
    data = request.get_json()
    description = data.get('description')
    base64_image = data.get('image')

    if not description or not base64_image:
        return jsonify({'status': 'error', 'message': 'Missing description or image data'}), 400
    
    # Update the session data
    session['description'] = description
    session['base64_image'] = base64_image
    
    print("submit endpoint: " + base64_image[:10])
    
    # Send a response indicating success
    response = {
        'status': 'success',
        'description': description,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
