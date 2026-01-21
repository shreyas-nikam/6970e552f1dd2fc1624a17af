# QuLab: Lab 2: AI Architecture Comparator

## AI Architecture Risk & Control Evaluation for OmniCorp Financial

![QuantUniversity Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

This Streamlit application, "QuLab: Lab 2: AI Architecture Comparator," provides a comprehensive tool for evaluating and comparing the risk profiles and control requirements of different AI architectural approaches (traditional Machine Learning, Large Language Models, and Agentic Systems). Developed for OmniCorp Financial, it assists AI Architects like Dr. Ava Sharma in making informed decisions by quantifying architectural risks, identifying control gaps, and generating executive-ready comparison artifacts for the AI Architecture Review Board.

The application simulates a real-world scenario where an enterprise architect needs to compare diverse AI architectures for a critical financial application (e.g., real-time fraud detection), ensuring both innovation and stringent security/compliance standards are met.

## Table of Contents

- [QuLab: Lab 2: AI Architecture Comparator](#qulab-lab-2-ai-architecture-comparator)
  - [AI Architecture Risk & Control Evaluation for OmniCorp Financial](#ai-architecture-risk--control-evaluation-for-omnicorp-financial)
  - [Table of Contents](#table-of-contents)
  - [1. Project Description](#1-project-description)
  - [2. Features](#2-features)
  - [3. Getting Started](#3-getting-started)
    - [3.1. Prerequisites](#31-prerequisites)
    - [3.2. Installation](#32-installation)
  - [4. Usage](#4-usage)
  - [5. Project Structure](#5-project-structure)
  - [6. Technology Stack](#6-technology-stack)
  - [7. Contributing](#7-contributing)
  - [8. License](#8-license)
  - [9. Contact](#9-contact)

## 1. Project Description

In today's fast-evolving financial landscape, deploying AI systems responsibly is paramount. OmniCorp Financial aims to enhance its real-time fraud detection capabilities using advanced AI. This project addresses the challenge faced by enterprise AI architects in evaluating the unique risk surfaces and control requirements of different AI paradigms:
*   **Traditional Machine Learning (ML)**
*   **Large Language Model (LLM)-based Systems**
*   **Advanced Agentic Systems**

The "AI Architecture Comparator" enables architects to systematically decompose AI systems, apply a standardized risk taxonomy, quantify architectural risks using deterministic rules, and identify control gaps against an assumed baseline. The ultimate goal is to produce transparent, comparable, and defensible risk assessments that inform strategic decisions and ensure compliance before significant investment.

**Learning Objectives:**
By using this application, users will be able to:
1.  Decompose AI systems into architectural features that materially affect risk.
2.  Compare how ML, LLM, and agentic designs change risk surfaces.
3.  Quantify architectural risk using deterministic rules.
4.  Identify non-negotiable control expectations per architecture.
5.  Produce an executive-ready comparison artifact suitable for design review.

## 2. Features

*   **Use Case Management**: Load pre-defined use case templates (`.json` files) that set baseline assumptions and enterprise constraints relevant to specific AI initiatives (e.g., "Real-time Fraud Detection").
*   **Configurable Architectural Features**: Dynamically enable or disable various architectural features (e.g., `human_approval_required`, `fine_tuned_model`, `real_time_execution`, `uses_external_apis`, `autonomous_execution_loop`, `tool_function_calling`) for ML, LLM, and Agent architectures. Changes trigger immediate recalculations.
*   **Deterministic Risk Scoring**: Automatically calculate raw and normalized risk scores (0-10) for each architecture across predefined risk categories (e.g., `Operational Risk`, `Model Risk`, `Privacy Risk`) based on the enabled features and a rule-based risk taxonomy.
*   **Control Baseline Identification**: Identify mandatory controls required for each architecture given its risk profile and OmniCorp's control baseline library.
*   **Control Gap Analysis**: Perform a gap analysis by comparing the identified required controls against a set of assumed existing enterprise controls, highlighting missing controls.
*   **Interactive Risk Visualization**: Display risk profiles using interactive radar charts (Plotly) for an intuitive visual comparison of different architectures across various risk dimensions.
*   **Artifact Export**: Generate a comprehensive ZIP package containing:
    *   Configuration snapshots (`architecture_config.json`)
    *   Detailed raw and normalized risk scores (`risk_scores_by_architecture.json`)
    *   Control gap checklists (`control_gaps_checklist.json`)
    *   A markdown-formatted executive summary (`session02_executive_summary.md`)
    *   A snapshot of all global definitions (risk taxonomy, rules, controls) used for the analysis (`config_snapshot.json`)
    *   An `evidence_manifest.json` with SHA-256 hashes of all generated artifacts to ensure integrity and non-repudiation.
*   **Session State Management**: Maintains user selections and calculations across different navigation pages.

## 3. Getting Started

Follow these instructions to get the application up and running on your local machine.

### 3.1. Prerequisites

*   **Python 3.8+**: Ensure you have a compatible version of Python installed.

### 3.2. Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/qu-lab-ai-architecture-comparator.git
    cd qu-lab-ai-architecture-comparator
    ```
    *(Replace `your-username/qu-lab-ai-architecture-comparator` with the actual repository path)*

2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(A `requirements.txt` file should include at least `streamlit`, `pandas`, `plotly`, `numpy`.)*
    Example `requirements.txt`:
    ```
    streamlit>=1.30.0
    pandas>=2.0.0
    plotly>=5.10.0
    numpy>=1.24.0
    ```

4.  **Ensure data files are present**:
    Make sure the `data` directory exists and contains `use_cases.json` as specified by `USE_CASE_FILE` in `source.py`. This file contains the pre-defined use case templates.
    A basic `data/use_cases.json` might look like:
    ```json
    [
      {
        "name": "Real-time Fraud Detection",
        "description": "Evaluate AI architectures for identifying financial fraud in real-time transactions.",
        "baseline_assumptions": [
          "High transaction volume (millions/sec)",
          "Low latency requirements (<100ms)",
          "Sensitive customer data involved"
        ],
        "enterprise_constraints": [
          "Regulatory compliance (e.g., GDPR, CCPA)",
          "Data residency restrictions",
          "Integration with existing payment gateways"
        ],
        "architectural_options_defaults": {
          "ML": {
            "uses_external_apis": false,
            "fine_tuned_model": true,
            "real_time_execution": true,
            "human_approval_required": "Partial",
            "autonomous_execution_loop": false,
            "tool_function_calling": false,
            "sensitive_data_handling": true,
            "feedback_loop": true
          },
          "LLM": {
            "uses_external_apis": true,
            "fine_tuned_model": false,
            "real_time_execution": true,
            "human_approval_required": "Mandatory",
            "autonomous_execution_loop": false,
            "tool_function_calling": true,
            "sensitive_data_handling": true,
            "feedback_loop": true
          },
          "Agent": {
            "uses_external_apis": true,
            "fine_tuned_model": false,
            "real_time_execution": true,
            "human_approval_required": "Partial",
            "autonomous_execution_loop": true,
            "tool_function_calling": true,
            "sensitive_data_handling": true,
            "feedback_loop": true
          }
        }
      }
    ]
    ```

## 4. Usage

To run the Streamlit application:

1.  **Activate your virtual environment** (if you created one):
    ```bash
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Start the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser.

**Basic Usage Instructions**:

1.  **Navigate**: Use the sidebar radio buttons to switch between "Home," "1. Use Case & Configuration," "2. Risk & Control Comparison," and "3. Export Artifacts."
2.  **Select Use Case**: On the sidebar, choose a use case from the dropdown and click "Load Use Case" to populate the initial configurations.
3.  **Configure Architectures**: On the "1. Use Case & Configuration" page, adjust the toggles and select boxes for ML, LLM, and Agent architectures based on your hypothetical design choices. Changes automatically trigger recalculations of risk scores.
4.  **Review Risk & Controls**: Go to the "2. Risk & Control Comparison" page to view the normalized risk scores, detailed control gap analysis, and the interactive radar chart comparing the risk profiles.
5.  **Export Artifacts**: On the "3. Export Artifacts" page, click "Generate Export & Download Package" to create a ZIP file containing all the analysis results, including a markdown executive summary and an evidence manifest.

## 5. Project Structure

```
.
├── app.py                     # Main Streamlit application file
├── source.py                  # Contains helper functions, risk taxonomy, rules, and control logic
├── data/                      # Directory for data files
│   └── use_cases.json         # Pre-defined use case templates
├── reports/                   # Output directory for generated artifacts (created dynamically)
├── venv/                      # Python virtual environment (if created)
├── requirements.txt           # List of Python dependencies
└── README.md                  # This README file
```

## 6. Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: For building the interactive web application interface.
*   **Pandas**: For data manipulation and tabular data handling.
*   **Plotly**: For creating interactive data visualizations (e.g., radar charts).
*   **JSON**: For structured data storage (use cases, configurations, outputs).
*   **`os` and `datetime`**: Standard Python libraries for file system operations and timestamping.

## 7. Contributing

This project is primarily a lab exercise. However, if you have suggestions for improvements or encounter issues, please feel free to open an issue in the GitHub repository.

## 8. License

This project is licensed under the MIT License - see the `LICENSE` file for details.
*(A `LICENSE` file should be added to the project root with the MIT license text.)*

## 9. Contact

For questions or feedback, please contact:

*   **QuantUniversity Team**
*   **Website**: [www.quantuniversity.com](https://www.quantuniversity.com)
*   **GitHub**: [https://github.com/QuantUniversity](https://github.com/QuantUniversity) *(Replace with the specific repo if available)*