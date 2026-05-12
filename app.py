import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Setup a temporary folder to save uploads before processing
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set a hard limit of 5MB for uploads to protect your server
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

def check_creative_compliance(filepath, expected_width, expected_height):
    results = {
        "Status": "✅ Pass",
        "File Type": "Unknown",
        "Size (KB)": "0",
        "Dimensions": "Unknown",
        "Animation Length (s)": "N/A",
        "Errors": []
    }

    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes / 1024
    results["Size (KB)"] = f"{size_kb:.2f}"
    
    if size_kb > 150:
        results["Errors"].append(f"Size is {size_kb:.2f} KB (Max allowed is 150 KB).")

    try:
        with Image.open(filepath) as img:
            file_format = img.format.upper()
            allowed_formats = ['JPEG', 'PNG', 'GIF'] 
            results["File Type"] = file_format
            
            if file_format not in allowed_formats:
                results["Errors"].append(f"Invalid type: {file_format}. Must be JPG, PNG, or GIF.")

            actual_width, actual_height = img.size
            results["Dimensions"] = f"{actual_width}x{actual_height}"
            
            if actual_width != expected_width or actual_height != expected_height:
                results["Errors"].append(f"Invalid dimensions: {actual_width}x{actual_height}. Expected {expected_width}x{expected_height}.")

            if file_format == 'GIF' and getattr(img, "is_animated", False):
                duration_ms = 0
                loop_count = img.info.get("loop", 1) 
                
                for frame in range(img.n_frames):
                    img.seek(frame)
                    duration_ms += img.info.get('duration', 100) 
                
                duration_sec = duration_ms / 1000.0
                results["Animation Length (s)"] = f"{duration_sec:.2f}"

                if loop_count == 0:
                    results["Errors"].append("GIF loops infinitely. Animations must stop within 30 seconds.")
                elif duration_sec > 30:
                    results["Errors"].append(f"Animation duration is {duration_sec:.2f}s (Max allowed is 30s).")

    except Exception as e:
        results["Errors"].append("Could not read image data. File might be corrupted.")

    if len(results["Errors"]) > 0:
        results["Status"] = "❌ Fail"

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    filename = None

    if request.method == 'POST':
        # Grab the file and dimensions from the form
        file = request.files.get('creative')
        expected_width = int(request.form.get('width', 0))
        expected_height = int(request.form.get('height', 0))

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save, Analyze, and Delete
            file.save(filepath)
            report = check_creative_compliance(filepath, expected_width, expected_height)
            os.remove(filepath) 

    return render_template('index.html', report=report, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)