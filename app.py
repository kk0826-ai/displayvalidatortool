import streamlit as st
import streamlit.components.v1 as components

# 1. Hide Streamlit's default padding to give the HTML full control
st.set_page_config(page_title="Display Validator", layout="wide")
st.markdown("""
    <style>
        .block-container { padding: 0rem !important; }
        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. The Premium HTML/JS Code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        /* Global & Reset */
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Manrope', sans-serif; }
        body { background-color: #F1F5F9; color: #0F172A; padding-bottom: 60px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

        /* Premium Header Banner */
        header {
            background-image: url('https://i.ibb.co/nMTJF4B9/vj-HZbu8-Imgur.jpg');
            background-size: cover;
            background-position: center;
            height: 80px; 
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2.5rem;
            box-shadow: inset 0 0 0 2000px rgba(15, 23, 42, 0.6); /* Deeper overlay for text contrast */
        }
        header h1 {
            color: #FFFFFF;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 1.5px;
        }

        /* Modern Upload Dropzone */
        .upload-section {
            background-color: #FFFFFF;
            border: 2px dashed #CBD5E1;
            padding: 50px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 2.5rem;
            border-radius: 0px; /* Sharp corners as requested */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .upload-section:hover, .upload-section.dragover {
            border-color: #3B82F6;
            background-color: #EFF6FF;
        }
        .upload-icon {
            width: 48px;
            height: 48px;
            color: #94A3B8;
            margin-bottom: 16px;
            transition: color 0.2s ease;
        }
        .upload-section:hover .upload-icon { color: #3B82F6; }
        .upload-text {
            color: #334155;
            font-size: 16px;
            font-weight: 600;
        }
        #file-input { display: none; }

        /* Enterprise SaaS Data Tables */
        .table-wrapper {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            margin-bottom: 2.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            display: none; /* Hidden initially */
        }
        .table-header-title {
            padding: 16px 20px;
            border-bottom: 1px solid #E2E8F0;
            background: #FFFFFF;
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        
        th { 
            background-color: #F8FAFC; 
            color: #64748B; 
            padding: 12px 20px; 
            font-size: 12px; 
            font-weight: 700; 
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: left; 
            border-bottom: 1px solid #E2E8F0; 
        }
        td { 
            padding: 16px 20px; 
            font-size: 14px; 
            color: #334155; 
            text-align: left; 
            border-bottom: 1px solid #F1F5F9; 
            vertical-align: middle; 
            word-wrap: break-word; 
        }
        tr:last-child td { border-bottom: none; }
        tr:hover { background-color: #F8FAFC; }

        /* Column Sizing */
        th:nth-child(1), td:nth-child(1) { width: 28%; font-weight: 500; color: #0F172A; }
        th:nth-child(2), td:nth-child(2) { width: 10%; }
        th:nth-child(3), td:nth-child(3) { width: 12%; }
        th:nth-child(4), td:nth-child(4) { width: 14%; }
        th:nth-child(5), td:nth-child(5) { width: 16%; }
        th:nth-child(6), td:nth-child(6) { width: 10%; }

        /* Pill Badges */
        .badge {
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            display: inline-block;
            text-align: center;
        }
        .badge-pass { background-color: #DCFCE7; color: #166534; }
        .badge-fail { background-color: #FEE2E2; color: #991B1B; }

        /* Status text formatting */
        .text-error { color: #DC2626; font-weight: 600; }
        .text-sub { color: #64748B; font-size: 12px; margin-top: 4px; display: block; }
    </style>
</head>
<body>
    <header><h1>DISPLAY VALIDATOR TOOL</h1></header>
    
    <div class="container">
        <div class="upload-section" id="dropzone" onclick="document.getElementById('file-input').click();">
            <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
            <span class="upload-text">Click to browse or drag & drop creatives</span>
            <input type="file" id="file-input" multiple accept=".jpg,.jpeg,.png,.gif">
        </div>

        <div class="table-wrapper" id="wrapper-fail">
            <div class="table-header-title">
                <span style="color: #DC2626;">●</span> Action Required
            </div>
            <table>
                <thead><tr><th>File Name</th><th>Format</th><th>Size</th><th>Dimensions</th><th>Animation</th><th>Status</th></tr></thead>
                <tbody id="tbody-fail"></tbody>
            </table>
        </div>

        <div class="table-wrapper" id="wrapper-pass">
            <div class="table-header-title">
                <span style="color: #16A34A;">●</span> Compliant Assets
            </div>
            <table>
                <thead><tr><th>File Name</th><th>Format</th><th>Size</th><th>Dimensions</th><th>Animation</th><th>Status</th></tr></thead>
                <tbody id="tbody-pass"></tbody>
            </table>
        </div>
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
                img.onerror = () => resolve("-");
                img.src = URL.createObjectURL(file);
            });
        }

        async function handleFiles(files) {
            document.getElementById('tbody-pass').innerHTML = "";
            document.getElementById('tbody-fail').innerHTML = "";
            let hasPass = false, hasFail = false;

            for (let file of files) {
                let status = "Pass", errors = [], animationHtml = "-";
                
                let sizeKB = file.size / 1024;
                let sizeStr = sizeKB.toFixed(2) + " KB";
                if (sizeKB > 150) { errors.push("Size > 150 KB"); status = "Fail"; }

                let ext = file.name.split('.').pop().toUpperCase();
                if (!['JPG', 'JPEG', 'PNG', 'GIF'].includes(ext)) { errors.push("Invalid format"); status = "Fail"; }

                let dimensions = await getImageDimensions(file);

                if (ext === "GIF") {
                    let gifData = await extractGIFData(file);
                    if (gifData.isAnimated) {
                        let cSec = gifData.duration;
                        let rawLoops = gifData.loops;
                        let displayLoops = rawLoops < 0 ? 1 : rawLoops; // Default to 1 play if no loop tag found

                        if (rawLoops === 0) {
                            animationHtml = `∞ Infinite <span class='text-sub'>(${cSec.toFixed(1)}s cycle)</span>`; 
                            errors.push("Infinite loop"); 
                            status = "Fail";
                        } else {
                            let tSec = cSec * displayLoops;
                            // MATH ALWAYS SHOWS HERE:
                            animationHtml = `${tSec.toFixed(1)}s <span class='text-sub'>(${cSec.toFixed(1)}s × ${displayLoops} plays)</span>`;
                            if (tSec > 30) { errors.push("Animation > 30s"); status = "Fail"; }
                        }
                    }
                }

                // Removed the separate remarks column and combined it with Status for a cleaner look
                let statBadge = status === "Pass" ? "<span class='badge badge-pass'>Compliant</span>" : "<span class='badge badge-fail'>Fail</span>";
                let errorHtml = status === "Fail" ? `<span class='text-sub text-error'>${errors.join(" • ")}</span>` : "";

                let tr = `<tr>
                    <td>${file.name}</td>
                    <td>${ext}</td>
                    <td><span class="${sizeKB > 150 ? 'text-error' : ''}">${sizeStr}</span></td>
                    <td>${dimensions}</td>
                    <td>${animationHtml}</td>
                    <td>${statBadge}${errorHtml}</td>
                </tr>`;

                if (status === "Pass") { document.getElementById('tbody-pass').innerHTML += tr; hasPass = true; } 
                else { document.getElementById('tbody-fail').innerHTML += tr; hasFail = true; }
            }

            document.getElementById('wrapper-pass').style.display = hasPass ? "block" : "none";
            document.getElementById('wrapper-fail').style.display = hasFail ? "block" : "none";
        }
    </script>
</body>
</html>
"""

# 3. Render the HTML inside a Streamlit component
components.html(html_code, height=1200, scrolling=True)
