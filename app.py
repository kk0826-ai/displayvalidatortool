import streamlit as st
import streamlit.components.v1 as components

# 1. Hide Streamlit's default padding
st.set_page_config(page_title="Display Validator", layout="wide")
st.markdown("""
    <style>
        .block-container { padding: 0rem !important; }
        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. The Robust, Commercial-Grade HTML/JS Code
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
        body { background-color: #FAFAFA; color: #0F172A; padding-bottom: 100px; }
        .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }

        /* Premium Header */
        header {
            background-image: url('https://i.ibb.co/nMTJF4B9/vj-HZbu8-Imgur.jpg');
            background-size: cover;
            background-position: center;
            height: 80px; 
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 3rem;
            box-shadow: inset 0 0 0 2000px rgba(15, 23, 42, 0.75); 
            border-bottom: 4px solid #111827;
        }
        header h1 { color: #FFFFFF; font-size: 24px; font-weight: 800; letter-spacing: 2px; }

        /* Sharp Upload Dropzone */
        .upload-section {
            background-color: #FFFFFF;
            border: 1.5px dashed #CBD5E1;
            padding: 50px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 2rem;
            border-radius: 0px; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .upload-section:hover, .upload-section.dragover {
            border-color: #0F172A;
            background-color: #F8FAFC;
        }
        .upload-icon { width: 42px; height: 42px; color: #64748B; margin-bottom: 12px; transition: color 0.2s ease; }
        .upload-section:hover .upload-icon { color: #0F172A; }
        .upload-text { color: #0F172A; font-size: 15px; font-weight: 700; letter-spacing: 0.3px; }
        .upload-subtext { color: #64748B; font-size: 13px; margin-top: 6px; font-weight: 500; }
        #file-input { display: none; }

        /* Summary Dashboard */
        .summary-dashboard {
            display: none; 
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 2rem;
        }
        .summary-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            border-radius: 0px; 
        }
        .summary-value { font-size: 28px; font-weight: 800; color: #0F172A; line-height: 1; }
        .summary-label { font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-top: 8px; }
        
        /* Status Colors */
        .val-pass { color: #10B981; }
        .val-caution { color: #F59E0B; }
        .val-fail { color: #EF4444; }

        /* Floating Sticky Clear Button */
        .sticky-action-bar {
            display: none;
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 100;
        }
        .clear-btn {
            background-color: #111827;
            color: #FFFFFF;
            border: none;
            padding: 12px 24px;
            font-size: 13px;
            font-weight: 700;
            border-radius: 0px; 
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: background-color 0.2s;
        }
        .clear-btn:hover { background-color: #334155; }

        /* Data Tables */
        .table-wrapper {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            margin-bottom: 2rem;
            display: none; 
            border-radius: 0px; 
        }
        .table-header-title {
            padding: 20px 24px;
            border-bottom: 1px solid #E2E8F0;
            background: #FAFAFA; 
            font-size: 16px;
            font-weight: 800;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { background-color: #F1F5F9; color: #334155; padding: 14px 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; text-align: left; border-bottom: 2px solid #E2E8F0; }
        td { padding: 18px 20px; font-size: 13px; color: #0F172A; text-align: left; border-bottom: 1px solid #E2E8F0; vertical-align: middle; word-wrap: break-word; font-weight: 500; }
        tr:last-child td { border-bottom: none; }
        tr.data-row:hover td { background-color: #F8FAFC !important; cursor: default; }

        /* 6 Column Sizing */
        th:nth-child(1), td:nth-child(1) { width: 26%; font-weight: 700; } 
        th:nth-child(2), td:nth-child(2) { width: 10%; } 
        th:nth-child(3), td:nth-child(3) { width: 10%; } 
        th:nth-child(4), td:nth-child(4) { width: 15%; } 
        th:nth-child(5), td:nth-child(5) { width: 14%; } 
        th:nth-child(6), td:nth-child(6) { width: 25%; } 

        .status-container { display: flex; flex-direction: column; gap: 4px; }
        .status-main { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 13px; }
        
        .dot { height: 8px; width: 8px; border-radius: 50%; display: inline-block; }
        .dot-pass { background-color: #10B981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15); }
        .dot-caution { background-color: #F59E0B; box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15); }
        .dot-fail { background-color: #EF4444; box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15); }
        
        .status-text-pass { color: #064E3B; }
        .status-text-caution { color: #92400E; }
        .status-text-fail { color: #7F1D1D; }

        .text-primary { color: #0F172A; font-size: 14px; font-weight: 700; }
        .text-secondary { color: #64748B; font-size: 12px; font-weight: 500; }
        .text-caution-detail { color: #D97706; font-size: 13px; font-weight: 700; }
        .text-error-detail { color: #DC2626; font-size: 13px; font-weight: 700; }
        
        .format-badge { color: #475569; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; }
    </style>
</head>
<body>
    <header><h1>DISPLAY VALIDATOR TOOL</h1></header>
    
    <div class="container">
        
        <div class="summary-dashboard" id="summary-dashboard">
            <div class="summary-card">
                <div class="summary-value val-pass" id="count-pass">0</div>
                <div class="summary-label">Compliant</div>
            </div>
            <div class="summary-card">
                <div class="summary-value val-caution" id="count-caution">0</div>
                <div class="summary-label">Review (Caution)</div>
            </div>
            <div class="summary-card">
                <div class="summary-value val-fail" id="count-fail">0</div>
                <div class="summary-label">Rejected</div>
            </div>
        </div>

        <div class="upload-section" id="dropzone" onclick="document.getElementById('file-input').click();">
            <svg class="upload-icon" id="upload-icon-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
            </svg>
            <span class="upload-text" id="upload-main-text">Drag & drop your creatives here</span>
            <span class="upload-subtext" id="upload-sub-text">or click to browse files</span>
            <input type="file" id="file-input" multiple accept=".jpg,.jpeg,.png,.gif">
        </div>

        <div class="sticky-action-bar" id="action-bar">
            <button class="clear-btn" onclick="clearResults()">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                Clear All Results
            </button>
        </div>

        <div class="table-wrapper" id="wrapper-fail">
            <div class="table-header-title">
                <span class="dot dot-fail" style="margin-right: 4px;"></span> Rejected Assets
            </div>
            <table>
                <thead><tr><th>File Name</th><th>File Type</th><th>Size</th><th>Dimensions</th><th>Animation</th><th>Status</th></tr></thead>
                <tbody id="tbody-fail"></tbody>
            </table>
        </div>

        <div class="table-wrapper" id="wrapper-caution">
            <div class="table-header-title">
                <span class="dot dot-caution" style="margin-right: 4px;"></span> Review Required (Caution)
            </div>
            <table>
                <thead><tr><th>File Name</th><th>File Type</th><th>Size</th><th>Dimensions</th><th>Animation</th><th>Status</th></tr></thead>
                <tbody id="tbody-caution"></tbody>
            </table>
        </div>

        <div class="table-wrapper" id="wrapper-pass">
            <div class="table-header-title">
                <span class="dot dot-pass" style="margin-right: 4px;"></span> Approved Assets
            </div>
            <table>
                <thead><tr><th>File Name</th><th>File Type</th><th>Size</th><th>Dimensions</th><th>Animation</th><th>Status</th></tr></thead>
                <tbody id="tbody-pass"></tbody>
            </table>
        </div>

    </div>

    <script>
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('file-input');
        
        let processedFiles = new Set();
        let passCount = 0;
        let cautionCount = 0;
        let failCount = 0;

        const STANDARD_DIMENSIONS = [
            "120x600", "160x600", "300x250", "300x600", "336x280",
            "468x60", "728x90", "970x250", "970x90", "300x50",
            "320x50", "320x480", "480x320", "768x1024", "1024x768"
        ];

        function updateSummary() {
            document.getElementById('count-pass').innerText = passCount;
            document.getElementById('count-caution').innerText = cautionCount;
            document.getElementById('count-fail').innerText = failCount;
            
            let total = passCount + cautionCount + failCount;
            
            if (total > 0) {
                document.getElementById('summary-dashboard').style.display = "grid";
                document.getElementById('action-bar').style.display = "block";
                
                // Only show the tables if they actually have rows
                document.getElementById('wrapper-fail').style.display = failCount > 0 ? "block" : "none";
                document.getElementById('wrapper-caution').style.display = cautionCount > 0 ? "block" : "none";
                document.getElementById('wrapper-pass').style.display = passCount > 0 ? "block" : "none";
            } else {
                document.getElementById('summary-dashboard').style.display = "none";
                document.getElementById('action-bar').style.display = "none";
                document.getElementById('wrapper-fail').style.display = "none";
                document.getElementById('wrapper-caution').style.display = "none";
                document.getElementById('wrapper-pass').style.display = "none";
            }
        }

        function clearResults() {
            processedFiles.clear();
            passCount = 0; cautionCount = 0; failCount = 0;
            document.getElementById('tbody-pass').innerHTML = "";
            document.getElementById('tbody-caution').innerHTML = "";
            document.getElementById('tbody-fail').innerHTML = "";
            fileInput.value = ""; 
            updateSummary();
        }

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
                function skipBlocks(o) { while (o < view.byteLength) { let s = view.getUint8(o++); if (s === 0) break; o += s; } return o; }

                while (offset < view.byteLength) {
                    const introducer = view.getUint8(offset++);
                    if (introducer === 0x3B) break; 
                    if (introducer === 0x21) { 
                        const label = view.getUint8(offset++);
                        if (label === 0xF9) { 
                            offset++; const delay = view.getUint16(offset + 1, true) * 10; totalMs += (delay === 0 ? 100 : delay); frames++; offset += 5; 
                        } else if (label === 0xFF) { 
                            const size = view.getUint8(offset++);
                            if (size === 11) {
                                const app = String.fromCharCode(...new Uint8Array(buffer, offset, 11)); offset += 11;
                                if (app === "NETSCAPE2.0" || app === "ANIMEXTS1.0") { offset += 2; loopCount = view.getUint16(offset, true); offset += 3; } 
                                else { offset = skipBlocks(offset); }
                            } else { offset += size; offset = skipBlocks(offset); }
                        } else { offset = skipBlocks(offset); }
                    } else if (introducer === 0x2C) { 
                        offset += 8; const imgPacked = view.getUint8(offset++); if (imgPacked & 0x80) offset += 3 * (2 << (imgPacked & 7)); offset++; offset = skipBlocks(offset);
                    } else { break; }
                }
                return { isAnimated: frames > 1, loops: loopCount, duration: totalMs / 1000 };
            } catch (error) { return { isAnimated: false }; }
        }

        function getImageInfo(file) {
            const imgPromise = new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve({ width: img.width, height: img.height, valid: true });
                img.onerror = () => resolve({ valid: false });
                img.src = URL.createObjectURL(file);
            });
            const timeoutPromise = new Promise((resolve) => setTimeout(() => resolve({ valid: false, timeout: true }), 2000));
            return Promise.race([imgPromise, timeoutPromise]);
        }

        async function handleFiles(files) {
            document.getElementById('upload-main-text').innerText = "Processing files...";
            document.getElementById('upload-icon-svg').style.color = "#3B82F6";
            await new Promise(resolve => setTimeout(resolve, 50)); 

            const allowedMimeTypes = ['image/jpeg', 'image/png', 'image/gif'];

            for (let file of files) {
                let fileId = file.name + "_" + file.size;
                if (processedFiles.has(fileId)) continue; 
                processedFiles.add(fileId);

                let status = "Pass", animationHtml = "<span class='text-secondary'>Static Image</span>";
                let sizeKB = file.size / 1024;
                let sizeStr = sizeKB.toFixed(1) + " KB";
                
                let rawExt = file.name.split('.').pop();
                let logicExt = rawExt.toUpperCase();
                let displayExt = "." + rawExt.toLowerCase();
                
                let dimHtml = "<span class='text-secondary'>-</span>";
                let dimHasWarning = false;
                
                // Hard Cap: Exceeds 5MB
                if (sizeKB > 5120) { 
                    status = "Fail";
                    appendRow(file.name, displayExt, sizeStr, dimHtml, animationHtml, status, sizeKB);
                    continue;
                }

                if (!allowedMimeTypes.includes(file.type) && !['JPG', 'JPEG', 'PNG', 'GIF'].includes(logicExt)) {
                    status = "Fail"; 
                }
                
                // Hard Cap: Size
                if (sizeKB > 150) { status = "Fail"; }

                let imgInfo = await getImageInfo(file);
                let dimHasError = false;

                if (!imgInfo.valid) {
                    status = "Fail";
                    dimHasError = true;
                    dimHtml = `<span class='text-error-detail'>Corrupted/Unreadable</span>`;
                } else {
                    let actualW = imgInfo.width;
                    let actualH = imgInfo.height;
                    let actualDimStr = `${actualW}x${actualH}`;

                    let isStandard = STANDARD_DIMENSIONS.includes(actualDimStr);
                    let isNearMiss = false;

                    // Expanded threshold: Now catches up to 4 pixels off (1, 2, 3, or 4 px bleeds)
                    if (!isStandard) {
                        for (let sDim of STANDARD_DIMENSIONS) {
                            let [sW, sH] = sDim.split('x').map(Number);
                            if (Math.abs(actualW - sW) <= 4 && Math.abs(actualH - sH) <= 4) {
                                isNearMiss = true;
                                break;
                            }
                        }
                    }

                    // Extract dimensions stated in filename
                    let nameRegex = /(?<!\d)(\d+)[xX](\d+)(?!\d)/;
                    let nameMatch = file.name.match(nameRegex);
                    let nameDimStr = nameMatch ? `${nameMatch[1]}x${nameMatch[2]}` : null;

                    // New Strict Dimension Logic
                    if (nameDimStr && nameDimStr !== actualDimStr) {
                        // 1. If filename claims a size and actual size is different -> INSTANT FAIL
                        status = "Fail"; dimHasError = true;
                    } else if (isStandard) {
                        // 2. If it's standard and name matched (or didn't exist) -> PASS
                        // Just let it keep status = "Pass"
                    } else if (isNearMiss) {
                        // 3. If it's a 1-4 pixel sloppy export from a standard size -> FAIL
                        status = "Fail"; dimHasError = true;
                    } else {
                        // 4. If it's a completely random size (e.g. 500x500) and no misleading filename -> CAUTION
                        if (status !== "Fail") status = "Caution"; dimHasWarning = true;
                    }

                    let dimColorClass = 'text-primary';
                    if (dimHasWarning) dimColorClass = 'text-caution-detail';
                    if (status === "Fail" && dimHasError) dimColorClass = 'text-error-detail';
                    
                    dimHtml = `<span class='${dimColorClass}'>${actualW} × ${actualH}</span>`;
                }

                // Hard Cap: Animation Time
                if (logicExt === "GIF" && imgInfo.valid) { 
                    let gifData = await extractGIFData(file);
                    if (gifData.isAnimated) {
                        let cSec = gifData.duration;
                        let rawLoops = gifData.loops;
                        let displayLoops = rawLoops < 0 ? 1 : rawLoops; 

                        if (rawLoops === 0) {
                            animationHtml = `<span class='text-error-detail'>∞ Infinite (${cSec.toFixed(1)}s)</span>`; 
                            status = "Fail";
                        } else {
                            let tSec = cSec * displayLoops;
                            if (tSec > 30) { 
                                animationHtml = `<span class='text-error-detail'>${tSec.toFixed(1)}s</span>`;
                                status = "Fail"; 
                            } else {
                                animationHtml = `<span class='text-primary'>${tSec.toFixed(1)}s</span>`;
                            }
                        }
                    }
                }

                appendRow(file.name, displayExt, sizeStr, dimHtml, animationHtml, status, sizeKB);
            }

            document.getElementById('upload-main-text').innerText = "Drag & drop your creatives here";
            document.getElementById('upload-icon-svg').style.color = "#64748B";
            updateSummary();
        }

        function appendRow(name, displayExt, sizeStr, dimHtml, animationHtml, status, sizeKB) {
            let sizeColorClass = sizeKB > 150 ? 'text-error-detail' : 'text-primary';
            let formattedSize = `<span class='${sizeColorClass}'>${sizeStr}</span>`;

            let statusBlock = "";
            let targetTbody = "";

            if (status === "Pass") {
                passCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-pass'><span class='dot dot-pass'></span> Pass</div></div>`;
                targetTbody = 'tbody-pass';
            } else if (status === "Caution") {
                cautionCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-caution'><span class='dot dot-caution'></span> Caution</div></div>`;
                targetTbody = 'tbody-caution';
            } else {
                failCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-fail'><span class='dot dot-fail'></span> Fail</div></div>`;
                targetTbody = 'tbody-fail';
            }

            let tr = `<tr class='data-row'>
                <td>${name}</td>
                <td><span class='format-badge'>${displayExt}</span></td>
                <td>${formattedSize}</td>
                <td>${dimHtml}</td>
                <td>${animationHtml}</td>
                <td>${statusBlock}</td>
            </tr>`;

            document.getElementById(targetTbody).innerHTML += tr;
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
