import streamlit as st
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Creative Inspector", layout="wide")

# 2. Injecting your specific CSS, Fonts, and Colors
st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Manrope:400,500,600,700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Apply Manrope Font globally */
        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif !important;
        }
        
        /* Style the Streamlit File Uploader to match your yellow/gold theme */
        [data-testid="stFileUploadDropzone"] {
            background-color: #FFCA011A !important;
            border: 2px dashed #d1d5db !important;
            border-radius: 8px;
            padding: 40px !important;
        }
        [data-testid="stFileUploadDropzone"]:hover {
            background-color: #FFCA0133 !important;
        }

        /* Custom Table Styling to match your tool */
        .custom-table-container {
            width: 100%;
            overflow-x: auto;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            margin-bottom: 2rem;
            background-color: white;
        }
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            text-align: center;
            font-size: 14px;
        }
        .custom-table th {
            background-color: #2B0030;
            color: white;
            padding: 12px 16px;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.05em;
        }
        .custom-table td {
            padding: 16px;
            border-top: 1px solid #e5e7eb;
            color: #4b5563;
        }
        .custom-table tbody tr:nth-child(even) {
            background-color: rgba(43, 0, 48, 0.02);
        }
        
        /* Text Alignments & Highlighting */
        .text-left { text-align: left; }
        .text-orange { color: #FF2000; font-weight: bold; }
        
        /* Section Headers */
        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 14px;
            font-weight: 600;
            color: #4b5563;
        }
        .icon-circle-fail {
            background-color: #FF20001A;
            color: #FF2000;
            padding: 8px;
            border-radius: 50%;
            display: inline-flex;
            margin-right: 12px;
        }
        .icon-circle-pass {
            background-color: #dcfce7;
            color: #16a34a;
            padding: 8px;
            border-radius: 50%;
            display: inline-flex;
            margin-right: 12px;
        }
        .material-icons { font-size: 18px !important; vertical-align: middle; margin-right: 6px; }
    </style>
""", unsafe_allow_html=True)

st.title("Display Creative Inspector")
st.write("Upload display assets to automatically extract their metadata and validate network compliance (Max 150 KB, Max 30s animation).")

# File uploader
uploaded_files = st.file_uploader("Click to upload or drag & drop", type=["jpg", "jpeg", "png", "gif"], accept_multiple_files=True)

if uploaded_files:
    compliant_rows = []
    non_compliant_rows = []

    for file in uploaded_files:
        # Default tracking
        file_name = file.name
        status = "Pass"
        file_type = "-"
        size_str = "0"
        dimensions = "-"
        animation = "N/A"
        errors = []

        # 1. Size Check
        size_kb = file.size / 1024
        size_str = f"{size_kb:.2f} KB"
        if size_kb > 150:
            errors.append(f"Size ({size_kb:.2f} KB) > 150 KB")
            status = "Fail"

        # 2. Image Processing
        try:
            with Image.open(file) as img:
                file_type = img.format.upper()
                if file_type not in ['JPEG', 'PNG', 'GIF']:
                    errors.append(f"Invalid type ({file_type})")
                    status = "Fail"

                dimensions = f"{img.size[0]}x{img.size[1]}"

                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    duration_ms = 0
                    loop_count = img.info.get("loop", 1)
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        duration_ms += img.info.get('duration', 100)
                    
                    duration_sec = duration_ms / 1000.0
                    animation = f"{duration_sec:.1f}s"

                    if loop_count == 0:
                        errors.append("Infinite loop")
                        status = "Fail"
                    elif duration_sec > 30:
                        errors.append(f"Animation > 30s")
                        status = "Fail"
        except Exception:
            errors.append("Corrupted file")
            status = "Fail"

        # 3. Format Data for the Table (Flattened HTML to prevent Markdown code block rendering)
        type_class = "text-orange" if file_type not in ['JPEG', 'PNG', 'GIF'] else ""
        size_class = "text-orange" if size_kb > 150 else ""
        anim_class = "text-orange" if (status == "Fail" and ("Infinite" in str(errors) or "Animation >" in str(errors))) else ""
        
        if status == "Pass":
            status_icon = '<span class="material-icons" style="color: #16a34a;">check_circle</span> Pass'
            row_html = f"<tr><td class='text-left' style='max-width: 200px; word-wrap: break-word;'>{file_name}</td><td class='{type_class}'>{file_type}</td><td class='{size_class}'>{size_str}</td><td>{dimensions}</td><td class='{anim_class}'>{animation}</td><td>{status_icon}</td></tr>"
            compliant_rows.append(row_html)
        else:
            status_icon = '<span class="material-icons" style="color: #FF2000;">cancel</span> Fail'
            error_text = ", ".join(errors)
            row_html = f"<tr><td class='text-left' style='max-width: 200px; word-wrap: break-word;'>{file_name}</td><td colspan='4' class='text-orange'>{error_text}</td><td>{status_icon}</td></tr>"
            non_compliant_rows.append(row_html)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- RENDER NON-COMPLIANT TABLE ---
    if non_compliant_rows:
        st.markdown(
            '<div class="section-header"><div class="icon-circle-fail"><span class="material-icons" style="margin:0;">warning</span></div><h2>Non-compliant</h2></div>'
            '<p style="font-size: 14px; color: #4b5563; margin-bottom: 16px;">Review the highlighted properties and provide amended files. Display assets must be JPG/PNG/GIF, under 150KB, and animations must stop within 30 seconds.</p>'
            '<div class="custom-table-container"><table class="custom-table"><thead><tr>'
            '<th class="text-left"><span class="material-icons">insert_drive_file</span> File Name</th>'
            '<th><span class="material-icons">description</span> Details / Errors</th>'
            '<th><span class="material-icons">check_circle</span> Status</th>'
            '</tr></thead><tbody>' + "".join(non_compliant_rows) + '</tbody></table></div>', 
            unsafe_allow_html=True
        )

    # --- RENDER COMPLIANT TABLE ---
    if compliant_rows:
        st.markdown(
            '<div class="section-header"><div class="icon-circle-pass"><span class="material-icons" style="margin:0;">check</span></div><h2>Compliant</h2></div>'
            '<div class="custom-table-container"><table class="custom-table"><thead><tr>'
            '<th class="text-left"><span class="material-icons">insert_drive_file</span> File Name</th>'
            '<th><span class="material-icons">image</span> File Type</th>'
            '<th><span class="material-icons">sd_storage</span> File Size</th>'
            '<th><span class="material-icons">aspect_ratio</span> Dimensions</th>'
            '<th><span class="material-icons">timer</span> Animation</th>'
            '<th><span class="material-icons">check_circle</span> Status</th>'
            '</tr></thead><tbody>' + "".join(compliant_rows) + '</tbody></table></div>', 
            unsafe_allow_html=True
        )
