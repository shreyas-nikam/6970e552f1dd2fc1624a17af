# Executive Summary: AI Architecture Risk Assessment for Customer Support Automation

**Date of Analysis:** 2026-01-21 11:28:28
**Primary Analyst:** Dr. Ava Sharma (Enterprise AI Architect, OmniCorp Financial)
**Objective:** This report compares the architectural risk profiles of proposed ML, LLM, and Agentic systems for **Customer Support Automation** to facilitate informed decision-making by the AI Architecture Review Board.

## Key Findings:
1.  **ML Architecture:** Generally exhibits lower inherent risk, particularly in 'Runtime Autonomy Risk' and 'Dependency / Vendor Risk', due to less reliance on external APIs and autonomous loops. However, 'Model Risk' remains a key concern.
2.  **LLM Architecture:** Introduces elevated risks in 'Data Risk' (due to RAG/vector stores), 'Dependency / Vendor Risk' (external APIs), and 'Model Risk' (fine-tuning complexity). Benefits from robust NLU but requires careful data governance.
3.  **Agentic Architecture:** Presents the highest 'Runtime Autonomy Risk' and 'Security Risk' due to autonomous execution and tool-calling capabilities. While offering significant automation potential, it mandates the most stringent control requirements.

## Risk Profile Summary (Normalized 0-10):
       Data Risk  Model Risk  Security Risk  Operational Risk  Transparency / Explainability Risk  Dependency / Vendor Risk  Runtime Autonomy Risk
ML           0.0         0.0            0.0               0.0                                 0.0                       0.0                    0.0
LLM         10.0         0.0            4.0               0.0                                 5.0                      10.0                    0.0
Agent       10.0         0.0           10.0              10.0                                10.0                      10.0                   10.0

*Note: 'tabulate' library not found. Table formatted using .to_string(). Install 'tabulate' for better markdown formatting.*


*See `risk_scores_by_architecture.json` for detailed scores.*

## Control Gap Analysis:
Based on OmniCorp's control baseline library and a risk threshold of 5 (normalized score), the following control gaps were identified when comparing against assumed enterprise controls:

### ML Architecture Gaps:
- No critical control gaps identified beyond assumed enterprise controls.
### LLM Architecture Gaps:
- ❌ **Audit trails of decisions**
- ❌ **Data anonymization/pseudonymization**
- ❌ **Data retention policies**
- ❌ **Fallback strategy for external APIs**
- ❌ **Third-party risk assessment**
- ❌ **User communication of AI use**
- ❌ **XAI framework implementation**
### Agent Architecture Gaps:
- ❌ **Approval gates for critical actions**
- ❌ **Audit trails of decisions**
- ❌ **Business continuity plan**
- ❌ **Data anonymization/pseudonymization**
- ❌ **Data retention policies**
- ❌ **Disaster recovery plan**
- ❌ **Fallback strategy for external APIs**
- ❌ **Intrusion detection systems**
- ❌ **Kill switch functionality**
- ❌ **Least privilege access**
- ❌ **Monitoring & alerting**
- ❌ **Step limits on actions**
- ❌ **Third-party risk assessment**
- ❌ **User communication of AI use**
- ❌ **XAI framework implementation**

*See `control_gaps_checklist.json` for a full list.*

## Recommendations:
1.  For highly autonomous systems (e.g., Agentic), prioritize implementation of 'Kill switch functionality' and 'Approval gates for critical actions'.
2.  For LLM-based systems, strengthen 'Data anonymization/pseudonymization' and 'Vendor SLA review' processes.
3.  Ensure continuous model validation and explainability frameworks are in place for all architectures, especially given the 'Model Risk'.

## Assumptions and Context:
**Use Case:** Customer Support Automation
**Use Case Description:** Automating responses to common customer queries and routing complex cases.
**Baseline Assumptions:** High accuracy in intent recognition, Scalability for peak loads
**Enterprise Constraints:** Brand voice consistency, Data privacy
**Assumed Enterprise Controls:** Access control lists (ACLs), Comprehensive audit logs, Data encryption (at rest/in transit), Incident response plan, Secure coding practices, Vendor SLA review, Vulnerability scanning
**Additional Free-Text Assumptions:** This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date.

---