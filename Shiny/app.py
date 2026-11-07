
from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget
import pathlib

# Prueba Ianna

# ==========================================
# CARGA DE LA BASE DE DATOS
# ==========================================

# Carga de la base de datos desde la raíz del proyecto
csv_path = pathlib.Path(__file__).parent.parent / "data.csv"

if not csv_path.exists():
    csv_path = "data.csv"

df = pd.read_csv(csv_path)


# ==========================================
# 1. INTERFAZ DE USUARIO (UI)
# ==========================================

app_ui = ui.page_fluid(

    ui.h2("Tablero de Indicadores de Salud Mental en Estudiantes"),
    ui.hr(),

    # Navegación principal con 4 pestañas
    ui.navset_tab(

        # ==================================
        # PESTAÑA 1: INICIO
        # ==================================

        ui.nav_panel(
            "Inicio",

            ui.h3("Bienvenido al proyecto"),

            ui.p(
                "Esta aplicación tiene como propósito explorar "
                "los factores académicos, conductuales y "
                "psicosociales relacionados con la salud mental "
                "de los estudiantes universitarios."
            ),

            ui.p(
                "Utiliza las pestañas superiores para explorar "
                "los diferentes análisis estadísticos."
            ),

            ui.hr(),

            # Plantilla inicial
            ui.h4("Prueba de la plantilla inicial"),

            ui.input_slider(
                "numero",
                "Selecciona un número",
                0,
                100,
                50
            ),

            ui.output_text("resultado")
        ),

        # ==================================
        # PESTAÑA 2: SUEÑO Y SALUD MENTAL
        # ==================================

        ui.nav_panel(
            "Sueño y Salud Mental",

            ui.h3("Análisis de Sueño, Ansiedad y Depresión"),

            ui.p(
                "En esta sección se explora la relación entre "
                "la duración y calidad del sueño y los niveles "
                "de ansiedad y depresión de los estudiantes."
            ),

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
                    )
                ),

                ui.card(
                    ui.card_header("Gráfico de Dispersión"),
                    output_widget("plot_sueno_ansiedad")
                )
            )
        ),

        # ==================================
        # PESTAÑA 3: ESTRÉS Y RENDIMIENTO
        # ==================================

ui.nav_panel(
    "Estrés y Rendimiento",

    ui.h3("Análisis de Estrés y Rendimiento Académico"),

    ui.p(
        "Explora la relación entre el estrés académico, "
        "el estrés financiero y el promedio de "
        "calificaciones (GPA) de los estudiantes."
    ),

    ui.layout_sidebar(

        ui.sidebar(
            ui.h4("Filtros del Gráfico"),

            # Seleccionar tipo de estrés
            ui.input_select(
                "tipo_estres",
                "Selecciona el tipo de estrés:",
                choices={
                    "AcademicStress": "Estrés Académico",
                    "FinancialStress": "Estrés Financiero"
                }
            ),

            ui.hr(),

            # Seleccionar tipo de gráfico
            ui.input_select(
                "tipo_grafico",
                "Selecciona el tipo de gráfico:",
                choices={
                    "dispersion": "Gráfico de Dispersión",
                    "cajas": "Diagrama de Cajas"
                }
            ),

            ui.hr(),

            # Barra para seleccionar observaciones
            ui.input_slider(
                "n_observaciones",
                "Número de observaciones:",
                min=1,
                max=len(df),
                value=min(300, len(df)),
                step=1
            ),

            ui.p(
                f"Total de registros disponibles: {len(df)}"
            )
        ),

        ui.card(
            ui.card_header(
                "Relación entre el Estrés y el GPA"
            ),

            output_widget("plot_estres_gpa"),

            ui.output_text("resumen_observaciones")
        )
    ),

    ui.hr(),

    # Interpretación debajo del gráfico
    ui.card(
        ui.card_header("Interpretación Estadística"),

        ui.output_ui("interpretacion_estres")
    )
        ),
        # ==================================
        # PESTAÑA 4: APOYO SOCIAL Y FAMILIAR
        # ==================================

        ui.nav_panel(
            "Apoyo Social y Familiar",

            ui.h3("Análisis de Factores Psicosociales"),

            ui.p(
                "Esta sección estará destinada a examinar "
                "la relación entre el apoyo familiar, "
                "la actividad social y el estado de "
                "salud mental de los estudiantes."
            ),

            ui.card(
                ui.card_header("Visualizaciones estadísticas"),
                ui.p("Gráficos en desarrollo.")
            )
        ),

        id="pestanas",
        selected="Inicio"
    )
)


