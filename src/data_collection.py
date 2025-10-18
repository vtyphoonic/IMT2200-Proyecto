import requests
import os

def descargar_datos_climaticos(api_key: str, lat: float, lon: float, ruta_destino: str):
    """
    Descarga datos climáticos históricos de OpenWeatherMap.
    NOTA: La API gratuita puede tener limitaciones en el rango de fechas.

    Args:
        api_key (str): Tu clave de API de OpenWeatherMap.
        lat (float): Latitud de la ubicación (e.g., Santiago).
        lon (float): Longitud de la ubicación (e.g., Santiago).
        ruta_destino (str): Carpeta donde se guardará el archivo.
    """
    # URL para datos históricos (puede variar según la suscripción)
    URL_API = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=month&appid={api_key}"
    
    nombre_archivo = "datos_climaticos_santiago.json"
    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    
    try:
        print(f"Descargando datos climáticos...")
        respuesta = requests.get(URL_API, timeout=30)
        respuesta.raise_for_status()
        
        with open(ruta_completa, 'wb') as f:
            f.write(respuesta.content)
            
        print(f"Datos climáticos guardados en: {ruta_completa}")
        return ruta_completa
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar datos climáticos: {e}")
        return None

if __name__ == '__main__':

    DIRECTORIO_RAW = "data/raw"
    API_KEY_CLIMA = "201009219a924b510d4598d50373f1b8"
    LATITUD_SANTIAGO = -33.4489
    LONGITUD_SANTIAGO = -70.6693
    
    descargar_datos_climaticos(
            api_key=API_KEY_CLIMA,
            lat=LATITUD_SANTIAGO,
            lon=LONGITUD_SANTIAGO,
            ruta_destino=DIRECTORIO_RAW
        )