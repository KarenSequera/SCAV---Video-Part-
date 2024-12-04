from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import os
import json
import app_lab1

app_seminar2 = Flask(__name__)

###############################################################################

##################### SEMINARIO 2

######## NOTA: LOS ENDPOINTS DE ESTE SEMINARIO SE ENCUENTRAN EN EL PUERTO 5001!!!!!!!!!!!

#################### Otros endpoints/funciones útiles

#Endpoint para poder subir archivos a la API
# - Método: Post
# - Input: Archivo en la clave 'file' del formulario web
# - Output:
#            - 400: Si la petición no tienen ningún archivo
#            - 200: Si el archivo se sube correctamente

@app_seminar2.route('/upload', methods=['POST'])
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
    directorio = "../shared_seminar2"
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

#Esta función limpia el directorio shared de contenidos 
def delete_ladder_contents():
    directorio = "../encoding_ladder"
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
#         -Dimensiones en la clave 'data' del formulario web, formato json {"Alto":"100","Ancho":100} :
#               -Ancho: Número de pixeles deseados para el ancho de la imagen
#               -Alto: Número de pixeles deseados para el alto de la imagen
# - Output: Video con las dimensiones deseadas

@app_seminar2.route('/resolution_changer', methods=['POST'])
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
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        # Directorio del output
        output_ffmpeg_path = f"../shared_seminar2/output_{ancho}x{alto}.mp4"

        app_lab1.funcion_resolution_changer(input_ffmpeg_path, output_ffmpeg_path, ancho, alto)

        # Directorio del output
        output_ffmpeg_path = f"../../shared_seminar2/output_{ancho}x{alto}.mp4"
        
        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(output_ffmpeg_path, mimetype='video/mp4', as_attachment=True, download_name=f"video_{ancho}x{alto}.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400


#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
# curl --location "http://localhost:5001/resolution_changer" ^
# --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
# --form "data={\"Alto\":\"100\",\"Ancho\":100}" ^
# --output output_file.mp4


##################### 2)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# -Directorio_output: Directorio relativo del video producido
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

@app_seminar2.route('/chroma_subsampling_changer', methods=['POST'])
def chroma_subsampling_changer():
    delete_share_contents()
    data = json.loads(request.form.get('data'))
    try:
        #Extraer el chroma subsampling al que se desea convertir el video
        tipo_chroma_subsampling = data['Type']
        
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        # Directorio del output
        output_ffmpeg_path = "../shared_seminar2/output_chroma_subsampling.mp4"

        # Transforma el video al formato deseado 
        funcion_chroma_subsampling_changer(input_ffmpeg_path, output_ffmpeg_path, tipo_chroma_subsampling)

        #Adapta al directorio de la aplicación de python
        output_ffmpeg_path = "../../shared_seminar2/output_chroma_subsampling.mp4"
        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(output_ffmpeg_path, mimetype='video/mp4', as_attachment=True, download_name=f"video_chroma_subsampled.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
#curl --location "http://localhost:5001/chroma_subsampling_changer" ^
#--form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
#--form "data={\"Type\":\"yuv420p\"}" ^
#--output output_file.mp4

##################### 3)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# Genera una un json con 5 datos relevantes del video extraidos del comando ffprobe

def funcion_get_information(directorio_input):
    output_file = "../shared_seminar2/output_information.json" 
    
    #Para obtener los 5 datos relevantes del video se formatea el output del comando ffprobe para convertirlo en un json
    # (https://ffmpeg.org/ffprobe.html)
    # grep -E 'format_name|duration|size|bit_rate|encoder' : filtramos por las lineas que contengan esas palabras. 
    # sed '1s/^/{{ /; $s/,$/ }}/' : introduce todo el contenido entre {}
    # tr -d '\\n' : elimina los saltos de linea
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

@app_seminar2.route('/video_info', methods=['POST'])

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
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)
        funcion_get_information(input_ffmpeg_path)

        # Directorio del output
        output_path = f"../../shared_seminar2/output_information.json"
        
        #Se devuelve el json con los datos del video
        return send_file(output_path, mimetype='json', as_attachment=False)

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400


#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
#curl --location "http://localhost:5001/video_info" ^
#--form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
#--output output_file.json

    
##################### 4)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# Genera un video con solo los primeros 20 segundos, se genera en el directorio compartido de los contenedores. 

def video_cut(directorio_input):

    directorio_output_video = "../shared_seminar2/output_20s.mp4"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-ss", "00:00:00", "-i", directorio_input,  "-c", "copy", "-t",  "00:00:20", directorio_output_video]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar video de 20s'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
#Genera una pista de audio aac de solo un canal, se genera en el directorio compartido de los contenedores. 
    
def mp4_to_AAC_mono_track(directorio_input):

    directorio_output_video = "../shared_seminar2/aac_mono_track.aac"
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

    directorio_output_video = "../shared_seminar2/mp4_to_mp3_stereo.mp3"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorio_input, "-acodec", "mp3", "-ac", "2", "-b:a", bitrate, directorio_output_video]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar la pista mp3'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
