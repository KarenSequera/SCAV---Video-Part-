# **Readme**

Este proyecto se basa en el desarrollo de técnicas y algoritmos de compresión con la finalidad de poder comprimir vídeos. Para esto usaremos una API desarrollada en Python utilizando Flask y librería ffmpeg para procesar imágenes/videos. 

Para la API hemos usado el framework de Flask, ya que teníamos experiencia de otros trabajos. Para mantener el código ordenado y más limpio, todos los nuevos ejercicios apartir del Seminario 2 se encuentran en un archivo separado y se usa el puerto 5001 para acceder a los endpoints. Si se quiere acceder a los endpoints del Lab 1, hay que usar el puerto 5000.

La API está dentro de un contenedor con base Linux Ubuntu, con todas las dependencias necesarias para ejecutarse y tiene abierto el puerto 5000 y 5001 para poder interactuar con ella. Esta, se conecta con otro contenedor que contiene ffmpeg (tambien con base Linux Ubuntu) para realizar algunas operaciones. Para poder instanciar los contenedores correctamente, permitir que se comuniquen entre sí y darles acceso a los directorios compartidos dónde se almacenan los inputs y los outputs, se ha creado un archivo de configuración llamado docker-compose.yml. Este archivo contiene toda la información necesaria para configurar, montar y gestionar los contenedores: se especifica la localización de las diferentes dockerfiles, las interfaces de redes (para que se puedan comunicar) y volúmenes (dónde se montan la carpetas locales a los contenedores). Los ejercicios del Lab1 necesitan que el input se encuentra en la carpeta compartida /shared_lab1/ y almacenará los outputs también en esa carpeta. Sin embargo, para este nuevo seminario hemos conseguido que la API obtenga el archivo directamente de la petición POST y sea capaz de enviar el output deseado en la respuesta. Cuando se sube un archivo, se almacena en la carpera /shared_seminar2/, donde también se almacenan el output del contenedor FFMPEG que despues la API envía al usuario. Cada vez que se llama a un endpoint del seminario 2 los contenidos de la carpeta /shared_seminar2/ se eliminan para que no acomule videos que ya no tienen utilidad. 

Para que el contenedor de ffmpeg esté siempre ejecutándose, se le indica que ejecute un proceso infinito que no ejecuta ninguna acción, de lo contrario la API no podría acceder a esa instancia. Para instanciar los contenedores usando el archivo de configuración,  usaremos el comando docker-compose.

A continuación, se describen la utilización y las principales funciones de este proyecto. 

## **Instalación y configuración**

Para poder usarlo primero se tiene que clonar el repositorio de manera local con el comando:
$ git clone <ruta del repositorio> 
Los contenidos de la entrega final (es decir, todo el proyecto acabado) se encuentran en la carpeta Final:

			     					   $ cd Final
             
Para instanciar los contenedores usando el archivo de configuración hay que ejecutar:

                      					         $ docker-compose up
              
Si es la primera vez que se ejecuta, puede tardar en instalar todas las dependencias de la API. Si ya se ha ejecutado anteriormente, usará la memoria caché para agilizar el proceso. 
Al terminar, se habrán creado las dos imágenes y las dos instancias de los contenedores, estando ahora estos activos. Ya se puede interactuar con la API mediante peticiones POST (en el caso de las funciones) y GET (para el unit test). 
 
## **INTERFAZ GRÁFICA**
Como parte de la última práctica, uno de los ejercicios ha consistido en desarrollar una interfaz gráfica para interactuar con la API. La interfaz ha sido desarrollada en HTML. Para acceder a ella es necesario abrir un servidor HTTP dentro de la carpeta front_end del projecto. Es importante que el servidor este servido en el puerto 8080, ya que las URLs usadas para navegar por las páginas de la interfaz usan este puerto. Las páginas se han organizado en carpetas con el nombre correspondiente a la práctica/seminario al que pertenecen. Hay una página por endpoint.

								        $ cd front_end
								$   python -m http.server 8080
	
