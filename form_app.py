"""Musa 509 week 12 demo app"""
import json
import logging
import random

from flask import Flask, request, render_template, Response

app = Flask(__name__, template_folder="templates")


# index page
@app.route("/")
def index():
    """Index page"""
    return render_template("arg_index.html")


@app.route("/argviewer")
def argviewer():
    args = dict(request.args)
    if request.args.get("really-important-check-box") is not None:
        color = "#990000"
    else:
        color = "#000000"

    return Response(
        render_template("arg_viewer.html", args=args, color=color),
        200,
        mimetype="text/html",
    )


# 404 page example
@app.errorhandler(404)
def page_not_found(err):
    """404 page"""
    return f"404 ({err})"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port=5001, debug=True)
