# Context-Aware AI Shopping Agent

A V1 AI product recommendation pipeline designed around contextual fashion discovery.

## Pipeline

User query
→ Context extraction
→ BGE embeddings
→ Semantic retrieval
→ Rule-based reranking
→ Personalization
→ Recommendations

## Tech stack

- Python
- Sentence Transformers
- BAAI BGE-small-en-v1.5
- NumPy
- Pandas
- Scikit-learn

## Setup

Create and activate a virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the synthetic catalog:

```bash
python data/generate_products.py
```

Run the recommendation agent:

```bash
python src/main.py
```

Example query:

```text
I have a friend's engagement in Delhi. I want something elegant and modern under 5000.
```

## Evaluation

Run:

```bash
python evaluation/evaluate.py
```

## Important

The product catalog is synthetic and exists only for demonstrating the recommendation pipeline.

## Future versions

V2:
- Qdrant vector database
- Hybrid dense + keyword retrieval
- Better reranking

V3:
- Image-based fashion search
- Multimodal embeddings
- Visual similarity

V4:
- Stronger feedback loops
- User preference modeling
- Offline recommendation evaluation
- LLM-based explanations
