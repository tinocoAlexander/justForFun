import pygame  # Pygame será la librería que nos ayudará a hacer el videojuego
import random  # Random es una librería que literalmente da valores aleatorios
import time

class Serpiente:  # Clase serpiente definirá todo lo que tenga que ver con la serpiente, sus atributos y sus movimientos
    def __init__(self, color=(0, 255, 0)):
        # Inicializa la serpiente con un tamaño inicial, posición, dirección, color y puntuación
        self.tamaño = 3  # Número de segmentos con los que empieza la serpiente
        self.posiciones = [((600 // 2), (600 // 2))]  # La serpiente empieza en el centro del tablero
        self.direccion = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Dirección inicial de la serpiente
        self.color = color  # Color de la serpiente
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
            return False
        else:
            # Inserta la nueva posición de la cabeza de la serpiente
            self.posiciones.insert(0, nuevo)
            # Elimina el último segmento si la serpiente no ha crecido
            if len(self.posiciones) > self.tamaño:
                self.posiciones.pop()
            return True

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
        # Inicializa la fruta con una posición aleatoria y un color
        self.ancho = ancho
        self.alto = alto
        self.posicion = (random.randint(0, ancho - 20) // 20 * 20, random.randint(0, alto - 20) // 20 * 20)
        self.color = (255, 0, 0)  # Color rojo de la fruta

    def dibujar(self, superficie):
        # Dibuja la fruta en la superficie proporcionada
        rect = pygame.Rect(self.posicion, (20, 20))
        pygame.draw.rect(superficie, self.color, rect)

    def nueva_posicion(self):
        # Genera una nueva posición aleatoria para la fruta
        self.posicion = (random.randint(0, self.ancho - 20) // 20 * 20, random.randint(0, self.alto - 20) // 20 * 20)

class Obstaculo:
    def __init__(self, ancho, alto):
        # Inicializa el obstáculo con una posición aleatoria y un color
        self.ancho = ancho
        self.alto = alto
        self.posicion = (random.randint(0, ancho - 20) // 20 * 20, random.randint(0, alto - 20) // 20 * 20)
        self.color = (255, 255, 0)  # Color amarillo del obstáculo

    def dibujar(self, superficie):
        # Dibuja el obstáculo en la superficie proporcionada
        rect = pygame.Rect(self.posicion, (20, 20))
        pygame.draw.rect(superficie, self.color, rect)

    def nueva_posicion(self):
        # Genera una nueva posición aleatoria para el obstáculo
        self.posicion = (random.randint(0, self.ancho - 20) // 20 * 20, random.randint(0, self.alto - 20) // 20 * 20)

class Tablero:
    def __init__(self, ANCHO=600, ALTO=600, color=(0, 255, 0)):
        # Inicializa el tablero con dimensiones específicas y crea una serpiente, fruta y obstáculo
        self.ANCHO = ANCHO
        self.ALTO = ALTO
        self.CORRIENDO = True
        self.serpiente = Serpiente(color)
        self.fruta = Fruta(ANCHO, ALTO)
        self.obstaculo = Obstaculo(ANCHO, ALTO)
        self.tiempo_obstaculo = 0

    def manejar_obstaculos(self):
        # Mueve el obstáculo cada 3 segundos si la puntuación es mayor o igual a 10
        if self.serpiente.puntuacion >= 10:
            tiempo_actual = time.time()
            if tiempo_actual - self.tiempo_obstaculo > 3:
                self.obstaculo.nueva_posicion()
                self.tiempo_obstaculo = tiempo_actual

class Juego(Tablero):
    def __init__(self, ANCHO=600, ALTO=600, color=(0, 255, 0)):
        # Inicializa el juego con dimensiones específicas y una fuente para la puntuación
        super().__init__(ANCHO, ALTO, color)
        self.fuente = pygame.font.SysFont('Arial', 25)

    def iniciar_juego(self):
        # Inicia el bucle principal del juego
        pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        reloj = pygame.time.Clock()
        icon = pygame.image.load('snake.png')
        pygame.display.set_caption('Snake')
        pygame.display.set_icon(icon)
        velocidad = 10

        while self.CORRIENDO:
            self.serpiente.manejar_teclas()
            if not self.serpiente.mover():
                self.game_over(pantalla)
                return
            if self.serpiente.obtener_posicion_cabeza() == self.fruta.posicion:
                self.serpiente.aumentar()
                self.fruta.nueva_posicion()
                velocidad += 0.25

            if self.serpiente.obtener_posicion_cabeza() == self.obstaculo.posicion:
                self.game_over(pantalla)
                return

            self.manejar_obstaculos()

            pantalla.fill((0, 0, 0))
            self.serpiente.dibujar(pantalla)
            self.fruta.dibujar(pantalla)
            if self.serpiente.puntuacion >= 10:
                self.obstaculo.dibujar(pantalla)
            self.mostrar_puntuacion(pantalla)
            pygame.display.update()
            reloj.tick(velocidad)

    def mostrar_puntuacion(self, pantalla):
        # Muestra la puntuación en la pantalla
        puntuacion_texto = self.fuente.render(f'Puntuación: {self.serpiente.puntuacion}', True, (255, 255, 255))
        pantalla.blit(puntuacion_texto, (10, 10))

    def game_over(self, pantalla):
        # Muestra el mensaje de Game Over y opciones para reiniciar o volver al menú
        fuente_game_over = pygame.font.SysFont('Arial', 50)
        texto_game_over = fuente_game_over.render('Game Over', True, (255, 0, 0))
        pantalla.blit(texto_game_over, (self.ANCHO // 2 - texto_game_over.get_width() // 2, self.ALTO // 3))

        boton_si = pygame.Rect(self.ANCHO // 2 - 100, self.ALTO // 2, 80, 50)
        boton_no = pygame.Rect(self.ANCHO // 2 + 20, self.ALTO // 2, 80, 50)
        
        pygame.draw.rect(pantalla, (0, 255, 0), boton_si)
        pygame.draw.rect(pantalla, (255, 0, 0), boton_no)

        fuente_boton = pygame.font.SysFont('Arial', 30)
        texto_si = fuente_boton.render('Sí', True, (0, 0, 0))
        texto_no = fuente_boton.render('No', True, (0, 0, 0))
        pantalla.blit(texto_si, (boton_si.x + (boton_si.width - texto_si.get_width()) // 2, boton_si.y + (boton_si.height - texto_si.get_height()) // 2))
        pantalla.blit(texto_no, (boton_no.x + (boton_no.width - texto_no.get_width()) // 2, boton_no.y + (boton_no.height - texto_no.get_height()) // 2))

        pygame.display.update()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if boton_si.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        esperando = False
                    elif boton_no.collidepoint(mouse_pos):
                        self.CORRIENDO = False
                        esperando = False

    def reiniciar_juego(self):
        self.serpiente.reiniciar()
        self.CORRIENDO = True
        self.iniciar_juego()

class Menu:
    def __init__(self, ancho, alto):
        # Inicializa el menú con dimensiones específicas y otros parámetros necesarios
        self.ANCHO = ancho
        self.ALTO = alto
        self.CORRIENDO = True
        self.fuente_titulo = pygame.font.SysFont('Arial', 50)
        self.fuente_boton = pygame.font.SysFont('Arial', 30)
        self.juego_iniciado = False
        self.customizar = False
        self.serpiente_color = (0, 255, 0)
        self.colores = [(0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)]
        self.color_index = 0
        self.colores_nombre = ["Verde", "Rojo", "Amarillo", "Azul"]
        self.icon = pygame.image.load('snake.png')  # Cargar el ícono una vez

    def dibujar_texto(self, superficie, texto, fuente, color, centro):
        # Dibuja texto en la superficie proporcionada
        texto_superficie = fuente.render(texto, True, color)
        texto_rect = texto_superficie.get_rect(center=centro)
        superficie.blit(texto_superficie, texto_rect)

    def dibujar_boton(self, superficie, texto, color, rect):
        # Dibuja un botón con texto en la superficie proporcionada
        pygame.draw.rect(superficie, color, rect)
        self.dibujar_texto(superficie, texto, self.fuente_boton, (0, 0, 0), rect.center)

    def manejar_eventos(self):
        # Maneja los eventos del menú principal
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.boton_jugar.collidepoint(mouse_pos):
                    self.juego_iniciado = True
                elif self.boton_customizar.collidepoint(mouse_pos):
                    self.customizar = True
                elif self.customizar:
                    if self.boton_izquierda.collidepoint(mouse_pos):
                        self.color_index = (self.color_index - 1) % len(self.colores)
                        self.serpiente_color = self.colores[self.color_index]
                    elif self.boton_derecha.collidepoint(mouse_pos):
                        self.color_index = (self.color_index + 1) % len(self.colores)
                        self.serpiente_color = self.colores[self.color_index]
                    elif self.boton_guardar.collidepoint(mouse_pos):
                        self.customizar = False
                    elif self.boton_volver.collidepoint(mouse_pos):
                        self.customizar = False

    def mostrar_menu(self):
        # Muestra el menú principal
        pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption('Menú Principal')
        pygame.display.set_icon(self.icon)

        while self.CORRIENDO:
            self.manejar_eventos()
            if self.juego_iniciado:
                juego = Juego(color=self.serpiente_color)
                juego.iniciar_juego()
                self.CORRIENDO = False
            elif self.customizar:
                self.mostrar_personalizar(pantalla)
            else:
                pantalla.fill((0, 0, 0))
                self.dibujar_texto(pantalla, 'Snake', self.fuente_titulo, (0, 255, 0), (self.ANCHO // 2, self.ALTO // 3))
                self.boton_jugar = pygame.Rect(self.ANCHO // 2 - 100, self.ALTO // 2 - 50, 200, 50)
                self.boton_customizar = pygame.Rect(self.ANCHO // 2 - 100, self.ALTO // 2 + 50, 200, 50)

                self.dibujar_boton(pantalla, 'Jugar', (0, 255, 0), self.boton_jugar)
                self.dibujar_boton(pantalla, 'Personalizar', (0, 255, 0), self.boton_customizar)

            pygame.display.update()

    def mostrar_personalizar(self, pantalla):
        # Muestra la pantalla de personalización de la serpiente
        pantalla.fill((0, 0, 0))
        self.dibujar_texto(pantalla, 'Personalizar', self.fuente_titulo, (0, 255, 0), (self.ANCHO // 2, self.ALTO // 4))

        self.boton_izquierda = pygame.Rect(self.ANCHO // 2 - 150, self.ALTO // 2, 50, 50)
        self.boton_derecha = pygame.Rect(self.ANCHO // 2 + 100, self.ALTO // 2, 50, 50)
        self.boton_guardar = pygame.Rect(self.ANCHO // 2 - 100, self.ALTO // 2 + 150, 200, 50)
        self.boton_volver = pygame.Rect(self.ANCHO // 2 - 100, self.ALTO // 2 + 220, 200, 50)

        pygame.draw.polygon(pantalla, (255, 255, 255), [(self.boton_izquierda.left + 50, self.boton_izquierda.top), 
                                                        (self.boton_izquierda.left + 50, self.boton_izquierda.bottom), 
                                                        (self.boton_izquierda.left, self.boton_izquierda.centery)])
        pygame.draw.polygon(pantalla, (255, 255, 255), [(self.boton_derecha.left, self.boton_derecha.top), 
                                                        (self.boton_derecha.left, self.boton_derecha.bottom), 
                                                        (self.boton_derecha.right, self.boton_derecha.centery)])

        self.dibujar_texto(pantalla, self.colores_nombre[self.color_index], self.fuente_boton, (255, 255, 255), (self.ANCHO // 2, self.ALTO // 2 + 75))

        serpiente = Serpiente(self.serpiente_color)
        serpiente.dibujar(pantalla)

        self.dibujar_boton(pantalla, 'Guardar', (0, 255, 0), self.boton_guardar)
        self.dibujar_boton(pantalla, 'Volver', (255, 0, 0), self.boton_volver)

        pygame.display.update()


class Principal:
    def __init__(self):
        # Inicializa el menú principal
        self.menu = Menu(600, 600)
        self.menu.mostrar_menu()


if __name__ == "__main__":
    pygame.init()  # Inicialización de Pygame
    Principal()
    pygame.quit()  # Salir de Pygame
