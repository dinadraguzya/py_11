class DomesticAnimal(object):

    def __init__(self, color, sound, legs_count):
        self.color = color
        self.sound = sound
        self.legs_count = legs_count

    def make_sound(self):
        print('I am {} and I make {}!'.format(self.__class__.__name__, self.sound))


class Ungulate(DomesticAnimal):
    def __init__(self, color, sound, legs_count='4'):
        super().__init__(color, sound, legs_count)


class Poultry(DomesticAnimal):
    def __init__(self, color, sound, legs_count='2'):
        super().__init__(color, sound, legs_count)


class Cow(Ungulate):
    def __init__(self, color, sound='Moo'):
        super().__init__(color, sound)


class Goat(Ungulate):
    def __init__(self, color, sound='Meee'):
        super().__init__(color, sound)


class Sheep(Ungulate):
    def __init__(self, color, sound='Baaa'):
        super().__init__(color, sound)


class Pig(Ungulate):
    def __init__(self, color, sound='Oink'):
        super().__init__(color, sound)


class Duck(Poultry):
    def __init__(self, color, sound='Quack'):
        super().__init__(color, sound)


class Chicken(Poultry):
    def __init__(self, color, sound='Cluck'):
        super().__init__(color, sound)


class Goose(Poultry):
    def __init__(self, color, sound='Honk'):
        super().__init__(color, sound)
