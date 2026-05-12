import streamlit as st
from PIL import Image

st.title("Display Creative Inspector")
st.write("Upload an asset to automatically detect its properties and verify standard limits (Max 150 KB, Max 30s animation).")

# File uploader
uploaded_file = st.file_uploader("Upload Asset (JPG, PNG, GIF)", type=["jpg", "jpeg", "png", "gif"])

if uploaded_file is not None:
    st.subheader(f"Asset Report: {uploaded_file.name}")
    
    results = {
        "Status": "✅ Pass",
        "File Type": "Unknown",
        "Size (KB)": "0",
        "Dimensions": "Unknown",
        "Animation Length (s)": "N/A",
        "Errors": []
    }

    # 1. Detect and Check Size
    size_kb = uploaded_file.size / 1024
    results["Size (KB)"] = f"{size_kb:.2f}"
    if size_kb > 150:
        results["Errors"].append(f"Size is {size_kb:.2f} KB (Max allowed is 150 KB).")

    # 2. Detect Image Metadata
    try:
        with Image.open(uploaded_file) as img:
            # Detect File Type
            file_format = img.format.upper()
            allowed_formats = ['JPEG', 'PNG', 'GIF'] 
            results["File Type"] = file_format
            
            if file_format not in allowed_formats:
                results["Errors"].append(f"Invalid type: {file_format}. Must be JPG, PNG, or GIF.")

            # Detect Dimensions Automatically
            actual_width, actual_height = img.size
            results["Dimensions"] = f"{actual_width}x{actual_height}"

            # 3. Detect and Check Animation (GIFs only)
            if file_format == 'GIF' and getattr(img, "is_animated", False):
                duration_ms = 0
                loop_count = img.info.get("loop", 1) 
                
                for frame in range(img.n_frames):
                    img.seek(frame)
                    duration_ms += img.info.get('duration', 100) 
                
                duration_sec = duration_ms / 1000.0
                results["Animation Length (s)"] = f"{duration_sec:.2f}"

                if loop_count == 0:
                    results["Errors"].append("GIF loops infinitely. Animations must stop within 30 seconds.")
                elif duration_sec > 30:
                    results["Errors"].append(f"Animation duration is {duration_sec:.2f}s (Max allowed is 30s).")

    except Exception as e:
        results["Errors"].append("Could not read image data. File might be corrupted.")

    if len(results["Errors"]) > 0:
        results["Status"] = "❌ Fail (Needs Replacement)"

    # Display Results
    if "Pass" in results["Status"]:
        st.success(f"**Status:** {results['Status']}")
    else:
        st.error(f"**Status:** {results['Status']}")

    st.write(f"**Detected File Type:** {results['File Type']}")
    st.write(f"**Detected Size:** {results['Size (KB)']} KB")
    st.write(f"**Detected Dimensions:** {results['Dimensions']}")
    
    # Only show animation length if it's actually a GIF
    if results["File Type"] == "GIF":
        st.write(f"**Detected Animation Length:** {results['Animation Length (s)']} seconds")

    if results["Errors"]:
        st.warning("**Issues Detected:**")
        for error in results["Errors"]:
            st.write(f"- {error}")
