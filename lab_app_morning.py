"""Musa 509 week 12 demo app"""
import io
import json
import logging

from flask import Flask, request, render_template, Response
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import requests

# load credentials from a file
with open("pg-credentials.json", "r") as f_in:
    pg_creds = json.load(f_in)

# mapbox
with open("mapbox_token.json", "r") as mb_token:
    MAPBOX_TOKEN = json.load(mb_token)["token"]

app = Flask(__name__, template_folder="templates")

# load credentials from JSON file
HOST = pg_creds["HOST"]
USERNAME = pg_creds["USERNAME"]
PASSWORD = pg_creds["PASSWORD"]
DATABASE = pg_creds["DATABASE"]
PORT = pg_creds["PORT"]


def get_sql_engine():
    """Generates a SQLAlchemy engine"""
    return create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")


@app.route("/")
def index():
    """"""
    return Response(render_template("lab_input.html"), 200, mimetype="text/html")


@app.route("/whereami")
def whereami():
    """Landing page"""
    address_text = request.args.get("address-text", "")
    address_dropdown = request.args.get("address-dropdown", "")

    if address_text != "":
        address = address_text
    elif address_dropdown != "":
        address = address_dropdown
    else:
        address = "Meyerson Hall, University of Pennsylvania"

    # Makes API call to Mapbox Geocoding API
    geocoding_call = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    resp = requests.get(geocoding_call, params={"access_token": MAPBOX_TOKEN})

    # return results
    lng, lat = resp.json()['features'][0]['geometry']['coordinates']

    return render_template(
        'whereami.html',
        lng=lng,
        lat=lat,
        address=address,
        html_map=render_template('point_map.html', lng=lng, lat=lat, mapbox_token=MAPBOX_TOKEN)
    )

# 404 page example
@app.errorhandler(404)
def page_not_found(err):
    """404 page"""
    return f"404 ({err})"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host="0.0.0.0", port=5002)
