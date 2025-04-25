import os
import pandas as pd

# Ruta de la carpeta que contiene los CSV
carpeta_csv = './'  # puedes cambiar esto a la ruta que necesites

# Lista para almacenar los DataFrames
dataframes = []

# Recorre los archivos en la carpeta
for archivo in os.listdir(carpeta_csv):
    if archivo.endswith('.csv') and archivo != 'TOTAL.csv':
        ruta_archivo = os.path.join(carpeta_csv, archivo)
        df = pd.read_csv(ruta_archivo)
        dataframes.append(df)

# Une todos los DataFrames en uno solo
if dataframes:
    total_df = pd.concat(dataframes, ignore_index=True)
    total_df.to_csv(os.path.join(carpeta_csv, 'TOTAL.csv'), index=False)
    print("CSV unificado guardado como TOTAL.csv")
else:
    print("No se encontraron archivos CSV para unir.")
