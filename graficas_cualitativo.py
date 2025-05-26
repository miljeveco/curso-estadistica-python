import csv
import argparse
import matplotlib.pyplot as plt
from collections import Counter
import os

def leer_columna_cualitativa(nombre_archivo):
    datos = []
    with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezado
        for fila in lector:
            if fila and fila[0].strip():
                datos.append(fila[0].strip())
    return datos

def calcular_frecuencias(datos):
    conteo = Counter(datos)
    total = sum(conteo.values())
    frecuencias = {}
    for categoria, fa in conteo.items():
        fr = fa / total
        frecuencias[categoria] = (fa, fr)
    return frecuencias

def graficar_barras(frecuencias, base_nombre):
    categorias = list(frecuencias.keys())
    cantidades = [frecuencias[c][0] for c in categorias]
    porcentajes = [frecuencias[c][1] for c in categorias]

    plt.figure(facecolor='white')
    bars = plt.bar(categorias, cantidades, width=0.8, color='skyblue', edgecolor='black')  # ancho reducido

    for i, bar in enumerate(bars):
        altura = bar.get_height()
        etiqueta = f"{cantidades[i]} ({porcentajes[i]*100:.1f}%)"
        plt.text(bar.get_x() + bar.get_width() / 2, altura, etiqueta,
                 ha='center', va='bottom', fontsize=9)

    plt.title("Gráfico de Barras - Frecuencia Absoluta y Relativa")
    plt.xlabel("Categoría")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, linestyle='--', axis='y', alpha=0.8)
    plt.savefig(f"barras_{base_nombre}.png", facecolor='white')
    plt.close()


def graficar_circular(frecuencias, base_nombre):
    categorias = list(frecuencias.keys())
    cantidades = [frecuencias[c][0] for c in categorias]
    total = sum(cantidades)
    etiquetas = [
        f"{cat}\n{fa} ({fr*100:.1f}%)"
        for cat, (fa, fr) in frecuencias.items()
    ]
    
    plt.figure(facecolor='white')
    plt.pie(cantidades, labels=etiquetas, startangle=90, textprops={'fontsize': 9})
    plt.title("Gráfico Circular - Frecuencia Absoluta y Relativa")
    plt.tight_layout()
    plt.savefig(f"circular_{base_nombre}.png", facecolor='white')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Gráficas de datos cualitativos")
    parser.add_argument("entrada", help="Archivo CSV de entrada con datos cualitativos")
    args = parser.parse_args()

    archivo_entrada = args.entrada
    base_nombre = os.path.splitext(os.path.basename(archivo_entrada))[0]

    datos = leer_columna_cualitativa(archivo_entrada)
    if not datos:
        print("No se encontraron datos válidos.")
        return

    frecuencias = calcular_frecuencias(datos)
    graficar_barras(frecuencias, base_nombre)
    graficar_circular(frecuencias, base_nombre)

    print("Gráficas cualitativas generadas correctamente.")

if __name__ == "__main__":
    main()

