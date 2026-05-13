import streamlit as st
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Creative Inspector", page_icon="🎨", layout="wide")

# 2. Ultra-Modern SaaS CSS
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Global Font Upgrade */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Modern App Header */
        .app-header {
            font-size: 28px;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
        }
        .app-subheader {
            font-size: 15px;
            color: #64748B;
            margin-bottom: 32px;
        }

        /* Sleek Upload Dropzone */
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #CBD5E1 !important;
            border-radius: 16px !important;
            background-color: #F8FAFC !important;
            padding: 48px 24px !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #6366F1 !important;
            background-color: #EEF2FF !important;
        }
        
        /* Hide the default "Limit 200MB per file" text for a cleaner look */
        [data-testid="stFileUploadDropzone"] small { display: none; }

        /* Modern Table Container */
        .modern-table-container {
            width: 100%;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            overflow: hidden;
            margin-bottom: 2rem;
        }

        /* Table Structure & Alignment */
        .modern-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        
        .modern-table thead {
            background-color: #F8FAFC;
            border-bottom: 1px solid #E2E8F0;
        }

        /* Perfect Header Centering */
        .modern-table th {
            padding: 16px 12px;
            font-size: 12px;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: center; /* CENTER ALIGNED */
        }
        .modern-table th.align-left {
            text-align: left; /* ONLY File Name & Remarks left-aligned */
        }

        /* Perfect Data Centering */
        .modern-table td {
            padding: 16px 12px;
            font-size: 14px;
            color: #334155;
            border-bottom: 1px solid #F1F5F9;
            vertical-align: middle;
            text-align: center; /* CENTER ALIGNED */
            word-wrap: break-word;
        }
        .modern-table td.align-left {
            text-align: left;
            font-weight: 500;
            color: #0F172A;
        }

        /* Hover Effects */
        .modern-table tbody tr:hover {
            background-color: #F8FAFC;
        }
        .modern-table tbody tr:last-child td {
            border-bottom: none;
        }

        /* Sleek Pill Badges */
        .badge-pass {
            background: #DCFCE7;
            color: #166534;
            padding: 6px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 12px;
            display: inline-block;
        }
        .badge-fail {
            background: #FEE2E2;
            color: #991B1B;
            padding: 6px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 12px;
            display: inline-block;
        }
        .badge-type {
            background: #F1F5F9;
            color: #475569;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }

        /* Text Highlighting */
        .text-error { color: #DC2626; font-weight: 600; }
        .remarks-text { font-size: 13px; color: #475569; }
        .remarks-error { font-size: 13px; color: #DC2626; font-weight: 500; }

        /* Column Widths */
        .col-name { width: 25%; }
        .col-type { width: 10%; }
        .col-size { width: 12%; }
        .col-dim  { width: 15%; }
        .col-anim { width: 15%; }
        .col-rem  { width: 13%; }
        .col-stat { width: 10%; }
    </style>
""", unsafe_allow_html=True)

# 3. Clean Header
st.markdown('<div class="app-header">Display Creative Inspector</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subheader">Validate network compliance (Max 150 KB, Max 30s animation).</div>', unsafe_allow_html=True)

# 4. Upload UI
uploaded_files = st.file_uploader(
    "Click to browse or drag & drop creatives below", 
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
        type_badge = f"<span class='badge-type'>{file_type}</span>"
        sc = "text-error" if fail_flags["size"] else ""
        ac = "text-error" if fail_flags["anim"] else ""
        
        if status == "Pass":
            stat_badge = "<span class='badge-pass'>Compliant</span>"
            rem_html = "<span class='remarks-text'>None</span>"
            row_html = f"<tr><td class='align-left'>{file_name}</td><td>{type_badge}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='align-left'>{rem_html}</td><td>{stat_badge}</td></tr>"
            compliant_rows.append(row_html)
        else:
            stat_badge = "<span class='badge-fail'>Action Required</span>"
            rem_html = f"<div class='remarks-error'>{'<br>'.join(errors)}</div>"
            row_html = f"<tr><td class='align-left'>{file_name}</td><td>{type_badge}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='align-left'>{rem_html}</td><td>{stat_badge}</td></tr>"
            non_compliant_rows.append(row_html)

    # Reusable Table Headers
    table_headers = """
        <thead>
            <tr>
                <th class="col-name align-left">File Name</th>
                <th class="col-type">Format</th>
                <th class="col-size">File Size</th>
                <th class="col-dim">Dimensions</th>
                <th class="col-anim">Animation</th>
                <th class="col-rem align-left">Remarks</th>
                <th class="col-stat">Status</th>
            </tr>
        </thead>
    """

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Tables
    if non_compliant_rows:
        st.markdown(
            f'<div class="modern-table-container"><table class="modern-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table></div>', 
            unsafe_allow_html=True
        )

    if compliant_rows:
        st.markdown(
            f'<div class="modern-table-container"><table class="modern-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table></div>', 
            unsafe_allow_html=True
        )
