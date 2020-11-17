"""Musa 509 week 12 demo app"""
import io
import json
import logging
import random

from flask import Flask, request, render_template, Response
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import geopandas as gpd
import numpy as np

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CSSResources, JSResources


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

bokeh_css = CSSResources(mode="cdn", version="2.2.3", minified=True)
bokeh_js = JSResources(mode="cdn", version="2.2.3", minified=True)

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


@app.route("/plot.png")
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), 200, mimetype="image/png")


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


def get_neighborhood_names():
    """Gets all neighborhoods for Philadelphia"""
    engine = get_sql_engine()
    query = text(
        """
        SELECT DISTINCT neighborhood_name
        FROM philadelphia_neighborhoods
        ORDER BY 1 ASC
    """
    )
    resp = engine.execute(query).fetchall()
    # get a list of names
    names = [row["neighborhood_name"] for row in resp]
    return names


# index page
@app.route("/")
def index():
    """Index page"""
    names = get_neighborhood_names()
    rand_name = random.choice(names)
    return render_template("input.html", nnames=names, rand_name=rand_name)


def get_bounds(geodataframe):
    """returns list of sw, ne bounding box pairs"""
    bounds = geodataframe.geom.total_bounds
    bounds = [[bounds[0], bounds[1]], [bounds[2], bounds[3]]]
    return bounds


def get_num_buildings(nname):
    """Get number of buildings in a neighborhood"""
    engine = get_sql_engine()
    building_stats = text(
        """
        SELECT
          count(v.*) as num_buildings
        FROM vacant_buildings as v
        JOIN philadelphia_neighborhoods as n
        ON ST_Intersects(v.geom, n.geom)
        WHERE n.neighborhood_name = :nname
    """
    )
    resp = engine.execute(building_stats, nname=nname).fetchone()
    return resp["num_buildings"]


def get_neighborhood_buildings(nname):
    """Get all buildings for a neighborhood"""
    engine = get_sql_engine()
    vacant_buildings = text(
        """
        SELECT
            "ADDRESS" as address,
            "BLDG_DESC" as building_description,
            "OPA_ID" as opa_id,
            v.geom as geom
        FROM vacant_buildings as v
        JOIN philadelphia_neighborhoods as n
        ON ST_Intersects(v.geom, n.geom)
        WHERE n.neighborhood_name = :nname
    """
    )
    buildings = gpd.read_postgis(vacant_buildings, con=engine, params={"nname": nname})
    return buildings


@app.route("/vacantviewer", methods=["GET"])
def vacant_viewer():
    """Test for form"""
    name = request.args["neighborhood"]
    buildings = get_neighborhood_buildings(name)
    bounds = get_bounds(buildings)

    # generate interactive map
    map_html = render_template(
        "geojson_map.html",
        geojson_str=buildings.to_json(),
        bounds=bounds,
        center_lng=(bounds[0][0] + bounds[1][0]) / 2,
        center_lat=(bounds[0][1] + bounds[1][1]) / 2,
        mapbox_token=MAPBOX_TOKEN,
    )
    return render_template(
        "vacant.html",
        num_buildings=get_num_buildings(name),
        nname=name,
        map_html=map_html,
        buildings=buildings[["address", "building_description", "opa_id"]].values,
        plot_html=make_building_chart(name),
    )


@app.route("/vacantviewer_download", methods=["GET"])
def vacant_download():
    """Download GeoJSON of data snapshot"""
    name = request.args["neighborhood"]
    buildings = get_neighborhood_buildings(name)
    return Response(buildings.to_json(), 200, mimetype="application/json")


# 404 page example
@app.errorhandler(404)
def page_not_found(err):
    """404 page"""
    return f"404 ({err})"


def make_building_chart(neighborhood_name):
    """Make a bar chart of number of buildings by description"""
    building_counts = get_building_desc_counts(neighborhood_name)

    plot = figure(
        x_range=building_counts["bldg_desc"],
        plot_height=250,
        title="Building Description Counts",
        toolbar_location=None,
        tools="",
        tooltips=[("Building Description", "@x"), ("Count", "@top")],
    )

    logging.warning(str(building_counts))
    plot.vbar(x=building_counts["bldg_desc"], top=building_counts["count"], width=0.9)

    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0

    script, div = components(plot)
    kwargs = {"script": script, "div": div, "js_files": bokeh_js.js_files}
    return render_template("html_plot.html", **kwargs)


def get_building_desc_counts(neighborhood_name):
    """Generates counts of buildings by type for each neighborhood"""
    engine = get_sql_engine()
    logging.warning("Neighborhood name: %s", neighborhood_name)
    query = text(
        """
        SELECT "BLDG_DESC" AS desc, count(*) as cnt
        FROM public.vacant_buildings as v
        JOIN public.philadelphia_neighborhoods as n
        ON ST_Intersects(v.geom, n.geom)
        WHERE neighborhood_name = :neighborhood_name
        GROUP BY 1
        ORDER BY 2 desc
        LIMIT 5
    """
    )

    resp = engine.execute(query, neighborhood_name=neighborhood_name)
    resp = [(row["desc"][:15], row["cnt"]) for row in resp]

    logging.warning("FIRST VIEW: %", str([row for row in resp]))
    result = {
        "bldg_desc": [row[0] for row in resp],
        "count": [row[1] for row in resp],
    }

    return result


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)
