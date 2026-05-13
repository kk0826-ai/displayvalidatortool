import streamlit as st
import streamlit.components.v1 as components

# 1. Hide Streamlit's default padding and header to give the HTML full control
st.set_page_config(page_title="Display Validator", layout="wide")
st.markdown("""
    <style>
        .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; }
        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. Paste our entire HTML/JS code inside this variable
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Manrope', sans-serif; }
        body { background-color: #F8FAFC; color: #111827; padding-bottom: 50px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

        header {
            background-image: url('https://i.ibb.co/nMTJF4B9/vj-HZbu8-Imgur.jpg');
            background-size: cover;
            background-position: center;
            height: 75px; 
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            box-shadow: inset 0 0 0 2000px rgba(0, 0, 0, 0.4); 
        }

        header h1 {
            color: #FFFFFF;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 1px;
        }

        .upload-section {
            background-color: #FFFFFF;
            border: 2px dashed #9CA3AF;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 2rem;
        }

        .upload-section:hover, .upload-section.dragover {
            border-color: #4B5563;
            background-color: #F9FAFB;
        }

        .upload-btn {
            background-color: #FFFFFF;
            border: 1px solid #D1D5DB;
            color: #374151;
            padding: 10px 20px;
            font-size: 15px;
            font-weight: 600;
            border-radius: 4px;
            cursor: pointer;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        #file-input { display: none; }

        .table-title { font-size: 20px; font-weight: 700; color: #111827; margin-top: 32px; margin-bottom: 12px; display: none; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; background-color: #FFFFFF; margin-bottom: 2rem; display: none; }
        th { background-color: #0F172A; color: #FFFFFF; padding: 12px 16px; font-size: 13px; font-weight: 600; text-align: left; border: 1px solid #334155; }
        td { padding: 12px 16px; font-size: 14px; color: #111827; text-align: left; border: 1px solid #E5E7EB; vertical-align: top; word-wrap: break-word; }
        tr:nth-child(even) { background-color: #F9FAFB; }

        th:nth-child(1), td:nth-child(1) { width: 25%; }
        th:nth-child(2), td:nth-child(2) { width: 10%; }
        th:nth-child(3), td:nth-child(3) { width: 10%; }
        th:nth-child(4), td:nth-child(4) { width: 15%; }
        th:nth-child(5), td:nth-child(5) { width: 15%; }
        th:nth-child(6), td:nth-child(6) { width: 15%; }
        th:nth-child(7), td:nth-child(7) { width: 10%; }

        .status-pass { color: #16A34A; font-weight: 600; }
        .status-fail { color: #DC2626; font-weight: 600; }
    </style>
</head>
<body>
    <header><h1>DISPLAY VALIDATOR TOOL</h1></header>
    <div class="container">
        <div class="upload-section" id="dropzone" onclick="document.getElementById('file-input').click();">
            <button class="upload-btn">Click to browse or drag & drop creatives</button>
            <input type="file" id="file-input" multiple accept=".jpg,.jpeg,.png,.gif">
        </div>

        <h2 class="table-title" id="title-fail">Non-compliant</h2>
        <table id="table-fail">
            <thead><tr><th>File Name</th><th>Format</th><th>File Size</th><th>Dimensions</th><th>Animation</th><th>Remarks</th><th>Status</th></tr></thead>
            <tbody id="tbody-fail"></tbody>
        </table>

        <h2 class="table-title" id="title-pass">Compliant</h2>
        <table id="table-pass">
            <thead><tr><th>File Name</th><th>Format</th><th>File Size</th><th>Dimensions</th><th>Animation</th><th>Remarks</th><th>Status</th></tr></thead>
            <tbody id="tbody-pass"></tbody>
        </table>
    </div>

    <script>
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('file-input');

        dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
        dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
        dropzone.addEventListener('drop', (e) => { e.preventDefault(); dropzone.classList.remove('dragover'); handleFiles(e.dataTransfer.files); });
        fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

        async function extractGIFData(file) {
            try {
                const buffer = await file.arrayBuffer();
                const view = new DataView(buffer);
                let offset = 0;

                if (view.getUint8(0) !== 0x47) return { isAnimated: false }; 
                offset += 13; 

                const packed = view.getUint8(10);
                if (packed & 0x80) offset += 3 * (2 << (packed & 7)); 

                let loopCount = -1, totalMs = 0, frames = 0;

                function skipBlocks(o) {
                    while (o < view.byteLength) {
                        let s = view.getUint8(o++);
                        if (s === 0) break;
                        o += s;
                    }
                    return o;
                }

                while (offset < view.byteLength) {
                    const introducer = view.getUint8(offset++);
                    if (introducer === 0x3B) break; 

                    if (introducer === 0x21) { 
                        const label = view.getUint8(offset++);
                        if (label === 0xF9) { 
                            offset++; 
                            const delay = view.getUint16(offset + 1, true) * 10;
                            totalMs += (delay === 0 ? 100 : delay);
                            frames++;
                            offset += 5; 
                        } else if (label === 0xFF) { 
                            const size = view.getUint8(offset++);
                            if (size === 11) {
                                const app = String.fromCharCode(...new Uint8Array(buffer, offset, 11));
                                offset += 11;
                                if (app === "NETSCAPE2.0" || app === "ANIMEXTS1.0") {
                                    offset += 2; loopCount = view.getUint16(offset, true); offset += 3; 
                                } else { offset = skipBlocks(offset); }
                            } else { offset += size; offset = skipBlocks(offset); }
                        } else { offset = skipBlocks(offset); }
                    } else if (introducer === 0x2C) { 
                        offset += 8;
                        const imgPacked = view.getUint8(offset++);
                        if (imgPacked & 0x80) offset += 3 * (2 << (imgPacked & 7));
                        offset++; offset = skipBlocks(offset);
                    } else { break; }
                }
                return { isAnimated: frames > 1, loops: loopCount, duration: totalMs / 1000 };
            } catch (error) { return { isAnimated: false }; }
        }

        function getImageDimensions(file) {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(`${img.width} × ${img.height}`);
                img.onerror = () => resolve("Error");
                img.src = URL.createObjectURL(file);
            });
        }

        async function handleFiles(files) {
            document.getElementById('tbody-pass').innerHTML = "";
            document.getElementById('tbody-fail').innerHTML = "";
            let hasPass = false, hasFail = false;

            for (let file of files) {
                let status = "Pass", errors = [], animation = "-";
                
                let sizeKB = file.size / 1024;
                let sizeStr = sizeKB.toFixed(2) + " KB";
                if (sizeKB > 150) { errors.push("Size > 150 KB"); status = "Fail"; }

                let ext = file.name.split('.').pop().toUpperCase();
                if (!['JPG', 'JPEG', 'PNG', 'GIF'].includes(ext)) { errors.push("Invalid format"); status = "Fail"; }

                let dimensions = await getImageDimensions(file);

                if (ext === "GIF") {
                    let gifData = await extractGIFData(file);
                    if (gifData.isAnimated) {
                        let cSec = gifData.duration, loops = gifData.loops;
                        if (loops === 0) {
                            animation = `∞ Infinite (${cSec.toFixed(1)}s)`; errors.push("Infinite loop"); status = "Fail";
                        } else if (loops > 0) {
                            let tSec = cSec * loops; animation = `${tSec.toFixed(1)}s`;
                            if (tSec > 30) { errors.push("Animation > 30s"); status = "Fail"; }
                        } else {
                            animation = `${cSec.toFixed(1)}s`;
                            if (cSec > 30) { errors.push("Animation > 30s"); status = "Fail"; }
                        }
                    }
                }

                let statHtml = status === "Pass" ? "<span class='status-pass'>On Track</span>" : "<span class='status-fail'>Action Required</span>";
                let remHtml = status === "Pass" ? "None" : `<span class='status-fail'>${errors.join(" • ")}</span>`;

                let tr = `<tr><td>${file.name}</td><td>${ext}</td><td>${sizeStr}</td><td>${dimensions}</td><td>${animation}</td><td>${remHtml}</td><td>${statHtml}</td></tr>`;

                if (status === "Pass") { document.getElementById('tbody-pass').innerHTML += tr; hasPass = true; } 
                else { document.getElementById('tbody-fail').innerHTML += tr; hasFail = true; }
            }

            document.getElementById('title-pass').style.display = hasPass ? "block" : "none";
            document.getElementById('table-pass').style.display = hasPass ? "table" : "none";
            document.getElementById('title-fail').style.display = hasFail ? "block" : "none";
            document.getElementById('table-fail').style.display = hasFail ? "table" : "none";
        }
    </script>
</body>
</html>
"""
# 3. Render the HTML inside a Streamlit component
# Setting height=1000 ensures there is plenty of room to see the tables, and scrolling=True allows scrolling if the table gets massive.
components.html(html_code, height=1200, scrolling=True)
