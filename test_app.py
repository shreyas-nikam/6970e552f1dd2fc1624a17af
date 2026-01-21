
import pytest
import json
import os
import pandas as pd
import tempfile
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest

# Define dummy content for use_cases.json that the app will attempt to load
DUMMY_USE_CASES_CONTENT = [
    {
        "name": "Fraud Detection Use Case",
        "description": "Detecting financial fraud in real-time transactions.",
        "baseline_assumptions": ["Existing security controls are effective.", "Data privacy regulations are adhered to."],
        "enterprise_constraints": ["Real-time processing required.", "Low latency for decisions."],
        "architectural_options_defaults": {
            "ML": {
                "uses_external_apis": False,
                "human_approval_required": "Partial",
                "fine_tuned_model": False,
                "real_time_execution": True,
                "data_drift_monitoring": True,
                "concept_drift_monitoring": True,
                "explainability_features": True,
                "adversarial_robustness_mechanisms": False
            },
            "LLM": {
                "uses_external_apis": True,
                "human_approval_required": "Mandatory",
                "fine_tuned_model": True,
                "real_time_execution": True,
                "data_drift_monitoring": True,
                "concept_drift_monitoring": False,
                "explainability_features": True,
                "adversarial_robustness_mechanisms": True
            },
            "Agent": {
                "uses_external_apis": True,
                "human_approval_required": "None",
                "fine_tuned_model": True,
                "real_time_execution": True,
                "data_drift_monitoring": True,
                "concept_drift_monitoring": True,
                "explainability_features": True,
                "adversarial_robustness_mechanisms": True,
                "autonomous_execution_loop": True,
                "tool_function_calling": True
            }
        }
    },
    {
        "name": "Customer Service Chatbot",
        "description": "Automated customer support via conversational AI.",
        "baseline_assumptions": ["Integration with CRM systems.", "Compliance with data retention policies."],
        "enterprise_constraints": ["High availability.", "Scalability for peak loads."],
        "architectural_options_defaults": {
            "ML": {
                "uses_external_apis": False,
                "human_approval_required": "Partial",
                "fine_tuned_model": False,
                "real_time_execution": True
            },
            "LLM": {
                "uses_external_apis": True,
                "human_approval_required": "Partial",
                "fine_tuned_model": True,
                "real_time_execution": True
            },
            "Agent": {
                "uses_external_apis": True,
                "human_approval_required": "Partial",
                "fine_tuned_model": True,
                "real_time_execution": True,
                "autonomous_execution_loop": False,
                "tool_function_calling": True
            }
        }
    }
]

# --- Mocking 'source' module globals and functions ---
# These mocks are critical for the AppTest to run without 'source.py' errors.
# In a real test environment, this would typically be handled by a pytest fixture
# or a similar test setup mechanism. The functions are mocked to return plausible
# data structures that the Streamlit app expects.

MOCK_SOURCE_GLOBALS = {
    "RISK_TAXONOMY": {
        "Data Privacy": {"description": "Risks related to unauthorized data access or leakage."},
        "Model Bias / Fairness": {"description": "Risks from biased model outputs."},
        "Security Vulnerabilities": {"description": "Risks from software flaws and attacks."},
        "Operational Resilience": {"description": "Risks from system failures or unavailability."},
        "Dependency / Vendor Risk": {"description": "Risks from third-party components or services."},
        "Regulatory / Compliance": {"description": "Risks from non-adherence to laws and regulations."}
    },
    "RISK_RULES": [], # Not directly tested, but needed for calculate_risk_scores mock to function
    "CONTROL_BASELINE_LIBRARY": {
        "Data Privacy": ["Control A", "Control B"],
        "Model Bias / Fairness": ["Control C"],
        "Security Vulnerabilities": ["Control D"],
        "Operational Resilience": ["Control E"],
        "Dependency / Vendor Risk": ["Control F"],
        "Regulatory / Compliance": ["Control G"]
    },
    "RISK_THRESHOLD": 5,
    "ARCHITECTURAL_FEATURES": [
        "uses_external_apis", "human_approval_required", "fine_tuned_model", "real_time_execution",
        "data_drift_monitoring", "concept_drift_monitoring", "explainability_features",
        "adversarial_robustness_mechanisms", "autonomous_execution_loop", "tool_function_calling"
    ]
}

