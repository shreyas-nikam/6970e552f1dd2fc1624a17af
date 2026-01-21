import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import json
from source import *

# Set page configuration
st.set_page_config(page_title="QuLab: Lab 2: AI Architecture Comparator", layout="wide")

# Sidebar header
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()

# Main title
st.title("QuLab: Lab 2: AI Architecture Comparator")
st.divider()

# --- Helper Functions ---

def recalculate_all_risks_and_controls():
    """Recalculates risk scores and controls based on current configuration."""
    # Assumes RISK_TAXONOMY, RISK_RULES, CONTROL_BASELINE_LIBRARY, RISK_THRESHOLD are global from source.py
    if st.session_state['architectures_config'] and 'RISK_TAXONOMY' in globals() and 'RISK_RULES' in globals():
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

def load_new_use_case():
    """Callback to load a new use case."""
    try:
        st.session_state['selected_use_case_data'] = load_use_case_template(USE_CASE_FILE, st.session_state['selected_use_case_name'])
        st.session_state['architectures_config'] = st.session_state['selected_use_case_data']['architectural_options_defaults']
        # Re-run calculations for new defaults
        recalculate_all_risks_and_controls()
    except Exception as e:
        st.error(f"Error loading use case: {e}")

def update_config_and_recalculate(arch_type, feature, value):
    """Callback to update configuration and recalculate risks."""
    if arch_type in st.session_state['architectures_config']:
        st.session_state['architectures_config'][arch_type][feature] = value
        recalculate_all_risks_and_controls()

# --- Session State Initialization ---

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

if 'use_cases_list' not in st.session_state:
    # Load all use case names for the selector
    try:
        with open(USE_CASE_FILE, 'r') as f:
            all_use_cases = json.load(f)
        st.session_state['use_cases_list'] = [uc['name'] for uc in all_use_cases]
    except Exception as e:
        st.error(f"Error loading use cases file: {e}")
        st.session_state['use_cases_list'] = ["Default Use Case"]

if 'selected_use_case_name' not in st.session_state:
    if st.session_state['use_cases_list']:
        st.session_state['selected_use_case_name'] = st.session_state['use_cases_list'][0]
    else:
        st.session_state['selected_use_case_name'] = ""

if 'selected_use_case_data' not in st.session_state:
    try:
        st.session_state['selected_use_case_data'] = load_use_case_template(USE_CASE_FILE, st.session_state['selected_use_case_name'])
    except Exception as e:
        # Only show error if we really can't load anything reasonable
        if st.session_state['selected_use_case_name']:
             st.error(f"Error loading default use case: {e}")
        st.session_state['selected_use_case_data'] = {}

if 'architectures_config' not in st.session_state:
    # Initialize with defaults from the loaded use case
    if st.session_state['selected_use_case_data']:
        st.session_state['architectures_config'] = st.session_state['selected_use_case_data'].get('architectural_options_defaults', {"ML": {}, "LLM": {}, "Agent": {}})
    else:
        st.session_state['architectures_config'] = {"ML": {}, "LLM": {}, "Agent": {}}

if 'free_text_assumptions' not in st.session_state:
    st.session_state['free_text_assumptions'] = "This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date. The risk threshold for mandatory controls (5/10) reflects a moderate risk appetite for new AI initiatives."

if 'raw_risk_scores_df' not in st.session_state:
    st.session_state['raw_risk_scores_df'] = pd.DataFrame()

if 'normalized_risk_scores_df' not in st.session_state:
    st.session_state['normalized_risk_scores_df'] = pd.DataFrame()

if 'required_controls_by_architecture' not in st.session_state:
    st.session_state['required_controls_by_architecture'] = {}

if 'assumed_controls_omnicorp' not in st.session_state:
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

# Perform initial calculation if config is available and dataframes are empty
if st.session_state['architectures_config'] and st.session_state['normalized_risk_scores_df'].empty:
    recalculate_all_risks_and_controls()

# --- Sidebar Navigation ---

st.sidebar.title("Navigation")
page_options = ["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"]

# Ensure current_page is valid
if st.session_state['current_page'] not in page_options:
    st.session_state['current_page'] = page_options[0]

st.session_state['current_page'] = st.sidebar.radio(
    "Go to", 
    page_options, 
    index=page_options.index(st.session_state['current_page'])
)

st.sidebar.header("Select Use Case")
if st.session_state['use_cases_list']:
    try:
        current_index = st.session_state['use_cases_list'].index(st.session_state['selected_use_case_name'])
    except ValueError:
        current_index = 0
        
    selected_uc_name = st.sidebar.selectbox(
        "Choose a Use Case Template:",
        st.session_state['use_cases_list'],
        index=current_index,
        key='sidebar_use_case_selector'
    )

    if selected_uc_name != st.session_state['selected_use_case_name']:
        st.session_state['selected_use_case_name'] = selected_uc_name
        st.sidebar.button("Load Use Case", on_click=load_new_use_case)
else:
    st.sidebar.warning("No use cases available.")

# --- Page Content ---

