import requests
from config import TMDB_API_KEY
from services.cache import get_cache, set_cache # Importa o cache

BASE_URL = "https://api.themoviedb.org/3"

def get_trending_movies():
    cache_key = "trending_movies"
    cached = get_cache(cache_key)
    if cached:
        return cached

    url = f"{BASE_URL}/trending/movie/day"
    params = {"api_key": TMDB_API_KEY, "language": "pt-BR"}
    response = requests.get(url, params=params)
    data = response.json().get("results", [])

    set_cache(cache_key, data)
    return data

def get_watch_providers(movie_id):
    cache_key = f"watch_{movie_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    data = response.json().get("results", {})
    
    br_data = data.get("BR", {})
    flatrate = br_data.get("flatrate", [])
    
    if not flatrate:
        result = "Disponível apenas para aluguel/compra ou não listado."
    else:
        providers = [p['provider_name'] for p in flatrate]
        result = ", ".join(providers)
        
    set_cache(cache_key, result)
    return result
