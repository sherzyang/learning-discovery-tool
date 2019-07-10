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
    query = data['user_input']
    top_50_df = f.top_k_text(query, k=50)
    articles = top_50_df.to_dict(orient='records')
    return render_template('article_table.html', articles=articles)
