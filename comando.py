import text_reader


class ComandoAtaque:

    def __init__(self, nombre='default', dano=0, area=False, desproteccion=False, derribar=False, aturdir=False,
                 descripcion=''):
        self.nombre = nombre
        self.dano = dano
        self.desproteccion = desproteccion
        self.derribar = derribar
        self.aturdir = aturdir
        self.area = area
        self.descripcion = descripcion

    def usar(self, user, jugadores, enemigos):
        if self.area:
            objetivos = enemigos
        else:
            if len(enemigos) == 1:
                objetivos = [enemigos[0]]
            else:
                number = 0
                print("Selecciona un objetivo: ")
                text_reader.TextReader.output_enemy_state(enemigos, selector=True)
                number = text_reader.TextReader.get_input_target('Escoge a un enemigo: ')
                objetivos = [enemigos[int(number)]]
        for target in objetivos:
            user.aplicarDano(target, self.dano)
            user.aplicarCambioDeEstado(target, self.desproteccion, self.derribar, self.aturdir)

    def to_string(self):
        to_str = text_reader.TextReader.colors['RED'] + '[ATQ] ' + self.nombre + text_reader.TextReader.colors[
            'END'] + ' / DMG: ' + str(self.dano)
        if (self.area):
            to_str += ' / ' + text_reader.TextReader.colors['UNDERLINE'] + 'DAÑO EN AREA' + \
                      text_reader.TextReader.colors['END']
        if self.desproteccion:
            to_str += text_reader.TextReader.colors['YELLOW'] + ' [DESPROTEGE] ' + text_reader.TextReader.colors['END']
        elif self.derribar:
            to_str += text_reader.TextReader.colors['YELLOW'] + ' [DERRIBA] ' + text_reader.TextReader.colors['END']
        elif self.aturdir:
            to_str += text_reader.TextReader.colors['YELLOW'] + ' [ATURDE] ' + text_reader.TextReader.colors['END']
        to_str += '\n       [?] ' + self.descripcion
        return to_str


class ComandoCura:

    def __init__(self, nombre='default', curacion=0, area=False, escudo=False, limpia_estados=False, buff_ataque=0,
                 buff_defensa=0, descripcion=''):
        self.nombre = nombre
        self.curacion = curacion
        self.escudo = escudo
        self.limpiaestados = limpia_estados
        self.buffoataque = buff_ataque
        self.buffodefensa = buff_defensa
        self.area = area
        self.descripcion = descripcion

    def usar(self, user, jugadores, enemigos):
        if self.area:
            objetivos = jugadores
        else:
            if len(jugadores) == 1:
                objetivos = [jugadores[0]]
            else:
                number = 0
                print("Selecciona un objetivo: ")
                text_reader.TextReader.player_state(jugadores, selector=True)
                number = text_reader.TextReader.get_input_target('Escoge a un jugador: ')
                objetivos = [jugadores[int(number)]]
        for target in objetivos:
            target.recibirCura(user.curacion_base + self.curacion)
            target.recibirEscudo(self.escudo)
            target.limpiarEstados(self.limpiaestados)
            target.buffarAtaque(self.buffoataque)
            target.buffarDefensa(self.buffodefensa)

    def to_string(self):
        to_str = text_reader.TextReader.colors['GREEN'] + '[SND] ' + self.nombre + text_reader.TextReader.colors['END']
        if self.curacion > 0:
            to_str += ' / CURA: ' + str(self.curacion)
        if self.escudo:
            to_str += text_reader.TextReader.colors['CYAN'] + ' [AÑADE ESCUDO]' + text_reader.TextReader.colors['END']
        if self.limpiaestados:
            to_str += text_reader.TextReader.colors['CYAN'] + ' [LIMPIA ESTADOS]' + text_reader.TextReader.colors['END']
        if self.buffoataque > 0:
            to_str += ' / AUMENTO DE DAÑO: ' + str(self.buffoataque)
        if self.buffodefensa > 0:
            to_str += ' / AUMENTO DE DEFENSA: ' + str(self.buffodefensa)
        if self.area:
            to_str += ' / ' + text_reader.TextReader.colors['UNDERLINE'] + 'APLICA EN ÁREA' + \
                      text_reader.TextReader.colors['END']

        to_str += '\n       [?] ' + self.descripcion
        return to_str


class ComandoTransformacion:

    def __init__(self, nombre='default', clase='', listo=False, descripcion = '', used=False):
        self.nombre = nombre
        self.clase = clase
        self.listo = listo
        self.descripcion = descripcion

    def usar(self, user, jugadores, enemigos):
        user.transformacion(self.clase)

    def to_string(self):
        to_str = text_reader.TextReader.colors['BLUE'] + '[TRANSFORMATION] ' + self.nombre + text_reader.TextReader.colors['END']
        to_str += '\n       [?] ' + self.descripcion
        return to_str
