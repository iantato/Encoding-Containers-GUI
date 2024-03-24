from flask import render_template, request, redirect

import app.config as config
from app.encode.base import encoding_bp
from app.exceptions.login import IncorrectLogin
from app.utils.driver import Webdriver

@encoding_bp.route("/login/vbs.1-stop.biz", methods=["GET", "POST"])
def login_route():
    
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        url = 'https://ictsi.vbs.1-stop.biz'
        
        # Setup webdriver.
        # Base case for driver initialization.
        if not hasattr(config, 'webdriver'):
            webdriver = Webdriver()
            config.webdriver = webdriver
    
        try:
            webdriver.login(webdriver.driver, username, password, url)
            return redirect('/scraper/date')
        except IncorrectLogin:
            return render_template("login.html", visibility="visible")
        finally:
            pass
        
    
    return render_template("login.html", visibility="hidden")