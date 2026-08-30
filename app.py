from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Persiapan string koneksi (Besok kita sesuaikan dengan kredensial asli)
# ENGINE = create_engine("mysql+pymysql://user:pass@host/db_jatelindo")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; }
    .glass-card { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); padding: 50px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); text-align: center; }
    h1 { margin-top: 0; font-size: 28px; font-weight: 600; }
    p { font-size: 16px; opacity: 0.8; }
    .metric-box { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; margin-top: 20px; font-family: monospace; font-size: 18px; }
  </style>
</head>
<body>
  <div class="glass-card">
    <h1>Jatelindo Monitoring UI</h1>
    <p>GitOps Automated • Python SQL Edition • v6.1</p>
    <div class="metric-box" id="metrics">Menunggu koneksi Database...</div>
  </div>
  <script>
    setInterval(() => {
      fetch('/api/metrics').then(r => r.json()).then(data => {
        document.getElementById('metrics').innerHTML = 
          `Status DB: <b style="color:#facc15">${data.status}</b><br>Timeout Transaksi: <b>${data.timeout_count}</b>`;
      });
    }, 2000);
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/api/metrics')
def metrics():
    # Logika SQL lu bakal dieksekusi di sini besok
    # with ENGINE.connect() as conn:
    #     result = conn.execute(text("SELECT count(*) FROM transaksi WHERE status='timeout'"))
    
    return jsonify({
        "status": "Pending SQL Connection",
        "timeout_count": "Menyiapkan Dataset CSV..."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
