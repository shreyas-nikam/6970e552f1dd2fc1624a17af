id: 6970e552f1dd2fc1624a17af_documentation
summary: Lab 2: AI Architecture Comparator Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Lab 2: AI Architecture Comparator - A Developer's Guide

## 1. Introduction: Architecting Secure & Compliant AI
Duration: 00:05

Welcome to QuLab: Lab 2: AI Architecture Comparator! This codelab provides a comprehensive guide for developers to understand, run, and extend a Streamlit application designed to facilitate the comparison of different AI architectural approaches (such as traditional Machine Learning, Large Language Models, and Agentic systems) from a risk and control perspective.

<aside class="positive">
This application addresses a critical need in enterprise AI development: making **architectural risk visible, comparable, and defensible**. It helps organizations make informed strategic decisions before committing significant resources to building AI systems.
</aside>

**The Challenge:**
In large organizations like OmniCorp Financial, Enterprise AI Architects like Dr. Ava Sharma are tasked with evaluating various AI proposals for critical functions (e.g., real-time fraud detection). Each architectural choice brings a unique risk surface and demands specific control measures. The challenge lies in objectively comparing these diverse approaches, quantifying their risks, identifying control gaps, and presenting these findings to stakeholders like AI Program Leads and Risk/Security Partners in a clear, actionable manner.

**Application Overview:**
This Streamlit application simulates Dr. Sharma's workflow, providing a structured approach to:
1.  **Decompose AI Systems:** Break down complex AI systems into configurable architectural features that materially impact risk.
2.  **Quantify Risk:** Apply a standardized risk taxonomy and deterministic rules to assign risk scores to each architectural option based on its features.
3.  **Identify Controls & Gaps:** Determine required security controls for each architecture and highlight any missing controls against an assumed baseline.
4.  **Visualize & Compare:** Generate intuitive visualizations (e.g., radar charts) to make risk profiles immediately understandable.
5.  **Generate Artifacts:** Produce an executive-ready comparison package, including a summary and auditable evidence.

**Key Concepts Explained:**
*   **AI Architecture Comparison:** Evaluating different design paradigms for AI systems (ML, LLM, Agent) and their implications.
*   **Risk Taxonomy:** A standardized classification of potential risks (e.g., Data Privacy, Model Bias, Dependency Risk).
*   **Deterministic Risk Scoring:** Using predefined rules to assign numerical risk values based on system features, ensuring consistency and auditability.
*   **Control Baseline:** A set of minimum security and operational controls expected for systems with certain risk profiles.
*   **Control Gap Analysis:** Identifying where existing or assumed controls fall short of the required baseline for a new system.

This codelab will walk you through the application's structure, its core logic (residing in an assumed `source.py` file), and how to extend its capabilities.

## 2. Setting Up Your Development Environment
Duration: 00:10

To get started, you'll need Python installed and the necessary libraries. We'll assume you have the main application file (`main.py`) and a `source.py` file, along with a `use_cases.json` for predefined use cases.

### Prerequisites

1.  **Python:** Ensure you have Python 3.8+ installed.
2.  **Required Libraries:** Install the necessary Python packages using `pip`.

    ```console
    pip install streamlit pandas plotly
    ```

### Application Structure

Your project directory should typically look like this:

```
your-project/
├── main.py
├── source.py
└── use_cases.json
```

*   `main.py`: This is the Streamlit application itself, handling UI, session state, and orchestrating calls to `source.py`.
*   `source.py`: (Assumed) This file contains the core business logic, data definitions (risk taxonomy, rules, controls), and utility functions for risk calculation, control identification, plotting, and artifact generation.
*   `use_cases.json`: This JSON file stores predefined use case templates, including descriptions, baseline assumptions, constraints, and default architectural configurations.

### Understanding `use_cases.json`

The `use_cases.json` file is crucial for defining the context of your AI projects. It's a list of dictionaries, where each dictionary represents a use case.

**Example `use_cases.json` Structure:**

