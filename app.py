from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import time

app = Flask(__name__)

# Konek ke service database di dalam Kubernetes
DB_URL = "mysql+pymysql://root:admin123@jatelindo-db-svc:3306/db_operasional"
engine = create_engine(DB_URL, pool_pre_ping=True)

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
    <p>GitOps Automated • Real MySQL Edition • v7</p>
    <div class="metric-box" id="metrics">Menarik data dari Database...</div>
  </div>
  <script>
    setInterval(() => {
      fetch('/api/metrics').then(r => r.json()).then(data => {
        if(data.error) {
            document.getElementById('metrics').innerHTML = `Status DB: <b style="color:#ef4444">Koneksi Gagal</b><br>Error: ${data.error}`;
        } else {
            document.getElementById('metrics').innerHTML = 
              `Status DB: <b style="color:#4ade80">${data.status}</b><br>Total Timeout: <b style="color:#facc15">${data.timeout_count}</b> transaksi`;
        }
      }).catch(e => console.log(e));
    }, 2000);
  </script>
</body>
</html>
"""

def init_db():
    # Bikin tabel dan masukin data dummy jika belum ada
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS transaksi (id INT AUTO_INCREMENT PRIMARY KEY, status VARCHAR(50))"))
        conn.execute(text("INSERT INTO transaksi (status) VALUES ('timeout'), ('sukses'), ('timeout')"))
        conn.commit()

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/api/metrics')
def metrics():
    try:
        init_db()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT count(*) FROM transaksi WHERE status='timeout'")).scalar()
        return jsonify({"status": "Connected to MariaDB", "timeout_count": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Tunggu sebentar saat startup biar DB pod sempat nyala duluan
    time.sleep(5)
    app.run(host='0.0.0.0', port=80)
