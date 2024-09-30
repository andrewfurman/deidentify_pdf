from flask import Flask, render_template, request, send_file, url_for, redirect
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def delete_previous_files():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    pdf_file = files[0] if files else None
    return render_template('index.html', pdf_file=pdf_file)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['pdf_file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file and file.filename.lower().endswith('.pdf'):
        delete_previous_files()  # Delete previously uploaded files
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return render_template('index.html', pdf_file=file.filename)

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_pdf(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)