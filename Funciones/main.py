from multiprocessing import Process
from seguidores import scrapear_usuario

if __name__ == '__main__':
    usuarios = ['canalN_', 'ClubSCristal', 'congresoperu', 'Cristiano', 'elonmusk', 'exitosape', 'KeikoFujimori', 'LaLiga', 'larepublica_co', 'Libertadores', 'Metropolitano_L', 'NBALatam', 'NetflixLAT', 'PolloFarsantePe', 'rlopezaliaga1', 'RPPNoticias', 'solopasaenperu', 'Spotify', 'Tesla', 'uniceflac', 'willaxtv']
    procesos = []

    for usuario in usuarios:
        p = Process(target=scrapear_usuario, args=(usuario,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()
