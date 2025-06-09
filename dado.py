import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import Counter
import time # Importamos time para el efecto de retardo

class DiceSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Dados - Probabilidad y Estadística")
        self.root.geometry("1100x800") # Aumentar el ancho para el nuevo layout
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50") # Fondo oscuro

        self.rolls = []
        self.current_roll_value = 1
        self.is_rolling = False # Bandera para evitar lanzamientos múltiples durante la animación

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50", bd=5, relief="raised")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        title_label = tk.Label(main_frame, text="¡Lanza el Dado y Explora la Probabilidad!",
                               font=("Arial", 28, "bold"), fg="#ecf0f1", bg="#2c3e50")
        title_label.pack(pady=20)

        # Frame para el contenido principal (dado + datos)
        content_frame = tk.Frame(main_frame, bg="#2c3e50")
        content_frame.pack(fill="both", expand=True)

        # --- Columna Izquierda: Dado y Botones de Lanzamiento ---
        left_column_frame = tk.Frame(content_frame, bg="#2c3e50")
        left_column_frame.pack(side="left", padx=20, pady=10, fill="y")

        # Área de visualización del dado
        self.dice_canvas = tk.Canvas(left_column_frame, width=200, height=200, bg="#ecf0f1", bd=0, highlightthickness=0, relief="flat")
        self.dice_canvas.pack(pady=20)
        self.draw_dice(self.current_roll_value)

        # Valor del lanzamiento actual
        self.roll_value_label = tk.Label(left_column_frame, text="Último lanzamiento: -",
                                         font=("Arial", 20, "bold"), fg="#3498db", bg="#2c3e50")
        self.roll_value_label.pack(pady=10)

        # Botón de lanzamiento individual
        self.roll_button = ttk.Button(left_column_frame, text="¡Lanzar Dado Una Vez!", command=self.start_roll_animation, style="TButton")
        self.roll_button.pack(pady=10)

        # --- Sección para N lanzamientos ---
        n_rolls_frame = tk.LabelFrame(left_column_frame, text="Lanzar N Veces",
                                      font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#34495e", bd=3, relief="groove")
        n_rolls_frame.pack(pady=20, padx=10, fill="x")

        n_entry_label = tk.Label(n_rolls_frame, text="Número de lanzamientos (N):",
                                 font=("Arial", 12), fg="#ecf0f1", bg="#34495e")
        n_entry_label.pack(pady=(10, 5))

        self.n_entry = ttk.Entry(n_rolls_frame, width=10, font=("Arial", 14))
        self.n_entry.insert(0, "100") # Valor por defecto
        self.n_entry.pack(pady=5)

        self.n_roll_button = ttk.Button(n_rolls_frame, text="Simular N Lanzamientos", command=self.simulate_n_rolls, style="TButton")
        self.n_roll_button.pack(pady=10)


        # --- Columna Derecha: Datos de Simulación ---
        right_column_frame = tk.Frame(content_frame, bg="#2c3e50")
        right_column_frame.pack(side="right", padx=20, pady=10, fill="both", expand=True)

        # Frame para la simulación
        simulation_frame = tk.LabelFrame(right_column_frame, text="Resultados de la Simulación",
                                         font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#34495e", bd=3, relief="groove")
        simulation_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Etiquetas para mostrar los datos de la simulación
        self.total_rolls_label = tk.Label(simulation_frame, text="Total de lanzamientos: 0",
                                          font=("Arial", 14), fg="#ecf0f1", bg="#34495e")
        self.total_rolls_label.pack(anchor="w", padx=10, pady=5)

        self.frequency_label = tk.Label(simulation_frame, text="Frecuencia de cada cara:\n",
                                        font=("Arial", 14), fg="#ecf0f1", bg="#34495e", justify="left")
        self.frequency_label.pack(anchor="w", padx=10, pady=5)

        self.relative_frequency_label = tk.Label(simulation_frame, text="Frecuencia relativa (Probabilidad empírica):\n",
                                                 font=("Arial", 14), fg="#ecf0f1", bg="#34495e", justify="left")
        self.relative_frequency_label.pack(anchor="w", padx=10, pady=5)

        # Botón para reiniciar
        reset_button = ttk.Button(main_frame, text="Reiniciar Simulación", command=self.reset_simulation, style="TButton")
        reset_button.pack(pady=10)

        # Configuración de estilo del botón
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 16, "bold"), background="#27ae60", foreground="#ffffff",
                        padding=10, relief="raised", borderwidth=0)
        style.map("TButton", background=[("active", "#2ecc71")])

        # Créditos (pequeños y abajo)
        credit_label = tk.Label(main_frame, text="Desarrollado para curso de Probabilidad y Estadística",
                                font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50")
        credit_label.pack(pady=5)

    def draw_dice(self, value):
        self.dice_canvas.delete("all")
        size = 200
        padding = 20
        dot_radius = 12

        # Dibujar el cuadrado del dado
        self.dice_canvas.create_rectangle(padding, padding, size - padding, size - padding,
                                          fill="#ffffff", outline="#34495e", width=5, tags="dice_body")

        # Coordenadas para los puntos
        dot_positions = {
            1: [(size/2, size/2)],
            2: [(size/4, size/4), (3*size/4, 3*size/4)],
            3: [(size/4, size/4), (size/2, size/2), (3*size/4, 3*size/4)],
            4: [(size/4, size/4), (3*size/4, 3*size/4), (size/4, 3*size/4), (3*size/4, size/4)],
            5: [(size/4, size/4), (3*size/4, 3*size/4), (size/4, 3*size/4), (3*size/4, size/4), (size/2, size/2)],
            6: [(size/4, size/4), (3*size/4, 3*size/4), (size/4, 3*size/4), (3*size/4, size/4), (size/4, size/2), (3*size/4, size/2)]
        }

        # Dibujar los puntos
        for x, y in dot_positions[value]:
            self.dice_canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius,
                                         fill="#e74c3c", outline="#c0392b", width=2, tags="dice_dot")

    def start_roll_animation(self):
        if self.is_rolling: # Evitar múltiples lanzamientos
            return

        self.is_rolling = True
        self.roll_button.config(state=tk.DISABLED) # Deshabilitar botón durante el lanzamiento
        self.n_roll_button.config(state=tk.DISABLED) # Deshabilitar el botón de N lanzamientos también
        self.animate_roll(0)

    def animate_roll(self, current_frame):
        # Número de "frames" de la animación y duración
        num_frames = 15
        delay_ms = 70 # Milisegundos entre cada cambio de cara

        if current_frame < num_frames:
            # Muestra una cara aleatoria rápidamente
            self.draw_dice(random.randint(1, 6))
            self.roll_value_label.config(text="Rodando...")
            self.root.after(delay_ms, self.animate_roll, current_frame + 1)
        else:
            # Al final de la animación, realiza el lanzamiento real
            self.current_roll_value = random.randint(1, 6)
            self.rolls.append(self.current_roll_value)
            self.draw_dice(self.current_roll_value)
            self.roll_value_label.config(text=f"Último lanzamiento: {self.current_roll_value}")
            self.update_simulation_data()
            self.is_rolling = False
            self.roll_button.config(state=tk.NORMAL) # Habilitar botón de nuevo
            self.n_roll_button.config(state=tk.NORMAL) # Habilitar el botón de N lanzamientos también

    def simulate_n_rolls(self):
        if self.is_rolling:
            return

        try:
            n = int(self.n_entry.get())
            if n <= 0:
                messagebox.showerror("Entrada Inválida", "Por favor, ingresa un número positivo para N.")
                return
            if n > 1000000: # Límite para evitar cuelgues con números muy grandes
                messagebox.showwarning("Número muy grande", "Un valor de N tan grande puede tardar mucho o congelar la aplicación. Se recomienda un máximo de 1,000,000.")
                return

            self.is_rolling = True
            self.roll_button.config(state=tk.DISABLED)
            self.n_roll_button.config(state=tk.DISABLED)
            self.roll_value_label.config(text=f"Simulando {n} lanzamientos...")
            self.draw_dice(1) # Mostrar una cara estática durante la simulación masiva

            # Realizar N lanzamientos sin animación visual por cada uno
            for _ in range(n):
                self.rolls.append(random.randint(1, 6))

            self.update_simulation_data()
            self.roll_value_label.config(text=f"Simulación de {n} lanzamientos terminada.")
            self.is_rolling = False
            self.roll_button.config(state=tk.NORMAL)
            self.n_roll_button.config(state=tk.NORMAL)

        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, ingresa un número entero válido para N.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")


    def update_simulation_data(self):
        total_rolls = len(self.rolls)
        self.total_rolls_label.config(text=f"Total de lanzamientos: {total_rolls}")

        # Calcular frecuencias
        frequencies = Counter(self.rolls)
        freq_text = "Frecuencia de cada cara:\n"
        for i in range(1, 7):
            freq_text += f"  Cara {i}: {frequencies[i]} veces\n"
        self.frequency_label.config(text=freq_text)

        # Calcular frecuencias relativas (probabilidad empírica)
        relative_freq_text = "Frecuencia relativa (Probabilidad empírica):\n"
        if total_rolls > 0:
            for i in range(1, 7):
                prob = (frequencies[i] / total_rolls) * 100 if total_rolls > 0 else 0
                relative_freq_text += f"  Cara {i}: {prob:.2f}%\n"
        else:
            for i in range(1, 7):
                relative_freq_text += f"  Cara {i}: 0.00%\n"
        self.relative_frequency_label.config(text=relative_freq_text)

    def reset_simulation(self):
        confirm = messagebox.askyesno("Reiniciar Simulación", "¿Estás seguro de que quieres reiniciar la simulación? Se borrarán todos los datos.")
        if confirm:
            self.rolls = []
            self.current_roll_value = 1
            self.draw_dice(self.current_roll_value)
            self.roll_value_label.config(text="Último lanzamiento: -")
            self.update_simulation_data()
            messagebox.showinfo("Simulación Reiniciada", "La simulación ha sido reiniciada con éxito.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceSimulator(root)
    root.mainloop()
