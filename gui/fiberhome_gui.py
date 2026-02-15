import threading
import time
import webbrowser
import sys
import hashlib
import re
import os
import subprocess
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# --- Core Logic ---
UPPER = "ACDFGHJMNPRSTUWXY"
LOWER = "abcdfghjkmpstuwxy"
DIGIT = "2345679"
SYMBOL = "!@$&%"

def mac_to_pass(mac: str) -> str:
    mac = mac.upper()
    if not re.fullmatch(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac):
        return ""

    md5 = hashlib.md5()
    md5.update(mac.encode())
    md5.update(b"AEJLY")
    digest = md5.hexdigest()

    vals = []
    for c in digest[:20]:
        if '0' <= c <= '9':
            vals.append(ord(c) - ord('0'))
        elif 'a' <= c <= 'f':
            vals.append(ord(c) - ord('a') + 10)
        elif 'A' <= c <= 'F':
            vals.append(ord(c) - ord('A') + 10)
        else:
            vals.append(0)

    password = [''] * 16
    for i in range(16):
        v = vals[i]
        case_type = v % 4
        if case_type == 0: password[i] = UPPER[(v * 2) % 17]
        elif case_type == 1: password[i] = LOWER[(v * 2 + 1) % 17]
        elif case_type == 2: password[i] = DIGIT[6 - (v % 7)]
        elif case_type == 3: password[i] = SYMBOL[4 - (v % 5)]

    p0 = (vals[16] + 1) % 16
    p1 = (vals[17] + 1) % 16
    while p1 == p0: p1 = (p1 + 1) % 16
    p2 = (vals[18] + 1) % 16
    while p2 == p0 or p2 == p1: p2 = (p2 + 1) % 16
    p3 = (vals[19] + 1) % 16
    while p3 == p0 or p3 == p1 or p3 == p2: p3 = (p3 + 1) % 16

    password[p0] = UPPER[(vals[16] * 2) % 17]
    password[p1] = LOWER[(vals[17] * 2 + 1) % 17]
    password[p2] = DIGIT[6 - (vals[18] % 7)]
    password[p3] = SYMBOL[4 - (vals[19] % 5)]

    return ''.join(password)

def get_router_mac():
    try:
        if sys.platform == 'win32':
            # Get default gateway
            result = subprocess.run('ipconfig', capture_output=True, text=True)
            gateway_ip = None
            for line in result.stdout.splitlines():
                # Flexible matching for "Default Gateway"
                if "Default Gateway" in line or "Passerelle" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        ip = parts[-1].strip()
                        if ip: 
                            gateway_ip = ip
                            break
            
            if not gateway_ip:
                # Fallback: assume typical home router IPs
                gateway_ip = "192.168.1.1" # Most common

            # Get ARP table
            arp_result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            mac = None
            
            # Prioritize matching the exact gateway IP
            for line in arp_result.stdout.splitlines():
                if gateway_ip and gateway_ip in line:
                     match = re.search(r'([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}', line)
                     if match:
                         mac = match.group(0).replace('-', ':').upper()
                         # Exclude broadcasts
                         if mac == "FF:FF:FF:FF:FF:FF": mac = None
                         else: return mac

            # If not found specifically, take the first dynamic entry that looks like a router (usually ends in .1)
            for line in arp_result.stdout.splitlines():
                if "dynamic" in line.lower() or "dynamique" in line.lower():
                     match = re.search(r'([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}', line)
                     if match:
                         potential_mac = match.group(0).replace('-', ':').upper()
                         if potential_mac != "FF:FF:FF:FF:FF:FF" and not potential_mac.startswith("01:00:5E"):
                             return potential_mac

        return None
    except Exception as e:
        print(f"Error detecting MAC: {e}")
        return None

