from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget
from pathlib import Path

# ==========================================
# CARGA DE DATOS
# ==========================================
BASE = Path(__file__).resolve().parent
CSV = BASE.parent / "data.csv"
if not CSV.exists():
    CSV = BASE / "data.csv"
if not CSV.exists():
    raise FileNotFoundError("No se encontró data.csv en la raíz del proyecto ni en Shiny/.")
df = pd.read_csv(CSV)

# Paleta inspirada en la imagen de referencia (morado -> coral/rosa -> naranja -> amarillo cálido)
PALETA_SUENO = ["#6a51a3", "#9e5db6", "#d6728c", "#eb9678", "#f8b365", "#fdd458"]

# Imagen del pie de página: se lee del disco y se incrusta en la propia página,
# así no depende de que el servidor entregue la carpeta www.
def cargar_imagen_base64(ruta):
    try:
        import base64
        datos = Path(ruta).read_bytes()
        return "data:image/png;base64," + base64.b64encode(datos).decode("ascii")
    except Exception:
        return None

FOOTER_IMG = cargar_imagen_base64(BASE / "www" / "footer.png")

# ==========================================
# COMPONENTES DE DISEÑO
# ==========================================
def encabezado(titulo, descripcion, etiqueta=None):
    return ui.tags.div(
        ui.tags.span(etiqueta, class_="eyebrow") if etiqueta else None,
        ui.h2(titulo),
        ui.p(descripcion),
        class_="section-heading"
    )


def indicador(etiqueta, id_salida):
    """Tarjeta estadística sin íconos, con un valor reactivo."""
    return ui.tags.div(
        ui.tags.span(etiqueta, class_="metric-label"),
        ui.tags.div(ui.output_text(id_salida), class_="metric-value"),
        class_="metric-card"
    )


