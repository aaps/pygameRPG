Tipos = "planetaestrellasatelitecometa"
Operaciones = "UNIONINTERSECCIONDIFERENCIAPERTENECEADICIONAR"
Conjuntos = []

class ObjetoEspacial:
    def __init__(self, x, y):
        if x not in Tipos:
            return False
        self.tipo = x
        self.nombre = y
        
class Conjunto:
    def __init__(self):
        self.conjunto = []
        
    def esta(self, x, y):
        for elemento in self.conjunto:
            if elemento.tipo == x and elemento.nombre == y:
                return True
        return False
    
    def vacio(self):
        if len(self.conjunto) == 0:
            return True
        return False
    
    def agregar(self, x):
        for elemento in self.conjunto:
            if elemento == x:
                return False
        self.conjunto.append(x)
        return True
    
    def eliminar(self, x, y):
        for i in range(len(self.conjunto)):
            if self.conjunto[i].tipo == x and self.conjunto[i].nombre == y:
                self.conjunto = self.conjunto[0:i] + self.conjunto[i+1:]
                return True
        return False
    
    def union(self, x, y):
        conjunto = Conjunto()
        for elemento in self.conjunto:
            if elemento.tipo == y:
                conjunto.agregar(elemento)
        for elemento in x.conjunto:
            if elemento.tipo == y:
                if not conjunto.esta(elemento.tipo, elemento.nombre):
                    conjunto.agregar(elemento)
        return conjunto
    
    def interseccion(self, x, y):
        conjunto = Conjunto()
        for elemento in self.conjunto:
            if elemento.tipo == y:
                if x.esta(elemento.tipo, elemento.nombre):
                    conjunto.agregar(elemento)
        return conjunto
    
    def diferencia(self, x, y):
        inter = self.interseccion(x, y)
        conjunto = Conjunto()
        for elemento in self.conjunto:
            tipo = elemento.tipo
            nombre = elemento.nombre
            if not inter.esta(tipo, nombre):
                conjunto.agregar(elemento)
        self.conjunto = conjunto
                
    
    def __str__(self):
        string = ""
        for elemento in self.conjunto:
            string += elemento.tipo+","+elemento.nombre+" "
        return string
    
    
def comando():
    cmd = raw_input("Comando?").split(" ")
    if cmd[0] not in Operaciones and cmd[0] != "FIN":
        conjunto = Conjunto()
        if len(cmd) > 1:
            for elemento in cmd[1:]:
                elemento = elemento.split(",")
                conjunto.agregar(elemento[0], elemento[1])
        Conjuntos.append((cmd[0],conjunto))
    elif cmd[0] in Operaciones:
        c = 0
        if cmd[0] == "UNION":
            for conjunto in Conjuntos:
                if conjunto[0] == cmd[1]:
                    A = conjunto
                    c += 1
                if conjunto[0] == cmd[2]:
                    B = conjunto
                    c += 1
                if c == 2:
                    break
            A.union(B, cmd[3])
        #elif cmd[0] == "INTERSECCION":
        #elif cmd[0] == "DIFERENCIA":
        #elif cmd[0] == "PERTENECE":
        #elif cmd[0] == "ADICIONAR":
        
        