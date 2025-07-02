# AI Readiness Assessment (6-Layer) Framework

This Streamlit app helps assess your organization's AI maturity across six architectural layers - Infrastructure, Data Foundation, AI Foundation Layer, Agentic Framework, Continuous Innovation.

## Features
- One question per architectural component
- Maturity scale from 0 (Not Started) to 4 (Optimized)
- Per-pillar and overall score interpretation
- Agentic recommendations via OpenAI Assistant (GPT-4o)
- PDF and CSV report downloads

## Deployment Instructions
1. Upload files to a new GitHub repository.
2. Deploy via [Streamlit Cloud](https://share.streamlit.io).
3. Add your OpenAI API key to Streamlit secrets:

```bash
streamlit secrets set OPENAI_API_KEY "sk-..."
```

## Maturity Scale
- 0: Not Started
- 1: Pilot
- 2: Operational
- 3: Industrialized
- 4: Optimized

## License
zaldynuque