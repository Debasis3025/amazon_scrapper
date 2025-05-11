import pandas as pd

# Load the scraped data
try:
    df = pd.read_csv("cleaned_data.csv")
except FileNotFoundError:
    print("Error: 'cleaned_data.csv' not found. Please run the scraping script first.")
    exit()

# Print out the column names to verify
print("Columns in the dataframe:", df.columns)

# Clean the data
# Remove duplicates
df.drop_duplicates(subset=['Title', 'Brand'], keep='first', inplace=True)

# Ensure price, reviews, and ratings are in numerical format
# First, check the column names again
df.columns = df.columns.str.strip()  # Remove any leading or trailing spaces in column names

# Update the column name from 'Selling Price' to 'Price'
if 'Price' in df.columns:
    df['Price'] = df['Price'].replace({'₹': '', ',': ''}, regex=True).astype(float)
else:
    print("Column 'Price' not found. Available columns are:", df.columns)
    exit()

# Clean the 'Reviews' column by converting 'k' to 1000 and 'M' to 1000000
if 'Reviews' in df.columns:
    def convert_reviews(review_str):
        # Check if the review_str is a valid number or contains 'k' or 'M'
        if isinstance(review_str, str):
            # Filter out invalid entries
            if 'k' in review_str:
                try:
                    return float(review_str.replace('k', '')) * 1000
                except ValueError:
                    return None  # Return None if the conversion fails
            elif 'M' in review_str:
                try:
                    return float(review_str.replace('M', '')) * 1000000
                except ValueError:
                    return None
            else:
                try:
                    return float(review_str)  # Attempt to convert to float
                except ValueError:
                    return None  # Return None if conversion fails
        return None  # Return None if review_str is not a string
    
    # Apply the conversion function and drop rows with invalid reviews
    df['Reviews'] = df['Reviews'].apply(convert_reviews)
    df.dropna(subset=['Reviews'], inplace=True)  # Remove rows where 'Reviews' is NaN
    df['Reviews'] = df['Reviews'].astype(int)
else:
    print("Column 'Reviews' not found. Available columns are:", df.columns)
    exit()

# Ensure 'Rating' column exists and clean it
if 'Rating' in df.columns:
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
else:
    print("Column 'Rating' not found. Available columns are:", df.columns)
    exit()

# Handle missing or corrupted values
df.dropna(subset=['Title', 'Brand', 'Price', 'Reviews', 'Rating'], inplace=True)

# Save cleaned data to a new CSV file
df.to_csv("cleaned_data_processed.csv", index=False)

# Show first few rows to verify
print(df.head())