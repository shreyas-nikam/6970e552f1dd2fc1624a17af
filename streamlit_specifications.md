
# Streamlit Application Specification: AI Architecture Risk Comparator

## 1. Application Overview

This Streamlit application, "AI Architecture Risk Comparator," is designed to assist Enterprise AI Architects (like Dr. Ava Sharma at OmniCorp Financial), AI Program Leads, and Risk/Security Partners in systematically evaluating the architectural risks of different AI system paradigms: Traditional ML, LLM-based, and Agentic AI. The application enables explicit risk trade-off analysis, mirroring the workflow of enterprise AI architecture review boards.

**High-level Story Flow:**

1.  **Home Page (Welcome & Context):** Dr. Ava Sharma is introduced to the application, its purpose, and the critical role of architectural risk analysis at OmniCorp Financial. She understands that the goal is to make risk visible, comparable, and defensible across different AI system proposals for a specific use case.
2.  **Use Case Selection:** Dr. Sharma selects a predefined use case (e.g., "Fraud Detection") from OmniCorp's knowledge base. This loads baseline assumptions, enterprise constraints, and default architectural configurations, ensuring a standardized starting point.
3.  **Architecture Configuration:** For the chosen use case, Dr. Sharma configures the specific features for ML, LLM, and Agentic architectures. She can toggle architectural characteristics (e.g., "Uses external APIs", "Autonomous execution loop") to model different design choices. This step allows for direct architectural risk trade-off analysis.
4.  **Risk & Control Analysis:** Upon configuration, the application dynamically calculates architectural risk scores (normalized 0-10) across predefined risk categories (Data, Model, Security, etc.) using OmniCorp's deterministic rule-based scoring. It then identifies minimum required controls based on these risk scores and performs a gap analysis against a set of assumed enterprise controls.
5.  **Visualization & Comparison:** The results are presented visually through interactive radar charts, comparing the risk profiles of each architecture side-by-side. A clear control gap checklist is also displayed, highlighting missing controls. These visualizations provide an executive-ready view for the AI Architecture Review Board.
6.  **Export & Reporting:** Finally, Dr. Sharma can generate a comprehensive export package, including configuration snapshots, detailed risk scores, control gap checklists, and an executive summary. This package, bundled into a ZIP file with SHA-256 integrity checks, serves as an auditable artifact for design review, compliance, and program management.

The application does not "choose" the best architecture but surfaces risk deltas and required controls to inform strategic decisions before significant build investment.

## 2. Code Requirements

### Import Statement

```python
from source import *
import streamlit as st
import pandas as pd # Explicitly imported for DataFrame operations/display
import plotly.graph_objects as go # Explicitly imported for radar chart type hinting/display
from datetime import datetime # Explicitly imported for timestamping
import os # Explicitly imported for file path operations
```

### `st.session_state` Management

`st.session_state` will be used to preserve the application's state across user interactions and page navigations.

**Initialization (at the start of `app.py`):**

