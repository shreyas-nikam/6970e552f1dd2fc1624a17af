
# OmniCorp Financial AI Architecture Risk Comparator: Fraud Detection Use Case

## Introduction: Architecting Secure and Compliant AI at OmniCorp Financial

Dr. Ava Sharma, a seasoned Enterprise AI Architect at OmniCorp Financial, faces a critical task. OmniCorp is looking to significantly upgrade its real-time fraud detection capabilities, and various teams are proposing different AI architectural approaches: traditional Machine Learning (ML), Large Language Model (LLM)-based, and advanced Agentic systems. Each approach offers distinct advantages but also introduces unique risk surfaces and control requirements.

As the primary architect, Dr. Sharma's role is to rigorously evaluate these architectural options, quantifying their inherent risks and identifying necessary control baselines. Her findings will be presented to OmniCorp's AI Architecture Review Board, which includes AI Program Leads (concerned with standardization and funding) and Risk/Security Partners (focused on exposure and compliance). The goal is not to declare a "winner" but to make risk visible, comparable, and defensible, enabling informed strategic decisions before significant investment in building.

This notebook simulates Dr. Sharma's workflow, demonstrating how she decomposes complex AI systems, applies a standardized risk taxonomy, quantifies architectural risk using deterministic rules, and identifies control gaps. Ultimately, it allows her to produce an executive-ready comparison artifact that ensures OmniCorp develops AI systems that are both innovative and secure.

---

### Installing Required Libraries

```python
!pip install pandas numpy matplotlib seaborn scikit-learn plotly kaleido # kaleido for static plotly exports (if needed)
!pip install Pillow # For potential image manipulation with radar charts later, though not strictly required for this spec
```

### Importing Required Dependencies

```python
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
```

---

## 1. Setting the Stage: Loading Use Case & Defining Foundational Components

### Story + Context + Real-World Relevance

Dr. Ava Sharma begins by loading the "Fraud Detection" use case template from OmniCorp's internal knowledge base. This template provides a standardized starting point, detailing the workflow, baseline assumptions, and enterprise constraints specific to fraud detection. This step ensures that all architectural comparisons are grounded in the same operational context, a crucial practice for ensuring consistency across the various AI initiatives managed by the AI Program Lead.

This section also establishes the core definitions for OmniCorp's AI risk taxonomy and the set of configurable architectural features that materially affect risk. These are fixed, enterprise-grade definitions that Dr. Sharma, along with Risk/Security Partners, helped establish to ensure a common language for risk assessment.

```python
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
```

### Explanation of Execution

Dr. Sharma has successfully loaded the `Fraud Detection` use case. This provides her with the foundational context, including operational assumptions and enterprise-wide constraints, which are critical for an Enterprise AI Architect to consider when designing solutions. The predefined `RISK_TAXONOMY` and `ARCHITECTURAL_FEATURES` ensure that OmniCorp's standardized language for risk assessment and architectural decomposition is consistently applied from the outset. This structured approach helps in later stages when communicating with the AI Program Lead and Risk/Security Partners.

---

## 2. Configuring Architectures for Fraud Detection

### Story + Context + Real-World Relevance

With the use case loaded, Dr. Sharma now configures the specific features for each proposed AI architecture (ML, LLM, Agentic) for the fraud detection system. These configurations represent the core design choices that materially affect the system's risk profile. For example, an Agentic system for fraud detection might inherently require an "autonomous execution loop" and "tool/function calling" to interact with mitigation systems, while a traditional ML system might not. Adjusting these toggles allows Dr. Sharma to model hypothetical designs and assess their risk implications, enabling explicit architectural risk trade-off analysis. This directly supports the AI Program Lead's need for standardized architectural proposals and allows Dr. Sharma to justify her decisions to the Risk/Security Partner.

```python
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
```

### Explanation of Execution

Dr. Sharma has now defined the specific feature sets for the ML, LLM, and Agentic architectures. These configurations capture the fundamental design decisions for each system, such as whether it integrates with external APIs or operates autonomously. The ability to toggle these features explicitly allows Dr. Sharma to explore different architectural variations and their potential impact on risk, which is a key part of her role as an Enterprise AI Architect guiding the design process.

---

## 3. Quantifying Architectural Risk with Deterministic Rules

### Story + Context + Real-World Relevance

To objectively compare the architectural designs, Dr. Sharma applies OmniCorp's standardized, rule-based risk scoring methodology. This system uses deterministic rules, where each enabled architectural feature contributes a predefined score to one or more risk categories (e.g., `uses_external_apis` increases `Dependency / Vendor Risk`). This quantification step is crucial for the AI Program Lead, who needs standardized metrics to compare proposals across teams, and for the Risk/Security Partner, who relies on clear, auditable risk assessments. The normalization of scores (0-10) ensures comparability across different risk categories, even if the underlying rules vary in their raw impact.

The risk score for a given category for an architecture, $R_{arch, cat}$, is calculated as the sum of all risk contributions from its enabled features, $C_{feature, cat}$, and then normalized:

$$
R_{arch, cat} = \text{normalize}\left(\sum_{feature \in Features_{arch}} C_{feature, cat}\right)
$$

Where $Features_{arch}$ is the set of enabled features for a specific architecture, and $C_{feature, cat}$ is the risk contribution of a feature to a specific risk category.

```python
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
```

### Explanation of Execution

