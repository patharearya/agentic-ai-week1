import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import faiss
import numpy as np
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

print("\n========== SEMANTIC SEARCH DEMO ==========\n")

# ------------------------------------------------
# 1️⃣ Load Embedding Model
# ------------------------------------------------

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

print("Model Loaded:", model_name)
print("Embedding Dimension:", model.get_sentence_embedding_dimension())

# ------------------------------------------------
# 2️⃣ Random Text Documents (Your Knowledge Base)
# ------------------------------------------------

documents = [
    "Artificial intelligence is transforming cybersecurity.",
    "Red teaming helps test AI safety systems.",
    "Python is widely used in machine learning.",
    "FAISS is a library for fast similarity search.",
    "Transformers use attention mechanisms.",
    "Embeddings convert text into numerical vectors.",
    "Cybersecurity protects systems from attacks.",
    "Neural networks learn from large datasets.",
    "Data science involves statistics and programming.",
    "Large language models are trained on massive text data."
]

print("\nNumber of Documents:", len(documents))

# ------------------------------------------------
# 3️⃣ Convert Documents to Embeddings
# ------------------------------------------------

doc_embeddings = model.encode(documents)
doc_embeddings = F.normalize(torch.tensor(doc_embeddings), p=2, dim=1)
doc_embeddings = doc_embeddings.numpy().astype("float32")

print("Document Embedding Shape:", doc_embeddings.shape)

# ------------------------------------------------
# 4️⃣ Store in FAISS (LOCAL)
# ------------------------------------------------

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine if normalized)

index.add(doc_embeddings)

print("Vectors Stored in FAISS:", index.ntotal)

# ------------------------------------------------
# 5️⃣ Ask Question
# ------------------------------------------------

query = "How does AI improve security?"
print("\nQuery:", query)

query_embedding = model.encode([query])
query_embedding = F.normalize(torch.tensor(query_embedding), p=2, dim=1)
query_embedding = query_embedding.numpy().astype("float32")

# ------------------------------------------------
# 6️⃣ Search Top 3 Results
# ------------------------------------------------

k = 3
scores, indices = index.search(query_embedding, k)

print("\nTop Results:\n")

for rank, idx in enumerate(indices[0]):
    print(f"Rank {rank+1}")
    print("Score:", scores[0][rank])
    print("Document:", documents[idx])
    print("-" * 40)

print("\n========== DONE ==========\n")