```python
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'
if 'use_cases_list' not in st.session_state:
    # Load all use case names for the selector
    with open(USE_CASE_FILE, 'r') as f:
        all_use_cases = json.load(f)
    st.session_state['use_cases_list'] = [uc['name'] for uc in all_use_cases]

if 'selected_use_case_name' not in st.session_state:
    st.session_state['selected_use_case_name'] = st.session_state['use_cases_list'][0] # Default to first

if 'selected_use_case_data' not in st.session_state:
    try:
        st.session_state['selected_use_case_data'] = load_use_case_template(USE_CASE_FILE, st.session_state['selected_use_case_name'])
    except Exception as e:
        st.error(f"Error loading default use case: {e}")
        st.session_state['selected_use_case_data'] = {} # Fallback

if 'architectures_config' not in st.session_state:
    # Initialize with defaults from the loaded use case
    if st.session_state['selected_use_case_data']:
        st.session_state['architectures_config'] = st.session_state['selected_use_case_data']['architectural_options_defaults']
    else:
        st.session_state['architectures_config'] = {"ML": {}, "LLM": {}, "Agent": {}} # Empty fallback

if 'free_text_assumptions' not in st.session_state:
    st.session_state['free_text_assumptions'] = "This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date. The risk threshold for mandatory controls (5/10) reflects a moderate risk appetite for new AI initiatives." # Pre-populate

if 'raw_risk_scores_df' not in st.session_state:
    st.session_state['raw_risk_scores_df'] = pd.DataFrame()

if 'normalized_risk_scores_df' not in st.session_state:
    st.session_state['normalized_risk_scores_df'] = pd.DataFrame()

if 'required_controls_by_architecture' not in st.session_state:
    st.session_state['required_controls_by_architecture'] = {}

if 'assumed_controls_omnicorp' not in st.session_state:
    # Default assumed controls, can be made configurable if needed later
    st.session_state['assumed_controls_omnicorp'] = {
        "ML": ["Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Vulnerability scanning", "Secure coding practices", "Incident response plan"],
        "LLM": ["Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Vulnerability scanning", "Secure coding practices", "Incident response plan", "Vendor SLA review"],
        "Agent": ["Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Vulnerability scanning", "Secure coding practices", "Incident response plan", "Vendor SLA review", "Comprehensive audit logs"]
    }

if 'control_gaps_by_architecture' not in st.session_state:
    st.session_state['control_gaps_by_architecture'] = {}

if 'run_id' not in st.session_state:
    st.session_state['run_id'] = None

if 'export_zip_filepath' not in st.session_state:
    st.session_state['export_zip_filepath'] = None

# Perform initial calculation if config is available
if st.session_state['architectures_config'] and not st.session_state['normalized_risk_scores_df'].empty:
    # Ensure all core constants are available for initial calculation
    # These are global in source.py but ensure they are recognized in app.py's context
    if 'RISK_TAXONOMY' in globals() and 'RISK_RULES' in globals() and 'CONTROL_BASELINE_LIBRARY' in globals() and 'RISK_THRESHOLD' in globals():
        st.session_state['normalized_risk_scores_df'], st.session_state['raw_risk_scores_df'] = calculate_risk_scores(
            st.session_state['architectures_config'], globals()['RISK_TAXONOMY'], globals()['RISK_RULES']
        )
        st.session_state['required_controls_by_architecture'] = identify_required_controls(
            st.session_state['normalized_risk_scores_df'], globals()['CONTROL_BASELINE_LIBRARY'], globals()['RISK_THRESHOLD']
        )
        st.session_state['control_gaps_by_architecture'] = perform_control_gap_analysis(
            st.session_state['required_controls_by_architecture'], st.session_state['assumed_controls_omnicorp']
        )
```

**Updates and Reads:**

*   `current_page`: Updated via `st.sidebar.radio` callback. Read for conditional rendering of main content.
*   `selected_use_case_name`: Updated via `st.sidebar.selectbox`.
*   `selected_use_case_data`: Updated when the "Load Use Case" button is clicked. Read to display use case details and to initialize `architectures_config`.
    *   **Callback on "Load Use Case"**:
        ```python
        def load_new_use_case():
            st.session_state['selected_use_case_data'] = load_use_case_template(USE_CASE_FILE, st.session_state['selected_use_case_name'])
            st.session_state['architectures_config'] = st.session_state['selected_use_case_data']['architectural_options_defaults']
            # Re-run calculations for new defaults
            recalculate_all_risks_and_controls()

        def recalculate_all_risks_and_controls():
            # Assumes RISK_TAXONOMY, RISK_RULES, CONTROL_BASELINE_LIBRARY, RISK_THRESHOLD are global from source.py
            if st.session_state['architectures_config'] and globals()['RISK_TAXONOMY'] and globals()['RISK_RULES']:
                st.session_state['normalized_risk_scores_df'], st.session_state['raw_risk_scores_df'] = calculate_risk_scores(
                    st.session_state['architectures_config'], globals()['RISK_TAXONOMY'], globals()['RISK_RULES']
                )
                st.session_state['required_controls_by_architecture'] = identify_required_controls(
                    st.session_state['normalized_risk_scores_df'], globals()['CONTROL_BASELINE_LIBRARY'], globals()['RISK_THRESHOLD']
                )
                st.session_state['control_gaps_by_architecture'] = perform_control_gap_analysis(
                    st.session_state['required_controls_by_architecture'], st.session_state['assumed_controls_omnicorp']
                )
            else:
                st.warning("Cannot calculate risks: Architectural configurations or global risk definitions are missing.")
        ```
