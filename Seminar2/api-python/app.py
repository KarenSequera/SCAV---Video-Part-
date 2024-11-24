from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json
import numpy as np
from scipy.fftpack import dct, idct
import pywt
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import unit_test

app = Flask(__name__)

###############################################################################
##################### LAB 1

## RGB to YUV

class Color_Translator:
    #Los dos metodos asumen que el input es correcto (float)

    #Método para obtener el color en sistema YUV dado RGB, usa la formula proporcionada en las slides.
    # -Y: Float conteniendo el valor Y del sistema YUV.
    # -U: Float conteniendo el valor U del sistema YUV.
    # -V: Float conteniendo el valor V del sistema YUV. 
    @staticmethod
    def metodo_rgb_to_yuv(R,G,B):
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
    def metodo_yuv_to_rgb(Y,U,V):
        R = 1.164 * (Y - 16) + 1.596 * (V - 128)
        G = 1.164 * (Y - 16) - 0.813 * (V - 128) - 0.391 * (U - 128)
        B = 1.164 * (Y - 16) + 2.018 * (U - 128)

        #El color RGB se devuelve en una lista
        return [R,G,B]

@app.route('/rgb_to_yuv', methods=['POST'])
def rgb_to_yuv():
    data = request.get_json()    

    try:
        R = data['R']
        G = data['G']
        B = data['B']

        [Y,U,V] = Color_Translator.metodo_rgb_to_yuv(R,G,B)
    
        #El color YUV se devuelve en una lista
        return jsonify({
            'Y': Y,
            'U': U,
            'V': V
        })
    
    except KeyError as e:
        return jsonify({'error': f'Falta Parametro: {e}'}), 400
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/rgb_to_yuv -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"R":255,"G":100,"B":50}' -ContentType "application/json"

## YUV to RBG
@app.route('/yuv_to_rgb', methods=['POST'])
def yuv_to_rgb():
    data = request.get_json()    

    try:
        Y = data['Y']
        U = data['U']
        V = data['V']
    
        [R,G,B] = Color_Translator.metodo_yuv_to_rgb(Y,U,V) 

        return jsonify({
            'R': R,
            'G': G,
            'B': B
        })

    except KeyError as e:
        return jsonify({'error': f'Falta Parametro: {e}'}), 400
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/yuv_to_rgb -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Y":128,"U":128,"V":128}' -ContentType "application/json"

##############################################

# Esta función lee la matriz siguiendo el orden "Serpentine" establecido en las slides de clase
# -Matriz: Se asume que es una Lista de Listas (matriz)
# -output: Contiene el contenido de la matriz en orden "serpentine"
def funcion_serpentine(matriz):
    
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

@app.route('/serpentine', methods=['POST'])
def serpentine():
    data = request.get_json() 
    try:
        matriz = data['Matriz']   
        output = funcion_serpentine(matriz)

        return jsonify({
            'Output': output,
        })

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/serpentine -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Matriz":[[1,2,6,7,14],[3,5,8,13,15],[4,9,12,16,19],[10,11,17,18,20]]}' -ContentType "application/json"

##############################################

#Esta función implementa el run_lenght algoritmo presentado en las slides
# - List: lista conteniendo el data stream al que se le desea aplicar el algoritmo
# - output_list: Lista conteniendo el resultado. Las posiciones que contienen 0+Count, son strings.
def funcion_run_lenght(list):
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

