import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import hashlib
import zipfile
import os
from datetime import datetime
import plotly.graph_objects as go

# Ensure matplotlib and seaborn are set up for consistent plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('viridis')
# Define file paths and constants
USE_CASE_FILE = "sample_usecases.json"
REPORTS_DIR_BASE = "reports/session02"

# Define the risk taxonomy (fixed categories as per OmniCorp's standard)
RISK_TAXONOMY = [
    "Data Risk",
    "Model Risk",
    "Security Risk",
    "Operational Risk",
    "Transparency / Explainability Risk",
    "Dependency / Vendor Risk",
    "Runtime Autonomy Risk"
]

# Define all configurable architectural features
ARCHITECTURAL_FEATURES = [
    "uses_external_apis",
    "uses_rag_vector_store",
    "uses_tool_function_calling",
    "autonomous_execution_loop",
    "human_approval_required", # Categorical: None, Partial, Mandatory
    "fine_tuned_model",
    "real_time_execution"
]

# Create a dummy sample_usecases.json for demonstration if it doesn't exist
if not os.path.exists(USE_CASE_FILE):
    sample_usecases_data = [
        {
            "name": "Fraud Detection",
            "description": "Real-time detection and mitigation of suspicious financial activities.",
            "baseline_assumptions": [
                "High availability of the system is critical.",
                "Low latency for real-time decisions is crucial.",
                "Integration with existing financial systems is mandatory.",
                "Robust audit trails are required."
            ],
            "enterprise_constraints": [
                "Strict regulatory compliance (e.g., PCI DSS, AML, Basel III).",
                "Adherence to OmniCorp's Ethical AI guidelines.",
                "Data privacy (PII) must be protected.",
                "Budgetary constraints for infrastructure and operational costs."
            ],
            "architectural_options_defaults": {
                "ML": {
                    "uses_external_apis": False,
                    "uses_rag_vector_store": False,
                    "uses_tool_function_calling": False,
                    "autonomous_execution_loop": False,
                    "human_approval_required": "Partial",
                    "fine_tuned_model": False,
                    "real_time_execution": True
                },
                "LLM": {
                    "uses_external_apis": True,
                    "uses_rag_vector_store": True,
                    "uses_tool_function_calling": False,
                    "autonomous_execution_loop": False,
                    "human_approval_required": "Partial",
                    "fine_tuned_model": True,
                    "real_time_execution": True
                },
                "Agent": {
                    "uses_external_apis": True,
                    "uses_rag_vector_store": True,
                    "uses_tool_function_calling": True,
                    "autonomous_execution_loop": True,
                    "human_approval_required": "None",
                    "fine_tuned_model": True,
                    "real_time_execution": True
                }
            }
        },
        {
            "name": "Customer Support Automation",
            "description": "Automating responses to common customer queries and routing complex cases.",
            "baseline_assumptions": ["High accuracy in intent recognition", "Scalability for peak loads"],
            "enterprise_constraints": ["Brand voice consistency", "Data privacy"],
            "architectural_options_defaults": {
                "ML": {
                    "uses_external_apis": False, "uses_rag_vector_store": False, "uses_tool_function_calling": False,
                    "autonomous_execution_loop": False, "human_approval_required": "Partial", "fine_tuned_model": False,
                    "real_time_execution": True
                },
                "LLM": {
                    "uses_external_apis": True, "uses_rag_vector_store": True, "uses_tool_function_calling": False,
                    "autonomous_execution_loop": False, "human_approval_required": "Partial", "fine_tuned_model": True,
                    "real_time_execution": True
                },
                "Agent": {
                    "uses_external_apis": True, "uses_rag_vector_store": True, "uses_tool_function_calling": True,
                    "autonomous_execution_loop": True, "human_approval_required": "None", "fine_tuned_model": True,
                    "real_time_execution": True
                }
            }
        }
    ]
    with open(USE_CASE_FILE, 'w') as f:
        json.dump(sample_usecases_data, f, indent=4)

