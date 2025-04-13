from bs4 import BeautifulSoup
import csv

# Cargar el contenido del archivo HTML
with open("pagina_contenido.txt", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Inicializar lista de resultados
tweets_data = []

# Buscar todos los divs que podrían contener tweets
possible_tweets = soup.find_all("article")

# Procesar cada uno
for tweet in possible_tweets:
    try:
        usuario = tweet.find('div', attrs={'dir': 'ltr'}).text.strip()
        fecha_tag = tweet.find('time')
        fecha = fecha_tag['datetime'] if fecha_tag else ''
        
        # Buscar contenido del tweet
        contenido_div = tweet.find('div', attrs={'data-testid': 'tweetText'})
        contenido = contenido_div.text.strip() if contenido_div else ''
        
        # Reemplazar saltos de línea por espacios
        contenido = ' '.join(contenido.splitlines())

        # Buscar estadísticas: respuestas, retuits, me gusta, guardados
        estadisticas = tweet.find_all('div', attrs={'data-testid': 'app-text-transition-container'})
        comentarios = estadisticas[0].text if len(estadisticas) > 0 else '0'
        retuits = estadisticas[1].text if len(estadisticas) > 1 else '0'
        likes = estadisticas[2].text if len(estadisticas) > 2 else '0'
        guardados = estadisticas[3].text if len(estadisticas) > 3 else '0'

        tweets_data.append([usuario, fecha, contenido, comentarios, retuits, likes, guardados])
    except Exception as e:
        continue  # Ignorar errores en tweets individuales

# Escribir a CSV
csv_path = "tweets_extraidos.csv"
with open(csv_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["usuario", "fecha", "tweet", "numero_comentarios", "numero_retweets", "numero_likes", "numero_guardados"])
    writer.writerows(tweets_data)

print(f"Archivo CSV generado: {csv_path}")
