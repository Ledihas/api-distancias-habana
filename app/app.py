from flask import Flask, request
from dotenv import load_dotenv
import requests
import os
from math import sqrt, radians
from app.direcciones import DIRECCIONES , DIRECCIONES_Municipi

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>El servicio está vivo!</p>"

@app.route('/enviar', methods=['GET', "POST"])
def enviar():
    # Obtener los parámetros de la cadena desde la solicitud GET
    string1 = request.args.get('string1')
    string2 = request.args.get('string2')

    # Verificar que ambos parámetros estén presentes
    if string1 and string2:
        # Construir el texto a enviar a Wit.ai
        texto_a_enviar = f"deme la direccion gps de {string1} y {string2} "

        # URL de la API de Wit.ai para el procesamiento del texto
        url_post = 'https://api.wit.ai/message'
        access_token = os.getenv('WIT_AI_TOKEN')  

        # Realizar la solicitud GET a Wit.ai
        response = requests.get(
            url_post, 
            headers={'Authorization': f'Bearer {access_token}'}, 
            params={'q': texto_a_enviar}
        )
        print("Respuesta de Wit.ai:", response.status_code)  
        # Procesar la respuesta de Wit.ai
        data = response.json()
        print("Respuesta de Wit.ai:", data)

        # Inicializar coordenadas
        coordenadas1 = None
        coordenadas2 = None

        # Buscar coordenadas para string1
        for clave in DIRECCIONES.keys():
            if clave.lower() in string1.lower():
                coordenadas1 = DIRECCIONES[clave]
                break

        # Buscar coordenadas para string2
        for clave in DIRECCIONES.keys():
            if clave.lower() in string2.lower():
                coordenadas2 = DIRECCIONES[clave]
                break

        # Si no se encontraron coordenadas en DIRECCIONES, buscar en DIRECCIONES_Municipi
        if coordenadas1 is None:
            for clave in DIRECCIONES_Municipi.keys():
                if clave.lower() in string1.lower():
                    coordenadas1 = DIRECCIONES_Municipi[clave]
                    break

        if coordenadas2 is None:
            for clave in DIRECCIONES_Municipi.keys():
                if clave.lower() in string2.lower():
                    coordenadas2 = DIRECCIONES_Municipi[clave]
                    break

        # Verificar si se encontraron coordenadas válidas
        if coordenadas1 is None or coordenadas2 is None:
            return {
                "error": "Coordenadas incompletas o inválidas para una o ambas ubicaciones",
                "ubicacion_problema": "" if coordenadas1 is not None else ""
            }, 400

        # Calcular la distancia
        x1, y1 = coordenadas1
        x2, y2 = coordenadas2

        # Calcular la distancia (en km)
        distancia_km = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2)) * 6371

        # Convertir la respuesta a número si es posible
        try:
            distancia_numerica = float(distancia_km)
            distancia_numerica = round(distancia_numerica, 2)
            return {"distancia": distancia_numerica, "coordenadas1": coordenadas1, "coordenadas2": coordenadas2}, 200
        except (ValueError, TypeError):
            return {"error": "No se pudo convertir la distancia a número"}, 400

    return 'Faltan parámetros string1 o string2', 400

@app.route('/desviacion', methods=['GET','POST'])
def desviacion():
    string1 = request.args.get('string1')
    string2 = request.args.get('string2')
    string3 = request.args.get('string3')

    
    if string1 and string2 and string3:
        try:
            lat1, lon1 = string1.split(',')
            lat2, lon2 = string2.split(',')
            coordenadas1 = [float(lat1), float(lon1)]
            coordenadas2 = [float(lat2), float(lon2)]
        except ValueError:
            return {"error": "Formato de coordenadas inválido"}, 400
        
        texto_a_enviar = f"deme la direccion gps de {string3}"
        url_post = 'https://api.wit.ai/message'
        access_token = os.getenv('WIT_AI_TOKEN')  

        # Realizar la solicitud GET a Wit.ai
        response = requests.get(
            url_post, 
            headers={'Authorization': f'Bearer {access_token}'}, 
            params={'q': texto_a_enviar}
        )
        print("Respuesta de Wit.ai:", response.status_code)  
        # Procesar la respuesta de Wit.ai
        data = response.json()
        print("Respuesta de Wit.ai:", data)
        # Extraer la distancia si se reconoce correctamente el intent
        if 'intents' in data and data['intents']:
            intent_name = data['intents'][0]['name']
            if intent_name == "ubicacion":
                
                
                

                # Obtener los lugares reconocidos (origen y destino)
                lugares = [entity['body'] for entity in data['entities'].get('wit$location:location', [])]
                
                print("Lugares reconocidos:", lugares) 
                coordesvio = 0
                
                for lugar in lugares:
                    
                    if lugar in DIRECCIONES:
                        
                        coordesvio = DIRECCIONES[str(lugar)]
                    else:
                        return "No se encontró alguna de las dos direcciones"
                        
                    
               
                if not coordenadas1 or coordesvio == 0:
                    return {
                        "error": "Coordenadas incompletas o inválidas para una o ambas ubicaciones",
                        
                    }, 400

                x1 = coordenadas1[0]
                y1 = coordenadas1[1]
                x2 = coordesvio[0]
                y2 = coordesvio[1]
                x3 = coordenadas2[0]
                y3 = coordenadas2[1]
                            
                x1 = radians(x1)
                y1 = radians(y1)
                            
                x2 = radians(x2)
                y2 = radians(y2)
                
                x3 = radians(x3)
                y3 = radians(y3)
                            
                            
                distancia_km1 = sqrt(pow((x2-x1),2) + pow((y2-y1),2)) * 6371
                distancia_km2 = sqrt(pow((x2-x3),2) + pow((y2-y3),2)) * 6371
                distancia_km = distancia_km1 + distancia_km2
                
                            
                # Convertir la respuesta a número si es posible
                try:
                    distancia_numerica = float(distancia_km)
                    distancia_numerica = round(distancia_numerica, 2) 
                    distancia_numerica += distancia_numerica * 0.40  
                    return {"distancia": distancia_numerica}, 200
                except (ValueError, TypeError):
                    return {"error": "No se pudo convertir la distancia a número"}, 400

                
            else:
                return "No se pudo procesar la solicitud.", 400
        else:
            return 'Faltan parámetros string1 o string2', 400
        
    
    pass
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

