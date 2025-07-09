import pandas as pd
from scipy.stats import percentileofscore

def get_solution():
    return pd.read_csv("templates/solver.csv", encoding="utf-8")

def get_student_a():
    df = pd.read_csv("templates/student1.csv", encoding="utf-8")
    return df.iloc[:, [1]+ list(range(7, df.shape[1]))]

def get_student_b():
    df = pd.read_csv("templates/student2.csv", encoding="utf-8")
    return df.iloc[:, [1]+ list(range(7, df.shape[1]))]

def resultado_estudiante(respuestas_estudiante, respuestas_correctas, area, componente, competencia):
    """
    Calcula el resultado de un estudiante
    """
    resultado = {
        'codigo': int(respuestas_estudiante.iloc[0]),
        'Ciencias Naturales': 0,
        'Matemáticas': 0,
        'Ciencias sociales': 0,
        'Lectura': 0,
        'Aleatorio': 0,
        'Numérico-variacional': 0,
        'Espacial-métrico': 0,
        'Entorno vivo': 0,
        'CTS': 0,
        'Entorno físico': 0,
        'Multiperspectivismo': 0,
        'Pensamiento sistémico': 0,
        'Conocimiento': 0,
        'Planteamiento y resolución de problemas': 0,
        'Comunicación, modelación y representación': 0,
        'Razonamiento y argumentación': 0,
        'Comprende el sentido local y global del texto mediante inferencias de información implícita': 0,
        'Asume una posición crítica sobre el texto mediante la evaluación de su forma y contenido.': 0,
        'Recupera información literal expresada en fragmentos del texto.': 0,
        'Argumentación en contextos ciudadanos': 0,
    }
    for index, respuesta in enumerate(respuestas_estudiante[1:], start=0):
        if respuesta == respuestas_correctas[index]:
            resultado[area[index]] += 1
            if not pd.isna(componente[index]):
                resultado[componente[index]] += 1
            if not pd.isna(competencia[index]):
                resultado[competencia[index]] += 1
    return resultado

def resultado_estudiantes(respuestas_estudiantes, respuestas_correctas, area, componente, competencia):
    """
    Calcula el resultado de varios estudiantes
    """
    resultados = []
    for i in range(respuestas_estudiantes.shape[0]):
        
        resultado = resultado_estudiante(respuestas_estudiantes.iloc[i], respuestas_correctas, area, componente, competencia)
        resultados.append(resultado)
    return resultados

def calcular_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade una columna 'percentil' al DataFrame que indica el
    porcentaje de estudiantes con un puntaje total inferior dentro de cada IE.
    """
    df = df.copy()
    df["percentil"] = df.groupby("Institucion")["total"].transform(
        lambda x: x.apply(lambda v: int(round(percentileofscore(x, v, kind="rank"))))
    )
    return df

def calcular_puestos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade una columna 'puesto' al DataFrame que indica el puesto de cada estudiante
    dentro de su IE, ordenado jerárquicamente por total, matemáticas,
    comprensión lectora, ciencias naturales, ciencias sociales e inglés.
    """
    df = df.copy()
    
    # Definir columnas de orden jerárquico
    orden = [
        "total",
        "matematicas",
        "lectura_critica",
        "ciencias_naturales",
        "ciencias_sociales",
    ]
    
    # Ordenar por Institucion + criterios de desempate
    df.sort_values(
        by=["Institucion"] + orden,
        ascending=[True] + [False] * len(orden),
        inplace=True,
    )
    
    # Asignar puesto: enumerar dentro de cada municipio
    df["puesto"] = (
        df.groupby("Institucion").cumcount() + 1
    )
    
    return df




def get_all():
    A = get_student_a()

    """
    merged contiene todas las respuestas de los estudiantes con ID Number
    es decir, el ID Number de cada estudiante con las respuestas
    """
    #merged = pd.merge(A, B, on="ID Number", how="outer", suffixes=('_A', '_B'))
    
    solucionario = get_solution()

    respuestas_correctas = solucionario.iloc[:,2]
    area = solucionario.iloc[:,3]
    componente = solucionario.iloc[:,4]
    Competencia = solucionario.iloc[:,5]

    
    resultados = resultado_estudiantes(A, respuestas_correctas, area, componente, Competencia)
    
    
    res = pd.DataFrame(resultados)

    print (res.head())
    
    count_questions = area.value_counts()

    count_questions = 100 / count_questions

    componentes_value = componente.value_counts()
    componentes_value = 100 / componentes_value

    competencias_value = Competencia.value_counts()
    competencias_value = 100 / competencias_value

    for area_name in ['Ciencias Naturales', 'Matemáticas', 'Ciencias sociales', 'Lectura']:
        res[area_name] = res[area_name] * count_questions[area_name]

    for componente_name in componentes_value.index:
        if componente_name in res.columns:
            res[componente_name] = res[componente_name] * componentes_value[componente_name]

    for competencia_name in competencias_value.index:
        if competencia_name in res.columns:
            res[competencia_name] = res[competencia_name] * competencias_value[competencia_name]
    
    res['total'] = (
        res['Lectura'] * 3 +
        res['Matemáticas'] * 3 +
        res['Ciencias sociales'] * 3 +
        res['Ciencias Naturales'] * 3
    ) / 12

    res['total'] = (res['total'] * 4).round()
    res.columns = [
        'codigo', 'ciencias_naturales', 'matematicas', 'ciencias_sociales', 'lectura_critica', 
        'aleatorio', 'numerico_variacional', 'espacial_metricos', 'entorno_vivo',
        'cts', 'entorno_fisico', 'multiperspectivismo', 'pensamiento_sistemico',
        'conocimiento', 'planteamiento_y_resolucion_de_problemas',
        'comunicacion_modelacion_y_representacion', 'razonamiento_y_argumentacion',
        'comprende_sentido_del_texto', 'asume_posicion_critica', 'recupera_informacion_literal',
        'argumentacion_en_contextos_ciudadanos',
        'total',        
        ]
    res = res.astype(int)
    
    # Verificar si existen códigos repetidos en 'res'
    
    codes_with_name = pd.read_csv("templates/codes.csv", encoding="utf-8")
    codes_with_name['Grupo'] = codes_with_name['Grupo'].fillna(0).astype(int).astype(str)
    #codes_with_name['Documento'] = codes_with_name['Documento'].fillna(0).astype(int).astype(str)

    #codes_with_name = codes_with_name.drop(columns=['Firma'])
    final_df = pd.merge(codes_with_name, res, on="codigo", how="right")
    
    final_df = final_df.fillna(0)
    final_df = calcular_percentiles(final_df)
    final_df = calcular_puestos(final_df)
    
    # Verificar si existen códigos repetidos en 'final_df'
    duplicated_codes = final_df[final_df.duplicated(subset=['codigo'], keep=False)]
    if not duplicated_codes.empty:
        print("Códigos repetidos encontrados:")
        for _, row in duplicated_codes.iterrows():
            print(f"Código: {row['codigo']}, Municipio: {row.get('Municipio', 'N/A')}")
    
    final_df.to_csv("templates/final_results.csv", index=False, encoding="utf-8")
    return final_df
    

estudiantes = get_all()
#promedio_general(estudiantes)
