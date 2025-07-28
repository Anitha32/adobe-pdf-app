
from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import fitz  # PyMuPDF
import json
from extract_outline import extract_outline_from_pdf
from extract_relevant import extract_relevant_info

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_outline', methods=['POST'])
def extract_outline():
    uploaded_files = request.files.getlist("pdf_files")
    results = []
    for file in uploaded_files:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        outline = extract_outline_from_pdf(filepath)
        output_path = os.path.join(OUTPUT_FOLDER, file.filename.replace('.pdf', '.json'))
        with open(output_path, 'w') as f:
            json.dump(outline, f, indent=2)
        results.append({file.filename: outline})
    return jsonify(results)
@app.route('/extract_relevant', methods=['POST'])
def extract_relevant():
    uploaded_files = request.files.getlist("pdf_files")
    persona_file = request.files['persona_file']

    # Save persona.json
    persona_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(persona_file.filename))
    persona_file.save(persona_path)

    # 🔧 FIX: Always use UTF-8
    with open(persona_path, encoding='utf-8') as pf:
        persona_data = json.load(pf)

    # Call your Round 1B function
    extract_relevant_info(uploaded_files, persona_data)

    return jsonify({"status": "success", "message": "Relevant content extracted."})



@app.route('/output/<filename>')
def download_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
