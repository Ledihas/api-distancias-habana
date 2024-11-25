from flask import Flask, request
from dotenv import load_dotenv
import requests
import os

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
                
                distancias = {
                    ("Cuba", "China"): 13659.23,
                    ("La Habana", "La Habana"): 0,
                    ("La Habana, Cuba ","Santiago de Cuba"): 765,
                    ("La Habana, Cuba ","Camagüey, Cuba"): 505,
                    ("La Habana, Cuba ","Holguín, Cuba"): 685,
                    ("La Habana, Cuba ","Guantánamo, Cuba"): 831,
                    ("La Habana, Cuba ","Santa Clara, Cuba"): 261,
                    ("La Habana, Cuba ","Bayamo, Cuba"): 675,
                    ("La Habana, Cuba ","Manzanillo, Cuba"): 630,
                    ("La Habana, Cuba ","Varadero, Cuba"): 150,
                    ("La Habana, Cuba ","Trinidad,Cuba"): 300,
                    ("La Habana, Cuba ","Ciego de Ávila:, Cuba"): 405,
                    ("La Habana", "Almendares"): 5,
                    ("Almendares", "La Habana"): 5,
                    ("La Habana", "Diez de Octubre"): 6,
                    ("Diez de Octubre", "La Habana"): 6,
                    ("La Habana", "Arroyo Naranjo"): 11,
                    ("Arroyo Naranjo", "La Habana"): 11,
                    ("La Habana", "Mantilla"): 8,
                    ("Mantilla", "La Habana"): 8,
                    ("La Habana", "Boyeros"): 14,
                    ("Boyeros", "La Habana"): 14,
                    ("La Habana", "Fontanar"): 12,
                    ("Fontanar", "La Habana"): 12,
                    ("La Habana", "Ciudad Camilo Cienfuegos"): 6,
                    ("Ciudad Camilo Cienfuegos", "La Habana"): 6,
                    ("Ciudad Camilo Cienfuegos", "Arroyo Naranjo"): 14,
                    ("Arroyo Naranjo", "Ciudad Camilo Cienfuegos"): 14,
                    ("Almendares", "Diez de Octubre"): 7,
                    ("Diez de Octubre", "Almendares"): 7,
                    ("Almendares", "Arroyo Naranjo"): 9,
                    ("Arroyo Naranjo", "Almendares"): 9,
                    ("Almendares", "Mantilla"): 10,
                    ("Mantilla", "Almendares"): 10,
                    ("Boyeros", "Mantilla"): 9,
                    ("Mantilla", "Boyeros"): 9,
                    ("Ciudad Camilo Cienfuegos", "Mantilla"): 10,
                    ("Mantilla", "Ciudad Camilo Cienfuegos"): 10,
                    ("Diez de Octubre", "Arroyo Naranjo"): 6,
                    ("Arroyo Naranjo", "Diez de Octubre"): 6,
                    ("Diez de Octubre", "Mantilla"): 3,
                    ("Mantilla", "Diez de Octubre"): 3,

                    ("Arroyo Naranjo", "Boyeros"): 4,
                    ("Boyeros", "Arroyo Naranjo"): 4,
                    ("Almendares", "Boyeros"): 12,
                    ("Boyeros", "Almendares"): 12,
                    ("Boyeros", "Fontanar"): 2,
                    ("Fontanar", "Boyeros"): 2,
                    ("Ciudad Camilo Cienfuegos", "Boyeros"): 19,
                    ("Boyeros", "Ciudad Camilo Cienfuegos"): 19,

                    # Otros municipios
                    ("Boyeros", "Diez de Octubre"): 10,
                    ("Diez de Octubre", "Boyeros"): 10,

                    ("Fontanar", "Diez de Octubre"): 9,
                    ("Diez de Octubre", "Fontanar"): 9,
                    ("Fontanar", "Ciudad Camilo Cienfuegos"): 17,
                    ("Ciudad Camilo Cienfuegos", "Fontanar"): 17,
                    ("Fontanar", "Almendares"): 10,
                    ("Almendares", "Fontanar"): 10,
                    ("Fontanar", "Arroyo Naranjo"): 4,
                    ("Arroyo Naranjo", "Fontanar"): 4,
                    ("Fontanar", "Mantilla"): 8,
                    ("Mantilla", "Fontanar"): 8,
                    ("Boyeros", "Fontanar"): 2,
                    ("Fontanar", "Boyeros"): 2,
                    ("Fontanar", "Fontanar"): 0,
                    ("Boyeros", "Boyeros"): 0,
                    ("Mantilla", "Mantilla"): 0,
                    ("Arroyo Naranjo", "Arroyo Naranjo"): 0,
                    ("Diez de Octubre", "Diez de Octubre"): 0,
                    ("Almendares", "Almendares"): 0,
                    ("Ciudad Camilo Cienfuegos", "Ciudad Camilo Cienfuegos"): 0,
                    

                    ("San Miguel del Padrón", "La Habana"): 14, 
                    ("La Habana", "San Miguel del Padrón"): 14, 
                
                    ("Cotorro", "Diez de Octubre"): 12, 
                    ("Diez de Octubre", "Cotorro"): 12, 

                    ("Cotorro", "Arroyo Naranjo"): 15, 
                    ("Arroyo Naranjo", "Cotorro"): 15, 

                    ("Cotorro", "San Miguel del Padrón"): 10, 
                    ("San Miguel del Padrón", "Cotorro"): 10, 

                    ("Playa", "La Habana"): 8,
                    ("Plaza de la Revolución", "La Habana"): 4,
                    ("Centro Habana", "La Habana"): 2,
                    ("Habana Vieja", "La Habana"): 0,  
                    ("Regla", "La Habana"): 5,
                    ("Habana del Este", "La Habana"): 10,
                    ("Guanabacoa", "La Habana"): 12,
                    ("Marianao", "La Habana"): 12,
                    ("La Lisa", "La Habana"): 14,
                    ("Cerro", "La Habana"): 6,

                    # Distancias entre municipios
                    ("Playa", "Plaza de la Revolución"): 4,
                    ("Playa", "Marianao"): 5,
                    ("Playa", "La Lisa"): 6,
                    ("Plaza de la Revolución", "Centro Habana"): 2,
                    ("Plaza de la Revolución", "Cerro"): 4,
                    ("Centro Habana", "Habana Vieja"): 2,
                    ("Centro Habana", "Cerro"): 3,
                    ("Habana Vieja", "Regla"): 5,
                    ("Regla", "Habana del Este"): 6,
                    ("Regla", "Guanabacoa"): 4,
                    ("Habana del Este", "Guanabacoa"): 5,
                    ("Marianao", "La Lisa"): 3,
                    ("Marianao", "Cerro"): 6,
                    ("La Lisa", "Boyeros"): 8,
                    ("Boyeros", "La Lisa"): 8,
                    
                    ("Cerro", "Diez de Octubre"): 3,
                    ("Diez de Octubre", "Cerro"): 3,
                    ("Guanabacoa", "San Miguel del Padrón"): 5,
                    ("San Miguel del Padrón", "Diez de Octubre"): 4,
                    
                    # Distancias adicionales entre municipios
                    ("Plaza de la Revolución", "Diez de Octubre"): 5,
                    ("Diez de Octubre", "Plaza de la Revolución"): 5,
                    ("Centro Habana", "Plaza de la Revolución"): 2,
                    ("Marianao", "Plaza de la Revolución"): 7,
                    ("Cerro", "Boyeros"): 7,
                    ("Habana del Este", "San Miguel del Padrón"): 8,
                    ("La Lisa", "Playa"): 6,
                    ("Guanabacoa", "Cotorro"): 9,
                    ("San Miguel del Padrón", "Cerro"): 5,
                    ("Regla", "San Miguel del Padrón"): 4,
                    ("Marianao", "Boyeros"): 9,
                    
                    # Distancias a cero para el mismo municipio
                    ("Playa", "Playa"): 0,
                    ("Plaza de la Revolución", "Plaza de la Revolución"): 0,
                    ("Centro Habana", "Centro Habana"): 0,
                    ("Habana Vieja", "Habana Vieja"): 0,
                    ("Regla", "Regla"): 0,
                    ("Habana del Este", "Habana del Este"): 0,
                    ("Guanabacoa", "Guanabacoa"): 0,
                    ("Marianao", "Marianao"): 0,
                    ("La Lisa", "La Lisa"): 0,
                    ("Cerro", "Cerro"): 0,
                                            
                }

                # Obtener los lugares reconocidos (origen y destino)
                lugares = [entity['value'] for entity in data['entities'].get('wit$location:location', [])]

                print("Lugares reconocidos:", lugares)  # Para depuración

                if len(lugares) == 2:
                    # Intentar obtener la distancia en ambas direcciones
                    distancia_km = distancias.get((lugares[0], lugares[1])) or distancias.get((lugares[1], lugares[0])) or "Distancia no disponible"
                    
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
