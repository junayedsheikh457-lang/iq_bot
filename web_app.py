import json
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
CFG = json.loads(Path('config.json').read_text(encoding='utf-8'))
STATE = {'mode': CFG.get('mode','paper'), 'instrument': CFG['instrument'], 'timeframe': CFG['timeframe'], 'running': False, 'last_signal': None, 'current_stake': CFG['stakes'][0], 'consecutive_losses': 0}

@app.get('/')
def home():
    return '''<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>IQ Bot</title><style>body{font-family:Arial;background:#0b1020;color:#fff;margin:0;padding:20px} .card{max-width:760px;margin:auto;background:#151c33;border-radius:16px;padding:22px} .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.item{background:#0e1529;padding:14px;border-radius:12px}button{padding:12px 18px;border:0;border-radius:10px;margin-right:8px;cursor:pointer}</style></head><body><div class='card'><h1>IQ Bot</h1><div class='grid'><div class='item'>Instrument<br><b id='instrument'></b></div><div class='item'>Timeframe<br><b id='tf'></b></div><div class='item'>Mode<br><b id='mode'></b></div><div class='item'>Stake<br><b id='stake'></b></div><div class='item'>Signal<br><b id='signal'></b></div><div class='item'>Losses<br><b id='losses'></b></div></div><p><button onclick='setRun(true)'>Start</button><button onclick='setRun(false)'>Stop</button></p><p id='status'></p></div><script>async function refresh(){let s=await fetch('/api/status').then(r=>r.json());for(let k of ['instrument','tf','mode','stake','signal','losses'])document.getElementById(k).textContent=s[k==='tf'?'timeframe':k==='stake'?'current_stake':k==='signal'?'last_signal':k==='losses'?'consecutive_losses':k]??'-';document.getElementById('status').textContent=s.running?'Bot monitor: RUNNING':'Bot monitor: STOPPED'}async function setRun(v){await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({running:v})});refresh()}refresh();setInterval(refresh,3000)</script></body></html>'''

@app.get('/api/status')
def status():
    return jsonify(STATE)

@app.post('/api/run')
def run_toggle():
    data=request.get_json(silent=True) or {}
    STATE['running']=bool(data.get('running',False))
    return jsonify(STATE)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(__import__('os').environ.get('PORT','10000')))
