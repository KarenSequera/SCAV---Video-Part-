#Imports
import ffmpeg
import numpy as np
from scipy.fftpack import dct, idct
import pywt
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage.color import rgb2gray

## Pregunta 1
def pregunta_1():
    #En esta pregunta hay que comprobar la versión de ffmpeg. 
    #Esta funcion enseña la imagen de la primera linea que aparece en la consola al ejecutar "ffmpeg"
    imagen = (imread("ffmpeg.jpg"))
    
    plt.figure()
    plt.imshow(imagen), plt.axis('off'), plt.title('Version FFMPEG', size=20)
    plt.show()

## Pregunta 2

class Color_Translator:
    #Los dos metodos asumen que el input es correcto (float)

    #Método para obtener el color en sistema YUV dado RGB, usa la formula proporcionada en las slides.
    # -Y: Float conteniendo el valor Y del sistema YUV.
    # -U: Float conteniendo el valor U del sistema YUV.
    # -V: Float conteniendo el valor V del sistema YUV. 
    @staticmethod
    def rgb_to_yuv(R,G,B):
        Y = 0.257 * R + 0.504*G + 0.098*B + 16
        U = -0.148*R - 0.291*G + 0.439*B + 128
        V = 0.439*R - 0.368*G - 0.071*B + 128
        #El color YUV se devuelve en una lista
        return [Y,U,V]
    
    #Método para obtener el color en sistema RGB dado YUV, usa la formula proporcionada en las slides.
    # -R: Float conteniendo el valor R del sistema RGB.
    # -G: Float conteniendo el valor G del sistema RGB.
    # -B: Float conteniendo el valor B del sistema RGB. 
    @staticmethod  
    def yuv_to_rgb(Y,U,V):
        R = 1.164 * (Y - 16) + 1.596 * (V - 128)
        G = 1.164 * (Y - 16) - 0.813 * (V - 128) - 0.391 * (U - 128)
        B = 1.164 * (Y - 16) + 2.018 * (U - 128)

        #El color RGB se devuelve en una lista
        return [R,G,B]
    
def pregunta_2():
    print("\nPregunta 2")
    while True:
        print("\nEste script permite convertir los colores de formato RGB a formato YUV y viceversa")
        print("a) De RGB a YUV")
        print("b) De YUV a RGB")
        print("c) salir")
        opcion = input("\nIntroduce la opción deseada: ")

        if opcion == "a":
            print("\nPorfavor, usa . para los decimales.")
            R = float(input("Introduce el componente R del color: "))
            G = float(input("Introduce el componente G del color: "))
            B = float(input("Introduce el componente B del color: "))
            
            color_yuv = Color_Translator.rgb_to_yuv(R,G,B)
            
            print(f"\nEl color en YUV es Y:{color_yuv[0]} , U:{color_yuv[1]} , V:{color_yuv[2]}")
        
        elif opcion == "b":
            print("\nPorfavor, usa . para los decimales.")
            Y = float(input("Introduce el componente Y del color: "))
            U = float(input("Introduce el componente U del color: "))
            V = float(input("Introduce el componente V del color: "))
            
            color_rgb = Color_Translator.yuv_to_rgb(Y,U,V)
            
            print(f"\nEl color en RGB es R:{color_rgb[0]} , G:{color_rgb[1]} , B:{color_rgb[2]}")
        
        elif opcion == "c":
           break
        
        else:
            print("Selecciona una opción válida")

## Pregunta 3
#Esta función genera un comando de ffmpeg que dado:
# -Directorio: Directorio relativo de la imagen, si esta en la misma carpeta el nombre del archivo es suficiente
# -Ancho: Número de pixeles deseados para el ancho de la imagen
# -Alto: Número de pixeles deseados para el alto de la imagen
# Genera una imagen con las dimensiones deseadas
def resolution_changer(directorio, ancho, alto, output_name):
    ffmpeg.input(directorio).output(output_name, vf=f'scale={ancho}:{alto}').run()

def pregunta_3():
    print("\nPregunta 3")
    print("\nEste script permite cambiar la resolución de una imagen.")

    directorio = input("Introduce el directorio relativo de la imagen: ")
    ancho = int(input("Introduce el número de pixeles  para el ancho: "))
    alto = int(input("Introduce el número de pixeles  para el alto: "))

    #Llamada a la función que cambia la resolució.
    resolution_changer(directorio, ancho, alto,'output_p3.jpg')

    imagen_input = imread(directorio)
    imagen_output = imread('output_p3.jpg')
    
    #Código para mostrar las imagenes
    plt.figure()
    plt.subplot(121), plt.imshow(imagen_input), plt.axis('off'), plt.title('Imagen original')
    plt.subplot(122), plt.imshow(imagen_output), plt.axis('off'), plt.title(f'Imagen escala={ancho}x{alto}')
    plt.show()

