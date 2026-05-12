import streamlit as st
from PIL import Image

# 1. Page Config (Make it wide and give it a tab title/icon)
st.set_page_config(page_title="Creative Inspector", page_icon="🎨", layout="wide")

# 2. Custom CSS to make it look less like "Streamlit" and more like a custom web app
st.markdown("""
    <style>
    /* Clean up the main background and font */
    .main { background-color: #f8f9fa; font-family: 'Segoe UI', Roboto, sans-serif; }
    
    /* Style the metrics cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Make the title stand out */
    h1 { color: #1e3a8a; font-weight: 700; padding-bottom: 0px;}
    .subtitle { color: #64748b; font-size: 1.1rem; margin-bottom: 30px; }
    
    /* Pass/Fail Badges */
    .badge-pass { background-color: #dcfce7; color: #166534; padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 14px;}
    .badge-fail { background-color: #fee2e2; color: #991b1b; padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 14px;}
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.title("🎨 Display Creative Inspector")
st.markdown("<p class='subtitle'>Upload display assets to automatically extract their metadata and validate network compliance (Max 150 KB, Max 30s animation).</p>", unsafe_allow_html=True)

# 4. Uploader Section (Centered in a column to not be overly wide)
upload_col, _ = st.columns([2, 1])
with upload_col:
    uploaded_files = st.file_uploader("Drag and drop creatives here", type=["jpg", "jpeg", "png", "gif"], accept_multiple_files=True)

st.divider()

# 5. Process Files
if uploaded_files:
    st.markdown(f"### Processed **{len(uploaded_files)}** creative(s)")
    
    for uploaded_file in uploaded_files:
        
        # Initialize default results
        results = {
            "Status": "Pass",
            "File Type": "-",
            "Size (KB)": "0",
            "Dimensions": "-",
            "Animation Length": "N/A",
            "Errors": []
        }

        # --- DETECTION LOGIC ---
        size_kb = uploaded_file.size / 1024
        results["Size (KB)"] = f"{size_kb:.2f}"
        if size_kb > 150:
            results["Errors"].append(f"File size is {size_kb:.2f} KB (Maximum allowed is 150 KB).")

        try:
            with Image.open(uploaded_file) as img:
                file_format = img.format.upper()
                allowed_formats = ['JPEG', 'PNG', 'GIF'] 
                results["File Type"] = file_format
                
                if file_format not in allowed_formats:
                    results["Errors"].append(f"Invalid format: {file_format}. Must be JPG, PNG, or GIF.")

                actual_width, actual_height = img.size
                results["Dimensions"] = f"{actual_width} x {actual_height}"

                if file_format == 'GIF' and getattr(img, "is_animated", False):
                    duration_ms = 0
                    loop_count = img.info.get("loop", 1) 
                    
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        duration_ms += img.info.get('duration', 100) 
                    
                    duration_sec = duration_ms / 1000.0
                    results["Animation Length"] = f"{duration_sec:.1f}s"

                    if loop_count == 0:
                        results["Errors"].append("GIF loops infinitely. Must stop within 30 seconds.")
                    elif duration_sec > 30:
                        results["Errors"].append(f"Animation is {duration_sec:.1f}s (Max allowed is 30s).")

        except Exception as e:
            results["Errors"].append("Could not read image. The file might be corrupted.")

        if len(results["Errors"]) > 0:
            results["Status"] = "Fail"

        # --- UI DISPLAY LOGIC (DASHBOARD STYLE) ---
        with st.expander(f"📁 {uploaded_file.name}", expanded=True):
            
            # Show Pass/Fail Badge
            if results["Status"] == "Pass":
                st.markdown("<span class='badge-pass'>✅ Approved</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='badge-fail'>❌ Rejected</span>", unsafe_allow_html=True)
            
            st.write("") # Spacer

            # Create a 4-column row for clean data display
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(label="File Type", value=results["File Type"])
            with col2:
                # Add a subtle warning color if size is close to limit
                st.metric(label="Size", value=f"{results['Size (KB)']} KB")
            with col3:
                st.metric(label="Dimensions", value=results["Dimensions"])
            with col4:
                st.metric(label="Animation", value=results["Animation Length"])

            # Errors Display
            if results["Errors"]:
                st.error("**Required Fixes:**\n" + "\n".join([f"- {err}" for err in results["Errors"]]))
