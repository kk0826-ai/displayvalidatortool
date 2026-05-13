import streamlit as st
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Validator Tool", layout="wide")

# 2. Header with Background Image from URL
header_image_url = "https://i.ibb.co/nMTJF4B9/vj-HZbu8-Imgur.jpg"

st.markdown(f"""
    <div style="
        background-image: url('{header_image_url}');
        background-size: cover;
        background-position: center;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: -1rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 0 0 2000px rgba(0, 0, 0, 0.3);
        border-radius: 4px;
    ">
        <h1 style="color: #FFFFFF; font-size: 36px; font-weight: 700; font-family: 'Manrope', sans-serif; margin: 0; letter-spacing: 1.5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            DISPLAY VALIDATOR TOOL
        </h1>
    </div>
""", unsafe_allow_html=True)

# 3. Custom CSS for UI Components
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
           UPLOAD UI (Classic Box-in-Box Style)
           -------------------------------------- */
        
        /* The Outer Pale Yellow/Beige Container */
        [data-testid="stFileUploader"] {
            background-color: #FDF9F1 !important; 
            padding: 30px !important; 
            border-radius: 4px;
            margin-bottom: 2rem;
        }

        /* The Inner White Dashed Dropzone */
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

        /* HIDE THE 200MB AND TYPE LIMIT TEXT */
        [data-testid="stFileUploader"] small { 
            display: none !important; 
        }
        
        /* Hide the top "Drag and drop file here" label for a cleaner look */
        .st-emotion-cache-16idsys p {
            display: none !important;
        }

        /* --------------------------------------
           HIGH-CONTRAST DASHBOARD TABLE
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
        
        /* Dark Header Matching "Summary" Screenshot */
        .custom-table th {
            background-color: #0F172A; 
            color: #FFFFFF;
            padding: 14px 16px;
            font-size: 13px; 
            font-weight: 600;
            text-align: left; 
            border: 1px solid #334155; 
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .custom-table td {
            padding: 14px 16px;
            font-size: 14px;
            color: #374151;
            text-align: left; 
            border: 1px solid #E5E7EB; 
            vertical-align: middle;
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
        .status-pass { color: #16A34A; font-weight: 600; }
        .status-fail { color: #DC2626; font-weight: 600; }
        .cell-fail { background-color: #FEF2F2 !important; color: #DC2626 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. Upload UI
uploaded_files = st.file_uploader(
    "Upload Files", 
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

        # Size Check
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
                        animation = f"∞ Infinite ({cycle_sec:.1f}s)"
                        errors.append("Infinite loop")
                        status = "Fail"
                        fail_flags["anim"] = True
                    elif loop_count > 0:
                        total_plays = loop_count
                        total_sec = cycle_sec * total_plays
                        animation = f"{total_sec:.1f}s"
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
            errors.append("Corrupted or unreadable")
            status = "Fail"
            file_type = "ERROR"
            fail_flags["type"] = True

        sc = "cell-fail" if fail_flags["size"] else ""
        ac = "cell-fail" if fail_flags["anim"] else ""
        tc = "cell-fail" if fail_flags["type"] else ""
        
        if status == "Pass":
            stat_html = "<span class='status-pass'>On Track</span>" 
            rem_html = "Compliant"
            row_html = f"<tr><td>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td>{rem_html}</td><td>{stat_html}</td></tr>"
            compliant_rows.append(row_html)
        else:
            stat_html = "<span class='status-fail'>Action Required</span>"
            rem_html = f"<span class='status-fail'>{' • '.join(errors)}</span>"
            row_html = f"<tr><td>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td>{rem_html}</td><td>{stat_html}</td></tr>"
            non_compliant_rows.append(row_html)

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

    if non_compliant_rows:
        st.markdown('<div class="table-title">Non-compliant Assets</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table>', unsafe_allow_html=True)

    if compliant_rows:
        st.markdown('<div class="table-title">Compliant Assets</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table>', unsafe_allow_html=True)
