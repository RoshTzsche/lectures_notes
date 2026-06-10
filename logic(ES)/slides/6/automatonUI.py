import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from matplotlib.widgets import Button

# ==============================================================================
# MOTOR DEL AUTÓMATA CELULAR ELEMENTAL (REGLA 30) - EVALUACIÓN MATEMÁTICA
# ==============================================================================

class AutomataInteractivo:
    def __init__(self, pasos_tiempo=50, ancho_espacio=51):
        # Dimensiones del tensor espacio-temporal (T x N)
        self.pasos_tiempo = pasos_tiempo
        self.ancho_espacio = ancho_espacio
        
        # Inicialización de la matriz de estados en el subespacio nulo
        self.matriz_estados = np.zeros((self.pasos_tiempo, self.ancho_espacio), dtype=int)
        
        # Variables de control de la Máquina de Estados Finitos (FSM)
        self.evaluacion_activa = False
        self.limite_alcanzado = False
        self.anim = None
        self.t_actual = 1
        
        self._configurar_interfaz()

    def _configurar_interfaz(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        plt.subplots_adjust(bottom=0.2, top=0.85)
        
        self.titulo = self.ax.set_title(
            "Definición del Vector de Estado Inicial (C^0)\n"
            "Asigne valores en Z_2 a los elementos de la fila t=0.", 
            fontsize=12, color='white', pad=25
        )
        
        # Telemetría de la Norma L1
        self.texto_telemetria = self.ax.text(
            0.5, 1.02, 
            "Iteración (t): 0  |  Norma L1 (Peso de Hamming): 0", 
            transform=self.ax.transAxes, 
            ha='center', color='#11CAA0', 
            fontsize=12, fontfamily='monospace', weight='bold'
        )
        
        # Mapeo de Z_2 a representación visual (0 -> #333333, 1 -> white)
        cmap_personalizado = mcolors.ListedColormap(['#333333', 'white'])
        
        self.matriz_visual = self.ax.imshow(
            self.matriz_estados, 
            cmap=cmap_personalizado, 
            interpolation='nearest', 
            aspect='auto',
            vmin=0, vmax=1
        )
        
        # Geometría de la cuadrícula
        self.ax.set_xticks(np.arange(-.5, self.ancho_espacio, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.pasos_tiempo, 1), minor=True)
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=1.5)
        
        self.ax.tick_params(which='minor', size=0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for espina in self.ax.spines.values():
            espina.set_color('black')
        
        # Asignación de callbacks
        self.fig.canvas.mpl_connect('button_press_event', self._modificar_vector_inicial)
        
        ejes_boton = plt.axes([0.4, 0.05, 0.2, 0.075])
        self.boton_control = Button(
            ejes_boton, 'Iniciar Evaluación de $\Phi$', color='#1a1a1a', hovercolor='#555555'
        )
        self.boton_control.label.set_color('white')
        self.boton_control.on_clicked(self._gestionar_boton)
        
        plt.show()

    def _modificar_vector_inicial(self, event):
        # Bloqueo de mutabilidad si la matriz está siendo procesada
        if self.evaluacion_activa or self.limite_alcanzado or event.inaxes != self.ax:
            return
            
        if event.xdata is not None:
            columna_x = int(round(event.xdata))
            
            # Restricción de dominio: Modificación exclusiva del vector C^0
            if 0 <= columna_x < self.ancho_espacio:
                # Modulo 2 de adición lógica
                self.matriz_estados[0, columna_x] = 1 - self.matriz_estados[0, columna_x]
                self.matriz_visual.set_data(self.matriz_estados)
                
                # Actualización de la Norma L1 para el vector inicial
                norma_l1 = np.sum(self.matriz_estados[0])
                self.texto_telemetria.set_text(f"Iteración (t): 0  |  Norma L1 (Peso de Hamming): {norma_l1}")
                
                self.fig.canvas.draw_idle()

    def _gestionar_boton(self, event):
        # Enrutador de estados
        if self.limite_alcanzado:
            self._restablecer_matriz()
        elif not self.evaluacion_activa:
            self._iniciar_evaluacion()

    def _iniciar_evaluacion(self):
        self.evaluacion_activa = True
        self.titulo.set_text("Integración Numérica en Progreso...")
        self.titulo.set_color('#11CAA0')
        
        self.boton_control.color = 'black'
        self.boton_control.label.set_text('Calculando Tensor...')
        self.boton_control.label.set_color('gray')
        
        self.anim = animation.FuncAnimation(
            self.fig, 
            self._aplicar_transicion_global, 
            frames=self.pasos_tiempo - 1, 
            interval=50, 
            blit=True, 
            repeat=False
        )
        self.fig.canvas.draw_idle()

    def _aplicar_transicion_global(self, frame):
        # Criterio de parada: Límite del dominio temporal t_max alcanzado
        if self.t_actual >= self.pasos_tiempo:
            self.evaluacion_activa = False
            self.limite_alcanzado = True
            
            self.anim.event_source.stop()
            
            self.titulo.set_text(f"Condición de Frontera Temporal Alcanzada (t = {self.pasos_tiempo}).")
            self.titulo.set_color('#FF4444')
            
            # Habilitar el botón para la operación de reinicio
            self.boton_control.color = '#1a1a1a'
            self.boton_control.label.set_color('white')
            self.boton_control.label.set_text('Restablecer Matriz (Mapeo Nulo)')
            
            self.fig.canvas.draw_idle()
            return [self.matriz_visual, self.texto_telemetria]
            
        vector_anterior = self.matriz_estados[self.t_actual - 1]
        vector_nuevo = np.zeros(self.ancho_espacio, dtype=int)
        
        # Subconjuntos del dominio espacial para la regla local
        p = vector_anterior[0:-2]
        q = vector_anterior[1:-1]
        r = vector_anterior[2:]
        
        # Función booleana escalar aplicada al tensor: p XOR (q OR r)
        vector_nuevo[1:-1] = p ^ (q | r)
        
        self.matriz_estados[self.t_actual] = vector_nuevo
        self.matriz_visual.set_data(self.matriz_estados)
        
        norma_l1 = np.sum(vector_nuevo)
        self.texto_telemetria.set_text(f"Iteración (t): {self.t_actual}  |  Norma L1 (Peso de Hamming): {norma_l1}")
        
        self.t_actual += 1
        return [self.matriz_visual, self.texto_telemetria]

    def _restablecer_matriz(self):
        # Asignación del tensor nulo y restablecimiento de variables del sistema
        self.matriz_estados.fill(0)
        self.t_actual = 1
        self.limite_alcanzado = False
        
        # Restauración de la interfaz gráfica a condiciones iniciales
        self.matriz_visual.set_data(self.matriz_estados)
        self.titulo.set_text(
            "Definición del Vector de Estado Inicial (C^0)\n"
            "Asigne valores en Z_2 a los elementos de la fila t=0."
        )
        self.titulo.set_color('white')
        self.texto_telemetria.set_text("Iteración (t): 0  |  Norma L1 (Peso de Hamming): 0")
        
        self.boton_control.label.set_text('Iniciar Evaluación de $\Phi$')
        
        # Renderizado estático
        self.fig.canvas.draw_idle()

# ==============================================================================
# EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    simulacion = AutomataInteractivo()