def load_use_case_template(filename, use_case_name):
    """
    Loads a specific use case template from a JSON file.

    Args:
        filename (str): The path to the JSON file containing use cases.
        use_case_name (str): The name of the use case to load.

    Returns:
        dict: The loaded use case template.

    Raises:
        ValueError: If the use case is not found.
    """
    with open(filename, 'r') as f:
        use_cases = json.load(f)
    for uc in use_cases:
        if uc["name"] == use_case_name:
            return uc
    raise ValueError(f"Use case '{use_case_name}' not found in {filename}")

# Load the "Fraud Detection" use case
selected_use_case = load_use_case_template(USE_CASE_FILE, "Fraud Detection")

print(f"Loaded Use Case: {selected_use_case['name']}")
print(f"Description: {selected_use_case['description']}")
print(f"Baseline Assumptions: {selected_use_case['baseline_assumptions']}")
print(f"Enterprise Constraints: {selected_use_case['enterprise_constraints']}")
# Define the architectural configurations based on the selected use case defaults,
# but allow for manual overrides to simulate design choices.
# Dr. Sharma can modify these feature toggles to explore different scenarios.

architectures_config = selected_use_case["architectural_options_defaults"]

# Example: Adjust an LLM architecture for minimal human approval for specific, low-impact fraud alerts
# architectures_config['LLM']['human_approval_required'] = "None"

# Example: Imagine a highly autonomous ML system
# architectures_config['ML']['autonomous_execution_loop'] = True

# Display current configuration
print("Current Architectural Configurations:")
for arch_type, config in architectures_config.items():
    print(f"\n--- {arch_type} Architecture ---")
    for feature, value in config.items():
        print(f"  {feature}: {value}")
# Define deterministic, config-driven, and versioned rule-based risk scoring definitions
# Each rule maps an architectural feature to its risk contributions across categories.
# Values represent points added to a risk category.
# These rules are part of OmniCorp's standardized risk assessment framework.
RISK_RULES = {
    "uses_external_apis": {"Dependency / Vendor Risk": 3, "Security Risk": 1},
    "uses_rag_vector_store": {"Data Risk": 2, "Security Risk": 1, "Transparency / Explainability Risk": 1},
    "uses_tool_function_calling": {"Security Risk": 2, "Operational Risk": 2, "Runtime Autonomy Risk": 1},
    "autonomous_execution_loop": {"Runtime Autonomy Risk": 3, "Operational Risk": 2, "Security Risk": 1},
    "human_approval_required": { # Categorical treatment for this feature
        "None": {"Operational Risk": 2, "Transparency / Explainability Risk": 2},
        "Partial": {"Operational Risk": 1, "Transparency / Explainability Risk": 1},
        "Mandatory": {"Operational Risk": 0, "Transparency / Explainability Risk": 0},
    },
    "fine_tuned_model": {"Model Risk": 2, "Operational Risk": 1, "Transparency / Explainability Risk": 1},
    "real_time_execution": {"Operational Risk": 2, "Security Risk": 1, "Data Risk": 1}
}

