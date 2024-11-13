import unittest
import first_seminar 
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
from matplotlib import pyplot as plt

# Nota: este codigo ha sido creado con la ayuda de la IA como se menciona en el enunciado
# Se ha tenido que corregir manualmente los resultados esperados ya que en muchos casos eran erroneos

class TestColorTranslator(unittest.TestCase):

    def test_rgb_to_yuv(self):
        translator = first_seminar.Color_Translator()
        # Test con un color RGB (255, 0, 0) que debe dar un color YUV cercano a [81.535, 90.26, 239.945]
        result = translator.rgb_to_yuv(255, 0, 0)
        self.assertAlmostEqual(result[0], 81.535, delta=0.1)  # Y
        self.assertAlmostEqual(result[1], 90.26, delta=0.1)  # U
        self.assertAlmostEqual(result[2], 239.945, delta=0.1)   # V

    def test_yuv_to_rgb(self):
        translator = first_seminar.Color_Translator()
        # Test con un color YUV (81.535, 90.26, 239.945) que debe dar un color RGB cercano a [255.0, 0.0, 0.0]
        result = translator.yuv_to_rgb(81.535, 90.26, 239.945)
        self.assertAlmostEqual(result[0], 255.0, delta=1)  # R
        self.assertAlmostEqual(result[1], 0.0, delta=1)    # G
        self.assertAlmostEqual(result[2], 0.0, delta=1)    # B

class TestSerpentine(unittest.TestCase):

    def test_serpentine(self):
        # Test con una matriz de ejemplo
        matriz = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        # El recorrido serpenteante de esta matriz debe devolver:
        # [1, 2, 4, 7, 5, 3, 6, 8, 9]
        expected_result = [1, 2, 4, 7, 5, 3, 6, 8, 9]
        result = first_seminar.serpentine(matriz)
        self.assertEqual(result, expected_result)

        # Test con una matriz más grande
        matriz = [
            [1,    2,     3,      4],
            [5,    6,     7,      8],
            [9,    10,    11,    12]
        ]
        # El recorrido serpenteante debe devolver:
        # [1, 2, 5, 9, 6, 3, 4, 7, 10, 11, 8, 12]
        expected_result = [1, 2, 5, 9, 6, 3, 4, 7, 10, 11, 8, 12]
        result = first_seminar.serpentine(matriz)
        self.assertEqual(result, expected_result)

class TestRunLength(unittest.TestCase):

    def test_run_length(self):
        # Test con una lista que tiene ceros consecutivos
        lista = [1, 0, 0, 2, 0, 0, 0, 3]
        # El resultado esperado debería ser: [1, '02', 2, '03', 3]
        expected_result = [1, '02', 2, '03', 3]
        result = first_seminar.run_lenght(lista)
        self.assertEqual(result, expected_result)

        # Test con una lista sin ceros
        lista = [1, 2, 3, 4, 5]
        # El resultado debería ser la misma lista ya que no hay ceros
        expected_result = [1, 2, 3, 4, 5]
        result = first_seminar.run_lenght(lista)
        self.assertEqual(result, expected_result)

        # Test con una lista que solo tiene ceros
        lista = [0, 0, 3, 4, 8, 6, 33, 0, 0, 0, 4]
        # El resultado esperado es: ['02', 3, 4, 8, 6, 33,'03', 4]
        expected_result = ['02', 3, 4, 8, 6, 33,'03', 4]
        result = first_seminar.run_lenght(lista)
        self.assertEqual(result, expected_result)

##Para los unit test de las funciones que utilizan ffmpeg simplemente vamos a llamar a las funciones con diferentes imagenes.
def ejecutar_tests_resolution_changer():

    #Nota: El output se guarda en la carpeta unit_test_output_resize, se recomienda eliminar el contenido para que 
    #ffmpeg no pregunte en cada prueba si se deseaa reescribir el contenido. 

    archivos = ['bosque.jpg', 'gato.jpg', 'perro.jpg']
    resoluciones = [(800, 600), (320, 240), (10,10)]
    
    i = 0
    for archivo in archivos:
        print(f"\nProbando el archivo {archivo} con diferentes resoluciones...")

        for ancho, alto in resoluciones:
            print(f" - Resolución {ancho}x{alto}")

            # Nombre de salida específico para cada imagen redimensionada
            output_name = f'unit_test_output_resize/output_{i}.jpg'

            # Llamada a la función que cambia la resolución
            first_seminar.resolution_changer(archivo, ancho, alto, output_name)

            # Cargar y mostrar la imagen de entrada y la imagen resultante
            imagen_input = imread(archivo)
            imagen_output = imread(output_name)  # Cargar la imagen redimensionada desde output_name

            # Mostrar imágenes
            plt.figure(figsize=(10, 5))
            plt.subplot(121), plt.imshow(imagen_input), plt.axis('off'), plt.title('Imagen original', size=15)
            plt.subplot(122), plt.imshow(imagen_output), plt.axis('off'), plt.title(f'Resolución {ancho}x{alto}', size=15)
            plt.show()
            
            i += 1

