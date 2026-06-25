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
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        /* Global & Reset */
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Manrope', sans-serif; font-weight: 400; }
        body { background-color: #FAFAFA; color: #0F172A; padding-bottom: 250px; }
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
        
        header h1 { 
            color: #FFFFFF; 
            font-size: 44px; 
            font-family: 'Century Gothic', Arial, sans-serif; 
            font-weight: 400; 
            letter-spacing: 2px; 
        }

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
        .upload-text { color: #0F172A; font-size: 15px; font-weight: 400; letter-spacing: 0.3px; }
        .upload-subtext { color: #64748B; font-size: 13px; margin-top: 6px; font-weight: 400; }
        #file-input { display: none; }

        /* Summary Dashboard */
        .summary-dashboard {
            display: none; 
            grid-template-columns: repeat(2, 1fr);
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
        .summary-value { font-size: 28px; font-weight: 400; color: #0F172A; line-height: 1; }
        .summary-label { 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            gap: 6px; 
            font-size: 11px; 
            color: #64748B; 
            text-transform: uppercase; 
            font-weight: 400; 
            letter-spacing: 0.5px; 
            margin-top: 10px; 
        }

        /* Action Bar */
        .action-bar-container {
            display: none;
            justify-content: center;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        .clear-btn {
            background-color: #111827;
            color: #FFFFFF;
            border: none;
            padding: 12px 24px;
            font-size: 13px;
            font-weight: 400;
            border-radius: 0px; 
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: background-color 0.2s, transform 0.1s;
        }
        .clear-btn:hover { background-color: #334155; }
        .clear-btn:active { transform: scale(0.98); }

        /* Data Tables */
        .table-wrapper {
            background: transparent;
            margin-bottom: 3rem;
            display: none; 
        }
        
        .table-header-title {
            padding: 0 0 12px 0;
            font-size: 18px;
            font-weight: 400;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .table-container {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 0px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            overflow: visible; 
        }

        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        
        /* Unified Left Alignment for Headers */
        th { 
            background-color: #2C0A38; 
            color: #FFFFFF; 
            padding: 10px 16px; 
            font-size: 11px; 
            font-weight: 400; 
            text-transform: uppercase; 
            letter-spacing: 0.05em; 
            text-align: center; 
            border-bottom: none; 
            white-space: nowrap; 
        }

        .th-content { display: flex; align-items: center; gap: 8px; }
        
        /* Left Align ONLY the first column */
        th:nth-child(1) { text-align: left; }
        th:not(:nth-child(1)) .th-content { justify-content: center; }
        .th-content svg { width: 14px; height: 14px; fill: #FFFFFF; }
        
        /* Unified Base Alignment & Text Style for All Data Cells */
        td { 
            padding: 14px 16px; 
            font-size: 13px; 
            color: #0F172A; 
            text-align: center; 
            border-bottom: 1px solid #E2E8F0; 
            vertical-align: middle; 
            word-break: break-word; 
            overflow-wrap: anywhere;
            font-weight: 400; 
        }

        /* Left Align ONLY the first column */
        td:nth-child(1) { text-align: left; }

        tr:last-child td { border-bottom: none; }
        tr.data-row:hover td { background-color: #F8FAFC !important; cursor: default; }

        th:nth-child(1), td:nth-child(1) { width: 28%; font-weight: 400; } 
        th:nth-child(2), td:nth-child(2) { width: 13%; } 
        th:nth-child(3), td:nth-child(3) { width: 12%; } 
        th:nth-child(4), td:nth-child(4) { width: 15%; } 
        th:nth-child(5), td:nth-child(5) { width: 14%; } 
        th:nth-child(6), td:nth-child(6) { width: 18%; } 

        .status-container { display: flex; flex-direction: column; gap: 4px; }
        .status-main { display: flex; align-items: center; justify-content: center; gap: 8px; font-weight: 400; font-size: 13px; }
        
        /* Three distinct colors for hierarchy */
        .status-text-pass { color: #22C55E; }
        .status-text-review { color: #3B82F6; } 
        .status-text-caution { color: #F59E0B; } 
        .status-text-fail { color: #DC2626; }    

        /* Specific dimension highlight colors */
        .text-review-detail { color: #3B82F6; font-weight: 400; }
        .text-caution-detail { color: #DC2626; font-weight: 400; }
        .text-error-detail { color: #DC2626; font-weight: 400; }
        
        /* HOVER PREVIEW CSS */
        .filename-wrapper {
            position: relative;
            display: inline-block;
            cursor: pointer;
            transition: color 0.2s;
            max-width: 100%;
            word-break: break-all;
        }
        .filename-wrapper:hover {
            color: #3B82F6; 
        }
        .preview-tooltip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            left: 100%;
            top: -15px; 
            margin-left: 15px;
            z-index: 1000;
            background: #FFFFFF;
            padding: 8px;
            border: 1px solid #CBD5E1;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            transition: opacity 0.2s ease, visibility 0.2s ease;
            pointer-events: none;
            width: max-content;
        }
        .preview-tooltip img {
            max-width: 220px; 
            max-height: 220px;
            display: block;
            object-fit: contain;
            background-color: #f0f0f0;
            background-image: linear-gradient(45deg, #e4e4e4 25%, transparent 25%), linear-gradient(-45deg, #e4e4e4 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #e4e4e4 75%), linear-gradient(-45deg, transparent 75%, #e4e4e4 75%);
            background-size: 10px 10px;
            background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
        }
        .preview-tooltip::before {
            content: ''; position: absolute; top: 20px; left: -6px; 
            border-width: 6px 6px 6px 0; border-style: solid;
            border-color: transparent #CBD5E1 transparent transparent;
        }
        .preview-tooltip::after {
            content: ''; position: absolute; top: 21px; left: -5px; 
            border-width: 5px 5px 5px 0; border-style: solid;
            border-color: transparent #FFFFFF transparent transparent;
        }
        .filename-wrapper:hover .preview-tooltip {
            visibility: visible;
            opacity: 1;
        }
        
        /* App Footer Styling */
        .app-footer {
            margin-top: 5rem;
            padding-top: 24px;
            border-top: 1px solid #E2E8F0;
            text-align: center;
            font-size: 12px;
            color: #64748B;
            line-height: 1.6;
            letter-spacing: 0.5px;
        }
        .app-footer strong {
            color: #0F172A;
            font-weight: 600;
        }
        .app-footer-team {
            font-size: 11px;
            text-transform: uppercase;
            color: #94A3B8;
            font-weight: 500;
            margin-top: 2px;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <header id="main-header"><h1>Display Validator Tool</h1></header>
    
    <div class="container">
        
        <div class="summary-dashboard" id="summary-dashboard">
            <div class="summary-card">
                <div class="summary-value" style="color: #22C55E;" id="count-pass">0</div>
                <div class="summary-label">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" class="val-pass"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Compliant
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-value" style="color: #EF4444;" id="count-fail">0</div>
                <div class="summary-label">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" class="val-fail"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Non-Compliant
                </div>
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

        <script>
            const thRowHTML = `
                <tr>
                    <th><div class="th-content"><svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg> FILE NAME</div></th>
                    <th><div class="th-content"><svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z"/></svg> FILE TYPE</div></th>
                    <th><div class="th-content"><svg viewBox="0 0 24 24"><path d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zM5 15h14v3H5z"/></svg> SIZE</div></th>
                    <th><div class="th-content"><svg viewBox="0 0 24 24"><path d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zm-8-2h6v-2h-6v2zm-2-4h8v-2h-8v2zm-2-4h10V7H9v2z"/></svg> DIMENSIONS</div></th>
                    <th><div class="th-content"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg> ANIMATION</div></th>
                    <th><div class="th-content"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg> STATUS</div></th>
                </tr>
            `;
        </script>

        <div class="table-wrapper" id="wrapper-fail">
            <div style="padding: 0 0 12px 0;">
                <div class="table-header-title" style="padding-bottom: 4px;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                        <line x1="12" y1="9" x2="12" y2="13"></line>
                        <line x1="12" y1="17" x2="12.01" y2="17"></line>
                    </svg> 
                    Non-Compliant
                </div>
                <div id="legend-container" style="display: none; font-size: 13px; color: #0F172A; font-weight: 400; margin-top: 4px; gap: 24px; align-items: center; line-height: 1.4;">
                    <span id="legend-mismatch" style="display: none;"><strong style="font-weight: 600;">Dimension Mismatch:</strong> Filename dimensions do not match the actual asset dimensions.</span>
                    <span id="legend-review" style="display: none;"><strong style="font-weight: 600;">Review:</strong> Non-standard dimensions.</span>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead id="thead-fail"></thead>
                    <tbody id="tbody-fail"></tbody>
                </table>
            </div>
        </div>

        <div class="table-wrapper" id="wrapper-pass">
            <div class="table-header-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                Compliant
            </div>
            <div class="table-container">
                <table>
                    <thead id="thead-pass"></thead>
                    <tbody id="tbody-pass"></tbody>
                </table>
            </div>
        </div>

        <div class="action-bar-container" id="action-bar">
            <button class="clear-btn" onclick="clearResults()">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                Clear All Results
            </button>
        </div>

        <footer class="app-footer">
            <div>Made by <strong>KIRANKUMAR</strong></div>
            <div class="app-footer-team">MiQ Ad Ops Team</div>
        </footer>

    </div>

    <script>
        document.getElementById('thead-fail').innerHTML = thRowHTML;
        document.getElementById('thead-pass').innerHTML = thRowHTML;

        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('file-input');
        
        let processedFiles = new Set();
        let compliantCount = 0;
        let nonCompliantCount = 0;
        
        let hasMismatchIssue = false;
        let hasReviewIssue = false;

        let activePreviewURLs = [];

        let passRows = [];
        let reviewRows = [];
        let alertRows = [];
        let failRows = [];

        const MASTER_DIMENSIONS = [
            "120x600", "160x600", "250x250", "300x250", "300x50", "300x600", 
            "320x100", "320x480", "320x50", "336x280", "468x60", "480x320", 
            "728x90", "970x250", "970x90", "768x1024", "1024x768"
        ];

        const iconPass = `<svg width="18" height="18" viewBox="0 0 24 24" fill="#22C55E" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11"/><path d="M8 12.5L10.5 15L16 9" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
        const iconReview = `<svg width="18" height="18" viewBox="0 0 24 24" fill="#3B82F6" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11"/><path d="M12 10V16M12 7H12.01" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
        const iconAlert = `<svg width="18" height="18" viewBox="0 0 24 24" fill="#F59E0B" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11"/><path d="M12 7V13M12 17H12.01" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
        const iconFail = `<svg width="18" height="18" viewBox="0 0 24 24" fill="#DC2626" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11"/><path d="M15 9L9 15M9 9L15 15" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

        function updateSummary() {
            document.getElementById('count-pass').innerText = compliantCount;
            document.getElementById('count-fail').innerText = nonCompliantCount;
            
            let total = compliantCount + nonCompliantCount;
            
            if (total > 0) {
                document.getElementById('summary-dashboard').style.display = "grid";
                document.getElementById('action-bar').style.display = "flex";
                
                document.getElementById('wrapper-fail').style.display = nonCompliantCount > 0 ? "block" : "none";
                document.getElementById('wrapper-pass').style.display = compliantCount > 0 ? "block" : "none";
                
                if (hasMismatchIssue || hasReviewIssue) {
                    document.getElementById('legend-container').style.display = "flex";
                    document.getElementById('legend-mismatch').style.display = hasMismatchIssue ? "block" : "none";
                    document.getElementById('legend-review').style.display = hasReviewIssue ? "block" : "none";
                } else {
                    document.getElementById('legend-container').style.display = "none";
                }
                
            } else {
                document.getElementById('summary-dashboard').style.display = "none";
                document.getElementById('action-bar').style.display = "none";
                document.getElementById('wrapper-fail').style.display = "none";
                document.getElementById('wrapper-pass').style.display = "none";
                document.getElementById('legend-container').style.display = "none";
            }
        }

        function clearResults() {
            processedFiles.clear();
            compliantCount = 0; nonCompliantCount = 0;
            passRows = []; reviewRows = []; alertRows = []; failRows = [];
            
            hasMismatchIssue = false;
            hasReviewIssue = false;
            
            activePreviewURLs.forEach(url => URL.revokeObjectURL(url));
            activePreviewURLs = [];

            document.getElementById('tbody-pass').innerHTML = "";
            document.getElementById('tbody-fail').innerHTML = "";
            fileInput.value = ""; 
            updateSummary();
            
            try { document.getElementById('main-header').scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch(e) {}
            window.scrollTo({ top: 0, behavior: 'smooth' });
            try { window.parent.scrollTo({ top: 0, behavior: 'smooth' }); } catch(e) {}
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
                const objectUrl = URL.createObjectURL(file);
                
                img.onload = () => {
                    resolve({ width: img.width, height: img.height, valid: true, previewUrl: objectUrl });
                };
                img.onerror = () => {
                    URL.revokeObjectURL(objectUrl);
                    resolve({ valid: false, previewUrl: null });
                };
                img.src = objectUrl;
            });
            const timeoutPromise = new Promise((resolve) => setTimeout(() => resolve({ valid: false, timeout: true, previewUrl: null }), 2000));
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

                let status = "Pass", animationHtml = "Static Image", errors = [];
                let sizeKB = file.size / 1024;
                let sizeStr = sizeKB.toFixed(1) + " KB";
                
                let rawExt = file.name.split('.').pop();
                let logicExt = rawExt.toUpperCase();
                let displayExt = "." + rawExt.toLowerCase();
                
                let dimHtml = "-";
                let dimHasWarning = false;
                let dimHasError = false;
                
                if (sizeKB > 5120) { 
                    status = "Fail";
                    errors.push("File exceeds 5MB hard limit");
                    appendRow(file.name, displayExt, sizeStr, dimHtml, animationHtml, status, errors, sizeKB, null);
                    continue;
                }

                if (!allowedMimeTypes.includes(file.type) && !['JPG', 'JPEG', 'PNG', 'GIF'].includes(logicExt)) {
                    status = "Fail"; 
                    errors.push(`Invalid format: ${displayExt}`);
                    appendRow(file.name, displayExt, sizeStr, dimHtml, animationHtml, status, errors, sizeKB, null);
                    continue;
                }
                
                if (sizeKB > 150) { 
                    status = "Fail"; 
                    errors.push("File size exceeds 150 KB limit");
                }

                let imgInfo = await getImageInfo(file);
                let finalPreviewUrl = imgInfo.previewUrl;
                
                if (finalPreviewUrl) {
                    activePreviewURLs.push(finalPreviewUrl);
                }

                if (!imgInfo.valid) {
                    status = "Fail";
                    dimHasError = true;
                    dimHtml = `<span class='text-error-detail'>Unreadable</span>`;
                    errors.push("Image file is corrupted or unreadable");
                } else {
                    let actualW = imgInfo.width;
                    let actualH = imgInfo.height;
                    let actualDimStr = `${actualW}x${actualH}`;

                    let isStandard = MASTER_DIMENSIONS.includes(actualDimStr);
                    let isNearMiss = false;
                    let closestStandard = "";

                    if (!isStandard) {
                        for (let sDim of MASTER_DIMENSIONS) {
                            let [sW, sH] = sDim.split('x').map(Number);
                            if (Math.abs(actualW - sW) <= 4 && Math.abs(actualH - sH) <= 4) {
                                isNearMiss = true;
                                closestStandard = sDim;
                                break;
                            }
                        }
                    }

                    let nameRegex = /(?<!\d)(\d+)\s*[xX]\s*(\d+)(?!\d)/;
                    let nameMatch = file.name.match(nameRegex);
                    let nameDimStr = nameMatch ? `${nameMatch[1]}x${nameMatch[2]}` : null;

                    let handledAsAlert = false;
                    let mismatchTriggered = false;

                    if (isStandard) {
                        if (nameDimStr && nameDimStr !== actualDimStr) {
                            if (status === "Pass") status = "Alert"; 
                            dimHasWarning = true;
                            errors.push(`Dimension Mismatch`);
                            mismatchTriggered = true;
                            hasMismatchIssue = true;
                        }
                    } else {
                        if (nameDimStr && nameDimStr !== actualDimStr) {
                            if (status === "Pass") status = "Alert"; 
                            dimHasWarning = true;
                            errors.push(`Dimension Mismatch`);
                            handledAsAlert = true;
                            mismatchTriggered = true;
                            hasMismatchIssue = true;
                        }
                        
                        if (isNearMiss && !mismatchTriggered) {
                            if (status === "Pass") status = "Alert"; 
                            dimHasWarning = true;
                            errors.push(`Invalid Dimension`);
                            handledAsAlert = true;
                        }

                        if (!handledAsAlert) {
                            if (status !== "Fail") {
                                status = "Review"; 
                                dimHasWarning = true; 
                                hasReviewIssue = true;
                            } else {
                                dimHasError = true; 
                            }
                        }
                    }

                    if (dimHasWarning) {
                        if (status === "Review") {
                            dimHtml = `<span class='text-review-detail'>${actualW} × ${actualH}</span>`;
                        } else {
                            dimHtml = `<span class='text-caution-detail'>${actualW} × ${actualH}</span>`;
                        }
                    } else if (status === "Fail" && dimHasError) {
                        dimHtml = `<span class='text-error-detail'>${actualW} × ${actualH}</span>`;
                    } else {
                        dimHtml = `${actualW} × ${actualH}`;
                    }
                }

                if (logicExt === "GIF" && imgInfo.valid) { 
                    let gifData = await extractGIFData(file);
                    if (gifData.isAnimated) {
                        let cSec = gifData.duration;
                        let rawLoops = gifData.loops;
                        let displayLoops = rawLoops < 0 ? 1 : rawLoops; 

                        if (rawLoops === 0) {
                            animationHtml = `<span class='text-error-detail'>Infinite</span>`; 
                            status = "Fail";
                            errors.push("Animates over 30 s");
                        } else {
                            let tSec = cSec * displayLoops;
                            if (tSec > 30) { 
                                animationHtml = `<span class='text-error-detail'>${tSec.toFixed(1)} s</span>`;
                                status = "Fail"; 
                                errors.push(`Animates over 30 s`);
                            } else {
                                animationHtml = `${tSec.toFixed(1)} s`;
                            }
                        }
                    }
                }

                appendRow(file.name, displayExt, sizeStr, dimHtml, animationHtml, status, errors, sizeKB, finalPreviewUrl);
            }

            document.getElementById('tbody-pass').innerHTML = passRows.join('');
            document.getElementById('tbody-fail').innerHTML = reviewRows.join('') + alertRows.join('') + failRows.join('');

            document.getElementById('upload-main-text').innerText = "Drag & drop your creatives here";
            document.getElementById('upload-icon-svg').style.color = "#64748B";
            updateSummary();
        }

        function appendRow(name, displayExt, sizeStr, dimHtml, animationHtml, status, errors, sizeKB, previewUrl) {
            let formattedSize = sizeKB > 150 ? `<span class='text-error-detail'>${sizeStr}</span>` : sizeStr;

            let finalMessages = [];
            errors.forEach(e => finalMessages.push(`<div class='text-error-detail' style='font-size:12px; line-height:1.25;'>• ${e}</div>`));
            let msgHtml = finalMessages.join("");

            let statusBlock = "";

            if (status === "Pass") {
                compliantCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-pass'>${iconPass} Pass</div></div>`;
            } else if (status === "Review") {
                nonCompliantCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-review'>${iconReview} Review</div>${msgHtml}</div>`;
            } else if (status === "Alert") {
                nonCompliantCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-caution'>${iconAlert} Alert</div>${msgHtml}</div>`;
            } else {
                nonCompliantCount++;
                statusBlock = `<div class='status-container'><div class='status-main status-text-fail'>${iconFail} Fail</div>${msgHtml}</div>`;
            }

            let filenameHtml = name;
            if (previewUrl) {
                filenameHtml = `
                <div class='filename-wrapper'>
                    ${name}
                    <div class='preview-tooltip'>
                        <img src="${previewUrl}" alt="Preview">
                    </div>
                </div>
                `;
            }

            let tr = `<tr class='data-row'>
                <td>${filenameHtml}</td>
                <td>${displayExt}</td>
                <td>${formattedSize}</td>
                <td>${dimHtml}</td>
                <td>${animationHtml}</td>
                <td>${statusBlock}</td>
            </tr>`;

            if (status === "Pass") {
                passRows.push(tr);
            } else if (status === "Review") {
                reviewRows.push(tr);
            } else if (status === "Alert") {
                alertRows.push(tr);
            } else {
                failRows.push(tr);
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
