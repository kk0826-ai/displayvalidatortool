import streamlit as st
from PIL import Image

st.set_page_config(page_title="Display Creative Inspector", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Manrope:400,500,600,700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Global Typography */
        html, body, [class*="css"] { font-family: 'Manrope', sans-serif !important; }
        
        /* Premium File Uploader UI */
        [data-testid="stFileUploadDropzone"] { 
            background-color: #FFCA011A !important; 
            border: 2px dashed #CBD5E1 !important; 
            border-radius: 12px; 
            padding: 50px 20px !important; 
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stFileUploadDropzone"]:hover { 
            background-color: #FFCA0133 !important; 
            border-color: #94A3B8 !important;
        }
        
        /* Clean Table Container with Shadow */
        .custom-table-container { 
            width: 100%; 
            border: 1px solid #E2E8F0; 
            border-radius: 8px; 
            margin-bottom: 2.5rem; 
            background-color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            overflow: hidden; /* Keeps the rounded corners sharp */
        }
        
        /* Rigid Table Layout */
        .custom-table { 
            width: 100%; 
            border-collapse: collapse; 
            table-layout: fixed; /* STRICT COLUMN SIZING */
            text-align: center; 
            font-size: 14px; 
        }
        
        /* Column Width Definitions */
        .col-name { width: 26%; text-align: left; }
        .col-type { width: 10%; }
        .col-size { width: 12%; }
        .col-dim  { width: 14%; }
        .col-anim { width: 14%; }
        .col-rem  { width: 14%; text-align: left; }
        .col-stat { width: 10%; }

        /* Headers */
        .custom-table th { 
            background-color: #2B0030; 
            color: white; 
            padding: 16px 12px; 
            font-weight: 600; 
            text-transform: uppercase; 
            font-size: 12px; 
            letter-spacing: 0.05em; 
            border-bottom: 2px solid #1a001d;
        }
        
        /* Rows and Cells */
        .custom-table td { 
            padding: 16px 12px; 
            border-bottom: 1px solid #F1F5F9; 
            color: #334155; 
            vertical-align: middle;
            word-wrap: break-word; /* Prevents long file names from breaking the table */
        }
        .custom-table tbody tr:nth-child(even) { background-color: #F8FAFC; }
        .custom-table tbody tr:hover { background-color: #F1F5F9; } /* Hover effect for rows */
        
        /* Highlighting and Status Badges */
        .cell-fail { background-color: #FEF2F2 !important; color: #DC2626 !important; font-weight: 700; }
        .remarks-fail { color: #DC2626; font-size: 13px; font-weight: 600; text-align: left; line-height: 1.4;}
        
        /* Section Headers */
        .section-header { display: flex; align-items: center; margin-bottom: 0.75rem; font-size: 15px; font-weight: 700; color: #1E293B; }
        .icon-circle-fail { background-color: #FEF2F2; color: #DC2626; padding: 6px; border-radius: 50%; display: inline-flex; margin-right: 10px; }
        .icon-circle-pass { background-color: #DCFCE7; color: #16A34A; padding: 6px; border-radius: 50%; display: inline-flex; margin-right: 10px; }
        .material-icons { font-size: 18px !important; vertical-align: middle; margin-right: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("Display Creative Inspector")
st.write("Upload display assets to automatically extract their metadata and validate network compliance (Max 150 KB, Max 30s animation).")

uploaded_files = st.file_uploader("Click to upload or drag & drop", type=["jpg", "jpeg", "png", "gif"], accept_multiple_files=True)

if uploaded_files:
    compliant_rows = []
    non_compliant_rows = []

    for file in uploaded_files:
        file_name = file.name
        status = "Pass"
        file_type = "-"
        size_str = "0"
        dimensions = "-"
        animation = "N/A"
        errors = []
        
        fail_flags = {"type": False, "size": False, "anim": False}

        # 1. Size Check
        size_kb = file.size / 1024
        size_str = f"{size_kb:.2f} KB"
        if size_kb > 150:
            errors.append(f"Size > 150 KB")
            status = "Fail"
            fail_flags["size"] = True

        # 2. Image Processing
        try:
            with Image.open(file) as img:
                file_type = img.format.upper()
                if file_type not in ['JPEG', 'PNG', 'GIF']:
                    errors.append(f"Invalid format")
                    status = "Fail"
                    fail_flags["type"] = True

                dimensions = f"{img.size[0]}x{img.size[1]}"

                # --- GIF LOGIC (Loop Count as Total Plays) ---
                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    cycle_duration_ms = 0
                    loop_count = img.info.get("loop", -1) 
                    
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
            errors.append("Corrupted file")
            status = "Fail"
            fail_flags["type"] = True

        # 3. Apply Classes
        tc = "col-type cell-fail" if fail_flags["type"] else "col-type"
        sc = "col-size cell-fail" if fail_flags["size"] else "col-size"
        ac = "col-anim cell-fail" if fail_flags["anim"] else "col-anim"
        
        if status == "Pass":
            status_icon = '<span class="material-icons" style="color: #16A34A;">check_circle</span> Pass'
            remarks = '<span style="color: #16A34A; font-weight: 500;">Compliant</span>'
            row_html = f"<tr><td class='col-name'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td class='col-dim'>{dimensions}</td><td class='{ac}'>{animation}</td><td class='col-rem'>{remarks}</td><td class='col-stat'>{status_icon}</td></tr>"
            compliant_rows.append(row_html)
        else:
            status_icon = '<span class="material-icons" style="color: #DC2626;">cancel</span> Fail'
            remarks = f"<div class='remarks-fail'>{'<br>• '.join([''] + errors)}</div>"
            
            if "Corrupted file" in str(errors):
                 row_html = f"<tr><td class='col-name'>{file_name}</td><td colspan='4' class='cell-fail' style='text-align: center;'>Unreadable File</td><td class='col-rem'>{remarks}</td><td class='col-stat'>{status_icon}</td></tr>"
            else:
                 row_html = f"<tr><td class='col-name'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td class='col-dim'>{dimensions}</td><td class='{ac}'>{animation}</td><td class='col-rem'>{remarks}</td><td class='col-stat'>{status_icon}</td></tr>"
            
            non_compliant_rows.append(row_html)

    st.markdown("<br>", unsafe_allow_html=True)

    # Reusable Table HTML String with Column Classes attached to Headers
    table_headers = """
        <thead>
            <tr>
                <th class="col-name"><span class="material-icons">insert_drive_file</span> File Name</th>
                <th class="col-type"><span class="material-icons">image</span> Type</th>
                <th class="col-size"><span class="material-icons">sd_storage</span> Size</th>
                <th class="col-dim"><span class="material-icons">aspect_ratio</span> Dimensions</th>
                <th class="col-anim"><span class="material-icons">timer</span> Animation</th>
                <th class="col-rem"><span class="material-icons">rule</span> Remarks</th>
                <th class="col-stat"><span class="material-icons">check_circle</span> Status</th>
            </tr>
        </thead>
    """

    if non_compliant_rows:
        st.markdown(
            f'<div class="section-header"><div class="icon-circle-fail"><span class="material-icons" style="margin:0;">warning</span></div><h2>Non-compliant</h2></div>'
            f'<div class="custom-table-container"><table class="custom-table">{table_headers}<tbody>' + "".join(non_compliant_rows) + '</tbody></table></div>', 
            unsafe_allow_html=True
        )

    if compliant_rows:
        st.markdown(
            f'<div class="section-header"><div class="icon-circle-pass"><span class="material-icons" style="margin:0;">check</span></div><h2>Compliant</h2></div>'
            f'<div class="custom-table-container"><table class="custom-table">{table_headers}<tbody>' + "".join(compliant_rows) + '</tbody></table></div>', 
            unsafe_allow_html=True
        )
