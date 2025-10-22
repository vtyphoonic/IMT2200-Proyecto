# Optimización del Consumo Energético Residencial en la Región Metropolitana

Este proyecto busca desarrollar un modelo predictivo que cuantifique la influencia de factores socioeconómicos y climáticos en el consumo energético residencial en la Región Metropolitana de Chile. El objetivo final es informar políticas públicas y estrategias de eficiencia que permitan una reducción del gasto energético.

## Pregunta Central
¿Cómo podemos reducir el consumo energético residencial en un 5-10% identificando los factores más influyentes a través del análisis de datos?

## Estado Actual del Proyecto (Octubre 2025)

Se ha completado la fase de **Adquisición, Limpieza, Combinación y Análisis Exploratorio de Datos (EDA)**. Se ha construido un dataset unificado (`dataset_final_energia_clima_socio.csv` en `data/processed/`) que integra:
* Datos de consumo energético de la CNE.
* Datos meteorológicos (temperatura media, máxima y mínima mensual) de la DMC.
* Datos socioeconómicos (Índice de Pobreza Multidimensional) del INE/MDS.

El análisis exploratorio inicial confirma una fuerte estacionalidad en el consumo (correlacionada con la temperatura) y diferencias significativas entre comunas. Se identificaron y eliminaron datos anómalos/corruptos.

## Fuentes de Datos Utilizadas

1.  **Consumo Energético (CNE):**
    * **Fuente:** Comisión Nacional de Energía (CNE), Plataforma Energía Abierta.
    * **Método:** Descarga manual controlada (`consumo_electrico_cne_2024.xlsx` en `data/raw/`) debido a API en mantención.

2.  **Datos Climáticos (DMC):**
    * **Fuente:** Dirección Meteorológica de Chile (DMC), portal climatológico.
    * **Método:** Descarga manual de archivos CSV anuales (`330020_*.csv` en `data/raw/`) para la estación "Quinta Normal" (2015-2025), consolidados y procesados programáticamente. Se pivotó desde OpenWeatherMap (API gratuita sin acceso histórico).

3.  **Datos Socioeconómicos (INE/MDS):**
    * **Fuente:** Instituto Nacional de Estadísticas (INE) o Ministerio de Desarrollo Social (MDS).
    * **Método:** Descarga manual de archivo (`datos_socioeconomicos.csv` en `data/raw/`) con datos comunales anuales (ej. Índice de Pobreza).

## Pipeline de Procesamiento (Resumen en `notebooks/Limpieza_y_EDA.ipynb`)

1.  **Carga y Limpieza CNE:** Lee `.xlsx`, maneja formato "CSV dentro de Excel", convierte tipos, imputa NaNs con 0.
2.  **Filtrado CNE:** Selecciona solo 'Región Metropolitana de Santiago', crea columna `fecha`, elimina datos anómalos (Nov-Dic 2022).
3.  **Carga y Limpieza DMC:** Consolida CSVs anuales, limpia nombres, convierte tipos, elimina datos futuros.
4.  **Agregación DMC:** Calcula promedios diarios y luego mensuales para `temperatura_promedio_c`, `temperatura_maxima_c`, `temperatura_minima_c`. Rellena NaNs.
5.  **Carga y Limpieza Socioeconómico:** Lee `.csv`, renombra columnas, limpia nombres de comuna para merge, convierte variable socioeconómica (ej. `indice_pobreza_pct`) a numérica.
6.  **Fusión Final:** Une los DataFrames de energía (limpio y filtrado), clima (mensual) y socioeconómico (anual) usando `fecha` y `anio`/`comuna` como claves. Rellena NaNs post-fusión.
7.  **Ingeniería de Características:** Crea variables temporales (`trimestre`, `inicio_mes`).
8.  **EDA Combinado:** Visualiza tendencias, matriz de correlación, scatter plots (consumo vs. temp, consumo vs. pobreza).
9.  **Guardado:** Exporta el DataFrame final procesado a `data/processed/dataset_final_energia_clima_socio.csv`.

## Próximos Pasos (en `notebooks/3_Modelado_y_Evaluacion.ipynb`)

1.  **Cargar Dataset Final:** Leer `dataset_final_energia_clima_socio.csv`.
2.  **Preparar Datos para Modelado:** Seleccionar características finales, aplicar One-Hot Encoding a `comuna`.
3.  **Entrenar Modelo Base:** Implementar y evaluar Regresión Lineal Múltiple.
4.  **Entrenar Modelo Avanzado:** Implementar y evaluar `RandomForestRegressor`.
5.  **Comparar y Analizar:** Evaluar métricas (R², MSE), analizar importancia de características y errores del modelo.
6.  **Iterar:** Refinar características, probar otros modelos (ej. Gradient Boosting), optimizar hiperparámetros.

## Estructura del Repositorio

-   **/data**: Almacena todos los datos (excluidos por `.gitignore`).
    -   **/data/raw**: Datos originales descargados.
    -   **/data/processed**: Datasets limpios y combinados listos para modelar.
-   **/notebooks**: Contiene los Jupyter Notebooks.
    -   `Limpieza_y_EDA.ipynb`: Carga, limpieza, fusión y EDA.
    -   `3_Modelado_y_Evaluacion.ipynb`: Entrenamiento y evaluación de modelos.
-   **/src**: Código fuente modularizado (ej. `data_collection.py`, aunque actualmente no se usa para descarga automática).
-   **/reports**: Entregables finales (figuras, informe).
-   `requirements.txt`: Dependencias del proyecto.

## Autores

-   Vicente Rodríguez
-   Bastián Pérez
-   Thomas Johnson

## Advertencia: Proceso de Adquisición de Datos

Las fuentes de datos CNE y DMC requirieron descargas manuales debido a limitaciones de las APIs o portales. Esto introduce una dependencia manual en la reproducibilidad inicial. El pipeline de procesamiento *a partir* de los archivos descargados es programático y está contenido en los notebooks.