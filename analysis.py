import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


# ==========================================
# 1. FETCH PRODUCT DATA FROM REST API
# ==========================================

api_url = "https://fakestoreapi.com/products"

response = requests.get(api_url)

if response.status_code != 200:
    print("ERROR: Could not fetch product data.")
    exit()

products = response.json()


# ==========================================
# 2. SCRAPE CUSTOMER REVIEWS
# ==========================================

with open("data/reviews.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

reviews = soup.find_all("div", class_="review")


# ==========================================
# 3. ANALYSE SENTIMENT
# ==========================================

sentiment_results = []

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

    sentiment_results.append({
        "product": product_name,
        "review": review_text,
        "sentiment": sentiment,
        "polarity": polarity
    })


# ==========================================
# 4. COMBINE PRODUCT DATA + SENTIMENT
# ==========================================

combined_results = []

for product in products:

    product_name = product["title"]

    matching_review = None

    for review in sentiment_results:
        if review["product"].lower() == product_name.lower():
            matching_review = review
            break

    if matching_review:

        combined_results.append({
            "product": product_name,
            "price": product["price"],
            "category": product["category"],
            "rating": product["rating"]["rate"],
            "review": matching_review["review"],
            "sentiment": matching_review["sentiment"],
            "polarity": matching_review["polarity"]
        })


# ==========================================
# 5. CALCULATE SUMMARY
# ==========================================

positive = sum(
    1 for item in combined_results
    if item["sentiment"] == "Positive"
)

negative = sum(
    1 for item in combined_results
    if item["sentiment"] == "Negative"
)

neutral = sum(
    1 for item in combined_results
    if item["sentiment"] == "Neutral"
)


# ==========================================
# 6. DISPLAY CLIENT REPORT
# ==========================================

print("\n")
print("=" * 60)
print("          PRODUCT SENTIMENT ANALYSIS REPORT")
print("=" * 60)

print("Total products fetched:", len(products))
print("Total reviews scraped:", len(reviews))
print("Products successfully combined:", len(combined_results))

print("\nSENTIMENT SUMMARY")
print("-" * 60)

print("Positive reviews:", positive)
print("Negative reviews:", negative)
print("Neutral reviews:", neutral)


print("\nPRODUCT DETAILS")
print("-" * 60)

for item in combined_results:

    print("\nProduct:", item["product"])
    print("Price: $", item["price"])
    print("Category:", item["category"])
    print("Rating:", item["rating"])
    print("Review:", item["review"])
    print("Sentiment:", item["sentiment"])
    print("Polarity:", round(item["polarity"], 2))
    print("-" * 60)


print("\nREPORT COMPLETE")
print("=" * 60)
# ==========================================
# 7. CREATE CLIENT REPORT FILE
# ==========================================

report_file = "reports/client_report.txt"

with open(report_file, "w", encoding="utf-8") as file:

    file.write("PRODUCT SENTIMENT ANALYSIS REPORT\n")
    file.write("=" * 60 + "\n\n")

    file.write(f"Total products fetched: {len(products)}\n")
    file.write(f"Total reviews scraped: {len(reviews)}\n")
    file.write(f"Products successfully combined: {len(combined_results)}\n\n")

    file.write("SENTIMENT SUMMARY\n")
    file.write("-" * 60 + "\n")
    file.write(f"Positive reviews: {positive}\n")
    file.write(f"Negative reviews: {negative}\n")
    file.write(f"Neutral reviews: {neutral}\n\n")

    file.write("PRODUCT DETAILS\n")
    file.write("-" * 60 + "\n")

    for item in combined_results:

        file.write(f"\nProduct: {item['product']}\n")
        file.write(f"Price: ${item['price']}\n")
        file.write(f"Category: {item['category']}\n")
        file.write(f"Rating: {item['rating']}\n")
        file.write(f"Review: {item['review']}\n")
        file.write(f"Sentiment: {item['sentiment']}\n")
        file.write(f"Polarity: {round(item['polarity'], 2)}\n")
        file.write("-" * 60 + "\n")

print("\nClient report created successfully!")
print("Location: reports/client_report.txt")