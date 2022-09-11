from flask import Flask, render_template
from scrape_data import data

app = Flask(__name__)


@app.route('/')
def get_gene_cards():
    return render_template("index.html"
                           , data=data
                           )


if __name__ == "__main__":
    app.run(debug=True)
