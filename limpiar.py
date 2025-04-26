"""import pandas as pd

def limpiar_csv(nombre_csv):
    df = pd.read_csv(nombre_csv)
    df.reset_index(drop=True, inplace=True)

    # Regla 1: Eliminar filas donde los 4 campos son 0 simultáneamente
    df = df[~((df['Seguidores'] == 0) & 
              (df['Tweets'] == 0) & 
              (df['Following'] == 0) & 
              (df['Goal'] == 0))].copy()
    df.reset_index(drop=True, inplace=True)

    i = 0
    while i < len(df) - 1:
        fila_actual = df.loc[i]
        fila_siguiente = df.loc[i + 1]
        eliminar_siguiente = False
        eliminar_actual = False

        # Regla 2: si la fila siguiente tiene un salto mayor que la fila actual en cualquiera de los campos
        for campo in ['Seguidores', 'Tweets', 'Following', 'Goal']:
            if abs(fila_siguiente[campo] - fila_actual[campo]) > fila_actual[campo]:
                eliminar_siguiente = True
                break

        # Regla 3: si cualquier campo de la fila actual es 0 y en la siguiente es mayor a 10000
        for campo in ['Seguidores', 'Tweets', 'Following', 'Goal']:
            if fila_actual[campo] == 0 and fila_siguiente[campo] > 10000:
                eliminar_actual = True
                break

        if eliminar_actual:
            df.drop(index=i, inplace=True)
            df.reset_index(drop=True, inplace=True)
            # Después de eliminar la fila actual, no avanzamos i, sino que seguimos comparando con la nueva fila siguiente
        elif eliminar_siguiente:
            df.drop(index=i + 1, inplace=True)
            df.reset_index(drop=True, inplace=True)
            # Si se elimina la fila siguiente, solo avanzamos una posición para seguir comparando con la siguiente fila
            # No incrementamos i, ya que la fila actual ahora se debe comparar con la nueva fila siguiente
        else:
            # Si no se elimina ninguna fila, simplemente avanzamos al siguiente índice
            i += 1

    nuevo_nombre = nombre_csv.replace('.csv', '_limpio.csv')
    df.to_csv(nuevo_nombre, index=False)
    print(f"✅ Guardado como: {nuevo_nombre}")

limpiar_csv("seguidores_elonmusk.csv")
"""


import pandas as pd

def limpiar_csv(nombre_csv):
    df = pd.read_csv(nombre_csv)
    df.reset_index(drop=True, inplace=True)

    # Regla 1: Eliminar filas donde los 4 campos son 0 simultáneamente
    df = df[~((df['Seguidores'] == 0) & 
              (df['Tweets'] == 0) & 
              (df['Following'] == 0) & 
              (df['Goal'] == 0))].copy()
    df.reset_index(drop=True, inplace=True)

    i = 0
    while i < len(df) - 1:
        fila_actual = df.loc[i]
        fila_siguiente = df.loc[i + 1]
        eliminar_siguiente = False
        eliminar_actual = False

        # Regla 2: si la fila siguiente tiene un salto mayor que la fila actual en cualquier campo
        for campo in ['Seguidores', 'Tweets', 'Following', 'Goal']:
            if abs(fila_siguiente[campo] - fila_actual[campo]) > fila_actual[campo]:
                eliminar_siguiente = True
                break

        # Regla 3: eliminar bloque de 0s si luego hay un valor > 10000
        indices_para_eliminar = []
        for campo in ['Seguidores', 'Tweets', 'Following', 'Goal']:
            if fila_actual[campo] == 0:
                j = i
                while j < len(df) and df.loc[j][campo] == 0:
                    indices_para_eliminar.append(j)
                    j += 1
                if j < len(df) and df.loc[j][campo] > 10000:
                    eliminar_actual = True
                    break  # Basta con que un campo cumpla para eliminar ese bloque

        if eliminar_actual:
            df.drop(index=indices_para_eliminar, inplace=True)
            df.reset_index(drop=True, inplace=True)
            # No incrementamos i, porque debemos revisar la nueva fila que quedó en la posición i
        elif eliminar_siguiente:
            df.drop(index=i + 1, inplace=True)
            df.reset_index(drop=True, inplace=True)
        else:
            i += 1

    nuevo_nombre = nombre_csv.replace('.csv', '_limpio.csv')
    df.to_csv(nuevo_nombre, index=False)
    print(f"✅ Guardado como: {nuevo_nombre}")

limpiar_csv("seguidores_Cristiano.csv")
