import random
from functools import wraps
import time
import text_reader


class Arana():

    def __init__(self, nombre:str='default', estado:int=0, vida:float=100,
                 descripcion:str='Araña que ataca a los jugadores de forma aleatoria. Si la desproteges y luego la derribas, morirá al momento'):
        self.nombre = nombre
        self.estado = estado
        self.vida = vida
        self.descripcion = descripcion

    def attack(self, targets) -> None:
        text_reader.TextReader.printColor('RED', ' [!] ' + self.nombre + ' está atacando con sus colmillos ')
        random.choice(targets).recibirDano(10)

    def get_hit(self, dano:float) -> None:
        if self.estado == 0:
            self.vida -= dano
        elif self.estado == 1:
            self.vida -= dano * 2

    def aplicarDesproteccion(self) -> None:
        if self.estado == 0:
            self.estado = 1

    def aplicarDerribar(self) -> None:
        self.vida = 0

    def estadoActual(self) -> str:
        if self.estado == 0:
            return '[SE PUEDE DESPROTEGER]'
        elif self.estado == 1:
            return '[DESPROTEGIDA]'
        elif self.estado == 2:
            return '[DERRIBADA]'
        return ''


class Conejo():

    def __init__(self, nombre:str='default', suertudo:bool=True, vida:float=7,
                 descripcion:str='Conejo que puede atacar varias veces y que solo recibirá 1 de daño mientras tenga el estado suertudo, que se le quita aplicándole ATURDIR'):
        self.nombre = nombre
        self.suertudo = suertudo
        self.vida = vida
        self.descripcion = descripcion

    def attack(self, targets) -> None:
        text_reader.TextReader.printColor('RED', ' [!] ' + self.nombre + ' está lanzando patadas voladoras ')
        for target in targets:
            do_several_times(target.recibirDano, random.randint(1, 2))(7)

    def get_hit(self, dano:float) -> None:
        if self.suertudo:

            self.vida -= 1
        else:
            self.vida -= dano

    def aplicarAturdir(self) -> None:
        self.suertudo = False

    def estadoActual(self) -> str:
        if self.suertudo:
            return '[SUERTUDO]'
        return ''


class Dragon:

    def __init__(self, nombre:str='default', vida:float=500,
                 descripcion:str='Dragón que ataca a un solo objetivo y que podrá quemar, además de tener la habilidad de cambiar a dragón feérico'):
        self.nombre = nombre
        self.vida = vida
        self.descripcion = descripcion

    def attack(self, targets) -> None:
        text_reader.TextReader.printColor('RED', ' [!] ' + self.nombre + ' está lanzando su aliento de fuego ')
        target = random.choice(targets)
        burn(target.recibirDano, random.getrandbits(1), target)(15)

    def morph(self) -> None:
        text_reader.TextReader.printColor('RED',
                                          ' [!] ' + self.nombre + ' se ha transformado en un dragón feérico y se ha curado 200 de vida ')
        self.__class__ = Fae
        self.vida += 200

    def get_hit(self, dano:float) -> None:
        self.vida -= dano / 1.5


class Fae:
    def __init__(self, nombre:str='default', vida:float=500,
                 descripcion:str='Dragón feérico que podrá curar a los enemigos y cambiar a dragón de fuego'):
        self.nombre = nombre
        self.vida = vida
        self.descripcion = descripcion

    def heal(self, targets) -> None:
        text_reader.TextReader.printColor('PINK',
                                          ' [!] ' + self.nombre + ' está curando a todos los enemigos ')
        for target in targets:
            text_reader.TextReader.printColor('YELLOW',
                                              ' [!] ' + target.nombre + ' se ha curado 200 de vida')
            target.vida += 200

    def morph(self) -> None:
        text_reader.TextReader.printColor('RED', ' [!] ' + self.nombre + ' se ha transformado en un dragón de fuego ')
        self.__class__ = Dragon

    def get_hit(self, dano:float) -> None:
        self.vida -= dano / 2


class Fantasma:

    def __init__(self, nombre:str='default', vida:float=40, descripcion:str='Enemigo que solamente aplica coma a un jugador'):
        self.nombre = nombre
        self.vida = vida
        self.descripcion = descripcion

    def attack(self, targets) -> None:
        target = random.choice(targets)
        text_reader.TextReader.printColor('RED', ' [!] ' + self.nombre + ' está invocando pesadillas ')
        debuff_defensa(target.aplicar_coma, 5, target)()

    def get_hit(self, dano:float) -> None:
        self.vida -= dano


