import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_csv("coolmovies_cleaned.csv")
    df['genres'] = df['genres'].apply(eval)  # Convert string list to real list
    return df

df = load_data()

# ---- Prepare exploded DataFrame for filtering and plots ----
df_exploded = df.explode('genres')

# ---- App Title ----
st.title("🎬 The Coolest Movies Explorer!")

# ---- Genre Filter ----
st.subheader("🎭 Browse by Genre")
unique_genres = sorted(df_exploded['genres'].dropna().unique())
selected_genre = st.selectbox("Choose a genre to view its movies:", unique_genres)

# Filter by selected genre
genre_filtered_df = df_exploded[df_exploded['genres'] == selected_genre]
st.write(f"🎞️ Found {genre_filtered_df.shape[0]} movies in **{selected_genre}**")
st.dataframe(genre_filtered_df[['title', 'year', 'genres']])

# ---- Year Filter ----
st.subheader("📅 Filter by Year Range")
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider("Select a year range", min_year, max_year, (2000, 2010))
year_filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
st.write(f"🎬 {year_filtered_df.shape[0]} movies between {year_range[0]} and {year_range[1]}")
st.dataframe(year_filtered_df[['title', 'year', 'genres']])

# ---- Visualization 1: Genre Growth in Last 10 Years ----
st.subheader("📈 Genre Growth in the Last 10 Years")

# Calculate growth
recent = df_exploded[df_exploded['year'] >= max_year - 10]
past = df_exploded[(df_exploded['year'] >= max_year - 20) & (df_exploded['year'] < max_year - 10)]
recent_counts = recent['genres'].value_counts()
past_counts = past['genres'].value_counts()
growth_df = pd.DataFrame({'past': past_counts, 'recent': recent_counts}).fillna(0)
growth_df['change'] = growth_df['recent'] - growth_df['past']
growth_df = growth_df.sort_values(by='change', ascending=False)

# Plot
fig1, ax1 = plt.subplots(figsize=(12,5))
sns.barplot(x=growth_df.index, y=growth_df['change'], palette='coolwarm', ax=ax1)
ax1.axhline(0, color='gray', linestyle='--')
ax1.set_title("Genre Growth in the Last 10 Years")
ax1.set_ylabel("Change in Number of Movies")
ax1.set_xlabel("Genre")
plt.xticks(rotation=90)
st.pyplot(fig1)

# ---- Visualization 2: Top Genre per Year ----
st.subheader("📊 Most Produced Genre Each Year")

# Group and get top genre per year
genre_year = df_exploded.groupby(['year', 'genres']).size().reset_index(name='count')
top_genre_year = genre_year.loc[genre_year.groupby('year')['count'].idxmax()]

# Plot
fig2, ax2 = plt.subplots(figsize=(12,5))
sns.lineplot(data=top_genre_year, x='year', y='count', hue='genres', marker='o', ax=ax2)
ax2.set_title("Top Genre per Year (Most Produced)")
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Movies")
ax2.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig2)

# ---- Visualization 3: Dominant Genres in Most Productive Year ----
st.subheader("🏆 Genres in the Most Productive Year")

most_year = df_exploded['year'].value_counts().idxmax()
top_genres_year = df_exploded[df_exploded['year'] == most_year]['genres'].value_counts()

# Plot
fig3, ax3 = plt.subplots(figsize=(12,5))
sns.barplot(x=top_genres_year.index, y=top_genres_year.values, ax=ax3)
ax3.set_title(f"Genres in the Most Productive Year: {most_year}")
ax3.set_xlabel("Genre")
ax3.set_ylabel("Number of Movies")
plt.xticks(rotation=90)
st.pyplot(fig3)