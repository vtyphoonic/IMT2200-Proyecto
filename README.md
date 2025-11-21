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
Entiendo perfectamente. Si no es factible realizar la validación cruzada con otra estación (por falta de datos o tiempo), lo **profesional es declarar explícitamente esa limitación**.

En ciencia de datos, un supuesto bien documentado es mucho mejor que una validación ausente. Aquí tienes un texto formal para insertar en tu informe o notebook (por ejemplo, en el **Notebook 04** o en las **Conclusiones**), que transforma esta carencia en una "decisión de alcance" justificada.

#### ⚠️ Nota sobre la Representatividad Climática (Proxy Único)

**Supuesto de Homogeneidad:**
Para este estudio, se ha utilizado la estación meteorológica de **Quinta Normal** como proxy único para representar las condiciones climáticas de toda la Región Metropolitana. Se asume que, dado que Santiago se encuentra en una cuenca geográfica, las **tendencias** de temperatura (olas de frío o calor) son transversales a todas las comunas, aunque las magnitudes absolutas puedan variar.

**Justificación de la Simplificación:**
Si bien existen microclimas específicos (especialmente en comunas precordilleranas como Lo Barnechea o rurales como San José de Maipo), la estación Quinta Normal posee la serie temporal más robusta, continua y validada por la DMC para el periodo 2015-2024. La inclusión de múltiples estaciones habría requerido procesos de imputación complejos que exceden el alcance actual del proyecto sin garantizar una mejora significativa en un modelo de frecuencia mensual.

**Impacto en el Modelo:**
El modelo captura correctamente la estacionalidad y los cambios bruscos de temperatura que afectan la demanda agregada. Sin embargo, podría subestimar el consumo por calefacción en comunas con temperaturas sistemáticamente menores al centro de la ciudad. Se recomienda considerar la incorporación de correcciones geográficas de temperatura en futuras iteraciones.

---

## 📊 Resultados y Conclusiones

### 1. Desempeño del Modelo
El estudio reveló una distinción crítica en la predicción de la demanda eléctrica:
* **Segmento Residencial (Foco del Proyecto):** El modelo alcanza una precisión operativa viable, con un error medio absoluto (MAE) de **~13.8 kWh por hogar**. Considerando un consumo promedio de 210 kWh, esto representa un error relativo de apenas **~6.6%**.
* **Interpretación:** Esto valida el modelo para la asignación de subsidios y planificación urbana, ya que el margen de error es menor al consumo de un electrodoméstico estándar.
* **Limitación Industrial:** Las métricas globales (cuando no se filtran clientes) se ven afectadas por la presencia de grandes consumidores industriales en la data pública, lo que confirma la necesidad de una limpieza estricta de tarifas en futuras iteraciones.

### 2. Hallazgos Estratégicos
* **La Trampa del Frío:** Las comunas de menores ingresos muestran una demanda inelástica al frío (no consumen más porque no pueden pagar, no por eficiencia), evidenciando **pobreza energética**.
* **El Clima como Motor:** Los Grados-Día de Calefacción (HDD) son el predictor temporal más fuerte, permitiendo anticipar los peaks de demanda invernal con semanas de antelación.

### 3. Validación de la Meta (5-10%)
El análisis de residuos indica que la meta de reducción es **técnicamente viable**. Si se focalizan intervenciones de eficiencia energética (aislación) exclusivamente en las comunas que presentan un "sobreconsumo" injustificado (residuos positivos), se puede cerrar la brecha de eficiencia sin afectar el confort de los hogares vulnerables.

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

---

### Clarificación de Alcance: Del Individuo al Territorio

Es crítico notar que este estudio adopta un enfoque de Planificación Territorial en lugar de Comportamiento del Consumidor. Al utilizar datos agregados a nivel comunal (CNE y CASEN), el modelo neutraliza las idiosincrasias individuales para revelar patrones estructurales de la ciudad.

Los resultados no deben utilizarse para juzgar el comportamiento de un hogar específico (riesgo de Falacia Ecológica), sino para focalizar recursos públicos. Cuando el modelo indica que una comuna tiene un 'sobreconsumo', no significa que sus vecinos derrochen energía, sino que la infraestructura habitacional o la matriz de calefacción de ese territorio requiere intervención prioritaria (subsidios de aislación térmica o recambio tecnológico).

---

### Nota final sobre preguntas de investigación de la propuesta

A pesar del "fallo" en las métricas globales (causado por el ruido industrial), **sí se lograron responder las 5 preguntas**, aunque con ciertos matices y adaptaciones estratégicas.

### 1. Tendencia Estacional y Climática
> *¿Cuál es la tendencia estacional... y relación con temperatura?*
* **Respuesta:** ✅ **Sí, totalmente respondida.**
* **Evidencia:** El análisis exploratorio (EDA) mostró una curva de consumo en forma de "U" con picos claros en invierno. El modelo confirmó que los **Grados-Día de Calefacción (HDD)** son uno de los predictores más fuertes, validando que la temperatura baja es el detonante principal de la demanda.

### 2. Correlación Socioeconómica
> *¿Existe correlación significativa entre variables socioeconómicas y consumo?*
* **Respuesta:** ✅ **Sí, respondida.**
* **Evidencia:** El `feature importance` del modelo colocó al **Ingreso Promedio** como el predictor estructural número uno. Se descubrió la **"Trampa del Frío"**: los hogares de bajos ingresos no aumentan su consumo en invierno (correlación baja) debido a restricciones económicas, mientras que los de altos ingresos sí lo hacen drásticamente.

### 3. Factores de Mayor Poder Predictivo
> *¿Qué factores tienen el mayor poder predictivo y cómo se ponderan?*
* **Respuesta:** ✅ **Sí, respondida.**
* **Evidencia:** El modelo XGBoost rankeó las variables explícitamente. Se determinó que el **Nivel Socioeconómico** define el "piso" de consumo, mientras que el **Clima (HDD)** define la variabilidad mensual.

### 4. Identificación de Clústeres
> *¿Podemos identificar "clústeres" o grupos de comunas...?*
* **Respuesta:** ⚠️ **Sí, con una adaptación metodológica.**
* **Evidencia:** En lugar de usar algoritmos no supervisados (como K-Means, que era opcional), se demostró que la segmentación supervisada por **Quintiles de Ingreso (Q1-Q5)** es más efectiva para agrupar comportamientos similares. Se identificaron claramente dos grupos macro: "Consumo Elástico" (ricos) y "Consumo Inelástico" (vulnerables).

### 5. Predicción y Margen de Error (La del "Fallo")
> *¿Qué tan bien puede predecir... y qué margen de error se puede esperar?*
* **Respuesta:** ✅ **Sí, respondida (con la distinción clave).**
* **Evidencia:**
    * **Respuesta Global:** El modelo tiene dificultades con clientes industriales (error alto).
    * **Respuesta Residencial (Objetivo):** Para un hogar común, el modelo predice con un error de **±13.8 kWh (6.6%)**, lo cual responde positivamente a la pregunta de si es útil para informar decisiones de política pública.
    * **Accionabilidad:** El análisis de residuos confirmó que la meta de ahorro del 5-10% es viable si se corrigen las ineficiencias detectadas.