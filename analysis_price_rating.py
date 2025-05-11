import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function for Price vs Rating Analysis
def analyze_price_rating(data_file="cleaned_data.csv"):
    df = pd.read_csv(data_file)

    # Remove rows with missing price or rating
    df = df.dropna(subset=["Price", "Rating"])

    # Scatter Plot: Price vs Rating
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="Price", y="Rating", data=df, color='blue', alpha=0.6)
    plt.title("Price vs Rating")
    plt.xlabel("Price (₹)")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig("price_vs_rating_scatter.png")
    plt.close()

    # Bar chart: Average Price by Rating Range
    df['Rating Range'] = pd.cut(df['Rating'], bins=[0, 2, 4, 5], labels=["0-2", "2-4", "4-5"])
    avg_price_by_rating = df.groupby('Rating Range')['Price'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Rating Range", y="Price", data=avg_price_by_rating, palette="viridis")
    plt.title("Average Price by Rating Range")
    plt.xlabel("Rating Range")
    plt.ylabel("Average Price (₹)")
    plt.tight_layout()
    plt.savefig("avg_price_by_rating.png")
    plt.close()

    print("Price vs Rating Analysis complete!")

if __name__ == "__main__":
    analyze_price_rating()