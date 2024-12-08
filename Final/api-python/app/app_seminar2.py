from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json
from flask_cors import CORS

################## CODIGO CORREGIDO DE LA IA

# Importar las funcionalidades del primer laboratorio
import app_lab1

# Inicialización de la aplicación
app_seminar2 = Flask(__name__)
CORS(app_seminar2)

# Configuración
UPLOAD_DIR = "../uploads"
SHARED_DIR = "../shared_seminar2"
ENCODING_LADDER_DIR = "../encoding_ladder"

# Utilidades generales
def clean_directory(directory):
    """Limpia todos los archivos dentro del directorio especificado."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))

def save_file_from_request(request_key, save_path):
    """Guarda un archivo enviado en una solicitud POST."""
    if request_key not in request.files:
        raise ValueError("La petición no contiene el archivo requerido.")

    file = request.files[request_key]
    if file.filename == '':
        raise ValueError("El archivo enviado está vacío.")

    file.save(save_path)
    return save_path

def get_json_from_request(request_key):
    """Obtiene un JSON desde los datos del formulario en la solicitud POST."""
    raw_data = request.form.get(request_key)
    if not raw_data:
        raise ValueError("La petición no contiene los datos requeridos.")
    return json.loads(raw_data)

def adjust_output_path(shared_path):
    """Convierte la ruta de salida desde el contenedor Docker al servidor Python."""
    return shared_path.replace("../shared_seminar2", "../../shared_seminar2")

# Endpoints
@app_seminar2.route('/upload', methods=['POST'])
def upload_video():
    try:
        save_path = save_file_from_request('file', os.path.join(UPLOAD_DIR, request.files['file'].filename))
        return jsonify({"message": f"Archivo {os.path.basename(save_path)} subido exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app_seminar2.route('/resolution_changer', methods=['POST'])
def resolution_changer():
    clean_directory(SHARED_DIR)
    try:
        # Procesar entrada
        data = get_json_from_request('data')
        width, height = data['Ancho'], data['Alto']

        input_path = save_file_from_request('file', os.path.join(SHARED_DIR, request.files['file'].filename))
        output_path = os.path.join(SHARED_DIR, f"output_{width}x{height}.mp4")

        # Llamar la función para cambiar la resolución
        app_lab1.funcion_resolution_changer(input_path, output_path, width, height)

        # Ajustar la ruta de salida para la respuesta
        adjusted_output_path = adjust_output_path(output_path)

        # Devolver archivo procesado
        return send_file(adjusted_output_path, mimetype='video/mp4', as_attachment=True, download_name=f"video_{width}x{height}.mp4")
    except (ValueError, KeyError) as e:
        return jsonify({'error': str(e)}), 400

@app_seminar2.route('/chroma_subsampling_changer', methods=['POST'])
def chroma_subsampling_changer():
    clean_directory(SHARED_DIR)
    try:
        # Procesar entrada
        data = get_json_from_request('data')
        chroma_type = data['Type']

        input_path = save_file_from_request('file', os.path.join(SHARED_DIR, request.files['file'].filename))
        output_path = os.path.join(SHARED_DIR, "output_chroma_subsampling.mp4")

        # Cambiar chroma subsampling
        command = [
            "docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-y", "-i", input_path,
            "-c:v", "libx265", "-vf", f"format={chroma_type}", output_path
        ]
        subprocess.run(command, check=True)

        # Ajustar la ruta de salida para la respuesta
        adjusted_output_path = adjust_output_path(output_path)

        # Devolver archivo procesado
        return send_file(adjusted_output_path, mimetype='video/mp4', as_attachment=True, download_name="video_chroma_subsampled.mp4")
    except (ValueError, KeyError, subprocess.CalledProcessError) as e:
        return jsonify({'error': str(e)}), 400

@app_seminar2.route('/video_container_creator', methods=['POST'])
def video_container_creator():
    clean_directory(SHARED_DIR)
    try:
        data = get_json_from_request('data')
        bitrate = data['Bitrate']

        input_path = save_file_from_request('file', os.path.join(SHARED_DIR, request.files['file'].filename))
        video_20s_path = os.path.join(SHARED_DIR, "output_20s.mp4")
        aac_path = os.path.join(SHARED_DIR, "aac_mono_track.aac")
        mp3_path = os.path.join(SHARED_DIR, "mp4_to_mp3_stereo.mp3")
        ac3_path = os.path.join(SHARED_DIR, "mp4_to_ac3.ac3")
        final_output_path = os.path.join(SHARED_DIR, "BBC20s_package.mp4")

        # Generar videos y pistas de audio
        command_cut = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-ss", "00:00:00", "-i", input_path, "-c", "copy", "-t", "00:00:20", video_20s_path]
        subprocess.run(command_cut, check=True)

        command_aac = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", video_20s_path, "-acodec", "aac", "-ac", "1", aac_path]
        subprocess.run(command_aac, check=True)

        command_mp3 = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", video_20s_path, "-acodec", "mp3", "-ac", "2", "-b:a", bitrate, mp3_path]
        subprocess.run(command_mp3, check=True)

        command_ac3 = ["docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", video_20s_path, "-acodec", "ac3", ac3_path]
        subprocess.run(command_ac3, check=True)

        # Crear contenedor final
        command_package = [
            "docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", video_20s_path, "-i", aac_path, "-i", mp3_path, "-i", ac3_path,
            "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a", "-c:v", "copy", "-c:a", "copy", final_output_path
        ]
        subprocess.run(command_package, check=True)

        # Ajustar la ruta de salida para la respuesta
        adjusted_output_path = adjust_output_path(final_output_path)

        return send_file(adjusted_output_path, mimetype='video/mp4', as_attachment=True, download_name="BBC20s_package.mp4")
    except (ValueError, subprocess.CalledProcessError) as e:
        return jsonify({'error': str(e)}), 400

@app_seminar2.route('/motion_vectors_macroblocks', methods=['POST'])
def motion_vectors_macroblocks():
    clean_directory(SHARED_DIR)
    try:
        input_path = save_file_from_request('file', os.path.join(SHARED_DIR, request.files['file'].filename))
        output_path = os.path.join(SHARED_DIR, "motion_vectors.mp4")

        command = [
            "docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-flags2", "+export_mvs", "-i", input_path,
            "-vf", "codecview=mv=pf+bf+bb", output_path
        ]
        subprocess.run(command, check=True)

        # Ajustar la ruta de salida para la respuesta
        adjusted_output_path = adjust_output_path(output_path)

        return send_file(adjusted_output_path, mimetype='video/mp4', as_attachment=True, download_name="video_motion_vectors_macroblocks.mp4")
    except (ValueError, subprocess.CalledProcessError) as e:
        return jsonify({'error': str(e)}), 400

@app_seminar2.route('/YUV_histograms', methods=['POST'])
def YUV_histograms():
    clean_directory(SHARED_DIR)
    try:
        input_path = save_file_from_request('file', os.path.join(SHARED_DIR, request.files['file'].filename))
        output_path = os.path.join(SHARED_DIR, "histograms.mp4")

        command = [
            "docker", "exec", "contenedor_ffmpeg", "ffmpeg", "-i", input_path,
            "-vf", "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay", output_path
        ]
        subprocess.run(command, check=True)

        # Ajustar la ruta de salida para la respuesta
        adjusted_output_path = adjust_output_path(output_path)

        return send_file(adjusted_output_path, mimetype='video/mp4', as_attachment=True, download_name="video_histograms.mp4")
    except (ValueError, subprocess.CalledProcessError) as e:
        return jsonify({'error': str(e)}), 400
    

################## CODIGO QUE SE MANTIENE, IA no ha gestionado bien los ejercicios de la información del video y el numero de tracks

def funcion_get_information(directorio_input):
    output_file = "../shared_seminar2/output_information.json" 
    
    command = ["docker", "exec", "contenedor_ffmpeg", "sh", "-c", f"ffprobe -v quiet -print_format json -show_format  {directorio_input} | grep -E 'format_name|duration|size|bit_rate|encoder'  | sed '1s/^/{{ /; $s/,$/ }}/' | tr -d '\\n' | sed 's/, /,/g'> {output_file} 2>&1"]
        
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al extraer la informacion del video'}), 400
        

@app_seminar2.route('/video_info', methods=['POST'])

def video_info():
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


def get_number_of_tracks(directorio_input):
    output_file = "../shared_seminar2/number_of_tracks.txt" 

    # Usamos el mismo comando ffprobe que para el ejercicio de los 5 datos del video
    # grep -E 'Stream' | grep -E 'Audio': Esta vez, filtramos por las filas que contienen la palabra "Stream" y despues las que contienen la palabra "Audio"
    command = ["docker", "exec", "contenedor_ffmpeg", "sh", "-c", f"ffprobe -i  {directorio_input} 2>&1 | grep -E 'Stream' | grep -E 'Audio' > {output_file}"]
    try: 
        subprocess.run(command, check=True, capture_output=True, text=True)
    except:
        return jsonify({'Error': 'Error al extraer la informacion del video'}), 400

def count_lines_txt(directorio_input):
    fichero = open(directorio_input)
    return len(fichero.readlines())


@app_seminar2.route('/get_numer_of_tracks', methods=['POST'])
def get_numer_of_tracks():
    clean_directory(SHARED_DIR)
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

        return jsonify({'Number_of_tracks': str(number_of_tracks)}), 400

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
     

if __name__ == '__main__':
    app_seminar2.run(host="0.0.0.0", port=5001)