Una vez los contenedores de la API y el DOCKER están instanciados y el servidor HTTP está abierto en el puerto 8080, se puede acceder a la interfaz gráfica mediante cualquier navegador, accediendo a http://localhost:8080 para visualizar la página del indice.

![Captura de pantalla 2024-12-10 145556](https://github.com/user-attachments/assets/b3c54c99-ff6c-4b47-b3ff-afae9a7945b1)
Dentro del índice se puede acceder a cualquier endpoint donde se muestran las indicaciones y el resultado, como por ejemplo en el siguiente endpoint:
![Captura de pantalla 2024-12-10 150035](https://github.com/user-attachments/assets/5f3578c2-00ca-4950-b0d8-55e0c26b11ea)

Nota* El endpoint de la encoding ladder no interactúa directamente con la API. En su lugar, hemos almacenado la encoding ladder resultante de procesar el video de BBB a través de la API, y lo que hace la GUI es obtenerla mediante HLS y mostrarla en pantalla. 

Nota** Uno de los últimos ejercicios también ha consistido en realizar mejoras con IA. Hay un documento pdf explicando los cambios.

# **ENDPOINTS LAB 1**

### **/rgb_to_yuv POST** 

Dados los valores RGB, este endpoint devuelve su equivalente en sistema YUV. Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/rgb_to_yuv -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"R":255,"G":100,"B":50}' -ContentType "application/json"
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"U":83.11000000000001,"V":199.59500000000003,"Y":136.835}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 59
                        Content-Type: application/json
                        Date: Mon, 18 Nov 2024 19:38:15 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
                        {"U":83.11000000000001,"V":199.5950...
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 59], [Content-Type, application/json], [Date, Mon, 18 Nov 2024 19:38:15 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 59
    
    



### **/yuv_to_rgb POST**

Dados los valores YUV, este EndPoint devuelve su equivalente en sistema RGB. Ejemplo:



    $ Invoke-WebRequest -Uri http://localhost:5000/yuv_to_rgb -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Y":128,"U":128,"V":128}' -ContentType "application/json"
    
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"B":130.368,"G":130.368,"R":130.368}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 38
                        Content-Type: application/json       
                        Date: Mon, 18 Nov 2024 19:44:27 GMT  
                        Server: Werkzeug/3.0.6 Python/3.8.10 
    
                        {"B":130.368,"G":130.368,"R":130.36...
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 38], [Content-Type, application/json], [Date, Mon, 18 Nov 2024 19:44:27 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 38
    





### **/serpentine POST**

Dada una matriz, este endpoint devuelve una lista con el resultado de leerla de forma “serpentine” (siguiendo la manera de leer de las slides de clase). Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/serpentine -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Matriz":[[1,2,6,7,14],[3,5,8,13,15],[4,9,12,16,19],[10,11,17,18,20]]}' -ContentType "application/json"
    
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"Output":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 64
                        Content-Type: application/json
                        Date: Mon, 18 Nov 2024 19:49:08 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
    
                        {"Output":[1,2,3,4,5,6,7,8,9,10,11,...
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 64], [Content-Type, application/json], [Date, Mon, 18 Nov 2024 19:49:08 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 64 



### **/run_lenght POST** 

Dada una lista conteniendo un stream de datos, este Endpoint devuelve una lista con el resultado de aplicar el algoritmo “run lenght”. Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/run_lenght -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Data_stream":[0, 0, 3, 4, 8, 6, 33, 0, 0, 0, 4]}' -ContentType "application/json" 
    
    Output: 
    StatusCode        : 200
    StatusDescription : OK 
    Content           : {"Output":["02",3,4,8,6,33,"03",4]}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 36
                        Content-Type: application/json
                        Date: Mon, 18 Nov 2024 19:51:55 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
    
                        {"Output":["02",3,4,8,6,33,"03",4]}...
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 36], [Content-Type, application/json], [Date, Mon, 18 Nov 2024 19:51:55 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 36
    



### **/bw_converter POST**

Dada el nombre de una imagen de input (tiene que estar guardada dentro de la carpeta /share/) y el nombre para la imagen de output, este endpoint llama al container ffmpeg para que genere una versión en blanco y negro del input. Devuelve el directorio dónde se encuentra el output. Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/bw_converter -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg", "Nombre Output": "output_bw.jpg"}' -ContentType "application/json"
    
    Nota: La imagen output se encuentra en el directorio /shared/. Las funciones tienen como output alguna imagen, siempre devuelven un mensaje con el directorio.
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"Msj":"La imagen en blanco y negro se encuentra en /shared/output_bw.jpg"}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 76
                        Content-Type: application/json
                        Date: Mon, 18 Nov 2024 20:04:14 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
                        
                        {"Msj":"El resultado se encuenta en...
                        
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 76], [Content-Type, application/json], [Date, Mon, 18 Nov 2024 20:04:14 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 76
    


### **/resolution_changer POST** 

Dada el nombre de una imagen de input (tiene que estar guardada dentro de la carpeta /share/), el nombre para la imagen de output, y las dimensiones (píxeles de ancho y de alto), este Endpoint llama al container ffmpeg para que genere una versión en la resolución indicada. Devuelve el directorio dónde se encuentra el output. Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/resolution_changer -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg", "Nombre Output": "output_resolution_changer.jpg", "Alto": 10, "Ancho": 10}' -ContentType "application/json"
    Nota: La imagen output se encuentra en el directorio /shared/. Las funciones tienen como output alguna imagen, siempre devuelven un mensaje con el directorio.
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"Msj":"La imagen con resolucion 10x10 se encuentra en /shared/output_resolution_changer.jpg"}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 95
                        Content-Type: application/json
                        Date: Tue, 19 Nov 2024 17:44:13 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
    
                       {"Msj":"El resultado se encuenta en...

    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 95], [Content-Type, application/json], [Date, Tue, 19 Nov 2024       
                        17:44:13 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 95
  



### **/dct_encoder POST** 

Dada el nombre de una imagen de input (tiene que estar guardada dentro de la carpeta /share/), este endpoint codifica la imagen usando la dct y la descodifica. Después, genera una imagen que contiene la original, una visualización de la DCT y la reconstruida. Devuelve el directorio dónde se encuentra la imagen generada. Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/dct_encoder -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg"}' -ContentType "application/json"
    
    Nota: La imagen output se encuentra en el directorio /shared/. Las funciones tienen como output alguna imagen, siempre devuelven un mensaje con el directorio.
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"Msj":"El resultado se encuenta en el directorio/shared/DCT/"}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 64
                        Content-Type: application/json
                        Date: Tue, 19 Nov 2024 17:49:25 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
    
                        {"Msj":"El resultado se encuenta en...
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 64], [Content-Type, application/json], [Date, Tue, 19 Nov 2024 
                        17:49:25 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 64

### **/dwt_encoder POST** 

Dada el nombre de una imagen de input (tiene que estar guardada dentro de la carpeta /share/), este endpoint codifica la imagen usando la dwt y la descodifica. Después, genera una imagen que contiene la original y la reconstruida para poder compararlas. Además, también genera una imagen que contiene la descomposición en LL, LH, HL y HH de la DWT. Devuelve el directorio dónde se encuentran las imágenes generadas. Ejemplo:


    $ Invoke-WebRequest -Uri http://localhost:5000/dwt_encoder -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Nombre Input": "input.jpg"}' -ContentType "application/json"
        
    Nota: La imagen output se encuentra en el directorio /shared/. Las funciones tienen como output alguna imagen, siempre devuelven un mensaje con el directorio.
    Output: 
    StatusCode        : 200
    StatusDescription : OK
    Content           : {"Msj":"El resultado se encuenta en el directorio/shared/DWT/"}
    
    RawContent        : HTTP/1.1 200 OK
                        Connection: close
                        Content-Length: 64
                        Content-Type: application/json
                        Date: Tue, 19 Nov 2024 17:56:42 GMT
                        Server: Werkzeug/3.0.6 Python/3.8.10
    
                        {"Msj":"El resultado se encuenta en...
    Forms             : {}
    Headers           : {[Connection, close], [Content-Length, 64], [Content-Type, application/json], [Date, Tue, 19 Nov 2024 
                        17:56:42 GMT]...}
    Images            : {}
    InputFields       : {}
    Links             : {}
    ParsedHtml        : mshtml.HTMLDocumentClass
    RawContentLength  : 64

Hay que mencionar que para poder usar estos endpoints, /dct_encoder y /dwt_encoder, a la hora de hacer la parte de la interfaz gráfica hemos adaptado estas funciónes para mejorar su usabilidad. Para ello hemos hecho que el usuario pueda seleccionar un archivo directamente como input desde su dispositivo sin necesidad de tenerlo en una carpeta específica. Este archivo se guardara en la carpeta de DCT o DWT, segun el endpoint que se use, igual que el output que se genere. Además, hemos añadido que al terminar la función los archivos generados se eliminen para evitar que se acumulen archivos innecesarios. 

Para comprobar el funcionamiento de las funciones hemos usado POSTMAN. Hemos usando como input el campo "file" donde subimos una imagen que seleccionamos, la cual junto con el ouput que genere se guarda en la carpeta correspondiente y, además, se muestra el output generado por pantalla.  

Ejemplo de petición de la DCT usando curl en la CMD:

						     curl --location "http://localhost:5000/dct_encoder" ^
						     --form "file=@C:/Users/karen/Downloads/input.jpg" ^
						     --output outputDCT.png

Ejemplo de petición de la DWT usando curl en la CMD:

						     curl --location "http://localhost:5000/dwt_encoder" ^
						     --form "file=@C:/Users/karen/Downloads/input.jpg" ^
						     --output DWT_decomposición.png

### **/run_test GET**

Al llamar a este endpoint ejecuta los unit tests del seminario anterior. Para las funciones que devuelven imágenes, en lugar de unit test se prueba el código con diferentes parámetros y inputs. Resultados dentro de las respectivas carpetas. Ejemplo:
Petición que almacena el json:

    $ Invoke-WebRequest -Uri http://localhost:5000/run_tests -Method GET -Headers @{ "Content-Type" = "application/json" }).Content | Set-Content -Path .\test_results.json
    Output: 
    {"BWConverter":"Output files in: /shared/unit_tests/bw",
    "DCTEncoder":"Output files in: /shared/unit_tests/DCT",
    "DWTEncoder":"Output files in: /shared/unit_tests/DWT",
    "ResolutionChanger":"Output files in: /shared/unit_tests/resize",
    "TestColorTranslator":"Pruebas ejecutadas: 2 \nPruebas exitosas: 2 \nFallos: 0 \nErrores: 0\n",
    "TestRunLength":"Pruebas ejecutadas: 1 \nPruebas exitosas: 1 \nFallos: 0 \nErrores: 0\n",
    "TestSerpentine":"Pruebas ejecutadas: 1 \nPruebas exitosas: 1 \nFallos: 0 \nErrores: 0\n"}
    

# **ENDPOINTS SEMINAR 2**

Para los endpoints de este seminario, se recomienda usar POSTMAN para las requests con este formato:

![Captura de pantalla 2024-11-27 173020](https://github.com/user-attachments/assets/893d1312-2883-451b-8a37-52bec61c6dd4)

Hemos creado un repositorio de POSTMAN con un ejemplo para cada uno de los ENDPOINTS: https://documenter.getpostman.com/view/39631696/2sAYBXAAd1
Si se abre desde POSTMAN desktop y la API esta funcionando, se pueden ejecutar las requests que hemos creado. Solo haría falta cambiar el video de input ya que usa path relativo. 

El formulario tiene dos campos, para el funcionamiento adecuado de la API tienen que llamarse "file" y "data". El campo de file contiene el video que se desea subir y el campo de data un json con la información necesaria. El campo de data no siempre es necesario, depende del endpoint.

También vamos a incluir un ejemplo de petición con curl. 

### **/resolution_changer POST**

Este endpoint recibe un video en el campo "file" y la resolución deseada en formato json (ej. {"Alto":"100","Ancho":100}) en el campo de "data", y devuelve una version del video en dicha resolución. 

Ejemplo de petición usando curl en la CMD:

					      curl --location "http://localhost:5001/resolution_changer" ^
					    --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
					    --form "data={\"Alto\":\"100\",\"Ancho\":100}" ^
					    --output output_file.mp4


### **/chroma_subsampling_changer POST**

Este endpoint recibe un video en el campo "file" y el tipo de chroma subsampling deseado en formato json (ej.{"Type":"yuv420p"}) en el campo "data", y devuelve una versión del video en dicho formato de chroma subsampling. Agunos ejemplos de tipo de chroma subsampling son: yuv420p, yuv422p, yuv444p, yuv420p10le, yuv422p10le, yuv444p10le, etc. 

Ejemplo de petición usando curl en la CMD:

					     curl --location "http://localhost:5001/chroma_subsampling_changer" ^
					     --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
					     --form "data={\"Type\":\"yuv420p\"}" ^
					     --output output_file.mp4

### **/video_info POST**

Este endpoint recibe un video en el campo de "file" y devuelve un json con 5 datos importantes del video. 

Ejemplo de petición usando curl en la CMD:

					     curl --location "http://localhost:5001/video_info" ^
					     --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
					     --output output_file.json

Ejemplo de output:

{
    "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
    "duration": "20.063000",
    "size": "21186520",
    "bit_rate": "8447996",
    "encoder": "Lavf58.29.100"
}

### **/video_container_creator POST**

Este endpoint recibe un video en el campo de "file" y un bitrate en formato json (ej. {"Bitrate":"32k"}) en el campo de "data". Dado el video de input, este endpoint genera una versión del video de 20s y tres archivos de audio con diferentes formatos:  aac mono, mp3 estereo con el bitrate especificado y aac3. Por último, genera un contenedor mp4 que contiene el video y las diferentes pistas de audio y la envia al usuario. 

Ejemplo de petición usando curl en la CMD:

						     curl --location "http://localhost:5001/video_container_creator" ^
						     --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
						     --form "data={\"Bitrate\":\"32k\"}" ^
						     --output output_file.mp4

### **/get_numer_of_tracks POST**

Este endpoint recibe un video en el campo de "file" y devuelve un archivo json que contiene la información de cuantas pistas de audio tiene el video. 

Ejemplo de petición usando curl en la CMD:

					      curl --location "http://localhost:5001/get_numer_of_tracks" ^
					      --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
					      --output output_file.json
      
Ejemplo de output:

{
    "Number of tracks": "3"
}

### **/motion_vectors_macroblocks POST**

Este endpoint recibe un video en el campo de "file" y devuelve una versión del video con los motion vectors.  

Ejemplo de petición usando curl en la CMD:

					      curl --location "http://localhost:5001/motion_vectors_macroblocks" ^
					      --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
					      --output output_file.mp4

### **/YUV_histograms POST**

Este endpoint recibe un video en el campo de "file" y devuelve una versión del video los histogramas YUV. Para este endpoint se recomienda el de POSTMAN!

      ![Captura de pantalla 2024-11-27 200225](https://github.com/user-attachments/assets/e19cd932-1c31-4299-9a55-5a4fbfd0456a)

# **ENDPOINTS PRÁCTICA 2**

También se han añadido al repositorio de postman
 
### **/video_codec_converter POST**

Este endpoint recibe un video en el campo de "file" y un tipo de codec en formato json (ej. {"Codec":"VP8"}) en el campo de "data".

					      curl --location "http://localhost:5001/video_codec_converter" ^
					    --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
					    --form "data={\"Codec\":\"VP8\"}" ^
					    --output output_file.mp4
				      
### **/encoding_ladder_creator POST**

Este endpoint recibe un video en el campo de "file" y crea una encodding ladder con resoluciones 640x360, 1280x720, 1920x1080 y 2560x1140 dentro del directorio /encoding_ladder. 

					      curl --location "http://localhost:5001/encoding_ladder_creator" ^
	     				     --form "file=@C:/Users/karen/Downloads/BBC20s_package.mp4" ^
	       					--output output_file.json
