#Imports
import ffmpeg
import numpy as np
from scipy.fftpack import dct, idct
import pywt
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage.color import rgb2gray
##############################################################
##### Clases para la pregunta 2

##Esta clase almacena colores en formato YUV y tiene un método para convertirlos en RGB
class ColorYUV:

    #Atributos de la clase, los 3 valores
    def __init__(self, Y,U, V):
        self.Y = Y
        self.U = U
        self.V = V

    #Función para obtener el color en sistema RGB, usa la formula proporcionada en las slides.
    def yuv_to_rgb(self):
        R = 1.164 * (self.Y - 16) + 1.596 * (self.V - 128)
        G = 1.164 * (self.Y - 16) - 0.813 * (self.V - 128) - 0.391 * (self.U - 128)
        B = 1.164 * (self.Y - 16) + 2.018 * (self.U - 128)

        #El color se devuelve en un objeto de la clase ColorRGB (Definida abajo)
        color_rgb = ColorRGB(R,G,B)
        return color_rgb

##Esta clase almacena colores en formato RGB y tiene un método para convertirlos en YUV
class ColorRGB:

   #Atributos de la clase, los 3 valores
    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

     #Función para obtener el color en sistema YUV, usa la formula proporcionada en las slides.
    def rgb_to_yuv(self):
        Y = 0.257 * self.R + 0.504*self.G + 0.098*self.B + 16
        U = -0.148*self.R - 0.291*self.G + 0.439*self.B + 128
        V = 0.439*self.R - 0.368*self.G - 0.071*self.B + 128
        
        #El color se devuelve en un objeto de la clase ColorRGB (Definida abajo)
        color_yuv = ColorYUV(Y,U,V)
        return color_yuv

class DCT_Encoder:
   #Atributos de la clase, tiene la imagen, la imagen codificada y el resultado de aplicar la inversa
    def __init__(self, input):
        self.imagen_original = input
        self.imagen_codificada = self.encode()
        self.imagen_reconstruida  = self.decode()

     #Función para calcular la DCT
    def encode(self):
        return dct(self.imagen_original)
    
    #Función para calcular la IDCT
    def decode(self):
        return idct(self.imagen_codificada)

class DWT_Encoder:
   #Atributos de la clase, tiene la imagen, la imagen codificada y el resultado de aplicar la inversa
    def __init__(self, input):
        self.imagen_original = input
        self.imagen_codificada = self.encode()
        self.imagen_reconstruida  = self.decode()

     #Función para calcular la DCT
    def encode(self):
        return pywt.dwt2(self.imagen_original, 'haar')
    
    #Función para calcular la IDCT
    def decode(self):
        return pywt.idwt2(self.imagen_codificada, 'haar')

    
##############################################################
##### Funciones para las diferentes preguntas

def pregunta_1():
    #En esta pregunta hay que comprobar la versión de ffmpeg. 
    ffmpeg

def pregunta_2():

    print("Pregunta 2")
    while True:
        print("Este script permite convertir los colores de formato RGB a formato YUV y viceversa")
        print("a) De RGB a YUV")
        print("b) De YUV a RGB")
        print("c) salir")
        opcion = input("Introduce la opción deseada: ")

        if opcion == "a":
            print("Porfavor, usa . para los decimales.")
            R = float(input("Introduce el componente R del color: "))
            G = float(input("Introduce el componente G del color: "))
            B = float(input("Introduce el componente B del color: "))
            
            color_rgb = ColorRGB(R,G,B)
            color_yuv = color_rgb.rgb_to_yuv()
            
            print(f"El color en YUV es Y:{color_yuv.Y} , U:{color_yuv.U} , V:{color_yuv.V}")
        
        elif opcion == "b":
            print("Porfavor, usa . para los decimales.")
            Y = float(input("Introduce el componente Y del color: "))
            U = float(input("Introduce el componente U del color: "))
            V = float(input("Introduce el componente V del color: "))
            
            color_yuv = ColorYUV(Y,U,V)
            color_rgb = color_yuv.yuv_to_rgb()
            
            print(f"El color en RGB es R:{color_rgb.R} , G:{color_rgb.G} , B:{color_rgb.B}")
        
        elif opcion == "c":
           break
        
        else:
            print("Selecciona una opción válida") 


def pregunta_3():
    print("Pregunta 3")
    print("Este script permite cambiar la resolución de una imagen.")

    path = input("Introduce el directorio relativo de la imagen: ")

    ancho = int(input("Introduce el número de pixeles  para el ancho: "))
    alto = int(input("Introduce el número de pixeles  para el alto: "))

    ffmpeg.input(path).output('output.jpg', vf=f'scale={ancho}:{alto}').run()

