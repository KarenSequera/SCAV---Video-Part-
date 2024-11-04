#Imports
import ffmpeg
import numpy

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
    #Dada una matriz 8 x 8 leerla de manera serpentine
    directorio = input("Introduce el directorio relativo de la matriz: ")
    archivo = open(directorio, 'r')
    numero_filas = len(archivo.readlines())
    print(numero_filas)
    matrix = []
    for i in range(numero_filas):
        matrix[i] = archivo.readline()
        print(matrix[i])

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
            case _:
                print("Selecciona una opción valida.")

    

if __name__ == '__main__':
    main()

