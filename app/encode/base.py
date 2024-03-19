from flask import Blueprint

encoding_bp = Blueprint(
    name="encode",
    import_name=__name__,
    url_prefix="/scraper"
)