from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import pickle
import time
import os
import random  # <- Importamos random para pausas aleatorias

def scroll_suave(driver, pasos=5, pausa=0.1):
    """
    Desplaza hacia abajo la página en pequeños pasos.
    
    :param driver: Instancia del WebDriver
    :param pasos: Número de mini-scrolls para llegar al fondo
    :param pausa: Tiempo de espera entre cada paso (en segundos)
    """
    altura_total = driver.execute_script("return document.body.scrollHeight")
    altura_actual = driver.execute_script("return window.scrollY")
    incremento = (altura_total - altura_actual) / pasos

    for i in range(pasos):
        driver.execute_script(f"window.scrollBy(0, {incremento});")
        time.sleep(pausa)


def scrape_twitter(search_url, output_file):
    # Configura las opciones de EdgeDriver
    options = Options()
    options.add_argument("start-maximized")  # Maximiza la ventana del navegador

    # Configura el servicio para EdgeDriver
    service = Service('D:\\PYTHON\\TWITTER\\msedgedriver.exe')

    # Inicia el WebDriver de Edge con las opciones y el servicio configurado
    driver = webdriver.Edge(service=service, options=options)

    # Carga la página de inicio
    driver.get('https://x.com')

    # Carga las cookies previamente guardadas
    cookies = pickle.load(open("../Archivos/cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Vuelve a cargar la página con la búsqueda específica
    driver.get(search_url)

    # Asegúrate de que el directorio existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Abre el archivo en modo append para agregar contenido progresivamente
    with open(output_file, "a", encoding="utf-8") as file:
        for i in range(500):  # Número de miniscrolls
            scroll_suave(driver, pasos=20, pausa=0.2)  # Puedes ajustar los valores

            # Pausa aleatoria entre 2.5 y 5 segundos
            wait_time = random.uniform(0.5, 2)
            print(f"Scroll #{i + 1}: esperando {wait_time:.2f} segundos...")
            time.sleep(wait_time)

            # Captura el contenido del body
            body_content = driver.find_element("tag name", "body").get_attribute('outerHTML')

            # Escribe el contenido del body con separación
            file.write(f"\n\n--- Scroll #{i + 1} ---\n\n")
            file.write(body_content)

    # Cierra el navegador
    driver.quit()

if __name__ == "__main__":
    scrape_twitter(
        'https://x.com/search?q=Sanna&src=trend_click&vertical=trends',
        '../Archivos/pagina_contenido.txt'
    )
