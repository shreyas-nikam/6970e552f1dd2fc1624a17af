id: 6970e552f1dd2fc1624a17af_user_guide
summary: Lab 2: AI Architecture Comparator User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Lab 2: AI Architecture Comparator User Guide

## 1. Welcome to the AI Architecture Risk Comparator
Duration: 0:05:00

<aside class="positive">
This introductory step sets the stage for understanding the purpose and capabilities of the AI Architecture Risk Comparator. It explains the core problem it solves and what you, as a user, will learn to achieve.
</aside>

Dr. Ava Sharma, a key Enterprise AI Architect at OmniCorp Financial, is tasked with evaluating different AI architectural approaches for critical systems like real-time fraud detection. Teams propose various solutions: traditional Machine Learning (ML), Large Language Model (LLM)-based, and advanced Agentic systems. Each option comes with unique advantages, but also introduces distinct risk profiles and demands specific control measures.

The **AI Architecture Risk Comparator** application simulates Dr. Sharma's workflow. It allows you to:
1.  **Decompose AI systems** into key architectural features that influence risk.
2.  **Compare** how different designs (ML, LLM, Agent) alter the risk landscape.
3.  **Quantify architectural risk** using a set of predefined, deterministic rules.
4.  **Identify essential control requirements** for each architecture and highlight any missing controls (gaps).
5.  **Generate an executive-ready comparison artifact** to support informed strategic decisions.

This tool helps make architectural risks visible, comparable, and defensible, ensuring that OmniCorp develops innovative AI systems that are also secure and compliant.



### Understanding the Navigation

On the left sidebar, you'll find the main navigation elements:

*   **Navigation:** This section allows you to move between the main sections of the application:
    *   **Home:** The current introductory page.
    *   **1. Use Case & Configuration:** Where you select and customize architectural designs.
    *   **2. Risk & Control Comparison:** Where you analyze the quantified risks and control gaps.
    *   **3. Export Artifacts:** Where you generate and download a comprehensive report.
*   **Select Use Case:** Here, you can choose from a list of pre-defined use case templates. Each template provides a unique scenario and default architectural configurations to start your analysis.

<aside class="positive">
<b>Tip:</b> Always start by selecting the appropriate use case from the sidebar. This loads the foundational context for your analysis.
</aside>

## 2. Load a Use Case & Configure Architectures
Duration: 0:10:00

In this step, you'll learn how to load a specific use case and then configure the architectural features for different AI system types. These configurations are crucial as they directly impact the risk assessment.

### Selecting a Use Case

1.  On the left sidebar, locate the "Select Use Case" section.
2.  From the "Choose a Use Case Template:" dropdown, select a use case. For this guide, let's select "OmniCorp Fraud Detection".
3.  Click the "Load Use Case" button directly below the dropdown.

<aside class="console">
**Sidebar:**
Select Use Case
Choose a Use Case Template:
[Dropdown with "OmniCorp Fraud Detection" selected]
Load Use Case [Button]
</aside>

Once loaded, the main panel will update to show details about the selected use case, including its description, baseline assumptions, and enterprise constraints. This provides the foundational context for your analysis, ensuring all architectural comparisons are consistent and relevant to OmniCorp's operational environment.

### Configuring Architectural Features

After loading a use case, scroll down on the "1. Use Case & Configuration" page to the "Configuring Architectures" section. Here, you'll see three columns: "ML Architecture", "LLM Architecture", and "Agent Architecture". Each column represents a different AI system type you can configure.

These sections allow you to enable or disable specific architectural features for each AI type. These features are the core design choices that influence the system's risk profile.

For example, an Agentic system for fraud detection might inherently require an "Autonomous execution loop" or "Tool/function calling" to interact with mitigation systems, whereas a traditional ML system typically would not.

**How to Configure:**

*   **Toggles (Checkboxes):** For features like "Autonomous execution loop" or "Uses external APIs", simply check the box to enable the feature or uncheck it to disable it.
    <aside class="console">
    [ ] Autonomous execution loop
    [X] Uses external APIs
    </aside>