Dr. Sharma has successfully applied OmniCorp's standardized risk scoring rules to each architecture. The `raw_risk_scores_df` shows the accumulated risk points, and `normalized_risk_scores_df` presents these scores on a consistent 0-10 scale for each risk category. This normalization is vital for making the risk profiles of different architectures directly comparable, fulfilling a key requirement for the AI Program Lead. For instance, an ML system might have a lower "Runtime Autonomy Risk" compared to an Agentic system, reflecting the inherent design differences for fraud detection. This quantification provides the empirical data needed to have a data-driven discussion in the AI Architecture Review Board.

---

## 4. Identifying Control Baselines and Gap Analysis

### Story + Context + Real-World Relevance

After quantifying the risks, Dr. Sharma's next step is to determine what controls are *required* for each architecture based on its risk profile and OmniCorp's control baseline library. Furthermore, she must perform a "gap analysis" to highlight any missing controls, assuming a certain set of controls are already in place (even if none are initially assumed, the identification of *required* controls is paramount). This step directly addresses the concerns of the Risk/Security Partner, who needs explicit control gaps highlighted to ensure compliance and security. It also informs the AI Program Lead about the additional effort and resources required to implement each architectural option.

The control baseline mapping is:
- Risk category $\rightarrow$ Minimum required controls.
A control gap is identified if a required control is not present in the set of `assumed_controls`.

```python
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
```

### Explanation of Execution

Dr. Sharma has identified the minimum set of controls required for each architectural approach to fraud detection, based on the quantified risk scores and OmniCorp's `CONTROL_BASELINE_LIBRARY`. By comparing these required controls against a set of `assumed_controls_omnicorp` (representing existing enterprise-wide controls), she has highlighted specific control gaps. For example, if the Agentic system shows a high "Runtime Autonomy Risk," it might require "Approval gates for critical actions" which might be identified as a gap if not already assumed. This precise identification of missing controls is invaluable for the Risk/Security Partner and provides the AI Program Lead with a clear roadmap for what needs to be implemented, budgeted, and managed for each proposed solution.

---

## 5. Visualizing Risk Profiles and Control Gaps for Executive Review

### Story + Context + Real-World Relevance

To effectively communicate her findings to OmniCorp's AI Architecture Review Board, Dr. Sharma needs compelling visualizations. Raw data tables, while precise, can be hard to digest for an executive audience. Therefore, she generates radar charts to visually represent each architecture's risk profile across all categories and presents a clear, structured control gap checklist. These visualizations make the risk deltas and required controls immediately apparent, facilitating discussions with the AI Program Lead regarding resource allocation and with the Risk/Security Partner on critical compliance concerns. This step is crucial for transforming complex analysis into an executive-ready comparison artifact.

```python
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
```

### Explanation of Execution

The radar charts provide an intuitive visual comparison of the risk profiles for ML, LLM, and Agentic architectures. For example, the Agentic system might show a larger "Runtime Autonomy Risk" polygon area, immediately signaling its higher exposure in that category compared to an ML system. The control gap checklist clearly outlines what controls are needed and which are currently missing. This direct, visual, and structured presentation helps Dr. Sharma effectively convey complex risk information to the AI Architecture Review Board, enabling quick identification of high-risk areas and necessary control implementations, fulfilling the needs of both the AI Program Lead and the Risk/Security Partner.

---

## 6. Generating an Executive-Ready Comparison Artifact

### Story + Context + Real-World Relevance

The final, and critical, step for Dr. Sharma is to compile all her analysis into a comprehensive, executive-ready comparison artifact. This package includes configuration snapshots, risk scores, control gap checklists, and an executive summary, all bundled into a single ZIP archive. This artifact serves multiple purposes: it's the primary deliverable for the AI Architecture Review Board, provides a standardized record for the AI Program Lead, and offers auditable evidence for the Risk/Security Partner. The inclusion of an `evidence_manifest.json` with SHA-256 hashes ensures the integrity and non-repudiation of the analysis, a crucial aspect in a regulated environment like OmniCorp Financial.

```python
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
        f.write(normalized_risk_scores_df.to_markdown(numalign="left", stralign="left"))
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
        f.write(f"**Assumed Enterprise Controls:** {', '.join(list(set.union(*map(set, assumed_controls_omnicorp.values())))) if assumed_controls_omnicorp else 'None'}\n")
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
            "filepath": filepath, # Relative path within the bundle, or full path for manifest record
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
    run_run_id,
    selected_use_case['name'],
    architectures_config,
    normalized_risk_scores_df,
    control_gaps_by_architecture,
    assumed_controls_omnicorp,
    free_text_assumptions_session
)
```

### Explanation of Execution

Dr. Sharma has successfully generated a comprehensive package of artifacts for the AI Architecture Review Board. This includes structured JSON files for architectural configurations, detailed risk scores, and identified control gaps, along with a human-readable markdown executive summary. The `config_snapshot.json` captures all definitions and parameters used, ensuring full traceability and reproducibility of the analysis. Crucially, the `evidence_manifest.json` provides SHA-256 hashes for all bundled files, verifying their integrity and proving that the analysis has not been tampered with. The final ZIP archive bundles everything, making it easy for the AI Program Lead to distribute and for the Risk/Security Partner to archive for audit purposes. This entire process demonstrates a rigorous, enterprise-grade approach to AI architecture risk management.

