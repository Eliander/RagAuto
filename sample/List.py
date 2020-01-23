class List:

    def __init__(self, head, tail):
        self.car = head
        self.cdr = tail

    @staticmethod
    def cons(car, cdr):
        return List(car, cdr)

    def car(self):
        if type(self.car).__name__ == 'String':
            return self.car
        if type(self.car).__name__ == 'List':
            return self.car(self.car)

    def cdr(self):
        if type(self.cdr).__name__ == 'String':
            return self.cdr
        if type(self.cdr).__name__ == 'List':
            return self.cdr(self.cdr)

    def atom(self):
        if type(self).__name__ == 'List':
            return False