# ==========================================
# 2. SERVIDOR (LÓGICA)
# ==========================================

def server(input, output, session):

    # --------------------------------------
    # PESTAÑA 1: PRUEBA DEL SLIDER
    # --------------------------------------

    @render.text
    def resultado():
        return f"El número seleccionado es: {input.numero()}"

    # --------------------------------------
    # PESTAÑA 2: GRÁFICO DE SUEÑO Y SALUD MENTAL
    # --------------------------------------

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
            title=(
                f"Relación entre "
                f"{nombres_etiquetas.get(col_x, col_x)} "
                f"y {nombres_etiquetas.get(col_y, col_y)}"
            ),
            labels=nombres_etiquetas,
            template="plotly_white"
        )

        return fig
    
   
    # ==========================================
    # PESTAÑA 3: ESTRÉS Y RENDIMIENTO
    # ==========================================

    @reactive.calc
    def datos_estres():

        variable = input.tipo_estres()
        n = input.n_observaciones()

        # Convertir variables a numéricas
        datos = df[[variable, "GPA"]].copy()

        datos[variable] = pd.to_numeric(
            datos[variable], errors="coerce"
        )

        datos["GPA"] = pd.to_numeric(
            datos["GPA"], errors="coerce"
        )

        datos = datos.dropna()

        # Seleccionar una muestra aleatoria reproducible
        # La semilla fija evita que cambie al alternar gráficos
        n = min(n, len(datos))

        if n > 0:
            datos = datos.sample(
                n=n,
                random_state=42
            )

        return datos

    # ==========================================
    # GRÁFICO INTERACTIVO
    # ==========================================

    @render_widget
    def plot_estres_gpa():

        variable = input.tipo_estres()
        tipo = input.tipo_grafico()
        datos = datos_estres().copy()

        nombres = {
            "AcademicStress": "Estrés Académico",
            "FinancialStress": "Estrés Financiero"
        }

        nombre = nombres[variable]

        if tipo == "dispersion":

            fig = px.scatter(
                datos,
                x=variable,
                y="GPA",
                color=variable,
                title=f"Relación entre {nombre} y GPA",
                labels={
                    variable: nombre,
                    "GPA": "Promedio de Calificaciones (GPA)"
                },
                template="plotly_white",
                opacity=0.6
            )

            fig.update_traces(
                marker=dict(size=8)
            )

            fig.update_layout(
                coloraxis_showscale=False
            )

        else:

            # Tratar los niveles de estrés como categorías
            datos["NivelEstres"] = datos[variable].astype(str)

            orden = [
                str(x)
                for x in sorted(datos[variable].unique())
            ]

            fig = px.box(
                datos,
                x="NivelEstres",
                y="GPA",
                color="NivelEstres",
                points="outliers",
                category_orders={
                    "NivelEstres": orden
                },
                title=f"Distribución del GPA según {nombre}",
                labels={
                    "NivelEstres": nombre,
                    "GPA": "Promedio de Calificaciones (GPA)"
                },
                template="plotly_white"
            )

            fig.update_layout(
                showlegend=False
            )

        fig.update_layout(
            title_x=0.5,
            height=500,
            margin=dict(t=70, b=60)
        )

        return fig

    # ==========================================
    # CONTADOR DE OBSERVACIONES
    # ==========================================

    @render.text
    def resumen_observaciones():

        n = len(datos_estres())

        return f"Observaciones utilizadas en el gráfico: {n}"

    # ==========================================
    # INTERPRETACIÓN AUTOMÁTICA
    # ==========================================

    @render.ui
    def interpretacion_estres():

        variable = input.tipo_estres()
        tipo = input.tipo_grafico()

        datos = datos_estres()

        nombres = {
            "AcademicStress": "estrés académico",
            "FinancialStress": "estrés financiero"
        }

        nombre = nombres[variable]
        n = len(datos)

        if n < 3:
            return ui.p(
                "Selecciona al menos 3 observaciones "
                "válidas para realizar el análisis."
            )

        promedio_gpa = datos["GPA"].mean()
        mediana_gpa = datos["GPA"].median()

        # Calcular correlación de Pearson
        if (
            datos[variable].nunique() > 1
            and datos["GPA"].nunique() > 1
        ):
            r = datos[variable].corr(datos["GPA"])
        else:
            r = float("nan")

        if pd.isna(r):
            texto_correlacion = (
                "No es posible calcular la correlación "
                "con las observaciones seleccionadas."
            )
            valor_r = "No disponible"

        else:
            valor_r = f"{r:.3f}"

            # Intensidad de la asociación
            if abs(r) < 0.20:
                fuerza = "muy débil"
            elif abs(r) < 0.40:
                fuerza = "débil"
            elif abs(r) < 0.60:
                fuerza = "moderada"
            elif abs(r) < 0.80:
                fuerza = "fuerte"
            else:
                fuerza = "muy fuerte"

            # Dirección
            if r > 0:
                direccion = "positiva"
                tendencia = (
                    "los estudiantes con mayor nivel de estrés "
                    "tienden a presentar un GPA más alto"
                )
            elif r < 0:
                direccion = "negativa"
                tendencia = (
                    "los estudiantes con mayor nivel de estrés "
                    "tienden a presentar un GPA más bajo"
                )
            else:
                direccion = "nula"
                tendencia = (
                    "no se observa una relación lineal"
                )

            texto_correlacion = (
                f"Se identifica una asociación lineal "
                f"{direccion} de intensidad {fuerza} "
                f"entre el {nombre} y el GPA. "
                f"En la muestra analizada, {tendencia}."
            )

        # Interpretación según el tipo de gráfico
        if tipo == "dispersion":

            texto_grafico = (
                "El gráfico de dispersión permite observar "
                "cómo se distribuyen las calificaciones "
                "individuales según los niveles de estrés. "
                "La correlación resume la tendencia lineal "
                "entre ambas variables."
            )

        else:

            texto_grafico = (
                "El diagrama de cajas permite comparar "
                "la distribución del GPA en cada nivel "
                "de estrés. La línea central de cada caja "
                "representa la mediana, mientras que la "
                "caja representa el rango intercuartílico. "
                "Los puntos externos indican posibles "
                "valores atípicos."
            )

        return ui.div(

            ui.h4("Resumen de los datos"),

            ui.p(
                ui.strong("Observaciones analizadas: "),
                str(n)
            ),

            ui.p(
                ui.strong("GPA promedio: "),
                f"{promedio_gpa:.2f}"
            ),

            ui.p(
                ui.strong("Mediana del GPA: "),
                f"{mediana_gpa:.2f}"
            ),

            ui.p(
                ui.strong("Correlación de Pearson: "),
                valor_r
            ),

            ui.hr(),

            ui.h4("Interpretación del gráfico"),

            ui.p(texto_grafico),

            ui.h4("Interpretación estadística"),

            ui.p(texto_correlacion),

            ui.hr(),

            ui.p(
                "Nota: Los resultados corresponden a una "
                "muestra aleatoria reproducible de los datos "
                "válidos. Las asociaciones no implican "
                "relaciones de causa y efecto."
            )
        )


# ==========================================
# 3. CREACIÓN DE LA APLICACIÓN
# ==========================================

app = App(app_ui, server)
