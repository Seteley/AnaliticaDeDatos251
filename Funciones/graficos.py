import pandas as pd
import matplotlib.pyplot as plt

import os
import pandas as pd
from matplotlib import pyplot as plt

def graficar_serie(nombre_csv, usuario=None, hora_inicio=None, hora_fin=None, guardar=False):
    # Leer y preparar los datos
    df = pd.read_csv(nombre_csv)
    df['Hora'] = pd.to_datetime(df['Hora'])
    df = df.sort_values('Hora')

    # Si no se especifica hora_inicio o hora_fin, usar los extremos
    if hora_inicio is None:
        hora_inicio = df['Hora'].min()
    else:
        hora_inicio = pd.to_datetime(hora_inicio)
        
    if hora_fin is None:
        hora_fin = df['Hora'].max()
    else:
        hora_fin = pd.to_datetime(hora_fin)

    # Filtrar por el rango de tiempo
    mask_tiempo = (df['Hora'] >= hora_inicio) & (df['Hora'] <= hora_fin)
    df = df.loc[mask_tiempo]

    if df.empty:
        print("⚠️ No hay datos en el rango de tiempo especificado.")
        return

    # Determinar los usuarios
    if usuario:
        usuarios = [usuario]
    else:
        usuarios = df['Usuario'].unique()

    for user in usuarios:
        df_user = df[df['Usuario'] == user]

        if df_user.empty:
            print(f"⚠️ No se encontraron datos para el usuario: {user}")
            continue

        valores_iniciales = df_user.iloc[0][['Seguidores', 'Tweets', 'Following', 'Goal']]

        columnas = ['Seguidores', 'Tweets', 'Following', 'Goal']
        colores = ['blue', 'green', 'orange', 'purple']

        fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)
        fig.suptitle(f'Series de Tiempo relativas - {user}', fontsize=16)

        for i, col in enumerate(columnas):
            axs[i].plot(df_user['Hora'], df_user[col], color=colores[i], label=col)
            axs[i].axhline(valores_iniciales[col], color='red', linestyle='--', linewidth=1, label=f'Valor inicial: {valores_iniciales[col]}')
            axs[i].set_ylabel(col)
            axs[i].grid(True)
            axs[i].legend()

        axs[-1].set_xlabel('Hora')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        if guardar:
            # Crear carpeta si no existe
            carpeta_salida = './analiticadedatos251'
            os.makedirs(carpeta_salida, exist_ok=True)
            ruta_guardado = os.path.join(carpeta_salida, f'{user}_serie_completa.png')
            plt.savefig(ruta_guardado)
            plt.close(fig)
            print(f"✅ Gráfico guardado: {ruta_guardado}")
        else:
            plt.show()


import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

def graficar_serie_seguidores(hora_inicio, hora_fin, nombre_csv):
    # Leer y preparar los datos
    df = pd.read_csv(nombre_csv)
    df['Hora'] = pd.to_datetime(df['Hora'])
    df = df.sort_values('Hora')

    # Filtrar por el rango de tiempo
    mask = (df['Hora'] >= pd.to_datetime(hora_inicio)) & (df['Hora'] <= pd.to_datetime(hora_fin))
    df_filtrado = df.loc[mask]

    if df_filtrado.empty:
        print("⚠️ No hay datos en el rango de tiempo especificado.")
        return

    # Definir valor inicial de los seguidores
    seguidores_iniciales = df_filtrado.iloc[0]['Seguidores']

    # Preparar gráfico
    usuario = df_filtrado['Usuario'].iloc[0]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_filtrado['Hora'], df_filtrado['Seguidores'], color='blue', label='Seguidores')
    ax.axhline(seguidores_iniciales, color='red', linestyle='--', linewidth=1, label=f'Valor inicial: {seguidores_iniciales}')
    ax.set_ylabel('Seguidores')
    ax.set_xlabel('Hora')
    ax.set_title(f'Serie de Tiempo - Seguidores - {usuario}')
    ax.grid(True)
    ax.legend()

    # Asegurarse de que los valores del eje Y se muestran correctamente
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    plt.tight_layout()
    plt.show()


graficar_serie_seguidores("2025-04-24 12:41:07", "2025-04-25 22:38:11", "../Seguidores/seguidores_canalN__limpio.csv")