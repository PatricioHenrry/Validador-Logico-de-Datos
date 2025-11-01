"""
Validador lógico de registros


"""


from typing import List, Tuple
import pandas as pd
import re
import sys
from pathlib import Path


# ----- Config -----
EDAD_MIN, EDAD_MAX = 0, 100
DNI_MIN_DIG, DNI_MAX_DIG = 7, 8
CAT_SEXO = {"H", "M"}              
CAT_PLAN = {"basico", "premium"}  


def norm_str(x) -> str:
    return "" if pd.isna(x) else str(x).strip()


def normalizar_sexo(s: str) -> str:
    s = norm_str(s).strip().upper()
    if s in {"H", "HOMBRE"}:
        return "H"
    if s in {"M", "MUJER"}:
        return "M"
    return s  


# ----- Validación por fila -----
def validar_fila(fila: pd.Series, dni_duplicado: bool) -> Tuple[bool, List[str]]:
    razones: List[str] = []


    dni = norm_str(fila.get("dni", ""))
    if not re.fullmatch(rf"\d{{{DNI_MIN_DIG},{DNI_MAX_DIG}}}", dni):
        razones.append("DNI inválido")
    if dni_duplicado:
        razones.append("DNI duplicado")


    try:
        edad = int(norm_str(fila.get("edad", "")))
    except Exception:
        edad = -999
    if not (EDAD_MIN <= edad <= EDAD_MAX):
        razones.append("Edad inválida")


    sexo = normalizar_sexo(fila.get("sexo", ""))
    if sexo not in CAT_SEXO:
        razones.append("Sexo inválido")


    plan = norm_str(fila.get("plan_salud", "")).lower()
    if plan not in CAT_PLAN:
        razones.append("Plan inválido")


    es_valido = len(razones) == 0
    return es_valido, (["OK"] if es_valido else razones)


# ----- Validación del DataFrame completo -----
def validar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    columnas = ["dni", "nombre", "edad", "sexo", "plan_salud"]
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}. Se esperaban: {columnas}")


    out = df.copy()


    out["dni"] = out["dni"].apply(norm_str)
    out["nombre"] = out["nombre"].apply(norm_str)
    out["edad"] = out["edad"].apply(norm_str)
    out["sexo"] = out["sexo"].apply(norm_str)
    out["plan_salud"] = out["plan_salud"].apply(norm_str)


    out["_dni_duplicado"] = out["dni"].duplicated(keep=False)


    resultados = out.apply(lambda fila: validar_fila(fila, bool(fila["_dni_duplicado"])), axis=1)
    out["es_valido"] = resultados.apply(lambda x: x[0])
    out["explicacion"] = resultados.apply(lambda x: "; ".join(x[1]))


    out.drop(columns=["_dni_duplicado"], inplace=True)
    return out


# ----- Entradas -----
def cargar_por_teclado() -> pd.DataFrame:
    print("Carga por teclado. Deje 'DNI' vacío para terminar.\n", file=sys.stderr)
    filas = []
    while True:
        dni_in = input("DNI (Enter para terminar): ").strip()
        if dni_in == "":
            break
        if not re.fullmatch(rf"\d{{{DNI_MIN_DIG},{DNI_MAX_DIG}}}", dni_in):
            print("Formato de DNI inválido. Intente de nuevo.\n", file=sys.stderr)
            continue


        nombre = input("Nombre y Apellido: ").strip()
        edad_in = input("Edad: ").strip()
        sexo_in = input("Sexo (Hombre/Mujer): ").strip()
        plan_in = input("Plan (Basico/Premium): ").strip()


        filas.append({
            "dni": dni_in,
            "nombre": nombre,
            "edad": edad_in,
            "sexo": sexo_in,
            "plan_salud": plan_in
        })
        print("Registro agregado.\n", file=sys.stderr)


    if not filas:
        print("No se ingresaron registros.", file=sys.stderr)
        return pd.DataFrame(columns=["dni", "nombre", "edad", "sexo", "plan_salud"])
    return pd.DataFrame(filas)


def ejemplo_minidataset() -> pd.DataFrame:
    data = [
        {"dni":"37290938","nombre":"Gabriel Palacios","edad":17,"sexo":"M","plan_salud":"premium"},
        {"dni":"93457250","nombre":"Fabricio Sbeded","edad":150,"sexo":"H","plan_salud":"basico"},
        {"dni":"33299034","nombre":"Juan Stardust","edad":44,"sexo":"X","plan_salud":"premium"},
        {"dni":"34965920","nombre":"Ziggy Treli","edad":500,"sexo":"M","plan_salud":""},
        {"dni":"42441983","nombre":"Mariela Lana","edad":20,"sexo":"M","plan_salud":"basico"},
    ]
    return pd.DataFrame(data)


def guardar_unico_csv(df: pd.DataFrame, base_nombre: str = "salida_validada"):
    carpeta = Path(".")
    carpeta.mkdir(parents=True, exist_ok=True)


    existentes = sorted(carpeta.glob(f"{base_nombre}_*.csv"))
    if existentes:
        ultimo = existentes[-1].stem.split("_")[-1]
        try:
            n = int(ultimo) + 1
        except Exception:
            n = 1
    else:
        n = 1
    nombre = f"{base_nombre}_{n}.csv"
    ruta = carpeta / nombre
    df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"\nArchivo generado: {ruta.resolve()}")


# ----- Main -----
def main():
    print("=== Validador — modo simple con guardado incremental ===")
    print("1) Cargar por teclado")
    print("2) Usar dataset de ejemplo")
    opcion = input("Elegí una opción [1/2]: ").strip()


    if opcion == "1":
        df_in = cargar_por_teclado()
    elif opcion == "2":
        df_in = ejemplo_minidataset()
    else:
        print("Opción inválida. Saliendo.")
        return


    if df_in.empty:
        print("No hay datos para validar. Saliendo.")
        return


    df_val = validar_dataframe(df_in)
    print("\n=== Vista previa (primeras filas) ===")
    try:
        with pd.option_context('display.max_columns', None, 'display.width', 120):
            print(df_val.head(20).to_string(index=False))
    except Exception:
        print(df_val.head(20).to_string(index=False))


    guardar_unico_csv(df_val)


if __name__ == "__main__":
    main()