```json
[
  {
    "name": "Real-time Fraud Detection",
    "description": "Evaluating AI architectures for a new real-time fraud detection system.",
    "baseline_assumptions": [
      "Existing enterprise security controls are effective and up-to-date.",
      "Data privacy regulations (e.g., GDPR, CCPA) are fully adhered to."
    ],
    "enterprise_constraints": [
      "All models must be auditable and explainable.",
      "Maximum acceptable latency for real-time decisions is 100ms."
    ],
    "architectural_options_defaults": {
      "ML": {
        "uses_external_apis": false,
        "human_approval_required": "Partial",
        "fine_tuned_model": false,
        "real_time_execution": true,
        "data_ingestion_frequency": "Continuous",
        "model_retraining_frequency": "Weekly",
        "private_data_access": true,
        "third_party_model_integration": false,
        "autonomous_execution_loop": false,
        "tool_function_calling": false
      },
      "LLM": {
        "uses_external_apis": true,
        "human_approval_required": "Partial",
        "fine_tuned_model": true,
        "real_time_execution": true,
        "data_ingestion_frequency": "Continuous",
        "model_retraining_frequency": "Monthly",
        "private_data_access": true,
        "third_party_model_integration": true,
        "autonomous_execution_loop": false,
        "tool_function_calling": false
      },
      "Agent": {
        "uses_external_apis": true,
        "human_approval_required": "None",
        "fine_tuned_model": true,
        "real_time_execution": true,
        "data_ingestion_frequency": "Continuous",
        "model_retraining_frequency": "As Needed",
        "private_data_access": true,
        "third_party_model_integration": true,
        "autonomous_execution_loop": true,
        "tool_function_calling": true
      }
    }
  }
]
```

### Running the Application

Navigate to your project directory in the terminal and run the Streamlit application:

```console
streamlit run main.py
```

This command will open the application in your default web browser.

## 3. Understanding the Core Components: `source.py`
Duration: 00:15

The `source.py` file is the brain of the operation. It defines the foundational data structures for risk assessment and implements the core logic for calculating risks, identifying controls, and generating visualizations/exports.

**Assumed Contents of `source.py`:**

### Data Definitions

1.  **`ARCHITECTURAL_FEATURES`**: A list of strings defining all possible configurable features for an AI architecture.

    ```python
    ARCHITECTURAL_FEATURES = [
        "uses_external_apis",
        "human_approval_required", # Special handling in UI: "None", "Partial", "Mandatory"
        "fine_tuned_model",        # Special handling in UI: checkbox for "Fine-tuned vs Base Model"
        "real_time_execution",     # Special handling in UI: checkbox for "Real-time vs Batch Execution"
        "data_ingestion_frequency", # Placeholder, could be a dropdown (e.g., "Continuous", "Daily", "Batch")
        "model_retraining_frequency", # Placeholder, could be a dropdown (e.g., "Weekly", "Monthly", "As Needed")
        "private_data_access",
        "third_party_model_integration",
        "autonomous_execution_loop",
        "tool_function_calling"
    ]
    ```

2.  **`RISK_TAXONOMY`**: A list of dictionaries, where each dictionary defines a risk category, its description, and its relative importance/weight.

    ```python
    RISK_TAXONOMY = [
        {"name": "Data Privacy / PII Handling", "description": "Risks related to sensitive data access and processing.", "weight": 8},
        {"name": "Model Bias / Fairness", "description": "Risks from unfair or biased model outcomes.", "weight": 7},
        {"name": "Security Vulnerabilities", "description": "Risks from software flaws and attack vectors.", "weight": 9},
        {"name": "Dependency / Vendor Risk", "description": "Risks from reliance on external services or models.", "weight": 6},
        {"name": "Operational Stability / Reliability", "description": "Risks from system failures or performance issues.", "weight": 5},
        {"name": "Autonomous Action / Control", "description": "Risks from systems taking actions without human oversight.", "weight": 10},
        {"name": "Explainability / Interpretability", "description": "Risks from inability to understand model decisions.", "weight": 7},
        {"name": "Compliance / Regulatory", "description": "Risks from failing to meet legal or industry standards.", "weight": 8},
        {"name": "Data Quality / Integrity", "description": "Risks from inaccurate or corrupted input data.", "weight": 6},
        {"name": "Resource Consumption / Cost", "description": "Risks from high operational costs.", "weight": 4}
    ]
    ```

