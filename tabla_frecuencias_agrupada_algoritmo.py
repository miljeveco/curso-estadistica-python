import csv
import argparse
import math

def leer_datos_numericos(nombre_archivo):
    datos = []
    with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezado
        for fila in lector:
            if fila and fila[0].strip():
                try:
                    datos.append(float(fila[0]))
                except ValueError:
                    pass  # Ignorar valores no numéricos
    return datos

def construir_intervalos(datos, k=None):
    minimo = min(datos)
    maximo = max(datos)
    rango = maximo - minimo

    if k is None:
        k = round(1 + 3.322 * math.log10(len(datos)))  # Regla de Sturges
    amplitud = math.ceil(rango / k)

    intervalos = []
    inicio = minimo
    for _ in range(k):
        fin = inicio + amplitud
        intervalos.append((inicio, fin))
        inicio = fin
    return intervalos

def calcular_frecuencias_agrupadas(datos, intervalos):
    tabla = []
    fa_total = 0
    fa_acumulada = 0

    for (li, ls) in intervalos:
        # Frecuencia absoluta
        fa = 0
        for x in datos:
            if li <= x < ls or (x == ls and ls == intervalos[-1][1]):  # incluye extremo derecho del último
                fa += 1
        fa_acumulada += fa
        fr = fa / len(datos)
        marca = (li + ls) / 2

        tabla.append({
            'Límite inferior': round(li, 2),
            'Límite superior': round(ls, 2),
            'Marca de clase': round(marca, 2),
            'Frecuencia absoluta': fa,
            'Frecuencia acumulada': fa_acumulada,
            'Frecuencia relativa': round(fr, 4)
        })
        fa_total += fa

    return tabla

def escribir_csv(tabla, nombre_salida):
    with open(nombre_salida, mode='w', newline='', encoding='utf-8') as archivo:
        campos = ['Límite inferior', 'Límite superior', 'Marca de clase', 'Frecuencia absoluta', 'Frecuencia acumulada', 'Frecuencia relativa']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in tabla:
            escritor.writerow(fila)

def main():
    parser = argparse.ArgumentParser(description="Calcula tabla de frecuencias para datos agrupados")
    parser.add_argument("entrada", help="Archivo CSV con datos numéricos (1ra columna)")
    parser.add_argument("salida", help="Archivo CSV donde guardar tabla de frecuencias")
    parser.add_argument("--clases", type=int, default=None, help="Número de clases (intervalos)")
    args = parser.parse_args()

    datos = leer_datos_numericos(args.entrada)
    if not datos:
        print("No se encontraron datos numéricos válidos en el archivo.")
        return

    intervalos = construir_intervalos(datos, args.clases)
    tabla = calcular_frecuencias_agrupadas(datos, intervalos)
    escribir_csv(tabla, args.salida)

    print(f"Tabla de frecuencias agrupadas guardada en: {args.salida}")

if __name__ == "__main__":
    main()

