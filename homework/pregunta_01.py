from pathlib import Path
import pandas as pd

def pregunta_01():
    """
    Carga, limpia y guarda el archivo de solicitudes de crédito.
    Todo el proceso se hace en esta función sin ayuda de funciones auxiliares externas.
    """

    # Leer el archivo original
    entrada = Path("files/input/solicitudes_de_credito.csv")
    df = pd.read_csv(entrada, sep=";", index_col=0)

    # Eliminar valores nulos
    df = df.dropna()

    # Limpiar y convertir monto del crédito
    df["monto_del_credito"] = df["monto_del_credito"].apply(
        lambda x: float(x.replace("$ ", "").replace(",", ""))
    )

    # Formato general para columnas de texto
    columnas_texto = [
        "tipo_de_emprendimiento", "barrio", "idea_negocio", "línea_credito"
    ]
    for col in columnas_texto:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(".", "_")
            .str.replace("-", "_")
        )
        if col != "barrio":
            df[col] = df[col].str.strip()
        df[col] = df[col].astype("category")

    # Limpieza de columnas específicas
    df["sexo"] = df["sexo"].str.lower().astype("category")
    df["estrato"] = df["estrato"].astype("category")
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int).astype("category")
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], dayfirst=True, format="mixed"
    )

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Guardar archivo limpio
    salida = Path("files/output/solicitudes_de_credito.csv")
    salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(salida, sep=";")
