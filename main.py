from flask import Flask, render_template, request
import subprocess, socket
from geoip import get_country

app = Flask(__name__)

def ping_host(host):
    try:
        ip = socket.gethostbyname(host)
        result = subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stats = {"min": "-", "avg": "-", "max": "-", "loss": "100%", "ip": ip, "country": get_country(ip)}
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if "min/avg/max" in line:
                    parts = line.split('=')[1].strip().split()[0].split('/')
                    stats.update({"min": parts[0], "avg": parts[1], "max": parts[2]})
                if "packet loss" in line:
                    stats["loss"] = line.split(",")[2].strip()
        return stats
    except Exception as e:
        return {"ip": "-", "min": "-", "avg": "-", "max": "-", "loss": "100%", "country": "Unknown"}

@app.route("/")
def index():
    with open("domain.txt") as f:
        domains = [line.strip() for line in f if line.strip()]
    results = [{"domain": d, **ping_host(d)} for d in domains]
    results.sort(key=lambda x: float(x["avg"]) if x["avg"] != "-" else 9999)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)