# Mock functions for source.py
def mock_calculate_risk_scores(architectures_config, risk_taxonomy, risk_rules):
    # Return dummy dataframes that would typically be generated
    risk_categories = list(MOCK_SOURCE_GLOBALS['RISK_TAXONOMY'].keys())
    mock_normalized_df = pd.DataFrame({
        "Risk Category": risk_categories,
        "ML": [5, 4, 6, 7, 3, 5],
        "LLM": [7, 6, 8, 8, 6, 7],
        "Agent": [8, 7, 9, 9, 8, 9]
    }).set_index("Risk Category")
    mock_raw_df = pd.DataFrame({
        "Risk Category": risk_categories,
        "ML": [10, 8, 12, 14, 6, 10],
        "LLM": [14, 12, 16, 16, 12, 14],
        "Agent": [16, 14, 18, 18, 16, 18]
    }).set_index("Risk Category")
    return mock_normalized_df, mock_raw_df

def mock_identify_required_controls(normalized_risk_scores_df, control_baseline_library, risk_threshold):
    required_controls = {}
    for arch_type in normalized_risk_scores_df.columns:
        required_controls[arch_type] = ["Control A", "Control D"] # Example required controls
    return required_controls

def mock_perform_control_gap_analysis(required_controls_by_architecture, assumed_controls_omnicorp):
    control_gaps = {}
    for arch_type, required in required_controls_by_architecture.items():
        # Simulate some gaps, e.g., "Control D" is always missing
        control_gaps[arch_type] = [c for c in required if c == "Control D"]
    return control_gaps

def mock_load_use_case_template(file_path, use_case_name):
    for uc in DUMMY_USE_CASES_CONTENT:
        if uc['name'] == use_case_name:
            return uc
    return {} # Return empty dict if not found, to avoid error

def mock_plot_risk_radar_chart(normalized_risk_scores_df, risk_taxonomy):
    # Returns a dummy plotly figure
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[1,2,3], theta=['A','B','C'], fill='toself', name='Mock'))
    return fig

def mock_export_artifacts(*args, **kwargs):
    # Simulate a file being created for export
    dummy_zip_path = "mock_export.zip"
    if not os.path.exists("reports"):
        os.makedirs("reports")
    with open(os.path.join("reports", dummy_zip_path), 'w') as f:
        f.write("dummy zip content")
    return os.path.join("reports", dummy_zip_path)

@pytest.fixture(scope="module", autouse=True)
def setup_mock_environment():
    """
    Sets up a mocked environment for the Streamlit app.
    This fixture creates a temporary 'use_cases.json' and patches the 'source' module
    to provide mock implementations of its globals and functions.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Create a dummy use_cases.json file
        use_case_file_path = os.path.join(tmpdir, "use_cases.json")
        with open(use_case_file_path, "w") as f:
            json.dump(DUMMY_USE_CASES_CONTENT, f, indent=4)

        # 2. Create a mock `source` module
        mock_source = MagicMock()
        
        # Patch globals
        for key, value in MOCK_SOURCE_GLOBALS.items():
            setattr(mock_source, key, value)
        setattr(mock_source, "USE_CASE_FILE", use_case_file_path)

        # Patch functions
        mock_source.calculate_risk_scores.side_effect = mock_calculate_risk_scores
        mock_source.identify_required_controls.side_effect = mock_identify_required_controls
        mock_source.perform_control_gap_analysis.side_effect = mock_perform_control_gap_analysis
        mock_source.load_use_case_template.side_effect = mock_load_use_case_template
        mock_source.plot_risk_radar_chart.side_effect = mock_plot_risk_radar_chart
        mock_source.export_artifacts.side_effect = mock_export_artifacts

        # 3. Patch `sys.modules` to use our mock `source` module
        with patch.dict('sys.modules', {'source': mock_source}):
            yield # Run tests


def test_home_page_content():
    """Verifies the title and introductory text on the Home page."""
    at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "QuLab: Lab 2: AI Architecture Comparator"
    assert "OmniCorp Financial AI Architecture Risk Comparator" in at.markdown[0].value
    assert "Introduction: Architecting Secure and Compliant AI at OmniCorp Financial" in at.markdown[1].value


def test_use_case_page_initial_load():
    """Checks initial display of the 'Use Case & Configuration' page."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=1).run() # Navigate to page 1

    assert at.markdown[0].value == "# 1. Use Case & Architecture Configuration"
    assert "Selected Use Case: Fraud Detection Use Case" in at.subheader[1].value
    assert "Detecting financial fraud in real-time transactions." in at.markdown[2].value # Use case description


