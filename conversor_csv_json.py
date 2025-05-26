import csv
import json
import sys
import os

def csv_a_json(archivo_csv, archivo_json):
    try:
        with open(archivo_csv, mode='r', encoding='utf-8') as f_csv:
            lector = csv.DictReader(f_csv)
            datos = list(lector)
        with open(archivo_json, mode='w', encoding='utf-8') as f_json:
            json.dump(datos, f_json, indent=4, ensure_ascii=False)
        print(f"Conversión completada: {archivo_csv} → {archivo_json}")
    except Exception as e:
        print(f"Error al convertir CSV a JSON: {e}")

def json_a_csv(archivo_json, archivo_csv):
    try:
        with open(archivo_json, mode='r', encoding='utf-8') as f_json:
            datos = json.load(f_json)
        if not datos:
            raise ValueError("El archivo JSON está vacío o no contiene una lista de objetos.")
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f_csv:
            campos = datos[0].keys()
            escritor = csv.DictWriter(f_csv, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(datos)
        print(f"Conversión completada: {archivo_json} → {archivo_csv}")
    except Exception as e:
        print(f"Error al convertir JSON a CSV: {e}")

def main():
    tipo_conversion = input("Tipo de conversión (csv-json / json-csv): ").strip().lower()
    archivo_entrada = input("Nombre del archivo de entrada: ").strip()
    archivo_salida = input("Nombre del archivo de salida: ").strip()

    if tipo_conversion == 'csv-json':
        csv_a_json(archivo_entrada, archivo_salida)
    elif tipo_conversion == 'json-csv':
        json_a_csv(archivo_entrada, archivo_salida)
    else:
        print("Tipo de conversión no válido. Usa 'csv-json' o 'json-csv'.")

if __name__ == '__main__':
    main()

