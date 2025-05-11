import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function for Review & Rating Distribution Analysis
def analyze_reviews_rating(data_file="cleaned_data.csv"):
    df = pd.read_csv(data_file)

    # Remove rows with missing values in Rating or Reviews
    df = df.dropna(subset=["Rating", "Reviews"])

    # 1. Top 5 Products by Reviews
    top_reviews = df.sort_values(by="Reviews", ascending=False).head(5)

    # 2. Top 5 Products by Rating
    top_ratings = df.sort_values(by="Rating", ascending=False).head(5)

    # --- Visualization ---

    # Bar Chart: Top Rated Products
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Rating", y="Title", data=top_ratings, palette="viridis")
    plt.title("Top 5 Products by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig("top_rated_products_bar.png")
    plt.close()

    # Bar Chart: Most Reviewed Products
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Reviews", y="Title", data=top_reviews, palette="coolwarm")
    plt.title("Top 5 Products by Reviews")
    plt.xlabel("Reviews")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig("most_reviewed_products_bar.png")
    plt.close()

    # Print insights
    print("✅ Top 5 Products by Rating:\n", top_ratings[["Title", "Rating"]])
    print("\n✅ Top 5 Products by Reviews:\n", top_reviews[["Title", "Reviews"]])

if __name__ == "__main__":
    analyze_reviews_rating()