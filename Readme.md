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