*   `architectures_config`: Updated by `st.checkbox` and `st.selectbox` widgets on the "Configuration" page. Read for risk calculations and display.
    *   **Callback on feature toggle**:
        ```python
        def update_config_and_recalculate(arch_type, feature, value):
            st.session_state['architectures_config'][arch_type][feature] = value
            recalculate_all_risks_and_controls()
        ```
*   `free_text_assumptions`: Updated by `st.text_area`. Read for display and export.
*   `raw_risk_scores_df`, `normalized_risk_scores_df`, `required_controls_by_architecture`, `assumed_controls_omnicorp`, `control_gaps_by_architecture`: Updated by `recalculate_all_risks_and_controls` function (called after use case load or config change). Read for display on "Comparison" and "Export" pages.
*   `run_id`, `export_zip_filepath`: Updated by `export_artifacts` call. `export_zip_filepath` is read to enable the download button.

### Function Invocation Points

*   `load_use_case_template(USE_CASE_FILE, use_case_name)`: Called when `selected_use_case_name` changes and "Load Use Case" button is clicked. Updates `st.session_state['selected_use_case_data']` and `st.session_state['architectures_config']`.
*   `calculate_risk_scores(architectures_config, RISK_TAXONOMY, RISK_RULES)`: Called within `recalculate_all_risks_and_controls`. Updates `st.session_state['raw_risk_scores_df']` and `st.session_state['normalized_risk_scores_df']`.
*   `identify_required_controls(normalized_risk_scores_df, CONTROL_BASELINE_LIBRARY, RISK_THRESHOLD)`: Called within `recalculate_all_risks_and_controls`. Updates `st.session_state['required_controls_by_architecture']`.
*   `perform_control_gap_analysis(required_controls_by_arch, assumed_controls_by_arch)`: Called within `recalculate_all_risks_and_controls`. Updates `st.session_state['control_gaps_by_architecture']`.
*   `plot_risk_radar_chart(df_normalized_scores, risk_taxonomy)`: Called on the "Comparison" page. **Modification**: This function in `source.py` currently calls `fig.show()`. For Streamlit, it must be modified to `return fig` (a Plotly Figure object) which `st.plotly_chart()` can then render.
*   `export_artifacts(run_id, use_case_name, architectures_config, normalized_risk_scores_df, control_gaps_by_architecture, assumed_controls_omnicorp, free_text_assumptions)`: Called when the "Generate Export & Download" button is clicked. Updates `st.session_state['run_id']` and `st.session_state['export_zip_filepath']`. **Modification**: This function in `source.py` currently prints output and bundles the zip. It should return the `zip_filename` to `app.py` for the download button.
*   `generate_sha256(filepath)`: This is an internal helper function within `export_artifacts` and `source.py`. It will be implicitly called.

### Markdown Definitions

#### Sidebar Navigation

