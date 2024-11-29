from flask import Flask, request
from dotenv import load_dotenv
import requests
import os
from math import sqrt, radians
from app.direcciones import DIRECCIONES

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>El servicio está vivo!</p>"

@app.route('/enviar', methods=['GET'])
@app.route('/enviar', methods=['POST'])  # Cambiado a POST
def enviar():
    # Obtener los parámetros de la cadena desde la solicitud GET
    string1 = request.args.get('string1')
    string2 = request.args.get('string2')

    # Verificar que ambos parámetros estén presentes
    if not string1 or not string2:
        return 'Faltan parámetros string1 o string2', 400

    # Construir el texto a enviar a Wit.ai
    texto_a_enviar = f"deme la distancia que existe entre {string1} y {string2} por carretera"

    # URL de la API de Wit.ai para el procesamiento del texto
    url_post = 'https://api.wit.ai/message'
    access_token = os.getenv('WIT_AI_TOKEN')  

    # Realizar la solicitud GET a Wit.ai
    response = requests.get(
        url_post, 
        headers={'Authorization': f'Bearer {access_token}'}, 
        params={'q': texto_a_enviar}
    )
    
    # Procesar la respuesta de Wit.ai
    data = response.json()

    # Extraer la distancia si se reconoce correctamente el intent
    if 'intents' in data and data['intents']:
        intent_name = data['intents'][0]['name']
        if intent_name in ["distancia", "get_distancia"]:
            coordenadas1 = None
            coordenadas2 = None
            
            # Obtener los lugares reconocidos (origen y destino)
            lugares = [entity['value'] for entity in data['entities'].get('wit$location:location', [])]
            contador = 0
            
            print("Lugares reconocidos:", lugares) 

            for lugar in lugares:
                if lugar in DIRECCIONES:
                    if contador == 0:
                        coordenadas1 = DIRECCIONES[lugar]
                        contador += 1
                    elif contador == 1:
                        coordenadas2 = DIRECCIONES[lugar]
                        break  # Salir después de encontrar la segunda coincidencia
            
            if contador < 2:
                return "No se encontraron ambas direcciones", 400
            
            x1, y1 = coordenadas1
            x2, y2 = coordenadas2
            
            x1 = radians(x1)
            y1 = radians(y1)
            x2 = radians(x2)
            y2 = radians(y2)

            distancia_km = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2)) * 6371
            
            return {"distancia": distancia_km}, 200

        else:
            return "No se pudo procesar la solicitud.", 400
    
    return "Error al procesar la respuesta de Wit.ai", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