*   **Dropdowns (Selectboxes):** For features like "Human approval required", you'll select an option from a dropdown list (e.g., "None", "Partial", "Mandatory").
    <aside class="console">
    Human approval required:
    [None v]
    </aside>

<aside class="positive">
<b>Tip:</b> As you change a feature, the application automatically recalculates the risks and controls in the background. You don't need to manually save your changes for each toggle.
</aside>

Experiment with enabling and disabling various features for each architecture type. Notice how different choices might make an architecture more or less complex, and implicitly, more or less risky.

### Adding Free-Text Assumptions

At the bottom of the "1. Use Case & Configuration" page, you'll find an "Additional Assumptions" text area.

<aside class="console">
Free-Text Assumptions for this Session:
[Text area pre-filled with "This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date..."]
</aside>

This is where you can add any specific assumptions or contextual notes relevant to your current analysis session. These notes will be captured and included in the final exported report, providing valuable context for stakeholders reviewing your analysis.

<aside class="positive">
<b>Best Practice:</b> Use the free-text assumptions to document anything unique about your current analysis that isn't covered by the configurable features. This ensures your report is comprehensive and transparent.
</aside>

## 3. Analyze Risk Scores and Control Gaps
Duration: 0:15:00

Now that you've configured your architectural options, it's time to quantify their risks and identify necessary controls. Navigate to the "2. Risk & Control Comparison" page using the sidebar.

<aside class="console">
**Sidebar Navigation:**
Go to
[ ] Home
[ ] 1. Use Case & Configuration
[X] 2. Risk & Control Comparison
[ ] 3. Export Artifacts
</aside>

### Quantifying Architectural Risk

The application uses OmniCorp's standardized, rule-based risk scoring methodology. Each enabled architectural feature you configured contributes a predefined score to one or more risk categories (e.g., enabling `uses_external_apis` increases `Dependency / Vendor Risk`).

The risk score for a given category for an architecture, $R_{arch, cat}$, is calculated as the sum of all risk contributions from its enabled features, $C_{feature, cat}$, and then normalized:

$$ R_{arch, cat} = \text{normalize}\left(\sum_{feature \in Features_{arch}} C_{feature, cat}\right) $$

where $Features_{arch}$ is the set of enabled features for a specific architecture, and $C_{feature, cat}$ is the risk contribution of a feature to a specific risk category.

You'll see a table titled "**Normalized Risk Scores (0-10 per category):**"

<aside class="console">
Normalized Risk Scores (0-10 per category):
| Risk Category              | ML   | LLM  | Agent |
|-|||-|
| Data Privacy / Confidentiality | 3.5  | 6.0  | 6.0   |
| Security Vulnerabilities   | 4.0  | 5.5  | 7.0   |
| ...                        | ...  | ...  | ...   |
</aside>

Each row represents a risk category (e.g., Data Privacy / Confidentiality, Security Vulnerabilities), and each column represents one of your configured architectures (ML, LLM, Agent). The values range from 0 (lowest risk) to 10 (highest risk) and indicate the quantified risk level for that architecture in that specific category based on your feature selections.

<aside class="positive">
<b>Tip:</b> Higher scores indicate higher risk. This table allows you to quickly compare the risk exposure of each architecture across different categories.
</aside>

### Identifying Control Baselines and Gap Analysis

After quantifying risks, the application automatically determines what security controls are *required* for each architecture based on its risk profile and OmniCorp's control library. It then performs a "gap analysis" by comparing these required controls against a set of already assumed controls at OmniCorp.

The control baseline mapping is: Risk category $\rightarrow$ Minimum required controls. A control gap is identified if a required control is not present in the set of `assumed_controls`.

You'll see a section titled "**Comprehensive Control Gap Checklist**". This checklist provides a detailed breakdown for each architecture:

<aside class="console">
### ML Architecture Controls
#### Required Controls:
- Access control lists (ACLs) ✅ Present (or assumed)
- Data encryption (at rest/in transit) ✅ Present (or assumed)
- Input validation ❌ MISSING (GAP)
- Secure coding practices ✅ Present (or assumed)
</aside>

