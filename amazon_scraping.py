import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape Amazon
def scrape_amazon():
    search_query = "soft toys"
    base_url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}&ref=nb_sb_noss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Sending request to Amazon
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_data = []

    # Loop through each product
    for product in soup.find_all("div", class_="s-main-slot"):
        for item in product.find_all("div", class_="s-result-item"):
            try:
                # Title
                title_tag = item.find("span", class_="a-text-normal")
                title = title_tag.text if title_tag else "No Title"
                
                # Brand
                brand_tag = item.find("span", class_="a-size-base-plus a-color-base")
                brand = brand_tag.text if brand_tag else "Unknown Brand"
                
                # Reviews
                reviews_tag = item.find("span", class_="a-size-base")
                reviews = reviews_tag.text if reviews_tag else "0"
                
                # Rating
                rating_tag = item.find("span", class_="a-icon-alt")
                rating = rating_tag.text if rating_tag else "0"
                
                # Price
                price_tag = item.find("span", class_="a-price-whole")
                price = price_tag.text if price_tag else "0"
                
                # Image URL
                image_tag = item.find("img", class_="s-image")
                image_url = image_tag["src"] if image_tag else "No Image"
                
                # Product URL
                product_tag = item.find("a", class_="a-link-normal")
                product_url = "https://www.amazon.in" + product_tag["href"] if product_tag else "No Link"
                
                product_data.append([title, brand, reviews, rating, price, image_url, product_url])

            except Exception as e:
                print(f"Error processing item: {e}")
                continue

    # Save the data to CSV
    if product_data:
        with open("cleaned_data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Brand", "Reviews", "Rating", "Price", "Image URL", "Product URL"])
            writer.writerows(product_data)
        print(f"Data saved to cleaned_data.csv, {len(product_data)} products scraped.")
    else:
        print("No data to save.")

# Run the scraper
scrape_amazon()