```python
st.sidebar.title("Navigation")
page_options = ["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"]
st.session_state['current_page'] = st.sidebar.radio("Go to", page_options, index=page_options.index(st.session_state['current_page']))

st.sidebar.header("Select Use Case")
selected_uc_name = st.sidebar.selectbox(
    "Choose a Use Case Template:",
    st.session_state['use_cases_list'],
    index=st.session_state['use_cases_list'].index(st.session_state['selected_use_case_name']),
    key='sidebar_use_case_selector'
)
if selected_uc_name != st.session_state['selected_use_case_name']:
    st.session_state['selected_use_case_name'] = selected_uc_name
    st.sidebar.button("Load Use Case", on_click=load_new_use_case)
```

#### Home Page (`st.session_state['current_page'] == 'Home'`)

```python
st.markdown(f"# OmniCorp Financial AI Architecture Risk Comparator")
st.markdown(f"## Introduction: Architecting Secure and Compliant AI at OmniCorp Financial")
st.markdown(f"""
Dr. Ava Sharma, a seasoned Enterprise AI Architect at OmniCorp Financial, faces a critical task. OmniCorp is looking to significantly upgrade its real-time fraud detection capabilities, and various teams are proposing different AI architectural approaches: traditional Machine Learning (ML), Large Language Model (LLM)-based, and advanced Agentic systems. Each approach offers distinct advantages but also introduces unique risk surfaces and control requirements.

As the primary architect, Dr. Sharma's role is to rigorously evaluate these architectural options, quantifying their inherent risks and identifying necessary control baselines. Her findings will be presented to OmniCorp's AI Architecture Review Board, which includes AI Program Leads (concerned with standardization and funding) and Risk/Security Partners (focused on exposure and compliance). The goal is not to declare a "winner" but to make risk visible, comparable, and defensible, enabling informed strategic decisions before significant investment in building.

This application simulates Dr. Sharma's workflow, demonstrating how she decomposes complex AI systems, applies a standardized risk taxonomy, quantifies architectural risk using deterministic rules, and identifies control gaps. Ultimately, it allows her to produce an executive-ready comparison artifact that ensures OmniCorp develops AI systems that are both innovative and secure.

---
**Learning Objectives:**
By completing this analysis, users will be able to:
1. Decompose AI systems into architectural features that materially affect risk.
2. Compare how ML, LLM, and agentic designs change risk surfaces.
3. Quantify architectural risk using deterministic rules.
4. Identify non-negotiable control expectations per architecture.
5. Produce an executive-ready comparison artifact suitable for design review.
""")
```

#### Use Case & Configuration Page (`st.session_state['current_page'] == '1. Use Case & Configuration'`)

