from shiny import App, ui, render, reactive
from typing import List, Dict, Any

# === Constants/data ported from codelookup.py ===

SAS_TEMPLATE = """
/* {var_value} */
data new_varxx;
YearNum = 2023;
VarValID = {varvalid};
Topic_ID = {topic_id};
SubTopic_ID = {subtopic_id};
ExcludeInclude = 1;
SortOrder = 1;
Topic_SortOrder = 1;
SubTopic_SortOrder = 1;
Topic_DefaultID = 1;
DefaultID = 1;
Indicator_SortOrder = ;
YearDate = "2023-01-01";
Dataset = "{dataset}";
Dataset_Name = "{dataset_name}";
Dataset_Type = "Health Surveys";
VarCode = "{var_code}";
VarValue = "{var_value}";
VarType = "{var_type}";
VarName = "{var_name}";
Description = "{description}";
Topic = "{topic}";
Sub_Topic = "{sub_topic}";
PopulationDatasource = "{population}";
Note1 = "";
Note2 = "";
Note3 = "";
CrossNotes = "";
MapTitlePrefix = "";
MapTitleSuffix = "";
MapInsert = "";
VarComments = "";
Tag = "{var_name}_{tag_suffix}";
DefaultPopulationSource = "{population}";
output;
run;
"""

TOPICS = {
    "Children and Youth": {
        "id": 5,
        "subtopics": {
            "Child Development and Disabilities": 26,
            "Day Care and School": 34,
            "Drug and Alcohol Use": 10,
            "Health Care Use": 17,
            "Health Insurance": 15,
            "Household and Neighborhood": 16,
            "Health Status": 18,
            "Mental Health": 3,
            "Nutrition": 23,
            "Physical Activity": 35,
            "Physical Health Conditions": 12,
            "Population Characteristics": 11,
            "Safety": 4,
            "Sleep": 33,
            "Sexual Behavior": 30,
            "Smoking": 7,
            "Violence": 1,
        },
    },
    "Healthy Living": {
        "id": 4,
        "subtopics": {
            "Vaccinations": 29,
            "Drug and Alcohol Use": 10,
            "Health Status": 18,
            "Nutrition": 23,
            "Physical Activity": 35,
            "Safety": 4,
            "Screening": 19,
            "Sexual Behavior": 30,
        },
    },
    "Sleep": {"id": 33, "subtopics": {}},
    "Smoking": {"id": 7, "subtopics": {}},
    "Vaccinations": {"id": 29, "subtopics": {}},
    "Violence": {"id": 1, "subtopics": {}},
    "Community Characteristics": {
        "id": 6,
        "subtopics": {
            "Day Care and School": 34,
            "Economic Factors": 31,
            "Population Characteristics": 11,
            "Social Factors": 13,
        },
    },
    "Living and Environmental Conditions": {
        "id": 7,
        "subtopics": {
            "Built Environment": 28,
            "Housing": 14,
        },
    },
    "Safety": {"id": 4, "subtopics": {}},
    "Social Factors": {"id": 13, "subtopics": {}},
    "Mental Health": {
        "id": 3,
        "subtopics": {
            "Drug and Alcohol Use": 10,
            "Mental Health Conditions": 20,
            "Mental Health Counseling and Treatment": 27,
        },
    },
    "Diseases and Conditions": {
        "id": 1,
        "subtopics": {
            "Child Development and Disabilities": 26,
            "Chronic Diseases": 24,
            "Dental Health": 21,
            "Foodborne or Waterborne Infections": 43,
            "HIV-AIDS": 8,
            "Hearing and Vision Health": 36,
            "Hepatitis Infections": 48,
            "Invasive Bacterial Infections": 45,
            "Mosquitoborne Infections": 37,
            "Other and Rare Diseases": 46,
            "Person-to-Person Infections": 44,
            "Respiratory Infections": 41,
            "Sexually Transmitted Infections": 5,
            "Syndromic Surveillance": 39,
            "Tickborne Infections": 42,
            "Tuberculosis": 53,
            "Vaccine-Preventable Diseases": 47,
            "Zoonotic Infections": 40,
        },
    },
    "Health Care Access and Use": {
        "id": 2,
        "subtopics": {
            "Health Care Use": 17,
            "Health Insurance": 15,
            "Mental Health Counseling and Treatment": 27,
            "Screening": 19,
            "Vaccinations": 29,
        },
    },
    "Birth and Death": {
        "id": 8,
        "subtopics": {
            "Birth": 38,
            "Infant Mortality": 51,
            "Leading Cause of Death": 52,
            "Mortality and Premature Mortality": 49,
        },
    },
}

SURVEYS = {
    "YRBS": {"full_name": "NYC Youth Risk Behavior Survey", "population": "Youth", "tag_suffix": "YRBS"},
    "CHS": {"full_name": "Community Health Survey", "population": "Adult", "tag_suffix": "CHS"},
    "HANES": {"full_name": "NYC Health and Nutrition Examination Survey", "population": "Adult", "tag_suffix": "HANES"},
    "CCHS": {"full_name": "NYC Child Health Data", "population": "Youth", "tag_suffix": "CCHS"},
}

