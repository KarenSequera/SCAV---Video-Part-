from flask import Flask, request, jsonify

app = Flask(__name__)

## RGB to YUV
@app.route('/rgb_to_yuv', methods=['POST'])
def rgb_to_yuv():
    data = request.get_json()    

    try:
        R = data['R']
        G = data['G']
        B = data['B']
    
        Y = 0.257 * R + 0.504*G + 0.098*B + 16
        U = -0.148*R - 0.291*G + 0.439*B + 128
        V = 0.439*R - 0.368*G - 0.071*B + 128
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
    
        R = 1.164 * (Y - 16) + 1.596 * (V - 128)
        G = 1.164 * (Y - 16) - 0.813 * (V - 128) - 0.391 * (U - 128)
        B = 1.164 * (Y - 16) + 2.018 * (U - 128)
        #El color YUV se devuelve en una lista
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

@app.route('/serpentine', methods=['POST'])
def serpentine():
    data = request.get_json() 
    try:
        matriz = data['Matriz']   
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
        return jsonify({
            'Output': output,
        })

    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo
#Invoke-WebRequest -Uri http://localhost:5000/serpentine -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"matriz":[[1,2,6,7,14],[3,5,8,13,15],[4,9,12,16,19],[10,11,17,18,20]]}' -ContentType "application/json"

@app.route('/run_lenght', methods=['POST'])
def run_lenght():
    data = request.get_json() 
    try:
        list = data['Data_stream']  
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
        return jsonify({
            'Output': output_list,
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    
#Comando PowerShell para probarlo    
#Invoke-WebRequest -Uri http://localhost:5000/run_lenght -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"Data_stream":[0, 0, 3, 4, 8, 6, 33, 0, 0, 0, 4]}' -ContentType "application/json"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    