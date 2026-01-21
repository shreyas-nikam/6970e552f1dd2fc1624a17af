import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import json
import shutil
import time
from source import *

# Set page configuration
st.set_page_config(
    page_title="QuLab: Lab 2: AI Architecture Comparator", layout="wide")

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
        # Merge standard risk rules with custom feature rules
        merged_risk_rules = dict(globals()['RISK_RULES'])

        if 'custom_features' in st.session_state:
            for feat_name, feat_data in st.session_state['custom_features'].items():
                merged_risk_rules[feat_name] = feat_data['risk_impacts']

        # Merge standard control library with custom controls
        merged_control_library = dict(globals()['CONTROL_BASELINE_LIBRARY'])

        if 'custom_controls' in st.session_state:
            for risk_cat, controls in st.session_state['custom_controls'].items():
                if risk_cat in merged_control_library:
                    merged_control_library[risk_cat] = list(
                        merged_control_library[risk_cat]) + controls
                else:
                    merged_control_library[risk_cat] = controls

        st.session_state['normalized_risk_scores_df'], st.session_state['raw_risk_scores_df'] = calculate_risk_scores(
            st.session_state['architectures_config'], globals(
            )['RISK_TAXONOMY'], merged_risk_rules
        )
        st.session_state['required_controls_by_architecture'] = identify_required_controls(
            st.session_state['normalized_risk_scores_df'], merged_control_library, globals()[
                'RISK_THRESHOLD']
        )
        st.session_state['control_gaps_by_architecture'] = perform_control_gap_analysis(
            st.session_state['required_controls_by_architecture'], st.session_state['assumed_controls_omnicorp']
        )
    else:
        st.warning(
            "Cannot calculate risks: Architectural configurations or global risk definitions are missing.")


def load_new_use_case():
    """Callback to load a new use case."""
    try:
        st.session_state['selected_use_case_data'] = load_use_case_template(
            USE_CASE_FILE, st.session_state['selected_use_case_name'])
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
        st.session_state['use_cases_list'] = [uc['name']
                                              for uc in all_use_cases]
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
        st.session_state['selected_use_case_data'] = load_use_case_template(
            USE_CASE_FILE, st.session_state['selected_use_case_name'])
    except Exception as e:
        # Only show error if we really can't load anything reasonable
        if st.session_state['selected_use_case_name']:
            st.error(f"Error loading default use case: {e}")
        st.session_state['selected_use_case_data'] = {}

if 'architectures_config' not in st.session_state:
    # Initialize with defaults from the loaded use case
    if st.session_state['selected_use_case_data']:
        st.session_state['architectures_config'] = st.session_state['selected_use_case_data'].get(
            'architectural_options_defaults', {"ML": {}, "LLM": {}, "Agent": {}})
    else:
        st.session_state['architectures_config'] = {
            "ML": {}, "LLM": {}, "Agent": {}}

if 'free_text_assumptions' not in st.session_state:
    st.session_state[
        'free_text_assumptions'] = "This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date."

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

if 'export_reports_path' not in st.session_state:
    st.session_state['export_reports_path'] = None

# Perform initial calculation if config is available and dataframes are empty
if st.session_state['architectures_config'] and st.session_state['normalized_risk_scores_df'].empty:
    recalculate_all_risks_and_controls()

# --- Sidebar Navigation ---

st.sidebar.title("Navigation")
page_options = ["Home", "1. Use Case & Configuration",
                "2. Risk & Control Comparison", "3. Export Artifacts"]

# Ensure current_page is valid
if st.session_state['current_page'] not in page_options:
    st.session_state['current_page'] = page_options[0]

# Use selectbox instead of radio
selected_page = st.sidebar.selectbox(
    "Go to Page:",
    page_options,
    index=page_options.index(st.session_state['current_page']),
    key='page_selector'
)

if selected_page != st.session_state['current_page']:
    st.session_state['current_page'] = selected_page
    st.rerun()

# --- Page Content ---

