# 00. Warmup

Four scripts, meant to be run in order. Each one builds on the last.

| File | What to learn |
|---|---|
| `01-first-api-call` | Raw api mechanism: messages, roles, response shape |
| `02-tool-calling` | Giving the model one tool. Native OpenAI-style |
| `03-agent-loop` | The full reason -> act -> observe loop with multiple tools |

# 01. Notes Agent

A small agent the manages text notes using five tools: `calculator`, `get_current_time`,
`list_notes`, `read_note`, `write_note`.

| File | Role |
|---|---|
| `tools.py` | The actual functions and their OpenAI-compatible descriptions, and the sandbox guardrail |
| `agent.py` | The http call to model, and the hardened reasoning loop. |
| `main.py` | A REPL entry point |

# 02. Retrieval

Notes agent can now find the relevant note istead of only teh exact one.

Under the hood: every note gets embedded; a query gets embedded the same way;
cosine similarity ranks notes by how close their meaning is to the query.

| File | Role |
|---|---|
| `embedding.py` | Calls the embedings endpoint, plus cosine similarity |
| `index.py` | A JSON backed vector store: filename -> embedding, with linear-scan search |
| `tools.py` | Adds `search_notes`. Also `write_note`, `append_note` now keep the index in sync. |
| `reindex_notes.py` | One-time backfill for notes that predates the index. |
| `comparison-demo.py` | The actual point of this session. Run standlone. |
| `tools.py` | The actual functions and their OpenAI-compatible descriptions, and the sandbox guardrail |
| `agent.py` | The http call to model, and the hardened reasoning loop. |
| `main.py` | A REPL entry point |