# --- HTML Content ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fiberhome Generator</title>
    <style>
        :root {
            --primary: #6a11cb;
            --secondary: #2575fc;
            --bg: #111;
            --card: rgba(255, 255, 255, 0.05);
            --border: rgba(255, 255, 255, 0.1);
            --text: #eee;
        }
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            width: 90%;
            max-width: 450px;
            background: var(--card);
            border: 1px solid var(--border);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        h1 {
            background: linear-gradient(to right, #fff, #bbb);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin: 0 auto 0.5rem;
        }
        .input-group {
            display: flex;
            gap: 10px;
            margin: 1.5rem 0;
        }
        input {
            flex: 1;
            padding: 12px;
            background: rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #fff;
            text-align: center;
            font-size: 1rem;
            outline: none;
        }
        input:focus { border-color: var(--secondary); }
        button {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }
        .detect-btn {
            background: rgba(255,255,255,0.1);
            color: #ccc;
        }
        .detect-btn:hover { background: rgba(255,255,255,0.2); }
        .submit-btn {
            width: 100%;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            color: white;
            font-size: 1rem;
        }
        .submit-btn:hover { opacity: 0.9; transform: translateY(-1px); }
        
        #result {
            margin-top: 1.5rem;
            padding: 1rem;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            display: none;
            cursor: pointer;
        }
        #result code {
            display: block;
            font-size: 1.4rem;
            color: #4cd137;
            margin-top: 5px;
        }
        .error { color: #ff4757; margin-top: 10px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Fiberhome Local</h1>
        <div style="color:#888; margin-bottom: 20px; font-size: 0.9rem;">Standalone Generator</div>
        
        <div class="input-group">
            <input type="text" id="mac" placeholder="AA:BB:CC:DD:EE:FF" maxlength="17">
            <button class="detect-btn" id="detect" title="Auto-Detect Router">Detect</button>
        </div>
        
        <button class="submit-btn" id="generate">Generate Password</button>
        
        <div id="result" title="Click to Copy">
            <div style="font-size:0.8rem; color:#aaa;">Result</div>
            <code id="password"></code>
        </div>
        <div id="error" class="error"></div>
    </div>

    <script>
        const macInput = document.getElementById('mac');
        const detectBtn = document.getElementById('detect');
        const genBtn = document.getElementById('generate');
        const resultDiv = document.getElementById('result');
        const passCode = document.getElementById('password');
        const errorDiv = document.getElementById('error');

        // Auto-format
        macInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
            if (val.length > 12) val = val.substring(0, 12);
            let formatted = '';
            for(let i=0; i<val.length; i++) {
                if(i>0 && i%2===0) formatted += ':';
                formatted += val[i];
            }
            e.target.value = formatted;
        });

        detectBtn.addEventListener('click', async () => {
             detectBtn.innerText = '...';
             detectBtn.disabled = true;
             errorDiv.innerText = '';
             try {
                 const res = await fetch('/api/detect');
                 const data = await res.json();
                 if (data.mac) {
                     macInput.value = data.mac;
                 } else {
                     errorDiv.innerText = 'Could not detect router MAC.';
                 }
             } catch(e) {
                 errorDiv.innerText = 'Detection failed.';
             }
             detectBtn.innerText = 'Detect';
             detectBtn.disabled = false;
        });

        genBtn.addEventListener('click', async () => {
            const mac = macInput.value;
            if (mac.length < 17) {
                errorDiv.innerText = 'Invalid MAC format';
                return;
            }
            try {
                const res = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mac})
                });
                const data = await res.json();
                if(data.password) {
                    passCode.innerText = data.password;
                    resultDiv.style.display = 'block';
                    errorDiv.innerText = '';
                } else {
                    errorDiv.innerText = 'Invalid MAC.';
                    resultDiv.style.display = 'none';
                }
            } catch(e) {
                errorDiv.innerText = 'Server error.';
            }
        });
        
        resultDiv.addEventListener('click', () => {
             navigator.clipboard.writeText(passCode.innerText);
             const old = passCode.innerText;
             passCode.innerText = 'Copied!';
             setTimeout(() => passCode.innerText = old, 1000);
        });
    </script>
</body>
</html>
"""

# --- Flask Routes ---
@app.route('/')
def index():
    return INDEX_HTML

@app.route('/api/detect')
def api_detect():
    mac = get_router_mac()
    return jsonify({'mac': mac})

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json()
    mac = data.get('mac', '')
    pwd = mac_to_pass(mac)
    return jsonify({'password': pwd})

def open_browser():
    time.sleep(1.5) # Wait for server to start
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    # Run server
    app.run(host='127.0.0.1', port=5000, debug=False)
