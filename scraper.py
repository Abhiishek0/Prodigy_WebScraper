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

# Currency conversion rate
GBP_TO_INR = 105.0  # You can change this to latest rate if needed

for book in books:
    title = book.h3.a['title']
    
    # Extract and convert price
    price_pound = book.find('p', class_='price_color').text.strip()  # e.g., £51.77
    price_float = float(price_pound.replace('£', ''))  # Remove £ and convert to float
    price_inr = round(price_float * GBP_TO_INR, 2)  # Convert to INR

    # Extract rating
    rating_class = book.find('p', class_='star-rating')['class'][1]  # e.g., 'Three'

    # Append to list
    data.append({
        'Title': title,
        'Price (GBP)': price_pound,
        'Price (INR)': f'₹{price_inr}',
        'Rating': rating_class
    })

# Step 4: Save to CSV
df = pd.DataFrame(data)
df.to_csv('products.csv', index=False)

print("✅ Data scraped and saved to products.csv with INR conversion")
