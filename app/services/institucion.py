import pandas as pd

def get_solution():
    return pd.read_csv("templates/result.csv", encoding="utf-8")

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
    lectura_critica = info_by_area(resultados_estudiantes, 'lectura_critica', 35, 50, 65)
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


def promedios_instituciones (resultados_estudiantes):
    df = pd.DataFrame(resultados_estudiantes)

    stats_por_institucion = df.groupby("Institucion")[[
        "ciencias_naturales",
        "matematicas",
        "ciencias_sociales",
        "ingles",
        "comprension_lectora",
        "total"
    ]].agg(['mean', 'std', 'min', 'max']).reset_index()

    stats_por_institucion.iloc[:, 1:] = stats_por_institucion.iloc[:, 1:].round(0).astype(int)


    stats_por_institucion.columns = [
        f"{col[0]}_{col[1]}" if col[1] else col[0]
        for col in stats_por_institucion.columns.values
    ]

    return stats_por_institucion.to_dict(orient='records')

def get_all_means(resultados_estudiantes):

    resultados = resultados_estudiantes.iloc[:, 4:-2]
    
    medias = resultados.mean(axis=0).round(2)

    return(medias)


get_all_means(get_solution())