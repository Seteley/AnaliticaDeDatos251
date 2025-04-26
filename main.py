from multiprocessing import Process
from seguidores import scrapear_usuario

if __name__ == '__main__':
    usuarios = ['FCBarcelona', 'realmadrid', 'noticiAmerica', 'TuFPF', 'ESPNFC', 'IbaiLlanos', 'JBALVIN']
    procesos = []

    for usuario in usuarios:
        p = Process(target=scrapear_usuario, args=(usuario,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()
