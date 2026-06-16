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
                <thead><tr><th>File Name</th><th>File
