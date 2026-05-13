import streamlit as st
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Creative Inspector", layout="wide")

# 2. Custom CSS for Pixel-Perfect UI
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Clean AdOps Tracker Header (No Emoji, Clean Line) */
        .app-header {
            font-size: 32px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #E5E7EB;
        }

        /* --------------------------------------
           UPLOAD UI (Matching your screenshot)
           -------------------------------------- */
        
        /* 1. The Outer Pale Yellow Box */
        [data-testid="stFileUploader"] {
            background-color: #FAF6EB !important; /* Pale yellow */
            padding: 30px !important;
        }

        /* 2. The Inner White Dashed Box */
        [data-testid="stFileUploadDropzone"] {
            background-color: #FFFFFF !important;
            border: 1.5px dashed #A1A1AA !important; /* Clean gray dashed border */
            border-radius: 0px !important; /* Sharp corners like screenshot */
            padding: 50px 20px !important;
        }
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #111827 !important;
        }

        /* 3. Hide the 200MB text completely */
        [data-testid="stFileUploadDropzone"] small { 
            display: none !important; 
        }

        /* Style the text inside the dropzone */
        [data-testid="stFileUploadDropzone"] span {
            color: #374151 !important;
            font-size: 15px !important;
            font-weight: 400 !important;
        }

        /* --------------------------------------
           HIGH-CONTRAST GRID TABLE 
           -------------------------------------- */
        
        .table-title {
            font-size: 22px;
            font-weight: 500;
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
            background-color: #0F172A; 
            color: #FFFFFF;
            padding: 14px 16px;
            font-size: 14px;
            font-weight: 500;
            text-align: left; 
            border: 1px solid #334155; 
        }

        .custom-table td {
            padding: 14px 16px;
            font-size: 14px;
            color: #374151;
            text-align: left; 
            border: 1px solid #E5E7EB; 
            vertical-align: top;
            word-wrap: break-word;
        }

        .custom-table tbody tr:hover {
            background-color: #F9FAFB;
        }

        /* Column Widths */
        .col-name { width: 25%; }
        .col-type { width: 10%; }
        .col-size { width: 10%; }
        .col-dim  { width: 15%; }
        .col-anim { width: 15%; }
        .col-rem  { width: 15%; }
        .col-stat { width: 10%; }

        /* Status Colors */
        .status-pass { color: #16A34A; font-weight: 500; }
        .status-fail { color: #DC2626; font-weight: 500; }
        .text-error { color: #DC2626; font-weight: 500; }
        .remarks-text { color: #6B7280; }
        .remarks-error { color: #DC2626; }
    </style>
""", unsafe_allow_html=True)

# 3. App Header
st.markdown('<div class="app-header">Display Creative Inspector</div>', unsafe_allow_html=True)

# 4. Upload UI
uploaded_files = st.file_uploader(
    "Click to upload or drag & drop", 
    type=["jpg", "jpeg", "png", "gif"], 
    accept_multiple_files=True,
    label_visibility="collapsed"
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

        # 1. Size Check
        size_kb = file.size / 1024
        size_str = f"{size_kb:.2f} KB"
        if size_kb > 150:
            errors.append("Size > 150 KB")
            status = "Fail"
            fail_flags["size"] = True

        # 2. Image Processing
        try:
            with Image.open(file) as img:
                file_type = img.format.upper()
                if file_type not in ['JPEG', 'PNG', 'GIF']:
                    errors.append("Invalid format")
                    status = "Fail"
                    fail_flags["type"] = True

                dimensions = f"{img.size[0]} × {img.size[1]}"

                # --- GIF LOGIC ---
                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    cycle_duration_ms = 0
                    loop_count = img.info.get("loop", -1) 
                    
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        frame_dur = img.info.get('duration', 100)
                        if frame_dur <= 10: 
                            frame_dur = 100
                        cycle_duration_ms += frame_dur
                    
                    cycle_sec = cycle_duration_ms / 1000.0
                    
                    if loop_count == 0:
                        animation = f"∞ Infinite"
                        errors.append("Infinite loop")
                        status = "Fail"
                        fail_flags["anim"] = True
                    elif loop_count > 0:
                        total_plays = loop_count
                        total_sec = cycle_sec * total_plays
                        animation = f"{total_sec:.1f}s"
                        if total_sec > 30:
                            errors.append("Animation > 30s")
                            status = "Fail"
                            fail_flags["anim"] = True
                    else:
                        animation = f"{cycle_sec:.1f}s"
                        if cycle_sec > 30:
                            errors.append("Animation > 30s")
                            status = "Fail"
                            fail_flags["anim"] = True
        except Exception:
            errors.append("Unreadable file")
            status = "Fail"
            file_type = "ERROR"
            fail_flags["type"] = True

        # 3. Format UI Elements
        sc = "text-error" if fail_flags["size"] else ""
        ac = "text-error" if fail_flags["anim"] else ""
        tc = "text-error" if fail_flags["type"] else ""
        
        if status == "Pass":
            stat_html = "<span class='status-pass'>On Track</span>" 
            rem_html = "<span class='remarks-text'>None</span>"
            row_html = f"<tr><td>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td>{rem_html}</td><td>{stat_html}</td></tr>"
            compliant_rows.append(row_html)
        else:
            stat_html = "<span class='status-fail'>Action Required</span>"
            rem_html = f"<div class='remarks-error'>{'<br>'.join(errors)}</div>"
            row_html = f"<tr><td>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td>{rem_html}</td><td>{stat_html}</td></tr>"
            non_compliant_rows.append(row_html)

    # Clean Grid Headers
    table_headers = """
        <thead>
            <tr>
                <th class="col-name">File Name</th>
                <th class="col-type">Format</th>
                <th class="col-size">File Size</th>
                <th class="col-dim">Dimensions</th>
                <th class="col-anim">Animation</th>
                <th class="col-rem">Remarks</th>
                <th class="col-stat">Status</th>
            </tr>
        </thead>
    """

    # Render Tables
    if non_compliant_rows:
        st.markdown('<div class="table-title">Non-compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table>', unsafe_allow_html=True)

    if compliant_rows:
        st.markdown('<div class="table-title">Compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table>', unsafe_allow_html=True)
