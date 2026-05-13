import streamlit as st
import pandas as pd
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Display Creative Inspector", page_icon="🎨", layout="wide")

# 2. Sleek Custom CSS for Native Streamlit Components
st.markdown("""
    <style>
        /* Modern App-Style Header */
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E293B;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #E2E8F0;
            margin-bottom: 1.5rem;
        }
        
        /* Fix Streamlit's default padding at the top */
        .block-container {
            padding-top: 2.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# 3. The New Header (Removed the extra text as requested)
st.markdown('<div class="main-header">🎨 Display Creative Inspector</div>', unsafe_allow_html=True)

# 4. Improved Native Upload UI
st.markdown("##### 📤 Upload Files")
uploaded_files = st.file_uploader(
    "Click to browse or drag & drop creatives below", 
    type=["jpg", "jpeg", "png", "gif"], 
    accept_multiple_files=True, 
    label_visibility="collapsed"
)

if uploaded_files:
    results = []

    for file in uploaded_files:
        file_name = file.name
        status = "✅ Pass"
        file_type = "-"
        size_str = "0"
        dimensions = "-"
        animation = "N/A"
        remarks = "Compliant"
        errors = []

        # 1. Size Check
        size_kb = file.size / 1024
        size_str = f"{size_kb:.2f} KB"
        if size_kb > 150:
            errors.append("Size > 150 KB")

        # 2. Image Processing
        try:
            with Image.open(file) as img:
                file_type = img.format.upper()
                if file_type not in ['JPEG', 'PNG', 'GIF']:
                    errors.append("Invalid Format")

                dimensions = f"{img.size[0]}x{img.size[1]}"

                # --- GIF LOGIC ---
                if file_type == 'GIF' and getattr(img, "is_animated", False):
                    cycle_duration_ms = 0
                    loop_count = img.info.get("loop", -1) 
                    
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        cycle_duration_ms += img.info.get('duration', 0)
                    
                    cycle_sec = cycle_duration_ms / 1000.0
                    
                    if loop_count == 0:
                        animation = f"∞ ({cycle_sec:.1f}s cycle)"
                        errors.append("Infinite Loop")
                    elif loop_count > 0:
                        total_plays = loop_count
                        total_sec = cycle_sec * total_plays
                        animation = f"{total_sec:.1f}s ({cycle_sec:.1f}s × {total_plays})"
                        if total_sec > 30:
                            errors.append("Animation > 30s")
                    else:
                        animation = f"{cycle_sec:.1f}s"
                        if cycle_sec > 30:
                            errors.append("Animation > 30s")
        except Exception:
            errors.append("Unreadable File")
            file_type = "ERROR"

        # Determine Final Status
        if errors:
            status = "❌ Fail"
            remarks = " • ".join(errors)

        # Append to our data list
        results.append({
            "File Name": file_name,
            "Type": file_type,
            "Size": size_str,
            "Dimensions": dimensions,
            "Animation": animation,
            "Remarks": remarks,
            "Status": status
        })

    # Create a Pandas DataFrame
    df = pd.DataFrame(results)

    # 5. Pandas Styler to keep our Red Highlights on specific failing cells!
    def style_dataframe(row):
        styles = [''] * len(row)
        
        if row['Status'] == '❌ Fail':
            if 'Unreadable' in row['Remarks']:
                return ['background-color: #FEF2F2; color: #DC2626;'] * len(row)
            
            for i, col in enumerate(row.index):
                if col == 'Status' or col == 'Remarks':
                    styles[i] = 'color: #DC2626; font-weight: bold;'
                elif col == 'Size' and 'Size' in row['Remarks']:
                    styles[i] = 'background-color: #FEF2F2; color: #DC2626; font-weight: bold;'
                elif col == 'Type' and 'Format' in row['Remarks']:
                    styles[i] = 'background-color: #FEF2F2; color: #DC2626; font-weight: bold;'
                elif col == 'Animation' and ('Animation' in row['Remarks'] or 'Infinite' in row['Remarks']):
                    styles[i] = 'background-color: #FEF2F2; color: #DC2626; font-weight: bold;'
        else:
            styles[df.columns.get_loc('Status')] = 'color: #16A34A; font-weight: bold;'
            styles[df.columns.get_loc('Remarks')] = 'color: #16A34A; font-weight: bold;'
            
        return styles

    styled_df = df.style.apply(style_dataframe, axis=1)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📊 Compliance Report")
    
    # Render native Streamlit interactive dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "File Name": st.column_config.TextColumn(width="medium"),
            "Remarks": st.column_config.TextColumn(width="large")
        }
    )