3.  **`RISK_RULES`**: A dictionary that maps architectural features to their risk contributions across different categories. This is the core of the deterministic risk scoring.

    ```python
    RISK_RULES = {
        "uses_external_apis": {"Dependency / Vendor Risk": 3, "Security Vulnerabilities": 2, "Operational Stability / Reliability": 1},
        "human_approval_required": {
            "None": {"Autonomous Action / Control": 5, "Model Bias / Fairness": 2},
            "Partial": {"Autonomous Action / Control": 3},
            "Mandatory": {"Autonomous Action / Control": 1}
        },
        "fine_tuned_model": {"Model Bias / Fairness": 2, "Explainability / Interpretability": 1},
        "real_time_execution": {"Operational Stability / Reliability": 3, "Resource Consumption / Cost": 2},
        "private_data_access": {"Data Privacy / PII Handling": 4, "Security Vulnerabilities": 2},
        "third_party_model_integration": {"Dependency / Vendor Risk": 4, "Model Bias / Fairness": 2, "Security Vulnerabilities": 3},
        "autonomous_execution_loop": {"Autonomous Action / Control": 5, "Operational Stability / Reliability": 3},
        "tool_function_calling": {"Autonomous Action / Control": 4, "Security Vulnerabilities": 3, "Dependency / Vendor Risk": 2}
        # ... other rules ...
    }
    ```

4.  **`CONTROL_BASELINE_LIBRARY`**: A dictionary that maps risk categories to a list of recommended controls.

    ```python
    CONTROL_BASELINE_LIBRARY = {
        "Data Privacy / PII Handling": ["Data encryption (at rest/in transit)", "Data anonymization/pseudonymization", "Access control lists (ACLs)", "Data retention policies"],
        "Model Bias / Fairness": ["Bias detection and mitigation tools", "Regular fairness audits", "Explainable AI (XAI) techniques"],
        "Security Vulnerabilities": ["Vulnerability scanning", "Secure coding practices", "Penetration testing", "Incident response plan"],
        "Dependency / Vendor Risk": ["Vendor SLA review", "Third-party risk assessment", "Supply chain security audits"],
        "Operational Stability / Reliability": ["Monitoring and alerting systems", "Disaster recovery plan", "Redundancy and failover mechanisms"],
        "Autonomous Action / Control": ["Human-in-the-loop review", "Rollback mechanisms", "Comprehensive audit logs", "Kill switch functionality"],
        "Explainability / Interpretability": ["LIME/SHAP integration", "Model documentation", "Feature importance analysis"],
        "Compliance / Regulatory": ["Regulatory impact assessments", "Data governance framework", "Compliance auditing"],
        "Data Quality / Integrity": ["Data validation routines", "Data lineage tracking", "Data reconciliation"],
        "Resource Consumption / Cost": ["Cost monitoring and optimization", "Resource allocation limits"]
    }
    ```

5.  **`RISK_THRESHOLD`**: An integer defining the minimum normalized risk score in a category that mandates specific controls.

    ```python
    RISK_THRESHOLD = 5 # Example: If a risk category score is 5 or higher, specific controls are required.
    ```

### Core Functions

1.  **`load_use_case_template(file_path, use_case_name)`**:
    Loads a specific use case from the `use_cases.json` file.

    ```python
    # Signature example
    def load_use_case_template(file_path: str, use_case_name: str) -> dict:
        # ... logic to read JSON and find use case ...
        pass
    ```

2.  **`calculate_risk_scores(architectures_config, risk_taxonomy, risk_rules)`**:
    Calculates raw and normalized risk scores for each architecture based on its features and the defined risk rules. Normalization typically scales scores to a 0-10 range for comparability.

    ```python
    # Signature example
    def calculate_risk_scores(
        architectures_config: dict,
        risk_taxonomy: list,
        risk_rules: dict
    ) -> (pd.DataFrame, pd.DataFrame):
        # ... logic to iterate architectures, features, apply rules, and normalize ...
        pass
    ```

