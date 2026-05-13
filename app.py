import streamlit as st
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Validator Tool", layout="wide")

# 2. Compact Header Banner
header_image_url = "https://i.ibb.co/nMTJF4B9/vj-HZbu8-Imgur.jpg"

st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <div style="
        background-image: url('{header_image_url}');
        background-size: cover;
        background-position: center;
        height: 75px; 
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: -1rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 0 0 2000px rgba(0, 0, 0, 0.4);
        border-radius: 4px;
    ">
        <h1 style="color: #FFFFFF; font-size: 28px; font-weight: 800; font-family: 'Manrope', sans-serif; margin: 0; letter-spacing: 1px;">
            DISPLAY VALIDATOR TOOL
        </h1>
    </div>
""", unsafe_allow_html=True)

# 3. CSS Updates
st.markdown("""
    <style>
        /* Global Font */
        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif !important;
        }

        /* --------------------------------------
           UPLOADER TEXT HACKS
           -------------------------------------- */
        
        /* 1. Target the exact class you found in the inspector */
        .st-emotion-cache-epvm6 {
            display: none !important;
        }
        
        /* 2. Fallback to ensure any 'small' sub-text in the dropzone is hidden */
        [data-testid="stFileUploadDropzoneInstructions"] small {
            display: none !important;
        }

        /* Clean up the new label we are about to make visible */
        .stFileUploader label p {
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #111827 !important;
        }

        /* --------------------------------------
           CLEAN DASHBOARD TABLE STYLING 
           -------------------------------------- */
        .table-title {
            font-size: 20px;
            font-weight: 700;
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
            padding: 12px 16px;
            font-size: 13px; 
            font-weight: 600;
            text-align: left; 
            border: 1px solid #334155; 
        }

        .custom-table td {
            padding: 12px 16px;
            font-size: 14px;
            color: #111827;
            border: 1px solid #E5E7EB; 
            vertical-align: top;
            word-wrap: break-word; 
        }

        .custom-table tbody tr:nth-child(even) {
            background-color: #F9FAFB;
        }

        .col-name { width: 25%; }
        .col-type { width: 10%; }
        .col-size { width: 10%; }
        .col-dim  { width: 15%; }
        .col-anim { width: 15%; }
        .col-rem   { width: 15%; }
        .col-stat { width: 10%; }

        .status-pass { color: #16A34A; font-weight: 600; }
        .status-fail { color: #DC2626; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 4. Standard Streamlit Upload Dropzone
# Implementing your idea: Make the label visible and add the text directly here!
uploaded_files = st.file_uploader(
    "Upload Creatives (JPG, PNG, GIF) — Drag & drop below or click 'Browse files'", 
    type=["jpg", "jpeg", "png", "gif"], 
    accept_multiple_files=True,
    label_visibility="visible" # Changed from collapsed to visible
)

if uploaded_files:
    compliant_rows = []
    non_compliant_rows = []

    for file in uploaded_files:
        file_name = file.name
        status = "Pass"
        file_type = "-"
        size_str = f"{file.size / 1024:.2f} KB"
        dimensions = "-"
        animation = "-"
        errors = []

        if (file.size / 1024) > 150:
            errors.append("Size > 150 KB")
            status = "Fail"

        try:
            with Image.open(file) as img:
                file_type = img.format.upper()
                dimensions = f"{img.size[0]} × {img.size[1]}"
                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    duration = sum(img.info.get('duration', 0) for _ in range(img.n_frames)) / 1000
                    animation = f"{duration:.1f}s"
                    if duration > 30:
                        errors.append("Animation > 30s")
                        status = "Fail"
        except:
            status = "Fail"
            errors.append("Unreadable")

        stat_html = f"<span class='{'status-pass' if status=='Pass' else 'status-fail'}'>{'On Track' if status=='Pass' else 'Action Required'}</span>"
        rem_html = "None" if status == "Pass" else f"<span class='status-fail'>{' • '.join(errors)}</span>"
        
        row_html = f"<tr><td>{file_name}</td><td>{file_type}</td><td>{size_str}</td><td>{dimensions}</td><td>{animation}</td><td>{rem_html}</td><td>{stat_html}</td></tr>"
        
        if status == "Pass":
            compliant_rows.append(row_html)
        else:
            non_compliant_rows.append(row_html)

    table_headers = "<thead><tr><th class='col-name'>File Name</th><th class='col-type'>Format</th><th class='col-size'>File Size</th><th class='col-dim'>Dimensions</th><th class='col-anim'>Animation</th><th class='col-rem'>Remarks</th><th class='col-stat'>Status</th></tr></thead>"

    if non_compliant_rows:
        st.markdown('<div class="table-title">Non-compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table>', unsafe_allow_html=True)

    if compliant_rows:
        st.markdown('<div class="table-title">Compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table>', unsafe_allow_html=True)
