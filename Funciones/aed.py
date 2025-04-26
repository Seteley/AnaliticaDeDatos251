import pandas as pd

# Cargar el archivo limpio
df = pd.read_csv("../Seguidores/seguidores_canalN__limpio.csv", parse_dates=["Hora"])

# -----------------------------
# Dimensiones y tipos de datos
# -----------------------------
print("🔹 Dimensiones del DataFrame:", df.shape)
print("\n🔹 Tipos de datos:")
print(df.dtypes)

# -----------------------------
# Primeras y últimas filas
# -----------------------------
print("\n🔹 Primeras filas:")
print(df.head())
print("\n🔹 Últimas filas:")
print(df.tail())

# -----------------------------
# Valores nulos
# -----------------------------
print("\n🔹 Valores nulos por columna:")
print(df.isnull().sum())

# -----------------------------
# Estadísticas descriptivas
# -----------------------------
print("\n🔹 Estadísticas descriptivas:")
print(df.describe())

# -----------------------------
# Valores únicos por campo
# -----------------------------
print("\n🔹 Valores únicos por campo:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()} únicos")

# -----------------------------
# Moda, rango y outliers
# -----------------------------
numericas = ['Seguidores', 'Tweets', 'Following', 'Goal']

for col in numericas:
    print(f"\n🔸 Estadísticas para: {col}")
    print(f"  • Moda: {df[col].mode().iloc[0]}")
    print(f"  • Rango: {df[col].max() - df[col].min()}")
    
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
    print(f"  • Posibles outliers: {len(outliers)}")
