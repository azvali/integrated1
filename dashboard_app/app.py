from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    response = {
        'status': 'success',
        'data': data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)