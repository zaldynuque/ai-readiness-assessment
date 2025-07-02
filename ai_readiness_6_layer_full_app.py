
import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import openai
import time

st.set_page_config(page_title="AI Readiness Assessment", layout="wide")
st.title("🧠 AI Readiness Assessment (6-Layer) Framework")
st.markdown("Evaluate your AI maturity across six critical dimensions: Infrastructure, Orchestration, Knowledge, Model, Agent, and Governance.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

responses = {}
pillar_averages = {}
maturity_scale = {0: "Not Started", 1: "Pilot", 2: "Operational", 3: "Industrialized", 4: "Optimized"}

questions = {
    "1. Infrastructure Layer": [
        "Do you use a modern GPU stack (e.g., Hopper, Blackwell, Quantum2, Spectrum-X, DOX) for AI workloads?",
        "Do you utilize a flexible and scalable general compute stack for AI operations?",
        "Is your infrastructure integrated with edge computing and data center environments?",
        "Do you support hyperscaler integration for hybrid or non-sovereign compute needs?",
        "Have you deployed AI workloads in a sovereign data center environment?"
    ],
    "2. Orchestration Layer": [
        "Do you support horizontal and vertical elasticity with auto-scaling and reservation mechanisms?",
        "Have you implemented fractional GPU isolation and account-level multi-tenancy?",
        "Is your infrastructure containerized using platforms like Kubernetes or container registry?",
        "Are you leveraging serverless frameworks for executing cloud functions or AI agent tasks?",
        "Do you use virtualization for VM/Bare Metal provisioning, operations, and support?"
    ],
    "3. Data Foundation Layer": [
        "Do you have a data pipeline for integrating structured and unstructured data sources?",
        "Are synthetic data generation and management services implemented in your environment?",
        "Do you use vector stores, KGs, or blob-based semantic knowledge repositories?",
        "Do you have secure, scalable RAG or search capabilities deployed?",
        "Is your AI solution backed by a data vault, catalog, or secure marketplace?"
    ],
    "4. Model Layer": [
        "Are you fine-tuning or pre-training foundation models using custom recipes?",
        "Do you use traditional ML/DL SDKs, libraries, and notebooks like NeMo or TensorFlow?",
        "Have you applied optimization for model performance and inference efficiency?",
        "Is model deployment managed with tools like MLOps or LLMOps (e.g., NIMs)?",
        "Are inference endpoints available for multi-purpose or API-based serving?"
    ],
    "5. Agents & Applications Layer": [
        "Do you develop AI applications across web, mobile, and conversational UI platforms?",
        "Do you have workflows to manage the lifecycle of AI agents?",
        "Is there a central registry or catalog of custom or reusable AI agents?",
        "Do you manage a tools repository for supporting agent development and integration?",
        "Have you adopted prebuilt agents specific to your industry domain?"
    ],
    "6. Operations & Governance Layer": [
        "Do you use a model switchboard to manage decisioning, routing, and policy enforcement?",
        "Are AI usage, RAI, FinOps, and risk policies enforced through centralized controls?",
        "Are infrastructure security and access managed through baseline controls?",
        "Do you use observability tools to monitor the health and performance of AI workloads?",
        "Are there systems for security, audit logging, vulnerability scanning, and access governance?",
        "Is your AI infrastructure integrated with ITSM for service intelligence?",
        "Do you have disaster recovery and high-availability strategies in place for AI systems?"
    ]
}

# UI to collect scores
for pillar, qs in questions.items():
    st.subheader(pillar)
    scores = []
    for i, q in enumerate(qs, 1):
        score = st.slider(q, 0, 4, 0, key=f"{pillar}_{i}")
        scores.append(score)
    avg = sum(scores) / len(scores)
    responses[pillar] = scores
    pillar_averages[pillar] = avg

def interpret_score(score):
    if score == 0.0:
        return "Not Started"
    elif 0.0 < score <= 1.99:
        return "Pilot"
    elif 2.0 <= score <= 2.99:
        return "Operational"
    elif 3.0 <= score <= 3.99:
        return "Industrialized"
    else:
        return "Optimized"

# Display results
st.markdown("## 📊 Maturity Dashboard")
overall_score = sum(pillar_averages.values()) / len(pillar_averages)
report_data = []
for pillar, score in pillar_averages.items():
    maturity = interpret_score(score)
    st.markdown(f"**{pillar}**: {score:.2f} → **{maturity}**")
    report_data.append([pillar, score, maturity])

overall_level = interpret_score(overall_score)
st.markdown("---")
st.markdown(f"### 🧠 **Overall Maturity Score:** `{overall_score:.2f}`")
st.markdown(f"### 🏁 **Overall Maturity Level:** **{overall_level}**")

# Export
df_report = pd.DataFrame(report_data, columns=["Pillar", "Average Score", "Maturity Level"])
csv = df_report.to_csv(index=False).encode()
st.download_button("📥 Download CSV Report", csv, "ai_readiness_report.csv", "text/csv")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="AI Readiness Assessment Report", ln=True, align='C')
pdf.ln(10)
for row in report_data:
    pdf.multi_cell(0, 10, f"{row[0]}: Score = {row[1]:.2f}, Level = {row[2]}")
pdf.multi_cell(0, 10, f"Overall Score: {overall_score:.2f}, Level: {overall_level}")
pdf_buffer = BytesIO()
pdf_output = pdf.output(dest='S').encode('latin-1')
pdf_buffer.write(pdf_output)
pdf_buffer.seek(0)
pdf_buffer.seek(0)
st.download_button("📥 Download PDF Report", pdf_buffer, "ai_readiness_report.pdf", "application/pdf")

# Assistant for recommendations
if st.button("🔍 Ask AI Assistant for Recommendations"):
    with st.spinner("Thinking..."):
        formatted_scores = "\n".join([f"- {k}: {v:.2f}" for k, v in pillar_averages.items()])
        user_prompt = f"My AI readiness scores are:\n{formatted_scores}\n\nWhat is my overall maturity level and how can I improve?"
        thread = openai.beta.threads.create()
        openai.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_prompt)
        run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id="asst_Cwb6fNX3SumrUkCXO7y5sYGx")  # Replace with your actual assistant_id
        while True:
            status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if status.status in ["completed", "failed"]:
                break
            time.sleep(1)
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        st.markdown("### 🤖 AI Assistant Recommendation")
        st.markdown(response)
