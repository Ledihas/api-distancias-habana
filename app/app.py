from flask import Flask, request
from dotenv import load_dotenv
import requests
import os
from math import sqrt, radians
from app.direcciones import DIRECCIONES , DIRECCIONES_Municipi

app = Flask(__name__)
coordenadas1 = None
coordenadas2 = None
coordesvio = None

@app.route("/")
def hello_world():
    return "<p>El servicio está vivo!</p>"

@app.route('/enviar', methods=['GET',"POST"])
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
        # Extraer la distancia si se reconoce correctamente el intent
        if 'intents' in data and data['intents']:
            intent_name = data['intents'][0]['name']
            if intent_name == "ubicacion":
                
                
                

                # Obtener los lugares reconocidos (origen y destino)
                lugares = [entity['body'] for entity in data['entities'].get('wit$location:location', [])]
                contador = 0
                print("Lugares reconocidos:", lugares) 
                lugares_encontrados = 0
                

                for lugar in lugares:
                    # Verificar si alguna de las claves en DIRECCIONES está en el lugar reconocido
                    for clave in DIRECCIONES.keys():
                        if clave.lower() in lugar.lower():  # Comparar en minúsculas para evitar problemas de capitalización
                            if lugares_encontrados == 0:
                                coordenadas1 = DIRECCIONES[clave]
                            elif lugares_encontrados == 1:
                                coordenadas2 = DIRECCIONES[clave]
                            lugares_encontrados += 1
                            break  # Salir del bucle una vez que se encuentra una coincidencia

                # Si no se encontraron suficientes lugares, buscar en los strings directamente
                if lugares_encontrados < 2:
                    for clave in DIRECCIONES.keys():
                        if clave.lower() in string1.lower() and not coordenadas1:
                            coordenadas1 = DIRECCIONES[clave]
                            lugares_encontrados += 1
                        if clave.lower() in string2.lower() and not coordenadas2:
                            coordenadas2 = DIRECCIONES[clave]
                            lugares_encontrados += 1

                # Si aún no se encontraron suficientes lugares, buscar en DIRECCIONES_Municipi
                if lugares_encontrados < 2:
                    for clave in DIRECCIONES_Municipi.keys():
                        if clave.lower() in string1.lower() and not coordenadas1:
                            coordenadas1 = DIRECCIONES_Municipi[clave]
                            lugares_encontrados += 1
                        if clave.lower() in string2.lower() and not coordenadas2:
                            coordenadas2 = DIRECCIONES_Municipi[clave]
                            lugares_encontrados += 1

                if not coordenadas1 or not coordenadas2 or len(coordenadas1) < 2 or len(coordenadas2) < 2:
                    return {
                        "error": "Coordenadas incompletas o inválidas para una o ambas ubicaciones",
                        "ubicacion_problema": "" if not coordenadas1 or len(coordenadas1) < 2 else ""
                    }, 400

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
                    distancia_numerica = round(distancia_numerica, 2) 
                    distancia_numerica += distancia_numerica * 0.30  
                    return {"distancia": distancia_numerica, "coordenadas1": coordenadas1, "coordenadas2": coordenadas2}, 200
                except (ValueError, TypeError):
                    return {"error": "No se pudo convertir la distancia a número"}, 400

                
            else:
                return "No se pudo procesar la solicitud.", 400
        else:
            return 'Faltan parámetros string1 o string2', 400
    pass

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

                for lugar in lugares:
                    
                    if lugar in DIRECCIONES:
                        
                        coordesvio = DIRECCIONES[str(lugar)]
                    else:
                        return "No se encontró alguna de las dos direcciones"
                        
                    
               
                if not coordenadas1 or not coordesvio:
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

