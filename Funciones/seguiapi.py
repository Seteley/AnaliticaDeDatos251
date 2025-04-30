from unofficial_livecounts_api.twitter import TwitterAgent
from datetime import datetime
import csv
import time
import os

def monitorear_seguidores(nombre_usuario):
    carpeta = "Seguidores"
    os.makedirs(carpeta, exist_ok=True)  # Crea la carpeta si no existe

    archivo_csv = os.path.join(carpeta, f"seguidores_{nombre_usuario}.csv")
    
    if not os.path.exists(archivo_csv):
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hora", "Usuario", "Seguidores", "Tweets", "Following"])

    try:
        while True:
            hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            metricas = TwitterAgent.fetch_user_metrics(query=nombre_usuario)

            seguidores = metricas.follower_count
            tweets = metricas.tweet_count
            following = metricas.following_count

            with open(archivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([hora, f"@{nombre_usuario}", seguidores, tweets, following])

            print(f"[{hora}] @{nombre_usuario} | Seguidores: {seguidores} | Tweets: {tweets} | Following: {following}")
            time.sleep(10)

    except KeyboardInterrupt:
        print(f"\n🛑 Monitoreo finalizado para @{nombre_usuario}")