if st.session_state['current_page'] == 'Home':
    st.markdown(f"# OmniCorp Financial AI Architecture Risk Comparator")
    st.markdown(
        f"## Introduction: Architecting Secure and Compliant AI at OmniCorp Financial")
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

    st.markdown(
        f"## Setting the Stage: Loading Use Case & Defining Foundational Components")
    st.markdown(f"""
Dr. Ava Sharma begins by or adding a new one or loading a use case template from OmniCorp's internal knowledge base. This template provides a standardized starting point, detailing the workflow, baseline assumptions, and enterprise constraints specific to the use case. This step ensures that all architectural comparisons are grounded in the same operational context, a crucial practice for ensuring consistency across the various AI initiatives managed by the AI Program Lead.

This section also establishes the core definitions for OmniCorp's AI risk taxonomy and the set of configurable architectural features that materially affect risk. These are fixed, enterprise-grade definitions that Dr. Sharma, along with Risk/Security Partners, helped establish to ensure a common language for risk assessment.
""")

    st.markdown(f"---")

    # Tabs for Load and Add Use Cases
    uc_tab1, uc_tab2 = st.tabs(["📥 Load Use Case", "➕ Add Custom Use Case"])

    with uc_tab1:
        if st.session_state['use_cases_list']:
            try:
                current_index = st.session_state['use_cases_list'].index(
                    st.session_state['selected_use_case_name'])
            except ValueError:
                current_index = 0

            selected_uc_name = st.selectbox(
                "Choose a Use Case Template:",
                st.session_state['use_cases_list'],
                index=current_index,
                key='main_use_case_selector'
            )

            if selected_uc_name != st.session_state['selected_use_case_name']:
                st.session_state['selected_use_case_name'] = selected_uc_name
                load_new_use_case()
                st.rerun()
        else:
            st.warning("No use cases available.")

        st.subheader(
            f"Selected Use Case: {st.session_state['selected_use_case_name']}")
        if st.session_state['selected_use_case_data']:
            st.markdown(
                f"**Description:** {st.session_state['selected_use_case_data'].get('description', 'N/A')}")
            st.markdown(f"**Baseline Assumptions:**")
            baseline_assumptions = "\n".join(
                f"- {assumption}" for assumption in st.session_state['selected_use_case_data'].get('baseline_assumptions', []))
            st.markdown(baseline_assumptions)
            st.markdown(f"**Enterprise Constraints:**")
            enterprise_constraints = "\n".join(
                f"- {constraint}" for constraint in st.session_state['selected_use_case_data'].get('enterprise_constraints', []))
            st.markdown(enterprise_constraints)
            if st.button("Load This Use Case Configuration", type="primary"):
                # Load new configuration
                new_config = st.session_state['selected_use_case_data']['architectural_options_defaults']
                st.session_state['architectures_config'] = new_config

                # Update widget keys to match new configuration values
                architecture_types = ["ML", "LLM", "Agent"]
                features = globals().get('ARCHITECTURAL_FEATURES', [])
                for arch_type in architecture_types:
                    for feature in features:
                        widget_key = f"{arch_type}_{feature}"
                        new_value = new_config.get(arch_type, {}).get(feature)
                        if new_value is not None:
                            st.session_state[widget_key] = new_value

                recalculate_all_risks_and_controls()
                st.success(
                    f"Loaded configuration for {st.session_state['selected_use_case_name']}!")
                st.rerun()
        else:
            st.warning(
                "No use case data loaded. Please select and load a use case.")

    with uc_tab2:
        st.markdown("### Create a New Use Case")
        st.info(
            "Define your custom use case below. Once created, it will appear in the use case selector.")

        with st.form("add_use_case_form"):
            new_uc_name = st.text_input(
                "Use Case Name*", placeholder="e.g., Credit Risk Assessment")
            new_uc_description = st.text_area(
                "Description*", placeholder="Brief description of the use case...", height=100)

            st.markdown("**Baseline Assumptions** (one per line):")
            new_uc_assumptions = st.text_area("Baseline Assumptions",
                                              placeholder="e.g.,\nHigh availability required\nLow latency critical\nIntegration with existing systems",
                                              height=100)

            st.markdown("**Enterprise Constraints** (one per line):")
            new_uc_constraints = st.text_area("Enterprise Constraints",
                                              placeholder="e.g.,\nRegulatory compliance required\nData privacy must be protected\nBudget constraints apply",
                                              height=100)

            submitted = st.form_submit_button(
                "Create Use Case", type="primary")

            if submitted:
                if not new_uc_name or not new_uc_description:
                    st.error(
                        "Please provide both name and description for the use case.")
                else:
                    # Parse assumptions and constraints
                    assumptions_list = [
                        line.strip() for line in new_uc_assumptions.split('\n') if line.strip()]
                    constraints_list = [
                        line.strip() for line in new_uc_constraints.split('\n') if line.strip()]

                    # Create default architecture configuration with all features disabled/None
                    features = globals().get('ARCHITECTURAL_FEATURES', [])
                    new_arch_config = {"ML": {}, "LLM": {}, "Agent": {}}

                    for arch_type in ["ML", "LLM", "Agent"]:
                        for feature in features:
                            if feature == "human_approval_required":
                                new_arch_config[arch_type][feature] = "None"
                            else:
                                new_arch_config[arch_type][feature] = False

                    # Create new use case object
                    new_use_case = {
                        "name": new_uc_name,
                        "description": new_uc_description,
                        "baseline_assumptions": assumptions_list if assumptions_list else ["No specific assumptions provided"],
                        "enterprise_constraints": constraints_list if constraints_list else ["No specific constraints provided"],
                        "architectural_options_defaults": new_arch_config
                    }

                    # Load existing use cases from file
                    try:
                        with open(USE_CASE_FILE, 'r') as f:
                            all_use_cases = json.load(f)

                        # Check if use case name already exists
                        if any(uc['name'] == new_uc_name for uc in all_use_cases):
                            st.error(
                                f"A use case named '{new_uc_name}' already exists. Please use a different name.")
                        else:
                            # Add new use case
                            all_use_cases.append(new_use_case)

                            # Save back to file
                            with open(USE_CASE_FILE, 'w') as f:
                                json.dump(all_use_cases, f, indent=2)

                            # Update session state
                            st.session_state['use_cases_list'] = [
                                uc['name'] for uc in all_use_cases]
                            st.session_state['selected_use_case_name'] = new_uc_name
                            st.session_state['selected_use_case_data'] = new_use_case
                            st.session_state['architectures_config'] = new_arch_config

                            recalculate_all_risks_and_controls()
                            st.toast(
                                f"✅ Use case '{new_uc_name}' created successfully!", icon="✅")
                            time.sleep(1)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error saving use case: {e}")

    st.markdown(f"---")

    st.markdown(
        f"## Configuring Architectures for {st.session_state['selected_use_case_name']}")
    st.markdown(f"""
With the use case loaded, Dr. Sharma now configures the specific features for each proposed AI architecture. These configurations represent the core design choices that materially affect the system's risk profile. For example, an Agentic system might inherently require an "autonomous execution loop" and "tool/function calling" to interact with mitigation systems, while a traditional ML system might not. Adjusting these toggles allows Dr. Sharma to model hypothetical designs and assess their risk implications, enabling explicit architectural risk trade-off analysis. This directly supports the AI Program Lead's need for standardized architectural proposals and allows Dr. Sharma to justify her decisions to the Risk/Security Partner.
""")

    # Show Feature to Risk Mapping
    with st.expander("📊 View Feature-to-Risk Mapping Reference", expanded=False):
        st.markdown(
            "**How Architectural Features Contribute to Risk Categories:**")
        st.info("💡 Each enabled feature adds points to specific risk categories. Higher scores indicate higher risk.")

        risk_rules = globals().get('RISK_RULES', {})

        # Create a comprehensive mapping table
        mapping_data = []
        for feature, risks in risk_rules.items():
            if feature != "human_approval_required":
                for risk_cat, score in risks.items():
                    mapping_data.append({
                        "Feature": feature.replace('_', ' ').title(),
                        "Risk Category": risk_cat,
                        "Risk Points": f"+{score}"
                    })
            else:
                # Handle categorical feature
                for level, level_risks in risks.items():
                    for risk_cat, score in level_risks.items():
                        mapping_data.append({
                            "Feature": f"{feature.replace('_', ' ').title()} ({level})",
                            "Risk Category": risk_cat,
                            "Risk Points": f"+{score}"
                        })

        if mapping_data:
            mapping_df = pd.DataFrame(mapping_data)

            # Add color coding based on risk points
            def highlight_risk(val):
                if val.startswith('+'):
                    points = int(val[1:])
                    if points >= 3:
                        return 'background-color: #ffcccc'
                    elif points == 2:
                        return 'background-color: #ffffcc'
                    else:
                        return 'background-color: #ccffcc'
                return ''

            styled_df = mapping_df.style.applymap(
                highlight_risk, subset=['Risk Points'])
            st.dataframe(styled_df, use_container_width=True, height=400)

            # Add filter by feature
            col1, col2 = st.columns(2)
            with col1:
                selected_feature = st.selectbox(
                    "Filter by Feature:",
                    ["All Features"] +
                    sorted(mapping_df["Feature"].unique().tolist()),
                    key="feature_filter"
                )
            with col2:
                selected_risk = st.selectbox(
                    "Filter by Risk Category:",
                    ["All Categories"] +
                    sorted(mapping_df["Risk Category"].unique().tolist()),
                    key="risk_filter"
                )

            # Apply filters
            filtered_df = mapping_df.copy()
            if selected_feature != "All Features":
                filtered_df = filtered_df[filtered_df["Feature"]
                                          == selected_feature]
            if selected_risk != "All Categories":
                filtered_df = filtered_df[filtered_df["Risk Category"]
                                          == selected_risk]

            if len(filtered_df) < len(mapping_df):
                st.markdown("**Filtered Results:**")
                st.dataframe(filtered_df, use_container_width=True)

    # Architectural Feature Toggles (3-column layout)
    if st.session_state['architectures_config']:
        cols = st.columns(3)
        architecture_types = ["ML", "LLM", "Agent"]
        for i, arch_type in enumerate(architecture_types):
            with cols[i]:
                st.subheader(f"{arch_type} Architecture")
                current_config = st.session_state['architectures_config'].get(
                    arch_type, {})

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
                            update_config_and_recalculate(
                                arch_type, feature, new_value)

                    elif feature == "fine_tuned_model":
                        current_value = current_config.get(feature, False)
                        new_value = st.checkbox(
                            f"Fine-tuned Model",
                            value=current_value,
                            key=f"{arch_type}_{feature}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(
                                arch_type, feature, new_value)
                    elif feature == "real_time_execution":
                        current_value = current_config.get(feature, False)
                        new_value = st.checkbox(
                            f"Real-time Execution",
                            value=current_value,
                            key=f"{arch_type}_{feature}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(
                                arch_type, feature, new_value)
                    else:
                        current_value = current_config.get(feature, False)
                        new_value = st.checkbox(
                            f"{feature.replace('_', ' ').title()}",
                            value=current_value,
                            key=f"{arch_type}_{feature}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(
                                arch_type, feature, new_value)

                # Add custom features to the column view
                if 'custom_features' in st.session_state and st.session_state['custom_features']:
                    st.markdown("---")
                    st.markdown("**Custom Features:**")
                    for feat_name, feat_data in st.session_state['custom_features'].items():
                        current_value = current_config.get(feat_name, False)
                        new_value = st.checkbox(
                            feat_data['display_name'],
                            value=current_value,
                            key=f"{arch_type}_custom_{feat_name}",
                        )
                        if new_value != current_value:
                            update_config_and_recalculate(
                                arch_type, feat_name, new_value)
    else:
        st.warning(
            "Architectural configurations are not loaded. Please load a use case first.")

    st.markdown("---")
    st.markdown("## Add Custom Features")

    with st.expander("➕ Add Custom Feature-to-Risk Mapping", expanded=False):
        st.info(
            "Define custom architectural features and their impact on risk categories.")

        col1, col2 = st.columns([2, 1])

        with col1:
            custom_feature_name = st.text_input("Feature Name*",
                                                placeholder="e.g., uses_blockchain_integration",
                                                key="custom_feat_name")

        with col2:
            custom_feature_display = st.text_input("Display Name",
                                                   placeholder="e.g., Blockchain Integration",
                                                   help="How the feature appears in UI",
                                                   key="custom_feat_display")

        st.markdown("**Risk Impact Configuration:**")
        st.markdown(
            "Select which risk categories this feature affects and assign scores.")

        risk_taxonomy = globals().get('RISK_TAXONOMY', [])

        # Store selected risks and scores outside form
        if 'custom_feature_risks' not in st.session_state:
            st.session_state['custom_feature_risks'] = {}

        risk_cols = st.columns(2)
        selected_risks = {}

        for idx, risk_cat in enumerate(risk_taxonomy):
            with risk_cols[idx % 2]:
                enabled = st.checkbox(risk_cat, key=f"custom_risk_cb_{idx}")
                if enabled:
                    score = st.number_input(
                        f"Score for {risk_cat}",
                        min_value=1,
                        max_value=5,
                        value=2,
                        key=f"custom_score_input_{idx}",
                        help="Risk points contributed (1-5)"
                    )
                    selected_risks[risk_cat] = score

        st.markdown("**Architecture Enablement:**")
        arch_col1, arch_col2, arch_col3 = st.columns(3)

        with arch_col1:
            ml_enabled = st.checkbox(
                "Enable for ML", value=False, key="custom_ml_cb")
        with arch_col2:
            llm_enabled = st.checkbox(
                "Enable for LLM", value=False, key="custom_llm_cb")
        with arch_col3:
            agent_enabled = st.checkbox(
                "Enable for Agent", value=False, key="custom_agent_cb")

        if st.button("Add Custom Feature", type="primary", key="add_custom_feat_btn"):
            if not custom_feature_name:
                st.error("Please provide a feature name.")
            elif not selected_risks:
                st.error(
                    "Please select at least one risk category and assign a score.")
            else:
                # Add to session state custom features
                if 'custom_features' not in st.session_state:
                    st.session_state['custom_features'] = {}

                st.session_state['custom_features'][custom_feature_name] = {
                    "display_name": custom_feature_display or custom_feature_name.replace('_', ' ').title(),
                    "risk_impacts": selected_risks
                }

                # Initialize feature in architectures as False
                for arch_type in ["ML", "LLM", "Agent"]:
                    if arch_type in st.session_state['architectures_config']:
                        st.session_state['architectures_config'][arch_type][custom_feature_name] = False

                # Update architecture configurations based on checkboxes
                if ml_enabled and 'ML' in st.session_state['architectures_config']:
                    st.session_state['architectures_config']['ML'][custom_feature_name] = True
                if llm_enabled and 'LLM' in st.session_state['architectures_config']:
                    st.session_state['architectures_config']['LLM'][custom_feature_name] = True
                if agent_enabled and 'Agent' in st.session_state['architectures_config']:
                    st.session_state['architectures_config']['Agent'][custom_feature_name] = True

                recalculate_all_risks_and_controls()
                st.toast(
                    f"✅ Custom feature '{custom_feature_name}' added successfully!", icon="✅")
                time.sleep(1)
                st.rerun()

        # Display existing custom features
        if 'custom_features' in st.session_state and st.session_state['custom_features']:
            st.markdown("### Existing Custom Features")

            custom_features_data = []
            for feat_name, feat_data in st.session_state['custom_features'].items():
                risk_list = ", ".join(
                    [f"{k} (+{v})" for k, v in feat_data['risk_impacts'].items()])

                ml_status = "✅" if st.session_state['architectures_config'].get(
                    'ML', {}).get(feat_name, False) else "❌"
                llm_status = "✅" if st.session_state['architectures_config'].get(
                    'LLM', {}).get(feat_name, False) else "❌"
                agent_status = "✅" if st.session_state['architectures_config'].get(
                    'Agent', {}).get(feat_name, False) else "❌"

                custom_features_data.append({
                    "Feature": feat_data['display_name'],
                    "Risk Impacts": risk_list,
                    "ML": ml_status,
                    "LLM": llm_status,
                    "Agent": agent_status
                })

            if custom_features_data:
                custom_df = pd.DataFrame(custom_features_data)
                st.dataframe(custom_df, use_container_width=True)

    st.markdown("---")
    st.markdown("## Add Custom Controls")

    with st.expander("🛡️ Add Custom Control Baseline", expanded=False):
        st.info(
            "Add custom controls to risk categories. These will be included in the control baseline library.")

        # Initialize custom controls in session state
        if 'custom_controls' not in st.session_state:
            st.session_state['custom_controls'] = {}

        col1, col2 = st.columns([2, 1])

        with col1:
            new_control_text = st.text_area("Control Description*",
                                            placeholder="e.g., Implement multi-factor authentication for all system access",
                                            height=100,
                                            key="new_control_input")

        with col2:
            risk_taxonomy = globals().get('RISK_TAXONOMY', [])
            selected_risk_category = st.selectbox("Risk Category*",
                                                  risk_taxonomy,
                                                  key="new_control_category")

        if st.button("Add Control", type="primary", key="add_control_btn"):
            if not new_control_text:
                st.error("Please provide a control description.")
            else:
                # Add control to custom controls
                if selected_risk_category not in st.session_state['custom_controls']:
                    st.session_state['custom_controls'][selected_risk_category] = [
                    ]

                st.session_state['custom_controls'][selected_risk_category].append(
                    new_control_text)

                st.toast(
                    f"✅ Control added to {selected_risk_category}!", icon="🛡️")
                time.sleep(1)
                st.rerun()

        # Display existing custom controls
        if st.session_state['custom_controls']:
            st.markdown("### Custom Controls Added")

            for risk_cat, controls in st.session_state['custom_controls'].items():
                with st.expander(f"**{risk_cat}** ({len(controls)} custom control(s))"):
                    for idx, control in enumerate(controls, 1):
                        st.markdown(f"{idx}. {control}")

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

    if st.button("Recalculate Risk & Controls"):
        recalculate_all_risks_and_controls()
        st.success("Risk scores and controls recalculated!")

