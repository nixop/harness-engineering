# ADR-0001: Embedding model for English project docs and Russian meeting transcripts

**Status:** Proposed
**Date:** 2026-10-05
**Deciders:** harness-engineering lab owner

## Context

We are building a retrieval layer (RAG) over two corpora:

| Source | Language | Shape |
|---|---|---|
| Project documentation | English | Edited prose in two formats: Markdown in Git repositories and Confluence pages (storage-format XHTML with macros, tables, attachments). Long structured pages, code identifiers |
| Meeting transcripts | Russian | ASR output, noisy, speaker turns, heavy code-switching into English for technical terms (service names, tickets, tools) |

The original framing was "an embedding model for English text". That framing does not survive contact with the data: half of the corpus is Russian, and the realistic query pattern is cross-lingual. A Russian question asked after a meeting ("что мы решили про gateway timeout?") must retrieve the English page that documents the decision, and an English question must retrieve the Russian transcript where it was discussed. So the decision is really: **one multilingual model that puts Russian and English in the same vector space**, or two monolingual models with two indexes.

Hard constraints:

- **Local inference only.** The model must run via `llama.cpp` (GGUF) or Ollama. No hosted embedding APIs. This rules out every closed model and any open model that has no stable GGUF / llama.cpp architecture support.
- **Commercial-safe license.** Apache-2.0, MIT or equivalent. Non-commercial licenses are rejected even for a lab, because the lab is meant to produce something we can ship.
- **Runs on a developer laptop and in a Kubernetes cluster** on CPU, or a single consumer GPU. Practical budget: under about 1B parameters, under about 2 GB on disk.
- **Vector store is Qdrant.** Embedding dimension is fixed per collection, so changing the model means a full re-index.

Soft requirements:

- Context window of at least 2K tokens, so that a transcript chunk covering several speaker turns is embedded whole.
- Strong retrieval quality for Russian specifically, not just "100+ languages" on the box. Most multilingual models are tuned on Western European languages; Russian is often a second-tier language for them.
- Minimal prompt-format surface. Models that need different prefixes or instructions for queries versus documents are a known source of silent quality bugs: a mismatched prefix does not error, it just degrades recall.

Non-goals for this ADR: how the model is served (see [ADR-0002](0002-embedding-server-deployment-topology.md) for the cluster and [TASK-0001](../../tasks/0001-run-bge-m3-locally.md) for laptops), the reranker, chunking, and the evaluation harness.

## Decision

Use **BAAI `bge-m3`** (568M params, 1024-dim dense embeddings, 8192-token context, MIT) as the single embedding model for both corpora. All sources go into one Qdrant collection with a `source` payload field (`docs-md` | `docs-confluence` | `meeting`) and a `lang` field, so that filtering by source stays possible while cross-lingual retrieval works by default.

**Qwen3-Embedding-0.6B** is the named alternative. If it is later shown to beat bge-m3 on our own Russian-to-English queries by a clear margin, this ADR gets superseded.

## Options Considered

Models that fail a hard constraint are listed at the end under *Rejected without full evaluation*.

### Option A: `bge-m3` (BAAI) — chosen

| Dimension | Assessment |
|---|---|
| Complexity | Low. Encoder (XLM-RoBERTa-large), CLS pooling, no query/document prefixes. First-party Ollama entry; mature llama.cpp support for the BERT family. |
| Cost | 568M params, ~1.2 GB F16 / ~0.6 GB Q8_0. Runs on CPU at usable speed. |
| Quality / fit | Best sub-1B model on ruMTEB retrieval (74.8 retrieval, 69.7 reranking in the ruMTEB paper, NAACL 2025). 100+ languages, trained explicitly on long documents up to 8K. Dense + sparse + multi-vector outputs available if we ever want hybrid search. |
| Team familiarity | High. It has been the default "boring multilingual choice" since 2024 and is widely documented. |

**Pros:**
- Strongest evidence of all candidates specifically for Russian retrieval, not just aggregate multilingual scores.
- Symmetric model: the same text encodes the same way whether it is a query or a passage. Nothing to get wrong in the pipeline.
- 8K context covers any sane chunk size for transcripts.
- MIT license.
- Available out of the box in both runtimes we care about.

**Cons:**
- Older architecture (early 2024). On aggregate MMTEB it sits below Qwen3-Embedding-0.6B and multilingual-e5-large-instruct.
- Fixed 1024 dims; no Matryoshka truncation, so storage per vector is what it is.
- Multi-vector and sparse heads are not exposed through Ollama; only dense is available there.