```python
st.markdown(f"# 1. Use Case & Architecture Configuration")

st.markdown(f"## Setting the Stage: Loading Use Case & Defining Foundational Components")
st.markdown(f"""
Dr. Ava Sharma begins by loading the "{st.session_state['selected_use_case_name']}" use case template from OmniCorp's internal knowledge base. This template provides a standardized starting point, detailing the workflow, baseline assumptions, and enterprise constraints specific to the use case. This step ensures that all architectural comparisons are grounded in the same operational context, a crucial practice for ensuring consistency across the various AI initiatives managed by the AI Program Lead.

This section also establishes the core definitions for OmniCorp's AI risk taxonomy and the set of configurable architectural features that materially affect risk. These are fixed, enterprise-grade definitions that Dr. Sharma, along with Risk/Security Partners, helped establish to ensure a common language for risk assessment.
""")

st.subheader(f"Selected Use Case: {st.session_state['selected_use_case_name']}")
if st.session_state['selected_use_case_data']:
    st.markdown(f"**Description:** {st.session_state['selected_use_case_data']['description']}")
    st.markdown(f"**Baseline Assumptions:**")
    for assumption in st.session_state['selected_use_case_data']['baseline_assumptions']:
        st.markdown(f"- {assumption}")
    st.markdown(f"**Enterprise Constraints:**")
    for constraint in st.session_state['selected_use_case_data']['enterprise_constraints']:
        st.markdown(f"- {constraint}")
else:
    st.warning("No use case data loaded. Please select and load a use case.")

st.markdown(f"---")

st.markdown(f"## Configuring Architectures for {st.session_state['selected_use_case_name']}")
st.markdown(f"""
With the use case loaded, Dr. Sharma now configures the specific features for each proposed AI architecture (ML, LLM, Agentic) for the fraud detection system. These configurations represent the core design choices that materially affect the system's risk profile. For example, an Agentic system for fraud detection might inherently require an "autonomous execution loop" and "tool/function calling" to interact with mitigation systems, while a traditional ML system might not. Adjusting these toggles allows Dr. Sharma to model hypothetical designs and assess their risk implications, enabling explicit architectural risk trade-off analysis. This directly supports the AI Program Lead's need for standardized architectural proposals and allows Dr. Sharma to justify her decisions to the Risk/Security Partner.
""")

# Architectural Feature Toggles (3-column layout)
if st.session_state['architectures_config']:
    cols = st.columns(3)
    architecture_types = ["ML", "LLM", "Agent"]
    for i, arch_type in enumerate(architecture_types):
        with cols[i]:
            st.subheader(f"{arch_type} Architecture")
            current_config = st.session_state['architectures_config'].get(arch_type, {})
            for feature in ARCHITECTURAL_FEATURES: # ARCHITECTURAL_FEATURES is global from source.py
                if feature == "human_approval_required":
                    options = ["None", "Partial", "Mandatory"]
                    current_value = current_config.get(feature, options[0])
                    new_value = st.selectbox(
                        f"{feature.replace('_', ' ').title()}:",
                        options,
                        index=options.index(current_value) if current_value in options else 0,
                        key=f"{arch_type}_{feature}",
                        on_change=update_config_and_recalculate, args=(arch_type, feature, )
                    )
                    if new_value != current_value:
                        update_config_and_recalculate(arch_type, feature, new_value)

                elif feature == "fine_tuned_model":
                    current_value = current_config.get(feature, False) # Default to False
                    new_value = st.checkbox(
                        f"Fine-tuned vs Base Model",
                        value=current_value,
                        key=f"{arch_type}_{feature}",
                        on_change=update_config_and_recalculate, args=(arch_type, feature, )
                    )
                    if new_value != current_value:
                        update_config_and_recalculate(arch_type, feature, new_value)
                elif feature == "real_time_execution":
                    current_value = current_config.get(feature, False) # Default to False
                    new_value = st.checkbox(
                        f"Real-time vs Batch Execution",
                        value=current_value,
                        key=f"{arch_type}_{feature}",
                        on_change=update_config_and_recalculate, args=(arch_type, feature, )
                    )
                    if new_value != current_value:
                        update_config_and_recalculate(arch_type, feature, new_value)
                else: # Boolean toggles
                    current_value = current_config.get(feature, False)
                    new_value = st.checkbox(
                        f"{feature.replace('_', ' ').title()}",
                        value=current_value,
                        key=f"{arch_type}_{feature}",
                        on_change=update_config_and_recalculate, args=(arch_type, feature, )
                    )
                    if new_value != current_value:
                        update_config_and_recalculate(arch_type, feature, new_value)
else:
    st.warning("Architectural configurations are not loaded. Please load a use case first.")

st.markdown("---")
st.markdown("## Additional Assumptions")
st.markdown("""
Provide any optional free-text assumptions relevant to this analysis. These notes will be captured and included in the export.
""")
st.session_state['free_text_assumptions'] = st.text_area(
    "Free-Text Assumptions for this Session:",
    value=st.session_state['free_text_assumptions'],
    height=150,
    key="free_text_assumptions_input"
)

# Recalculate button for completeness, though changes trigger recalculation
if st.button("Recalculate Risk & Controls (Manual Trigger)"):
    recalculate_all_risks_and_controls()
    st.success("Risk scores and controls recalculated!")
```

#### Risk & Control Comparison Page (`st.session_state['current_page'] == '2. Risk & Control Comparison'`)

