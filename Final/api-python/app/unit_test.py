import unittest
import app_lab1
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
from matplotlib import pyplot as plt

# Nota: este codigo ha sido creado con la ayuda de la IA como se menciona en el enunciado
# Se ha tenido que corregir manualmente los resultados esperados ya que en muchos casos eran erroneos

class TestColorTranslator(unittest.TestCase):

    def test_rgb_to_yuv(self):
        translator = app_lab1.Color_Translator()
        # Test con un color RGB (255, 0, 0) que debe dar un color YUV cercano a [81.535, 90.26, 239.945]
        result = translator.metodo_rgb_to_yuv(255, 0, 0)
        self.assertAlmostEqual(result[0], 81.535, delta=1)  # Y
        self.assertAlmostEqual(result[1], 90.26, delta=1)  # U
        self.assertAlmostEqual(result[2], 239.945, delta=1)   # V

    def test_yuv_to_rgb(self):
        translator = app_lab1.Color_Translator()
        # Test con un color YUV (81.535, 90.26, 239.945) que debe dar un color RGB cercano a [255.0, 0.0, 0.0]
        result = translator.metodo_yuv_to_rgb(81.535, 90.26, 239.945)
        self.assertAlmostEqual(result[0], 255.0, delta=1)  # R
        self.assertAlmostEqual(result[1], 0.0, delta=1)    # G
        self.assertAlmostEqual(result[2], 0.0, delta=1)    # B

def run_TestColorTranslator():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestColorTranslator)
    runner = unittest.TextTestRunner(resultclass=unittest.TestResult)
    result = runner.run(suite)

    # Crear una cadena con el resumen de los resultados
    result_string = f"Pruebas ejecutadas: {result.testsRun}\n"
    result_string += f"Pruebas exitosas: {len(result.successes) if hasattr(result, 'successes') else result.testsRun - len(result.failures) - len(result.errors)}\n"
    result_string += f"Fallos: {len(result.failures)}\n"
    result_string += f"Errores: {len(result.errors)}\n"

    if result.failures:
        result_string += "Detalles de los fallos:\n"
        for failed_test, traceback in result.failures:
            result_string += f"{failed_test}: {traceback}\n"
    
    if result.errors:
        result_string += "Detalles de los errores:\n"
        for errored_test, traceback in result.errors:
            result_string += f"{errored_test}: {traceback}\n"
    
    return result_string

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
        result = app_lab1.funcion_serpentine(matriz)
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
        result = app_lab1.funcion_serpentine(matriz)
        self.assertEqual(result, expected_result)

def run_TestSerpentine():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSerpentine)
    runner = unittest.TextTestRunner(resultclass=unittest.TestResult)
    result = runner.run(suite)

    # Crear una cadena con el resumen de los resultados
    result_string = f"Pruebas ejecutadas: {result.testsRun}\n"
    result_string += f"Pruebas exitosas: {len(result.successes) if hasattr(result, 'successes') else result.testsRun - len(result.failures) - len(result.errors)}\n"
    result_string += f"Fallos: {len(result.failures)}\n"
    result_string += f"Errores: {len(result.errors)}\n"

    if result.failures:
        result_string += "Detalles de los fallos:\n"
        for failed_test, traceback in result.failures:
            result_string += f"{failed_test}: {traceback}\n"
    
    if result.errors:
        result_string += "Detalles de los errores:\n"
        for errored_test, traceback in result.errors:
            result_string += f"{errored_test}: {traceback}\n"
    
    return result_string

class TestRunLength(unittest.TestCase):

    def test_run_length(self):
        # Test con una lista que tiene ceros consecutivos
        lista = [1, 0, 0, 2, 0, 0, 0, 3]
        # El resultado esperado debería ser: [1, '02', 2, '03', 3]
        expected_result = [1, '02', 2, '03', 3]
        result = app_lab1.funcion_run_lenght(lista)
        self.assertEqual(result, expected_result)

        # Test con una lista sin ceros
        lista = [1, 2, 3, 4, 5]
        # El resultado debería ser la misma lista ya que no hay ceros
        expected_result = [1, 2, 3, 4, 5]
        result = app_lab1.funcion_run_lenght(lista)
        self.assertEqual(result, expected_result)

        # Test con una lista que solo tiene ceros
        lista = [0, 0, 3, 4, 8, 6, 33, 0, 0, 0, 4]
        # El resultado esperado es: ['02', 3, 4, 8, 6, 33,'03', 4]
        expected_result = ['02', 3, 4, 8, 6, 33,'03', 4]
        result = app_lab1.funcion_run_lenght(lista)
        self.assertEqual(result, expected_result)
    
def run_TestRunLength():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRunLength)
    runner = unittest.TextTestRunner(resultclass=unittest.TestResult)
    result = runner.run(suite)

    # Crear una cadena con el resumen de los resultados
    result_string = f"Pruebas ejecutadas: {result.testsRun}\n"
    result_string += f"Pruebas exitosas: {len(result.successes) if hasattr(result, 'successes') else result.testsRun - len(result.failures) - len(result.errors)}\n"
    result_string += f"Fallos: {len(result.failures)}\n"
    result_string += f"Errores: {len(result.errors)}\n"

    if result.failures:
        result_string += "Detalles de los fallos:\n"
        for failed_test, traceback in result.failures:
            result_string += f"{failed_test}: {traceback}\n"
    
    if result.errors:
        result_string += "Detalles de los errores:\n"
        for errored_test, traceback in result.errors:
            result_string += f"{errored_test}: {traceback}\n"
    
    return result_string

