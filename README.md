# ⚡ Predicción de Consumo Eléctrico Residencial en la Región Metropolitana

Este proyecto implementa un pipeline de Ciencia de Datos *end-to-end* para predecir el consumo eléctrico mensual a nivel comunal. Integra fuentes heterogéneas (energía, clima y datos socioeconómicos) para entrenar modelos de Machine Learning capaces de capturar estacionalidad, tendencias económicas y comportamiento térmico.

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura modular y secuencial para garantizar la reproducibilidad:

```
├── data/
│   ├── raw/                # Datos crudos (Excel, SAV, CSV)
│   └── processed/          # Datos limpios y Master Table final
├── notebooks/
│   ├── 01_Data_Collection_Consumo_Energetico.ipynb  # Ingesta CNE
│   ├── 02_Data_Collection_Meteorologica.ipynb       # Ingesta DMC + Cálculo HDD/CDD
│   ├── 03_Data_Collection_Socioeconomica.ipynb      # Ingesta CASEN + Interpolación
│   ├── 04_Limpieza_y_EDA.ipynb                      # Merge, Ingeniería de Features y Análisis
│   └── 05_Modelamiento_Predictivo.ipynb             # Entrenamiento y Evaluación (XGBoost)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación principal
```

-----

## 🧠 Supuestos Críticos y Decisiones de Diseño

Este modelo se construye sobre una serie de supuestos simplificadores necesarios para alinear fuentes de datos con frecuencias y granularidades dispares. **Es crucial entender estas premisas para interpretar correctamente los resultados:**

### 1\. Supuestos de Alineación Temporal (Frequency Mismatch)

  * **La "Verdad" es Mensual:** Dado que la variable objetivo (facturación de energía) es mensual, todas las demás variables se han forzado a esta frecuencia. No se intenta predecir consumo diario.
  * **Estabilidad Socioeconómica Intra-anual:** Se asume que el nivel de ingresos y la tasa de pobreza de una comuna se mantienen **constantes durante los 12 meses de un mismo año**. El modelo no captura shocks económicos mensuales (ej: un bono del gobierno en un mes específico).
  * **Agregación Climática no Lineal:** Se asume que el promedio simple de temperatura mensual *destruye* información valiosa. Por ello, se utilizan **Grados-Día (HDD/CDD)** acumulados mensualmente para capturar la *intensidad* del frío o calor diario que detona el uso de calefacción o aire acondicionado.

### 2\. Supuestos de Imputación y Proyección (Notebook 03)

  * **Linealidad entre Encuestas CASEN:** Para los años sin encuesta (ej: 2016, 2018-2019), se asume una **evolución lineal** entre los puntos de datos reales (2015, 2017, 2020, 2022). Esto ignora fluctuaciones económicas de corto plazo.
  * **Inercia Futura (Forward Fill):** Para los años posteriores a la última CASEN disponible (2023-2025), se asume que las condiciones socioeconómicas se mantienen estables en el último valor conocido (2022). El modelo *no* predice cambios macroeconómicos futuros.
  * **Impacto Pandémico (2020):** Se asume que la caída/aumento de ingresos capturada en la CASEN 2020 refleja adecuadamente el shock del COVID-19 para efectos de consumo eléctrico, sin necesidad de variables dummy externas.

### 3\. Supuestos Geoespaciales

  * **Homogeneidad Climática Regional:** Se utiliza una estación meteorológica representativa (Quinta Normal) para toda la Región Metropolitana. Se asume que las variaciones microclimáticas entre comunas (ej: Lo Barnechea vs. Pudahuel) son marginales para el consumo agregado o se cancelan en el promedio mensual.
  * **Normalización de Comunas:** Se asume que las discrepancias en nombres ("Santiago" vs "Santiago Centro") se resuelven completamente mediante normalización de texto (NFKD, lowercase), sin pérdida de datos por descalce de llaves.

-----

## 🛠️ Pipeline de Datos

