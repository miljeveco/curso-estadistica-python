import csv
import argparse
from collections import Counter

def calcular_frecuencias(lista):
    frecuencia_abs = Counter(lista)
    total = sum(frecuencia_abs.values())

    valores_ordenados = sorted(frecuencia_abs.keys())
    
    tabla = []
    acumulada = 0
    for valor in valores_ordenados:
        fa = frecuencia_abs[valor]
        acumulada += fa
        fr = fa / total
        tabla.append({
            'Valor': valor,
            'Frecuencia absoluta': fa,
            'Frecuencia acumulada': acumulada,
            'Frecuencia relativa': round(fr, 4),
            '% Frecuencia relativa': str(round(fr*100, 4))+'%'
        })
    return tabla

def leer_csv_primera_columna(nombre_archivo):
    lista = []
    with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezado
        for fila in lector:
            if fila:
                lista.append(int(fila[1]))
    return lista

def escribir_tabla_frecuencia(tabla, nombre_salida):
    with open(nombre_salida, mode='w', newline='', encoding='utf-8') as archivo:
        campos = ['Valor', 'Frecuencia absoluta', 'Frecuencia acumulada', 'Frecuencia relativa','% Frecuencia relativa']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in tabla:
            escritor.writerow(fila)

def main():
    parser = argparse.ArgumentParser(description="Calcula tabla de frecuencias a partir de un CSV")
    parser.add_argument("entrada", help="Nombre del archivo CSV de entrada")
    parser.add_argument("salida", help="Nombre del archivo CSV de salida")
    args = parser.parse_args()

    lista_valores = leer_csv_primera_columna(args.entrada)
    tabla_frecuencia = calcular_frecuencias(lista_valores)
    escribir_tabla_frecuencia(tabla_frecuencia, args.salida)

    print(f"Tabla de frecuencias guardada en: {args.salida}")

if __name__ == "__main__":
    main()