# ==========================================
# INTERFAZ: CINCO PESTAÑAS
# ==========================================
app_ui = ui.page_fluid(
    ui.include_css(BASE / "estilos.css"),
    ui.tags.div(
        ui.h1("Salud mental en estudiantes universitarios", class_="titulo-principal"),
        ui.p(
            "Exploración interactiva de indicadores de bienestar, hábitos y vida académica.",
            class_="subtitulo-principal"
        ),
        class_="hero-simple"
    ),
    ui.navset_tab(
        # ----------------------------------
        # PESTAÑA 1: INICIO
        # ----------------------------------
        ui.nav_panel(
            "Inicio",
            encabezado(
                "Explora el bienestar estudiantil",
                "Un espacio para descubrir patrones en la salud mental universitaria mediante visualizaciones y datos.",
                "PRESENTACIÓN"
            ),
            ui.layout_columns(
                indicador("Estudiantes en el conjunto", "kpi_estudiantes"),
                indicador("GPA promedio", "kpi_gpa"),
                indicador("Horas de sueño promedio", "kpi_sueno"),
                indicador("Estrés académico promedio", "kpi_estres"),
                col_widths=(3, 3, 3, 3)
            ),
            ui.tags.div(
                ui.tags.div(
                    ui.tags.span("NUESTRO PROPÓSITO", class_="eyebrow"),
                    ui.h3("¿Qué buscamos comprender?"),
                    ui.p(
                        "El proyecto analiza asociaciones entre factores académicos, "
                        "conductuales y psicosociales y el bienestar mental estudiantil. "
                        "Permite explorar tendencias, comparar grupos y construir "
                        "interpretaciones estadísticas sin asumir relaciones causales."
                    ),
                    class_="intro-copy"
                ),
                ui.tags.div(
                    ui.tags.div(ui.tags.span("01", class_="step-number"), ui.tags.strong("Sueño y salud mental"), ui.p("Horas de descanso, calidad del sueño, ansiedad y depresión."), class_="topic-row"),
                    ui.tags.div(ui.tags.span("02", class_="step-number"), ui.tags.strong("Estrés y rendimiento"), ui.p("Estrés académico y financiero en relación con el GPA."), class_="topic-row"),
                    ui.tags.div(ui.tags.span("03", class_="step-number"), ui.tags.strong("Apoyo social y familiar"), ui.p("Exploración de los factores psicosociales y del bienestar."), class_="topic-row"),
                    class_="topics"
                ),
                class_="intro-panel"
            )
        ),
        # ----------------------------------
        # PESTAÑA 2: BASE DE DATOS
        # ----------------------------------
        ui.nav_panel(  #ui.nav_panel() Permite crear una pestaña de navegacion dentro de la aplicacion 
            "Base de datos", #Aca se nombra la pestaña de navegacion
            encabezado(
                "Exploración de la base de datos",
                "Consultá registros con búsqueda por variable, filtros y paginación.",
                "DATOS"
            ),
            #Creacion de los buscadores y filtros de la base de datos
            #Este bloque se encarga de construir los controles con los que el usuario interactúa.

            ui.tags.div( #ui.tags.div() es una funcion que permite crear un contenedor de elementos HTML dentro de la applicacion
                ui.layout_columns( # ui.layout_columns() organiza los elemntos en columnas
                    ui.input_text("buscar", "Buscar registros", placeholder="Escribí un valor para buscar"), #ui.input_text() crea un cuadro de texto para que el usuario ingrese su busqueda
                    ui.input_select("columna", "Buscar en la variable", choices=["Todas"] + list(df.columns)), #ui.input_select() crea un menu despegable para que el usuario seleccione la variable que desea buscar
                    ui.input_select("cantidad", "Registros por página", choices=["10", "25", "50", "100"], selected="10"),
                    col_widths=(4, 5, 3)
                ),
                class_="filter-card"
            ),
            ui.tags.div(
                ui.tags.div(ui.tags.strong("Registros disponibles"), ui.tags.span(ui.output_text("total_registros"), class_="result-counter"), class_="table-heading"), #Esta linea crea un contenedor que muestra el total de registros disponibles en la base de datos
                ui.tags.div(ui.output_data_frame("tabla"), class_="table-scroll"), #Creacion de la tabla interactiva que muestra los datos filtrados
                ui.tags.div( #Aca se crean los botones de paginacion para navegar entre paginas de la tabla
                    ui.input_action_button("anterior", "← Anterior", class_="pagination-btn"),
                    ui.tags.span(ui.output_text("pagina_actual"), class_="page-label"),
                    ui.input_action_button("siguiente", "Siguiente →", class_="pagination-btn"),
                    class_="pagination-row"
                ),
                class_="table-card"
            ), 

            # ----------------------------------
            # DESCRIPCIÓN DE LAS VARIABLES
            # ----------------------------------

            ui.hr(), #Crea una linea horizontal que separa la tabla de la descripccion de las variables

            encabezado(
                "Descripción de las variables",
                "Conocé el significado y la escala de medición "
                "de las variables presentes en la base de datos.",
                "VARIABLES"
            ),

            ui.tags.div( #Esta funcion crea un contenedor que contiene una tabla con la descripcion de las variables
                ui.tags.table( #Crea la tabla HTML que contiene la descripcion de las variables 
                    {"class": "table table-striped table-bordered table-hover"},

                    ui.tags.thead( #Permite contruir el encabezado de la tabla
                        ui.tags.tr( #Permite crear una fila dentro de la tabla
                            ui.tags.th("Variable"),
                            ui.tags.th("Descripción")
                        )
                    ),

                    ui.tags.tbody( 
                        *[
                            ui.tags.tr(
                                ui.tags.td(ui.tags.code(variable)),
                                ui.tags.td(descripcion)
                            )

                            for variable, descripcion in [ #En esta parte se definen las variables y sus descripcciones que se mostraran en la tabla

                                ("PHQ-9",
                                 "Nivel de depresión (0-27) – Cuestionario de salud del paciente"),

                                ("GAD-7",
                                 "Nivel de ansiedad (0-21) – Escala de Trastorno de Ansiedad Generalizada"),

                                ("SleepHours",
                                 "Duración media diaria del sueño (3-10 horas)"),

                                ("ExerciseFreq",
                                 "Frecuencia de ejercicio físico (0-7 días/semana)"),

                                ("SocialActivity",
                                 "Frecuencia de actividades sociales"),

                                ("OnlineStress",
                                 "Estrés percibido por el aprendizaje en línea (0-10)"),

                                ("GPA",
                                 "Rendimiento académico (0-4.0)"),

                                ("FamilySupport",
                                 "Apoyo emocional y financiero familiar (0-1)"),

                                ("ScreenTime",
                                 "Promedio de exposición a pantallas (1-12 horas/día)"),

                                ("AcademicStress",
                                 "Presión por la carga de trabajo académico (0-10)"),

                                ("DietQuality",
                                 "Puntuación de nutrición y dieta equilibrada (1-10)"),

                                ("SelfEfficacy",
                                 "Confianza para afrontar desafíos (0-10)"),

                                ("PeerRelationship",
                                 "Relación con compañeros de clase (0-10)"),

                                ("FinancialStress",
                                 "Intensidad de la carga financiera (0-10)"),

                                ("SleepQuality",
                                 "Satisfacción subjetiva con el sueño (0-10)"),

                                ("MentalHealthStatus",
                                 "El estado de salud mental se determina mediante: "
                                 "P(Healthy) = 1 / (1 + e^(-Z/10))")
                            ]
                        ]
                    )
                ),

                class_="table-card"
            )

        ),  
            

        # ----------------------------------
        # PESTAÑA 3: SUEÑO Y SALUD MENTAL
        # ----------------------------------
        ui.nav_panel(
    "Sueño y Salud Mental",
    encabezado(
        "Sueño, ansiedad y depresión",
        "Explorá cómo se relacionan la duración y calidad del sueño con los indicadores de ansiedad y depresión.",
        "ANÁLISIS 01"
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Personalizar gráfico"),
            ui.input_select(
                "metrica_salud", "Indicador psicológico promedio (eje Y)",
                choices={"GAD7": "Ansiedad (GAD-7)", "PHQ9": "Depresión (PHQ-9)"}
            ),
            ui.input_select(
                "metrica_sueno", "Agrupar por indicador de sueño (eje X)",
                choices={"SleepHours": "Horas de Sueño", "SleepQuality": "Calidad del Sueño"}
            ),
            ui.input_switch(
                "ordenar_sueno_desc", "Ordenar barras de mayor a menor",
                value=False
            ),
            ui.input_switch(
                "mostrar_etiquetas_sueno", "Mostrar valores sobre las barras",
                value=True
            )
        ),
        ui.div(
            ui.card(
                ui.card_header("Promedio del indicador psicológico según sueño"),
                output_widget("plot_sueno_ansiedad")
            ),
            ui.card(
                ui.card_header("Horas de sueño vs. otras variables"),
                ui.input_checkbox_group(
                    "vars_vs_sueno",
                    "Seleccioná las variables a comparar con Horas de Sueño:",
                    choices={
                        "ScreenTime": "Tiempo de Pantalla",
                        "AcademicStress": "Estrés Académico",
                        "OnlineStress": "Estrés Online",
                        "FinancialStress": "Estrés Financiero",
                        "SocialActivity": "Actividad Social",
                        "ExerciseFreq": "Frecuencia de Ejercicio",
                        "DietQuality": "Calidad de Dieta",
                        "SelfEfficacy": "Autoeficacia",
                        "FamilySupport": "Apoyo Familiar",
                        "PeerRelationship": "Relación con Pares",
                        "GPA": "Promedio Académico (GPA)"
                    },
                    selected=["ScreenTime", "AcademicStress", "SocialActivity", "FinancialStress"],
                    inline=True
                ),
                output_widget("plot_sueno_vs_seleccion")
            )
        )
    )
),
        # ----------------------------------
        # PESTAÑA 4: ESTRÉS Y RENDIMIENTO
        # ----------------------------------
        ui.nav_panel(
            "Estrés y Rendimiento",
            encabezado(
                "Estrés y rendimiento académico",
                "Compará el estrés académico y financiero con el promedio de calificaciones (GPA).",
                "ANÁLISIS 02"
            ),
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h4("Personalizar gráfico"),
                    ui.input_select(
                        "tipo_grafico", "Tipo de gráfico",
                        choices={"dispersion": "Gráfico de dispersión", "cajas": "Diagramas de cajas"}
                    ),
                    ui.panel_conditional(
                        "input.tipo_grafico === 'dispersion'",
                        ui.input_select(
                            "tipo_estres", "Tipo de estrés",
                            choices={"AcademicStress": "Estrés académico", "FinancialStress": "Estrés financiero"}
                        )
                    ),
                    ui.hr(),
                    ui.input_slider("n_observaciones", "Número de observaciones", min=1, max=max(1, len(df)), value=min(300, max(1, len(df))), step=1),
                    ui.p(f"Registros totales: {len(df)}", class_="sidebar-note")
                ),
                ui.card(
                    ui.card_header("Relación entre estrés y GPA"),
                    output_widget("plot_estres_gpa"),
                    ui.tags.div(ui.output_text("resumen_observaciones"), class_="figure-footer")
                )
            ),
            ui.tags.div(
                ui.card(ui.card_header("Interpretación estadística"), ui.output_ui("interpretacion_estres")),
                class_="analysis-card"
            )
        ),
        # ----------------------------------
        # PESTAÑA 5: APOYO SOCIAL Y FAMILIAR
        # ----------------------------------
        ui.nav_panel(
            "Apoyo Social y Familiar",
            encabezado(
                "Apoyo social y familiar",
                "Explorá cómo se relacionan el apoyo familiar, la actividad social y las relaciones con compañeros con el estado de salud mental.",
                "ANÁLISIS 03"
            ),
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h4("Personalizar gráfico"),
                    ui.input_select(
                        "variable_social", "Factor social",
                        choices={
                            "FamilySupport": "Apoyo familiar",
                            "SocialActivity": "Actividad social",
                            "PeerRelationship": "Relación con compañeros"
                        }
                    ),
                    ui.input_select(
                        "tipo_grafico_social", "Tipo de gráfico",
                        choices={
                            "barras": "Barras: % de estudiantes saludables",
                            "cajas": "Cajas: indicador psicológico"
                        }
                    ),
                    ui.panel_conditional(
                        "input.tipo_grafico_social === 'cajas'",
                        ui.input_select(
                            "indicador_social", "Indicador psicológico",
                            choices={"PHQ9": "Depresión (PHQ-9)", "GAD7": "Ansiedad (GAD-7)"}
                        )
                    ),
                    ui.input_slider(
                        "n_grupos_social", "Número de grupos",
                        min=3, max=6, value=4, step=1
                    ),
                    ui.p(
                        "Los estudiantes se dividen en grupos del mismo tamaño según el factor elegido.",
                        class_="sidebar-note"
                    )
                ),
                ui.card(
                    ui.card_header("Factores sociales y salud mental"),
                    output_widget("plot_social"),
                    ui.tags.div(ui.output_text("resumen_social"), class_="figure-footer")
                )
            ),
            ui.tags.div(
                ui.card(
                    ui.card_header("Interpretación estadística"),
                    ui.output_ui("interpretacion_social")
                ),
                class_="analysis-card"
            )
        ),
        id="pestanas",
        selected="Inicio"
    ),
    ui.tags.footer(
        ui.tags.img(
            src=FOOTER_IMG or "/footer.png",
            alt="Salud mental universitaria",
            class_="footer-imagen"
        ),
        ui.tags.p(
            "Proyecto académico · Análisis exploratorio · Los resultados no sustituyen una evaluación clínica.",
            class_="footer-nota"
        ),
        class_="app-footer"
    )
)


