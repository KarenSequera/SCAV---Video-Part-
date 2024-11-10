import unittest
import first_seminar 

# Nota: este codigo ha sido creado con la ayuda de la IA como se menciona en el enunciado
# Se ha tenido que corregir manualmente los resultados esperados ya que en muchos casos eran erroneos
# No se han incluido tests para las funciones de resize y blanco y negro ya que son comandos ffmpeg que visualmente ya se ven que dan buenos 
# resultados.
# Tampoco se han incluido unit tests para las DCT y la DWT ya las las funciones son sacadas de una libreria y además se pueden probar 
# visualmente.

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
import unittest

def main():
    while True:
        print("\nSeleccione los tests que desea ejecutar:")
        print("0) Salir")
        print("1) Tests para Color_Translator")
        print("2) Tests para serpentine")
        print("3) Tests para run_lenght")

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

        elif choice == '0':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
