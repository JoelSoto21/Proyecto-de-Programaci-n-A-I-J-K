from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget
import pathlib

# Carga de la base de datos desde la raíz del proyecto
csv_path = pathlib.Path(__file__).parent.parent / "data.csv"
if not csv_path.exists():
    csv_path = "data.csv"

df = pd.read_csv(csv_path)

# 1. Interfaz de Usuario (UI)
app_ui = ui.page_fluid(
    ui.h2("Tablero de Indicadores de Salud Mental en Estudiantes"),
    
    # Plantilla inicial
    ui.hr(),
    ui.h4("Prueba de la plantilla inicial"),
    ui.input_slider("numero", "Selecciona un número", 0, 100, 50),
    ui.output_text("resultado"),
    ui.hr(),

    # Sección de Sueño, Ansiedad y Depresión
    ui.h3("Análisis de Sueño, Ansiedad y Depresión"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Filtros del Gráfico"),
            ui.input_select(
                id="metrica_salud",
                label="Selecciona el indicador psicológico (Eje Y):",
                choices={
                    "GAD7": "Ansiedad (GAD-7)", 
                    "PHQ9": "Depresión (PHQ-9)"
                }
            ),
            ui.input_select(
                id="metrica_sueno",
                label="Selecciona el indicador de sueño (Eje X):",
                choices={
                    "SleepHours": "Horas de Sueño", 
                    "SleepQuality": "Calidad del Sueño"
                }
            ),
        ),
        ui.card(
            ui.card_header("Gráfico de Dispersión"),
            output_widget("plot_sueno_ansiedad")
        )
    )
)

# 2. Servidor (Lógica)
def server(input, output, session):
    @render.text
    def resultado():
        return f"El número seleccionado es: {input.numero()}"

    @render_widget
    def plot_sueno_ansiedad():
        col_y = input.metrica_salud()
        col_x = input.metrica_sueno()
        
        df_plot = df.copy()
        if "MentalHealthStatus" in df_plot.columns:
            df_plot["EstadoSalud"] = df_plot["MentalHealthStatus"].map({
                1: "Saludable",
                0: "En riesgo",
                True: "Saludable",
                False: "En riesgo"
            })
        else:
            df_plot["EstadoSalud"] = "Desconocido"

        nombres_etiquetas = {
            "SleepHours": "Horas Promedio de Sueño",
            "SleepQuality": "Calidad de Sueño (0-10)",
            "GAD7": "Puntuación de Ansiedad (GAD-7)",
            "PHQ9": "Puntuación de Depresión (PHQ-9)",
            "EstadoSalud": "Estado de Salud Mental"
        }

        fig = px.scatter(
            df_plot,
            x=col_x,
            y=col_y,
            color="EstadoSalud",
            hover_data=["GPA", "AcademicStress"], 
            title=f"Relación entre {nombres_etiquetas.get(col_x, col_x)} y {nombres_etiquetas.get(col_y, col_y)}",
            labels=nombres_etiquetas,
            template="plotly_white"
        )
        return fig

app = App(app_ui, server)