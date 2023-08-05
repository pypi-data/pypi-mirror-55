from ..two.two_class import TwoClass


class OneClass:
    def use_two(self):
        obj = TwoClass()
        return obj.func()