```python
st.markdown(f"# 2. Architectural Risk & Control Comparison")

st.markdown(f"## Quantifying Architectural Risk with Deterministic Rules")
st.markdown(f"""
To objectively compare the architectural designs, Dr. Sharma applies OmniCorp's standardized, rule-based risk scoring methodology. This system uses deterministic rules, where each enabled architectural feature contributes a predefined score to one or more risk categories (e.g., `uses_external_apis` increases `Dependency / Vendor Risk`). This quantification step is crucial for the AI Program Lead, who needs standardized metrics to compare proposals across teams, and for the Risk/Security Partner, who relies on clear, auditable risk assessments. The normalization of scores (0-10) ensures comparability across different risk categories, even if the underlying rules vary in their raw impact.
""")

st.markdown(r"The risk score for a given category for an architecture, $R_{arch, cat}$, is calculated as the sum of all risk contributions from its enabled features, $C_{feature, cat}$, and then normalized:")
st.markdown(r"$$ R_{arch, cat} = \text{normalize}\left(\sum_{feature \in Features_{arch}} C_{feature, cat}\right) $$")
st.markdown(r"where $Features_{arch}$ is the set of enabled features for a specific architecture, and $C_{feature, cat}$ is the risk contribution of a feature to a specific risk category.")

if not st.session_state['normalized_risk_scores_df'].empty:
    st.subheader("Normalized Risk Scores (0-10 per category):")
    st.dataframe(st.session_state['normalized_risk_scores_df'])
else:
    st.warning("Risk scores not available. Please configure architectures and load a use case.")

st.markdown(f"---")

st.markdown(f"## Identifying Control Baselines and Gap Analysis")
st.markdown(f"""
After quantifying the risks, Dr. Sharma's next step is to determine what controls are *required* for each architecture based on its risk profile and OmniCorp's control baseline library. Furthermore, she must perform a "gap analysis" to highlight any missing controls, assuming a certain set of controls are already in place (even if none are initially assumed, the identification of *required* controls is paramount). This step directly addresses the concerns of the Risk/Security Partner, who needs explicit control gaps highlighted to ensure compliance and security. It also informs the AI Program Lead about the additional effort and resources required to implement each architectural option.
""")
st.markdown(r"The control baseline mapping is: Risk category $\rightarrow$ Minimum required controls. A control gap is identified if a required control is not present in the set of `assumed_controls`.")

if st.session_state['required_controls_by_architecture'] and st.session_state['control_gaps_by_architecture']:
    st.subheader(f"Comprehensive Control Gap Checklist (Risk Threshold >= {RISK_THRESHOLD})")
    for arch_type in st.session_state['required_controls_by_architecture'].keys():
        st.markdown(f"### {arch_type} Architecture Controls")
        if not st.session_state['required_controls_by_architecture'][arch_type]:
            st.markdown("- No specific controls required based on current risk profile and threshold.")
            continue
        st.markdown("#### Required Controls:")
        for control in st.session_state['required_controls_by_architecture'][arch_type]:
            status = "✅ Present (or assumed)"
            if control in st.session_state['control_gaps_by_architecture'][arch_type]:
                status = "❌ MISSING (GAP)"
            st.markdown(f"- {control} {status}")
else:
    st.warning("Control requirements or gaps not available. Please ensure risk calculations are complete.")

st.markdown(f"---")

st.markdown(f"## Visualizing Risk Profiles")
st.markdown(f"""
To effectively communicate her findings to OmniCorp's AI Architecture Review Board, Dr. Sharma needs compelling visualizations. Raw data tables, while precise, can be hard to digest for an executive audience. Therefore, she generates radar charts to visually represent each architecture's risk profile across all categories. These visualizations make the risk deltas and required controls immediately apparent, facilitating discussions with the AI Program Lead regarding resource allocation and with the Risk/Security Partner on critical compliance concerns. This step is crucial for transforming complex analysis into an executive-ready comparison artifact.
""")

if not st.session_state['normalized_risk_scores_df'].empty:
    # Plotly radar chart (assuming plot_risk_radar_chart from source.py is modified to return a figure)
    # The actual plot_risk_radar_chart function in source.py needs to be adjusted to return the plotly figure object.
    # For instance, replace fig.show() with return fig.
    try:
        radar_fig = plot_risk_radar_chart(st.session_state['normalized_risk_scores_df'], globals()['RISK_TAXONOMY'])
        st.plotly_chart(radar_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating radar chart: {e}")
        st.warning("Ensure the `plot_risk_radar_chart` function in `source.py` returns a Plotly figure object.")
else:
    st.warning("Cannot generate radar chart: Normalized risk scores are not available.")
```