## Pregunta 4
# Esta función lee la matriz siguiendo el orden "Serpentine" establecido en las slides de clase
# -Matriz: Se asume que es una Lista de Listas (matriz)
# -output: Contiene el contenido de la matriz en orden "serpentine"
def serpentine(matriz):
    
    #Definimos las variables que contienen el numero máximo de filas y columnas
    M = len(matriz)
    N = len(matriz[0]) if M > 0 else 0

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
                output.append(matriz[i][j])
                i += 1
                j -= 1
                
                #Si llegamos a los limites (primera columna o la ultima fila), se cambia el orden de lectura 
                # y se avanza una posicion hacia abajo (si estamos en la primera columna) o una posicion a la derecha (si estamos)
                if i == M or j < 0: 
                    if j < 0 and i < M:
                        #Se avanza una posición hacía abajo
                        #Como ya hemos avanzado una posicion en la i, solo hace falta que la que j sea 0
                        j = 0
                    else:  
                        #Se avanza una posición a la derecha
                        #Como se le ha restado una a la j anteriormente, hay que sumarle 2. 
                        #Tenemos que quitarle lo que se le ha añadido a la i
                        j += 2
                        i -= 1
                    numero_iteracion += 1
                    break
        
        else:
            #Si estamos en una iteración impar, leemos de abajo a arriba. El número de la columna (j) crece y el de la fila (x) decrece.
            while i >= 0 and j < N:
                #Añadimos el valor actual al output y modificamos los indices acorde al orden de lectura
                output.append(matriz[i][j])
                i -= 1
                j += 1
                
                #Si llegamos a los limites (primera fila o la ultima columna), se cambia el orden de lectura 
                # y se avanza una posicion hacia abajo (si estamos en la última columna) o una posicion a la derecha (si estamos en la primera fila)
                if i < 0 or j == N:  
                    if i < 0 and j < N: 
                        #Se avanza una posición hacia abajo,
                        #Como ya se ha avanzado una posición de la j, solo hay que reiniciar la i a 0
                        i = 0
                    else:  
                        #Se abanza una posición a la derecha
                        #Como se le ha restado una a la i, para avanzar a la derecha hay que sumarle dos. 
                        #Correjimos la cantidad añadida a la j
                        i += 2
                        j -= 1
                    numero_iteracion += 1
                    break
    return output

def pregunta_4():
    print("\nPregunta 4")
    matriz = [[1,2,6,7,14],[3,5,8,13,15],[4,9,12,16,19],[10,11,17,18,20]]
    output = serpentine(matriz)
    print("Ouput: ", output)

## Pregunta 5

#Esta función genera un comando de ffmpeg que dado:
# -Directorio: Directorio relativo de la imagen, si esta en la misma carpeta el nombre del archivo es suficiente
# Genera una versión en blanco y negro de la imagen
def bw_converter(directorio, output_name):
    ffmpeg.input(directorio).filter("format", "gray").output(output_name).run()

def pregunta_5():
    print("\nPregunta 5")
    print("\nEste script permite cambiar la imagen a blanco y negro")

    directorio = input("Introduce el directorio relativo de la imagen: ")
    
    bw_converter(directorio, 'output_p5.jpg')

    #Código para mostrar las imagenes
    imagen_input = imread(directorio)
    imagen_output = imread('output_p5.jpg')
    plt.figure()
    plt.subplot(121), plt.imshow(imagen_input), plt.axis('off'), plt.title('Imagen original', size=20)
    plt.subplot(122), plt.imshow(imagen_output), plt.axis('off'), plt.title('Imagen BW', size=20)
    plt.show()

## Pregunta 6

#Esta función dado un directorio conteniendo un data stream (.txt) en formato mostrado en las slides
#es decir, números separados por espacios, los introduce en una lista.
#  -Directorio: Directorio relativo de .txt, si esta en la misma carpeta el nombre del archivo es suficiente
#  -Output_list: Lista con los contenidos del .txt
def lector_data_stream(directorio):
    input_stream = open(directorio, 'r')
    data_stream = input_stream.read()

    output_list = []
    item = ""

    for i in data_stream:
        #Si no hay espacio en blanco, dos characteres consecutivos constituyen el mismo número
        #Y se guardan en la misma posición de la lista
        if i !=  " ":
            item += i
        
        #Si encontramos un espacio en blanco, hay que almacenar el número y resetear 
        # la variable que acomula los carácteres
        else:
            output_list.append(int(item))
            item = ""
    
    #Si el último número no esta seguido de un espacio en blanco,
    #no se añadirá. Comprobamos el caso manualmente
    if item != "":
        output_list.append(int(item))
    
    input_stream.close()
    return output_list

