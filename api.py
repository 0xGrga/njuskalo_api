from njuskalo import *
njuskalo = njuskalo()

from flask import Flask, jsonify, request
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

@app.get("/")
@cache.cached(timeout=600)
def load_all_gpus():
    filter = request.args.get("filter")
    return jsonify(njuskalo.load_gpus(filter = filter))

@app.get("/api")
def load_gpus():
    min_price = request.args.get("min")
    max_price = request.args.get("max")
    locationID = request.args.get("locationID")
    search = request.args.get("search")
    filter = json.loads(request.args.get("filter").lower())
    return jsonify(njuskalo.load_gpus(search = search, min_price = min_price, max_price = max_price, locationID = locationID, filter = filter))

@app.get("/locations")
def loactions():
    return {
        "Bjelovarsko-bilogorska": 1150,
        "Brodsko-posavska": 1151,
        "Dubrova\u010dko-neretvanska": 1152,
        "Istarska": 1154,
        "Karlova\u010dka": 1155,
        "---": 0,
        "Koprivni\u010dko-kri\u017eeva\u010dka": 1156,
        "Krapinsko-zagorska": 1157,
        "Li\u010dko-senjska": 1158,
        "Me\u0111imurska": 1159,
        "Osje\u010dko-baranjska": 1160,
        "Po\u017ee\u0161ko-slavonska": 1161,
        "Primorsko-goranska": 1162,
        "Sisa\u010dko-moslava\u010dka": 1163,
        "Splitsko-dalmatinska": 1164,
        "\u0160ibensko-kninska": 1165,
        "Vara\u017edinska": 1166,
        "Viroviti\u010dko-podravska": 1167,
        "Vukovarsko-srijemska": 1168,
        "Zadarska": 1169,
        "Grad Zagreb": 1153,
        "Zagreba\u010dka": 1170,
        "Izvan Hrvatske - Unutar EU": -30,
        "Izvan Hrvatske - Izvan EU": -40
    }



app.run(debug=True)
