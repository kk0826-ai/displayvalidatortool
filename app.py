import streamlit as st
from PIL import Image

st.set_page_config(page_title="Display Creative Inspector", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Manrope:400,500,600,700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Manrope', sans-serif !important; }
        [data-testid="stFileUploadDropzone"] { background-color: #FFCA011A !important; border: 2px dashed #d1d5db !important; border-radius: 8px; padding: 40px !important; }
        [data-testid="stFileUploadDropzone"]:hover { background-color: #FFCA0133 !important; }
        
        /* Table Styles */
        .custom-table-container { width: 100%; overflow-x: auto; border: 1px solid #e5e7eb; border-radius: 4px; margin-bottom: 2rem; background-color: white; }
        .custom-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 14px; }
        .custom-table th { background-color: #2B0030; color: white; padding: 12px 16px; font-weight: 700; text-transform: uppercase; font-size: 12px; letter-spacing: 0.05em; }
        .custom-table td { padding: 16px; border-top: 1px solid #e5e7eb; color: #4b5563; vertical-align: middle;}
        .custom-table tbody tr:nth-child(even) { background-color: rgba(43, 0, 48, 0.02); }
        
        /* Highlighting Classes */
        .text-left { text-align: left; }
        .cell-fail { background-color: #FF20001A; color: #FF2000; font-weight: 700; border-radius: 4px; }
        .remarks-fail { color: #FF2000; font-size: 13px; font-weight: 600; text-align: left;}
        
        /* Headers */
        .section-header { display: flex; align-items: center; margin-bottom: 1rem; font-size: 14px; font-weight: 600; color: #4b5563; }
        .icon-circle-fail { background-color: #FF20001A; color: #FF2000; padding: 8px; border-radius: 50%; display: inline-flex; margin-right: 12px; }
        .icon-circle-pass { background-color: #dcfce7; color: #16a34a; padding: 8px; border-radius: 50%; display: inline-flex; margin-right: 12px; }
        .material-icons { font-size: 18px !important; vertical-align: middle; margin-right: 6px; }
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
        
        # Track which specific cells failed for highlighting
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

                # --- UPGRADED GIF LOGIC ---
                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    cycle_duration_ms = 0
                    
                    # -1 usually means no loop specified (plays once). 0 means infinite.
                    loop_count = img.info.get("loop", -1) 
                    
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        # Pillow sometimes returns 0 if the duration isn't set, fallback to 100
                        frame_dur = img.info.get('duration', 100) 
                        
                        # THE FIX: Only penalize frames 10ms or less. 
                        # 20ms (50 FPS) is a perfectly valid speed for smooth display ads!
                        if frame_dur <= 10: 
                            frame_dur = 100
                            
                        cycle_duration_ms += frame_dur
                    
                    cycle_sec = cycle_duration_ms / 1000.0
                    
                    if loop_count == 0:
                        animation = f"Infinite Loop ({cycle_sec:.1f}s cycle)"
                        errors.append("Infinite loop")
                        status = "Fail"
                        fail_flags["anim"] = True
                    else:
                        # If loop_count is 2, it repeats 2 times (plays 3 times total)
                        total_plays = (loop_count + 1) if loop_count > 0 else 1
                        total_sec = cycle_sec * total_plays
                        animation = f"{total_sec:.1f}s"
                        
                        if total_sec > 30:
                            errors.append("Animation > 30s")
                            status = "Fail"
                            fail_flags["anim"] = True
        except Exception:
            errors.append("Corrupted file")
            status = "Fail"
            fail_flags["type"] = True

        # 3. Format Cell Classes based on flags
        tc = "cell-fail" if fail_flags["type"] else ""
        sc = "cell-fail" if fail_flags["size"] else ""
        ac = "cell-fail" if fail_flags["anim"] else ""
        
        if status == "Pass":
            status_icon = '<span class="material-icons" style="color: #16a34a;">check_circle</span> Pass'
            remarks = '<span style="color: #16a34a;">Compliant</span>'
            row_html = f"<tr><td class='text-left' style='max-width: 180px; word-wrap: break-word;'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='text-left'>{remarks}</td><td>{status_icon}</td></tr>"
            compliant_rows.append(row_html)
        else:
            status_icon = '<span class="material-icons" style="color: #FF2000;">cancel</span> Fail'
            remarks = f"<div class='remarks-fail'>{'<br>• '.join([''] + errors)}</div>"
            
            if "Corrupted file" in str(errors):
                 row_html = f"<tr><td class='text-left' style='max-width: 180px; word-wrap: break-word;'>{file_name}</td><td colspan='4' class='cell-fail'>Unreadable File</td><td class='text-left'>{remarks}</td><td>{status_icon}</td></tr>"
            else:
                 row_html = f"<tr><td class='text-left' style='max-width: 180px; word-wrap: break-word;'>{file_name}</td><td class='{tc}'>{file_type}</td><td class='{sc}'>{size_str}</td><td>{dimensions}</td><td class='{ac}'>{animation}</td><td class='text-left'>{remarks}</td><td>{status_icon}</td></tr>"
            
            non_compliant_rows.append(row_html)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Reusable Table HTML String
    table_headers = '<thead><tr><th class="text-left"><span class="material-icons">insert_drive_file</span> File Name</th><th><span class="material-icons">image</span> Type</th><th><span class="material-icons">sd_storage</span> Size</th><th><span class="material-icons">aspect_ratio</span> Dimensions</th><th><span class="material-icons">timer</span> Animation</th><th class="text-left"><span class="material-icons">rule</span> Remarks</th><th><span class="material-icons">check_circle</span> Status</th></tr></thead>'

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
