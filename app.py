from flask import Flask,request, jsonify
from rag import load_pdf,split_documents,create_vector_store
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
        chunks=split_documents(docs)
        create_vector_store(chunks)
        return jsonify({'message': 'File processed successfully',
                         'pages': len(docs),
                         'chunks': len(chunks)}), 200
    
@app.route("/preview/<filename>")
def preview(filename):
    filepath=os.path.join(UPLOAD_FOLDER,filename)
    docs= load_pdf(filepath)
    content=""
    for doc in docs:
        content+=doc.page_content
    return jsonify({"text": content[:2000]})


@app.route("/chunks/<filename>")
def show_chunks(filename):
    filepath=os.path.join(UPLOAD_FOLDER,filename)
    docs=load_pdf(filepath)
    chunks=split_documents(docs)
    return jsonify({
        "total_chunks":len(chunks),
        "first_chunk":chunks[0].page_content
    })

if __name__ == '__main__':
    app.run(debug=True)