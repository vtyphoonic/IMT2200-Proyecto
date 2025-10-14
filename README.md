# Optimización del Consumo Energético Residencial en la Región Metropolitana

Este proyecto busca desarrollar un modelo predictivo que cuantifique la influencia de factores socioeconómicos y climáticos en el consumo energético residencial en la Región Metropolitana de Chile. El objetivo final es informar políticas públicas y estrategias de eficiencia que permitan una reducción del gasto energético.

## Pregunta Central
¿Cómo podemos reducir el consumo energético residencial en un 5-10% identificando los factores más influyentes a través del análisis de datos?

## Estructura del Repositorio

- **/data**: Almacena todos los datos.
  - **/data/raw**: Datos originales, sin procesar, extraídos de las fuentes. **Este directorio es inmutable.**
  - **/data/processed**: Datos limpios, transformados y combinados, listos para el análisis y modelado.
- **/notebooks**: Contiene los Jupyter Notebooks para la exploración, experimentación y comunicación de resultados. Siguen el flujo de trabajo del proyecto.
- **/src**: Contiene el código fuente modularizado y reutilizable.
  - `data_collection.py`: Scripts para descargar datos de las APIs y fuentes web (CNE, OpenWeatherMap, INE).
  - `data_processing.py`: Funciones para limpiar, transformar y realizar ingeniería de características.
  - `modeling.py`: Funciones para entrenar, evaluar y ejecutar los modelos de predicción.
- **/reports**: Contiene los entregables finales.
  - **/reports/figures**: Gráficos, mapas y otras visualizaciones generadas para el informe.
- `requirements.txt`: Dependencias del proyecto.

## Autores

- Vicente Rodríguez
- Bastián Pérez
- Thomas Johnson