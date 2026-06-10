import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from matplotlib.widgets import Button

# ==============================================================================
# MOTOR DEL AUTÓMATA CELULAR 2D (JUEGO DE LA VIDA) - TOPOLOGÍA TOROIDAL
# ==============================================================================

class AutomataBidimensional:
    def __init__(self, dimension_x=50, dimension_y=50, iteraciones_max=500):
        # Definición del espacio métrico finito
        self.dim_x = dimension_x
        self.dim_y = dimension_y
        self.iteraciones_max = iteraciones_max
        
        # Tensor de estado Z_2 inicializado en el subespacio nulo
        self.matriz_estados = np.zeros((self.dim_y, self.dim_x), dtype=int)
        
        # Máquina de Estados Finitos (FSM)
        self.evaluacion_activa = False
        self.limite_alcanzado = False
        self.anim = None
        self.t_actual = 0
        
        self._configurar_interfaz()

    def _configurar_interfaz(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        plt.subplots_adjust(bottom=0.15, top=0.88)
        
        self.titulo = self.ax.set_title(
            "Vector de Estado Inicial C^0 en Topología Toroidal Z^2\n"
            "Asigne la configuración topológica haciendo clic en el retículo.", 
            fontsize=12, color='white', pad=20
        )
        
        self.texto_telemetria = self.ax.text(
            0.5, 1.02, 
            "Iteración (t): 0  |  Norma L1 (Peso de Hamming): 0", 
            transform=self.ax.transAxes, 
            ha='center', color='#11CAA0', 
            fontsize=12, fontfamily='monospace', weight='bold'
        )
        
        # Mapeo: 0 -> #333333 (Vacío), 1 -> white (Materia)
        cmap_personalizado = mcolors.ListedColormap(['#333333', 'white'])
        
        self.matriz_visual = self.ax.imshow(
            self.matriz_estados, 
            cmap=cmap_personalizado, 
            interpolation='nearest', 
            vmin=0, vmax=1
        )
        
        # Geometría discreta para forzar la visibilidad del tensor
        self.ax.set_xticks(np.arange(-.5, self.dim_x, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.dim_y, 1), minor=True)
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=1.0)
        
        self.ax.tick_params(which='both', size=0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for espina in self.ax.spines.values():
            espina.set_color('black')
        
        self.fig.canvas.mpl_connect('button_press_event', self._modificar_tensor_inicial)
        
        ejes_boton = plt.axes([0.35, 0.04, 0.3, 0.05])
        self.boton_control = Button(
            ejes_boton, 'Iniciar Evaluación de $\Phi$', color='#1a1a1a', hovercolor='#555555'
        )
        self.boton_control.label.set_color('white')
        self.boton_control.on_clicked(self._gestionar_boton)
        
        plt.show()

    def _modificar_tensor_inicial(self, event):
        if self.evaluacion_activa or self.limite_alcanzado or event.inaxes != self.ax:
            return
            
        if event.xdata is not None and event.ydata is not None:
            col_x = int(round(event.xdata))
            fila_y = int(round(event.ydata))
            
            if 0 <= col_x < self.dim_x and 0 <= fila_y < self.dim_y:
                # Modulación escalar en Z_2
                self.matriz_estados[fila_y, col_x] = 1 - self.matriz_estados[fila_y, col_x]
                self.matriz_visual.set_data(self.matriz_estados)
                
                norma_l1 = np.sum(self.matriz_estados)
                self.texto_telemetria.set_text(f"Iteración (t): 0  |  Norma L1 (Peso de Hamming): {norma_l1}")
                
                self.fig.canvas.draw_idle()

    def _gestionar_boton(self, event):
        if self.limite_alcanzado:
            self._restablecer_tensor()
        elif not self.evaluacion_activa:
            self._iniciar_evaluacion()

    def _iniciar_evaluacion(self):
        self.evaluacion_activa = True
        self.titulo.set_text("Evolución Dinámica en Progreso (Mapeo de Conway)...")
        self.titulo.set_color('#11CAA0')
        
        self.boton_control.color = 'black'
        self.boton_control.label.set_text('Integrando Tensor...')
        self.boton_control.label.set_color('gray')
        
        self.anim = animation.FuncAnimation(
            self.fig, 
            self._aplicar_transicion_global, 
            frames=self.iteraciones_max, 
            interval=80, 
            blit=True, 
            repeat=False
        )
        self.fig.canvas.draw_idle()

    def _aplicar_transicion_global(self, frame):
        if self.t_actual >= self.iteraciones_max:
            self.evaluacion_activa = False
            self.limite_alcanzado = True
            
            self.anim.event_source.stop()
            self.titulo.set_text(f"Límite de Evaluación Alcanzado (t = {self.iteraciones_max}).")
            self.titulo.set_color('#FF4444')
            
            self.boton_control.color = '#1a1a1a'
            self.boton_control.label.set_color('white')
            self.boton_control.label.set_text('Restablecer Espacio (Mapeo Nulo)')
            
            self.fig.canvas.draw_idle()
            return [self.matriz_visual, self.texto_telemetria]
            
        C = self.matriz_estados
        
        # Evaluación simultánea del Vecindario de Moore mediante geometría toroidal (np.roll)
        V = (np.roll(C, 1, axis=0) + np.roll(C, -1, axis=0) +
             np.roll(C, 1, axis=1) + np.roll(C, -1, axis=1) +
             np.roll(np.roll(C, 1, axis=0), 1, axis=1) +
             np.roll(np.roll(C, 1, axis=0), -1, axis=1) +
             np.roll(np.roll(C, -1, axis=0), 1, axis=1) +
             np.roll(np.roll(C, -1, axis=0), -1, axis=1))
        
        # Resolución del operador booleano C^{t+1} = (V == 3) OR (C^t == 1 AND V == 2)
        nuevo_C = np.logical_or(V == 3, np.logical_and(C == 1, V == 2)).astype(int)
        
        self.matriz_estados = nuevo_C
        self.matriz_visual.set_data(self.matriz_estados)
        
        self.t_actual += 1
        norma_l1 = np.sum(self.matriz_estados)
        self.texto_telemetria.set_text(f"Iteración (t): {self.t_actual}  |  Norma L1 (Peso de Hamming): {norma_l1}")
        
        return [self.matriz_visual, self.texto_telemetria]

    def _restablecer_tensor(self):
        self.matriz_estados = np.zeros((self.dim_y, self.dim_x), dtype=int)
        self.t_actual = 0
        self.limite_alcanzado = False
        
        self.matriz_visual.set_data(self.matriz_estados)
        self.titulo.set_text(
            "Vector de Estado Inicial C^0 en Topología Toroidal Z^2\n"
            "Asigne la configuración topológica haciendo clic en el retículo."
        )
        self.titulo.set_color('white')
        self.texto_telemetria.set_text("Iteración (t): 0  |  Norma L1 (Peso de Hamming): 0")
        
        self.boton_control.label.set_text('Iniciar Evaluación de $\Phi$')
        self.fig.canvas.draw_idle()

# ==============================================================================
# EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    # Retículo de 50x50 para garantizar la resolución sin colapso de Nyquist
    simulacion = AutomataBidimensional(dimension_x=50, dimension_y=50, iteraciones_max=500)
