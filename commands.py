import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from tmdb_service import get_trending_movies, get_watch_providers
from ai_service import generate_movie_summary

# Função auxiliar para rodar as requisições síncronas de forma assíncrona/paralela
async def get_movie_data(movie):
    loop = asyncio.get_event_loop()
    
    # Executa as funções síncronas em threads separadas para não travar o bot
    onde = await loop.run_in_executor(None, get_watch_providers, movie['id'])
    
    try:
        resumo = await loop.run_in_executor(None, generate_movie_summary, movie)
    except:
        resumo = movie['overview'][:150] + "..."
        
    return movie, onde, resumo

async def top_movies(update: Update, context: ContextTypes.DEFAULT_TYPE, start_index=0):
    query = update.callback_query
    
    if query:
        await query.answer()
        await query.edit_message_text("🔄 Buscando informações e gerando resumos com IA...")

    movies = get_trending_movies()
    end_index = start_index + 3
    current_movies = movies[start_index:end_index]
    
    if not current_movies:
        return

    # Executa a busca de dados e resumos dos 3 filmes PARALELAMENTE
    tasks = [get_movie_data(m) for m in current_movies]
    results = await asyncio.gather(*tasks)

    text = f"🎬 **Filmes em Alta ({start_index + 1}º ao {end_index}º)**\n\n"
    
    for movie, onde_assistir, resumo in results:
        text += f"🍿 *{movie['title']}*\n"
        text += f"📝 {resumo}\n"
        text += f"📺 Onde ver: {onde_assistir}\n\n"
        text += "---" + "\n\n"

    # Teclado inteligente com botões de Voltar e Avançar
    keyboard_row = []
    
    if start_index > 0:
        keyboard_row.append(InlineKeyboardButton("⬅️ Voltar", callback_data=f"page_{start_index-3}"))
        
    if end_index < 20:
        keyboard_row.append(InlineKeyboardButton("Próximo ➡️", callback_data=f"page_{end_index}"))
        
    reply_markup = InlineKeyboardMarkup([keyboard_row])

    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    start_index = int(query.data.split("_")[1])
    await top_movies(update, context, start_index=start_index
)
