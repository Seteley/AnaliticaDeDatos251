from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import pickle
import time

# Configura las opciones de EdgeDriver
options = Options()
options.add_argument("start-maximized")  # Maximiza la ventana del navegador

# Configura el servicio para EdgeDriver
service = Service('D:\PYTHON\TWITTER\msedgedriver.exe')

# Inicia el WebDriver de Edge con las opciones y el servicio configurado
driver = webdriver.Edge(service=service, options=options)

# Carga la página de inicio
driver.get('https://x.com/search?q=congreso&src=recent_search_click&f=live')

# Carga las cookies previamente guardadas
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# Vuelve a cargar la página para aplicar las cookies
driver.get('https://x.com/search?q=congreso&src=recent_search_click&f=live')

# Ahora deberías estar autenticado sin tener que iniciar sesión manualmente

# Realiza el scroll y guarda el contenido como antes
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Obtén el contenido del <body> y guárdalo en un archivo
body_content = driver.find_element("tag name", "body").get_attribute('outerHTML')

# Guarda el contenido en un archivo de texto
with open("pagina_contenido.txt", "w", encoding="utf-8") as file:
    file.write(body_content)

# Cierra el navegador
driver.quit()