#Esta función implementa el run_lenght algoritmo presentado en las slides
# - List: lista conteniendo el data stream al que se le desea aplicar el algoritmo
# - output_list: Lista conteniendo el resultado. Las posiciones que contienen 0+Count, son strings.
def run_lenght(list):
    output_list = []
    count = 0
    for i in list:
        if i == 0:
            #Si hay un cero la variable count augmenta
            count += 1

        elif i != 0 and count > 0:
            #Si count es mayor a uno y el siguiente número no es cero, 
            #hay que escribir en el output el número de ceros consecutivos "0 Count"
            output_list.append("0"+ str(count))
            #Se escribe el número normalmente 
            output_list.append(i)
            count = 0
        else:
            #Se escribe el número normalmente 
            output_list.append(int(i))

    return output_list
            
def pregunta_6():
    print("\nPregunta 6")
    directorio = input("\nIntroduce el directorio relativo de un archivo .txt conteniendo el stream de datos:")
    list = lector_data_stream(directorio)
    output_list = run_lenght(list)
    print("\nEl output es:")
    print(output_list)


## Pregunta 7
class DCT_Encoder:
    #Nuestro encoder usa la implementación de la DCT y la IDCT de la libreria scipy.fftpack siguiendo un ejemplo de uso de
    #Stack Overflow para imagenes
    
    #Referencias: https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html
    #             https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.idct.html
    #             https://stackoverflow.com/questions/7110899/how-do-i-apply-a-dct-to-an-image-in-python

    #Función para calcular la DCT
    @staticmethod
    def encode(imagen):
        return dct(dct(imagen.T, norm='ortho').T, norm='ortho')
    #Función para calcular la IDCT
    @staticmethod
    def decode(imagen):
        return idct(idct(imagen.T, norm='ortho').T, norm='ortho')

def pregunta_7():
    print("\nPregunta 7")  
    path = input("\nIntroduce el directorio relativo de la imagen: ")

    #En el ejemplo solo vamos a visualizar un canal, asi que usamos la imagen en blanco y negro
    #Para usarlo en RGB hay que codificar cada uno de los canales.

    imagen = (rgb2gray(imread(path)))
    imagen_encoded = DCT_Encoder.encode(imagen)
    imagen_decoded = DCT_Encoder.decode(imagen_encoded)

    #Código para mostrar las imagenes
    plt.gray()
    plt.subplot(131), plt.imshow(imagen), plt.axis('off'), plt.title('Imagen original', size=20)
    #Visualizamos la magnitud de la dct de manera logaritmica 
    plt.subplot(132), plt.imshow(np.log(np.abs(imagen_encoded),),cmap='hot'), plt.axis('off'), plt.title('Coeficientes DCT (Escala log)', size=15)
    plt.subplot(133), plt.imshow(imagen_decoded), plt.axis('off'), plt.title('Imagen reconstruida (DCT+IDCT)', size=20)
    plt.show()

class DCT_Encoder_SlidesFormula:
    #Función alpha, si el input es 0 tiene valor raiz(1/8), sino raiz(2/8)
    def alpha(n):
        if n == 0:
            output = np.sqrt(1/8)
        else:
            output = np.sqrt(2/8)
        return  output
    
    @staticmethod
    #La formula de las slides esta pensada para matrices de 8x8, así que se asume que la matriz va a tener esas dimensiones
    def encode(matrix): 

        #Inicializamos la matriz que va a contener el output
        G = np.zeros((8,8))
        
        #Ahora iteramos por cada uno de los "pixeles"/valores de la matriz (u y v en la formula)
        for u in range(8):
            for v in range(8):

                coef = DCT_Encoder_SlidesFormula.alpha(u) * DCT_Encoder_SlidesFormula.alpha(v)
                sum = 0

                for x in range(8):
                    for y in range(8):
                        sum += matrix[x][y] * np.cos((np.pi / 8) * (x + 1/2) * u) * np.cos((np.pi / 8) * (y + 1/2) * v)
                                                                                           
                G[u][v] = coef * sum

        return G 

    @staticmethod
    def decode(encoded_matrix):
        # Inicializamos la matriz que va a contener el output
        matrix = np.zeros((8, 8))

        # Operación inversa para obtener los valores iniciales de la matriz
        # Referencias: Hemos adaptado la formula de la idct de la pagina 14 para que se adecue al ejemplo de las slides de clase (8x8)
        #              https://es.slideshare.net/slideshow/discrete-cosine-transform/13643007#14

        for x in range(8):
            for y in range(8):
                
                sum = 0
                for u in range(8):
                    for v in range(8):
                        coef = DCT_Encoder_SlidesFormula.alpha(u) * DCT_Encoder_SlidesFormula.alpha(v)
                        sum += coef * encoded_matrix[u][v] * np.cos((np.pi / 8) * (x + 1/2) * u) * np.cos((np.pi / 8) * (y + 1/2) * v)

                matrix[x][y] = sum

        return matrix
    

