# Executive Summary: AI Architecture Risk Assessment for Clinical / Operations Triage

**Date of Analysis:** 2026-01-21 11:14:47
**Primary Analyst:** Dr. Ava Sharma (Enterprise AI Architect, OmniCorp Financial)
**Objective:** This report compares the architectural risk profiles of proposed ML, LLM, and Agentic systems for **Clinical / Operations Triage** to facilitate informed decision-making by the AI Architecture Review Board.

## Key Findings:
1.  **ML Architecture:** Generally exhibits lower inherent risk, particularly in 'Runtime Autonomy Risk' and 'Dependency / Vendor Risk', due to less reliance on external APIs and autonomous loops. However, 'Model Risk' remains a key concern.
2.  **LLM Architecture:** Introduces elevated risks in 'Data Risk' (due to RAG/vector stores), 'Dependency / Vendor Risk' (external APIs), and 'Model Risk' (fine-tuning complexity). Benefits from robust NLU but requires careful data governance.
3.  **Agentic Architecture:** Presents the highest 'Runtime Autonomy Risk' and 'Security Risk' due to autonomous execution and tool-calling capabilities. While offering significant automation potential, it mandates the most stringent control requirements.

## Risk Profile Summary (Normalized 0-10):
           Data Risk  Model Risk  Security Risk  Operational Risk  Transparency / Explainability Risk  Dependency / Vendor Risk  Runtime Autonomy Risk
ML               0.0         0.0            0.0              0.00                                0.00                       0.0                    0.0
LLM             10.0        10.0            4.0              1.67                                6.67                      10.0                    0.0
Agent           10.0        10.0           10.0             10.00                               10.00                      10.0                   10.0
Custom ML        0.0         0.0            8.0              8.33                                3.33                      10.0                   10.0

*Note: 'tabulate' library not found. Table formatted using .to_string(). Install 'tabulate' for better markdown formatting.*


*See `risk_scores_by_architecture.json` for detailed scores.*

## Control Gap Analysis:
Based on OmniCorp's control baseline library and a risk threshold of 5 (normalized score), the following control gaps were identified when comparing against assumed enterprise controls:

### ML Architecture Gaps:
- No critical control gaps identified beyond assumed enterprise controls.
### LLM Architecture Gaps:
- ❌ **Audit trails of decisions**
- ❌ **Change control for models**
- ❌ **Data anonymization/pseudonymization**
- ❌ **Data retention policies**
- ❌ **Fallback strategy for external APIs**
- ❌ **Model documentation (RID)**
- ❌ **Model validation (drift/bias)**
- ❌ **Regular model retraining**
- ❌ **Third-party risk assessment**
- ❌ **User communication of AI use**
- ❌ **XAI framework implementation**
### Agent Architecture Gaps:
- ❌ **Approval gates for critical actions**
- ❌ **Audit trails of decisions**
- ❌ **Business continuity plan**
- ❌ **Change control for models**
- ❌ **Data anonymization/pseudonymization**
- ❌ **Data retention policies**
- ❌ **Disaster recovery plan**
- ❌ **Fallback strategy for external APIs**
- ❌ **Intrusion detection systems**
- ❌ **Kill switch functionality**
- ❌ **Least privilege access**
- ❌ **Model documentation (RID)**
- ❌ **Model validation (drift/bias)**
- ❌ **Monitoring & alerting**
- ❌ **Regular model retraining**
- ❌ **Step limits on actions**
- ❌ **Third-party risk assessment**
- ❌ **User communication of AI use**
- ❌ **XAI framework implementation**
### Custom ML Architecture Gaps:
- ❌ **Approval gates for critical actions**
- ❌ **Business continuity plan**
- ❌ **Comprehensive audit logs**
- ❌ **Disaster recovery plan**
- ❌ **Fallback strategy for external APIs**
- ❌ **Incident response plan**
- ❌ **Intrusion detection systems**
- ❌ **Kill switch functionality**
- ❌ **Least privilege access**
- ❌ **Monitoring & alerting**
- ❌ **Secure coding practices**
- ❌ **Step limits on actions**
- ❌ **Third-party risk assessment**
- ❌ **Vendor SLA review**
- ❌ **Vulnerability scanning**

*See `control_gaps_checklist.json` for a full list.*

## Recommendations:
1.  For highly autonomous systems (e.g., Agentic), prioritize implementation of 'Kill switch functionality' and 'Approval gates for critical actions'.
2.  For LLM-based systems, strengthen 'Data anonymization/pseudonymization' and 'Vendor SLA review' processes.
3.  Ensure continuous model validation and explainability frameworks are in place for all architectures, especially given the 'Model Risk'.

## Assumptions and Context:
**Use Case:** Clinical / Operations Triage
**Use Case Description:** AI-assisted triage and prioritization of clinical operations and patient care workflows.
**Baseline Assumptions:** High accuracy in risk assessment is critical for patient safety., Integration with Electronic Health Records (EHR) systems is required., Compliance with HIPAA and other healthcare regulations is mandatory., Real-time decision support for clinical staff.
**Enterprise Constraints:** Strict regulatory compliance (HIPAA, FDA guidelines for medical AI)., Patient safety is paramount - errors can have life-threatening consequences., Data privacy and security for Protected Health Information (PHI)., Liability and malpractice considerations., Need for clinician oversight and final decision authority.
**Assumed Enterprise Controls:** Access control lists (ACLs), Comprehensive audit logs, Data encryption (at rest/in transit), Incident response plan, Secure coding practices, Vendor SLA review, Vulnerability scanning
**Additional Free-Text Assumptions:** This analysis assumes OmniCorp's existing enterprise security controls are effective and up-to-date. The risk threshold for mandatory controls (5/10) reflects a moderate risk appetite for new AI initiatives.

---