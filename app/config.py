
##################################
# BASE DIRECTORY CONSTANT
##################################
from pathlib import Path
BASE_DIR = str(Path().resolve())

##################################
# DOWNLOAD DIR
##################################
DOWNLOAD_DIR = BASE_DIR + "\\data"

##################################
# WEBDRIVER
##################################
from app.utils.driver import Webdriver  # noqa: E402
webdriver: Webdriver