### Option B: `Qwen3-Embedding-0.6B` (Alibaba) — named alternative

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Decoder-based, last-token pooling, and queries are supposed to carry a task instruction (`Instruct: ... \nQuery: ...`). Output quality depends on the instruction string, which must be versioned alongside the index. Ollama has a first-party entry (`qwen3-embedding:0.6b`); llama.cpp needs the right pooling flag. |
| Cost | 0.6B params, ~0.64 GB Q8_0. Comparable to bge-m3. |
| Quality / fit | Higher aggregate MMTEB score (64.33 for the 0.6B, per the Qwen3-Embedding paper, June 2025) than bge-m3. 100+ languages, 32K context, Matryoshka dims 32–1024. Russian-specific retrieval numbers are less established than for bge-m3. |
| Team familiarity | Medium. Newer; fewer production war stories. |

**Pros:**
- Likely the best quality-per-parameter of the open models that fit our budget.
- 32K context and variable dimensions give room to shrink storage later.
- Apache-2.0. Larger siblings (4B, 8B) exist if we ever get a GPU budget, same vector space family.

**Cons:**
- Asymmetric query/document handling is exactly the prompt-surface risk called out in Context.
- Aggregate benchmark lead does not automatically translate into a lead on noisy Russian ASR text. Unproven on our data.

### Option C: `multilingual-e5-large-instruct` (Microsoft)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Same XLM-R-large backbone as bge-m3, but queries need an instruction prefix. Not in the Ollama library; must be imported from a community GGUF. |
| Cost | 560M params, same footprint as bge-m3. |
| Quality / fit | Roughly tied with bge-m3 on ruMTEB retrieval (74.0) and slightly above on MMTEB. **512-token context** is the problem. |
| Team familiarity | High. |

**Pros:** proven on Russian; MIT.
**Cons:** 512-token limit forces small chunks and loses meeting context; needs prefixes; no first-party Ollama entry. Dominated by bge-m3 for our use.

### Option D: `nomic-embed-text-v2-moe` (Nomic)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Requires `search_query:` / `search_document:` prefixes. MoE architecture; llama.cpp support landed in 2025, but it is not a first-party Ollama entry. |
| Cost | 475M total / 305M active params. Cheapest per token of the serious multilingual candidates. |
| Quality / fit | Good multilingual scores; Russian is in the training mix but is not a headline language. **512-token context.** 768 dims with Matryoshka down to 256. |
| Team familiarity | Low. |

**Pros:** cheap inference, Apache-2.0, small vectors.
**Cons:** 512-token context, prefix requirement, weaker Russian evidence, less mature runtime support.

The English-only predecessor, `nomic-embed-text-v1.5`, is what the reference material for this lab uses. It is a fine English model and a well-trodden llama.cpp path, but it cannot embed the Russian half of the corpus, so it only appears here inside Option F.

### Option E: `embeddinggemma-300m` (Google)

| Dimension | Assessment |
|---|---|
| Complexity | Low-Medium. First-party Ollama entry; task prompts are recommended for best quality. |
| Cost | Smallest option: 300M params, ~0.6 GB. Built for on-device use. |
| Quality / fit | Respectable MMTEB for its size, below the 0.6B class. 2K context, 768 dims with Matryoshka to 128. Gemma Terms of Use rather than a standard OSI license. |
| Team familiarity | Low. |

**Pros:** tiny, fast, 100+ languages.
**Cons:** quality ceiling is lower; license is a custom one that needs review; 2K context is enough but tight.

### Option F: Two monolingual models (one for English docs, one for Russian transcripts)

For example `nomic-embed-text-v1.5` or `mxbai-embed-large` for English, and FRIDA (ai-forever) or GigaEmbeddings for Russian.

| Dimension | Assessment |
|---|---|
| Complexity | **High.** Two models, two Qdrant collections, two vector spaces that cannot be searched together. Cross-lingual queries require either query translation or result merging with incomparable scores. |
| Cost | Two models in memory. |
| Quality / fit | Each model is best-in-class in its own language, and FRIDA/GigaEmbeddings lead ruMTEB. But FRIDA is a T5 encoder and GigaEmbeddings is a multi-billion-parameter decoder; neither has a clean llama.cpp / Ollama path today. |
| Team familiarity | Medium. |

**Pros:** best possible monolingual quality per corpus.
**Cons:** kills the primary use case (cross-lingual retrieval); doubles the pipeline surface; the Russian-only leaders fail the local-runtime constraint.

