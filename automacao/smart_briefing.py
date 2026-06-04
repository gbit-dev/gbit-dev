import requests
import json
import datetime
import os

# ==========================================
# ⚙️ CONFIGURAÇÕES
# ==========================================
# Localização para previsão do tempo (Ex: São Paulo, Brasil)
LATITUDE = -23.5489
LONGITUDE = -46.6388

# Número de notícias do HackerNews para buscar
TOP_STORIES_COUNT = 5

def fetch_weather() -> dict:
    """Busca a previsão do tempo usando a API pública do Open-Meteo."""
    print("🌤️ Buscando dados do clima...")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Pega a previsão do dia atual (índice 0)
        daily = data.get("daily", {})
        temp_max = daily.get("temperature_2m_max", [None])[0]
        temp_min = daily.get("temperature_2m_min", [None])[0]
        
        return {
            "max": temp_max,
            "min": temp_min,
            "status": "Sucesso"
        }
    except Exception as e:
        print(f"❌ Erro ao buscar clima: {e}")
        return {"status": "Erro"}

def fetch_tech_news() -> list:
    """Busca as top notícias de tecnologia via API do HackerNews."""
    print("📰 Buscando notícias de tecnologia...")
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    news_list = []
    
    try:
        # Busca IDs das top stories
        response = requests.get(top_stories_url)
        response.raise_for_status()
        story_ids = response.json()[:TOP_STORIES_COUNT]
        
        # Busca detalhes de cada notícia
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_res = requests.get(story_url)
            if story_res.status_code == 200:
                story_data = story_res.json()
                news_list.append({
                    "title": story_data.get("title", "Sem Título"),
                    "url": story_data.get("url", f"https://news.ycombinator.com/item?id={story_id}")
                })
        return news_list
    except Exception as e:
        print(f"❌ Erro ao buscar notícias: {e}")
        return []

def generate_markdown(weather: dict, news: list) -> str:
    """Gera o conteúdo do resumo em formato Markdown."""
    hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    
    md_content = f"# 🌅 Smart Briefing Matinal - {hoje}\n\n"
    
    # Seção de Clima
    md_content += "## 🌤️ Previsão do Tempo\n"
    if weather["status"] == "Sucesso":
        md_content += f"- **Máxima:** {weather['max']}°C\n"
        md_content += f"- **Mínima:** {weather['min']}°C\n\n"
    else:
        md_content += "- *Não foi possível carregar o clima hoje.*\n\n"
        
    # Seção de Notícias
    md_content += "## 💻 Top Tech News (HackerNews)\n"
    if news:
        for index, item in enumerate(news, start=1):
            md_content += f"{index}. [{item['title']}]({item['url']})\n"
    else:
        md_content += "- *Não foi possível carregar as notícias.*\n"
        
    md_content += "\n---\n*Gerado automaticamente pelo script Smart Briefing. 🤖*"
    return md_content

def main():
    print("🚀 Iniciando geração do Smart Briefing...")
    
    # 1. Coleta de Dados
    weather_data = fetch_weather()
    news_data = fetch_tech_news()
    
    # 2. Processamento e Geração
    report = generate_markdown(weather_data, news_data)
    
    # 3. Salvamento do Arquivo
    filename = f"briefing_{datetime.datetime.now().strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"✅ Briefing gerado com sucesso: {filename}")

if __name__ == "__main__":
    main()