def pregunta_4():
    print("Pregunta 4")
    #Dada una matriz leerla de manera serpentine
    print("Este script permite leer de manera 'serpentine' una imagen.")
    #path = input("Introduce el directorio relativo de la imagen: ")
    #matriz = input("Introduce una matriz a leer: ")

    #Dada una matriz 8 x 8 leerla de manera serpentine
    #directorio = input("Introduce el directorio relativo de la matriz: ")
    #archivo = open(directorio, 'r')
    #numero_filas = len(archivo.readlines())
    #print(numero_filas)
    #for i in range(numero_filas):
        #matrix[i] = archivo.readline()
        #print(matrix[i])

    #Definimos la matriz a leer TODO: Cogerlo de un archivo 
    matrix = [[1,2,6,7,14],[3,5,8,13,15],[4,9,12,16,19],[10,11,17,18,20]]

    #Definimos las variables que contienen el numero máximo de filas y columnas
    M = len(matrix)
    N = len(matrix[0]) if M > 0 else 0

    #Esta array va a contener los valores de la matriz en el orden de lectura "serpentine"
    output = []

    #Inicializamos los indices para leer la matriz
    i, j = 0, 0  

    #El numero de la iteración, va a definir el sentido de lectura de la "serpentine"
    numero_iteracion = 1

    #Hay tantas iteraciones como elementos de la matriz
    while len(output) < M * N:
        #Si estamos en una iteración par, leemos de arriba a abajo. El número de la columna (j) decrece y el de la fila (x) crece
        if numero_iteracion % 2 == 0:
            while i < M and j >= 0:
                #Añadimos el valor actual al output y modificamos los indices acorde al orden de lectura
                output.append(matrix[i][j])
                i += 1
                j -= 1
                
                #Si llegamos a los limites (primera columna o la ultima fila), se cambia el orden de lectura 
                # y se avanza una posicion hacia abajo (si estamos en la primera columna) o una posicion a la derecha (si estamos)
                if i == M or j < 0: 
                    if j < 0 and i < M:
                        #Como ya hemos avanzado una posicion en la i, solo hace falta que la que j sea 0
                        j = 0
                    else:  
                        #Como se le ha restado una a la j anteriormente, hay que sumarle 2. Tenemos que quitarle lo que se le ha añadido a la i
                        j += 2
                        i -= 1
                    numero_iteracion += 1
                    break
        
        
        else:
            #Si estamos en una iteración impar, leemos de abajo a arriba. El número de la columna (j) crece y el de la fila (x) decrece.
            while i >= 0 and j < N:
                #Añadimos el valor actual al output y modificamos los indices acorde al orden de lectura
                output.append(matrix[i][j])
                i -= 1
                j += 1
                
                #Si llegamos a los limites (primera fila o la ultima columna), se cambia el orden de lectura 
                # y se avanza una posicion hacia abajo (si estamos en la última columna) o una posicion a la derecha (si estamos en la primera fila)
                if i < 0 or j == N:  
                    if i < 0 and j < N: 
                        #Como ya se ha avanzado una posición de la j, solo hay que reiniciar la i a 0
                        i = 0
                    else:  
                        #Como se le ha restado una a la i, para avanzar a la derecha hay que sumarle dos. Correjimos la cantidad añadida a la j
                        i += 2
                        j -= 1
                    numero_iteracion += 1
                    break
    print("Ouput: ", output)


def pregunta_5():
    print("Pregunta 5")
    print("Este script permite cambiar la imagen a blanco y negro")

    path = input("Introduce el directorio relativo de la imagen: ")
    ffmpeg.input(path).filter("format", "gray").output('output_bw.jpg').run()

def pregunta_6():
    #TODO: CERRAR LOS ARCHIVOS
    print("Pregunta 6")
    directorio = input("Introduce el directorio relativo de un archivo .txt conteniendo el stream de datos:")
    
    input_stream = open(directorio, 'r')
    data_stream = input_stream.read()

    count = 0
    output = open("output.txt",'w')
    for i in data_stream:
        if i == "0":
            count += 1
        elif i != "0" and count > 0 and i != " ":
            output.write("0")
            output.write(str(" "))
            output.write(str(count))
            output.write(str(" "))
            output.write(str(i))
            count = 0
        elif i != "0" and count > 0 and i == " ":
            pass
        else:
            output.write(str(i))

def pregunta_7():
    print("Pregunta 7")  
    path = input("Introduce el directorio relativo de la imagen: ")
    encoder = DCT_Encoder(rgb2gray(imread(path)))
    #
    plt.gray()
    plt.subplot(121), plt.imshow(encoder.imagen_original), plt.axis('off'), plt.title('Imagen original', size=20)
    plt.subplot(122), plt.imshow(encoder.imagen_reconstruida), plt.axis('off'), plt.title('Imagen reconstruida(DCT+IDCT)', size=20)

    plt.show()

def pregunta_8():
    print("Pregunta 8")  
    path = input("Introduce el directorio relativo de la imagen: ")
    encoder = DWT_Encoder(rgb2gray(imread(path)))
    #
    plt.gray()
    plt.subplot(121), plt.imshow(encoder.imagen_original), plt.axis('off'), plt.title('Imagen original', size=20)
    plt.subplot(122), plt.imshow(encoder.imagen_reconstruida), plt.axis('off'), plt.title('Imagen reconstruida(DWT+IDWT)', size=20)

    plt.show()

def main():
    print("Lab 1")

    while True:  
        print("Hay una función por cada pregunta, a que pregunta deseas acceder?")
        print("0) Salir del script")
        print("1) Pregunta 1")
        print("2) Pregunta 2")
        print("3) Pregunta 3")
        print("4) Pregunta 4")
        print("5) Pregunta 5")
        print("6) Pregunta 6")
        print("7) Pregunta 7")
        print("8) Pregunta 8")

        opcion = input("Selecciona el número de pregunta que deseas:")
       
        match opcion:
            case "0":
                print("Saliendo del Script")
                break
            case "1":
                pregunta_1()
            case "2":
                pregunta_2()
            case "3":
                pregunta_3()
            case "4":
                pregunta_4()
            case "5":
                pregunta_5()
            case "6":
                pregunta_6()
            case "7":
                pregunta_7()
            case "8":
                pregunta_8()
            case _:
                print("Selecciona una opción valida.")

    

if __name__ == '__main__':
    main()

