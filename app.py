from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from prediction_service import prediction

wepapp_root = "webapp"
static_dir = os.path.join(wepapp_root, "static")
template_dir = os.path.join(wepapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:  # from webfrom
                data = dict(request.form)
                response = prediction.form_response(data)
                return render_template("index.html", response = response)
            elif request.json:  # from api
                response = prediction.api_response(request.json)
                return jsonify(response)
        except Exception as ex:
            print(ex)
            error = {"error": "Something went wrong!!", "exception": ex}
            return render_template("404.html", error)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    print("ApplicationStarted")
    app.run(host='0.0.0.0', port=5000, debug=True)
