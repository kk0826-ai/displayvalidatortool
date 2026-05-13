import streamlit as st
import base64
import os
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Validator Tool", layout="wide")

# 2. Dynamic Image Background Banner Logic
def get_image_as_base64(file_path):
    try:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

# Load the image you uploaded
img_base64 = get_image_as_base64("vj-HZbu8-Imgur.jpg")

if img_base64:
    bg_style = f"background-image: url('data:image/jpeg;base64,{img_base64}');"
else:
    bg_style = "background-color: #111827;" # Dark fallback if image is missing

# Render the Banner
st.markdown(f"""
    <div style="
        {bg_style}
        background-size: cover;
        background-position: center;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: -1rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 0 0 2000px rgba(0, 0, 0, 0.4); /* Optional: Darkens image slightly so white text pops */
    ">
        <h1 style="color: #FFFFFF; font-size: 36px; font-weight: 600; font-family: 'Manrope', sans-serif; margin: 0; letter-spacing: 1px;">
            DISPLAY VALIDATOR TOOL
        </h1>
    </div>
""", unsafe_allow_html=True)

# 3. Custom CSS for Uploader and Tables
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Material+Icons&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif !important;
        }
        .material-icons {
            font-size: 18px !important;
            vertical-align: middle !important;
            margin-right: 6px !important;
        }

        /* --------------------------------------
           UPLOAD UI (Perfect Box-in-Box)
           -------------------------------------- */
        
        /* The Outer Pale Yellow/Beige Box */
        [data-testid="stFileUploader"] {
            background-color: #FDF9F1 !important; 
            padding: 30px !important; 
            border-radius: 4px;
        }

        /* The Inner White Dashed Box */
        [data-testid="stFileUploadDropzone"] {
            background-color: #FFFFFF !important;
            border: 2px dashed #D1D5DB !important; 
            border-radius: 0px !important; 
            padding: 50px 20px !important;
        }
        
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #9CA3AF !important;
            background-color: #F9FAFB !important;
        }

        /* HIDE THE 200MB TEXT */
        [data-testid="stFileUploader"] small, 
        [data-testid="stFileUploadDropzone"] small { 
            display: none !important; 
        }

        /* Hide the default label text above the uploader */
        .st-emotion-cache-16idsys p {
            display: none !important;
        }

        /* --------------------------------------
           POLISHED GRID TABLES
           -------------------------------------- */
        
        .table-title {
            font-size: 22px;
            font-weight: 600;
            color: #111827;
            margin-top: 32px;
            margin-bottom: 12px;
        }

        .custom-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            margin-bottom: 2rem;
            background-color: #FFFFFF;
        }
        
        .custom-table th {
            background-color: #2B0030; 
            color: #FFFFFF;
            padding: 12px 16px;
            font-size: 12px; 
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: center; 
            border-right: 1px solid #4B5563; 
        }
        .custom-table th:last-child { border-right: none; }

        .custom-table td {
            padding: 16px;
            font-size: 14px;
            color: #4B5563;
            text-align: center; 
            border-right: 1px solid #E5E7EB; 
            border-bottom: 1px solid #E5E7EB;
            vertical-align: middle;
            word-wrap: break-word; 
        }
        .custom-table td:last-child { border-right: none; }
        .custom-table tbody tr:last-child td { border-bottom: none; }

        .custom-table tbody tr:hover {
            background-color: #F9FAFB;
        }

        .text-left { text-align: left !important; }
        .custom-table tbody tr:nth-child(even) td { background-color: rgba(43, 0, 48, 0.015); }

        .col-name { width: 25%; }
        .col-type { width: 10%; }
        .col-size { width: 10%; }
        .col-dim  { width: 15%; }
        .col-anim { width: 15%; }
        .col-rem  { width: 15%; }
        .col-stat { width: 10%; }

        .status-badge {
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 5px 10px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
        }
        .status-badge-pass { background-color: #DCFCE7; color: #166534; }
        .status-badge-fail { background-color: #FEE2E2; color: #991B1B; }
        
        .remarks-fail { color: #DC2626; font-weight: 600; font-size: 13px; }
        .cell-fail { background-color: rgba(220, 38, 38, 0.08) !important; color: #DC2626 !important; font-weight: 600; }
        .custom-table td.col-rem { text-align: left; }
    </style>
""", unsafe_allow_html=True)

# 4. Upload UI (Space trick to force dropzone without showing text)
uploaded_files = st.file_uploader(
    " ", 
    type=["jpg", "jpeg", "png", "gif"], 
    accept_multiple_files=True
)

if uploaded_files:
    compliant_rows = []
    non_compliant_rows = []

    for file in uploaded_files:
        file_name = file.name
        status = "Pass"
        file_type = "-"
        size_str = "0"
        dimensions = "-"
        animation = "-"
        errors = []
        fail_flags = {"type": False, "size": False, "anim": False}

        size_kb = file.size / 1024
        size_str = f"{size_kb:.2f} KB"
        if size_kb > 150:
            errors.append("Size > 150 KB")
            status = "Fail"
            fail_flags["size"] = True

        try:
            with Image.open(file) as img:
                file_type = img.format.upper()
                if file_type not in ['JPEG', 'PNG', 'GIF']:
                    errors.append("Invalid format")
                    status = "Fail"
                    fail_flags["type"] = True

                dimensions = f"{img.size[0]} × {img.size[1]}"

                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    cycle_duration_ms = 0
                    loop_count = img.info.get("loop", 1) 
                    
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        cycle_duration_ms += img.info.get('duration', 0)
                    
                    cycle_sec = cycle_duration_ms / 1000.0
                    
                    if loop_count == 0:
                        animation = f"∞ Infinite ({cycle_sec:.1f}s cycle)"
                        errors.append("Infinite loop")
                        status = "Fail"
                        fail_flags["anim"] = True
                    elif loop_count > 0:
                        total_plays = loop_count
                        total_sec = cycle_sec * total_plays
                        animation = f"{total_sec:.1f}s ({cycle_sec:.1f}s × {total_plays})"
                        if total_sec > 30:
                            errors.append(f"Animation > 30s")
                            status = "Fail"
                            fail_flags["anim"] = True
                    else:
                        animation = f"{cycle_sec:.1f}s"
                        if cycle_sec > 30:
                            errors.append(f"Animation > 30s")
                            status = "Fail"
                            fail_flags["anim"] = True
        except Exception:
            errors.append("Corrupted file or unreadable")
            status = "Fail"
            file_type = "ERROR"
            fail_flags["type"] = True

        sc = "cell-fail" if fail_flags["size"] else ""
        ac = "cell-fail" if fail_flags["anim"] else ""
        tc = "cell-fail" if fail_flags["type"] else ""
        
        if status == "Pass":
            stat_html = "<span class='status-badge status-badge-pass'><span class='material-icons'>check</span> Pass</span>" 
            rem_html = "None"
            row_html = f"<tr><td class='text-left'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='col-rem'>{rem_html}</td><td>{stat_html}</td></tr>"
            compliant_rows.append(row_html)
        else:
            stat_html = "<span class='status-badge status-badge-fail'><span class='material-icons'>close</span> Fail</span>"
            rem_html = f"<div class='remarks-fail'>{'<br>'.join(errors)}</div>"
            
            if "Corrupted" in str(errors) or "ERROR" == file_type:
                row_html = f"<tr><td class='text-left'>{file_name}</td><td colspan='4' class='text-left cell-fail' style='padding-left:16px;'>Unreadable File - Details not extracted</td><td class='col-rem'>{rem_html}</td><td>{stat_html}</td></tr>"
            else:
                row_html = f"<tr><td class='text-left'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='col-rem'>{rem_html}</td><td>{stat_html}</td></tr>"
            non_compliant_rows.append(row_html)

    table_headers = """
        <thead>
            <tr>
                <th class="col-name text-left"><span class="material-icons">insert_drive_file</span>File Name</th>
                <th class="col-type"><span class="material-icons">description</span>File Type</th>
                <th class="col-size"><span class="material-icons">sd_storage</span>File Size</th>
                <th class="col-dim"><span class="material-icons">aspect_ratio</span>Dimensions</th>
                <th class="col-anim"><span class="material-icons">timer</span>Animation</th>
                <th class="col-rem"><span class="material-icons">rule</span>Remarks</th>
                <th class="col-stat"><span class="material-icons">check_circle</span>Status</th>
            </tr>
        </thead>
    """

    if non_compliant_rows:
        st.markdown('<div class="table-title">Non-compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table>', unsafe_allow_html=True)

    if compliant_rows:
        st.markdown('<div class="table-title">Compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table>', unsafe_allow_html=True)
