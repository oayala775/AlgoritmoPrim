class Arista:
    def __init__(self,x1,y1,x2,y2,costo):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__costo = costo
        
    def getX1(self):
        return self.__x1
    
    def setX1(self,x1):
        self.__x1 = x1
        
    def getY1(self):
        return self.__y1
    
    def setY1(self,y1):
        self.__y1 = y1
        
    def getX2(self):
        return self.__x2
    
    def setX2(self,x2):
        self.__x2 = x2
        
    def getY2(self):
        return self.__y2
    
    def setY1(self,y2):
        self.__y2 = y2
        
    def getCosto(self):
        return self.__costo
    
    def setCosto(self,costo):
        self.__costo = costo
        
    def setID(self, identificador):
        self.__id = identificador
        
    def getVertice1(self):
        return [self.__x1, self.__y1]
    
    def setVertice1(self, vertice):
        self.__x1 = vertice[0]
        self.__y1 = vertice[1]
    
    def getVertice2(self):
        return [self.__x2, self.__y2]
    
    def setVertice2(self, vertice):
        self.__x2 = vertice[0]
        self.__y2 = vertice[1]
        
    def __str__(self):
        return f"Vertice ({self.__x1},{self.__y1}) a ({self.__x2},{self.__y2}) con costo {self.__costo}"
    
    def __eq__(self,other):
        return ((self.__x1 == other.getX1()) and (self.__y1 == other.getY1()) and (self.__x2 == other.getX2()) and (self.__y2 == other.getY2())) or ((self.__x2 == other.getX1()) and (self.__y2 == other.getY1()) and (self.__x1 == other.getX2()) and (self.__y2 == other.getY2())) 
    
    def __gt__(self,other):
            return self.__costo > other.getCosto()
        