def ejecutar_tests_bw():

    #Nota: El output se guarda en la carpeta unit_test_bw, se recomienda eliminar el contenido para que 
    #ffmpeg no pregunte en cada prueba si se deseaa reescribir el contenido. 
    
    archivos = ['bosque.jpg', 'gato.jpg', 'perro.jpg']    

    i = 0
    for archivo in archivos:
        print(f"\nTransformando {archivo} a blanco y negro...")

        output_name = f'unit_test_bw/output_{i}.jpg'
        first_seminar.bw_converter(archivo, output_name)

        #Código para mostrar las imagenes
        imagen_input = imread(archivo)
        imagen_output = imread(output_name)
        plt.figure()
        plt.subplot(121), plt.imshow(imagen_input), plt.axis('off'), plt.title('Imagen original', size=20)
        plt.subplot(122), plt.imshow(imagen_output), plt.axis('off'), plt.title('Imagen BW', size=20)
        plt.show()
        i += 1

def ejecutar_tests_dct_encoder():

    # Directorio de salida (opcional, si deseas guardar resultados)

    archivos = ['bosque.jpg', 'gato.jpg', 'perro.jpg']

    for archivo in archivos:

        print(f"\nAplicando DCT e IDCT a la imagen {archivo}...")

        # Cargar la imagen y convertir a escala de grises
        imagen = rgb2gray(imread(archivo))

        # Aplicar la DCT y la IDCT
        imagen_encoded = first_seminar.DCT_Encoder.encode(imagen)
        imagen_decoded = first_seminar.DCT_Encoder.decode(imagen_encoded)

        # Visualizar las imágenes: original, coeficientes DCT (en escala log), y la imagen reconstruida
        plt.figure(figsize=(15, 5))
        plt.gray()
        
        # Imagen original
        plt.subplot(131)
        plt.imshow(imagen), plt.axis('off')
        plt.title('Imagen original', size=20)
        
        # Coeficientes DCT (logarítmica)
        plt.subplot(132)
        plt.imshow(np.log(np.abs(imagen_encoded)), cmap='hot') 
        plt.axis('off')
        plt.title('Coeficientes DCT (Escala log)', size=15)
        
        # Imagen reconstruida
        plt.subplot(133)
        plt.imshow(imagen_decoded), plt.axis('off')
        plt.title('Imagen reconstruida (DCT+IDCT)', size=20)
        
        plt.show()

def ejecutar_tests_dwt_encoder():

    archivos = ['bosque.jpg', 'gato.jpg', 'perro.jpg']

    for archivo in archivos:
        print(f"\nAplicando DWT e IDWT a la imagen {archivo}...")

        # Cargar la imagen y convertir a escala de grises
        imagen = rgb2gray(imread(archivo))

        # Aplicar la DWT y la IDWT
        imagen_encoded = first_seminar.DWT_Encoder.encode(imagen)
        imagen_decoded = first_seminar.DWT_Encoder.decode(imagen_encoded)

        # Visualizar la imagen original y la imagen reconstruida
        plt.figure(figsize=(10, 5))
        plt.gray()
        
        # Imagen original
        plt.subplot(121)
        plt.imshow(imagen), plt.axis('off')
        plt.title('Imagen original', size=20)
        
        # Imagen reconstruida
        plt.subplot(122)
        plt.imshow(imagen_decoded), plt.axis('off')
        plt.title('Imagen reconstruida (DWT+IDWT)', size=20)
        
        plt.show()

        # Visualizar la descomposición 2D de la DWT
        titles = ['LL - Aproximación', 'LH - Detalle horizontal', 'HL - Detalle vertical', 'HH - Detalle diagonal']
        LL, (LH, HL, HH) = imagen_encoded
        
        fig = plt.figure(figsize=(12, 3))
        for i, componente in enumerate([LL, LH, HL, HH]):
            ax = fig.add_subplot(1, 4, i + 1)
            ax.imshow(componente, interpolation="nearest", cmap=plt.cm.gray)
            ax.set_title(titles[i], fontsize=10)
            ax.set_xticks([])
            ax.set_yticks([])

        fig.tight_layout()
        plt.show()

