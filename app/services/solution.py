import pandas as pd

def get_solution():
    return pd.read_csv("templates/solver.csv", encoding="utf-8").iloc[:, :4]

def get_student_a():
    df = pd.read_csv("templates/student1.csv", encoding="utf-8")
    return df.iloc[1:, [1]+ list(range(7, df.shape[1]))[0:-4]]

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


def get_all():
    A = get_student_a()
    B = get_student_b()

    """
    merged contiene todas las respuestas de los estudiantes con ID Number
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
    res['total'] = res[['Ciencias Naturales', 'Matemáticas', 'Ciencias sociales', 'Inglés', 'Comprención lectora']].sum(axis=1)
    
    res.columns = ['codigo', 'ciencias_naturales', 'matematicas', 'ciencias_sociales', 'ingles', 'comprension_lectora', 'total']
    res = res.astype(int)

    return res.to_dict(orient='records')
    
get_all()