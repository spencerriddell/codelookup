from shiny import App, ui, render, reactive

app_ui = ui.page_fluid(
    ui.h2("CodeLookup: SAS Code Generator"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_text("lookup_term", "Lookup term", placeholder="e.g., ICD10: I10"),
            ui.input_text("dataset", "Dataset name", placeholder="e.g., claims"),
            ui.input_text("code_column", "Code column", placeholder="e.g., diag_code"),
            ui.input_action_button("generate", "Generate SAS code"),
            ui.hr(),
            ui.markdown("""
- Enter lookup term(s) and metadata.
- Click Generate to produce SAS code.
- Copy/paste into your SAS workflow.
            """),
        ),
        ui.card(
            ui.card_header("Generated SAS Code"),
            ui.output_text_verbatim("sas_code"),
        ),
    ),
)

def server(input, output, session):
    @reactive.event(input.generate)
    def _():
        pass

    @output
    @render.text
    def sas_code():
        term = input.lookup_term() or ""
        dataset = input.dataset() or "mydata"
        column = input.code_column() or "code"
        # Placeholder SAS code generation logic — replace with your codelookup logic
        # TODO: Add input validation/sanitization when implementing real codelookup logic
        lines = [
            f"/* Generated SAS code for term: {term} */",
            f"data filtered;",
            f"  set {dataset};",
            f"  if {column} = '{term}' then output;",
            f"run;",
        ]
        return "\n".join(lines)

app = App(app_ui, server)