def calculate_risk_scores(architectures_config, risk_taxonomy, risk_rules):
    """
    Calculates raw and normalized risk scores for each architecture based on enabled features and rules.

    Args:
        architectures_config (dict): Dictionary where keys are architecture types (e.g., "ML")
                                     and values are dictionaries of feature toggles.
        risk_taxonomy (list): List of defined risk categories.
        risk_rules (dict): Dictionary mapping features to their risk contributions.

    Returns:
        pd.DataFrame: A DataFrame with normalized risk scores (0-10) for each architecture and category.
        pd.DataFrame: A DataFrame with raw risk scores for each architecture and category.
    """
    raw_scores = {arch_type: {category: 0 for category in risk_taxonomy}
                  for arch_type in architectures_config.keys()}

    for arch_type, config in architectures_config.items():
        for feature, is_enabled in config.items():
            if feature in risk_rules:
                if isinstance(is_enabled, bool): # Handle boolean features
                    if is_enabled:
                        for risk_category, score_impact in risk_rules[feature].items():
                            if risk_category in risk_taxonomy:
                                raw_scores[arch_type][risk_category] += score_impact
                elif feature == "human_approval_required": # Handle categorical feature
                    approval_level = is_enabled
                    if approval_level in risk_rules[feature]:
                        for risk_category, score_impact in risk_rules[feature][approval_level].items():
                            if risk_category in risk_taxonomy:
                                raw_scores[arch_type][risk_category] += score_impact

    raw_scores_df = pd.DataFrame(raw_scores).T

    # Normalize scores to a 0-10 scale per category
    normalized_scores_df = pd.DataFrame(index=raw_scores_df.index, columns=raw_scores_df.columns)
    for col in raw_scores_df.columns:
        min_val = raw_scores_df[col].min()
        max_val = raw_scores_df[col].max()
        if max_val == min_val: # Avoid division by zero if all scores for a category are the same
            normalized_scores_df[col] = 0.0 # Or some default low risk if all are same
        else:
            normalized_scores_df[col] = (raw_scores_df[col] - min_val) / (max_val - min_val) * 10

    # Fill NaN with 0 if there were no features contributing to a category
    normalized_scores_df = normalized_scores_df.fillna(0.0)

    return normalized_scores_df.round(2), raw_scores_df

# Calculate the risk scores
normalized_risk_scores_df, raw_risk_scores_df = calculate_risk_scores(
    architectures_config, RISK_TAXONOMY, RISK_RULES
)

print("\nRaw Risk Scores:")
print(raw_risk_scores_df)

print("\nNormalized Risk Scores (0-10 per category):")
print(normalized_risk_scores_df)
# Define OmniCorp's Control Baseline Library, mapping risk categories to minimum required controls.
# These are fixed expectations for any AI system within OmniCorp.
CONTROL_BASELINE_LIBRARY = {
    "Data Risk": ["Data anonymization/pseudonymization", "Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Data retention policies"],
    "Model Risk": ["Model validation (drift/bias)", "Model documentation (RID)", "Change control for models", "Regular model retraining"],
    "Security Risk": ["Vulnerability scanning", "Secure coding practices", "Intrusion detection systems", "Least privilege access"],
    "Operational Risk": ["Incident response plan", "Monitoring & alerting", "Business continuity plan", "Disaster recovery plan"],
    "Transparency / Explainability Risk": ["XAI framework implementation", "Audit trails of decisions", "User communication of AI use"],
    "Dependency / Vendor Risk": ["Vendor SLA review", "Fallback strategy for external APIs", "Third-party risk assessment"],
    "Runtime Autonomy Risk": ["Step limits on actions", "Approval gates for critical actions", "Comprehensive audit logs", "Kill switch functionality"]
}

def identify_required_controls(risk_scores_df, control_baseline_library, risk_threshold=5):
    """
    Identifies required controls for each architecture based on risk scores exceeding a threshold.

    Args:
        risk_scores_df (pd.DataFrame): Normalized risk scores for each architecture and category.
        control_baseline_library (dict): Mapping of risk categories to minimum required controls.
        risk_threshold (int): The minimum normalized risk score (0-10) in a category
                              to trigger the requirement for its associated controls.

    Returns:
        dict: A dictionary where keys are architecture types and values are lists of required controls.
    """
    required_controls = {arch_type: set() for arch_type in risk_scores_df.index}

    for arch_type in risk_scores_df.index:
        for category in risk_scores_df.columns:
            if risk_scores_df.loc[arch_type, category] >= risk_threshold:
                if category in control_baseline_library:
                    required_controls[arch_type].update(control_baseline_library[category])

    return {arch: sorted(list(controls)) for arch, controls in required_controls.items()}

