#Imports
import ffmpeg

class ColorYUV:

    #Atributos de la clase
    def __init__(self, Y,U, V):
        self.Y = Y
        self.U = U
        self.V = V

    #Función para obtener el color en sistema 
    def yuv_to_rgb(self):
        R = 1.164 * (self.Y - 16) + 1.596 * (self.V - 128)
        G = 1.164 * (self.Y - 16) - 0.813 * (self.V - 128) - 0.391 * (self.U - 128)
        B = 1.164 * (self.Y - 16) + 2.018 * (self.U - 128)
        color_rgb = ColorRGB(R,G,B)
        return color_rgb


class ColorRGB:

    #Atributos de la clase
    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

    #Función para obtener el color en sistema 
    def rgb_to_yuv(self):
        Y = 0.257 * self.R + 0.504*self.G + 0.098*self.B + 16
        U = -0.148*self.R - 0.291*self.G + 0.439*self.B + 128
        V = 0.439*self.R - 0.368*self.G - 0.071*self.B + 128
        color_yuv = ColorYUV(Y,U,V)
        return color_yuv
def pregunta_1():
    #En esta pregunta hay que comprobar la versión de ffmpeg
    ffmpeg

def pregunta_2():
    print("Pregunta 2")
    opcion = "a"
    while opcion != "c":
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
        
        elif opcion != "c":
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
   
def main():
    print("Lab 1")
    opcion = "1"
    while opcion != "0":  
        print("Hay una función por cada pregunta, a que pregunta deseas acceder?")
        print("0) Salir del script")
        print("1) Pregunta 1")
        print("2) Pregunta 2")
        print("3) Pregunta 3")


        opcion = input("Selecciona el número de pregunta que deseas:")
        
        if opcion == "1":
            pregunta_1()
        
        elif opcion == "2":
            pregunta_2()
        
        elif opcion == "3":
            pregunta_2()

        elif opcion != "0":
            print("Selecciona una opción valida.")
    

if __name__ == '__main__':
    main()

