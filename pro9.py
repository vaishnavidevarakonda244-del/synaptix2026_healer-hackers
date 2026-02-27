from flask import Flask, render_template_string, jsonify
import numpy as np
import time
import threading

app = Flask(__name__)

# ==========================================
# 1. THE BRAIN: Risk Analysis Logic
# ==========================================
class HealthEngine:
    def __init__(self):
        self.history = []

    def analyze(self, hr, bp_sys, spo2):
        # Multi-signal correlation: 
        # High HR + Low SpO2 is a much higher risk than just High HR alone.
        score = 0
        if hr > 100: score += 20
        if spo2 < 95: score += 40
        
        # Detect "Subtle" correlation (HR rising while SpO2 drops)
        if hr > 90 and spo2 < 96:
            score += 30 # The "Subtle" penalty
            
        status = "Normal"
        if score > 70: status = "CRITICAL"
        elif score > 40: status = "MODERATE RISK"
        
        return {"score": min(score, 100), "status": status}

engine = HealthEngine()

# ==========================================
# 2. THE SIMULATOR: "Virtual Wearable" 
# ==========================================
# This replaces the C++ hardware code
virtual_vitals = {"hr": 72, "bp": 120, "spo2": 98}

def simulate_sensors():
    global virtual_vitals
    t = 0
    while True:
        t += 1
        # Normal fluctuation
        virtual_vitals["hr"] = 72 + np.random.normal(0, 2)
        virtual_vitals["spo2"] = 98 + np.random.normal(0, 0.5)
        
        # Simulate a "Subtle Emergency" after 20 seconds
        if t > 20:
            virtual_vitals["hr"] += (t - 20) * 2 # Rising HR
            virtual_vitals["spo2"] -= (t - 20) * 0.5 # Dropping Oxygen
            
        time.sleep(1)

# Start simulation in the background
threading.Thread(target=simulate_sensors, daemon=True).start()

# ==========================================
# 3. THE BRIDGE: API Endpoints
# ==========================================
@app.route('/data')
def get_data():
    vitals = virtual_vitals
    analysis = engine.analyze(vitals["hr"], vitals["bp"], vitals["spo2"])
    return jsonify({**vitals, **analysis})

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Real-Time Health Monitor</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: sans-serif; background: #1a1a1a; color: white; text-align: center; }
                .gauge-container { display: flex; justify-content: space-around; padding: 20px; }
                .card { background: #2d2d2d; padding: 20px; border-radius: 15px; width: 30%; }
                #alert { font-weight: bold; font-size: 1.5em; padding: 20px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>Multi-Signal Health Dashboard</h1>
            <div id="alert">SYSTEM SCANNING...</div>
            
            <div class="gauge-container">
                <div class="card"><h3>Heart Rate</h3><h2 id="hr">--</h2></div>
                <div class="card"><h3>Oxygen (SpO2)</h3><h2 id="spo2">--</h2></div>
                <div class="card"><h3>Risk Score</h3><h2 id="score">--</h2></div>
            </div>

            <div style="width: 80%; margin: auto;">
                <canvas id="healthChart"></canvas>
            </div>

            <script>
                const ctx = document.getElementById('healthChart').getContext('2d');
                const chart = new Chart(ctx, {
                    type: 'line',
                    data: { labels: [], datasets: [
                        { label: 'Heart Rate', data: [], borderColor: 'red' },
                        { label: 'SpO2', data: [], borderColor: 'blue' }
                    ]}
                });

                function fetchData() {
                    fetch('/data').then(res => res.json()).then(data => {
                        document.getElementById('hr').innerText = Math.round(data.hr) + " BPM";
                        document.getElementById('spo2').innerText = Math.round(data.spo2) + "%";
                        document.getElementById('score').innerText = data.score + "%";
                        
                        const alertDiv = document.getElementById('alert');
                        alertDiv.innerText = data.status;
                        alertDiv.style.color = data.score > 50 ? 'red' : 'green';

                        // Update Chart
                        if (chart.data.labels.length > 20) chart.data.labels.shift();
                        chart.data.labels.push(new Date().toLocaleTimeString());
                        chart.data.datasets[0].data.push(data.hr);
                        chart.data.datasets[1].data.push(data.spo2);
                        chart.update();
                    });
                }
                setInterval(fetchData, 1000);
            </script>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)