# ==========================================
# SERVIDOR: SE CONSERVA LA LÓGICA EXISTENTE
# ==========================================
def server(input, output, session):

    # --------------------------------------
    # INDICADORES DE LA PÁGINA INICIO
    # --------------------------------------

    @render.text
    def kpi_estudiantes():
        return f"{len(df):,}".replace(",", ".")

    @render.text
    def kpi_gpa():
        valores = pd.to_numeric(df["GPA"], errors="coerce")
        return f"{valores.mean():.2f}" if valores.notna().any() else "Sin datos"

    @render.text
    def kpi_sueno():
        valores = pd.to_numeric(df["SleepHours"], errors="coerce")
        return f"{valores.mean():.1f} h" if valores.notna().any() else "Sin datos"

    @render.text
    def kpi_estres():
        valores = pd.to_numeric(df["AcademicStress"], errors="coerce")
        return f"{valores.mean():.1f}" if valores.notna().any() else "Sin datos"


    # --------------------------------------
    # PESTAÑA 2: EXPLORACIÓN DE LA BASE DE DATOS
    # --------------------------------------
    #Toda la siguiente parte se encofa en recibir la informacion del usuario y de ahi limpiarla, analizarla y mostrarla en la tabla interactiva
    # Variable para controlar la página actual
    pagina = reactive.value(1)

    # Filtrar los datos según la búsqueda
    @reactive.calc
    def datos_filtrados():

        datos = df.copy()
        busqueda = input.buscar().strip()  #Recupera el texto que el usuario escribió en el buscador que creamos anteriormente en la interfaz, a demas con strip() se eliminan espacios en blanco 

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
            height="450px",
    styles=[
        {
            "style": {
                "min-width": "160px"
            }
        }
    ]
)
        

    # --------------------------------------
    # PESTAÑA 3: GRÁFICO DE SUEÑO Y SALUD MENTAL
    # --------------------------------------

    @render_widget
    def plot_sueno_ansiedad():
        try:
            col_y = input.metrica_salud() or "GAD7"
            col_x = input.metrica_sueno() or "SleepHours"

            if col_x not in df.columns or col_y not in df.columns:
                return px.bar(
                    title="Columnas no encontradas en los datos",
                    template="plotly_white"
                )

            sub = df[[col_x, col_y]].copy()
            sub[col_x] = pd.to_numeric(sub[col_x], errors="coerce")
            sub[col_y] = pd.to_numeric(sub[col_y], errors="coerce")
            sub = sub.dropna()

            if sub.empty:
                return px.bar(
                    title="Sin datos disponibles",
                    template="plotly_white"
                )

            if col_x == "SleepHours":
                bins = [-float("inf"), 5, 6, 7, 8, 9, float("inf")]
                labels = ["< 5h", "5–6h", "6–7h", "7–8h", "8–9h", "9+ h"]
                sub["Grupo"] = pd.cut(sub[col_x], bins=bins, labels=labels, right=False).astype(str)
                etiqueta_x = "Horas de Sueño"
                orden_x = labels
            else:
                sub["Grupo"] = sub[col_x].round().clip(lower=0, upper=10).astype(int).astype(str)
                etiqueta_x = "Calidad del Sueño"
                orden_x = [str(i) for i in range(0, 11)]

            df_bar = (
                sub.groupby("Grupo", as_index=False)
                .agg(
                    Promedio=(col_y, "mean"),
                    Estudiantes=(col_y, "count")
                )
            )
            df_bar["Promedio"] = df_bar["Promedio"].round(2)

            if bool(input.ordenar_sueno_desc()):
                df_bar = df_bar.sort_values("Promedio", ascending=False)
            else:
                mapa_orden = {k: i for i, k in enumerate(orden_x)}
                df_bar["orden_tmp"] = df_bar["Grupo"].map(mapa_orden).fillna(999)
                df_bar = df_bar.sort_values("orden_tmp").drop(columns=["orden_tmp"])

            etiqueta_y = "Ansiedad (GAD-7)" if col_y == "GAD7" else "Depresión (PHQ-9)"
            mostrar_txt = bool(input.mostrar_etiquetas_sueno())

            paleta = list(PALETA_SUENO) if "PALETA_SUENO" in globals() and len(PALETA_SUENO) > 0 else ["#7B5EA7", "#9B7EC4", "#5A4280", "#B89FE0", "#463266", "#D0BFEF"]
            while len(paleta) < max(1, len(df_bar)):
                paleta = paleta + paleta

            fig = px.bar(
                df_bar,
                x="Grupo",
                y="Promedio",
                color="Grupo",
                color_discrete_sequence=paleta,
                text="Promedio" if mostrar_txt else None,
                hover_data={"Estudiantes": True, "Promedio": ":.2f"},
                labels={
                    "Grupo": etiqueta_x,
                    "Promedio": f"Promedio {etiqueta_y}",
                },
                title=f"Promedio de {etiqueta_y} según {etiqueta_x}",
                template="plotly_white"
            )

            if mostrar_txt:
                fig.update_traces(
                    texttemplate="%{text:.2f}",
                    textposition="outside",
                    cliponaxis=False
                )

            max_val = float(df_bar["Promedio"].max()) if not df_bar.empty else 1.0
            fig.update_layout(
                showlegend=False,
                xaxis={"type": "category"},
                yaxis={"range": [0, max_val * 1.18 if max_val > 0 else 1]},
                margin=dict(t=60, b=50, l=50, r=20)
            )
            return fig

        except Exception as e:
            return px.bar(
                title=f"Error al generar gráfico: {e}",
                template="plotly_white"
            )
   
    # ==========================================
    # PESTAÑA 4: ESTRÉS Y RENDIMIENTO
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
                    "en los distintos niveles de ambos tipos de estrés."
                )
            )

    # ==========================================
    # PESTAÑA 5: APOYO SOCIAL Y FAMILIAR
    # ==========================================

    NOMBRES_SOCIAL = {
        "FamilySupport": "Apoyo familiar",
        "SocialActivity": "Actividad social",
        "PeerRelationship": "Relación con compañeros"
    }

    @reactive.calc
    def datos_social():
        """Prepara los datos y los divide en grupos del mismo tamaño (cuantiles)."""
        variable = input.variable_social()
        columnas = [variable, "MentalHealthStatus", "PHQ9", "GAD7"]

        datos = df[columnas].copy()
        for columna in columnas:
            datos[columna] = pd.to_numeric(datos[columna], errors="coerce")
        datos = datos.dropna()

        # Se calculan los límites de los grupos y se crean etiquetas legibles
        _, bordes = pd.qcut(
            datos[variable],
            q=input.n_grupos_social(),
            retbins=True,
            duplicates="drop"
        )
        etiquetas = [
            f"{bordes[i]:.2f} – {bordes[i + 1]:.2f}"
            for i in range(len(bordes) - 1)
        ]
        datos["Grupo"] = pd.cut(
            datos[variable],
            bins=bordes,
            labels=etiquetas,
            include_lowest=True
        )
        return datos, etiquetas

    @render_widget
    def plot_social():
        datos, etiquetas = datos_social()
        variable = input.variable_social()
        nombre = NOMBRES_SOCIAL[variable]

        # Misma paleta que usa el gráfico de Sueño y Salud Mental
        paleta = (
            list(PALETA_SUENO) if "PALETA_SUENO" in globals() and len(PALETA_SUENO) > 0
            else ["#6a51a3", "#9e5db6", "#d6728c", "#eb9678", "#f8b365", "#fdd458"]
        )
        while len(paleta) < max(1, len(etiquetas)):
            paleta = paleta + paleta

        def color_texto(color_hex):
            """Devuelve blanco u oscuro, el que mejor se lea sobre el color de la barra."""
            try:
                canales = [int(color_hex[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            except Exception:
                return "#ffffff"
            lineal = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
            luminancia = 0.2126 * lineal[0] + 0.7152 * lineal[1] + 0.0722 * lineal[2]
            contraste_blanco = 1.05 / (luminancia + 0.05)
            contraste_oscuro = (luminancia + 0.05) / 0.076
            return "#ffffff" if contraste_blanco >= contraste_oscuro else "#2d2d2d"

        if input.tipo_grafico_social() == "barras":
            # Porcentaje de estudiantes con estado de salud mental "saludable" en cada grupo
            resumen = (
                datos.groupby("Grupo", observed=True)["MentalHealthStatus"]
                .agg(["mean", "size"])
                .reset_index()
            )
            resumen["Porcentaje"] = resumen["mean"] * 100
            resumen["Etiqueta"] = resumen["Porcentaje"].round(1).astype(str) + "%"
            resumen = resumen.rename(columns={"size": "Estudiantes"})
            promedio_general = datos["MentalHealthStatus"].mean() * 100

            # Altura máxima del eje Y, con espacio arriba para las etiquetas
            y_maximo = max(resumen["Porcentaje"].max(), promedio_general) * 1.3
            valores = {str(g): v for g, v in zip(resumen["Grupo"], resumen["Porcentaje"])}

            fig = px.bar(
                resumen,
                x="Grupo",
                y="Porcentaje",
                color="Grupo",
                color_discrete_sequence=paleta,
                text="Etiqueta",
                hover_data={"Estudiantes": True, "Porcentaje": ":.1f"},
                category_orders={"Grupo": etiquetas},
                labels={
                    "Grupo": f"{nombre} (rango del grupo)",
                    "Porcentaje": "Estudiantes saludables (%)"
                },
                title=f"Porcentaje de estudiantes saludables según {nombre.lower()}",
                template="plotly_white"
            )

            # Etiqueta de cada barra: afuera por defecto; si la línea del promedio
            # pasaría justo encima de la etiqueta, se coloca dentro de la barra
            def ajustar_etiqueta(traza):
                valor = valores.get(str(traza.name), 0)
                if valor < promedio_general <= valor + 0.08 * y_maximo:
                    traza.update(
                        textposition="inside",
                        insidetextanchor="end",
                        textfont=dict(size=13, color=color_texto(traza.marker.color))
                    )
                else:
                    traza.update(
                        textposition="outside",
                        textfont=dict(size=13, color="#333333")
                    )
                traza.update(cliponaxis=False)

            fig.for_each_trace(ajustar_etiqueta)

            # Línea del promedio general, sin texto encima para que no choque con las barras
            fig.add_hline(
                y=promedio_general,
                line_dash="dash",
                line_color="#4a4a4a",
                line_width=1.5
            )
            # El texto del promedio va fuera del gráfico, arriba a la derecha
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=1,
                y=1.02,
                xanchor="right",
                yanchor="bottom",
                showarrow=False,
                text=f"– – –  Promedio general: {promedio_general:.1f}%",
                font=dict(size=12, color="#4a4a4a")
            )

            fig.update_xaxes(type="category")
            fig.update_yaxes(range=[0, y_maximo])
            fig.update_layout(showlegend=False, height=500)

        else:
            indicador = input.indicador_social()
            nombre_indicador = "Depresión (PHQ-9)" if indicador == "PHQ9" else "Ansiedad (GAD-7)"

            fig = px.box(
                datos,
                x="Grupo",
                y=indicador,
                color="Grupo",
                color_discrete_sequence=paleta,
                points="outliers",
                category_orders={"Grupo": etiquetas},
                labels={
                    "Grupo": f"{nombre} (rango del grupo)",
                    indicador: nombre_indicador
                },
                title=f"{nombre_indicador} según {nombre.lower()}",
                template="plotly_white"
            )
            fig.update_xaxes(type="category")
            fig.update_layout(showlegend=False, height=500)

        fig.update_layout(title_x=0.5, margin=dict(t=90, b=70))
        return fig

    @render.text
    def resumen_social():
        datos, _ = datos_social()
        return f"Estudiantes analizados: {len(datos)}"

    @render.ui
    def interpretacion_social():
        datos, _ = datos_social()
        variable = input.variable_social()
        nombre = NOMBRES_SOCIAL[variable].lower()

        if len(datos) < 3:
            return ui.p("Se requieren al menos 3 observaciones para realizar el análisis.")

        def describir(r):
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
            direccion = "positiva" if r > 0 else "negativa" if r < 0 else "nula"
            return f"r = {r:.3f} (asociación {direccion} {fuerza})"

        r_estado = datos[variable].corr(datos["MentalHealthStatus"])
        r_phq = datos[variable].corr(datos["PHQ9"])
        r_gad = datos[variable].corr(datos["GAD7"])

        resumen = datos.groupby("Grupo", observed=True)["MentalHealthStatus"].mean() * 100
        mejor, peor = resumen.idxmax(), resumen.idxmin()

        return ui.div(
            ui.h4("Resumen estadístico"),
            ui.p(f"Porcentaje general de estudiantes saludables: {datos['MentalHealthStatus'].mean() * 100:.1f}%"),
            ui.p(
                f"Grupo con mayor porcentaje de estudiantes saludables ({nombre}: {mejor}): {resumen.max():.1f}%. "
                f"Grupo con menor porcentaje ({nombre}: {peor}): {resumen.min():.1f}%."
            ),
            ui.hr(),
            ui.h4(f"Correlaciones de Pearson con {nombre}"),
            ui.p(f"Estado de salud mental (0 = en riesgo, 1 = saludable): {describir(r_estado)}."),
            ui.p(f"Depresión (PHQ-9): {describir(r_phq)}."),
            ui.p(f"Ansiedad (GAD-7): {describir(r_gad)}."),
            ui.hr(),
            ui.p(
                "Las correlaciones describen asociaciones lineales y no implican causalidad. "
                "Cuando |r| es muy cercano a 0, el factor social elegido casi no explica "
                "las diferencias en salud mental dentro de este conjunto de datos."
            )
        )

app = App(app_ui, server)