from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    file.save(f'uploads/{file.filename}')

    response = {
        'status': 'success',
        'filename': file.filename
    }
    return jsonify(response)











if __name__ == '__main__':
    app.run(debug=True)
    