### Rejected without full evaluation

| Model | Reason |
|---|---|
| `jina-embeddings-v3` / v4 | CC BY-NC 4.0. Fails the license constraint. |
| `snowflake-arctic-embed2` | Targets English, French, Spanish, Italian, German. Russian is not a supported language. |
| `nomic-embed-text` v1.5, `mxbai-embed-large`, `all-minilm` | English-only. Only viable inside Option F. |
| FRIDA, GigaEmbeddings, ru-en-RoSBERTa | Russian-first and strong on ruMTEB, but no stable GGUF / Ollama path. Only viable inside Option F. |
| OpenAI / Voyage / Cohere / Gemini embedding APIs | Hosted. Fail the local-only constraint. |
| Qwen3-Embedding-4B / 8B | Exceed the laptop / cluster budget. Noted as the upgrade path if Option B is ever adopted and a GPU appears. |

## Trade-off Analysis

The decision reduces to bge-m3 versus Qwen3-Embedding-0.6B. Everything else is either dominated (C, D, E) or breaks the use case (F).

**Quality.** Qwen3 wins on aggregate multilingual benchmarks. bge-m3 has the stronger published evidence on Russian retrieval specifically. Neither has been measured on noisy, code-switched Russian ASR text, which is our hardest input.

**Operational risk.** bge-m3 is symmetric; Qwen3 is instruction-conditioned. We prefer the component with fewer silent failure modes as the default. A model that cannot be misconfigured by a missing prefix is worth a few benchmark points.

**Runtime support.** Both have first-party Ollama entries. bge-m3's BERT-family architecture has been stable in llama.cpp for longer; Qwen3's decoder-embedding path is newer and needs the correct pooling flag.

**Matryoshka Representation Learning (MRL).** The lab's reading list includes MRL, and three of the candidates (Qwen3-Embedding, nomic-embed-text-v2-moe, embeddinggemma) are trained with it: the first N dimensions of the vector are themselves a usable embedding, so a 1024-dim vector can be truncated to 256 at index time or at query time with a small, predictable quality loss. bge-m3 is not MRL-trained; its 1024 dims are all-or-nothing. We accept that for two reasons. First, scale: our corpus is tens of thousands of chunks, so full-size vectors cost tens of megabytes and nothing is gained by shrinking them. Second, the thing MRL optimises for (storage and ANN search cost at millions of vectors, or adaptive retrieval that re-ranks a coarse shortlist with full vectors) is a problem we do not have. If the corpus grows by two orders of magnitude, MRL becomes a real argument for Option B and is added to the revisit triggers below.

**What we give up** by choosing bge-m3: MRL as above, 32K context, and a few points of aggregate benchmark score. None of these matter at lab scale.

**Why not two models (F).** It optimises each corpus in isolation and destroys the thing we actually want, which is asking in one language and finding answers written in the other.

## Consequences

- **Easier:** one model, one Qdrant collection, one vector space. Cross-lingual retrieval works without translation. No prefix logic in the ingestion or query path.
- **Easier:** the embedder is a pure function `text -> vec[1024]`, which keeps every downstream component simple.
- **Harder:** any future model change is a full re-index of both corpora. Index payload must record the model name and quantization so stale vectors are detectable.
- **Harder:** Russian ASR noise is handled entirely by the embedder. If that is not enough, the fix is in chunking or transcript cleanup, not in this decision.
- **Harder:** the same model must produce the same vectors on a laptop and in the cluster. That is a serving concern and is handled in TASK-0001 and ADR-0002, but it exists because of this decision.
- **Revisit triggers:** (1) our own Russian-to-English retrieval numbers show Qwen3-Embedding-0.6B ahead by a clear margin; (2) a GPU budget appears that makes the 4B class viable; (3) a new sub-1B multilingual model with published ruMTEB numbers above bge-m3 and first-party Ollama support ships; (4) the corpus grows to the point where vector storage or ANN latency is a cost, which is when MRL truncation starts to pay. Check the MTEB leaderboard and ruMTEB when any of these happens, not on a schedule.

## Validation (2026-10-07, TASK-0003)

The decision was checked against the two MiniLM models the lab names, on the abox sandbox (branch `feat/llmd-embeddings`, 4-core Codespace), with the same 270 chunks of Kubernetes manifests indexed three times and the same 24 questions (12 English, 12 Russian) asked three ways. Raw retrieval was measured on the MCP `find` tool without an LLM; answer quality was measured through a kagent agent (gpt-5.4-mini) with one vector tool and a prompt that forbids translating the question. Full traces, scores and notes: `evals/retrieval/runs/2026-10-07/`.