def pregunta_7_manual():
    print("\nPregunta 7 - versión manual de la dct") 
    matriz = [[72, 70, 65, 65, 66, 68,  0,  0],
              [71, 65, 65, 63, 64, 67,  0,  0],
              [73, 66, 67, 65, 66, 69,  0,  0],
              [75, 65, 66, 64, 64, 63,  0,  0],
              [72, 68, 63, 62, 61, 60,  0,  0],
              [0,   0,  0,  0,  0,  0,  0,  0],
              [0,   0,  0,  0,  0,  0,  0,  0],
              [0,   0,  0, 0,   0,  0,  0,  0]]
    
    matriz_encoded = DCT_Encoder_SlidesFormula.encode(matriz)
    print("\nLa dct de la matriz introducida es: ") 
    print(matriz_encoded)
    matriz_decoded = DCT_Encoder_SlidesFormula.decode(matriz_encoded)
    print("\nLa dct de la matriz introducida es: ")
    print(matriz_decoded)

## Pregunta 8
class DWT_Encoder:
    #Nuestro encoder usa la implementación de la DWT y la IDWT de la libreria pwt siguiendo un ejemplo de uso de
    #para imagenes de un blog de la propia libreria.
    
    #Referencias: https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html
    #             https://pywavelets.readthedocs.io/en/latest/

     #Función para calcular la DWT
    @staticmethod
    def encode(imagen):
        return pywt.dwt2(imagen, 'bior1.3')
    
    #Función para calcular la IDWT
    @staticmethod
    def decode(imagen):
        return pywt.idwt2(imagen, 'bior1.3')

def pregunta_8():
    print("\nPregunta 8")  
    path = input("\nIntroduce el directorio relativo de la imagen: ")
   
    imagen = (rgb2gray(imread(path)))
    imagen_encoded = DWT_Encoder.encode(imagen)
    imagen_decoded = DWT_Encoder.decode(imagen_encoded)

    #Código para mostrar las imagenes
    plt.gray()
    plt.subplot(121), plt.imshow(imagen), plt.axis('off'), plt.title('Imagen original', size=20)
    plt.subplot(122), plt.imshow(imagen_decoded), plt.axis('off'), plt.title('Imagen reconstruida (DWT+IDWT)', size=20)

    plt.show()

    #Código para mostrar la decomposición 2D (extraido del blog)
    titles = ['LL - Approximation', 'LH - Horizontal detail','HL - Vertical detail', 'HH - Diagonal detail']
    LL, (LH, HL, HH) = imagen_encoded
    fig = plt.figure(figsize=(12, 3))
    for i, a in enumerate([LL, LH, HL, HH]):
        ax = fig.add_subplot(1, 4, i + 1)
        ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
        ax.set_title(titles[i], fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.tight_layout()
    plt.show()

## El unit TEST esta en un archivo separado!

###################
def main():
    print("Lab 1")

    while True:  
        print("\nHay una función por cada pregunta, a que pregunta deseas acceder?")
        print("0) Salir del script")
        print("1) Pregunta 1")
        print("2) Pregunta 2")
        print("3) Pregunta 3")
        print("4) Pregunta 4")
        print("5) Pregunta 5")
        print("6) Pregunta 6")
        print("7) Pregunta 7")
        print("8) Pregunta 8")
        print("9) Pregunta 7 - Implementación slides (funciona solo matrices)")


        opcion = input("\nSelecciona el número de pregunta que deseas:")
       
        if opcion == "0":
            print("\nSaliendo del Script")
            break
        elif opcion == "1":
            pregunta_1()
        elif opcion == "2":
            pregunta_2()
        elif opcion == "3":
            pregunta_3()
        elif opcion == "4":
            pregunta_4()
        elif opcion == "5":
            pregunta_5()
        elif opcion == "6":
            pregunta_6()
        elif opcion == "7":
            pregunta_7()
        elif opcion == "8":
            pregunta_8()
        elif opcion == "9":
            pregunta_7_manual()
        else:
            print("\nSelecciona una opción válida.")


if __name__ == '__main__':
    main()