#Genera una pista de audio con el codec ac3, se genera en el directorio compartido de los contenedores.

def mp4_to_ac3(directorio_input):

    directorio_output_video = "../shared_seminar2/mp4_to_ac3.ac3"
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorio_input, "-acodec", "ac3", directorio_output_video]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al generar la pista ac3'}), 400
    
    
#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
#Genera una pista de audio con el codec ac3, se genera en el directorio compartido de los contenedores.
    
def package(video20s_path, aac_mono_track_path, mp4_to_mp3_stereo_lower_bitrate_path, mp4_to_ac3_path):
    directorio_output_video = "../shared_seminar2/BBC20s_package.mp4"
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
# -Output: Archivo mp4 con el audio en los tres formatos deseados. 

@app_seminar2.route('/video_container_creator', methods=['POST'])
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
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        #Primera parte del ejercicio, cortar el video a 20s
        video_cut(input_ffmpeg_path)
        video20s_path = "../shared_seminar2/output_20s.mp4"
     
        #Segunda parte del ejercicio, generar una pista AAC mono
        mp4_to_AAC_mono_track(video20s_path)
        aac_mono_track_path = "../shared_seminar2/aac_mono_track.aac"
        
        #Tercera parte del ejercicio, generar una pista mp3 stereo con el bitrate deseado
        #Extraer del input el bitrate
        bitrate = data['Bitrate']
        mp4_to_mp3_stereo_lower_bitrate(video20s_path, bitrate)
        mp4_to_mp3_stereo_lower_bitrate_path = "../shared_seminar2/mp4_to_mp3_stereo.mp3"

        #Cuarta parte del ejercicio, generar una pista ac3
        mp4_to_ac3(video20s_path)
        mp4_to_ac3_path = "../shared_seminar2/mp4_to_ac3.ac3"

        #Última parte, introducirlo todo en un contenedor mp4
        package(video20s_path, aac_mono_track_path, mp4_to_mp3_stereo_lower_bitrate_path, mp4_to_ac3_path)
        video_final_path = "../../shared_seminar2/BBC20s_package.mp4"

        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(video_final_path, mimetype='video/mp4', as_attachment=True, download_name=f"BBC20s_package.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    

#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
#curl --location "http://localhost:5001/video_container_creator" ^
#--form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
#--form "data={\"Bitrate\":\"32k\"}" ^
#--output output_file.mp4
    
##################### 5)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# Genera una un txt con la información de las pistas de audio, cada linea representa una pista de audio

def get_number_of_tracks(directorio_input):
    output_file = "../shared_seminar2/number_of_tracks.txt" 

    # Usamos el mismo comando ffprobe que para el ejercicio de los 5 datos del video
    # grep -E 'Stream' | grep -E 'Audio': Esta vez, filtramos por las filas que contienen la palabra "Stream" y despues las que contienen la palabra "Audio"
    command = ["docker", "exec", "contenedor_ffmpeg", "sh", "-c", f"ffprobe -i  {directorio_input} 2>&1 | grep -E 'Stream' | grep -E 'Audio' > {output_file} "]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al extraer la informacion del video'}), 400


#Esta función cuenta las lindeas dentro del archivo txt especificado:
# -Directorio_input: Directorio relativo del video
# Genera una un txt con la información de las pistas de audio, cada linea representa una pista de audio 
def count_lines_txt(directorio_input):
    #fichero = open("../shared_seminar2/number_of_tracks.txt")
    fichero = open(directorio_input)
    return len(fichero.readlines())

#Este endpoint devuelve un json con el número de audio tracks del archivo input
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
# -Output: Json con el número de tracks
@app_seminar2.route('/get_numer_of_tracks', methods=['POST'])

def get_numer_of_tracks():
    delete_share_contents()
    try:
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        # Obtener un .txt con la información de las tracks
        get_number_of_tracks(input_ffmpeg_path)

        # Por cada una de las lineas del .txt hay una track. Hay que contar el número de lineas.
        video_final_path = "../../shared_seminar2/number_of_tracks.txt"
        number_of_tracks = count_lines_txt(video_final_path)

        return jsonify({'Number of tracks': str(number_of_tracks)}), 400

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    

#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
# curl --location "http://localhost:5001/get_numer_of_tracks" ^
# --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
# --output output_file.json

##################### 6)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video 
# Genera una una versión del video con macroblocks y los vectores de movimiento.
def motion_vectors(directorio_input):
    directorio_output = "../shared_seminar2/motion_vectors.mp4"
    #Segun este blog oficial de ffmpeg: https://trac.ffmpeg.org/wiki/Debug/MacroblocksAndMotionVectors
    #La opción de analizar los macroblock ha sido quitada en las versiones más recientes de ffmpeg. 
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-flags2", "+export_mvs", "-i", directorio_input,"-vf", "codecview=mv=pf+bf+bb", directorio_output ]
    try: 
        subprocess.run(command, check=True)
    except:
         return jsonify({'Error': 'Error al generar el video con los motion vectors'}), 400

#Esta función genera una una versión del video con macroblocks y los vectores de movimiento:
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
# - Output: Video con los vectores de movimiento y los macroblocks
@app_seminar2.route('/motion_vectors_macroblocks', methods=['POST'])
def motion_vectors_macroblocks():
    delete_share_contents()
    try:
    
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        # Transforma el video al formato deseado 
        motion_vectors(input_ffmpeg_path)

        directorio_output = "../../shared_seminar2/motion_vectors.mp4"
        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(directorio_output, mimetype='video/mp4', as_attachment=True, download_name=f"video_motion_vectors_macroblocks.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    

#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
# curl --location "http://localhost:5001/motion_vectors_macroblocks" ^
#  --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
#  --output output_file.mp4
    
##################### 7)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# Genera un video con los histogramas YUV del video input
def histogram_creator(directorio_input):
    directorio_output = "../shared_seminar2/histograms.mp4" 
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorio_input, "-vf", "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay", directorio_output]
    try: 
        subprocess.run(command, check=True)
    except:
         return jsonify({'Error': 'Error al generar el video con los histogramas YUV'}), 400

#Esta función genera un video con los histogramas YUV del video pasado como input:
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
# - Output: Video con los histogramas YUV del video input
@app_seminar2.route('/YUV_histograms', methods=['POST'])
def YUV_histograms():
    delete_share_contents()
    try:
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        # Transforma el video al formato deseado 
        histogram_creator(input_ffmpeg_path)

        directorio_output = "../../shared_seminar2/histograms.mp4"
        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(directorio_output, mimetype='video/mp4', as_attachment=True, download_name=f"video_histograms.mp4")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

### Se recomienda hacer desde postman! Curl no recibe bien este archivo. 
#### Ejemplo de petición, curl (cambiar localización del archivo) para la CMD de Windows: 
# curl --location "http://localhost:5001/YUV_histograms" ^
#    --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
#    --output output_file.mp4

###############################################################################

##################### Lab 2 

##################### 1)

#Esta función genera un comando de ffmpeg que dado:
# -Directorio_input: Directorio relativo del video
# -Codec: Codec deseado para el video de output
# Genera un video en el codec deseado
def video_convert(directorio_input, codec):
    directorio_output = f"../shared_seminar2/video_{codec}.mkv" 

    if codec == "vp8" or codec == "VP8":
        command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", directorio_input, "-c:v", "libvpx", directorio_output]
        try: 
            subprocess.run(command, check=True)
        except:
            return jsonify({'Error': 'Error al generar el video'}), 400
        
    elif codec == "vp9" or codec == "VP9":
        command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", directorio_input, "-c:v", "libvpx-vp9", directorio_output]
        try: 
            subprocess.run(command, check=True)
        except:
            return jsonify({'Error': 'Error al generar el video'}), 400
        
    elif codec == "h265" or codec == "H265":
        command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", directorio_input, "-c:v", "libx265", directorio_output]
        try: 
            subprocess.run(command, check=True)
        except:
            return jsonify({'Error': 'Error al generar el video'}), 400
        
    elif codec == "av1" or codec == "AV1":
        #El encoder 'libaom-av1' es experimental para usarlo hay que poner las flags '-strict -2'
        command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", directorio_input,"-c:v", "libaom-av1","-strict", "experimental", directorio_output]
        try: 
            subprocess.run(command, check=True)
        except:
            return jsonify({'Error': 'Error al generar el video'}), 400
    else:
         return jsonify({'Error': 'Codec no valido'}), 400 
    
#Esta función genera un video en el formato especificado: VP8, VP9, h256 o AV1:
# -Método: Post
# -Input:
#         -Archivo input en la clave 'file' del formulario web
#         -Codec deseado para el video en la clave 'data', formato json: {"Codec":"VP8"}
# - Output: Video  en el codec especificado
@app_seminar2.route('/video_codec_converter', methods=['POST'])
def video_codec_converter():
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
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        codec = data['Codec']
        # Transforma el video al formato deseado 
        video_convert(input_ffmpeg_path,codec)

        directorio_output = f"../../shared_seminar2/video_{codec}.mkv"
        #Se devuelve el archivo que ha producido ffmpeg
        return send_file(directorio_output, mimetype='video/mp4', as_attachment=True, download_name=f"video_{codec}.mkv")

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400


##################### 1)

def encoding_ladder_videos(directorio_input):
    resoluciones = [[640,360],[1280,720],[1920,1080],[2560,1140]]

    for i in resoluciones:
        ancho = i[0]
        alto = i[1]
        directorio_output = f"../shared_seminar2/video_{ancho}x{alto}.mp4" 
        app_lab1.funcion_resolution_changer(directorio_input, directorio_output, ancho, alto)

def encoding_ladder_master():
    delete_ladder_contents()
    resoluciones = [[640,360],[1280,720],[1920,1080],[2560,1140]]
    master_path = '../encoding_ladder/master_%v.m3u8' 
    directorios = [f"../shared_seminar2/video_{i[0]}x{i[1]}.mp4" for i in resoluciones]
    command = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", directorios[0], "-i", directorios[1],"-i", directorios[2],"-i", directorios[3],
               "-map", "0:v", "-map", "1:v", "-map", "2:v", "-map", "3:v",
            "-map", "0:a", "-map", "0:a", "-map", "0:a", "-map", "0:a",
            "-c:v", "copy", "-c:a", "copy",
            "-f", "hls", "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3",
            "-hls_time", "10", "-hls_playlist_type", "vod",
            "-master_pl_name", "master.m3u8", master_path]
    try: 
        subprocess.run(command, check=True)        
    except:
        return jsonify({'Error': 'Error al generar el video'}), 400
        


@app_seminar2.route('/encoding_ladder_creator', methods=['POST'])
def encoding_ladder_creator():
    delete_share_contents()
    try:
        #Extraer el archivo de la petición POST
        if 'file' not in request.files:
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "La petición no tiene ningún archivo"}), 400
        
        # Guardar el archivo dentro de la carpeta shared para que ffmpeg pueda acceder a el
        input_ffmpeg_path = f"../shared_seminar2/{file.filename}"
        file.save(input_ffmpeg_path)

        # Transforma el video al formato deseado 
        encoding_ladder_videos(input_ffmpeg_path)
        encoding_ladder_master()

        #Se devuelve el archivo que ha producido ffmpeg
        return  jsonify({'Output': 'El resultado se encuentra en el /encoding_ladder'}), 400

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app_seminar2.run(host="0.0.0.0", port=5001)
    