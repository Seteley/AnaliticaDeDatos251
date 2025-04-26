import os
import pandas as pd

# Ruta de la carpeta raíz (ANALITICADEDATOS251)
ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta de la carpeta donde están los CSV
carpeta_csv = os.path.join(ruta_base, 'Seguidores')

# Lista para almacenar los DataFrames
dataframes = []

# Recorre los archivos en la carpeta Seguidores
for archivo in os.listdir(carpeta_csv):
    if archivo.endswith('.csv'):
        ruta_archivo = os.path.join(carpeta_csv, archivo)
        df = pd.read_csv(ruta_archivo)
        dataframes.append(df)

# Une todos los DataFrames en uno solo
if dataframes:
    total_df = pd.concat(dataframes, ignore_index=True)
    # Guarda el CSV unido directamente en ANALITICADEDATOS251
    ruta_total = os.path.join(ruta_base, 'total.csv')
    total_df.to_csv(ruta_total, index=False)
    print(f"CSV unificado guardado como {ruta_total}")
else:
    print("No se encontraron archivos CSV para unir.")