if st.session_state['current_page'] == 'Home':
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

elif st.session_state['current_page'] == '1. Use Case & Configuration':
    st.markdown(f"# 1. Use Case & Architecture Configuration")

    st.markdown(f"## Setting the Stage: Loading Use Case & Defining Foundational Components")
    st.markdown(f"""
Dr. Ava Sharma begins by loading the "{st.session_state['selected_use_case_name']}" use case template from OmniCorp's internal knowledge base. This template provides a standardized starting point, detailing the workflow, baseline assumptions, and enterprise constraints specific to the use case. This step ensures that all architectural comparisons are grounded in the same operational context, a crucial practice for ensuring consistency across the various AI initiatives managed by the AI Program Lead.

This section also establishes the core definitions for OmniCorp's AI risk taxonomy and the set of configurable architectural features that materially affect risk. These are fixed, enterprise-grade definitions that Dr. Sharma, along with Risk/Security Partners, helped establish to ensure a common language for risk assessment.
""")

    st.subheader(f"Selected Use Case: {st.session_state['selected_use_case_name']}")
    if st.session_state['selected_use_case_data']:
        st.markdown(f"**Description:** {st.session_state['selected_use_case_data'].get('description', 'N/A')}")
        st.markdown(f"**Baseline Assumptions:**")
        for assumption in st.session_state['selected_use_case_data'].get('baseline_assumptions', []):
            st.markdown(f"- {assumption}")
        st.markdown(f"**Enterprise Constraints:**")
        for constraint in st.session_state['selected_use_case_data'].get('enterprise_constraints', []):
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
                
                # Ensure ARCHITECTURAL_FEATURES is available
                features_to_display = globals().get('ARCHITECTURAL_FEATURES', [])
                
                for feature in features_to_display:
                    if feature == "human_approval_required":
                        options = ["None", "Partial", "Mandatory"]
                        current_value = current_config.get(feature, options[0])
                        # Ensure current_value is valid
                        if current_value not in options:
                            current_value = options[0]
                            
                        new_value = st.selectbox(
                            f"{feature.replace('_', ' ').title()}:",
                            options,
                            index=options.index(current_value),
                            key=f"{arch_type}_{feature}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(arch_type, feature, new_value)

                    elif feature == "fine_tuned_model":
                        current_value = current_config.get(feature, False)
                        new_value = st.checkbox(
                            f"Fine-tuned vs Base Model",
                            value=current_value,
                            key=f"{arch_type}_{feature}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(arch_type, feature, new_value)
                    elif feature == "real_time_execution":
                        current_value = current_config.get(feature, False)
                        new_value = st.checkbox(
                            f"Real-time vs Batch Execution",
                            value=current_value,
                            key=f"{arch_type}_{feature}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(arch_type, feature, new_value)
                    else: 
                        current_value = current_config.get(feature, False)
                        new_value = st.checkbox(
                            f"{feature.replace('_', ' ').title()}",
                            value=current_value,
                            key=f"{arch_type}_{feature}",
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
    
    # Store text area input in session state
    st.session_state['free_text_assumptions'] = st.text_area(
        "Free-Text Assumptions for this Session:",
        value=st.session_state['free_text_assumptions'],
        height=150,
        key="free_text_assumptions_input"
    )

    if st.button("Recalculate Risk & Controls (Manual Trigger)"):
        recalculate_all_risks_and_controls()
        st.success("Risk scores and controls recalculated!")

elif st.session_state['current_page'] == '2. Risk & Control Comparison':
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
        current_threshold = globals().get('RISK_THRESHOLD', 5)
        st.subheader(f"Comprehensive Control Gap Checklist (Risk Threshold >= {current_threshold})")
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
        try:
            if 'RISK_TAXONOMY' in globals():
                radar_fig = plot_risk_radar_chart(st.session_state['normalized_risk_scores_df'], globals()['RISK_TAXONOMY'])
                st.plotly_chart(radar_fig, use_container_width=True)
            else:
                 st.warning("Global RISK_TAXONOMY missing, cannot plot chart.")
        except Exception as e:
            st.error(f"Error generating radar chart: {e}")
            st.warning("Ensure the `plot_risk_radar_chart` function in `source.py` returns a Plotly figure object.")
    else:
        st.warning("Cannot generate radar chart: Normalized risk scores are not available.")

elif st.session_state['current_page'] == '3. Export Artifacts':
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
                # Assumes export_artifacts returns the zip file path
                # Helper function ensures we are passing necessary data
                zip_file_path = export_artifacts(
                    st.session_state['run_id'],
                    st.session_state['selected_use_case_name'],
                    st.session_state['architectures_config'],
                    st.session_state['normalized_risk_scores_df'],
                    st.session_state['control_gaps_by_architecture'],
                    st.session_state['assumed_controls_omnicorp'],
                    st.session_state['free_text_assumptions']
                )
                st.session_state['export_zip_filepath'] = zip_file_path
                
                # REPORTS_DIR_BASE is usually in source, but we can display the ID
                st.success(f"Export package generated successfully. ID: {current_run_id}")
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