##Para los unit test de las funciones que utilizan ffmpeg simplemente vamos a llamar a las funciones con diferentes imagenes.
def ejecutar_tests_resolution_changer():

    #Nota: El output se guarda en la carpeta unit_test_output_resize, se recomienda eliminar el contenido para que 
    #ffmpeg no pregunte en cada prueba si se deseaa reescribir el contenido. 

    archivos = ['/shared_lab1/unit_tests/bosque.jpg', '/shared_lab1/unit_tests/gato.jpg', '/shared_lab1/unit_tests/perro.jpg']
    resoluciones = [(800, 600), (320, 240), (10,10)]
    
    for archivo in archivos:
        # Extraemos el nombre base del archivo sin la extensión
        if "bosque" in archivo:
            nombre_base = "bosque"
        elif "gato" in archivo:
            nombre_base = "gato"
        elif "perro" in archivo:
            nombre_base = "perro"

        for ancho, alto in resoluciones:
            # Nombre de salida específico para cada imagen redimensionada
            output_name = f'/shared_lab1/unit_tests/resize/output_{nombre_base}_{ancho}x{alto}.jpg'

            # Llamada a la función que cambia la resolución
            app_lab1.funcion_resolution_changer(archivo, output_name, ancho, alto)


def ejecutar_tests_bw():

    #Nota: El output se guarda en la carpeta unit_test_bw, se recomienda eliminar el contenido para que 
    #ffmpeg no pregunte en cada prueba si se deseaa reescribir el contenido. 
    
    archivos = ['/shared_lab1/unit_tests/bosque.jpg', '/shared_lab1/unit_tests/gato.jpg', '/shared_lab1/unit_tests/perro.jpg']    

    for archivo in archivos:
    
        # Determinamos el nombre base del archivo (bosque, gato, perro)
        if "bosque" in archivo:
            nombre_base = "bosque"
        elif "gato" in archivo:
            nombre_base = "gato"
        elif "perro" in archivo:
            nombre_base = "perro"

        # Nombre de salida específico para cada archivo transformado
        output_name = f'/shared_lab1/unit_tests/bw/output_{nombre_base}.jpg'

        # Llamada a la función que convierte la imagen a blanco y negro
        app_lab1.funcion_bw_converter(archivo, output_name)


def ejecutar_tests_dct_encoder():

    # Directorio de salida (opcional, si deseas guardar resultados)

    archivos = ['/shared_lab1/unit_tests/bosque.jpg', '/shared_lab1/unit_tests/gato.jpg', '/shared_lab1/unit_tests/perro.jpg']

    for archivo in archivos:
        # Determinamos el nombre base del archivo (bosque, gato, perro)
        if "bosque" in archivo:
            nombre_base = "bosque"
        elif "gato" in archivo:
            nombre_base = "gato"
        elif "perro" in archivo:
            nombre_base = "perro"

        # Cargar la imagen y convertir a escala de grises
        imagen = rgb2gray(imread(archivo))

        # Aplicar la DCT y la IDCT
        imagen_encoded = app_lab1.DCT_Encoder_Class.metodo_encode(imagen)
        imagen_decoded = app_lab1.DCT_Encoder_Class.metodo_decode(imagen_encoded)

        # Visualizar las imágenes: original, coeficientes DCT (en escala log), y la imagen reconstruida

        #En el lab anterior haciamos plots de las imagenes, docker no tiene acceso a la pantalla asi que no podemos realizarlos
        #En su lugar, los resultados se guardaran en la carpeta compartida
        #Código para mostrar las imagenes
        plt.figure(figsize=(15, 5))
        plt.gray()
        plt.subplot(131), plt.imshow(imagen), plt.axis('off'), plt.title('Imagen original', size=20)
        #Visualizamos la magnitud de la dct de manera logaritmica 
        plt.subplot(132), plt.imshow(np.log(np.abs(imagen_encoded),),cmap='hot'), plt.axis('off'), plt.title('Coeficientes DCT (Escala log)', size=15)
        plt.subplot(133), plt.imshow(imagen_decoded), plt.axis('off'), plt.title('Imagen reconstruida (DCT+IDCT)', size=20)

        #En lugar de plt.show(), guardamos el grafico
        plt.savefig(f'/shared_lab1/unit_tests/DCT/outputDCT_{nombre_base}.png', bbox_inches='tight')
        plt.close()
    

def ejecutar_tests_dwt_encoder():

    archivos = ['/shared_lab1/unit_tests/bosque.jpg', '/shared_lab1/unit_tests/gato.jpg', '/shared_lab1/unit_tests/perro.jpg']
    for archivo in archivos:
        if "bosque" in archivo:
            nombre_base = "bosque"
        elif "gato" in archivo:
            nombre_base = "gato"
        elif "perro" in archivo:
            nombre_base = "perro"

        # Cargar la imagen y convertir a escala de grises
        imagen = rgb2gray(imread(archivo))

        # Aplicar la DWT y la IDWT
        imagen_encoded = app_lab1.DWT_Encoder_Class.metodo_encode(imagen)
        imagen_decoded = app_lab1.DWT_Encoder_Class.metodo_decode(imagen_encoded)

        #Código para mostrar las imagenes
        plt.figure(figsize=(15, 5))
        plt.gray()
        plt.subplot(121), plt.imshow(imagen), plt.axis('off'), plt.title('Imagen original', size=20)
        plt.subplot(122), plt.imshow(imagen_decoded), plt.axis('off'), plt.title('Imagen reconstruida (DWT+IDWT)', size=20)

        #En lugar de plt.show(), guardamos el grafico
        plt.savefig(f'/shared_lab1/unit_tests/DWT/outputDWT{nombre_base}.png', bbox_inches='tight')
        plt.close()

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
        plt.savefig(f'/shared_lab1/unit_tests/DWT/DWT_decomposición{nombre_base}.png', bbox_inches='tight')
        plt.close()
        
