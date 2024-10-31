#Imports
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

def main():
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

if __name__ == '__main__':
    main()