elif st.session_state['current_page'] == '2. Risk & Control Comparison':
    st.markdown(f"# 2. Architectural Risk & Control Comparison")

    st.markdown(f"## Quantifying Architectural Risk with Deterministic Rules")
    st.markdown(f"""
To objectively compare the architectural designs, Dr. Sharma applies OmniCorp's standardized, rule-based risk scoring methodology. This system uses deterministic rules, where each enabled architectural feature contributes a predefined score to one or more risk categories (e.g., `uses_external_apis` increases `Dependency / Vendor Risk`). This quantification step is crucial for the AI Program Lead, who needs standardized metrics to compare proposals across teams, and for the Risk/Security Partner, who relies on clear, auditable risk assessments. The normalization of scores (0-10) ensures comparability across different risk categories, even if the underlying rules vary in their raw impact.
""")

    st.markdown(
        r"The risk score for a given category for an architecture, $R_{arch, cat}$, is calculated as the sum of all risk contributions from its enabled features, $C_{feature, cat}$, and then normalized:")
    st.markdown(
        r"$$ R_{arch, cat} = \text{normalize}\left(\sum_{feature \in Features_{arch}} C_{feature, cat}\right) $$")
    st.markdown(
        r"where $Features_{arch}$ is the set of enabled features for a specific architecture, and $C_{feature, cat}$ is the risk contribution of a feature to a specific risk category.")

    if not st.session_state['normalized_risk_scores_df'].empty:
        st.subheader("Normalized Risk Scores (0-10 per category):")
        st.dataframe(st.session_state['normalized_risk_scores_df'])
    else:
        st.warning(
            "Risk scores not available. Please configure architectures and load a use case.")

    st.markdown(f"---")

    st.markdown(f"## Identifying Control Baselines and Gap Analysis")
    st.markdown(f"""
After quantifying the risks, Dr. Sharma's next step is to determine what controls are *required* for each architecture based on its risk profile and OmniCorp's control baseline library. Furthermore, she must perform a "gap analysis" to highlight any missing controls, assuming a certain set of controls are already in place (even if none are initially assumed, the identification of *required* controls is paramount). This step directly addresses the concerns of the Risk/Security Partner, who needs explicit control gaps highlighted to ensure compliance and security. It also informs the AI Program Lead about the additional effort and resources required to implement each architectural option.
""")
    st.markdown(r"The control baseline mapping is: Risk category $\rightarrow$ Minimum required controls. A control gap is identified if a required control is not present in the set of `assumed_controls`.")

    # Show Risk to Control Mapping
    with st.expander("🛡️ View Risk-to-Control Baseline Mapping Reference", expanded=False):
        st.markdown("**Required Controls by Risk Category:**")
        st.info(
            "💡 When a risk category score exceeds the threshold, these controls become mandatory.")

        control_library = globals().get('CONTROL_BASELINE_LIBRARY', {})

        # Create a comprehensive control mapping table
        control_mapping_data = []
        for risk_cat, controls in control_library.items():
            for idx, control in enumerate(controls, 1):
                control_mapping_data.append({
                    "Risk Category": risk_cat,
                    "Control #": idx,
                    "Required Control": control
                })

        if control_mapping_data:
            control_df = pd.DataFrame(control_mapping_data)

            # Display summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Risk Categories", len(control_library))
            with col2:
                st.metric("Total Controls", len(control_mapping_data))
            with col3:
                avg_controls = len(control_mapping_data) / len(control_library)
                st.metric("Avg Controls per Category", f"{avg_controls:.1f}")

            st.markdown("---")

            # Add tabs for different views
            tab1, tab2 = st.tabs(["📋 Table View", "🎯 By Risk Category"])

            with tab1:
                # Filter by risk category
                selected_risk_cat = st.selectbox(
                    "Filter by Risk Category:",
                    ["All Categories"] +
                    sorted(control_df["Risk Category"].unique().tolist()),
                    key="control_risk_filter"
                )

                filtered_control_df = control_df.copy()
                if selected_risk_cat != "All Categories":
                    filtered_control_df = filtered_control_df[filtered_control_df["Risk Category"]
                                                              == selected_risk_cat]

                st.dataframe(filtered_control_df,
                             use_container_width=True, height=400)

            with tab2:
                # Group by risk category with expandable sections
                for risk_cat in sorted(control_library.keys()):
                    with st.expander(f"**{risk_cat}** ({len(control_library[risk_cat])} controls)"):
                        for idx, control in enumerate(control_library[risk_cat], 1):
                            st.markdown(f"{idx}. {control}")

    if st.session_state['required_controls_by_architecture']:
        current_threshold = globals().get('RISK_THRESHOLD', 5)
        st.subheader(
            f"Interactive Control Gap Checklist (Risk Threshold >= {current_threshold})")

        st.info("✅ Check the controls that are already implemented. Unchecked controls represent gaps that need to be addressed.")

        # Initialize implemented controls in session state if not exists
        if 'implemented_controls' not in st.session_state:
            st.session_state['implemented_controls'] = {
                "ML": list(st.session_state.get('assumed_controls_omnicorp', {}).get('ML', [])),
                "LLM": list(st.session_state.get('assumed_controls_omnicorp', {}).get('LLM', [])),
                "Agent": list(st.session_state.get('assumed_controls_omnicorp', {}).get('Agent', []))
            }

        # Display architectures side-by-side in three columns
        cols = st.columns(3)
        architecture_types = ["ML", "LLM", "Agent"]

        for idx, arch_type in enumerate(architecture_types):
            with cols[idx]:
                st.markdown(f"### {arch_type} Architecture")

                required_controls = st.session_state['required_controls_by_architecture'].get(
                    arch_type, [])

                if not required_controls:
                    st.markdown(
                        "No specific controls required based on current risk profile and threshold.")
                    continue

                implemented = st.session_state['implemented_controls'].get(
                    arch_type, [])

                st.markdown(f"**Required Controls: {len(required_controls)}**")

                # Show control checkboxes
                updated_implemented = []
                for control in required_controls:
                    is_implemented = st.checkbox(
                        control,
                        value=(control in implemented),
                        key=f"control_{arch_type}_{hash(control)}"
                    )
                    if is_implemented:
                        updated_implemented.append(control)

                # Update session state
                st.session_state['implemented_controls'][arch_type] = updated_implemented

                # Calculate and display gaps
                gaps = [c for c in required_controls if c not in updated_implemented]

                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("✅ Implemented", len(updated_implemented))
                with col_b:
                    st.metric("❌ Gaps", len(gaps))

                if gaps:
                    with st.expander(f"View {len(gaps)} Gap(s)"):
                        for gap in gaps:
                            st.markdown(f"⚠️ {gap}")

        # Recalculate gaps button
        if st.button("Update Control Gap Analysis", type="secondary"):
            # Recalculate gaps based on checkbox selections
            updated_gaps = {}
            for arch_type in architecture_types:
                required = st.session_state['required_controls_by_architecture'].get(
                    arch_type, [])
                implemented = st.session_state['implemented_controls'].get(
                    arch_type, [])
                updated_gaps[arch_type] = [
                    c for c in required if c not in implemented]

            st.session_state['control_gaps_by_architecture'] = updated_gaps
            st.success("✅ Control gap analysis updated!")
            st.rerun()
    else:
        st.warning(
            "Control requirements not available. Please ensure risk calculations are complete.")

    st.markdown(f"---")

    st.markdown(f"## Visualizing Risk Profiles")
    st.markdown(f"""
To effectively communicate her findings to OmniCorp's AI Architecture Review Board, Dr. Sharma needs compelling visualizations. Raw data tables, while precise, can be hard to digest for an executive audience. Therefore, she generates radar charts to visually represent each architecture's risk profile across all categories. These visualizations make the risk deltas and required controls immediately apparent, facilitating discussions with the AI Program Lead regarding resource allocation and with the Risk/Security Partner on critical compliance concerns. This step is crucial for transforming complex analysis into an executive-ready comparison artifact.
""")

    if not st.session_state['normalized_risk_scores_df'].empty:
        try:
            if 'RISK_TAXONOMY' in globals():
                radar_fig = plot_risk_radar_chart(
                    st.session_state['normalized_risk_scores_df'], globals()['RISK_TAXONOMY'])
                st.plotly_chart(radar_fig, use_container_width=True)
            else:
                st.warning("Global RISK_TAXONOMY missing, cannot plot chart.")
        except Exception as e:
            st.error(f"Error generating radar chart: {e}")
            st.warning(
                "Ensure the `plot_risk_radar_chart` function in `source.py` returns a Plotly figure object.")
    else:
        st.warning(
            "Cannot generate radar chart: Normalized risk scores are not available.")

