import pandas as pd
import numpy as np
from scipy.stats import percentileofscore

def get_solution():
    return pd.read_csv("templates/solver.csv", encoding="utf-8")

def get_student_a():
    df = pd.read_csv("templates/student1.csv", encoding="utf-8")
    return df

def resultado_estudiante(respuestas_estudiante, respuestas_correctas, area, componente):
    """
    Calcula el resultado de un estudiante
    """
    resultado = {
        'codigo': int(respuestas_estudiante.iloc[0]),
        #AREAS
        'FÍSICA': 0,
        'LECTURA CRÍTICA': 0,
        'QUÍMICA':0,
        'CIENCIAS SOCIALES': 0,
        'MATEMÁTICAS': 0,
        'BIOLOGÍA': 0,

        #componentes conceptuales
        "Identificación de la causa de un fenómeno (disminución de luminosidad) a partir de la información explícita del texto (método de los tránsitos).": 0,
        "Inferencia de una relación de proporcionalidad directa entre el tamaño del planeta y la magnitud del efecto observado.": 0,
        "Correlación entre una representación gráfica (curva de luz) y el fenómeno físico que describe (el paso del planeta frente a la estrella)": 0,
        "Comprensión del propósito de una técnica científica complementaria (velocidades radiales) para obtener un perfil más completo de un objeto de estudio.": 0,
        "Predicción de un resultado (forma de la curva de luz) aplicando un principio científico a una situación hipotética con múltiples variables.": 0,
        "Identificación de la función retórica de un párrafo (introducir y contextualizar el tema) dentro de la estructura global de un texto.": 0,
        "Comprensión de la función de un elemento gramatical (aclaración parentética) para especificar el punto de vista o marco de referencia.": 0,
        "Inferencia de la intención del autor (divulgación científica) a partir del tono, estilo y contenido general del texto.": 0,
        "Reflexión sobre la relación entre el avance tecnológico y la transformación de una pregunta filosófica en un campo de investigación empírica.": 0,
        "Interpretación del propósito de usar la escala cósmica para contextualizar la existencia humana y evaluar la probabilidad de vida en el universo.": 0,
        "Aplicación de operaciones con notación científica para calcular una cantidad total a partir de los datos proporcionados.": 0,
        "Cálculo de una razón o proporción entre dos valores porcentuales para establecer una comparación cuantitativa": 0,
        "Aplicación del concepto de porcentaje para calcular un valor específico a partir de un total y una proporción.": 0,
        "Comprensión del uso de una línea base o valor de referencia (concordancia al azar del 25%) para contextualizar y evaluar la significancia de un dato.": 0,
        "Inferencia de la intención crítica del autor sobre la divulgación científica a partir del análisis del título y el tono del texto.": 0,
        "Conocimiento sobre la herencia de genes conservados a partir de un ancestro común muy lejano como explicación de similitudes genéticas.": 0,
        "Relación entre el grado de similitud genética y la cercanía evolutiva (ancestro común más reciente) entre diferentes especies.": 0,
        "Conocimiento de la naturaleza química de los componentes del ADN, específicamente la identificación de las bases nitrogenadas.": 0,
        "Conocimiento de la estructura del ADN, identificando los puentes de hidrógeno como la interacción que une las dos hebras.": 0,
        "Reflexión sobre cómo la simplificación del conocimiento científico para el público puede llevar a la distorsión y creación de anécdotas imprecisas.": 0,
        "Comprensión del uso de analogías (dado de cuatro caras) como una herramienta pedagógica para hacer accesibles conceptos científicos abstractos": 0,
        "Reflexión sobre la búsqueda de la identidad humana y nuestro lugar en la naturaleza como motivación antropológica detrás de la comparación genómica.": 0,
        "Cálculo de un porcentaje (la diferencia) sobre un número grande para determinar una cantidad específica de pares de bases.": 0,
        "Cálculo de la probabilidad de un evento complementario (no coincidencia) a partir de la probabilidad del evento principal (coincidencia).": 0,
        "Aplicación de principios de combinatoria (principio de la multiplicación) para calcular el número total de posibles secuencias distintas.": 0
    }
    for index, respuesta in enumerate(respuestas_estudiante[2:], start=0):
        if respuesta == respuestas_correctas[index]:
            resultado[area[index]] += 1
            if not pd.isna(componente[index]):
                resultado[componente[index]] += 1
    return resultado

