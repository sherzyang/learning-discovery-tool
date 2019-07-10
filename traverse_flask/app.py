import functions as f 
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return a new article."""
    data = request.json
    data = str(data)
    result = f.top_50_text(data)
    return result

# @app.route('/traverse', methods=['GET', 'POST'])
# def level_up():
#     """Return a new article."""
#     data = request.json
#     data = str(data)
#     result = f.get_level_change(x,data)
#     return jsonify(result)