3.  **`identify_required_controls(normalized_risk_scores_df, control_baseline_library, risk_threshold)`**:
    Determines which controls are required for each architecture by comparing its normalized risk scores against the `RISK_THRESHOLD` and looking up controls in the `CONTROL_BASELINE_LIBRARY`.

    ```python
    # Signature example
    def identify_required_controls(
        normalized_risk_scores_df: pd.DataFrame,
        control_baseline_library: dict,
        risk_threshold: int
    ) -> dict:
        # ... logic to identify controls based on risk scores and threshold ...
        pass
    ```

4.  **`perform_control_gap_analysis(required_controls_by_architecture, assumed_controls_omnicorp)`**:
    Compares the `required_controls` for each architecture with OmniCorp's `assumed_controls` to highlight any gaps.

    ```python
    # Signature example
    def perform_control_gap_analysis(
        required_controls_by_architecture: dict,
        assumed_controls_omnicorp: dict
    ) -> dict:
        # ... logic to compare lists of controls ...
        pass
    ```

5.  **`plot_risk_radar_chart(normalized_risk_scores_df, risk_taxonomy)`**:
    Generates a Plotly radar chart visualization of the normalized risk scores across architectures.

    ```python
    # Signature example
    def plot_risk_radar_chart(
        normalized_risk_scores_df: pd.DataFrame,
        risk_taxonomy: list
    ) -> go.Figure:
        # ... Plotly code to create a radar chart ...
        pass
    ```

6.  **`export_artifacts(...)`**:
    Gathers all analysis results (config, scores, gaps, summary) and packages them into a ZIP file, including an `evidence_manifest.json` for integrity.

    ```python
    # Signature example (simplified)
    def export_artifacts(
        run_id: str,
        use_case_name: str,
        architectures_config: dict,
        normalized_risk_scores_df: pd.DataFrame,
        control_gaps_by_architecture: dict,
        assumed_controls_omnicorp: dict,
        free_text_assumptions: str
    ) -> str: # Returns path to the generated zip file
        # ... logic to write files and create zip ...
        pass
    ```

### Conceptual Flow of Risk Calculation and Control Gap Analysis

To better visualize how these components interact, consider the following flowcharts:

#### **Risk Scoring Flow**
```mermaid
graph TD
    A[Architectural Configurations] --> B{Retrieve RISK_RULES};
    B --> C{Iterate Architectures & Features};
    C --> D{Calculate Raw Risk Scores per Category};
    D --> E{Normalize Scores (0-10)};
    E --> F[Raw & Normalized Risk Scores DataFrames];
```

#### **Control Gap Analysis Flow**
```mermaid
graph TD
    G[Normalized Risk Scores] --> H{Compare with RISK_THRESHOLD};
    H --> I{Retrieve Controls from CONTROL_BASELINE_LIBRARY};
    I --> J[Required Controls per Architecture];
    J --> K{Compare with Assumed Controls (OmniCorp)};
    K --> L[Identified Control Gaps per Architecture];
```

## 4. Navigating the Application: Use Case & Configuration
Duration: 00:15

Let's walk through the user interface and understand how it interacts with the backend logic.

### Home Page

The "Home" page (`st.session_state['current_page'] == 'Home'`) serves as an introduction to the application, setting the context for Dr. Ava Sharma's task and outlining the learning objectives. It's designed to provide stakeholders with an immediate understanding of the tool's purpose and value.

### Sidebar Navigation and Use Case Selection

The sidebar is your primary tool for navigating between the application's stages and selecting a use case.

```python
# main.py snippet for sidebar navigation
st.sidebar.title("Navigation")
page_options = ["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"]
st.session_state['current_page'] = st.sidebar.radio(
    "Go to", 
    page_options, 
    index=page_options.index(st.session_state['current_page'])
)

st.sidebar.header("Select Use Case")
# ... use case selection logic ...
selected_uc_name = st.sidebar.selectbox(
    "Choose a Use Case Template:",
    st.session_state['use_cases_list'],
    index=current_index,
    key='sidebar_use_case_selector'
)

if selected_uc_name != st.session_state['selected_use_case_name']:
    st.session_state['selected_use_case_name'] = selected_uc_name
    st.sidebar.button("Load Use Case", on_click=load_new_use_case)
```

