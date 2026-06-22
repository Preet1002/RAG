from flask import Flask,request, jsonify
from rag import load_pdf
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        docs=load_pdf(filepath)
        return jsonify({'message': 'File loaded successfully', 'pages': len(docs)}), 200
    
@app.route("/preview/<filename>")
def preview(filename):
    filepath=os.path.join(UPLOAD_FOLDER,filename)
    docs= load_pdf(filepath)
    content=""
    for doc in docs:
        content+=doc.page_content
    return jsonify({"text": content[:2000]})

if __name__ == '__main__':
    app.run(debug=True)