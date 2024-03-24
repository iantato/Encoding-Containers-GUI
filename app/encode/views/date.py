from flask import render_template, request

import app.config as config
from app.encode.base import encoding_bp

@encoding_bp.route("/date", methods=["GET", "POST"])
def date_route():
    
    if request.method == "POST" and hasattr(config, 'webdriver'):
        start = request.values.get('start')
        end = request.values.get('end')

        webdriver = config.webdriver
        webdriver.download_csv(webdriver.driver, start, end)
    
    return render_template("dates.html")