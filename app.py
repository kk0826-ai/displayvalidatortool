import streamlit as st
from PIL import Image

st.title("Display Creative Validator")
st.write("Upload an asset to verify file type, max size (150 KB), dimensions, and animation length (Max 30s).")

# Standard Display Ad Sizes Dropdown
standard_sizes = [
    "300 x 250 (Medium Rectangle)",
    "728 x 90 (Leaderboard)",
    "160 x 600 (Wide Skyscraper)",
    "300 x 600 (Half Page)",
    "970 x 250 (Billboard)",
    "320 x 50 (Mobile Leaderboard)",
    "300 x 50 (Mobile Banner)",
    "Custom Size"
]

selected_size = st.selectbox("Select Expected Ad Size:", standard_sizes)

# Determine expected width and height based on selection
if selected_size == "Custom Size":
    col1, col2 = st.columns(2)
    with col1:
        expected_width = st.number_input("Expected Width (px):", min_value=1, value=800)
    with col2:
        expected_height = st.number_input("Expected Height (px):", min_value=1, value=600)
else:
    # Automatically extract the numbers from the dropdown text (e.g., "300 x 250")
    parts = selected_size.split(" ")
    expected_width = int(parts[0])
    expected_height = int(parts[2])

# File uploader
uploaded_file = st.file_uploader("Upload Asset (JPG, PNG, GIF)", type=["jpg", "jpeg", "png", "gif"])

# ... (Keep the rest of your existing code from 'if uploaded_file is not None:' downwards) ...
