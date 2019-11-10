
class c():

    def __init__(self):
        pass

    def f(self, msg):
        return "f said " + msg


def g():
    return "G"


cc = c()
c2 = c()

cc.q = g

print(dir(cc))
print(dir(c2))