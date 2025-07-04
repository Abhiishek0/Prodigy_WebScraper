import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Get the page
URL = 'https://books.toscrape.com/'
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'lxml')

# Step 2: Find all product containers
books = soup.find_all('article', class_='product_pod')

# Step 3: Extract data
data = []

for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    rating_class = book.find('p', class_='star-rating')['class'][1]  # like "Three", "Five"

    data.append({
        'Title': title,
        'Price': price,
        'Rating': rating_class
    })

# Step 4: Save to CSV
df = pd.DataFrame(data)
df.to_csv('products.csv', index=False)

print("✅ Data scraped and saved to products.csv")
