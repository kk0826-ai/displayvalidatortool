import streamlit as st
from PIL import Image

# 1. Page Config (E&lt;emoji&gt; ICON REMOVED, NEW TAB TITLE!)
st.set_page_config(page_title="Display Validator Tool", layout="wide")

# 2. Add your Header Image / Logo here
# st.image("path/to/image_6.png", use_container_width=True) # Replace with image_6.png file path
st.image("https://images.unsplash.com/photo-1549491630-f3b39c0e5a88?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTkyMXwwfDF8c2VhcmNofDEyfHxmaXJld29ya3N8ZW58MHx8fHwxNjQ4NDE4NjY4&ixlib=rb-1.2.1&q=80&w=1400", use_container_width=True) # Public example image
st.title("DISPLAY VALIDATOR TOOL")

# 3. Custom CSS for Pixel-Perfect UI
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Material+Icons&display=swap" rel="stylesheet">
    <style>
        /* Global typography and Material Icons */
        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif !important;
        }
        .material-icons {
            font-size: 18px !important;
            vertical-align: middle !important;
            margin-right: 6px !important;
        }

        /* --------------------------------------
           UPLOAD UI (Simplified & Clean Yellow)
           -------------------------------------- */
        
        /* 1. Target the main dropzone box */
        [data-testid="stFileUploadDropzone"] {
            background-color: #FDF9F1 !important; /* Pale yellow/beige */
            border: 2px dashed #D1D5DB !important; /* Crisp gray dashed border */
            border-radius: 4px; /* Slight rounding for a clean look */
            padding: 60px 20px !important; /* Large padding creates the outer box effect */
        }
        
        /* Hover effect on the box */
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #9CA3AF !important;
            background-color: #F9FAFB !important;
        }

        /* 2. Style the main text "Click to upload or drag & drop" */
        [data-testid="stFileUploadDropzone"] span {
            color: #4B5563 !important;
            font-size: 16px !important;
            font-weight: 400 !important;
        }

        /* 3. THE FIX: Hide the 200MB text completely */
        [data-testid="stFileUploadDropzone"] > div > small { 
            display: none !important; 
        }

        /* --------------------------------------
           POLISHED GRID TABLES (Spec/Dashboard style) 
           -------------------------------------- */
        
        /* Table section title ("Compliant", "Non-compliant") */
        .table-title {
            font-size: 22px;
            font-weight: 500;
            color: #111827;
            margin-top: 32px;
            margin-bottom: 12px;
        }

        /* Dashboard Table Structure with grid lines */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed; /* Rigid column sizing */
            margin-bottom: 2rem;
            background-color: #FFFFFF;
        }
        
        /* Table Headers: Uppercase, Bold, plum background, vertical dividers */
        .custom-table th {
            background-color: #2B0030; /* Dark plum from image_2.png */
            color: #FFFFFF;
            padding: 12px 16px;
            font-size: 12px; /* Small, clear font like a spec table */
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: center; /* Center-aligned for grid feel */
            border-right: 1px solid #4B5563; /* Vertical dividers */
        }
        .custom-table th:last-child { border-right: none; }

        /* Table Cells with vertical and horizontal dividers */
        .custom-table td {
            padding: 16px;
            font-size: 14px;
            color: #4B5563;
            text-align: center; /* Center-aligned for grid feel */
            border-right: 1px solid #E5E7EB; /* Light grey grid lines */
            border-bottom: 1px solid #E5E7EB;
            vertical-align: middle;
            word-wrap: break-word; /* Wrap long filenames */
        }
        .custom-table td:last-child { border-right: none; }
        .custom-table tbody tr:last-child td { border-bottom: none; }

        /* Hover effect on data rows */
        .custom-table tbody tr:hover {
            background-color: #F9FAFB;
        }

        /* Left-align text for specific data points like filename */
        .text-left { text-align: left !important; }

        /* Subtle even/odd row banding */
        .custom-table tbody tr:nth-child(even) td { background-color: rgba(43, 0, 48, 0.015); }

        /* Column Widths (Balanced for 7 columns) */
        .col-name { width: 25%; }
        .col-type { width: 10%; }
        .col-size { width: 10%; }
        .col-dim  { width: 15%; }
        .col-anim { width: 15%; }
        .col-rem  { width: 15%; }
        .col-stat { width: 10%; }

        /* Status badges and highlights (Red on red fail highlights) */
        .status-badge {
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 4px 10px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
        }
        .status-badge-pass { background-color: #DCFCE7; color: #166534; }
        .status-badge-fail { background-color: #FEE2E2; color: #991B1B; }
        
        .remarks-fail { color: #DC2626; font-weight: 500; font-size: 13px; }
        .cell-fail { background-color: rgba(220, 38, 38, 0.08) !important; color: #DC2626 !important; font-weight: 500; }
        
        /* Left-align Remarks text */
        .custom-table td.col-rem { text-align: left; }
    </style>
""", unsafe_allow_html=True)

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
        
        # Flags for red fail highlighting on specific cells
        fail_flags = {"type": False, "size": False, "anim": False}

        # 1. Size Check (150KB limit)
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
                # Type Check
                if file_type not in ['JPEG', 'PNG', 'GIF']:
                    errors.append("Invalid format")
                    status = "Fail"
                    fail_flags["type"] = True

                dimensions = f"{img.size[0]} × {img.size[1]}"

                # --- GIF LOGIC (30s limit) ---
                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    cycle_duration_ms = 0
                    
                    # Pillow -img.info.get("loop") - often 0 if infinite, fallback to 1 (plays once)
                    loop_count = img.info.get("loop", 1) 
                    
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        # The core fix: Sum the exact raw duration, do not apply fallbacks.
                        cycle_duration_ms += img.info.get('duration', 0)
                    
                    cycle_sec = cycle_duration_ms / 1000.0
                    
                    # 0 in the file means Infinite. Treat it as failure.
                    if loop_count == 0:
                        animation = f"∞ Infinite ({cycle_sec:.1f}s cycle)"
                        errors.append("Infinite loop")
                        status = "Fail"
                        fail_flags["anim"] = True
                    # A positive number is exact loops. Treat loop count as total plays.
                    elif loop_count > 0:
                        total_plays = loop_count
                        total_sec = cycle_sec * total_plays
                        animation = f"{total_sec:.1f}s ({cycle_sec:.1f}s × {total_plays})"
                        if total_sec > 30:
                            errors.append(f"Animation > 30s")
                            status = "Fail"
                            fail_flags["anim"] = True
                    # Treat `-1` or no specify as plays once (same as loop_count=1)
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

        # 3. Format UI Elements
        sc = "cell-fail" if fail_flags["size"] else ""
        ac = "cell-fail" if fail_flags["anim"] else ""
        tc = "cell-fail" if fail_flags["type"] else ""
        
        if status == "Pass":
            stat_html = "<span class='status-badge status-badge-pass'><span class='material-icons'>check</span> Pass</span>" 
            rem_html = "None"
            # Create a single row HTML string
            row_html = f"<tr><td class='text-left'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='col-rem'>{rem_html}</td><td>{stat_html}</td></tr>"
            compliant_rows.append(row_html)
        else:
            stat_html = "<span class='status-badge status-badge-fail'><span class='material-icons'>close</span> Fail</span>"
            rem_html = f"<div class='remarks-fail'>{'<br>'.join(errors)}</div>"
            
            # Special logic for Corrupted/Unreadable file to colspan across middle columns
            if "Corrupted" in str(errors) or "ERROR" == file_type:
                row_html = f"<tr><td class='text-left'>{file_name}</td><td colspan='4' class='text-left cell-fail' style='padding-left:16px;'>Unreadable File - Details not extracted</td><td class='col-rem'>{rem_html}</td><td>{stat_html}</td></tr>"
            else:
                row_html = f"<tr><td class='text-left'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='col-rem'>{rem_html}</td><td>{stat_html}</td></tr>"
            non_compliant_rows.append(row_html)

    # Polished Grid Table Headers with Icons and rigid column widths (based on image_2.png aesthetic)
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

    # Render Tables
    if non_compliant_rows:
        st.markdown('<div class="table-title">Non-compliant</div>', unsafe_allow_html=True)
        # Use single strings with raw table and join rows to prevent Streamlit from turning it into raw text
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table>', unsafe_allow_html=True)

    if compliant_rows:
        st.markdown('<div class="table-title">Compliant</div>', unsafe_allow_html=True)
        st.markdown(f'<table class="custom-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table>', unsafe_allow_html=True)
