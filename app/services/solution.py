import pandas as pd

def get_solution():
    return pd.read_csv("plantillas/solver.csv", encoding="utf-8").iloc[:, :4]

def get_student_a():
    df = pd.read_csv("plantillas/student1.csv", encoding="utf-8")
    return df.iloc[1:, [1]+ list(range(7, df.shape[1]))[0:-4]]

def get_student_b():
    df = pd.read_csv("plantillas/student2.csv", encoding="utf-8")
    return df.iloc[1:, [1]+ list(range(7, df.shape[1]))]

def main():
    print ( get_solution().head())

main()