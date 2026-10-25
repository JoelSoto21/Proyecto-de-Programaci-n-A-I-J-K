from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.h2("Mi primer tablero Shiny"),
    ui.input_slider("numero", "Selecciona un número", 0, 100, 50),
    ui.output_text("resultado"),
)

def server(input, output, session):
    @render.text
    def resultado():
        return f"El número seleccionado es: {input.numero()}"

app = App(app_ui, server)
