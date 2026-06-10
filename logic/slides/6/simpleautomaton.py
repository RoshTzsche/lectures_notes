# ==============================================================================
# DEMOSTRACIÓN EN CLASE: Autómata Celular Elemental (Regla 30)
# Isomorfismo de Shannon aplicado a una topología espacial Z^1
# ==============================================================================

def ejecutar_automata_celular():
    # 1. Definición del Espacio (L) y Estado Inicial
    # Usamos un ancho impar para tener un centro exacto
    ancho_espacio = 61
    pasos_tiempo = 30
    
    # Configuración global en t=0 (estado base lleno de ceros)
    universo = [0] * ancho_espacio
    
    # Inyección de entropía mínima (Condición inicial: una sola celda viva en el centro)
    # Matemáticamente análogo a una función Delta de Kronecker
    universo[ancho_espacio // 2] = 1

    print("Evolución Temporal de la Regla 30:")
    print("-" * ancho_espacio)

   # 2. Función de Evolución Global (Phi)
    for t in range(pasos_tiempo):
        # A. Mapeo visual (Traducción de Sintaxis a Semántica visual para el alumno)
        representacion = "".join(["█" if celda == 1 else " " for celda in universo])
        print(representacion)

        # B. Preparar el espacio para t+1
        nuevo_universo = [0] * ancho_espacio

        # C. Aplicar la Regla Local (delta) iterando sobre el espacio
        # Ignoramos los bordes extremos (i=0 e i=ancho-1) por simplicidad de límites
        for i in range(1, ancho_espacio - 1):
            
            # Extraer el vecindario N = (-1, 0, 1)
            izq = universo[i - 1]
            centro = universo[i]
            der = universo[i + 1]
            
            # Implementación estricta de la Regla local delta: izq XOR (centro OR der)
            # Esta línea destruye el determinismo predecible a largo plazo
            nuevo_universo[i] = izq ^ (centro | der)

        # D. Actualizar el estado global
        universo = nuevo_universo

if __name__ == "__main__":
    ejecutar_automata_celular()
