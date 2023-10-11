
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 7:15:53 2023

@author: GabrielMtz
"""

import cv2 
import numpy as np
import math
from aristas import Arista

innerVertixList = []
connectionsList = []
visitedVertixList = []

nombreMapa="3"
#para cargar el mapa
mapa=cv2.imread('mapa'+nombreMapa+'.png')
# Para cargar la lista de indices
vertices=np.load("verticeMapa"+nombreMapa+".npy")
#pasamos la imagen a escala de grises
gray = cv2.cvtColor(mapa,cv2.COLOR_BGR2GRAY)
#muestro la imagen en escala de grises
# cv2.imshow('mapa3',gray)
#obtengo un binarizacion en blaco todos lo pixeles cuyo valor en sea entre 254 y 2555
ret,th1 = cv2.threshold(gray,254,255,cv2.THRESH_BINARY)
#hago un kernel de 11x11 de unos. Los Kernels se acostumbra hacerse de tamaño no par y cuadrados
#para que se den una idea algo asi:
"""
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
"""
kernel = np.ones((11,11), np.uint8) 
#aplico un filtro de dilatacion. Este filtro hace que los puntos blancos se expandan 
#probocando que algunos puntitos negros desaparecan #le pueden hacer un cv.imshow para que vean el resultado
th1 = cv2.dilate(th1,kernel,1)
kernel = np.ones((11,11), np.uint8) 
#Despues aplico uno de erosion que hace lo opuesto al de dilatacion
th1 = cv2.erode(th1,kernel,1)
#aplico un flitro gausiando de 5x5  para suavisar los bordes 
th1 = cv2.GaussianBlur(th1,(5,5),cv2.BORDER_DEFAULT)
#binarizo la imagen
ret,th2 = cv2.threshold(th1,235,255,cv2.THRESH_BINARY)
th2 = cv2.dilate(th2,kernel,1)
th2 = cv2.cvtColor(th2,cv2.COLOR_GRAY2BGR)


for vertice in vertices:
    # Los parametros de la funcion circle son:
    # - imagne donde se van a pintar
    # - coordenada del centro del cisculo (x,y)
    # - radio del circulo
    # - color
    # - grosor de la linea (-1 es para pintar un circulo relleno)
    # Como los vertices vienen en fila columna para pintarlos en la imagen paso sus valores al reves 
    cv2.circle(th2,(vertice[1],vertice[0]),3,(255,0,0),-1)
# cv2.imshow('thres2',th2)

# Acuerdense que las funciones de opencv esperan x y
# y las de arreeglos esperan fila columna
pruebaMap3 = th2.copy()
lista_vertices_visitados = []
resultados = []
                     
def getHalf(vertice1,vertice2):
    distanceX = (vertice1[0] + vertice2[0])/2
    distanceY = (vertice1[1] + vertice2[1])/2
    distanceX = int(distanceX)
    distanceY = int(distanceY)
    return distanceX, distanceY

is_answer = False
for vertice in vertices:
    for innerVertice in vertices:
        if (innerVertice[0] != vertice[0]) and (innerVertice[1] != vertice[1]):
            # Obtener el punto medio (x,y)
            distanceX, distanceY = getHalf(vertice,innerVertice)
            if (th2[distanceX,distanceY] != (0,0,0)).any():
                # Se crea un vertice auxiliar para poder mandar a llamar la función getHalf
                verticeAux = (distanceX,distanceY)
                # Por arriba del punto medio
                distanceX, distanceY = getHalf(vertice,verticeAux)
                # Por debajo del punto medio
                distanceX1, distanceY1 = getHalf(verticeAux, innerVertice)
                # Checa si ninguno de los puntos es color negro
                if(th2[distanceX,distanceY] != (0,0,0)).any() and (th2[distanceX1,distanceY1] != (0,0,0)).any():
                    # Se crea un vertice auxiliar para poder mandar a llamar la función getHalf
                    verticeAux = (distanceX,distanceY)
                    # Por arriba del punto medio
                    distanceX, distanceY = getHalf(vertice,verticeAux)
                    # Por debajo del punto medio
                    distanceX1, distanceY1 = getHalf(verticeAux, innerVertice)
                    # Checa si ninguno de los puntos es color negro
                    if(th2[distanceX,distanceY] != (0,0,0)).any() and (th2[distanceX1,distanceY1] != (0,0,0)).any():
                        # Se crea un vertice auxiliar para poder mandar a llamar la función getHalf
                        verticeAux = (distanceX,distanceY)
                        # Por arriba del punto medio
                        distanceX, distanceY = getHalf(vertice,verticeAux)
                        # Por debajo del punto medio
                        distanceX1, distanceY1 = getHalf(verticeAux, innerVertice)
                        # Checa si ninguno de los puntos es color negro
                        if(th2[distanceX,distanceY] != (0,0,0)).any() and (th2[distanceX1,distanceY1] != (0,0,0)).any():
                            # En caso de que ninguno de los puntos haya sido negro lo marca como respuesta
                            is_answer = True
        # En caso de que haya sido respuesta
        if is_answer:
            # Se calcula el costo
            costo = math.sqrt((vertice[0]-innerVertice[0])**2 + (vertice[1]-innerVertice[1])**2)
            # Se crea un objeto arista
            arista = Arista(vertice[0],vertice[1],innerVertice[0],innerVertice[1],costo)
            # Se crea una arista reversa para verificar que no se repita
            reversedArista = Arista(innerVertice[0],innerVertice[1],vertice[0],vertice[1],costo)
            # Para cada elemento dentro de la lista de conexiones
            for elemento in connectionsList:
                # Verifica si ya existe la conexión o su inversa en la lista
                if elemento == arista or elemento == reversedArista:
                    # Si existe regresa la bandera a falso y sale de la ejecución
                    is_answer = False 
                    break
            # Si al terminar la verificación sigue siendo respuesta
            if is_answer:
                # Añade la arista a la lista de conexiones
                connectionsList.append(arista)
                # Regresa la bandera a falso para que pueda ser activada de nuevo
                is_answer = False

# Ordena la lista de conectiones por costo
connectionsList.sort(key=lambda x: x.getCosto())

# Algoritmo de Prim
# Toma el primer vertice de la primer arista lista de aristas
lista_vertices_visitados.append(connectionsList[0].getVertice1().copy())
# Cuando la longitud de la lista de vertices visitados es igual a lista de vertices original, entonces ya termina la ejecución
while len(lista_vertices_visitados) != len(vertices):
    # Verifica por cada arista en la lista de aristas
    for arista in connectionsList:
        # Si el vertice 1 de la arista se encuentra en los vertices visitados
        if arista.getVertice1() in lista_vertices_visitados:
            # Verifica si el vertice 2 no está visitado
            if arista.getVertice2() not in lista_vertices_visitados:
                # En caso de que no esté visitado lo agrega
                lista_vertices_visitados.append(arista.getVertice2())
                # Agrega la arista a resultados
                resultados.append(arista)
                # Quita la arista de la lista de aristas para evitar verificarlo de nuevo
                connectionsList.remove(arista)
                break
        # Verifica si el vertice 2 está visitado
        elif arista.getVertice2() in lista_vertices_visitados:
            # Verifica si el vertice 1 no está visitado
            if arista.getVertice1() not in lista_vertices_visitados:
                # Si no está visitado lo agrega a la lista de vertices visitados
                lista_vertices_visitados.append(arista.getVertice1())
                # Añade la arista a la lista de resultados
                resultados.append(arista)
                # Quita la arista de la lista de aristas para evitar verificarlo de nuevo
                connectionsList.remove(arista)
                break

# Dibuja los resultados en el mapa
for resultado in resultados:
    cv2.line(th2, (resultado.getY1(), resultado.getX1()), (resultado.getY2(), resultado.getX2()), (120,150,30), 2)
    
cv2.imshow("Final",th2)
cv2.waitKey()