# Análisis de la Salud Mental en Estudiantes Universitarios

### Aplicación interactiva desarrollada con Shiny para Python

## Descripción del proyecto

Este proyecto tiene como propósito analizar los **factores académicos, conductuales y psicosociales asociados con la salud mental de los estudiantes universitarios**, mediante el desarrollo de una aplicación interactiva utilizando **Shiny para Python**.

La aplicación busca facilitar la exploración y visualización de información relacionada con el bienestar psicológico estudiantil, permitiendo identificar posibles patrones y asociaciones entre diferentes variables.

Para ello, se utiliza el conjunto de datos **University Student Mental Health Indicators**, disponible en la plataforma **Kaggle**, que contiene información relacionada con indicadores de ansiedad, depresión, hábitos de sueño, estrés académico, estrés financiero, relaciones sociales y rendimiento académico.

El proyecto combina herramientas de programación, análisis exploratorio de datos y visualización interactiva, con el objetivo de presentar información estadística de manera clara, accesible y comprensible.

---

## Preguntas de investigación

### Pregunta general

**¿Qué relación existe entre los factores académicos, conductuales y psicosociales y el estado de salud mental de los estudiantes universitarios?**

### Preguntas específicas

1. ¿Qué relación existe entre la duración y la calidad del sueño y los niveles de ansiedad y depresión de los estudiantes universitarios?

2. ¿Cómo se relacionan el estrés académico y el estrés financiero con el rendimiento académico de los estudiantes universitarios?

3. ¿Qué relación existe entre el apoyo familiar y la actividad social y el estado de salud mental de los estudiantes universitarios?

---

## Objetivo del proyecto

Analizar la relación entre los factores académicos, conductuales y psicosociales y el bienestar psicológico de los estudiantes universitarios, utilizando herramientas estadísticas y visualizaciones interactivas que faciliten la interpretación de los datos.

## ¿Qué se analizará?

El proyecto se centrará en tres áreas principales:

1. **Sueño y salud mental:** Relación entre la duración y calidad del sueño y los niveles de ansiedad y depresión.

2. **Estrés y rendimiento académico:** Asociación entre el estrés académico, el estrés financiero y el promedio de calificaciones (GPA).

3. **Entorno social y bienestar:** Relación entre el apoyo familiar, la actividad social y los indicadores de salud mental.

## Variables principales 
| Variable | Descripción |
|---|---|
| `` | Descripcion |
| `PHQ-9` | Nivel de depresión (0-27) – Cuestionario de salud del paciente |
| `GAD-7` | Nivel de ansiedad (0-21) - Escala de Trastorno de Ansiedad Generalizada |
| `SleepHours` | Duración media diaria del sueño (3-10 horas) |
| `ExerciseFreq` | Frecuencia de ejercicio físico (0-7 días/semana) |
| `SocialActivity` | Frecuencia de ejercicio físico (0-7 días/semana) |
| `OnlineStress` | Estrés percibido por el aprendizaje en línea (0-10) |
| `GPA` | Rendimiento académico (0-4.0) |
| `FamilySupport` | Apoyo emocional/financiero familiar (0-1) |
| `ScreenTime` | Promedio de exposición a pantallas (1-12 horas/día) |
| `AcademicStress` | Presión por la carga de trabajo académico (0-10) |
| `DietQuality` | Puntuación de nutrición y dieta equilibrada (1-10) |
| `SelfEfficacy` | Confidence in coping with challenges (0-10) |
| `PeerRelationship` | Relación con compañeros de clase (0-10) |
| `FinancialStress` | Intensidad de la carga financiera (0-10) |
| `SleepQuality` | Satisfacción subjetiva con el sueño (0-10) |
| `MentalHealthStatus` | El estado de salud mental se determina mediante: P(Healthy) = 1 / (1 + e^(-Z/10)) |
## Tecnologías

- **Python:** Procesamiento y análisis de datos.
- **Shiny para Python:** Desarrollo de la aplicación interactiva.
- **Git y GitHub:** Control de versiones y trabajo colaborativo.

## ¿Qué se espera desarrollar?

Se pretende construir una aplicación que permita explorar el conjunto de datos mediante **gráficos estadísticos, filtros dinámicos y visualizaciones interactivas**, facilitando la identificación de tendencias y posibles relaciones entre las variables estudiadas.

El proyecto tiene un enfoque exploratorio y académico, por lo que los resultados permitirán identificar asociaciones, pero no establecer relaciones causales.

---

## Referencias

- Casasola Rivera. (2020). Publicación sobre salud mental y educación.
- Cuamba Osorio y Zazueta Sánchez. (2020). Estudio sobre salud mental en estudiantes universitarios.
- Kaggle. (s. f.). *University Student Mental Health Indicators* [Conjunto de datos].
- Paricahua Peralta et al. (2024). Estudio sobre calidad del sueño, salud mental y actividad física en estudiantes universitarios.

> **Nota:** Las referencias deberán completarse con los datos bibliográficos y enlaces de las fuentes originales.

---

## Consideraciones finales

Este proyecto tiene fines académicos y busca contribuir a la comprensión de los factores relacionados con la salud mental de los estudiantes universitarios mediante herramientas de análisis estadístico y visualización interactiva.

Los resultados obtenidos deben interpretarse considerando las características y limitaciones del conjunto de datos utilizado.

**La aplicación no constituye una herramienta de diagnóstico clínico ni sustituye la evaluación de profesionales de salud mental.**
