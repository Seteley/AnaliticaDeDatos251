from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import pickle
import time
import os

def save_twitter_cookies(driver_path, output_file, wait_time=60):
    """
    Save Twitter cookies after manual login.
    
    Args:
        driver_path (str): Path to the Edge driver executable
        output_file (str): Path where to save the cookies
        wait_time (int): Time to wait for manual login in seconds
    """
    # Configura las opciones de EdgeDriver
    options = Options()
    options.add_argument("start-maximized")  # Maximiza la ventana del navegador

    # Configura el servicio para EdgeDriver
    service = Service(driver_path)

    # Inicia el WebDriver de Edge con las opciones y el servicio configurado
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Carga la página de inicio de sesión
        driver.get('https://x.com/search?q=congreso&src=typed_query&f=live')

        # Espera a que inicies sesión manualmente
        print(f"Please log in manually. Waiting {wait_time} seconds...")
        time.sleep(wait_time)

        # Asegúrate de que el directorio existe
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Guarda las cookies después de que hayas iniciado sesión
        pickle.dump(driver.get_cookies(), open(output_file, "wb"))
        print(f"Cookies saved successfully to {output_file}")

    finally:
        # Cierra el navegador
        driver.quit()

if __name__ == "__main__":
    # Example usage
    driver_path = 'D:\PYTHON\TWITTER\msedgedriver.exe'
    output_file = '../Archivos/cookies.pkl'
    save_twitter_cookies(driver_path, output_file)