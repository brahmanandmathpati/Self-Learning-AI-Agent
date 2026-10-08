# Troubleshooting

| Problem | Fix |
|---|---|
| `sla: command not found` | Activate the virtual environment and run `pip install -e ".[dev]"` again. |
| `ModuleNotFoundError: torch` | `pip install torch --index-url https://download.pytorch.org/whl/cpu`. FrozenLake works without PyTorch. |
| `Error: Invalid config value for 'gamma'` | The message names the bad key; fix it in the YAML. |
| `Error: ... is not a run folder` | Pass `--run runs/<run_id>` (the folder that contains `config.yaml`). |
| `No checkpoints in runs/...` | The run stopped before its first checkpoint; lower `checkpoint_every` or train longer. |
| Dashboard shows NOT RUN everywhere | No experiments yet, or a different database: check `SLA_DB` and run `sla runs`. |
| `database is locked` | Close other tools holding the database (e.g. DB Browser for SQLite with unsaved changes). |
| Reflection says "Ollama offline" | Expected without Ollama; the template note is used. Start `ollama serve` to enable the LLM. |
| LLM note rejected | It contained numbers not in the facts; the template note is shown instead — this is the validator working. |
| CartPole picture missing | `pip install pygame` (optional). |
| Results differ slightly between computers | Floating-point and library differences; compare means over seeds. |