For each architecture:
*   **Required Controls:** This lists all controls identified as necessary due to the architecture's risk profile.
*   **Status (✅ Present / ❌ MISSING (GAP)):** This indicates whether the required control is already covered by OmniCorp's assumed baseline controls or if there is a gap that needs to be addressed.

<aside class="negative">
<b>Warning:</b> Any control marked with "❌ MISSING (GAP)" represents a critical area that needs attention. These are the non-negotiable controls that must be implemented or addressed for the chosen architecture.
</aside>

### Visualizing Risk Profiles

To make the comparison even clearer, the application generates a radar chart. This visual representation helps Dr. Sharma communicate her findings effectively to the AI Architecture Review Board.

Scroll to the bottom of the "2. Risk & Control Comparison" page to see the **Risk Radar Chart**.

<aside class="console">
[A radar chart will be displayed here, showing a polygon for ML, LLM, and Agent architectures, with each axis representing a risk category and the extent of the polygon indicating the normalized risk score for that category.]
</aside>

*   Each axis of the radar chart represents a specific **risk category** (e.g., Data Privacy, Security Vulnerabilities).
*   The **points along each axis** correspond to the normalized risk score (0-10).
*   Each **colored line (or 'web')** represents one of the architectural options (ML, LLM, Agent).

The larger the area covered by an architecture's web, the higher its overall risk profile. This visualization makes it easy to spot which architectures have higher risks in certain categories compared to others, facilitating discussions on risk trade-offs and resource allocation.

<aside class="positive">
<b>Tip:</b> Use the radar chart to quickly identify the "spiky" areas for an architecture – these are the risk categories where it performs worst compared to others, indicating potential hot spots for mitigation efforts.
</aside>

## 4. Generate and Export Analysis Artifacts
Duration: 0:05:00

The final and crucial step is to compile all your analysis into a comprehensive, executive-ready comparison artifact. Navigate to the "3. Export Artifacts" page using the sidebar.

<aside class="console">
**Sidebar Navigation:**
Go to
[ ] Home
[ ] 1. Use Case & Configuration
[ ] 2. Risk & Control Comparison
[X] 3. Export Artifacts
</aside>

### Understanding the Export Package

This page provides a summary of all the artifacts that will be generated and bundled into a single ZIP file. This package is the primary deliverable for stakeholders like the AI Architecture Review Board and Risk/Security Partners. It provides a standardized record and auditable evidence of your analysis.

The export package includes:

*   `architecture_config.json`: A snapshot of all the architectural features you configured for ML, LLM, and Agent systems.
*   `risk_scores_by_architecture.json`: Detailed raw and normalized risk scores for all categories and architectures.
*   `control_gaps_checklist.json`: A list of all identified control gaps for each architecture.
*   `session02_executive_summary.md`: A markdown-formatted executive summary of your analysis, providing high-level insights.
*   `config_snapshot.json`: All global definitions (risk taxonomy, rules, control baseline library) used for this specific analysis session. This ensures reproducibility and transparency.
*   `evidence_manifest.json`: Contains SHA-256 hashes of all generated artifacts. This is critical for ensuring the integrity and non-repudiation of the analysis, especially in regulated financial environments.

### Generating and Downloading the Package

1.  Click the "Generate Export & Download Package" button.
    <aside class="console">
    [Generate Export & Download Package]
    </aside>
2.  The application will process the data and generate the ZIP file. You'll see a success message with a unique run ID (e.g., "Export package generated successfully. ID: 20231027_103045").
3.  Once the package is ready, a "Download Export Package (.zip)" button will appear. Click this button to download the ZIP file to your local machine.

<aside class="console">
Export package generated successfully. ID: 20231027_103045
[Download Export Package (.zip)]
</aside>

Congratulations! You have successfully used the AI Architecture Risk Comparator to evaluate different AI architectural options, quantify their risks, identify control gaps, and generate a comprehensive executive-ready report. This process empowers informed decision-making for deploying secure and compliant AI systems at OmniCorp Financial.
