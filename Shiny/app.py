from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget
import pathlib

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

            # ==================================
            # DATOS TABULARES
            # ==================================

            ui.h4("Exploración de la base de datos"),

            ui.p(
            "En esta sección se pueden consultar los registros "
            "de la base de datos mediante herramientas de búsqueda, "
            "filtrado y paginación."
            ),

        ui.layout_columns(
            ui.input_text(
                "buscar",
                "Buscar registros:",
            placeholder="Escriba un valor para buscar"
         ),

        ui.input_select(
            "columna",
            "Buscar en la variable:",
            choices=["Todas"] + list(df.columns)
         ),

        ui.input_select(
            "cantidad",
            "Registros por página:",
            choices=["10", "25", "50", "100"],
            selected="10"
         )
    ),

ui.hr(),

ui.output_text("total_registros"),

ui.output_data_frame("tabla"),

ui.layout_columns(
    ui.input_action_button("anterior", "Anterior"),
    ui.output_text("pagina_actual"),
    ui.input_action_button("siguiente", "Siguiente")
  )
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

                    ui.input_select(
                        "tipo_grafico",
                        "Selecciona el tipo de gráfico:",
                        choices={
                            "dispersion": "Gráfico de Dispersión",
                            "cajas": "Diagrama de Cajas"
                        }
                    ),

                    # Solo se muestra para el gráfico de dispersión
                    ui.panel_conditional(
                        "input.tipo_grafico === 'dispersion'",

                        ui.input_select(
                            "tipo_estres",
                            "Selecciona el tipo de estrés:",
                            choices={
                                "AcademicStress": "Estrés Académico",
                                "FinancialStress": "Estrés Financiero"
                            }
                        )
                    ),

                    ui.hr(),

                    ui.input_slider(
                        "n_observaciones",
                        "Número de observaciones:",
                        min=1,
                        max=len(df),
                        value=min(300, len(df)),
                        step=1
                    ),

                    ui.p(f"Total de registros: {len(df)}")
                ),

                ui.card(
                    ui.card_header("Relación entre el Estrés y el GPA"),
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
# Variable para controlar la página actual
    pagina = reactive.value(1)

    # Filtrar los datos según la búsqueda
    @reactive.calc
    def datos_filtrados():

        datos = df.copy()
        busqueda = input.buscar().strip()

        if busqueda:

            if input.columna() == "Todas":
                mascara = datos.astype(str).apply(
                    lambda col: col.str.contains(
                        busqueda,
                        case=False,
                        na=False,
                        regex=False
                    )
                ).any(axis=1)

            else:
                mascara = datos[input.columna()].astype(str).str.contains(
                    busqueda,
                    case=False,
                    na=False,
                    regex=False
                )

            datos = datos[mascara]

        return datos

    # Calcular el número total de páginas
    @reactive.calc
    def numero_paginas():

        cantidad = int(input.cantidad())
        total = len(datos_filtrados())

        return max(1, (total + cantidad - 1) // cantidad)

    # Reiniciar página al modificar la búsqueda
    @reactive.effect
    @reactive.event(input.buscar, input.columna, input.cantidad)
    def reiniciar_pagina():
        pagina.set(1)

    # Avanzar de página
    @reactive.effect
    @reactive.event(input.siguiente)
    def avanzar():
        pagina.set(min(pagina() + 1, numero_paginas()))

    # Retroceder de página
    @reactive.effect
    @reactive.event(input.anterior)
    def retroceder():
        pagina.set(max(1, pagina() - 1))

    # Mostrar cantidad de registros encontrados
    @render.text
    def total_registros():
        return f"Registros encontrados: {len(datos_filtrados())}"

    # Mostrar número de página actual
    @render.text
    def pagina_actual():
        return f"Página {min(pagina(), numero_paginas())} de {numero_paginas()}"

    # Mostrar tabla interactiva
    @render.data_frame
    def tabla():

        datos = datos_filtrados()
        cantidad = int(input.cantidad())
        actual = min(pagina(), numero_paginas())

        inicio = (actual - 1) * cantidad
        fin = inicio + cantidad

        return render.DataGrid(
            datos.iloc[inicio:fin].reset_index(drop=True),
            filters=True,
            width="100%",
            height="450px"
        )

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

    
    # ==========================================
    # PESTAÑA 3: ESTRÉS Y RENDIMIENTO
    # ==========================================

    @reactive.calc
    def datos_estres():

        columnas = [
            "AcademicStress",
            "FinancialStress",
            "GPA"
        ]

        datos = df[columnas].copy()

        for columna in columnas:
            datos[columna] = pd.to_numeric(
                datos[columna],
                errors="coerce"
            )

        # Conservamos registros completos
        datos = datos.dropna()

        n = min(input.n_observaciones(), len(datos))

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


        datos = datos_estres().copy()
        tipo = input.tipo_grafico()

        nombres = {
            "AcademicStress": "Estrés Académico",
            "FinancialStress": "Estrés Financiero"
        }

        if tipo == "dispersion":

            variable = input.tipo_estres()
            nombre = nombres[variable]

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
                coloraxis_showscale=False,
                height=500
            )

        else:

            # Convertir los dos tipos de estrés
            # a formato largo
            datos_largos = datos.melt(
                id_vars="GPA",
                value_vars=[
                    "AcademicStress",
                    "FinancialStress"
                ],
                var_name="TipoEstres",
                value_name="NivelEstres"
            )

            datos_largos["TipoEstres"] = (
                datos_largos["TipoEstres"].map(nombres)
            )

            # Agrupar los niveles de estrés
            # en intervalos para facilitar la lectura
            etiquetas = [
                "Hasta 2",
                "2 a 4",
                "4 a 6",
                "6 a 8",
                "Más de 8"
            ]

            datos_largos["GrupoEstres"] = pd.cut(
                datos_largos["NivelEstres"],
                bins=[
                    float("-inf"),
                    2, 4, 6, 8,
                    float("inf")
                ],
                labels=etiquetas
            )

            # Dos diagramas de cajas:
            # académico y financiero
            fig = px.box(
                datos_largos,
                x="GrupoEstres",
                y="GPA",
                color="TipoEstres",
                facet_col="TipoEstres",
                points="outliers",
                category_orders={
                    "GrupoEstres": etiquetas,
                    "TipoEstres": [
                        "Estrés Académico",
                        "Estrés Financiero"
                    ]
                },
                labels={
                    "GrupoEstres": "Nivel de Estrés",
                    "GPA": "Promedio de Calificaciones (GPA)"
                },
                title=(
                    "Distribución del GPA según "
                    "Estrés Académico y Financiero"
                ),
                template="plotly_white"
            )

            fig.update_layout(
                showlegend=False,
                height=550
            )

            # Limpiar títulos de los paneles
            fig.for_each_annotation(
                lambda a: a.update(
                    text=a.text.split("=")[-1]
                )
            )

        fig.update_layout(
            title_x=0.5,
            margin=dict(t=90, b=70)
        )

        return fig

    # ==========================================
    # CONTADOR DE OBSERVACIONES
    # ==========================================

    @render.text
    def resumen_observaciones():

        n = len(datos_estres())

        return (
            f"Estudiantes analizados: {n}"
        )

    # ==========================================
    # INTERPRETACIÓN AUTOMÁTICA
    # ==========================================

    @render.ui
    def interpretacion_estres():

        datos = datos_estres()
        tipo = input.tipo_grafico()
        n = len(datos)

        if n < 3:
            return ui.p(
                "Se requieren al menos 3 observaciones "
                "para realizar el análisis."
            )

        promedio = datos["GPA"].mean()
        mediana = datos["GPA"].median()

        def analizar_correlacion(variable):

            if (
                datos[variable].nunique() < 2
                or datos["GPA"].nunique() < 2
            ):
                return (
                    "No es posible calcular la correlación "
                    "con esta selección."
                )

            r = datos[variable].corr(datos["GPA"])

            if pd.isna(r):
                return "Correlación no disponible."

            magnitud = abs(r)

            if magnitud < 0.20:
                fuerza = "muy débil"
            elif magnitud < 0.40:
                fuerza = "débil"
            elif magnitud < 0.60:
                fuerza = "moderada"
            elif magnitud < 0.80:
                fuerza = "fuerte"
            else:
                fuerza = "muy fuerte"

            if r > 0:
                direccion = "positiva"
                tendencia = (
                    "un GPA más alto"
                )
            elif r < 0:
                direccion = "negativa"
                tendencia = (
                    "un GPA más bajo"
                )
            else:
                direccion = "nula"
                tendencia = (
                    "ninguna tendencia lineal"
                )

            return (
                f"r = {r:.3f}. Se observa una asociación "
                f"lineal {direccion} de intensidad {fuerza}. "
                f"Los niveles más altos de estrés tienden "
                f"a relacionarse con {tendencia}."
                if r != 0 else
                "r = 0.000. No se observa "
                "una asociación lineal."
            )

        # ----------------------------------
        # INTERPRETACIÓN DE DISPERSIÓN
        # ----------------------------------

        if tipo == "dispersion":

            variable = input.tipo_estres()

            nombre = (
                "académico"
                if variable == "AcademicStress"
                else "financiero"
            )

            return ui.div(

                ui.h4("Resumen estadístico"),

                ui.p(
                    f"Estudiantes analizados: {n}"
                ),

                ui.p(
                    f"GPA promedio: {promedio:.2f}"
                ),

                ui.p(
                    f"Mediana del GPA: {mediana:.2f}"
                ),

                ui.hr(),

                ui.h4(
                    f"Interpretación del estrés {nombre}"
                ),

                ui.p(analizar_correlacion(variable)),

                ui.p(
                    "El gráfico permite observar la "
                    "distribución individual de las "
                    "calificaciones según el nivel de estrés."
                )
            )

        # ----------------------------------
        # INTERPRETACIÓN DE CAJAS
        # ----------------------------------

        else:

            # Resumen de medianas por intervalos
            etiquetas = [
                "Hasta 2",
                "2 a 4",
                "4 a 6",
                "6 a 8",
                "Más de 8"
            ]

            def resumen_cajas(variable):

                grupos = pd.cut(
                    datos[variable],
                    bins=[
                        float("-inf"),
                        2, 4, 6, 8,
                        float("inf")
                    ],
                    labels=etiquetas
                )

                resumen = (
                    datos.assign(GrupoEstres=grupos)
                    .groupby(
                        "GrupoEstres",
                        observed=True
                    )["GPA"]
                    .agg(["median", "count"])
                )

                partes = []

                for grupo, fila in resumen.iterrows():
                    partes.append(
                        f"{grupo}: mediana {fila['median']:.2f} "
                        f"(n={int(fila['count'])})"
                    )

                return "; ".join(partes)

            return ui.div(

                ui.h4("Resumen estadístico general"),

                ui.p(
                    f"Estudiantes analizados: {n}"
                ),

                ui.p(
                    f"GPA promedio: {promedio:.2f}"
                ),

                ui.p(
                    f"Mediana del GPA: {mediana:.2f}"
                ),

                ui.hr(),

                ui.h4("1. Estrés Académico"),

                ui.p(
                    analizar_correlacion("AcademicStress")
                ),

                ui.p(
                    "Medianas del GPA por nivel de "
                    "estrés académico: "
                    + resumen_cajas("AcademicStress")
                ),

                ui.hr(),

                ui.h4("2. Estrés Financiero"),

                ui.p(
                    analizar_correlacion("FinancialStress")
                ),

                ui.p(
                    "Medianas del GPA por nivel de "
                    "estrés financiero: "
                    + resumen_cajas("FinancialStress")
                ),

                ui.hr(),

                ui.h4("3. Comparación general"),

                ui.p(
                    "Los diagramas de cajas permiten "
                    "comparar la distribución del GPA "
                    "en los distintos niveles de ambos "
                    "tipos de estrés. Las medianas y "
                    "la dispersión ayudan a identificar "
                    "posibles diferencias entre grupos."
                ),

                ui.p(
                    "Las correlaciones de Pearson "
                    "describen la asociación lineal "
                    "de cada tipo de estrés con el GPA. "
                    "No representan una relación causal."
                )
            )



# ==========================================
# 3. CREACIÓN DE LA APLICACIÓN
# ==========================================

app = App(app_ui, server)
