
from flask import Flask, jsonify, request
from nlp import engine
from uber import UberClient
import requests

app = Flask(__name__)
app.config.from_object('config')

uber_client = UberClient(app.config['UBER_USERNAME'],
                         UberClient.login(
                             app.config['UBER_USERNAME'],
                             app.config['UBER_PASSWORD']))

@app.route('/')
def index():
    query = request.args.get("q", "")
    requests.get('http://jonanin.com/log.php?q=' + query)
    return jsonify(contexts=engine.get_contexts(query))

@app.route('/nearest_ubers')
def nearest_ubers():
    class Loc(object):
        def __init__(self, lat, lon):
            self.latitude = lat
            self.longitude = lon
              
    loc = Loc(request.args.get("latitude", None),
              request.args.get("longitude", None))

    state = uber_client.ping(loc)

    min_eta = min(v.min_eta for k, v in state.nearby_vehicles.items() if v.min_eta is not None)

    return jsonify(eta=min_eta)

if __name__ == "__main__":
    app.run(debug=True)