def compute_ids(var_type: str, topic: str, sub_topic: str) -> Dict[str, int]:
    topic_id = TOPICS.get(topic, {}).get("id", 0) if topic else 0
    subtopic_id = 0
    if var_type == "Indicator" and topic in TOPICS:
        subtopic_id = TOPICS.get(topic, {}).get("subtopics", {}).get(sub_topic, 0)
    return {"topic_id": topic_id, "subtopic_id": subtopic_id}

def generate_sas_for_variable(var_data: Dict[str, Any]) -> List[str]:
    parts: List[str] = []
    ids = compute_ids(var_data["var_type"], var_data.get("topic", ""), var_data.get("sub_topic", ""))
    for idx, val in enumerate(var_data["levels"], start=1):
        parts.append(
            SAS_TEMPLATE.format(
                varvalid=idx,
                topic_id=ids["topic_id"],
                subtopic_id=ids["subtopic_id"],
                dataset=var_data["dataset"],
                dataset_name=var_data["dataset_name"],
                var_code=var_data["var_code"],
                var_value=val,
                var_type=var_data["var_type"],
                var_name=var_data["var_name"],
                description=var_data["description"],
                topic=var_data.get("topic", ""),
                sub_topic=var_data.get("sub_topic", ""),
                population=var_data["population"],
                tag_suffix=var_data["tag_suffix"],
            )
        )
        parts.append("")  # blank line between entries
    return parts

# === UI (two columns for queue and output) ===

topic_options = sorted(TOPICS.keys())

app_ui = ui.page_fluid(
    ui.h2("SAS Code Generator (Client-side, Shinylive)"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("dataset", "Survey Dataset", choices=list(SURVEYS.keys()), selected="YRBS"),
            ui.input_text("var_code", "Variable Code"),
            ui.input_text("var_name", "Variable Name"),
            ui.input_text("description", "Description"),
            ui.input_select("var_type", "Variable Type", choices=["Indicator", "Demographic"], selected="Indicator"),
            ui.input_select("topic", "Topic", choices=topic_options, selected=topic_options[0]),
            # Initialize sub_topic with no choices and no selection
            ui.input_select("sub_topic", "Sub-Topic", choices=[], selected=None),
            ui.input_numeric("levels", "Number of Levels", 2, min=2, max=6),
            ui.output_ui("level_inputs"),
            ui.input_action_button("add_var", "Add Variable to Queue", class_="btn-primary"),
            ui.input_action_button("clear_queue", "Clear Queue", class_="btn-secondary"),
            ui.hr(),
            ui.input_action_button("generate", "Generate SAS Code", class_="btn-success"),
            ui.hr(),
            ui.output_text_verbatim("validation_errors"),
        ),
        ui.row(
            ui.column(
                6,
                ui.card(
                    ui.card_header("Queued Variables"),
                    ui.output_text_verbatim("queue_summary"),
                ),
            ),
            ui.column(
                6,
                ui.card(
                    ui.card_header("Generated SAS Code"),
                    ui.output_text_verbatim("sas_code"),
                ),
            ),
        ),
    ),
)

