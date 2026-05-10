import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

import streamlit as st
import httpx

API_KEY = "93e0a61ac13c1a2a4136a9e22f3d6ac3"
IMG_LARGE = "https://image.tmdb.org/t/p/w500"

GENRES = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Fantasy": 14,
    "Horror": 27, "Mystery": 9648, "Romance": 10749, "Sci-Fi": 878,
    "Thriller": 53, "War": 10752, "Western": 37, "Family": 10751,
    "History": 36, "Music": 10402
}

LANGUAGES = {
    "English": "en", "Korean": "ko", "Tamil": "ta",
    "Malayalam": "ml", "Hindi": "hi", "Japanese": "ja",
    "French": "fr", "Spanish": "es", "Italian": "it",
    "Chinese": "zh", "Arabic": "ar", "Portuguese": "pt"
}

sort_map = {
    "Popularity": "popularity.desc",
    "Highest Rated": "vote_average.desc",
    "Newest First": "primary_release_date.desc",
    "Most Voted": "vote_count.desc"
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;700;900&display=swap');

    .stApp {
        background: #000000;
        color: white;
        font-family: 'Montserrat', sans-serif;
    }

    .hero-banner {
        background: linear-gradient(180deg,
            rgba(0,0,0,0.3) 0%,
            rgba(0,0,0,0.7) 60%,
            rgba(0,0,0,1) 100%),
        url('https://image.tmdb.org/t/p/original/628Dep6AxEtDxjZoGP78TsOxYbK.jpg');
        background-size: cover;
        background-position: center;
        padding: 80px 40px 40px 40px;
        margin: -80px -80px 30px -80px;
        text-align: center;
        border-bottom: 3px solid #e50914;
    }

    .main-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 80px !important;
        font-weight: 900;
        color: white !important;
        text-shadow: 0 0 30px #e50914, 0 0 60px #e50914;
        letter-spacing: 8px;
        margin: 0;
        line-height: 1;
    }

    .subtitle {
        font-size: 18px;
        color: #aaaaaa !important;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 10px;
    }

    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #e50914 !important;
        border-radius: 10px !important;
    }

    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #e50914 !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        padding: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #e50914, #b20710) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 16px 60px !important;
        width: 100% !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        box-shadow: 0 0 20px rgba(229, 9, 20, 0.6) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #ff1a1a, #e50914) !important;
        box-shadow: 0 0 40px rgba(229, 9, 20, 0.9) !important;
    }

    .section-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 36px;
        color: #e50914 !important;
        letter-spacing: 4px;
        border-left: 5px solid #e50914;
        padding-left: 15px;
        margin: 30px 0 20px 0;
    }

    .movie-title {
        font-weight: 900;
        font-size: 16px;
        color: white !important;
        margin: 8px 0 4px 0;
    }

    .movie-meta {
        color: #e50914 !important;
        font-size: 13px;
        font-weight: 700;
    }

    .movie-overview {
        color: #aaaaaa !important;
        font-size: 12px;
        line-height: 1.4;
    }

    .rating-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 13px;
        margin: 4px 0;
    }

    .rating-great { background: #21d07a; color: black; }
    .rating-good { background: #f5c518; color: black; }
    .rating-avg { background: #e87c23; color: white; }
    .rating-bad { background: #e50914; color: white; }

    .results-count {
        background: linear-gradient(135deg, #e50914, #b20710);
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 900;
        font-size: 16px;
        display: inline-block;
        margin: 10px 0;
        letter-spacing: 2px;
    }

    label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-banner'>
    <div class='main-title'>MOVIE FINDER</div>
    <div class='subtitle'>Discover Movies From Around The World</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>SEARCH MOVIES</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("GENRE", list(GENRES.keys()))
with col2:
    language = st.selectbox("LANGUAGE", list(LANGUAGES.keys()))

keyword = st.text_input("KEYWORD SEARCH", placeholder="e.g. space, love, zombie, dragon...")

col3, col4 = st.columns(2)
with col3:
    num_movies = st.slider("NUMBER OF MOVIES", 5, 100, 10)
with col4:
    min_rating = st.slider("MINIMUM RATING (out of 10)", 0.0, 10.0, 6.0, 0.5)

sort_by = st.selectbox("SORT BY", list(sort_map.keys()))

def get_rating_badge(rating):
    if rating >= 8:
        return f"<span class='rating-badge rating-great'>⭐ {rating}/10 EXCELLENT</span>"
    elif rating >= 7:
        return f"<span class='rating-badge rating-good'>⭐ {rating}/10 GOOD</span>"
    elif rating >= 5:
        return f"<span class='rating-badge rating-avg'>⭐ {rating}/10 AVERAGE</span>"
    else:
        return f"<span class='rating-badge rating-bad'>⭐ {rating}/10 LOW</span>"

def fetch_movies(genre, language, keyword, num_movies, min_rating, sort_by):
    transport = httpx.HTTPTransport(retries=3)
    with httpx.Client(verify=False, follow_redirects=True, transport=transport) as client:
        all_movies = []
        page = 1
        total_pages = 999
        max_pages = (num_movies // 20) + 10

        while len(all_movies) < num_movies and page <= min(max_pages, total_pages):
            if keyword:
                url = "https://api.themoviedb.org/3/search/movie"
                params = {
                    "api_key": API_KEY,
                    "query": keyword,
                    "language": LANGUAGES[language],
                    "page": page
                }
            else:
                url = "https://api.themoviedb.org/3/discover/movie"
                params = {
                    "api_key": API_KEY,
                    "with_genres": GENRES[genre],
                    "with_original_language": LANGUAGES[language],
                    "sort_by": sort_map[sort_by],
                    "vote_average.gte": min_rating,
                    "page": page
                }
            try:
                response = client.get(url, params=params, timeout=30)
                data = response.json()
                total_pages = data.get("total_pages", 1)
                results = data.get("results", [])
                if not results:
                    break
                # For keyword search, apply client-side rating filter
                if keyword:
                    results = [m for m in results if m.get("vote_average", 0) >= min_rating]
                all_movies.extend(results)
                page += 1
            except Exception:
                break

        return all_movies[:num_movies] if all_movies else []

if st.button("FIND MOVIES NOW"):
    with st.spinner("Loading movies..."):
        try:
            movies = fetch_movies(genre, language, keyword, num_movies, min_rating, sort_by)
            if movies:
                st.markdown(f"<div class='results-count'>🎉 {len(movies)} MOVIES FOUND!</div>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>RESULTS</div>", unsafe_allow_html=True)
                cols = st.columns(3)
                for i, movie in enumerate(movies):
                    with cols[i % 3]:
                        poster = movie.get("poster_path")
                        if poster:
                            st.image(IMG_LARGE + poster, use_container_width=True)
                        else:
                            st.markdown("🎬 No Poster Available")
                        title = movie.get("title", "Unknown")
                        year = movie.get("release_date", "N/A")[:4]
                        rating = round(movie.get("vote_average", 0), 1)
                        votes = movie.get("vote_count", 0)
                        overview = movie.get("overview", "No description available")
                        st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='movie-meta'>📅 {year} &nbsp;|&nbsp; 🗳️ {votes:,} votes</div>", unsafe_allow_html=True)
                        st.markdown(get_rating_badge(rating), unsafe_allow_html=True)
                        st.markdown(f"<div class='movie-overview'>{overview[:120]}...</div>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.warning("No movies found! Try lowering the minimum rating or changing filters.")
        except Exception as e:
            st.error(f"Connection failed: {e}")