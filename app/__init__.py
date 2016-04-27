# Import Flask and template render library
from flask import Flask, render_template

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.msgrcv.controller import mod_msgrcv as msgrcv_module

app.register_blueprint(msgrcv_module)
