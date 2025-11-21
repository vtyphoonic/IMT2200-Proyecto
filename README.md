# ⚡ Optimización y Predicción del Consumo Eléctrico Residencial en la Región Metropolitana

**Un enfoque de Ciencia de Datos para la Planificación Energética Territorial**

*   **Integrantes:** Thomas Johnson, Bastián Pérez y Vicente Rodríguez
*   **Curso:** IMT2200 - Introducción a la Ciencia de Datos
*   **Fecha:** Noviembre 2025

---

## 📖 Resumen Ejecutivo

Este proyecto busca cuantificar la relación entre factores climáticos, socioeconómicos y tarifarios con el consumo eléctrico residencial a nivel comunal en la Región Metropolitana de Chile. A través de modelos predictivos de Machine Learning, entregamos herramientas para que distribuidoras y formuladores de políticas públicas puedan anticipar la demanda agregada y diseñar intervenciones de eficiencia energética más justas y efectivas.

---

## 🎯 Objetivos y Alcance

### La Pregunta de Investigación
> "¿Cómo podemos reducir el consumo energético residencial en un porcentaje ambicioso pero alcanzable (ej: 5-10%) en la Región Metropolitana, identificando los factores socioeconómicos y climáticos más influyentes, y cómo podemos predecir estos consumos para informar estrategias de eficiencia?"

### Alcance: Territorial vs. Individual
Si bien la propuesta original contemplaba la optimización a nivel de "hogar individual", la disponibilidad de datos públicos nos ha llevado a un enfoque **territorial (Macro)**.

**Objetivo Final:**
Desarrollar un modelo predictivo que permita estimar la demanda energética mensual por comuna, identificando patrones de desigualdad socioeconómica y sensibilidad térmica para apoyar la toma de decisiones en infraestructura y subsidios.

---

## 🛠️ Metodología: Pipeline de Datos

El proyecto sigue una arquitectura modular y secuencial para garantizar la reproducibilidad.

### 1. Energía (`01_Data_Collection_Consumo_Energetico.ipynb`)
*   **Fuente:** Comisión Nacional de Energía (CNE). ([http://energiaabierta.cl/categorias-estadistica/electricidad/])
*   **Proceso:** Normalización de nombres de comunas, conversión de fechas y filtrado por cliente residencial/comercial.
*   **Output:** Columna target `energia_kwh`.

### 2. Clima (`02_Data_Collection_Meteorologica.ipynb`)
*   **Fuente:** Dirección Meteorológica de Chile (DMC). ([https://climatologia.meteochile.gob.cl/application/historico/datosDescarga/330020])
*   **Proceso:** Ingesta de registros horarios, imputación de vacíos leves y cálculo diario de temperatura.
*   **Feature Engineering:** Cálculo de **Heating Degree Days (HDD)** (Base 15°C) y **Cooling Degree Days (CDD)** (Base 24°C). Se seleccionó la estación **Quinta Normal** como proxy climático único para toda la RM por su robustez histórica.

### 3. Socioeconómico (`03_Data_Collection_Socioeconomica.ipynb`)
*   **Fuente:** Encuesta CASEN (MDSF). ([https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2022])
*   **Proceso:** Fusión de múltiples archivos y códigos geográficos.
*   **Proyección:** Interpolación lineal para rellenar lagunas temporales entre años de encuesta.

### 4. Limpieza y EDA (`04_Limpieza_y_EDA.ipynb`)
*   **Consolidación:** Unificación de las 3 ramas mediante `Left Joins` estratégicos. Creación del `master_table.csv`.
*   **Análisis:** Correlación (Clima vs Consumo), estacionalidad y desigualdad energética.

### 5. Modelamiento Predictivo (`05_Modelamiento_Predictivo.ipynb`)
*   **Estrategia:** Entrenamiento de modelos de ensamble (**XGBoost Regressor**) respetando la causalidad temporal (Train: 2015-2022, Test: 2023+).
*   **Métricas:** MAE (Error Absoluto Medio) y R².

---

## 🧠 Supuestos Críticos y Limitaciones

> [!IMPORTANT]
> Este modelo se construye sobre supuestos simplificadores necesarios para alinear fuentes de datos con frecuencias dispares. Es crucial entender estas premisas para interpretar los resultados.

### 1. Alineación Temporal y Frecuencia
*   **La "Verdad" es Mensual:** Se predice facturación mensual, no consumo diario.
*   **Estabilidad Intra-anual:** Se asume que ingresos y pobreza se mantienen constantes durante los 12 meses de un mismo año.
*   **Agregación Climática:** Se utilizan **Grados-Día (HDD/CDD)** acumulados mensualmente para capturar la intensidad térmica, superando el promedio simple de temperatura.

### 2. Imputación y Proyección (Datos Socioeconómicos)
*   **Interpolación Lineal:** Para años sin encuesta CASEN (ej: 2016, 2018), se asume una evolución lineal.
*   **Inercia Futura (Forward Fill):** Para 2023-2025, se asume que las condiciones de 2022 se mantienen estáticas. El modelo no captura shocks económicos recientes post-2022.

### 3. Supuestos Geoespaciales
*   **Homogeneidad Climática:** Quinta Normal se usa como proxy para toda la RM. Se ignoran microclimas (ej: precordillera) que podrían afectar la demanda local.
*   **Normalización:** Se asume que las discrepancias de nombres comunales se resuelven completamente mediante normalización de texto.

### 4. Desfase de Facturación
*   Se asume que la energía facturada en un mes corresponde al consumo de ese mes calendario, ignorando los ciclos de lectura reales de los medidores.

---

## 📊 Resultados y Conclusiones

### Hallazgos Principales
1.  **La Trampa del Frío:** Las comunas de menores ingresos muestran menor elasticidad al frío (no pueden aumentar su consumo proporcionalmente para calefaccionar), sugiriendo **pobreza energética oculta**.
2.  **Estacionalidad Marcada:** Los Grados-Día de Calefacción (HDD) son el predictor climático más fuerte, confirmando que el invierno es el driver crítico de la demanda en la RM.

### Validación de Objetivos
*   ✅ **Predicción:** El modelo XGBoost logra predecir la facturación eléctrica mensual con métricas de error aceptables para la planificación macro.
*   ✅ **Factores Influyentes:** Se identificó al clima (HDD) y al nivel socioeconómico (Quintiles) como los factores determinantes.
*   ⚠️ **Meta de Reducción (5-10%):** El proyecto entrega el diagnóstico ("Dónde" y "Por qué") para que las políticas públicas focalicen subsidios o mejoras de aislamiento en las comunas críticas, permitiendo alcanzar esta meta de manera indirecta.

---

## 📂 Estructura del Proyecto

```
├── data/
│   ├── raw/                # Datos crudos (Excel, SAV, CSV)
│   └── processed/          # Datos limpios y Master Table final
├── notebooks/
│   ├── 01_Data_Collection_Consumo_Energetico.ipynb
│   ├── 02_Data_Collection_Meteorologica.ipynb
│   ├── 03_Data_Collection_Socioeconomica.ipynb
│   ├── 04_Limpieza_y_EDA.ipynb
│   └── 05_Modelamiento_Predictivo.ipynb
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivo de gitignore
└── README.md               # Documentación principal
```

---

## 🚀 Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/vtyphoonic/IMT2200-Proyecto.git
    cd IMT2200-Proyecto
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar Pipeline:**
    Ejecutar los notebooks en orden secuencial del `01` al `05` para reproducir los resultados.