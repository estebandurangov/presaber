import pandas as pd
from scipy.stats import percentileofscore

def get_solution():
    return pd.read_csv("templates/solver.csv", encoding="utf-8").iloc[:, :4]

def get_student_a():
    df = pd.read_csv("templates/student1.csv", encoding="utf-8")
    return df.iloc[1:, [1]+ list(range(7, df.shape[1]))]

def get_student_b():
    df = pd.read_csv("templates/student2.csv", encoding="utf-8")
    return df.iloc[1:, [1]+ list(range(7, df.shape[1]))]

def resultado_estudiante(respuestas_estudiante, respuestas_correctas, area):
    """
    Calcula el resultado de un estudiante
    """
    resultado = {
        'codigo': int(respuestas_estudiante.iloc[0]),
        'Ciencias Naturales': 0,
        'Matemáticas': 0,
        'Ciencias sociales': 0,
        'Inglés': 0,
        'Comprención lectora': 0,
    }
    for index, respuesta in enumerate(respuestas_estudiante[1:], start=0):
        if respuesta == respuestas_correctas[index]:
            resultado[area[index]] += 1
    return resultado

def resultado_estudiantes(respuestas_estudiantes, respuestas_correctas, area):
    """
    Calcula el resultado de varios estudiantes
    """
    resultados = []
    for i in range(respuestas_estudiantes.shape[0]):
        resultado = resultado_estudiante(respuestas_estudiantes.iloc[i], respuestas_correctas, area)
        resultados.append(resultado)
    return resultados

def calcular_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade una columna 'percentil' al DataFrame que indica el
    porcentaje de estudiantes con un puntaje total inferior.
    """
    df = df.copy()
    df["percentil"] = df["total"].apply(lambda x: int(round(percentileofscore(df["total"], x, kind="rank"))))
    return df

def calcular_puestos(df: pd.DataFrame) -> pd.DataFrame:
    # Ordenamos por los criterios especificados
    df_ordenado = df.sort_values(
        by=["total", "matematicas", "comprension_lectora", "ciencias_naturales", "ciencias_sociales", "ingles"],
        ascending=[False] * 6
    ).reset_index(drop=True)

    # Asignamos los puestos
    df_ordenado["puesto"] = range(1, len(df_ordenado) + 1)

    # Usamos el código como identificador para hacer merge y restaurar el orden original
    df_con_puesto = df.merge(
        df_ordenado[["codigo", "puesto"]],
        on="codigo",
        how="left"
    )

    return df_con_puesto

def promedios_grupo (resultados_estudiantes):
    df = pd.DataFrame(resultados_estudiantes)

    stats_por_grupo = df.groupby("Grupo")[[
        "ciencias_naturales",
        "matematicas",
        "ciencias_sociales",
        "ingles",
        "comprension_lectora",
        "total"
    ]].agg(['mean', 'std', 'min', 'max']).reset_index()

    stats_por_grupo.iloc[:, 1:] = stats_por_grupo.iloc[:, 1:].round(0).astype(int)


    stats_por_grupo.columns = [
        f"{col[0]}_{col[1]}" if col[1] else col[0]
        for col in stats_por_grupo.columns.values
    ]

    return stats_por_grupo.to_dict(orient='records')

def info_by_area(resultados_estudiantes, area: str, lvl_1, lvl_2, lvl_3):
    df = pd.DataFrame(resultados_estudiantes)
    resumen_area = df[area].agg(['mean', 'std', 'min', 'max']).reset_index()
    niveles = {
        'lvl_1': ((df[area] <= lvl_1)).sum(),
        'lvl_2': ((df[area] > lvl_1) & (df[area] <= lvl_2)).sum(),
        'lvl_3': ((df[area] > lvl_2) & (df[area] <= lvl_3)).sum(),
        'lvl_4': (df[area] > lvl_3).sum()
    }
    niveles_df = pd.DataFrame.from_dict(niveles, orient='index', columns=[area]).reset_index()
    

    resumen_area = pd.concat([
        resumen_area,
        niveles_df
    ])
    

    return resumen_area


def promedio_general(resultados_estudiantes):
    lectura_critica = info_by_area(resultados_estudiantes, 'comprension_lectora', 35, 50, 65)
    matematicas = info_by_area(resultados_estudiantes, 'matematicas', 35, 50, 70)
    ciencias_naturales = info_by_area(resultados_estudiantes, 'ciencias_naturales', 40, 55, 70)
    ingles = info_by_area(resultados_estudiantes, 'ingles', 36, 57, 70)
    ciencias_sociales = info_by_area(resultados_estudiantes, 'ciencias_sociales', 40, 55, 70)
    total = info_by_area(resultados_estudiantes, 'total', 235, 315, 415)

    resumen_general = pd.concat([
        lectura_critica,
        matematicas,
        ciencias_naturales,
        ingles,
        ciencias_sociales,
        total
    ], axis=1)
    resumen_general = resumen_general.loc[:, ~resumen_general.columns.duplicated()]

    df_melted = resumen_general.melt(id_vars='index', var_name='area', value_name='valor')
    df_pivot = df_melted.pivot(index='area', columns='index', values='valor').reset_index()
    numeric_columns = df_pivot.select_dtypes(include=['number']).columns
    df_pivot[numeric_columns] = df_pivot[numeric_columns].round(1)
    
    return df_pivot.to_dict(orient='records')

def get_all():
    A = get_student_a()
    B = get_student_b()

    """
    merged contiene todas las respuestas de los estudiantes con ID Number
    es decir, el ID Number de cada estudiante con las respuestas
    """
    merged = pd.merge(A, B, on="ID Number", how="outer", suffixes=('_A', '_B'))
    solucionario = get_solution()

    respuestas_correctas = solucionario.iloc[:,2]
    area = solucionario.iloc[:,3]

    
    resultados = resultado_estudiantes(merged, respuestas_correctas, area)
    res = pd.DataFrame(resultados)
    
    count_questions = area.value_counts()

    count_questions = 100 / count_questions

    for area_name in ['Ciencias Naturales', 'Matemáticas', 'Ciencias sociales', 'Inglés', 'Comprención lectora']:
        res[area_name] = res[area_name] * count_questions[area_name]
    
    res['total'] = (
        res['Inglés'] * 1 +
        res['Comprención lectora'] * 3 +
        res['Matemáticas'] * 3 +
        res['Ciencias sociales'] * 3 +
        res['Ciencias Naturales'] * 3
    ) / 13

    res['total'] = (res['total'] * 5).round()
    print (res)
    res.columns = ['codigo', 'ciencias_naturales', 'matematicas', 'ciencias_sociales', 'ingles', 'comprension_lectora', 'total']
    res = res.astype(int)
    codes_with_name = pd.read_csv("templates/codes.csv", encoding="utf-8")
    codes_with_name['Grupo'] = codes_with_name['Grupo'].fillna(0).astype(int).astype(str)

    #codes_with_name = codes_with_name.drop(columns=['Firma'])
    final_df = pd.merge(codes_with_name, res, on="codigo", how="outer")
    final_df = final_df.fillna(0)
    final_df = calcular_percentiles(final_df)
    final_df = calcular_puestos(final_df)
    # print(final_df)
    final_df.to_csv("templates/final_results.csv", index=False, encoding="utf-8")
    return final_df.to_dict(orient='records')
    

estudiantes = get_all()
promedio_general(estudiantes)
