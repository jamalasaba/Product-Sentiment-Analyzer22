from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

app = Flask(__name__)


@app.route("/")
def home():

    # Fetch products from API
    response = requests.get("https://fakestoreapi.com/products")
    products = response.json()

    # Read simulated review website
    with open("data/reviews.html", "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    reviews = soup.find_all("div", class_="review")

    results = []

    for review in reviews:

        product_name = review.find("h2").text.strip()
        review_text = review.find("p", class_="sentiment").text.strip()

        polarity = TextBlob(review_text).sentiment.polarity

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Match review with API product
        for product in products:

            if product["title"].lower() == product_name.lower():

                results.append({
                    "product": product["title"],
                    "price": product["price"],
                    "category": product["category"],
                    "rating": product["rating"]["rate"],
                    "review": review_text,
                    "sentiment": sentiment,
                    "polarity": round(polarity, 2)
                })

                break

    positive = sum(1 for r in results if r["sentiment"] == "Positive")
    negative = sum(1 for r in results if r["sentiment"] == "Negative")
    neutral = sum(1 for r in results if r["sentiment"] == "Neutral")

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Sentiment Analyzer</title>

        <style>
            body {
                font-family: Arial;
                background: #f2f2f2;
                padding: 30px;
            }

            .container {
                max-width: 1000px;
                margin: auto;
            }

            h1 {
                text-align: center;
            }

            .summary {
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }

            .box {
                background: white;
                padding: 20px;
                flex: 1;
                text-align: center;
                border-radius: 10px;
            }

            .product {
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
            }

            .positive {
                color: green;
                font-weight: bold;
            }

            .negative {
                color: red;
                font-weight: bold;
            }

            .neutral {
                color: orange;
                font-weight: bold;
            }
        </style>
    </head>

    <body>

    <div class="container">

        <h1>Product Sentiment Analysis</h1>

        <div class="summary">

            <div class="box">
                <h2>{{ total }}</h2>
                <p>Products Analysed</p>
            </div>

            <div class="box">
                <h2>{{ positive }}</h2>
                <p>Positive</p>
            </div>

            <div class="box">
                <h2>{{ negative }}</h2>
                <p>Negative</p>
            </div>

            <div class="box">
                <h2>{{ neutral }}</h2>
                <p>Neutral</p>
            </div>

        </div>

        {% for item in results %}

        <div class="product">

            <h2>{{ item.product }}</h2>

            <p><b>Price:</b> ${{ item.price }}</p>

            <p><b>Category:</b> {{ item.category }}</p>

            <p><b>Rating:</b> {{ item.rating }}</p>

            <p><b>Customer Review:</b> {{ item.review }}</p>

            <p>
                <b>Sentiment:</b>

                <span class="{{ item.sentiment.lower() }}">
                    {{ item.sentiment }}
                </span>
            </p>

            <p><b>Polarity:</b> {{ item.polarity }}</p>

        </div>

        {% endfor %}

    </div>

    </body>
    </html>
    """,
    results=results,
    total=len(results),
    positive=positive,
    negative=negative,
    neutral=neutral
    )


if __name__ == "__main__":
    app.run(debug=False)