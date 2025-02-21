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
        'Inglés': 0,
        'Matemáticas': 0,
        'Ciencias Naturales': 0,
        'Ciencias sociales': 0,
        'Comprención lectora': 0
    }
    print (respuestas_correctas)
    # for index, respuesta in enumerate(respuestas_estudiante, start=1):
        
    #     print(f'Pregunta {index}: {respuesta}')
        # if respuesta == respuestas_correctas[index]:
        #     resultado[area[index]] += 1
    return resultado

def main():
    A = get_student_a()
    B = get_student_b()

    """
    merged contiene todas las respuestas de un estudiante con ID Number
    """
    merged = pd.merge(A, B, on="ID Number", how="outer", suffixes=('_A', '_B'))
    solucionario = get_solution()

    print (solucionario.iloc[:,2].head())

    respuestas_correctas = solucionario.iloc[:,2]
    area = solucionario.set_index('Pregunta')['Área'].to_dict()

    respuestas_estudiante = merged.iloc[0, 1:]

    #resultado = resultado_estudiante(respuestas_estudiante, respuestas_correctas, area)

    #print (resultado)

main()