### 1\. Energía (`01_Energia`)

  * **Fuente:** Comisión Nacional de Energía (CNE). ([http://energiaabierta.cl/categorias-estadistica/electricidad/])
  * **Proceso:** Normalización de nombres de comunas, conversión de fechas y filtrado por cliente residencial/comercial.
  * **Clave:** Genera la columna target `energia_kwh`.

### 2\. Clima (`02_Clima`)

  * **Fuente:** Dirección Meteorológica de Chile (DMC). ([https://climatologia.meteochile.gob.cl/application/informacion/fichaDeEstacion/330020])
  * **Proceso:** Ingesta de registros horarios, imputación de vacíos leves y cálculo diario de temperatura.
  * **Feature Engineering:** Cálculo de **Heating Degree Days (HDD)** (Base 15°C) y **Cooling Degree Days (CDD)** (Base 24°C) antes de la agregación mensual.

### 3\. Socioeconómico (`03_Socio`)

  * **Fuente:** Encuesta CASEN (MDSF). ([https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2022])
  * **Proceso:** Fusión compleja de múltiples archivos (Datos + Códigos Geográficos + Diccionario Excel) para reconstruir la historia de cada comuna.
  * **Proyección:** Interpolación lineal para rellenar lagunas temporales.

### 4\. Consolidación (`04_Merge_EDA`)

  * **Proceso:** Unificación de las 3 ramas mediante `Left Joins` estratégicos para no perder datos de facturación.
  * **Limpieza:** Eliminación de columnas redundantes y manejo final de nulos.
  * **EDA:** Análisis de correlación (Clima vs Consumo) y estacionalidad.

### 5\. Modelado (`05_Modeling`)

  * **Modelo:** XGBoost Regressor / Random Forest.
  * **Validación:** Split temporal estricto (Train: \<2023, Test: \>=2023) para evitar *data leakage*.
  * **Métricas:** MAE (Error Absoluto Medio) y R² (Coeficiente de Determinación).

-----

## 🚀 Instalación y Ejecución

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/tu-usuario/imt2200-proyecto.git](https://github.com/tu-usuario/imt2200-proyecto.git)
    cd imt2200-proyecto
    ```

2.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar Pipeline:**
    Ejecutar los notebooks en orden secuencial del `01` al `05`.

-----

## 📊 Resultados Esperados

El modelo final permite estimar la demanda energética futura a nivel comunal, permitiendo a las distribuidoras:

  * Planificar compras de energía con mayor precisión.
  * Identificar comunas con alta sensibilidad térmica (pobreza energética).
  * Detectar anomalías de consumo no explicadas por el clima o la economía.

-----

**Integrantes:** Thomas Johnson, Bastián Pérez y Vicente Rodríguez
**Curso:** IMT2200 - Introducción a la Ciencia de Datos
**Fecha:** Noviembre 2025

-----

## ⚠️ Advertencia Crítica sobre Adquisición e Ingeniería de Datos

Este proyecto **no utiliza datos crudos directos** para el entrenamiento del modelo. Se ha implementado un pipeline de ingeniería de datos agresivo para alinear fuentes con frecuencias temporales incompatibles. 

Cualquier uso de este dataset (`master_table.csv`) o de los modelos resultantes debe considerar los siguientes **supuestos y fabricaciones controladas**:

### 1. Datos Socioeconómicos (CASEN) - Interpolación y Proyección
* **La realidad no es continua:** Las encuestas CASEN son fotos puntuales (2015, 2017, 2020, 2022). Para el modelado mensual, **se han "inventado" los datos de los años intermedios** (2016, 2018, 2019, 2021) mediante interpolación lineal.
* **Congelamiento del Presente:** Para el periodo 2023-2025, ante la falta de datos oficiales publicados al momento del estudio, se ha utilizado una estrategia de **Forward Fill** (inercia), asumiendo que las condiciones de ingresos y pobreza de 2022 se mantienen estáticas. El modelo no captura shocks económicos recientes post-2022.

### 2. Datos Climáticos (DMC) - Compresión de Varianza
* **Proxy Regional:** Se utiliza la estación de Quinta Normal como proxy climático para **toda la Región Metropolitana**. No se consideran microclimas locales (ej: la diferencia térmica entre Pudahuel y Lo Barnechea), lo que introduce un margen de error en comunas precordilleranas.
* **Pérdida de Resolución:** Al agregar los datos diarios a mensuales mediante **Grados-Día (HDD/CDD)**, se suavizan los eventos extremos de corta duración (olas de calor de 2 días) que podrían haber generado picos de consumo momentáneos.

### 3. Datos Energéticos (CNE) - Desfase de Facturación
* **Supuesto de Calendario:** Se asume que la "energía facturada" en un mes corresponde exactamente al consumo de ese mes calendario. En la realidad operativa, las lecturas de medidores tienen desfases y ciclos de facturación que pueden no coincidir perfectamente con el inicio y fin de mes, introduciendo un ruido residual en la variable objetivo.

**Conclusión:** Este dataset está optimizado para capturar **tendencias macro y estacionalidad**, no para auditoría forense de consumo exacto.