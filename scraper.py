from bs4 import BeautifulSoup

with open("data/reviews.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

reviews = soup.find_all("div", class_="review")

print("SCRAPED CUSTOMER SENTIMENT")
print("=" * 40)

for review in reviews:
    product = review.find("h2").text.strip()
    sentiment = review.find("p", class_="sentiment").text.strip()

    print("Product:", product)
    print("Review:", sentiment)
    print("-" * 40)