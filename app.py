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

# 2. The Ultra-Premium HTML/JS Code
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
        body { background-color: #FAFAFA; color: #0F172A; padding-bottom: 80px; }
        .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }

        /* Premium Header Banner */
        header {
            background-image: url('https://i.ibb.co/nMTJF4B9/vj-HZbu8-Imgur.jpg');
            background-size: cover;
            background-position: center;
            height: 80px; 
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 3rem;
            box-shadow: inset 0 0 0 2000px rgba(15, 23, 42, 0.7); 
            border-bottom: 4px solid #111827;
        }
        header h1 {
            color: #FFFFFF;
            font-size: 24px;
            font-weight: 300;
            letter-spacing: 2px;
        }

        /* Ultra-Clean Sharp Upload Dropzone */
        .upload-section {
            background-color: #FFFFFF;
            border: 1.5px dashed #CBD5E1;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1.5rem;
            border-radius: 0px; /* Razor sharp */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }
        .upload-section:hover, .upload-section.dragover {
            border-color: #0F172A;
            background-color: #F8FAFC;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        }
        .upload-icon {
            width: 42px;
            height: 42px;
            color: #64748B;
            margin-bottom: 16px;
            transition: color 0.3s ease;
        }
        .upload-section:hover .upload-icon { color: #0F172A; }
        .upload-text {
            color: #0F172A;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        .upload-subtext {
            color: #64748B;
            font-size: 13px;
            margin-top: 6px;
            font-weight: 500;
        }
        #file-input { display: none; }

        /* Action Bar (Clear Button) */
        .action-bar {
            display: none; 
            justify-content: center; /* Centered Button */
            margin-bottom: 2.5rem;
        }
        .clear-btn {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            color: #475569;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 700;
            border-radius: 0px; /* Razor sharp */
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .clear-btn:hover {
            background-color: #F1F5F9;
            color: #0F172A;
            border-color: #94A3B8;
        }

        /* Minimalist High-End Data Tables */
        .table-wrapper {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            margin-bottom: 3rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            display: none; 
            border-radius: 0px; /* Razor sharp */
        }
        .table-header-title {
            padding: 20px 24px;
            border-bottom: 1px solid #E2E8F0;
            background: #FAFAFA; /* Very subtle highlight for the title block */
            font-size: 16px;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        
        th { 
            background-color: #F1F5F9; /* Highlighted Header Row */
            color: #334155; 
            padding: 14px 24px; 
            font-size: 11px; 
            font-weight: 800; 
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-align: left; 
            border-bottom: 2px solid #E2E8F0; /* Stronger bottom border */
        }
        td { 
            padding: 18px 24px; 
            font-size: 13px; 
            color: #0F172A; 
            text-align: left; 
            border-bottom: 1px solid #E2E8F0; 
            vertical-align: middle; 
            word-wrap: break-word; 
            font-weight: 500;
        }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background-color: #F8FAFC !important; cursor: default; }

        /* Column Sizing */
        th:nth-child(1), td:nth-child(1) { width: 30%; font-weight: 700; } 
        th:nth-child(2), td:nth-child(2) { width: 12%; }
        th:nth-child(3), td:nth-child(3) { width: 14%; }
        th:nth-child(4), td:nth-child(4) { width: 18%; }
        th:nth-child(5), td:nth-child(5) { width: 26%; }

        /* Sleek Status Dots */
        .status-container { display: flex; flex-direction: column; gap: 4px; }
        .status-main { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 13px; }
        .dot { height: 8px; width: 8px; border-radius: 50%; display: inline-block; }
        .dot-pass { background-color: #10B981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15); }
        .dot-fail { background-color: #EF4444; box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15); }
        .status-text-pass { color: #064E3B; }
        .status-text-fail { color: #7F1D1D; }

        /* Typography Hierarchy */
        .text-primary { color: #0F172A; font-size: 14px; font-weight: 700; }
        .text-secondary { color: #64748B; font-size: 12px; font-weight: 500; margin-top: 4px; display: block; }
        .text-error-detail { color: #DC2626; font-size: 12px; font-weight: 600; margin-top: 4px; display: block; }
        .format-badge { background: #E2E8F0; color: #334155; padding: 4px 8px; border-radius: 0px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }

    </style>
</head>
<body>
    <header><h1>DISPLAY VALIDATOR TOOL</h1></header>
    
    <div class="container">
        <div class="upload-section" id="dropzone" onclick="document.getElementById('file-input').click();">
            <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
            </svg>
            <span class="upload-text">Drag & drop your creatives here</span>
            <span class="upload-subtext">or click to browse files</span>
            <input type="file" id="file-input" multiple accept=".jpg,.jpeg,.png,.gif">
        </div>

        <div class="action-bar" id="action-bar">
            <button class="clear-btn" onclick="clearResults()">
                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                CLEAR RESULTS
            </button>
        </div>

        <div class="table-wrapper" id="wrapper-fail">
            <div class="table-header-title">
                <span class="dot dot-fail" style="margin-right: 4px;"></span> Action Required
            </div>
            <table>
                <thead><tr><th>File Name</th><th>Format</th><th>Size & Dims</th><th>Animation</th><th>Status Report</th></tr></thead>
                <tbody id="tbody-fail"></tbody>
            </table>
        </div>

        <div class="table-wrapper" id="wrapper-pass">
            <div class="table-header-title">
                <span class="dot dot-pass" style="margin-right: 4px;"></span> Compliant Assets
            </div>
            <table>
                <thead><tr><th>File Name</th><th>Format</th><th>Size & Dims</th><th>Animation</th><th>Status Report</th></tr></thead>
                <tbody id="tbody-pass"></tbody>
            </table>
        </div>
    </div>

    <script>
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('file-input');

        // Clear Results Functionality
        function clearResults() {
            document.getElementById('tbody-pass').innerHTML = "";
            document.getElementById('tbody-fail').innerHTML = "";
            document.getElementById('wrapper-pass').style.display = "none";
            document.getElementById('wrapper-fail').style.display = "none";
            document.getElementById('action-bar').style.display = "none";
            fileInput.value = ""; 
        }

        // --- BUG FIX: Removed the extra curly brace here ---
        dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
        dropzone.addEventListener('dragleave', () => { dropzone.classList.remove('dragover'); });
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
            let hasPass = document.getElementById('tbody-pass').innerHTML !== "";
            let hasFail = document.getElementById('tbody-fail').innerHTML !== "";

            for (let file of files) {
                let status = "Pass", errors = [], animationHtml = "<span class='text-secondary'>Static Image</span>";
                
                let sizeKB = file.size / 1024;
                let sizeStr = sizeKB.toFixed(1) + " KB";
                if (sizeKB > 150) { errors.push("Exceeds 150 KB limit"); status = "Fail"; }

                let ext = file.name.split('.').pop().toUpperCase();
                if (!['JPG', 'JPEG', 'PNG', 'GIF'].includes(ext)) { errors.push("Invalid file format"); status = "Fail"; }

                let dimensions = await getImageDimensions(file);

                if (ext === "GIF") {
                    let gifData = await extractGIFData(file);
                    if (gifData.isAnimated) {
                        let cSec = gifData.duration;
                        let rawLoops = gifData.loops;
                        let displayLoops = rawLoops < 0 ? 1 : rawLoops; 

                        if (rawLoops === 0) {
                            animationHtml = `<span class='text-primary'>∞ Infinite</span><span class='text-secondary'>${cSec.toFixed(1)}s</span>`; 
                            errors.push("Contains infinite loop"); 
                            status = "Fail";
                        } else {
                            let tSec = cSec * displayLoops;
                            animationHtml = `<span class='text-primary'>${tSec.toFixed(1)}s</span>`;
                            if (tSec > 30) { errors.push("Animation exceeds 30s"); status = "Fail"; }
                        }
                    }
                }

                let sizeColorClass = sizeKB > 150 ? 'text-error-detail' : 'text-primary';
                let sizeDimHtml = `<span class='${sizeColorClass}'>${sizeStr}</span><span class='text-secondary'>${dimensions}</span>`;

                let statusBlock = "";
                if (status === "Pass") {
                    statusBlock = `<div class='status-container'>
                                      <div class='status-main status-text-pass'><span class='dot dot-pass'></span> Approved</div>
                                   </div>`;
                } else {
                    statusBlock = `<div class='status-container'>
                                      <div class='status-main status-text-fail'><span class='dot dot-fail'></span> Rejected</div>
                                      <span class='text-error-detail'>${errors.join("<br>")}</span>
                                   </div>`;
                }

                let tr = `<tr>
                    <td>${file.name}</td>
                    <td><span class='format-badge'>${ext}</span></td>
                    <td>${sizeDimHtml}</td>
                    <td>${animationHtml}</td>
                    <td>${statusBlock}</td>
                </tr>`;

                if (status === "Pass") { document.getElementById('tbody-pass').innerHTML += tr; hasPass = true; } 
                else { document.getElementById('tbody-fail').innerHTML += tr; hasFail = true; }
            }

            if (hasPass || hasFail) { document.getElementById('action-bar').style.display = "flex"; }
            document.getElementById('wrapper-pass').style.display = hasPass ? "block" : "none";
            document.getElementById('wrapper-fail').style.display = hasFail ? "block" : "none";
        }
    </script>
</body>
</html>
"""

# 3. Render the HTML inside a Streamlit component
components.html(html_code, height=1200, scrolling=True)