elif st.session_state['current_page'] == '3. Export Artifacts':
    st.markdown(f"# 3. Generating an Executive-Ready Comparison Artifact")
    st.markdown(f"""
The final, and critical, step for Dr. Sharma is to compile all her analysis into a comprehensive, executive-ready comparison artifact. This package includes configuration snapshots, risk scores, control gap checklists, and an executive summary, all bundled into a single ZIP archive. This artifact serves multiple purposes: it's the primary deliverable for the AI Architecture Review Board, provides a standardized record for the AI Program Lead, and offers auditable evidence for the Risk/Security Partner. The inclusion of an `evidence_manifest.json` with SHA-256 hashes ensures the integrity and non-repudiation of the analysis, a crucial aspect in a regulated environment like OmniCorp Financial.
""")

    st.markdown(
        f"## Export Summary for {st.session_state['selected_use_case_name']}")
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
                zip_file_path, reports_path = export_artifacts(
                    st.session_state['run_id'],
                    st.session_state['selected_use_case_name'],
                    st.session_state['selected_use_case_data'],
                    st.session_state['architectures_config'],
                    st.session_state['normalized_risk_scores_df'],
                    st.session_state['control_gaps_by_architecture'],
                    st.session_state['assumed_controls_omnicorp'],
                    st.session_state['free_text_assumptions']
                )
                st.session_state['export_zip_filepath'] = zip_file_path
                st.session_state['export_reports_path'] = reports_path

                # REPORTS_DIR_BASE is usually in source, but we can display the ID
                st.success(
                    f"Export package generated successfully. ID: {current_run_id}")
            except Exception as e:
                st.error(f"Error generating export package: {e}")
                st.session_state['export_zip_filepath'] = None
        else:
            st.warning(
                "Please ensure a use case is loaded and risk calculations are complete before exporting.")

    if st.session_state['export_zip_filepath'] and os.path.exists(st.session_state['export_zip_filepath']):
        col1, col2 = st.columns([3, 1])

        with col1:
            with open(st.session_state['export_zip_filepath'], "rb") as fp:
                st.download_button(
                    label="Download Export Package (.zip)",
                    data=fp.read(),
                    file_name=os.path.basename(
                        st.session_state['export_zip_filepath']),
                    mime="application/zip",
                )

        with col2:
            if st.button("🗑️ Clean Up Files", type="secondary"):
                try:
                    # Remove the ZIP file
                    if st.session_state['export_zip_filepath'] and os.path.exists(st.session_state['export_zip_filepath']):
                        os.remove(st.session_state['export_zip_filepath'])

                    # Remove the reports directory
                    if st.session_state['export_reports_path'] and os.path.exists(st.session_state['export_reports_path']):
                        shutil.rmtree(st.session_state['export_reports_path'])

                    # Clear session state
                    st.session_state['export_zip_filepath'] = None
                    st.session_state['export_reports_path'] = None
                    st.session_state['run_id'] = None

                    st.success("Export files cleaned up successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error cleaning up files: {e}")


# License
st.caption('''
---
## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
''')