When you select a new use case from the `st.sidebar.selectbox` and click "Load Use Case", the `load_new_use_case` callback function is triggered. This function loads the relevant data from `use_cases.json` into `st.session_state` and then calls `recalculate_all_risks_and_controls()` to update the risk assessment based on the new defaults.

### 1. Use Case & Architecture Configuration Page

This is where you define the specific characteristics of each AI architecture you want to compare.

#### Use Case Details

Upon navigating to "1. Use Case & Configuration", the application displays details of the `selected_use_case_name`, including its description, baseline assumptions, and enterprise constraints. These details are pulled directly from `st.session_state['selected_use_case_data']`, which was loaded by `load_new_use_case()`.

#### Architectural Feature Toggles

The core of this page is the configuration section, presented in a 3-column layout for ML, LLM, and Agent architectures. Each column contains a series of Streamlit widgets (checkboxes and select boxes) corresponding to the `ARCHITECTURAL_FEATURES` defined in `source.py`.

```python
# main.py snippet for architectural feature configuration
cols = st.columns(3)
architecture_types = ["ML", "LLM", "Agent"]
for i, arch_type in enumerate(architecture_types):
    with cols[i]:
        st.subheader(f"{arch_type} Architecture")
        current_config = st.session_state['architectures_config'].get(arch_type, {})
        
        for feature in globals().get('ARCHITECTURAL_FEATURES', []):
            if feature == "human_approval_required":
                options = ["None", "Partial", "Mandatory"]
                current_value = current_config.get(feature, options[0])
                new_value = st.selectbox(
                    f"{feature.replace('_', ' ').title()}:",
                    options,
                    index=options.index(current_value),
                    key=f"{arch_type}_{feature}",
                )
            elif feature == "fine_tuned_model":
                current_value = current_config.get(feature, False)
                new_value = st.checkbox(
                    f"Fine-tuned vs Base Model",
                    value=current_value,
                    key=f"{arch_type}_{feature}",
                )
            # ... similar logic for other specific features ...
            else: 
                current_value = current_config.get(feature, False)
                new_value = st.checkbox(
                    f"{feature.replace('_', ' ').title()}",
                    value=current_value,
                    key=f"{arch_type}_{feature}",
                )
            
            if new_value != current_value:
                update_config_and_recalculate(arch_type, feature, new_value)
```

<aside class="negative">
Notice the use of <code>globals().get('ARCHITECTURAL_FEATURES', [])</code>. This ensures that the application can still render even if <code>source.py</code> hasn't been fully loaded or <code>ARCHITECTURAL_FEATURES</code> isn't immediately available, preventing crashes.
</aside>

#### The `update_config_and_recalculate` Callback

Every time a user changes a feature (e.g., checks a checkbox or selects a new option), the `update_config_and_recalculate` function is called.

```python
# main.py snippet for update_config_and_recalculate
def update_config_and_recalculate(arch_type, feature, value):
    """Callback to update configuration and recalculate risks."""
    if arch_type in st.session_state['architectures_config']:
        st.session_state['architectures_config'][arch_type][feature] = value
        recalculate_all_risks_and_controls()
```

This function updates the `st.session_state['architectures_config']` with the new feature value and then immediately triggers `recalculate_all_risks_and_controls()`. This ensures that the risk scores and control requirements are always up-to-date with the latest architectural configurations. This real-time feedback is crucial for Dr. Sharma to understand the impact of design choices instantly.

#### Free-Text Assumptions

A text area is provided for entering "Free-Text Assumptions". This allows for capturing qualitative context that might influence the quantitative analysis, ensuring a holistic record. This text is stored in `st.session_state['free_text_assumptions']` and will be included in the exported artifacts.

## 5. Deep Dive into Risk & Control Comparison
Duration: 00:20

This section of the application provides the core analysis results: quantified risk scores, identified control requirements, and a visual comparison of the architectures.

### 2. Risk & Control Comparison Page

Upon navigating to "2. Risk & Control Comparison", the application displays the calculated risk scores and control gaps.

#### Normalized Risk Scores

The application presents the `normalized_risk_scores_df` as a Pandas DataFrame. These scores, ranging from 0-10, allow for a quick comparison of risk profiles across different categories for each architecture.