class TestDCT_Slides(unittest.TestCase):

    def setUp(self):
        # Tres matrices de prueba adicionales 8x8
        self.matrices = [
            np.array([[1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [1, 2, 3, 4, 5, 6, 7, 8]]),
            
            np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 2, 3, 4, 5, 6, 7],
                      [0, 2, 4, 6, 8, 10, 12, 14],
                      [0, 3, 6, 9, 12, 15, 18, 21],
                      [0, 4, 8, 12, 16, 20, 24, 28],
                      [0, 5, 10, 15, 20, 25, 30, 35],
                      [0, 6, 12, 18, 24, 30, 36, 42],
                      [0, 7, 14, 21, 28, 35, 42, 49]]),
            
            np.array([[255, 255, 255, 255, 255, 255, 255, 255],
                      [255, 0,   0,   0,   0,   0,   0,   0],
                      [255, 255, 0,   0,   0,   0,   0,   0],
                      [255, 255, 255, 0,   0,   0,   0,   0],
                      [255, 255, 255, 255, 0,   0,   0,   0],
                      [255, 255, 255, 255, 255, 0,   0,   0],
                      [255, 255, 255, 255, 255, 255, 0,   0],
                      [255, 255, 255, 255, 255, 255, 255, 0]])
        ]
    
    def test_dct_encoder_slides(self):
        for matriz in self.matrices:
            # DCT usando la implementación de first_seminar (supuestamente tu implementación)
            dct_encoded_scipy = first_seminar.DCT_Encoder.encode(matriz)
                
            dct_encoded_manual = first_seminar.DCT_Encoder_SlidesFormula.encode(matriz)
            dct_decoded_manual = first_seminar.DCT_Encoder_SlidesFormula.decode(dct_encoded_manual)
                
            # Comprobamos si los resultados de la DCT son lo suficientemente cercanos
            np.testing.assert_allclose(dct_encoded_scipy, dct_encoded_manual, atol=1, err_msg=f"Error en DCT para la matriz:\n{matriz}")
            np.testing.assert_allclose(matriz, dct_decoded_manual, atol=1, err_msg=f"Error en IDCT para la matriz:\n{matriz}")


def main():
    while True:
        print("\nSeleccione los tests que desea ejecutar:")
        print("0) Salir")
        print("1) Tests para Color_Translator")
        print("2) Tests para serpentine")
        print("3) Tests para run_lenght")
        print("4) Tests para el cambiador de resolución")
        print("5) Tests para el cambiador a blanco y negro")
        print("6) Tests para el DCT encoder-decoder")
        print("7) Tests para el DWT encoder-decoder")
        print("8) Tests para el DCT encoder-decoder - Versión formula slides (solo matrices)")


        choice = input("\nIngrese el número de la opción deseada: ")

        if choice == '1':
            print("\nEjecutando tests para Color_Translator...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestColorTranslator)
            unittest.TextTestRunner().run(suite)

        elif choice == '2':
            print("\nEjecutando tests para serpentine...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestSerpentine)
            unittest.TextTestRunner().run(suite)

        elif choice == '3':
            print("\nEjecutando tests para run_lenght...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestRunLength)
            unittest.TextTestRunner().run(suite)

        elif choice == '4':
            print("\nEjecutando tests el cambiador de resolución...")
            ejecutar_tests_resolution_changer()

        elif choice == '5':
            print("\nEjecutando tests el cambiador a blanco y negro...")
            ejecutar_tests_bw()
        
        elif choice == '6':
            print("\nEjecutando pruebas de codificación y decodificación DCT...")
            ejecutar_tests_dct_encoder()
        
        elif choice == '7':
            print("\nEjecutando pruebas de codificación y decodificación DWT...")
            ejecutar_tests_dwt_encoder()

        elif choice == '8':
            print("\nEjecutando pruebas de DCT versión slides...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestDCT_Slides)
            unittest.TextTestRunner().run(suite)
        
        elif choice == '0':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")



if __name__ == "__main__":
    main()
