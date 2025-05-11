import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("cleaned_data_processed.csv")
print("Columns in dataframe:", df.columns)

# --- Step 1: Basic cleaning & conversion ---
# Clean 'Price' column (₹ symbol, commas)
df['Price'] = df['Price'].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Clean 'Rating'
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Clean 'Reviews'
def convert_reviews(value):
    if isinstance(value, str):
        value = value.lower().replace(',', '').strip()
        if 'k' in value:
            return float(value.replace('k', '')) * 1000
        elif 'm' in value:
            return float(value.replace('m', '')) * 1000000
        elif value.isdigit():
            return int(value)
    try:
        return int(value)
    except:
        return None

df['Reviews'] = df['Reviews'].apply(convert_reviews)

# Drop rows where price is NaN
df = df.dropna(subset=['Price'])

# --- Step 2: Visualization Setup ---
sns.set(style='whitegrid')

# --- Top 10 Brands by Product Count ---
plt.figure(figsize=(10, 5))
top_brands = df['Brand'].value_counts().head(10)
sns.barplot(x=top_brands.index, y=top_brands.values, palette='viridis')
plt.xticks(rotation=45)
plt.title("Top 10 Brands by Product Count")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig("top_10_brands.png")
plt.show()

# --- Price Distribution ---
plt.figure(figsize=(8, 5))
sns.histplot(df['Price'], bins=30, kde=True, color='skyblue')
plt.title("Price Distribution")
plt.xlabel("Price (INR)")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig("price_distribution.png")
plt.show()

# --- Rating vs Price Scatter Plot ---
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Price', y='Rating', hue='Brand', legend=False)
plt.title("Price vs Rating")
plt.xlabel("Price")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig("price_vs_rating.png")
plt.show()

# --- Products with Highest Reviews ---
top_reviewed = df.sort_values(by='Reviews', ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_reviewed['Title'], y=top_reviewed['Reviews'], palette='magma')
plt.xticks(rotation=75)
plt.title("Top 10 Most Reviewed Products")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig("top_reviewed_products.png")
plt.show()