```python
# main.py snippet for displaying risk scores
if not st.session_state['normalized_risk_scores_df'].empty:
    st.subheader("Normalized Risk Scores (0-10 per category):")
    st.dataframe(st.session_state['normalized_risk_scores_df'])
else:
    st.warning("Risk scores not available. Please configure architectures and load a use case.")
```

The normalization process for a risk score $R_{arch, cat}$ for a given architecture (`arch`) and risk category (`cat`) is typically achieved by taking the sum of contributions from enabled features and scaling it to a 0-10 range. If $S_{arch, cat}$ is the sum of raw risk contributions for an architecture in a category, and $S_{max, cat}$ is the maximum possible raw score for that category across all potential features, then:

$$ R_{arch, cat} = 10 \times \frac{S_{arch, cat}}{S_{max, cat}} $$

This mathematical approach ensures that even if different categories have varying maximum raw scores, they are always compared on the same 0-10 scale.

#### Control Baselines and Gap Analysis

This section is vital for the Risk/Security Partner. It details the controls required based on the calculated risks and then highlights any `MISSING (GAP)` controls by comparing them against the `assumed_controls_omnicorp`.

```python
# main.py snippet for control gap analysis display
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
```

The `RISK_THRESHOLD` (e.g., 5) plays a crucial role here. A control for a specific risk category is deemed "required" only if the normalized risk score for that category in an architecture meets or exceeds this threshold. The `perform_control_gap_analysis` function then identifies which of these required controls are not present in the `st.session_state['assumed_controls_omnicorp']` for that architecture.

#### Visualizing Risk Profiles with Radar Charts

For executive audiences, visualizations are key. The application generates a radar chart (also known as a spider chart) using Plotly, which visually compares the risk profiles of the ML, LLM, and Agent architectures across all risk categories.

```python
# main.py snippet for radar chart
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
```

This chart instantly highlights which architectures have higher risk in particular categories and where their risk profiles diverge. For instance, an Agentic system might show a significantly larger "Autonomous Action / Control" risk area compared to a traditional ML system.

## 6. Generating and Understanding Exported Artifacts
Duration: 00:10

The final stage of the application is to compile all the analysis into a comprehensive, auditable export package. This is the primary deliverable for review boards and compliance teams.

### 3. Export Artifacts Page

This page outlines the artifacts that will be generated and provides a button to trigger the export process.

```python
# main.py snippet for export button
if st.button("Generate Export & Download Package"):
    if not st.session_state['normalized_risk_scores_df'].empty and st.session_state['architectures_config']:
        current_run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state['run_id'] = current_run_id
        
        try:
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
            
            st.success(f"Export package generated successfully. ID: {current_run_id}")
        except Exception as e:
            st.error(f"Error generating export package: {e}")
            st.session_state['export_zip_filepath'] = None
    else:
        st.warning("Please ensure a use case is loaded and risk calculations are complete before exporting.")
```

When the "Generate Export & Download Package" button is clicked, the `export_artifacts` function from `source.py` is invoked. This function takes all the relevant session state data, processes it, and saves it into a structured directory, finally zipping it up.

#### Generated Artifacts

The ZIP archive typically contains the following files, each serving a specific purpose:

*   **`architecture_config.json`**: A JSON snapshot of the exact architectural features configured for ML, LLM, and Agent architectures during this session. This provides the input data that drove the analysis.
*   **`risk_scores_by_architecture.json`**: Contains both raw and normalized risk scores for all architectures and risk categories. This is the quantified output of the risk assessment.
*   **`control_gaps_checklist.json`**: A detailed list of required controls and identified gaps for each architecture. This is crucial for planning remediation and compliance.
*   **`session02_executive_summary.md`**: A markdown file providing a narrative summary of the analysis, including the use case, key findings, and free-text assumptions. This makes the analysis human-readable and presentable.
*   **`config_snapshot.json`**: A snapshot of all global definitions (`RISK_TAXONOMY`, `RISK_RULES`, `CONTROL_BASELINE_LIBRARY`, `RISK_THRESHOLD`) used during this specific analysis run. This ensures full reproducibility and auditability of the results.
*   **`evidence_manifest.json`**: A critical file containing SHA-256 hashes of all other generated artifacts within the package.

