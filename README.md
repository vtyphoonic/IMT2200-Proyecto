# Optimización del Consumo Energético Residencial en la Región Metropolitana

Este proyecto busca desarrollar un modelo predictivo que cuantifique la influencia de factores socioeconómicos y climáticos en el consumo energético residencial en la Región Metropolitana de Chile. El objetivo final es informar políticas públicas y estrategias de eficiencia que permitan una reducción del gasto energético.

## Pregunta Central
¿Cómo podemos reducir el consumo energético residencial en un 5-10% identificando los factores más influyentes a través del análisis de datos?

## Estado Actual del Proyecto (Octubre 2025)

El proyecto ha completado la fase inicial de Adquisición, Limpieza y Exploración de Datos (EDA). Se ha construido un dataset unificado que combina datos de consumo energético (CNE) y datos climáticos (DMC). Se han establecido modelos de regresión base que demuestran la importancia de las variables geográficas (`comuna`) y la insuficiencia de usar solo variables de tiempo.

## Fuentes de Datos

1.  **Consumo Energético (CNE):**
    * **Fuente:** Comisión Nacional de Energía (CNE), Plataforma Energía Abierta.
    * **Estado:** La API oficial se encontraba en mantención. Se recurrió a una descarga manual controlada del archivo de consumo eléctrico (`consumo_electrico_cne_2024.xlsx`).

2.  **Datos Climáticos (DMC):**
    * **Fuente:** Dirección Meteorológica de Chile (DMC), portal climatológico.
    * **Estado:** La API de OpenWeatherMap (propuesta original) no autorizó el acceso a datos históricos. Se pivotó a la fuente oficial de Chile, descargando programáticamente los registros diarios de temperatura media de la estación "Quinta Normal" (2015-2025).

3.  **Datos Socioeconómicos (Pendiente):**
    * **Fuente:** Instituto Nacional de Estadísticas (INE) o Ministerio de Desarrollo Social.
    * **Estado:** Pendiente de adquisición.

## Pipeline de Procesamiento (Resumen)

El notebook `notebooks/2_Limpieza_y_EDA.ipynb` ejecuta el siguiente pipeline:

1.  **Carga y Limpieza (Energía):**
    * Detecta que el archivo `.xlsx` de la CNE es un "CSV dentro de un Excel".
    * Divide la única columna usando `;` como separador.
    * Convierte columnas a tipos numéricos (`energia_kwh`, etc.) e imputa valores nulos (`NaN`) con `0`.
2.  **Filtrado (Energía):**
    * Filtra el dataset para mantener únicamente las filas de la **'RegiÃ³n Metropolitana de Santiago'**.
    * Identifica y **elimina los datos anómalos** (Nov/Dic 2022) por considerarse corruptos.
3.  **Carga y Agregación (Clima):**
    * Consolida programáticamente todos los CSV de temperatura de la DMC.
    * Agrega los datos de temperatura diarios para obtener el **promedio mensual**.
4.  **Fusión Final:** Une el DataFrame de consumo de energía con el de temperatura promedio mensual usando la `fecha` como clave.

## Resultados Preliminares: Modelos Base

Se establecieron modelos de Regresión Lineal para medir el impacto de las variables:

1.  **Modelo 1 (Tiempo):** `energia_kwh ~ anio + mes + trimestre`
    * **R²: 0.00**
    * **Conclusión:** El tiempo por sí solo no tiene poder predictivo.

2.  **Modelo 2 (Tiempo + Ubicación):** `energia_kwh ~ anio + mes + comuna (One-Hot Encoded)`
    * **R²: 0.10**
    * **Conclusión:** La ubicación (`comuna`) es un factor crítico y explica el 10% de la varianza del consumo.

## Próximos Pasos

1.  **Re-entrenar:** Entrenar un modelo de Regresión Lineal que incluya las variables climáticas (`temperatura_promedio_c`) para cuantificar su impacto en el R².
2.  **Enriquecimiento (Socioeconómico):** Adquirir y fusionar los datos de ingreso o pobreza por comuna del INE.
3.  **Modelado Avanzado:** Entrenar un modelo `RandomForestRegressor` con el dataset completo (energía + clima + socioeconómico) para capturar relaciones no lineales y comparar su rendimiento.

## Estructura del Repositorio

-   **/data**: Almacena todos los datos (excluidos por `.gitignore`).
    -   **/data/raw**: Datos originales, sin procesar.
    -   **/data/processed**: Datos limpios y combinados.
-   **/notebooks**: Contiene los Jupyter Notebooks para la exploración y modelado.
-   **/src**: Contiene el código fuente modularizado.
-   **/reports**: Contiene los entregables finales.
-   `requirements.txt`: Dependencias del proyecto.

## Autores

-   Vicente Rodríguez
-   Bastián Pérez
-   Thomas Johnson