def perform_control_gap_analysis(required_controls_by_arch, assumed_controls_by_arch=None):
    """
    Compares required controls against assumed controls to identify gaps.

    Args:
        required_controls_by_arch (dict): Dictionary of architecture types to lists of required controls.
        assumed_controls_by_arch (dict, optional): Dictionary of architecture types to lists of assumed controls.
                                                If None, no controls are assumed, and all required are gaps.

    Returns:
        dict: A dictionary where keys are architecture types and values are lists of control gaps.
    """
    control_gaps = {}
    if assumed_controls_by_arch is None:
        assumed_controls_by_arch = {arch_type: [] for arch_type in required_controls_by_arch.keys()}

    for arch_type, required in required_controls_by_arch.items():
        assumed = set(assumed_controls_by_arch.get(arch_type, []))
        gaps = [control for control in required if control not in assumed]
        control_gaps[arch_type] = sorted(gaps)

    return control_gaps

# Identify required controls (e.g., if a risk category score is 5 or higher)
RISK_THRESHOLD = 5 # OmniCorp's internal threshold for mandatory controls
required_controls_by_architecture = identify_required_controls(
    normalized_risk_scores_df, CONTROL_BASELINE_LIBRARY, RISK_THRESHOLD
)

print(f"\nRequired Controls (for categories with normalized risk score >= {RISK_THRESHOLD}):")
for arch_type, controls in required_controls_by_architecture.items():
    print(f"--- {arch_type} Architecture ---")
    if controls:
        for control in controls:
            print(f"  - {control}")
    else:
        print("  No specific controls required based on current risk profile and threshold.")

# Define some *assumed* controls for demonstration (e.g., some basic security is always in place)
# Dr. Sharma might input these based on existing enterprise-wide security measures.
assumed_controls_omnicorp = {
    "ML": ["Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Vulnerability scanning", "Secure coding practices", "Incident response plan"],
    "LLM": ["Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Vulnerability scanning", "Secure coding practices", "Incident response plan", "Vendor SLA review"],
    "Agent": ["Access control lists (ACLs)", "Data encryption (at rest/in transit)", "Vulnerability scanning", "Secure coding practices", "Incident response plan", "Vendor SLA review", "Comprehensive audit logs"]
}

# Perform control gap analysis
control_gaps_by_architecture = perform_control_gap_analysis(
    required_controls_by_architecture, assumed_controls_omnicorp
)

print("\nControl Gaps Identified:")
for arch_type, gaps in control_gaps_by_architecture.items():
    print(f"--- {arch_type} Architecture ---")
    if gaps:
        for gap in gaps:
            print(f"  - {gap} (MISSING)")
    else:
        print("  No control gaps identified for this architecture.")
def plot_risk_radar_chart(df_normalized_scores, risk_taxonomy):
    """
    Generates a radar chart for each architecture's normalized risk scores.

    Args:
        df_normalized_scores (pd.DataFrame): Normalized risk scores (0-10) for each architecture and category.
        risk_taxonomy (list): List of defined risk categories.
    """
    num_architectures = len(df_normalized_scores)

    fig = go.Figure()

    categories = risk_taxonomy
    num_categories = len(categories)

    for arch_type in df_normalized_scores.index:
        values = df_normalized_scores.loc[arch_type].tolist()
        # Ensure the radar chart closes the loop by appending the first value again
        values = values + values[:1]

        # Create a list of angular positions for each category
        angles = [n / float(num_categories) * 2 * np.pi for n in range(num_categories)]
        angles = angles + angles[:1] # Close the loop

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]], # Close the loop for labels
            fill='toself',
            name=arch_type,
            hovertemplate='<b>%{theta}</b>: %{r:.2f}<extra></extra>'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10], # Risk scores are normalized 0-10
                tickvals=[0, 2, 4, 6, 8, 10],
                showline=True,
                linecolor='gray',
                linewidth=1
            ),
            angularaxis=dict(
                rotation=90, # Start labels from top
                direction="clockwise", # Arrange categories clockwise
                tickfont_size=10
            )
        ),
        showlegend=True,
        title="Architectural Risk Profile Comparison (Normalized Scores 0-10)",
        height=600,
        width=800
    )
    fig.show()

# Generate radar charts
print("Generating Risk Radar Charts...")
plot_risk_radar_chart(normalized_risk_scores_df, RISK_TAXONOMY)

