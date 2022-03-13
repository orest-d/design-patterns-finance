from liquer import *
import liquer.ext.lq_pandas
import liquer.ext.basic
import liquer.ext.meta
import liquer_gui
import liquer_pcv
import pipeline
from liquer.store import *
from liquer.recipes import *

from flask import Flask
import liquer.server.blueprint as bp

app = Flask(__name__)
app.register_blueprint(bp.app, url_prefix="/liquer")


@app.route("/")
@app.route("/index.html")
def index():
    return """<h1>My simulation control site</h1>
    <ul>
    <li><a href="/liquer/q/default_portfolio/simulation/report/baseline_performance.txt">Baseline performance</a></li>
    <li><a href="/liquer/web/gui">GUI</a></li>
    </ul>
    """


mount_folder("local", ".")
mount("results", RecipeSpecStore(FileStore("results")))

app.run()