class Robot:

    def __init__(self, nombre:str='default', estado:int=0, vida:float=1000,
                 descripcion:str='Robot que puede debuffar la defensa de los jugadores, además de añadir una cantidad extra de daño y curarse a él mismo'):
        self.nombre = nombre
        self.estado = estado
        self.vida = vida
        self.descripcion = descripcion
        self.dano_ataque = 100

    def attack(self, targets) -> None:
        target = random.choice(targets)
        text_reader.TextReader.printColor('RED',
                                          ' [!] ' + self.nombre + ' tiene a ' + target.nombre + ' en el punto de mira')
        target.recibirDano(200)
        text_reader.TextReader.printColor('RED',
                                          ' [!] ' + self.nombre + ' está lanzando una explosión de chispas ')
        for target in targets:
            reduction = random.randint(5, 10)
            text_reader.TextReader.printColor('YELLOW',
                                              ' [!] ' + self.nombre + ' ha reducido la defensa de ' + target.nombre + ' en ' + str(
                                                  reduction))
            debuff_defensa(deal_extra_damage(target.recibirDano, self.dano_ataque / 2, target), reduction, target)(
                self.dano_ataque / 4)

    def heal(self, targets) -> None:
        text_reader.TextReader.printColor('PINK',
                                          ' [!] ' + self.nombre + ' se repara las piezas curándose ' + str(
                                              120) + ' de vida')
        self.vida += 120

    def get_hit(self, dano:float) -> None:
        if self.estado == 0:
            self.vida -= dano
        elif self.estado >= 2:
            self.vida -= dano * 3

    def aplicarDesproteccion(self) -> None:
        if self.estado == 0:
            self.estado = 1
            text_reader.TextReader.printColor('BLUE',
                                              ' [!] Se ha reducido el daño de ' + self.nombre)
            self.dano_ataque = 50

    def aplicarDerribar(self) -> None:
        if self.estado == 1:
            self.estado = 2

    def aplicarAturdir(self) -> None:
        if self.estado == 2:
            self.estado = 0
            text_reader.TextReader.printColor('CYAN',
                                              '  [!] ' + self.nombre + ' ha recibido un total de ' + str(
                                                  self.vida / 2) + ' de daño por el combo desprotección-derribar-aturdir completo')
            self.vida -= self.vida / 2
            text_reader.TextReader.printColor('PINK',
                                              '  [!] ' + self.nombre + ' vuelve a estar en perfecto estado y atacando a toda potencia')
            self.dano_ataque = 100

    def estadoActual(self) -> str:
        if self.estado == 0:
            return '[SE PUEDE DESPROTEGER]'
        elif self.estado == 1:
            return '[DESPROTEGIDO]'
        elif self.estado == 2:
            return '[DERRIBADO]'
        elif self.estado == 3:
            return '[ATURDIDO]'
        return ''


def do_several_times(func, times):
    @wraps(func)
    def my_wrapper(*args, **kwarfs):
        for i in range(times + 1):
            result = func(*args, **kwarfs)
        return result

    return my_wrapper


def burn(func, will_burn, target):
    @wraps(func)
    def my_wrapper(*args, **kwarfs):
        result = func(*args, **kwarfs)
        if (will_burn):
            target.quemar()
        return result

    return my_wrapper


def apply_coma(func, will_coma, target):
    @wraps(func)
    def my_wrapper(*args, **kwarfs):
        result = func(*args, **kwarfs)
        if (will_coma):
            target.coma()
        return result

    return my_wrapper


def deal_extra_damage(func, damage_dealt, target):
    @wraps(func)
    def my_wrapper(*args, **kwarfs):
        result = func(*args, **kwarfs)
        target.reducirVida(damage_dealt)
        return result

    return my_wrapper


def debuff_defensa(func, reduccion, target):
    @wraps(func)
    def my_wrapper(*args, **kwarfs):
        target.buffarDefensa(-reduccion)
        result = func(*args, **kwarfs)
        return result

    return my_wrapper