def resultado_estudiantes(respuestas_estudiantes, respuestas_correctas, area, componente):
    """
    Calcula el resultado de varios estudiantes
    """
    resultados = []
    for i in range(respuestas_estudiantes.shape[0]):
        
        resultado = resultado_estudiante(respuestas_estudiantes.iloc[i], respuestas_correctas, area, componente)
        resultados.append(resultado)
    return resultados




def get_all():
    A = get_student_a()

    """
    merged contiene todas las respuestas de los estudiantes con ID Number
    es decir, el ID Number de cada estudiante con las respuestas
    """
    merged = A
    
    solucionario = get_solution()

    respuestas_correctas = solucionario.iloc[:,2]
    area = solucionario.iloc[:,1]
    componente = solucionario.iloc[:,3]

    
    resultados = resultado_estudiantes(merged, respuestas_correctas, area, componente)
    
    
    res = pd.DataFrame(resultados)
    
    count_questions = area.value_counts()
    count_questions = 5 / count_questions

    componentes_value = componente.value_counts()
    componentes_value = 1 / componentes_value


    for area_name in ['FÍSICA', 'LECTURA CRÍTICA', 'QUÍMICA', 'CIENCIAS SOCIALES', 'MATEMÁTICAS', 'BIOLOGÍA']:
        res[area_name] = res[area_name].astype(float)
        res[area_name] = (res[area_name] * float(count_questions[area_name])).round(1)
        res[area_name] = np.floor(res[area_name] + 0.5)


    for componente_name in componentes_value.index:
        if componente_name in res.columns:
            res[componente_name] = res[componente_name] * componentes_value[componente_name]

    res.columns = [
        'codigo', 
        'FISICA', 
        'LECTURA_CRÍTICA', 
        'QUÍMICA',
        'CIENCIAS_SOCIALES', 
        'MATEMÁTICAS', 
        'BIOLOGÍA',

        #Componentes
        "causa_fenomeno_transitos",
        "proporcionalidad_tamano_planeta",
        "curva_luz_fenomeno",
        "tecnica_velocidades_radiales",
        "prediccion_curva_luz",
        "funcion_retórica_parrafo",
        "funcion_elemento_gramatical",
        "intencion_autor_divulgacion",
        "avance_tecnologico_filosofia",
        "escala_cosmica_existencia",
        "operaciones_notacion_cientifica",
        "razon_proporcion_porcentual",
        "porcentaje_valor_especifico",
        "linea_base_concordancia_azar",
        "intencion_critica_autor",
        "herencia_genes_ancestro",
        "similitud_genetica_evolucion",
        "componentes_quimicos_adn",
        "estructura_adn_puentes_hidrogeno",
        "simplificacion_conocimiento_publico",
        "analogias_conceptos_cientificos",
        "identidad_humana_genomica",
        "porcentaje_diferencia_pares_bases",
        "probabilidad_evento_complementario",
        "principio_multiplicacion_combinatoria"
               
        ]
    res = res.astype(int)
    
    # Verificar si existen códigos repetidos en 'res'
    
    codes_with_name = pd.read_csv("templates/codes.csv", encoding="utf-8")
    codes_with_name['Grupo'] = codes_with_name['Grupo'].fillna(0).astype(int).astype(str)
    #codes_with_name['Documento'] = codes_with_name['Documento'].fillna(0).astype(int).astype(str)

    #codes_with_name = codes_with_name.drop(columns=['Firma'])
    final_df = pd.merge(codes_with_name, res, on="codigo", how="right")
    
    final_df = final_df.fillna(0)
    
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
