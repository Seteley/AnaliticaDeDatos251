# seguidores.py

import csv
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapear_usuario(nombre_usuario):
    service = Service(r"D:\PYTHON\TWITTER\msedgedriver.exe")  # ✅ sin comillas extra y con cadena raw
    options = webdriver.EdgeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("window-size=1920,1080")

    driver = webdriver.Edge(service=service, options=options)
    url = f"https://livecounts.io/twitter-live-follower-counter/{nombre_usuario}"
    driver.get(url)
    driver.execute_script("window.scrollBy(0, 300);")

    archivo_csv = f"seguidores_{nombre_usuario}.csv"
    if not os.path.exists(archivo_csv):
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hora", "Usuario", "Seguidores", "Tweets", "Following", "Goal"])

    def extraer_numero_odometer(elem):
        return ''.join(e.text.strip() for e in elem.find_elements(By.CLASS_NAME, "odometer-value"))

    print(f"📡 Recolectando datos de @{nombre_usuario} cada 2 segundos...")

    try:
        while True:
            hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                usuario_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'text-center') and contains(., '@')]"))
                )
                usuario = usuario_elem.get_attribute("innerText").split()[0].strip()
            except:
                usuario = f"@{nombre_usuario}"

            seguidores = "0000"
            datos = {"Tweets": "0000", "Following": "0000", "Goal": "0000"}

            try:
                odometer_block = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.odometer.odometer-auto-theme"))
                )
                seguidores = extraer_numero_odometer(odometer_block)
            except:
                pass

            try:
                tarjetas = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.grid > div"))
                )
                for tarjeta in tarjetas:
                    try:
                        label = tarjeta.find_element(By.TAG_NAME, "p").text.strip()
                        if label in datos:
                            datos[label] = extraer_numero_odometer(tarjeta)
                    except:
                        continue
            except:
                pass

            with open(archivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    hora,
                    usuario,
                    seguidores,
                    datos["Tweets"],
                    datos["Following"],
                    datos["Goal"]
                ])

            print(f"[{hora}] {usuario} | Seguidores: {seguidores} | Tweets: {datos['Tweets']} | Following: {datos['Following']} | Goal: {datos['Goal']}")
            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n🛑 Finalizado para @{nombre_usuario}")
    finally:
        driver.quit()