#### Export Artifacts Page (`st.session_state['current_page'] == '3. Export Artifacts'`)

```python
st.markdown(f"# 3. Generating an Executive-Ready Comparison Artifact")
st.markdown(f"""
The final, and critical, step for Dr. Sharma is to compile all her analysis into a comprehensive, executive-ready comparison artifact. This package includes configuration snapshots, risk scores, control gap checklists, and an executive summary, all bundled into a single ZIP archive. This artifact serves multiple purposes: it's the primary deliverable for the AI Architecture Review Board, provides a standardized record for the AI Program Lead, and offers auditable evidence for the Risk/Security Partner. The inclusion of an `evidence_manifest.json` with SHA-256 hashes ensures the integrity and non-repudiation of the analysis, a crucial aspect in a regulated environment like OmniCorp Financial.
""")

st.markdown(f"## Export Summary for {st.session_state['selected_use_case_name']}")
st.markdown("""
The following artifacts will be generated and bundled into a ZIP file:
- `architecture_config.json`: Snapshot of configured architectural features.
- `risk_scores_by_architecture.json`: Detailed raw and normalized risk scores.
- `control_gaps_checklist.json`: List of identified control gaps for each architecture.
- `session02_executive_summary.md`: A markdown-formatted executive summary of the analysis.
- `config_snapshot.json`: All global definitions (risk taxonomy, rules, controls) used for this analysis.
- `evidence_manifest.json`: SHA-256 hashes of all generated artifacts to ensure integrity.
""")

if st.button("Generate Export & Download Package"):
    if not st.session_state['normalized_risk_scores_df'].empty and st.session_state['architectures_config']:
        current_run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state['run_id'] = current_run_id
        
        try:
            # The export_artifacts function in source.py needs to return the zip_filename
            # The original source.py's export_artifacts uses global variables directly, which is fine.
            # We need to make sure the function returns the zip file path to enable download.
            zip_file_path = export_artifacts(
                st.session_state['run_id'],
                st.session_state['selected_use_case_name'],
                st.session_state['architectures_config'],
                st.session_state['normalized_risk_scores_df'],
                st.session_state['control_gaps_by_architecture'],
                st.session_state['assumed_controls_omnicorp'], # This global is used internally by export_artifacts
                st.session_state['free_text_assumptions']
            )
            st.session_state['export_zip_filepath'] = zip_file_path
            st.success(f"Export package generated successfully in `{REPORTS_DIR_BASE}/{current_run_id}/`")
        except Exception as e:
            st.error(f"Error generating export package: {e}")
            st.session_state['export_zip_filepath'] = None
    else:
        st.warning("Please ensure a use case is loaded and risk calculations are complete before exporting.")

if st.session_state['export_zip_filepath'] and os.path.exists(st.session_state['export_zip_filepath']):
    with open(st.session_state['export_zip_filepath'], "rb") as fp:
        st.download_button(
            label="Download Export Package (.zip)",
            data=fp.read(),
            file_name=os.path.basename(st.session_state['export_zip_filepath']),
            mime="application/zip",
        )
```