# Display the control gap checklist in a human-readable format
def display_control_gap_checklist(required_controls, control_gaps):
    """
    Displays the required controls and highlights control gaps.

    Args:
        required_controls (dict): Dictionary of architecture types to lists of required controls.
        control_gaps (dict): Dictionary of architecture types to lists of control gaps.
    """
    print("\n--- Comprehensive Control Gap Checklist ---")
    for arch_type in required_controls.keys():
        print(f"\n### {arch_type} Architecture Controls")

        if not required_controls[arch_type]:
            print("- No specific controls required based on current risk profile and threshold.")
            continue

        print("#### Required Controls:")
        for control in required_controls[arch_type]:
            status = "✅ Present (or assumed)"
            if control in control_gaps[arch_type]:
                status = "❌ MISSING (GAP)"
            print(f"- {control} {status}")
    print("\n--- End of Checklist ---")

display_control_gap_checklist(required_controls_by_architecture, control_gaps_by_architecture)
import pandas as pd
import numpy as np
import json
import hashlib
import zipfile
import os
from datetime import datetime
# Note: matplotlib.pyplot, seaborn, plotly.graph_objects are imported in a previous cell (Cell 3)
# and their styles/palettes are set globally, so they are not repeated here.

# Re-load selected_use_case from its original source to ensure it's a dictionary.
# This addresses potential issues where 'selected_use_case' might have been
# inadvertently overwritten in the global scope by a function definition (e.g., a pytest fixture)
# or become unavailable due to kernel state changes.
# The 'load_use_case_template' function and 'USE_CASE_FILE' global variable are
# assumed to be defined and available from previous cells (Cell 5).
try:
    if 'load_use_case_template' in globals() and 'USE_CASE_FILE' in globals():
        # Access the global variable directly if it exists, to re-assign it.
        # This explicitly ensures `selected_use_case` holds the expected dictionary value.
        selected_use_case = globals()['load_use_case_template'](globals()['USE_CASE_FILE'], "Fraud Detection")
    else:
        # Fallback if the necessary components for re-loading are missing.
        # In a typical notebook flow, this branch should not be reached if previous cells ran successfully.
        print("Warning: 'load_use_case_template' or 'USE_CASE_FILE' not found in globals. "
              "Ensure previous cells have been executed.")
        # If selected_use_case is already defined but corrupted, this might still fail.
        # If it's not defined, a NameError will occur later.
except Exception as e:
    print(f"Error re-loading selected_use_case: {e}. Attempting to proceed with existing variable (if any).")


def generate_sha256(filepath):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

# Dummy invocation for verification as per requirements
# This block is for testing generate_sha256 locally and should not affect global state
dummy_file_path = "dummy_file_for_hash.txt"
with open(dummy_file_path, "w") as f:
    f.write("This is a test file for hashing.")
dummy_hash = generate_sha256(dummy_file_path)
print(f"Test file '{dummy_file_path}' SHA-256 hash: {dummy_hash}")
os.remove(dummy_file_path) # Clean up the dummy file