def test_use_case_selection():
    """Simulates selecting a different use case and loading it."""
    at = AppTest.from_file("app.py").run()
    
    # Change selected use case in sidebar
    at.sidebar.selectbox[0].set_value("Customer Service Chatbot").run()
    
    # Click "Load Use Case" button
    at.sidebar.button[0].click().run()

    # Navigate to the configuration page to verify changes
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=1).run()
    
    assert "Selected Use Case: Customer Service Chatbot" in at.subheader[1].value
    assert "Automated customer support via conversational AI." in at.markdown[2].value


def test_architectural_feature_toggles_ml_checkbox():
    """Verifies interaction with an ML architecture checkbox updates session state."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=1).run()

    # Find the checkbox for 'ML' architecture, 'uses_external_apis' (assuming it's the first checkbox for ML)
    # The order of checkboxes for each architecture corresponds to ARCHITECTURAL_FEATURES
    # uses_external_apis is the first in MOCK_ARCHITECTURAL_FEATURES
    ml_uses_external_apis_checkbox = at.checkbox[0] # First checkbox in the app is ML -> uses_external_apis
    assert ml_uses_external_apis_checkbox.label == "Uses External Apis"
    assert ml_uses_external_apis_checkbox.value is False # Default from DUMMY_USE_CASES_CONTENT

    ml_uses_external_apis_checkbox.check().run()
    assert ml_uses_external_apis_checkbox.value is True
    assert at.session_state['architectures_config']['ML']['uses_external_apis'] is True


def test_architectural_feature_toggles_llm_selectbox():
    """Verifies interaction with an LLM architecture selectbox updates session state."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=1).run()

    # Find the selectbox for 'LLM' architecture, 'human_approval_required'
    # Selectboxes are identified by their label or index. 'human_approval_required' is a selectbox.
    # The first selectbox (index 0) is for ML. The second (index 1) should be for LLM.
    llm_human_approval_selectbox = at.selectbox[1] 
    assert llm_human_approval_selectbox.label == "Human Approval Required:"
    assert llm_human_approval_selectbox.value == "Mandatory" # Default from DUMMY_USE_CASES_CONTENT

    llm_human_approval_selectbox.set_value("Partial").run()
    assert llm_human_approval_selectbox.value == "Partial"
    assert at.session_state['architectures_config']['LLM']['human_approval_required'] == "Partial"


def test_free_text_assumptions_update():
    """Checks if the free-text assumptions text area updates session state."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=1).run()

    new_assumption_text = "New test assumption for analysis."
    at.text_area[0].set_value(new_assumption_text).run()

    assert at.session_state['free_text_assumptions'] == new_assumption_text


def test_manual_recalculate_button():
    """Verifies clicking the recalculate button triggers calculations and shows success."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=1).run()

    at.button[0].click().run() # Click "Recalculate Risk & Controls (Manual Trigger)"
    
    assert at.success[0].value == "Risk scores and controls recalculated!"
    assert not at.session_state['normalized_risk_scores_df'].empty
    assert not at.session_state['required_controls_by_architecture'] == {}


def test_risk_comparison_page_content():
    """Verifies the content of the 'Risk & Control Comparison' page."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=2).run() # Navigate to page 2

    assert at.markdown[0].value == "# 2. Architectural Risk & Control Comparison"
    assert "Normalized Risk Scores (0-10 per category):" in at.subheader[1].value
    assert not at.dataframe[0].empty # Check if dataframe is rendered and not empty

    assert "Comprehensive Control Gap Checklist (Risk Threshold >= 5)" in at.subheader[2].value
    assert "ML Architecture Controls" in at.markdown[4].value
    assert "❌ MISSING (GAP)" in at.markdown[6].value # Expecting Control D to be a gap from mock

    # The radar chart is a plotly_chart component, AppTest asserts its presence
    assert at.plotly_chart[0] is not None


def test_export_artifacts_page_and_download():
    """Verifies the 'Export Artifacts' page content and triggers export."""
    at = AppTest.from_file("app.py").run()
    at.sidebar.radio(options=["Home", "1. Use Case & Configuration", "2. Risk & Control Comparison", "3. Export Artifacts"], index=3).run() # Navigate to page 3

    assert at.markdown[0].value == "# 3. Generating an Executive-Ready Comparison Artifact"
    assert "Export Summary for Fraud Detection Use Case" in at.markdown[1].value

    at.button[0].click().run() # Click "Generate Export & Download Package"

    assert at.success[0].value.startswith("Export package generated successfully. ID:")
    assert at.download_button[0].label == "Download Export Package (.zip)"
    assert at.session_state['export_zip_filepath'].endswith("export.zip")
    assert os.path.exists(at.session_state['export_zip_filepath'])