| Embedder | Served by | Dims | RU hit@1 | RU hit@5 | EN hit@1 | EN hit@5 | Agent answers correct (RU / EN / all) | Peak RSS |
|---|---|---|---|---|---|---|---|---|
| **bge-m3** (chosen) | llama.cpp + branch `qdrant-mcp` | 1024 | **0.67** | **0.92** | **0.92** | 1.0 | **92% / 96% / 94%** | 1.4 GiB (llama.cpp) + 54 MiB (MCP) |
| all-MiniLM-L6-v2 (English-only) | official MCP, FastEmbed in-process | 384 | 0.58 | 0.83 | 0.83 | 1.0 | 88% / 92% / 90% | 2.0 GiB |
| paraphrase-multilingual-MiniLM-L12-v2 | official MCP, FastEmbed in-process | 384 | 0.58 | 0.92 | 0.50 | 1.0 | 83% / 96% / 90% | 2.7 GiB, **OOMKilled once at 3Gi** |

What the numbers say:

- **bge-m3 is the best retriever on both languages**, and the only one that is good at both: hit@1 0.67 on Russian and 0.92 on English. The multilingual MiniLM pays for its Russian with English (hit@1 0.50); the English-only MiniLM is weaker on Russian but not catastrophically so, because the questions carry Latin identifiers (Phoenix, kagent, llm-d) that it can match.
- **At the answer level the gap narrows to a few points** (94% vs 90% vs 90%): the agent reads five to ten chunks and a strong LLM recovers from a weak first hit. On a 270-chunk corpus any of the three is usable. The embedder's quality shows up in hit@1, in latency to a correct answer, and in how often the agent gives up ("not found" on ru06 for the English-only model, wrong rewrite on ru05 for the multilingual one).
- **Operationally the official MCP is the expensive part, not the model.** Embedding in-process with FastEmbed cost 2.0 and 2.7 GiB peak for two 384-dim models, and the multilingual one was OOMKilled at a 3Gi limit under ingest plus concurrent queries, losing 17 of 24 agent runs. The branch's MCP that delegates to llama.cpp stays at 54 MiB, and bge-m3 under llama.cpp sits at 1.4 GiB with no restarts, serving 1024-dim vectors with an 8K window. This confirms the branch author's reason for replacing the official server.
- **Chunking was sized for the weakest model** (350 characters, under the multilingual MiniLM's 128-token window), so bge-m3's long-context advantage was not exercised at all. The gap in favour of bge-m3 is a floor, not a ceiling.

Verdict: the decision stands. The named alternative for a future re-evaluation remains Qwen3-Embedding-0.6B, not either MiniLM.

## Follow-ups

- [TASK-0001](../../tasks/0001-run-bge-m3-locally.md): run the model locally on macOS / Linux with llama.cpp (recommended) or Ollama.
- [ADR-0002](0002-embedding-server-deployment-topology.md): how the model is served in the cluster (standalone, sidecar, llm-d).
- [TASK-0002](../../tasks/0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md): deploy it in the cluster per ADR-0002.

## References (checked 2026-10-05)

- bge-m3 on Ollama: https://ollama.com/library/bge-m3
- bge-m3 GGUF files: https://huggingface.co/gpustack/bge-m3-GGUF
- Qwen3-Embedding on Ollama: https://ollama.com/library/qwen3-embedding
- Qwen3-Embedding paper (MTEB multilingual scores): https://arxiv.org/abs/2506.05176
- ruMTEB benchmark paper, with per-model Russian retrieval scores (NAACL 2025): https://aclanthology.org/2025.naacl-long.12/
- multilingual-e5-large-instruct: https://huggingface.co/intfloat/multilingual-e5-large-instruct
- nomic-embed-text-v1.5 (the lab's reference model): https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
- nomic-embed-text-v2-moe: https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe
- embeddinggemma on Ollama: https://ollama.com/library/embeddinggemma
- snowflake-arctic-embed2 on Ollama (language list): https://ollama.com/library/snowflake-arctic-embed2
- GigaEmbeddings paper: https://arxiv.org/abs/2510.22369
- llama.cpp: https://llama-cpp.com/
- Matryoshka Representation Learning (Kusupati et al., 2022): https://arxiv.org/abs/2205.13147
