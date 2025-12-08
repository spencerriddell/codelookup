from shiny import App, ui, render, reactive
from typing import List, Dict, Any

# === Reused constants and structures from codelookup.py (GUI-independent) ===

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
    "YRBS": {
        "full_name": "NYC Youth Risk Behavior Survey",
        "population": "Youth",
        "tag_suffix": "YRBS",
    },
    "CHS": {
        "full_name": "Community Health Survey",
        "population": "Adult",
        "tag_suffix": "CHS",
    },
    "HANES": {
        "full_name": "NYC Health and Nutrition Examination Survey",
        "population": "Adult",
        "tag_suffix": "HANES",
    },
    "CCHS": {
        "full_name": "NYC Child Health Data",
        "population": "Youth",
        "tag_suffix": "CCHS",
    },
}

# === Helper to compute topic/subtopic IDs following original logic ===

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

# === Shiny UI mirroring the original inputs and constraints ===

topic_options = sorted(TOPICS.keys())

app_ui = ui.page_fluid(
    ui.h2("SAS Code Generator (Client-side, Shinylive)"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "dataset", "Survey Dataset", choices=list(SURVEYS.keys()), selected="YRBS"
            ),
            ui.input_text("var_code", "Variable Code"),
            ui.input_text("var_name", "Variable Name"),
            ui.input_text("description", "Description"),
            ui.input_select(
                "var_type",
                "Variable Type",
                choices=["Indicator", "Demographic"],
                selected="Indicator",
            ),
            ui.input_select("topic", "Topic", choices=topic_options, selected=topic_options[0]),
            ui.input_select("sub_topic", "Sub-Topic", choices=[], selected=None),
            ui.input_numeric("levels", "Number of Levels", 2, min=2, max=6),
            ui.output_ui("level_inputs"),
            ui.input_action_button("add_var", "Add Variable to List", class_="btn-primary"),
            ui.hr(),
            ui.input_action_button("generate", "Generate SAS Code", class_="btn-success"),
            ui.hr(),
            ui.markdown(
                "- Indicator requires Topic and Sub-Topic; Demographic disables both.\n"
                "- Levels 2–6; provide names for each level.\n"
                "- Click 'Add Variable to List' to queue multiple variables before Generate."
            ),
        ),
        ui.card(
            ui.card_header("Queued Variables"),
            ui.output_text_verbatim("queue_summary"),
        ),
        ui.card(
            ui.card_header("Generated SAS Code"),
            ui.output_text_verbatim("sas_code"),
        ),
    ),
)

def server(input, output, session):
    # Reactive store of queued variables (list of dicts)
    queued: reactive.Value[List[Dict[str, Any]]] = reactive.Value([])

    # Update topic/subtopic enablement based on var_type
    @reactive.calc
    def current_subtopics():
        vt = input.var_type()
        topic = input.topic()
        if vt == "Demographic" or not topic:
            return []
        return sorted(TOPICS.get(topic, {}).get("subtopics", {}).keys())

    @output
    @render.ui
    def level_inputs():
        # Render dynamic level name inputs
        n = input.levels()
        items = []
        for i in range(1, int(n) + 1):
            items.append(ui.input_text(f"level_{i}", f"Level {i} Name"))
        return ui.div(*items)

    # Keep sub_topic choices in sync
    @reactive.effect
    def _sync_subtopics():
        subs = current_subtopics()
        # Update sub_topic choices dynamically
        session.send_input_message(
            "sub_topic",
            {
                "options": [{"label": s, "value": s} for s in subs],
                "selected": (subs[0] if subs else None),
            },
        )
        # Disable topic/sub_topic when Demographic
        vt = input.var_type()
        session.send_input_message("topic", {"disabled": vt == "Demographic"})
        session.send_input_message("sub_topic", {"disabled": vt == "Demographic"})

    def validate_current() -> str:
        # Return empty string if valid; else an error message
        if not input.dataset():
            return "Please select a Survey Dataset."
        if not (input.var_code() or "").strip():
            return "Please enter Variable Code."
        if not (input.var_name() or "").strip():
            return "Please enter Variable Name."
        if not (input.description() or "").strip():
            return "Please enter Description."
        if input.var_type() not in ["Indicator", "Demographic"]:
            return "Please select Variable Type."
        if input.var_type() == "Indicator":
            if not input.topic() or not input.sub_topic():
                return "Please select Topic and Sub-Topic for Indicators."
        try:
            n = int(input.levels())
        except Exception:
            return "Please select a valid Number of Levels."
        if not (2 <= n <= 6):
            return "Number of Levels must be between 2 and 6."
        for i in range(1, n + 1):
            name = (session.get_input(f"level_{i}") or "").strip()
            if not name:
                return f"Please enter a name for Level {i}."
        return ""

    def build_var_data() -> Dict[str, Any]:
        dataset = input.dataset()
        survey = SURVEYS[dataset]
        n = int(input.levels())
        levels = [(session.get_input(f"level_{i}") or "").strip() for i in range(1, n + 1)]
        var_type = input.var_type()
        topic = input.topic() if var_type == "Indicator" else ""
        sub_topic = input.sub_topic() if var_type == "Indicator" else ""
        ids = compute_ids(var_type, topic, sub_topic)
        return {
            "dataset": dataset,
            "dataset_name": survey["full_name"],
            "population": survey["population"],
            "tag_suffix": survey["tag_suffix"],
            "var_code": (input.var_code() or "").strip(),
            "var_name": (input.var_name() or "").strip(),
            "description": (input.description() or "").strip(),
            "var_type": var_type,
            "topic": topic,
            "sub_topic": sub_topic,
            "topic_id": ids["topic_id"],
            "subtopic_id": ids["subtopic_id"],
            "levels": levels,
        }

    @reactive.event(input.add_var)
    def add_var():
        err = validate_current()
        if err:
            # Surface validation errors inline in queue summary pane
            queued.set(queued.get())
            session.send_notification(err, type="error")
            return
        q = queued.get().copy()
        q.append(build_var_data())
        queued.set(q)
        session.send_notification("Variable added to queue.", type="message")

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
        pass

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
