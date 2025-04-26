from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

# Configuración de Selenium para usar EdgeDriver
def init_driver():
    # Configura EdgeDriver con la ruta especificada
    edge_service = Service(executable_path='C:\\Users\\marzabe\\OneDrive\\Documentos\\edgedriver_win64\\msedgedriver.exe')
    options = Options()
    driver = webdriver.Edge(service=edge_service, options=options)
    driver.maximize_window()
    return driver

# Obtener datos del perfil de un usuario
def get_user_profile(driver, username):
    url = f"https://x.com/{username}"  # Cambia la URL si es necesario
    driver.get(url)
    
    # Esperar a que cargue la página y un elemento clave esté presente
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='primaryColumn']"))
        )
    except Exception as e:
        print(f"Error: No se pudo cargar la página de {username}: {e}")
        return None
    
    # Parsear la página con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Crear un diccionario para almacenar la información del perfil
    profile_data = {}

    try:
        # Obtener el nombre (sin el handle)
        profile_data['name'] = soup.find('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}).get_text(strip=True) if soup.find('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}) else None
        
        # Obtener el nombre de usuario con el handle (@)
        profile_data['username'] = soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'})[1].get_text(strip=True) if soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}) else None
        
        # Obtener la biografía (si está disponible)
        profile_data['bio'] = soup.find('div', {'data-testid': 'UserDescription'}).get_text(strip=True) if soup.find('div', {'data-testid': 'UserDescription'}) else None
        
        # Obtener el número de seguidores
        followers = soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'})[2].get_text(strip=True) if len(soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'})) > 2 else None
        profile_data['followers_count'] = followers
        
        # Obtener el número de seguidos
        following = soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'})[0].get_text(strip=True) if len(soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'})) > 0 else None
        profile_data['following_count'] = following
        
        # Obtener el número de tweets
        tweet_count = soup.find('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}).get_text(strip=True) if soup.find('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}) else None
        profile_data['tweet_count'] = tweet_count
        
        # Obtener la ubicación (si está disponible)
        location = soup.find('span', {'class': 'css-901oao'})
        profile_data['location'] = location.get_text(strip=True) if location else None
        
        # Obtener la fecha de unión
        join_date = soup.find('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}).get_text(strip=True) if soup.find('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'}) else None
        profile_data['join_date'] = join_date
    except Exception as e:
        print(f"Error al obtener datos de {username}: {e}")
        return None
    
    return profile_data

# Guardar los datos en un archivo JSON
def save_data_to_json(data, filename='twitter_profiles.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Iniciar el driver de Selenium
    driver = init_driver()
    
    # Lista de usuarios que deseas obtener
    usernames = ['elonmusk', 'jack', 'billgates']  # Agrega más usuarios si lo deseas

    # Almacenar los datos de todos los perfiles
    all_profiles = []
    
    for username in usernames:
        print(f"Obteniendo datos de {username}...")
        profile = get_user_profile(driver, username)
        if profile:
            all_profiles.append(profile)
        time.sleep(3)  # Pausa para evitar ser bloqueado
    
    # Guardar los resultados en un archivo JSON
    save_data_to_json(all_profiles)
    
    # Cerrar el driver de Selenium
    driver.quit()

    print(f"Datos guardados en twitter_profiles.json")