def export_artifacts(run_id, use_case_name, architectures_config, normalized_risk_scores_df,
                     control_gaps_by_architecture, assumed_controls_omnicorp, free_text_assumptions=""):
    """
    Exports all generated artifacts to a specified directory structure and bundles them into a ZIP archive.

    Args:
        run_id (str): Unique identifier for the current run (e.g., timestamp).
        use_case_name (str): The name of the use case.
        architectures_config (dict): The configuration of each architecture.
        normalized_risk_scores_df (pd.DataFrame): Normalized risk scores.
        control_gaps_by_architecture (dict): Identified control gaps.
        assumed_controls_omnicorp (dict): Controls assumed to be in place.
        free_text_assumptions (str): Optional free-text assumptions to include.
    """
    # Access global variables defined in previous cells directly.
    # No 'global' keyword is needed for reading global variables within a function.
    global REPORTS_DIR_BASE, ARCHITECTURAL_FEATURES, RISK_TAXONOMY, RISK_RULES, \
           CONTROL_BASELINE_LIBRARY, RISK_THRESHOLD, selected_use_case


    reports_path = os.path.join(REPORTS_DIR_BASE, run_id)
    os.makedirs(reports_path, exist_ok=True)

    # 1. architecture_config.json
    arch_config_path = os.path.join(reports_path, "architecture_config.json")
    with open(arch_config_path, 'w') as f:
        json.dump(architectures_config, f, indent=4)
    print(f"Exported: {arch_config_path}")

    # 2. risk_scores_by_architecture.json
    risk_scores_path = os.path.join(reports_path, "risk_scores_by_architecture.json")
    normalized_risk_scores_df.to_json(risk_scores_path, indent=4, orient='index')
    print(f"Exported: {risk_scores_path}")

    # 3. control_gaps_checklist.json
    control_gaps_path = os.path.join(reports_path, "control_gaps_checklist.json")
    with open(control_gaps_path, 'w') as f:
        json.dump(control_gaps_by_architecture, f, indent=4)
    print(f"Exported: {control_gaps_path}")

    # 4. session02_executive_summary.md
    executive_summary_path = os.path.join(reports_path, "session02_executive_summary.md")
    with open(executive_summary_path, 'w') as f:
        f.write(f"# Executive Summary: AI Architecture Risk Assessment for {use_case_name}\n\n")
        f.write(f"**Date of Analysis:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Primary Analyst:** Dr. Ava Sharma (Enterprise AI Architect, OmniCorp Financial)\n")
        f.write(f"**Objective:** This report compares the architectural risk profiles of proposed ML, LLM, and Agentic systems for **{use_case_name}** to facilitate informed decision-making by the AI Architecture Review Board.\n\n")
        f.write(f"## Key Findings:\n")
        f.write(f"1.  **ML Architecture:** Generally exhibits lower inherent risk, particularly in 'Runtime Autonomy Risk' and 'Dependency / Vendor Risk', due to less reliance on external APIs and autonomous loops. However, 'Model Risk' remains a key concern.\n")
        f.write(f"2.  **LLM Architecture:** Introduces elevated risks in 'Data Risk' (due to RAG/vector stores), 'Dependency / Vendor Risk' (external APIs), and 'Model Risk' (fine-tuning complexity). Benefits from robust NLU but requires careful data governance.\n")
        f.write(f"3.  **Agentic Architecture:** Presents the highest 'Runtime Autonomy Risk' and 'Security Risk' due to autonomous execution and tool-calling capabilities. While offering significant automation potential, it mandates the most stringent control requirements.\n\n")
        f.write(f"## Risk Profile Summary (Normalized 0-10):\n")
        try:
            f.write(normalized_risk_scores_df.to_markdown(numalign="left", stralign="left"))
        except ImportError:
            # Fallback if tabulate is not installed
            f.write(normalized_risk_scores_df.to_string())
            f.write("\n\n*Note: 'tabulate' library not found. Table formatted using .to_string(). Install 'tabulate' for better markdown formatting.*\n")
        f.write(f"\n\n*See `risk_scores_by_architecture.json` for detailed scores.*\n\n")
        f.write(f"## Control Gap Analysis:\n")
        f.write(f"Based on OmniCorp's control baseline library and a risk threshold of {RISK_THRESHOLD} (normalized score), the following control gaps were identified when comparing against assumed enterprise controls:\n\n")
        for arch_type, gaps in control_gaps_by_architecture.items():
            f.write(f"### {arch_type} Architecture Gaps:\n")
            if gaps:
                for gap in gaps:
                    f.write(f"- ❌ **{gap}**\n")
            else:
                f.write("- No critical control gaps identified beyond assumed enterprise controls.\n")
        f.write(f"\n*See `control_gaps_checklist.json` for a full list.*\n\n")
        f.write(f"## Recommendations:\n")
        f.write(f"1.  For highly autonomous systems (e.g., Agentic), prioritize implementation of 'Kill switch functionality' and 'Approval gates for critical actions'.\n")
        f.write(f"2.  For LLM-based systems, strengthen 'Data anonymization/pseudonymization' and 'Vendor SLA review' processes.\n")
        f.write(f"3.  Ensure continuous model validation and explainability frameworks are in place for all architectures, especially given the 'Model Risk'.\n\n")
        f.write(f"## Assumptions and Context:\n")
        f.write(f"**Use Case:** {use_case_name}\n")
        f.write(f"**Use Case Description:** {selected_use_case['description']}\n")
        f.write(f"**Baseline Assumptions:** {', '.join(selected_use_case['baseline_assumptions'])}\n")
        f.write(f"**Enterprise Constraints:** {', '.join(selected_use_case['enterprise_constraints'])}\n")

        # Robustly handle assumed_controls_omnicorp which might be empty
        all_assumed_controls_set = set()
        if assumed_controls_omnicorp:
            for arch_controls_list in assumed_controls_omnicorp.values():
                all_assumed_controls_set.update(arch_controls_list)
        assumed_controls_str = ', '.join(sorted(list(all_assumed_controls_set))) if all_assumed_controls_set else 'None'
        f.write(f"**Assumed Enterprise Controls:** {assumed_controls_str}\n")

        if free_text_assumptions:
            f.write(f"**Additional Free-Text Assumptions:** {free_text_assumptions}\n")
        f.write(f"\n---")
    print(f"Exported: {executive_summary_path}")

    # 5. config_snapshot.json
    config_snapshot_path = os.path.join(reports_path, "config_snapshot.json")
    snapshot_data = {
        "use_case_name": use_case_name,
        "architectural_features_definition": ARCHITECTURAL_FEATURES,
        "risk_taxonomy_definition": RISK_TAXONOMY,
        "risk_rules_definition": RISK_RULES,
        "control_baseline_library_definition": CONTROL_BASELINE_LIBRARY,
        "risk_threshold_for_controls": RISK_THRESHOLD,
        "assumed_controls_for_gap_analysis": assumed_controls_omnicorp,
        "free_text_assumptions": free_text_assumptions
    }
    with open(config_snapshot_path, 'w') as f:
        json.dump(snapshot_data, f, indent=4)
    print(f"Exported: {config_snapshot_path}")

    # --- Evidence Manifest and Zipping ---
    # Prepare list of files to be included in the manifest and zip
    files_to_bundle = [
        arch_config_path,
        risk_scores_path,
        control_gaps_path,
        executive_summary_path,
        config_snapshot_path
    ]

    # 6. evidence_manifest.json
    evidence_manifest_path = os.path.join(reports_path, "evidence_manifest.json")
    manifest_data = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "artifacts": []
    }
    for filepath in files_to_bundle:
        manifest_data["artifacts"].append({
            "filename": os.path.basename(filepath),
            "filepath": filepath, # Full path for manifest record
            "sha256_hash": generate_sha256(filepath)
        })
    with open(evidence_manifest_path, 'w') as f:
        json.dump(manifest_data, f, indent=4)
    print(f"Exported: {evidence_manifest_path}")
    files_to_bundle.append(evidence_manifest_path) # Add manifest itself to the zip

    # Bundle all generated files into a single ZIP archive
    zip_filename = os.path.join(REPORTS_DIR_BASE, f"Session_02_{run_id}.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_bundle:
            arcname = os.path.join(run_id, os.path.basename(file_path))
            zipf.write(file_path, arcname)
    print(f"\nAll artifacts bundled into: {zip_filename}")
    print(f"Report directory: {reports_path}")


# Define free-text assumptions for the current analysis session
free_text_assumptions_session = "This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date. The risk threshold for mandatory controls (5/10) reflects a moderate risk appetite for new AI initiatives."

# Generate a unique run ID based on timestamp
current_run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Export all artifacts
export_artifacts(
    current_run_id,
    selected_use_case['name'],
    architectures_config,
    normalized_risk_scores_df,
    control_gaps_by_architecture,
    assumed_controls_omnicorp,
    free_text_assumptions_session
)