@app.route('/run_lenght', methods=['POST'])
def run_lenght():
    data = request.get_json() 
    try:
        list = data['Data_stream']  
        output_list = funcion_run_lenght(list)
        
        return jsonify({
            'Output': output_list,
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo    
#Invoke-WebRequest -Uri http://localhost:5000/run_lenght -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Data_stream":[0, 0, 3, 4, 8, 6, 33, 0, 0, 0, 4]}' -ContentType "application/json"

##############################################

# -Directorio_input: Directorio relativo de la imagen de entrada
# -Directorio_output: Directorio relativo de la imagen de salida
# Genera una versión en blanco y negro de la imagen en el directorio del output
def funcion_bw_converter(directorio_input, directorio_output):
    #Construcción de una lista de strings conteniendo el comando
        command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg","-y", "-i", directorio_input , "-vf", "format=gray", directorio_output]
        try: 
            subprocess.run(command, check=True)
        except:
            return jsonify({'Error': 'Asegurate de que el archivo de output no existe!'}), 400

@app.route('/bw_converter', methods=['POST'])
def bw_converter():
    data = request.get_json() 
    try:
        #Las imagenes tienen que estar localizadas en el directorio "shared", si no los contenedores no serán capaces de acceder a ellas
        nombre_input = data['Nombre Input']
        nombre_output =  data['Nombre Output'] 
        
        directorio_input = "/shared/" + nombre_input
        directorio_output = "/shared/" + nombre_output

        funcion_bw_converter(directorio_input,directorio_output)
        
        return jsonify({
            'Msj': f"La imagen en blanco y negro se encuentra en {directorio_output}",
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo,
#Invoke-WebRequest -Uri http://localhost:5000/bw_converter -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg", "Nombre Output": "output_bw.jpg"}' -ContentType "application/json"

##############################################

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo de la imagen
# -Directorio_output: Directorio relativo de la imagen producida
# -Ancho: Número de pixeles deseados para el ancho de la imagen
# -Alto: Número de pixeles deseados para el alto de la imagen
# Genera una imagen con las dimensiones deseadas en el directorio introducido
def funcion_resolution_changer(directorio_input, directorio_output, ancho, alto):
    #Construcción de una lista de strings conteniendo el comando
    # la opcion "y" hace que no pregunte si deseas substituir el directorio que ya existe. 
        command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", directorio_input , "-vf", f"scale={ancho}:{alto}", directorio_output]
        try: 
            subprocess.run(command, check=True)
        except:
            return jsonify({'Error': 'Asegurate de que el archivo de output no existe!'}), 400

#Comentado porque en el Seminario 2, se hace una version mejorada
# @app.route('/resolution_changer_', methods=['POST'])
# def resolution_changer():
#     data = request.get_json() 
#     try:
#         #Las imagenes tienen que estar localizadas en el directorio "shared", si no los contenedores no serán capaces de acceder a ellas
#         nombre_input = data['Nombre Input']
#         nombre_output =  data['Nombre Output'] 
#         alto = data['Alto']
#         ancho = data['Ancho']

#         directorio_input = "/shared/" + nombre_input
#         directorio_output = "/shared/" + nombre_output
        
#         funcion_resolution_changer(directorio_input, directorio_output, ancho, alto)
        
#         return jsonify({
#             'Msj': f"La imagen con resolucion {ancho}x{alto} se encuentra en {directorio_output}",
#         })
        
#     except (ValueError, TypeError) as e:
#         return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/resolution_changer -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg", "Nombre Output": "output_resolution_changer.jpg", "Alto": 10, "Ancho": 10}' -ContentType "application/json"

##############################################

class DCT_Encoder_Class:
    #Nuestro encoder usa la implementación de la DCT y la IDCT de la libreria scipy.fftpack siguiendo un ejemplo de uso de
    #Stack Overflow para imagenes
    
    #Referencias: https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html
    #             https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.idct.html
    #             https://stackoverflow.com/questions/7110899/how-do-i-apply-a-dct-to-an-image-in-python

    #Función para calcular la DCT
    @staticmethod
    def metodo_encode(imagen):
        return dct(dct(imagen.T, norm='ortho').T, norm='ortho')
    #Función para calcular la IDCT
    @staticmethod
    def metodo_decode(imagen):
        return idct(idct(imagen.T, norm='ortho').T, norm='ortho')
    

@app.route('/dct_encoder', methods=['POST'])
def dct_encoder():
    data = request.get_json() 
    try:
        #Las imagenes tienen que estar localizadas en el directorio "shared", si no los contenedores no serán capaces de acceder a ellas
        nombre_input = data['Nombre Input']

        directorio_input = "/shared/" + nombre_input
        directorio_output = "/shared/DCT/"
        imagen = (rgb2gray(imread(directorio_input)))
        imagen_encoded = DCT_Encoder_Class.metodo_encode(imagen)
        imagen_decoded = DCT_Encoder_Class.metodo_decode(imagen_encoded)
        
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
        plt.savefig(f'{directorio_output}outputDCT.png', bbox_inches='tight')
        plt.close() 

        return jsonify({
            'Msj': f"El resultado se encuenta en el directorio{directorio_output}",
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/dct_encoder -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg"}' -ContentType "application/json"

##############################################

class DWT_Encoder_Class:
    #Nuestro encoder usa la implementación de la DWT y la IDWT de la libreria pwt siguiendo un ejemplo de uso de
    #para imagenes de un blog de la propia libreria.
    
    #Referencias: https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html
    #             https://pywavelets.readthedocs.io/en/latest/

     #Función para calcular la DWT
    @staticmethod
    def metodo_encode(imagen):
        return pywt.dwt2(imagen, 'bior1.3')
    
    #Función para calcular la IDWT
    @staticmethod
    def metodo_decode(imagen):
        return pywt.idwt2(imagen, 'bior1.3')

@app.route('/dwt_encoder', methods=['POST'])
def dwt_encoder():
    data = request.get_json()
    try:
        nombre_input = data['Nombre Input']

        directorio_input = "/shared/" + nombre_input
        directorio_output = "/shared/DWT/"
        imagen = (rgb2gray(imread(directorio_input)))
    
        imagen_encoded = DWT_Encoder_Class.metodo_encode(imagen)
        imagen_decoded = DWT_Encoder_Class.metodo_decode(imagen_encoded)

        #Código para mostrar las imagenes
        plt.figure(figsize=(15, 5))
        plt.gray()
        plt.subplot(121), plt.imshow(imagen), plt.axis('off'), plt.title('Imagen original', size=20)
        plt.subplot(122), plt.imshow(imagen_decoded), plt.axis('off'), plt.title('Imagen reconstruida (DWT+IDWT)', size=20)

        #En lugar de plt.show(), guardamos el grafico
        plt.savefig(f'{directorio_output}outputDWT.png', bbox_inches='tight')
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
        plt.savefig(f'{directorio_output}DWT_decomposición.png', bbox_inches='tight')
        plt.close()

        return jsonify({
            'Msj': f"El resultado se encuenta en el directorio{directorio_output}",
        })
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/dwt_encoder -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg"}' -ContentType "application/json"

##############################################

@app.route('/run_tests', methods=['GET'])
def run_tests_endpoint():
    results = {}

    # Tests con modulo unittest
    try:
        # Ejecutar los unit tests y recoger resultados como strings
        results['TestColorTranslator'] = unit_test.run_TestColorTranslator()
        results['TestSerpentine'] = unit_test.run_TestSerpentine()
        results['TestRunLength'] = unit_test.run_TestRunLength()
    except Exception as e:
        results['unit_test_error'] = f"Error while running unit tests: {str(e)}"

    # Tests manuales con imágenes
    try:

        # Directorio donde se almacenan los resultados
        resolution_changer_dir = '/shared/unit_tests/resize'
        bw_converter_dir = '/shared/unit_tests/bw'
        dct_dir = '/shared/unit_tests/DCT'
        dwt_dir = '/shared/unit_tests/DWT'

        # Ejecutar los tests de imagen
        unit_test.ejecutar_tests_resolution_changer()
        unit_test.ejecutar_tests_bw()
        unit_test.ejecutar_tests_dct_encoder()
        unit_test.ejecutar_tests_dwt_encoder()

        # Agregar resultados de los directorios
        results['ResolutionChanger'] = f"Output files in: {resolution_changer_dir}"
        results['BWConverter'] = f"Output files in: {bw_converter_dir}"
        results['DCTEncoder'] = f"Output files in: {dct_dir}"
        results['DWTEncoder'] = f"Output files in: {dwt_dir}"

    except Exception as e:
        results['image_test_error'] = f"Error while running image tests: {str(e)}"

    return jsonify(results)

#Comando de powershell para obtener el JSON con los resultados de los unit tests. 
# Invoke-WebRequest -Uri http://localhost:5000/run_tests -Method GET -Headers @{ "Content-Type" = "application/json" } | Out-File -FilePath .\test_results.txt


###############################################################################

##################### SEMINARIO 2

#################### Otros

#Endpoint para poder subir archivos a la API
# - Método: Post
# - Input: Archivo en la clave 'file' del formulario web
# - Output:
#            - 400: Si la petición no tienen ningún archivo
#            - 200: Si el archivo se sube correctamente

@app.route('/upload', methods=['POST'])
def upload_video():

    if 'file' not in request.files:
        return jsonify({"error": "La petición no tiene ningún archivo"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "La petición no tiene ningún archivo"}), 400

    # Guardar el archivo dentro de la carpeta uploads
    save_path = f"../uploads/{file.filename}"
    file.save(save_path)
    
    return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200


#Esta función limpia el directorio shared de contenidos 
def delete_share_contents():
    directorio = "../shared"
    #Iterar por los archivos del directorio
    for archivo in os.listdir(directorio):
        #Obtiene el directorio completo y los elimina
        ruta_completa = os.path.join(directorio, archivo)
        os.remove(ruta_completa) 

#Esta función limpia el directorio shared de contenidos 
def delete_uploads_contents():
    directorio = "../uploads"
    #Iterar por los archivos del directorio
    for archivo in os.listdir(directorio):
        #Obtiene el directorio completo y los elimina
        ruta_completa = os.path.join(directorio, archivo)
        os.remove(ruta_completa) 

##################### 1)

#Esta función cambia la resolución del video envíado:
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
#         -Dimensiones en la clave 'data' del formulario web, formato json:
#               -Ancho: Número de pixeles deseados para el ancho de la imagen
#               -Alto: Número de pixeles deseados para el alto de la imagen
# - Output: Video con las dimensiones deseadas

@app.route('/resolution_changer', methods=['POST'])
def resolution_changer():
    delete_share_contents()
    data = json.loads(request.form.get('data'))
    try:
        #Extraer la resolución a la que se desea convertir el video
        alto = data['Alto']
        ancho = data['Ancho']

        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared/{file.filename}"
        file.save(input_ffmpeg_path)

        # Directorio del output
        output_ffmpeg_path = f"../shared/output_{ancho}x{alto}.mp4"

        funcion_resolution_changer(input_ffmpeg_path, output_ffmpeg_path, ancho, alto)

        # Eliminar el archivo subido después de procesarlo
        os.remove(input_ffmpeg_path)

        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(output_ffmpeg_path, mimetype='video/mp4', as_attachment=True, download_name=f"video_{ancho}x{alto}.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

##################### 2)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# -Directorio_output: Directorio relativo del video producida
# -Tipo: Tipo de chroma subsampling, ej. yuv420p
# Genera una imagen con las dimensiones deseadas en el directorio introducido
def funcion_chroma_subsampling_changer(directorio_input, directorio_output, tipo_chroma_subsampling):
    
    #Construcción de una lista de strings conteniendo el comando
    # la opcion "y" hace que no pregunte si deseas substituir el directorio que ya existe. 
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", directorio_input , "-c:v", "libx265",  "-vf", f"format={tipo_chroma_subsampling}", directorio_output]

    try: 
        subprocess.run(command, check=True)
    except:
         return jsonify({'Error': 'Ese tipo de chroma subsampling no esta disponible'}), 400

#Esta función cambia el chroma subsampling del video envíado:
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
#         -Tipo de Chroma subsampling en la clave 'data' del formulario web, formato json: {"Type":"yuv420p"}
#               -Type: Por ejemplo: yuv420p, yuv422p, yuv444p, yuv420p10le, yuv422p10le, yuv444p10le
# - Output: Video con las dimensiones deseadas

@app.route('/chroma_subsampling_changer', methods=['POST'])
def chroma_subsampling_changer():
    delete_share_contents()
    data = json.loads(request.form.get('data'))
    try:
        #Extraer la resolución a la que se desea convertir el video
        tipo_chroma_subsampling = data['Type']
        
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared/{file.filename}"
        file.save(input_ffmpeg_path)

        # Directorio del output
        output_ffmpeg_path = f"../shared/output_chroma_subsampling.mp4"

        # Transforma el video al formato deseado 
        funcion_chroma_subsampling_changer(input_ffmpeg_path, output_ffmpeg_path, tipo_chroma_subsampling)

        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(output_ffmpeg_path, mimetype='video/mp4', as_attachment=True, download_name=f"video_chroma_subsampled.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

##################### 3)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# Genera una un json con 5 datos relevantes del video extraidos del comando ffprobe

def funcion_get_information(directorio_input):
    output_file = "../shared/output_information.json" 
    
    #Para obtener los 5 datos relevantes del video se formatea el output del comando ffprobe para convertirlo en un json
    # (https://ffmpeg.org/ffprobe.html)
    # grep -E 'format_name|duration|size|bit_rate|encoder' : filtramos por las lineas que contengan esas palabras. 
    # sed '1s/^/{{ /; $s/,$/ }}/' : introduce todo el contenido entre {}
    # tr -d '\\n' : elimina los santos de linea
    # sed 's/, /,/g' elima los espacios despues de las comas
    # Por último se redirige el output formateado a un archivo json
    command = ["docker", "exec", "contenedor_ffmpeg", "sh", "-c", f"ffprobe -v quiet -print_format json -show_format  {directorio_input} | grep -E 'format_name|duration|size|bit_rate|encoder'  | sed '1s/^/{{ /; $s/,$/ }}/' | tr -d '\\n' | sed 's/, /,/g'> {output_file} 2>&1"]
        
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al extraer la informacion del video'}), 400
        
        

#Este endpoint devuelve un json con 5 caracteristicas del video introducido:
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
# -Output: Json con los datos: format_name, duration, size, bit_rate y encoder

@app.route('/video_info', methods=['POST'])

def video_info():
    delete_share_contents()
    try:
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared/{file.filename}"
        file.save(input_ffmpeg_path)
        funcion_get_information(input_ffmpeg_path)

        # Directorio del output
        output_path = f"../shared/output_information.json"
        

        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(output_path, mimetype='json', as_attachment=False)

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
##################### 4)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# Genera un video con solo los primeros 20 segundos, se genera en el directorio compartido de los contenedores. 

def video_cut(directorio_input):

    directorio_output_video = "../shared/output_20s.mp4"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-ss", "00:00:00", "-i", directorio_input,  "-c", "copy", "-t",  "00:00:20", directorio_output_video]
    
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar video de 20s'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
#Genera una pista de audio aac de solo un canal, se genera en el directorio compartido de los contenedores. 
    
def mp4_to_AAC_mono_track(directorio_input):

    directorio_output_video = "../shared/aac_mono_track.aac"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorio_input, "-acodec", "aac", "-ac", "1", directorio_output_video]

    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar la pista aac'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# -Bitrate: Bitrate de la nueva pista
#Genera una pista de audio mp3 estereo con el bitrate espeficicado, se genera en el directorio compartido de los contenedores.

def mp4_to_mp3_stereo_lower_bitrate(directorio_input, bitrate):

    directorio_output_video = "../shared/mp4_to_mp3_stereo.mp3"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorio_input, "-acodec", "mp3", "-ac", "2", "-b:a", bitrate, directorio_output_video]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar la pista mp3'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
#Genera una pista de audio con el codec ac3, se genera en el directorio compartido de los contenedores.

def mp4_to_ac3(directorio_input):
    directorio_output_video = "../shared/mp4_to_ac3.ac3"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorio_input, "-acodec", "ac3", directorio_output_video]

    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar la pista ac3'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
#Genera una pista de audio con el codec ac3, se genera en el directorio compartido de los contenedores.
    
def package(video20s_path, aac_mono_track_path, mp4_to_mp3_stereo_lower_bitrate_path, mp4_to_ac3_path):
    directorio_output_video = "../shared/BBC20s_package.mp4"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", video20s_path, "-i", aac_mono_track_path, 
               "-i", mp4_to_mp3_stereo_lower_bitrate_path, "-i", mp4_to_ac3_path, "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a", "-c:v", 
               "copy", "-c:a",  "copy", directorio_output_video]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar el contenedor mp4'}), 400
    

# Este endpoint genera un contenedor mp4 que contiene una version de 20 segundos del video subido y el audio en tres formatos diferentes: aac mono,
# mp3 estereo con el bitrate especificado, aac3.  
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
#         -Bitrate deseado para la pista mp3 estereo en la clave 'data', formato json: {"Bitrate":"32k"}
# -Output: Json con los datos: format_name, duration, size, bit_rate y encoder

@app.route('/video_container_creator', methods=['POST'])
def video_container_creator():
    delete_share_contents()
    data = json.loads(request.form.get('data'))
    try:
       
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared/{file.filename}"
        file.save(input_ffmpeg_path)

        #Primera parte del ejercicio, cortar el video a 20s
        video_cut(input_ffmpeg_path)
        video20s_path = "../shared/output_20s.mp4"
     
        #Segunda parte del ejercicio, generar una pista AAC mono
        mp4_to_AAC_mono_track(video20s_path)
        aac_mono_track_path = "../shared/aac_mono_track.aac"
        
        #Tercera parte del ejercicio, generar una pista mp3 stereo con el bitrate deseado
        #Extraer del input el bitrate
        bitrate = data['Bitrate']
        mp4_to_mp3_stereo_lower_bitrate(video20s_path, bitrate)
        mp4_to_mp3_stereo_lower_bitrate_path = "../shared/mp4_to_mp3_stereo.mp3"

        #Cuarta parte del ejercicio, generar una pista ac3
        mp4_to_ac3(video20s_path)
        mp4_to_ac3_path = "../shared/mp4_to_ac3.ac3"

        #Última parte, introducirlo todo en un contenedor mp4
        package(video20s_path, aac_mono_track_path, mp4_to_mp3_stereo_lower_bitrate_path, mp4_to_ac3_path)
        video_final_path = "../shared/BBC20s_package.mp4"

        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(video_final_path, mimetype='video/mp4', as_attachment=True, download_name=f"BBC20s_package.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    