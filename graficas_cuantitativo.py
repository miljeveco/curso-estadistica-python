import csv
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import os

def leer_columna_numerica(nombre_archivo):
    datos = []
    with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezado
        for fila in lector:
            try:
                datos.append(float(int(fila[1])))
            except (ValueError, IndexError):
                pass
    return datos

def calcular_frecuencias(datos):
    conteo = Counter(datos)
    total = sum(conteo.values())

    valores_ordenados = sorted(conteo)
    acumulada = 0
    tabla = []

    for valor in valores_ordenados:
        fa = conteo[valor]
        acumulada += fa
        fr = fa / total
        tabla.append({
            'Valor': valor,
            'FA': fa,
            'FR': round(fr, 4),
            'FAA': acumulada
        })
    return tabla

def guardar_tabla_csv(tabla, salida="tabla_frecuencias.csv"):
    df = pd.DataFrame(tabla)
    df.to_csv(salida, index=False)

def graficar_histograma_absoluto(tabla, base_nombre):
    x = [fila['Valor'] for fila in tabla]
    y = [fila['FA'] for fila in tabla]
    plt.figure(facecolor='white')
    bars = plt.bar(x, y, color='skyblue', edgecolor='black')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, str(height), 
                 ha='center', va='bottom', fontsize=9)
    plt.title("Histograma de Frecuencia Absoluta")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia Absoluta")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(f"histograma_absoluto_{base_nombre}.png", facecolor='white')
    plt.close()

def graficar_histograma_relativo(tabla, base_nombre):
    x = [fila['Valor'] for fila in tabla]
    y = [fila['FR'] for fila in tabla]
    plt.figure(facecolor='white')
    bars = plt.bar(x, y, color='lightgreen', edgecolor='black')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, f"{100*height:.0f}%", 
                 ha='center', va='bottom', fontsize=9)
    plt.title("Histograma de Frecuencia Relativa")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia Relativa")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(f"histograma_relativo_{base_nombre}.png", facecolor='white')
    plt.close()

def graficar_poligono_absoluto(tabla, base_nombre):
    x = [fila['Valor'] for fila in tabla]
    y = [fila['FA'] for fila in tabla]
    plt.figure(facecolor='white')
    plt.plot(x, y, marker='o', linestyle='-', color='blue')
    for i, txt in enumerate(y):
        plt.text(x[i], y[i], str(txt), ha='center', va='bottom', fontsize=9)
    plt.title("Polígono de Frecuencia Absoluta")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia Absoluta")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(f"poligono_absoluto_{base_nombre}.png", facecolor='white')
    plt.close()

def graficar_poligono_relativo(tabla, base_nombre):
    x = [fila['Valor'] for fila in tabla]
    y = [fila['FR'] for fila in tabla]
    plt.figure(facecolor='white')
    plt.plot(x, y, marker='o', linestyle='-', color='green')
    for i, txt in enumerate(y):
        plt.text(x[i], y[i], f"{txt:.2f}", ha='center', va='bottom', fontsize=9)
    plt.title("Polígono de Frecuencia Relativa")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia Relativa")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(f"poligono_relativo_{base_nombre}.png", facecolor='white')
    plt.close()

def graficar_ojiva(tabla, base_nombre):
    x = [fila['Valor'] for fila in tabla]
    y = [fila['FAA'] for fila in tabla]
    plt.figure(facecolor='white')
    plt.plot(x, y, marker='o', linestyle='-', color='red')
    for i, txt in enumerate(y):
        plt.text(x[i], y[i], str(txt), ha='center', va='bottom', fontsize=9)
    plt.title("Ojiva (Frecuencia Acumulada)")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia Acumulada")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(f"ojiva_{base_nombre}.png", facecolor='white')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Genera tabla de frecuencias y gráficas estadísticas")
    parser.add_argument("entrada", help="Nombre del archivo CSV de entrada")
    args = parser.parse_args()

    archivo_entrada = args.entrada
    base_nombre = os.path.splitext(os.path.basename(archivo_entrada))[0]

    datos = leer_columna_numerica(archivo_entrada)
    if not datos:
        print("No se encontraron datos numéricos válidos.")
        return

    tabla = calcular_frecuencias(datos)
    guardar_tabla_csv(tabla, f"tabla_frecuencias_{base_nombre}.csv")

    graficar_histograma_absoluto(tabla, base_nombre)
    graficar_histograma_relativo(tabla, base_nombre)
    graficar_poligono_absoluto(tabla, base_nombre)
    graficar_poligono_relativo(tabla, base_nombre)
    graficar_ojiva(tabla, base_nombre)

    print("Gráficas y tabla generadas correctamente.")

if __name__ == "__main__":
    main()

