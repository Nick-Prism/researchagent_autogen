# Research AutoGen - Virtual Research Assistant

## One-line summary
A small Streamlit app that fetches research papers for a topic, summarizes them with an LLM, and produces concise, pointwise advantages and disadvantages for each paper.

## Who this is for
This repository is for someone who wants quick, human-readable summaries of academic work without reading every paper. It’s aimed at researchers and engineers who want to triage literature rapidly and get a short pros/cons view to help decide what to read next.

## What it does
- Takes a research topic as input.
- Fetches relevant papers from ArXiv (and optionally Google Scholar).
- Uses configured assistant agents to generate:
  - A concise summary of each paper.
  - A pointwise list of advantages and disadvantages based on the summary.
- Presents results in a Streamlit UI with title, link, summary, and pros/cons.

## Project structure
- `app.py` — Streamlit application and UI wiring. Reads an API key, accepts a user query, fetches papers, calls agents, and renders results.
- `agents.py` — Thin agent wrapper that configures two AssistantAgent instances: a summarizer and an advantages/disadvantages analyzer.
- `data_loader.py` — Responsible for fetching papers from ArXiv and Google Scholar. Returns structured paper records: title, summary, link.
- `requirement.txt` — Declared dependencies.

## Quick start
1. Create a file named `.env` at the repository root and set your API key:

```bash
# example
GROQ_API_KEY=your_api_key_here
```

2. Install dependencies:

```bash
pip install -r requirement.txt
```

3. Run the app:

```bash
streamlit run app.py
```

Open the local Streamlit URL it prints and enter a research topic.

## Configuration
- The app expects a `GROQ_API_KEY` environment variable for the LLM configuration.
- Agents are configured in `agents.py` via the `autogen` AssistantAgent interface; adjust `llm_config` to change model or provider settings.

## Notes on behavior and limitations
- The app fetches up to five papers per query. If fewer results appear, it attempts to expand search topics.
- External network calls (ArXiv, Google Scholar, LLM provider) may fail or be rate-limited. Expect variability in results and response times.
- Outputs from the agents are presented as plain text; the UI does not attempt to parse or normalize semantic content from LLM replies.

## Suggestions for reuse or extension
- Add caching for paper queries to avoid repeated network calls.
- Return structured agent outputs (JSON with `summary`, `highlights`, `confidence`) to make downstream processing or filtering reliable.
- Add pagination and filtering in the UI for larger result sets.
- Add unit tests that mock network and agent calls so CI can validate basic flows.

## Dependencies
See `requirement.txt` for the list. The main pieces are:
- `streamlit` — UI
- `autogen` — agent wrapper used to talk to an LLM provider
- `scholarly` — optional Google Scholar helper
- `python-dotenv` — environment variable loader

## Closing
This is a compact, practical tool for rapid literature triage. It’s designed to be readable and easy to adapt: change the agent prompts, swap the LLM configuration, or extend the data sources as needed.
