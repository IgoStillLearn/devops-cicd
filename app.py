from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from flask_cors import CORS
import time
import csv
import os

app = Flask(__name__)
CORS(app)

DB_URL = "mysql+pymysql://root:admin123@jatelindo-db-svc:3306/db_operasional"
engine = create_engine(DB_URL, pool_pre_ping=True)

def init_db():
    """Bikin tabel duluan, terlepas CSV-nya ada atau nggak"""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS log_transaksi (
                trx_id INT PRIMARY KEY, 
                status VARCHAR(50),
                waktu VARCHAR(10)
            )
        """))
        conn.commit()

def sync_csv_to_db():
    if not os.path.exists('report.csv'):
        return
    with engine.connect() as conn:
        with open('report.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    conn.execute(text(
                        f"INSERT IGNORE INTO log_transaksi (trx_id, status, waktu) VALUES ({row['trx_id']}, '{row['status']}', '{row['waktu']}')"
                    ))
                except:
                    pass
        conn.commit()

@app.route('/api/metrics')
def metrics():
    try:
        init_db()          # 1. Pastikan tabel selalu ada
        sync_csv_to_db()   # 2. Injeksi data CSV
        
        with engine.connect() as conn:
            total_timeout = conn.execute(text("SELECT count(*) FROM log_transaksi WHERE status='timeout'")).scalar()
            total_sukses = conn.execute(text("SELECT count(*) FROM log_transaksi WHERE status='sukses'")).scalar()
            
        alert_status = "AMAN"
        alert_color = "0xFF4ade80" # Hijau format Flutter
        
        if total_timeout >= 3:
            alert_status = "KRITIS: Lonjakan Timeout!"
            alert_color = "0xFFef4444" # Merah format Flutter

        return jsonify({
            "status": "DB Sync Berhasil",
            "timeout_count": total_timeout,
            "sukses_count": total_sukses,
            "alert": alert_status,
            "color": alert_color
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    time.sleep(5)
    app.run(host='0.0.0.0', port=80)
