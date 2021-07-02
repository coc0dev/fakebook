from flask import Flask

app = Flask(__name__)

# building the rest of the flask application (configurations, additional packages, etc)
from  .import routes