def server(input, output, session):
    queued: reactive.Value[List[Dict[str, Any]]] = reactive.Value([])
    last_error: reactive.Value[str] = reactive.Value("")
    awaiting_confirmation: reactive.Value[bool] = reactive.Value(False)
    pending_validation_errors: reactive.Value[List[str]] = reactive.Value([])

    # Dynamic level inputs
    @output
    @render.ui
    def level_inputs():
        n = int(input.levels() or 2)
        return ui.div(*[ui.input_text(f"level_{i}", f"Level {i} Name") for i in range(1, n + 1)])

    # Sub-topic updater effect (reacts to both var_type and topic)
    @reactive.effect
    def _update_subtopics():
        vt = input.var_type()
        topic = input.topic()

        # Disable/enable based on variable type
        is_demographic = vt == "Demographic"
        session.send_input_message("topic", {"disabled": is_demographic})
        session.send_input_message("sub_topic", {"disabled": is_demographic})

        # Build options
        if is_demographic or not topic:
            options = []
            selected = None
        else:
            options = sorted(TOPICS.get(topic, {}).get("subtopics", {}).keys())
            selected = options[0] if options else None

        # Use ui.update_select for updating choices - more reliable than send_input_message
        ui.update_select(
            "sub_topic",
            session=session,
            choices=options,
            selected=selected,
        )

    def validate_current() -> List[str]:
        """Validate current inputs and return list of missing fields."""
        errors = []
        
        if not input.dataset():
            errors.append("Survey Dataset")
        if not (input.var_code() or "").strip():
            errors.append("Variable Code")
        if not (input.var_name() or "").strip():
            errors.append("Variable Name")
        if not (input.description() or "").strip():
            errors.append("Description")
        
        vt = input.var_type()
        if vt not in ["Indicator", "Demographic"]:
            errors.append("Variable Type")
        elif vt == "Indicator":
            # Require a topic with at least one subtopic choice and a selected sub_topic
            topic = input.topic()
            subs = sorted(TOPICS.get(topic, {}).get("subtopics", {}).keys()) if topic else []
            if not topic or not subs:
                errors.append("Topic (with Sub-Topics)")
            if not input.sub_topic():
                errors.append("Sub-Topic")
        
        try:
            n = int(input.levels())
            if not (2 <= n <= 6):
                errors.append("Number of Levels (must be 2-6)")
        except Exception:
            errors.append("Number of Levels")
            n = 0
        
        if n >= 2:
            for i in range(1, n + 1):
                try:
                    name = (input[f"level_{i}"]() or "").strip()
                except (KeyError, AttributeError):
                    name = ""
                if not name:
                    errors.append(f"Level {i} Name")
        
        return errors

    def build_var_data() -> Dict[str, Any]:
        """Build variable data from current inputs, handling missing values gracefully."""
        dataset = input.dataset() or ""
        survey = SURVEYS.get(dataset, {"full_name": "", "population": "", "tag_suffix": ""})
        
        try:
            n = int(input.levels())
        except Exception:
            n = 0
        
        # Get level values, handling cases where inputs might not exist yet
        levels = []
        for i in range(1, n + 1):
            try:
                level_val = (input[f"level_{i}"]() or "").strip()
            except (KeyError, AttributeError):
                level_val = ""
            levels.append(level_val)
        var_type = input.var_type() or "Indicator"
        topic = input.topic() if var_type == "Indicator" else ""
        sub_topic = input.sub_topic() if var_type == "Indicator" else ""
        ids = compute_ids(var_type, topic or "", sub_topic or "")
        
        return {
            "dataset": dataset,
            "dataset_name": survey["full_name"],
            "population": survey["population"],
            "tag_suffix": survey["tag_suffix"],
            "var_code": (input.var_code() or "").strip(),
            "var_name": (input.var_name() or "").strip(),
            "description": (input.description() or "").strip(),
            "var_type": var_type,
            "topic": topic or "",
            "sub_topic": sub_topic or "",
            "topic_id": ids["topic_id"],
            "subtopic_id": ids["subtopic_id"],
            "levels": levels,
        }

    @reactive.effect
    @reactive.event(input.add_var)
    def add_var():
        errors = validate_current()
        
        if errors:
            # Store errors and show confirmation modal
            pending_validation_errors.set(errors)
            awaiting_confirmation.set(True)
            
            error_list = "\n• ".join([""] + errors)
            
            m = ui.modal(
                ui.markdown(f"**Incomplete values for:**{error_list}"),
                ui.p("Add to queue anyway?"),
                title="Validation Warning",
                easy_close=False,
                footer=ui.div(
                    ui.input_action_button("modal_add_anyway", "Yes, Add Anyway", class_="btn-warning"),
                    ui.input_action_button("modal_cancel", "Cancel", class_="btn-secondary"),
                    style="display: flex; gap: 10px; justify-content: flex-end;"
                ),
            )
            ui.modal_show(m)
            return
        
        # No errors, add directly
        q = queued.get().copy()
        q.append(build_var_data())
        queued.set(q)
        last_error.set("")
        ui.notification_show("Variable added to queue.", type="message")
    
    @reactive.effect
    @reactive.event(input.modal_add_anyway)
    def modal_add_anyway():
        # User confirmed to add despite missing values
        ui.modal_remove()
        awaiting_confirmation.set(False)
        
        q = queued.get().copy()
        q.append(build_var_data())
        queued.set(q)
        last_error.set("")
        ui.notification_show("Variable added to queue (with incomplete values).", type="message")
    
    @reactive.effect
    @reactive.event(input.modal_cancel)
    def modal_cancel():
        # User cancelled, just close modal
        ui.modal_remove()
        awaiting_confirmation.set(False)
        errors = pending_validation_errors.get()
        error_msg = "Missing: " + ", ".join(errors)
        last_error.set(error_msg)

    @reactive.event(input.clear_queue)
    def _clear():
        queued.set([])
        ui.notification_show("Queue cleared.", type="message")

    @output
    @render.text
    def validation_errors():
        return last_error.get() or ""

    @output
    @render.text
    def queue_summary():
        q = queued.get()
        if not q:
            return "No variables queued."
        lines = []
        for i, v in enumerate(q, start=1):
            lines.append(
                f"{i}. [{v['dataset']}] {v['var_code']} - {v['var_name']} "
                f"({v['var_type']}) Levels: {len(v['levels'])}"
            )
        return "\n".join(lines)

    @reactive.event(input.generate)
    def _generate():
        if not queued.get():
            msg = "No variables to generate SAS code."
            last_error.set(msg)
            ui.notification_show(msg, type="error")

    @output
    @render.text
    def sas_code():
        q = queued.get()
        if not q:
            return "No variables to generate SAS code."
        parts: List[str] = []
        for v in q:
            parts.extend(generate_sas_for_variable(v))
        return "\n".join(parts)

app = App(app_ui, server)
