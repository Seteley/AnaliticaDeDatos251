from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import pickle
import time
import os

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
        for i in range(100):  # Número de miniscrolls
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)  # Espera que cargue nuevo contenido

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
