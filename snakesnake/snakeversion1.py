import pygame  # Pygame será la librería que nos ayudará a hacer el videojuego
import random  # Random es una librería que literalmente da valores aleatorios

# Definición de clases que vamos a usar
class Serpiente:  # Clase serpiente definirá todo lo que tenga que ver con la serpiente, sus atributos y sus movimientos
    def __init__(self):
        self.tamaño = 3  # Número de segmentos con los que empieza la serpiente
        self.posiciones = [((600 // 2), (600 // 2))]  # La serpiente empieza en el centro del tablero
        self.direccion = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Dirección inicial de la serpiente
        self.color = (0, 255, 0)  # Color verde de la serpiente
        self.puntuacion = 0  # Puntuación inicial del jugador

    def obtener_posicion_cabeza(self):
        # Retorna la posición de la cabeza de la serpiente
        return self.posiciones[0]

    def girar(self, punto):
        # Cambia la dirección de la serpiente
        # Evita que la serpiente se mueva hacia la dirección opuesta si tiene más de un segmento
        if self.tamaño > 1 and (punto[0] * -1, punto[1] * -1) == self.direccion:
            return
        else:
            self.direccion = punto

    def mover(self):
        # Mueve la serpiente en la dirección actual
        actual = self.obtener_posicion_cabeza()
        x, y = self.direccion
        nuevo = (((actual[0] + (x * 20)) % 600), (actual[1] + (y * 20)) % 600)
        if len(self.posiciones) > 2 and nuevo in self.posiciones[2:]:
            # Si la serpiente se muerde a sí misma, reinicia el juego
            self.reiniciar()
        else:
            # Inserta la nueva posición de la cabeza de la serpiente
            self.posiciones.insert(0, nuevo)
            # Elimina el último segmento si la serpiente no ha crecido
            if len(self.posiciones) > self.tamaño:
                self.posiciones.pop()

    def reiniciar(self):
        # Reinicia la serpiente a su estado inicial
        self.tamaño = 3
        self.posiciones = [((600 // 2), (600 // 2))]
        self.direccion = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Nueva dirección aleatoria
        self.puntuacion = 0

    def aumentar(self):
        # Aumenta el tamaño de la serpiente y la puntuación
        self.tamaño += 1
        self.puntuacion += 1

    def dibujar(self, superficie):
        # Dibuja la serpiente en la superficie proporcionada
        for p in self.posiciones:
            rect = pygame.Rect((p[0], p[1]), (20, 20))
            pygame.draw.rect(superficie, self.color, rect)
            pygame.draw.rect(superficie, (0, 0, 0), rect, 1)

    def manejar_teclas(self):
        # Maneja los eventos del teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.girar((0, -1))
                elif evento.key == pygame.K_DOWN:
                    self.girar((0, 1))
                elif evento.key == pygame.K_LEFT:
                    self.girar((-1, 0))
                elif evento.key == pygame.K_RIGHT:
                    self.girar((1, 0))


class Fruta:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        # Establecer la posición inicial de la fruta
        self.posicion = (random.randint(0, ancho - 20) // 20 * 20, random.randint(0, alto - 20) // 20 * 20)
        self.color = (255, 0, 0)  # Color rojo de la fruta

    def dibujar(self, superficie):
        # Dibuja la fruta en la superficie proporcionada
        rect = pygame.Rect(self.posicion, (20, 20))
        pygame.draw.rect(superficie, self.color, rect)

    def nueva_posicion(self):
        # Genera una nueva posición aleatoria para la fruta
        self.posicion = (random.randint(0, self.ancho - 20) // 20 * 20, random.randint(0, self.alto - 20) // 20 * 20)


class Tablero:
    def __init__(self, ANCHO=600, ALTO=600):
        self.ANCHO = ANCHO
        self.ALTO = ALTO
        self.CORRIENDO = True
        self.serpiente = Serpiente()
        self.fruta = Fruta(ANCHO, ALTO)  # Añadir una fruta al tablero


class Juego(Tablero):
    def __init__(self, ANCHO=600, ALTO=600):
        super().__init__(ANCHO, ALTO)

    def iniciar_juego(self):
        pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))  # Despliega la pantalla del juego
        reloj = pygame.time.Clock()  # Control del tiempo
        icon = pygame.image.load('snake.png')
        pygame.display.set_caption('Serpiente')
        pygame.display.set_icon(icon)
        while self.CORRIENDO:  # Mantiene la pantalla abierta
            self.serpiente.manejar_teclas()  # Maneja las teclas presionadas
            self.serpiente.mover()  # Mueve la serpiente
            if self.serpiente.obtener_posicion_cabeza() == self.fruta.posicion:
                # Si la serpiente toca la fruta, aumenta su tamaño y genera una nueva posición para la fruta
                self.serpiente.aumentar()
                self.fruta.nueva_posicion()
            pantalla.fill((0, 0, 0))  # Llenar la pantalla con negro
            self.serpiente.dibujar(pantalla)  # Dibuja la serpiente
            self.fruta.dibujar(pantalla)  # Dibuja la fruta
            pygame.display.update()  # Actualizar la pantalla
            reloj.tick(10)  # Configurar la velocidad de los fotogramas a 10 FPS


# Clase que ejecutará todo el juego
class Principal:
    def __init__(self):
        self.juego = Juego()
        self.juego.iniciar_juego()


# Inicialización del juego
if __name__ == "__main__":
    pygame.init()  # Inicialización de Pygame
    Principal()
    pygame.quit()  # Salir de Pygame
