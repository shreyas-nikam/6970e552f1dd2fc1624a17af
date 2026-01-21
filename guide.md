# Lab Guide: AI Architecture Risk Comparator

## Case Context

OmniCorp Financial, a mid-sized regional bank, is under pressure to modernize its fraud detection system after experiencing a 40% increase in sophisticated fraud attempts. The Board has allocated $2M for an AI-driven solution, but three competing teams have proposed different architectures: traditional Machine Learning, LLM-based analysis, and autonomous Agentic systems. Each promises faster detection but introduces unknown security and compliance risks.

The AI Architecture Review Board—comprising the CTO, Chief Risk Officer, and Head of Compliance—must make a decision within two weeks. They need a quantifiable, auditable risk comparison that balances innovation with regulatory obligations under banking regulations. A wrong choice could mean regulatory fines, security breaches, or a system that fails to meet operational requirements.

## Your Role

You are a Junior Enterprise AI Architect supporting Dr. Ava Sharma in preparing the risk assessment for the Board. Dr. Sharma has tasked you with using OmniCorp's standardized AI Risk Comparator tool to evaluate the three architectural proposals for the fraud detection use case. Your analysis will directly inform a $2M investment decision and shape OmniCorp's AI strategy for the next three years.

Your deliverable is an executive-ready comparison report that quantifies risks across architectures, identifies control gaps, and provides visual comparisons. The Board expects objectivity, transparency, and compliance-ready documentation—not a recommendation, but clear risk visibility to support their decision-making process.

## What You Will Do

- Load the fraud detection use case and configure architectural features for ML, LLM, and Agent designs
- Compare quantified risk scores across security, compliance, and operational risk categories
- Identify required security controls and gaps for each architecture
- Generate visualizations and export an auditable analysis package for Board review

## Step-by-Step Instructions

1. **Launch the Application**
   - Open the Streamlit app and review the Home page scenario

2. **Configure Use Case & Architectures**
   - Navigate to "1. Use Case & Configuration"
   - a. Select "Real-time Fraud Detection" from the use case dropdown
   - b. Load the configuration by clicking "Load This Use Case Configuration"
   - c. Review the three architecture columns (ML, LLM, Agent)
   - d. Toggle architectural features for each design (e.g., enable "external APIs" for LLM, "autonomous execution" for Agent)
   - e. Click "Recalculate Risk & Controls" to update scores

3. **Analyze Risk & Control Gaps**
   - Navigate to "2. Risk & Control Comparison"
   - a. Review the normalized risk scores table (0-10 scale)
   - b. Examine the interactive radar chart showing risk profiles
   - c. Scroll to the control gap checklist
   - d. Check boxes for controls OmniCorp already has in place
   - e. Note remaining gaps for each architecture

4. **Export Analysis Package**
   - Navigate to "3. Export Artifacts"
   - a. Click "Generate Export & Download Package"
   - b. Download the ZIP file containing risk scores, control gaps, and executive summary
   - c. Review the exported markdown summary

## What This Lab Is Really Teaching

- How architectural choices directly impact organizational risk across multiple dimensions
- The importance of deterministic, rule-based risk quantification for defensible decision-making
- Gap analysis techniques for identifying missing security controls before system deployment
- Creating auditable, executive-ready documentation for high-stakes technology decisions
- Balancing innovation velocity with risk management in regulated environments

## Discussion

- If the Agent architecture has the highest risk score but promises 60% faster fraud detection, what factors should the Board weigh in their decision?
- Why is it critical to identify control gaps *before* building rather than during security audits after deployment?
- How might this risk comparison methodology apply to other AI use cases like loan underwriting or customer service chatbots?

## Takeaway

Effective AI architecture decisions require transparent risk quantification, not just technical capability comparisons. This methodology transforms subjective debates into objective, auditable risk assessments that build stakeholder confidence.
