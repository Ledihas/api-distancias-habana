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
def enviar():
    # Obtener los parámetros de la cadena desde la solicitud GET
    string1 = request.args.get('string1')
    string2 = request.args.get('string2')

    # Verificar que ambos parámetros estén presentes
    if string1 and string2:
        # Construir el texto a enviar a Wit.ai
        texto_a_enviar = f"deme la distancia que existe entre los municipios   {string1} y {string2} por carretera"

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
            if intent_name == "distancia" or intent_name == "get_distancia":
                
                DIRECCIONES

                # Obtener los lugares reconocidos (origen y destino)
                lugares = [entity['value'] for entity in data['entities'].get('wit$location:location', [])]

                print("Lugares reconocidos:", lugares) 

                if len(lugares) == 2:
                    # Intentar obtener la distancia en ambas direcciones
                    coordenadas1 = DIRECCIONES.get(lugares[0])
                    coordenadas2 = DIRECCIONES.get(lugares[1])
                    
                    x1 = coordenadas1[0]
                    y1 = coordenadas1[1]
                    x2 = coordenadas2[0]
                    y2 = coordenadas2[1]
                    
                    x1 = radians(x1)
                    y1 = radians(y1)
                    
                    x2 = radians(x2)
                    y2 = radians(y2)
                    
                    
                    distancia_km = sqrt(pow((x2-x1),2) + pow((y2-y1),2)) * 6371
                    
                    # Convertir la respuesta a número si es posible
                    try:
                        distancia_numerica = float(distancia_km)
                        return {"distancia": distancia_numerica}, 200
                    except (ValueError, TypeError):
                        return {"error": "No se pudo convertir la distancia a número"}, 400

            else:
                return "Intento no reconocido.", 400
        else:
            return "No se pudo procesar la solicitud.", 400
    else:
        return 'Faltan parámetros string1 o string2', 400
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
