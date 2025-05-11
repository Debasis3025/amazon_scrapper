import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# ✅ Load CSV
df = pd.read_csv('/Users/debasispurohit/Downloads/vscode/python/youtube_video_finder/amazon_scrapper/cleaned_data_processed.csv')

# ✅ Strip extra spaces from column names
df.columns = df.columns.str.strip()

# ✅ Show actual columns (debug purpose)
print("Available Columns:", df.columns.tolist())

# ✅ Rename & convert data types safely
df['Rating'] = pd.to_numeric(df.get('Rating', pd.Series()), errors='coerce')
df['Reviews'] = pd.to_numeric(df.get('Reviews', pd.Series()), errors='coerce')
df['Selling Price'] = pd.to_numeric(df.get('Selling Price', df.get('SellingPrice', pd.Series())), errors='coerce')

# ✅ Clean text columns
df['Brand'] = df['Brand'].astype(str).str.strip()
df['Title'] = df['Title'].astype(str).str.strip()

# -----------------------------------
# 1. Brand Performance Analysis
# -----------------------------------
brand_freq = df['Brand'].value_counts().nlargest(5).reset_index()
brand_freq.columns = ['Brand', 'Frequency']

brand_rating = df.groupby('Brand')['Rating'].mean().reset_index().sort_values(by='Rating', ascending=False).head(5)

fig_brand_bar = px.bar(brand_freq, x='Brand', y='Frequency', title='Top 5 Brands by Frequency',
                       color='Frequency', text='Frequency')

fig_brand_pie = px.pie(brand_freq, names='Brand', values='Frequency', title='Top 5 Brands Share (%)')

# -----------------------------------
# 2. Price vs Rating Analysis
# -----------------------------------
fig_scatter = px.scatter(df, x='Selling Price', y='Rating', color='Brand', hover_data=['Title'],
                         title='Price vs Rating (Outlier Detection)', size='Reviews')

# Rating Ranges: 0-2, 2-4, 4-5
df['Rating_Range'] = pd.cut(df['Rating'], bins=[0, 2, 4, 5], labels=["1-2", "2-4", "4-5"])
price_by_rating = df.groupby('Rating_Range')['Selling Price'].mean().reset_index()

fig_bar_price_rating = px.bar(price_by_rating, x='Rating_Range', y='Selling Price',
                              title='Average Price by Rating Range', text='Selling Price')

# -----------------------------------
# 3. Review & Rating Distribution
# -----------------------------------
top_reviewed = df.nlargest(5, 'Reviews')[['Title', 'Reviews']]
fig_top_reviews = px.bar(top_reviewed, x='Title', y='Reviews', title='Top 5 Products by Reviews',
                         text='Reviews')

top_rated = df.sort_values(by='Rating', ascending=False).dropna(subset=['Rating']).drop_duplicates('Title').head(5)
fig_top_rated = px.bar(top_rated, x='Title', y='Rating', title='Top 5 Products by Rating',
                       text='Rating')

# -----------------------------------
# Dash App Layout
# -----------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Amazon Soft Toys Dashboard"

app.layout = dbc.Container([
    html.H1("🧸 Amazon Soft Toys Dashboard", className="text-center my-4"),

    dbc.Tabs([
        # Tab 1
        dbc.Tab(label="Brand Performance", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_brand_bar), md=6),
                dbc.Col(dcc.Graph(figure=fig_brand_pie), md=6)
            ])
        ]),

        # Tab 2
        dbc.Tab(label="Price vs Rating", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_scatter), md=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_bar_price_rating), md=6),
            ])
        ]),

        # Tab 3
        dbc.Tab(label="Review & Rating Distribution", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_top_rated), md=6),
                dbc.Col(dcc.Graph(figure=fig_top_reviews), md=6)
            ])
        ]),
    ])
], fluid=True)

# ✅ Run the server
if __name__ == "__main__":
    app.run(debug=True)