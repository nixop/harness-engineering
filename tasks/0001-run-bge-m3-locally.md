# TASK-0001: Run bge-m3 locally on macOS / Linux

**Status:** Open
**Source:** [ADR-0001](../docs/adr/0001-embedding-model-for-docs-and-meeting-transcripts.md)
**Deliverable:** bge-m3 serving `POST /v1/embeddings` on the developer's machine, callable with curl, with the exact parameters below; a short smoke record saved in this repo

---

## Goal

Get the chosen model running on a laptop so that it can be called by any OpenAI-compatible client. **llama.cpp is the recommended runtime**; Ollama is the fallback for people who already have it. Both paths must produce the same vectors for the same input, so the parameter contract is identical and is the point of this task.

## Parameter contract

This is the single source of truth for every runtime, local or cluster. ADR-0002 and TASK-0002 reference it rather than repeat it.

| Parameter | Value | llama.cpp flag | Ollama |
|---|---|---|---|
| Model file | `gpustack/bge-m3-GGUF` → `bge-m3-FP16.gguf` | `-m <file>` or `-hf gpustack/bge-m3-GGUF:FP16` | library tag `bge-m3:567m` (F16) |
| sha256 | `daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c` (1 157 671 200 bytes) | verify after download | pin by digest from `ollama show` |
| Mode | embeddings only | `--embeddings` | implicit |
| Pooling | CLS | `--pooling cls` | from model metadata |
| Normalisation | L2 | `--embd-normalize 2` | always on in `/api/embed` |
| Context | 8192 tokens per slot | `--ctx-size 8192 --parallel 1` | `options.num_ctx: 8192` on every call (default is 2048/4096) |
| Batch | one request fits one micro-batch | `--batch-size 8192 --ubatch-size 8192` | n/a |
| Over-length input | rejected with an error, never truncated | default behaviour | `truncate: false` on every call |
| Endpoint | OpenAI-compatible | `POST /v1/embeddings` | `POST /v1/embeddings` or `/api/embed` |

## Path A (recommended): llama.cpp

### 1. Install

macOS:

```bash
brew install llama.cpp
# or the upstream installer, which also provides the newer `llama` CLI:
curl -LsSf https://llama.app/install.sh | sh
```

Linux:

```bash
curl -LsSf https://llama.app/install.sh | sh
# or download a prebuilt archive from https://github.com/ggml-org/llama.cpp/releases
# (pick the one matching your CPU / GPU backend) and put llama-server on PATH
```

Record the build: `llama-server --version`. The cluster image in TASK-0002 should pin the same build line; vectors across llama.cpp builds are normally identical, but a kernel change can move them, and the build number is how you find out.

### 2. Fetch the model and verify it

```bash
mkdir -p ~/models/bge-m3 && cd ~/models/bge-m3
curl -fL --retry 5 -o bge-m3-FP16.gguf \
  https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-FP16.gguf
echo "daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c  bge-m3-FP16.gguf" | shasum -a 256 -c
```

`shasum -a 256 -c` must print `OK`. On Linux without `shasum`, use `sha256sum -c`.

### 3. Serve

```bash
llama-server \
  --host 127.0.0.1 --port 8090 \
  --embeddings --pooling cls --embd-normalize 2 \
  --ctx-size 8192 --batch-size 8192 --ubatch-size 8192 --parallel 1 \
  -m ~/models/bge-m3/bge-m3-FP16.gguf
```

Quick alternative that skips step 2 (llama.cpp downloads into its own cache; you do not get to check the hash):

```bash
llama-server -hf gpustack/bge-m3-GGUF:FP16 \
  --host 127.0.0.1 --port 8090 \
  --embeddings --pooling cls --embd-normalize 2 \
  --ctx-size 8192 --batch-size 8192 --ubatch-size 8192 --parallel 1
```

Notes:
- `--ubatch-size` is the real per-request ceiling for a pooled embedding; it must be at least the slot size. The default (512) silently fails long inputs with a batch error, which looks like a bug but is the wrong flag.
- On Apple Silicon the Metal backend is used automatically. On Linux CPU, an 8192-token input materialises a large attention working set; if memory spikes, add `--flash-attn on` and note it in the report.
- `--parallel 1` is enough for a laptop. `--parallel N` divides `--ctx-size` by N, so `--parallel 2` needs `--ctx-size 16384` to keep an 8192 slot.

## Path B (fallback): Ollama

```bash
ollama pull bge-m3
ollama show bge-m3 --modelfile | head -5        # record the digest
```

Every call must carry the context and truncation overrides, because Ollama's defaults are wrong for this model:

```bash
curl -s http://127.0.0.1:11434/api/embed -d '{
  "model": "bge-m3",
  "input": ["что мы решили про gateway timeout?", "what did we decide about the gateway timeout?"],
  "truncate": false,
  "options": {"num_ctx": 8192}
}' | jq '.embeddings | map(length)'
```

If a client library cannot set per-call options, create a Modelfile with `PARAMETER num_ctx 8192` and run `ollama create bge-m3-8k -f Modelfile`, then call `bge-m3-8k`. Truncation still has to be disabled per call; Ollama has no model-level switch for it.

## Verify (both paths)

Replace the host/port for Ollama (`127.0.0.1:11434`, same `/v1/embeddings` path).

```bash
curl -s http://127.0.0.1:8090/v1/embeddings -H 'Content-Type: application/json' -d '{
  "model": "bge-m3",
  "input": ["что мы решили про gateway timeout?", "what did we decide about the gateway timeout?"]
}' | tee /tmp/embed.json | jq '.data | map({dim: (.embedding|length), norm: (.embedding|map(.*.)|add|sqrt)})'

# cosine between the Russian and the English sentence
jq -r '.data[0].embedding as $a | .data[1].embedding as $b
       | [range(0; $a|length)] | map($a[.] * $b[.]) | add' /tmp/embed.json
```

Expected:

| Check | Expected |
|---|---|
| `dim` | 1024 for both |
| `norm` | 1.0 ± 0.001 |
| cosine RU↔EN | above 0.8 (the cross-lingual property ADR-0001 relies on) |
| input of ~9000 tokens | HTTP error, not a vector |

Save the raw `/tmp/embed.json`, the server version line, and the exact command used under `evals/embeddings/local-smoke/<hostname>-<date>/` in this repo. TASK-0002 compares cluster output against it.

## Acceptance criteria

- [ ] `llama-server` (or Ollama) is running with the parameter contract above and survives a restart of the terminal (document how: launchd/systemd unit, or just the command in a `Makefile` target, your call).
- [ ] `POST /v1/embeddings` returns 1024-dim, L2-normalised vectors for Russian and English input.
- [ ] Over-length input is rejected.
- [ ] GGUF sha256 verified (Path A) or Ollama digest recorded (Path B).
- [ ] Smoke record saved under `evals/embeddings/local-smoke/`.
- [ ] Report filled in.

## Report

- **Machine (OS, CPU/GPU, RAM):**
- **Runtime and build:**
- **Path used:** A / B
- **Model digest / sha256 verified:** yes / no
- **dim / norm / RU↔EN cosine:**
- **Flash attention needed:** yes / no
- **Deviations from the parameter contract:** none / list
