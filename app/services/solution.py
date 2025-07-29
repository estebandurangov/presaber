import pandas as pd
from scipy.stats import percentileofscore

def get_solution():
    return pd.read_csv("templates/solver.csv", encoding="utf-8")

def get_student_a():
    df = pd.read_csv("templates/student1.csv", encoding="utf-8")
    return df.iloc[:, [1]+ list(range(8, df.shape[1]))]

def get_student_b():
    df = pd.read_csv("templates/student2.csv", encoding="utf-8")
    return df.iloc[:, [1]+ list(range(8, df.shape[1]))]

def resultado_estudiante(respuestas_estudiante, respuestas_correctas, area, componente, competencia):
    """
    Calcula el resultado de un estudiante
    """
    resultado = {
        'codigo': int(respuestas_estudiante.iloc[0]),
        'Ciencias Naturales': 0,
        'Matemáticas': 0,
        'Ciencias sociales': 0,
        'Inglés': 0,
        'Comprension lectora': 0,
        'Estadística': 0,
        'Algebra y Cálculo': 0,
        'Geometría': 0,
        'Fisica': 0,
        'Biologia': 0,
        'Quimica': 0,
        'Reflexionar a partir de un texto y evaluar su contenido': 0,
        'Identificar y entender los contenidos locales que conforman un texto': 0,
        'Comprender cómo se articulan las partes de un texto para darle un sentido global': 0,
        'Pensamiento Social': 0,
        'Pensamiento reflexivo y sistémico': 0,
        'Interpretación y análisis de perspectivas': 0,
        'Léxico': 0,
        'Pragmático': 0,
        'Comunicativo': 0,
        'Gramatical': 0,
        'Comprensión lectora': 0,
        'Lectura inferencial': 0,
        'Léxico-gramatical': 0,
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
        "comprension_lectora",
        "ciencias_naturales",
        "ciencias_sociales",
        "ingles",
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
    B = get_student_b()

    """
    merged contiene todas las respuestas de los estudiantes con ID Number
    es decir, el ID Number de cada estudiante con las respuestas
    """
    merged = pd.merge(A, B, on="ID Number", how="outer", suffixes=('_A', '_B'))
    
    solucionario = get_solution()

    respuestas_correctas = solucionario.iloc[:,2]
    area = solucionario.iloc[:,3]
    componente = solucionario.iloc[:,4]
    Competencia = solucionario.iloc[:,5]

    
    resultados = resultado_estudiantes(merged, respuestas_correctas, area, componente, Competencia)
    
    
    res = pd.DataFrame(resultados)
    
    count_questions = area.value_counts()

    count_questions = 100 / count_questions

    componentes_value = componente.value_counts()
    componentes_value = 100 / componentes_value

    competencias_value = Competencia.value_counts()
    competencias_value = 100 / competencias_value

    for area_name in ['Ciencias Naturales', 'Matemáticas', 'Ciencias sociales', 'Inglés', 'Comprension lectora']:
        res[area_name] = res[area_name] * count_questions[area_name]

    for componente_name in componentes_value.index:
        if componente_name in res.columns:
            res[componente_name] = res[componente_name] * componentes_value[componente_name]

    for competencia_name in competencias_value.index:
        if competencia_name in res.columns:
            res[competencia_name] = res[competencia_name] * competencias_value[competencia_name]
    
    res['total'] = (
        res['Inglés'] * 1 +
        res['Comprension lectora'] * 3 +
        res['Matemáticas'] * 3 +
        res['Ciencias sociales'] * 3 +
        res['Ciencias Naturales'] * 3
    ) / 13

    res['total'] = (res['total'] * 5).round()
    res.columns = [
        'codigo', 'ciencias_naturales', 'matematicas', 'ciencias_sociales', 'ingles', 'lectura_critica', 
        'estadistica', 'algebra','geometria', 
        'fisica', 'biologia', 'quimica ',
        'evaluar_texto', 'entender_contenidos', 'articular_partes',
        'pensamiento_social', 'pensamiento_reflexivo', 'interpretacion_perspectivas',
        'lexico', 'pragmatico', 'comunicativo', 'gramatical',
        'comprension_lectora', 'lectura_inferencial', 'lexico_gramatical',
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
            print(f"Código: {row['codigo']}, Institucion: {row.get('Institucion', 'N/A')}")
    
    final_df.to_csv("templates/final_results.csv", index=False, encoding="utf-8")
    return final_df
    

estudiantes = get_all()
#promedio_general(estudiantes)
