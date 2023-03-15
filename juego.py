import text_reader
import comando
import random
import time

class Juego:

    def __init__(self):
        self.numero_turno = 0

    def game_start(self):
        text_reader.TextReader.game_start()
        self.jugadores = text_reader.TextReader.create_players()
        self.enemigos = text_reader.TextReader.spawn_next_enemies()

    def turno(self):
        while True:
            self.numero_turno += 1
            text_reader.TextReader.printColor('BOLD', '-- TURNO: ' + str(self.numero_turno) + ' --')
            self.turnoJugadores()
            self.burn_health()
            self.turnoEnemy()


    def turnoJugadores(self):
        for jugador in self.jugadores:
            self.check_game()
            text_reader.TextReader.printBlack('Turno del jugador: ' + jugador.to_string())
            if not jugador.coma:
                numero_comando = 0
                for comando in jugador.lista_comandos:
                    try:
                        if self.numero_turno == 5 and not comando.listo:
                            comando.listo = True
                        is_comando_ready = comando.listo
                        if is_comando_ready and not jugador.transformado:
                            text_reader.TextReader.printBlack('     [' + str(numero_comando) + '] ' + comando.to_string())
                            numero_comando += 1
                    except AttributeError:
                        text_reader.TextReader.printBlack('     [' + str(numero_comando) + '] ' + comando.to_string())
                        numero_comando += 1
                numero = text_reader.TextReader.get_input_comando("Escoge un comando (número): ")
                comando = jugador.lista_comandos[int(numero)]
                comando.usar(jugador, self.jugadores, self.enemigos)
            else:
                text_reader.TextReader.printColor('YELLOW',
                                                  '   [!] El jugador no puede realizar ninguna acción porque está en coma')
            self.state_of_game()

    def turnoEnemy(self):
        dict_actions = { 'attack': 'self.jugadores', 'heal': 'self.enemigos', 'morph': ''}
        for enemigo in self.enemigos:
            self.check_game()
            text_reader.TextReader.printBlack('Turno del enemigo: ' + enemigo.nombre)
            command_name, command_parameters = random.choice(list(dict_actions.items()))
            try:
                exec('enemigo.' + command_name + '(' + command_parameters + ')')
            except AttributeError:
                text_reader.TextReader.printColor('BOLD',
                                                  '     [!] ' + enemigo.nombre + ' no ha realizado ninguna acción')
            self.state_of_game()

    def burn_health(self):
        for jugador in self.jugadores:
            if jugador.quemado:
                jugador.reducirVida(jugador.vida_maxima / 10, True)

    def state_of_game(self):
        print('\n')
        for jugador in self.jugadores:
            if jugador.vida <= 0:
                self.jugadores.remove(jugador)
                text_reader.TextReader.printColor('RED', '  [!!!!] ' + jugador.nombre + ' ha muerto ')
        if len(self.jugadores)==0:
            text_reader.TextReader.printColor('BOLD', '------------DERROTA: Han muerto todos los jugadores------------')
            exit()
        for enemigo in self.enemigos:
            if enemigo.vida <= 0:
                text_reader.TextReader.printColor('PINK', '     [!!] Has eliminado a ' + enemigo.nombre)
                self.enemigos.remove(enemigo)
        text_reader.TextReader.printColor('BOLD', '--ESTADO DE LOS JUGADORES--')
        text_reader.TextReader.player_state(self.jugadores)
        print('\n')
        text_reader.TextReader.printColor('BOLD', '--ESTADO DE LOS ENEMIGOS--')
        text_reader.TextReader.output_enemy_state(self.enemigos)
        print('\n')

    def check_game(self):
        if len(self.enemigos) == 0:
            self.enemigos = text_reader.TextReader.spawn_next_enemies()


if __name__ == '__main__':
    play = Juego()
    if text_reader.TextReader.auto:
        text_reader.TextReader.get_ejecucion_commands()
        text_reader.TextReader.get_ejecucion_targets()
    play.game_start()
    play.turno()