<aside class="positive">
The <b><code>evidence_manifest.json</code></b> is especially important in regulated environments like OmniCorp Financial. It provides cryptographic proof that the generated artifacts have not been tampered with since their creation, ensuring the integrity and non-repudiation of the analysis.
</aside>

After successful generation, a "Download Export Package (.zip)" button appears, allowing users to download the complete set of artifacts.

## 7. Extending and Customizing the Application
Duration: 00:15

This application is designed to be extensible. As a developer, you can customize and enhance various aspects to fit new requirements or refine the existing methodology.

### 1. Adding New Architectural Features

To introduce a new architectural feature:
1.  **Update `ARCHITECTURAL_FEATURES` in `source.py`**: Add the new feature's string identifier to this list.
2.  **Update `main.py` UI**: In the "1. Use Case & Configuration" section, add a new `st.checkbox` or `st.selectbox` for your feature. Remember to call `update_config_and_recalculate` on change.
    *   If it's a simple boolean feature, a `st.checkbox` is sufficient.
    *   If it has multiple states (like `human_approval_required`), use `st.selectbox` and handle its options.
3.  **Update `RISK_RULES` in `source.py`**: Define how this new feature contributes to various risk categories.

    ```python
    # Example: Adding a new feature 'uses_blockchain_ledger'
    ARCHITECTURAL_FEATURES = [
        # ... existing features ...
        "uses_blockchain_ledger" 
    ]

    RISK_RULES = {
        # ... existing rules ...
        "uses_blockchain_ledger": {
            "Operational Stability / Reliability": 2,
            "Resource Consumption / Cost": 3,
            "Security Vulnerabilities": 1
        }
    }
    ```

### 2. Modifying Risk Categories and Rules

*   **Add/Remove Risk Categories**: Modify the `RISK_TAXONOMY` list in `source.py`. Remember to update `RISK_RULES` and `CONTROL_BASELINE_LIBRARY` if you add new categories.
*   **Adjust Risk Contributions**: Change the numerical values in `RISK_RULES` to reflect a different weighting of a feature's impact on a risk category.
*   **Refine Normalization**: If the 0-10 scale for `normalized_risk_scores_df` doesn't fit, you could adjust the normalization logic in `calculate_risk_scores` in `source.py`.

### 3. Customizing Control Baselines

*   **Update `CONTROL_BASELINE_LIBRARY` in `source.py`**: Add new controls or modify existing ones for specific risk categories.
*   **Adjust `RISK_THRESHOLD`**: Changing `RISK_THRESHOLD` will directly impact how many controls are deemed "required" based on the risk scores. A higher threshold means fewer controls are mandated.

### 4. Creating New Use Case Templates

To add new use cases without modifying code:
1.  **Edit `use_cases.json`**: Add a new JSON object to the array, following the existing structure.
2.  Define `name`, `description`, `baseline_assumptions`, `enterprise_constraints`, and critically, `architectural_options_defaults` for your new use case. These defaults will pre-populate the configuration toggles when the use case is loaded.

### 5. Enhancements and Future Work

Consider these potential enhancements:

*   **Dynamic `assumed_controls_omnicorp`**: Allow users to edit the assumed controls directly in the UI, rather than having them hardcoded in `main.py`. This would enable more flexible gap analysis.
*   **More Sophisticated Risk Models**: Instead of simple additive rules, implement more complex risk models (e.g., multiplicative risks, contextual risk factors).
*   **User Authentication/Authorization**: For a production enterprise environment, integrate user login and role-based access control.
*   **Database Integration**: Store use cases, architectural configurations, and analysis results in a database instead of JSON files and session state for better persistence and scalability.
*   **Interactive Risk Rule Editor**: Create a UI for defining and modifying `RISK_RULES` directly within the application, abstracting `source.py` further.
*   **Generate Different Report Formats**: Besides Markdown, allow exporting to PDF or other presentation formats.

By following these guidelines and understanding the underlying structure, you can effectively leverage and expand the capabilities of the QuLab AI Architecture Comparator to meet evolving architectural assessment needs.
