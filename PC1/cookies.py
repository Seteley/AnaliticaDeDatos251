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

# Carga la página de inicio de sesión
driver.get('https://x.com/search?q=congreso&src=typed_query&f=live')

# Espera a que inicies sesión manualmente (este es un paso opcional, dependiendo del sitio)
time.sleep(60)  # Dale tiempo para iniciar sesión manualmente

# Guarda las cookies después de que hayas iniciado sesión
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# Cierra el navegador
driver.quit()
