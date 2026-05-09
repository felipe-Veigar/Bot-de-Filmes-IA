import google.generativeai as genai
from config import GEMINI_API_KEY
from services.cache import get_cache, set_cache # Importa o cache

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_movie_summary(movie):
    cache_key = f"summary_{movie['id']}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    prompt = f"""
    Faça um resumo detalhado e atrativo sobre o filme abaixo:

    Título: {movie['title']}
    Sinopse: {movie['overview']}

    Explique:
    - gênero implícito
    - clima do filme
    - para quem é recomendado
    - se parece blockbuster, cult, suspense etc
    """
    response = model.generate_content(prompt)
    result = response.text

    set_cache(cache_key, result)
    return result
