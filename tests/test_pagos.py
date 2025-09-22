import requests
import json
import sys
import time

def check_server(url, max_retries=3):
    print("Verificando conexión al servidor...")
    for i in range(max_retries):
        try:
            response = requests.get(url)
            print("✅ Servidor en línea!")
            return True
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"Intento {i+1}: Servidor no disponible. Reintentando en 2 segundos...")
                time.sleep(2)
            else:
                print("\n❌ Error: No se pudo conectar al servidor.")
                print("Por favor, asegúrate de que el servidor Django esté corriendo con:")
                print("python manage.py runserver")
                return False

def test_crear_pago():
    BASE_URL = "http://localhost:8000"
    
    if not check_server(f"{BASE_URL}/pagos/crear/"):
        return

    # Datos de prueba
    data = {
        "monto": "150000",
        "metodo_pago": "TRANSFERENCIA",
        "referencia_pago": "TEST123"
    }
    
    try:
        # Hacer la petición POST
        print("\nProbando crear pago...")
        response = requests.post(
            f"{BASE_URL}/pagos/crear/",
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.json()}")
        
        if response.ok:
            # Si la creación fue exitosa, probar obtener estado
            id_transaccion = response.json()['id_transaccion']
            test_obtener_estado(BASE_URL, id_transaccion)
    
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error al realizar la petición: {str(e)}")
    except json.JSONDecodeError:
        print("\n❌ Error: Respuesta no válida del servidor")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")

def test_obtener_estado(base_url, id_transaccion):
    try:
        print("\nProbando obtener estado...")
        response = requests.get(f"{base_url}/pagos/estado/{id_transaccion}/")
        
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.json()}")
    
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error al obtener estado: {str(e)}")

if __name__ == "__main__":
    test_crear_pago()
