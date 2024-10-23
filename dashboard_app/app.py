from flask import Flask, render_template, request, jsonify
import base64

app = Flask(__name__)

# Global variables to hold the base64 image and description
base64_image = ""
description = "Fake parking lot"

@app.route('/')
def home():
    global base64_image
    global description
    return render_template('index.html', base64_image=base64_image, description=description)

# Route to receive base64 string and description from Raspberry Pi
@app.route('/submit', methods=['POST'])
async def submit():
    global base64_image
    global description

    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400

    data = await request.get_json()
    
    # Update the image and description with incoming data from the Raspberry Pi
    base64_image = data.get('image', base64_image)  # Update base64 string
    description = data.get('description', description)  # Update description

    return jsonify({
        'status': 'success',
        'description': description,
        'image': base64_image
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
