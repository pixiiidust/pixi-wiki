---
source_url: https://youtu.be/2bq64wjtgnQ
source_title: "Machine Learning Engineering Episode 4: Embeddings, Semantic Search, and RAG"
source_creator: Tonbi
ingested: 2026-06-15
sha256: 8445a2f616e350800c96bc98873a2d40e8b4107ee02fbd73f4e27543e2c84e86
---

# Machine Learning Engineering Episode 4: Embeddings, Semantic Search, and RAG

## Introduction

Welcome to episode 4 of the Machine Learning Engineering series. This episode focuses on embeddings, a concept you have probably already encountered.

Embeddings are vectors of numbers that represent meaning. In this episode, we use them as a practical tool. By the end, we will have a working semantic search engine and a retrieval-augmented generation pipeline, also called RAG.

Embeddings are a crucial part of AI systems because they allow models to search through large amounts of data efficiently. First, we will break down what embeddings are, what they mean, how they are used, and where they appear inside models. Then, in the practical section, we will use embeddings to build a semantic search engine for the One Piece synopsis dataset from previous episodes.

## What Are Embeddings?

An embedding is a list of numbers, also called a vector, that represents a piece of text.

The key property of embeddings is this: text with similar meaning produces similar vectors.

For example, sentences about animals tend to cluster together. A sentence like “cat sat on a mat” may be close to “kitten on the rug” or “dog lay on the bed,” even if the exact words are different.

A separate cluster might contain anime or action-related sentences, such as “Luffy punched” or “Zoro slashed.” Another cluster might contain sentences about the economy.

A useful way to think about embeddings is as GPS coordinates for meaning. Every sentence gets a location in meaning space. Similar sentences are nearby. Different sentences are far apart. By measuring the distance between these locations, we can search by meaning instead of only by exact keywords.

This is why embeddings are useful for semantic search. A query like “dog lay on bed” can still be considered similar to “cat sat on mat,” even though the words are not the same. The system understands that both sentences are about an animal resting on something.

## Embeddings You Have Already Seen

Embeddings are not a completely new concept in this series.

In episode 2, our mini GPT used:

```python
nn.Embedding(vocab_size, d_model)
```

That embedding layer was a lookup table that converted each token into a vector of numbers.

In the previous episode, we also saw that Qwen 2.5B had a hidden size of a little over 2,000 numbers per token flowing through the transformer.

In those examples, the vectors were intermediate representations. They flowed through the model on the way to predicting the next token. We cared about the final prediction, not the vectors themselves.

In this episode, the situation is different. We use models that are specifically trained so the final vector is a meaningful summary of the input text. The whole point is the vector itself.

## How Embeddings Capture Meaning

Because embeddings represent meaning as numbers, we can do math on meaning.

A famous example is:

```text
king - man + woman ≈ queen
```

The vector for “king” minus the vector for “man” removes the male-associated direction while keeping the royalty-related meaning. Adding “woman” moves the result toward “queen.”

Other classic examples include:

```text
Paris - France + Japan ≈ Tokyo
walked - walk + swim ≈ swam
bigger - big + small ≈ smaller
```

These examples come from the original word2vec research. They are somewhat cherry-picked, and the math does not always work this cleanly, especially with modern sentence-level embeddings.

However, the underlying idea is real. Meaning is organized into a structured space with consistent directions. Relationships are encoded in the geometry.

This structure is what makes similarity search possible. If meaning is organized consistently, then sentences about similar topics naturally cluster together.

## From Token Vectors to Sentence Embeddings

A transformer usually produces one vector per token.

For the sentence:

```text
Luffy found the treasure.
```

The model produces separate vectors for each token. But for semantic search, we usually need one vector for the whole sentence, so we can compare it against other sentences.

There are a few ways to combine token vectors into one sentence vector.

## Mean Pooling

The most common method is mean pooling.

Mean pooling averages all token vectors together to produce one sentence embedding.

This is simple mathematically, but it works well because embedding models are trained to make that average meaningful.

## CLS Token Pooling

Another method is CLS token pooling.

Some BERT-style models prepend a special CLS token at the beginning of the input. During training, the model learns to pack the meaning of the whole sentence into this token’s vector.

At the end, we take the CLS token vector and ignore the rest.

In both cases, we go from many token vectors to one sentence vector. That single vector is what we store in a database and compare against queries.

In practice, these vectors are not just two-dimensional. Most embedding vectors have hundreds or thousands of dimensions, often between 384 and over 1,000.

## Similarity Metrics

Once we have embeddings, we need a way to compare them.

The most common method is cosine similarity.

Cosine similarity measures the angle between two vectors while ignoring their length.

The general scale is:

```text
1.0  = same direction, very similar meaning
0.0  = perpendicular, mostly unrelated
-1.0 = opposite direction, opposite meaning
```

In practice, many embedding models usually produce scores mostly between 0 and 1. A score above 0.7 or 0.8 often means the sentences are about the same thing.

For example, “cat on the mat” and “kitten on the rug” would likely have a high similarity score because the meaning is very close. “Cat on the mat” and “Luffy punched” would have a much lower score because the topics are different.

## Why Cosine Similarity Is Useful

Cosine similarity is useful because it ignores vector magnitude.

A short document and a long document about the same topic might have vectors with different lengths. But if they point in the same direction, cosine similarity will still treat them as similar.

A simple distance metric might miss that relationship because it is affected by vector length.

This is why cosine similarity is the standard way to compare embeddings.

## Embedding Models

Not every language model produces good embeddings.

You cannot simply take a random Qwen or Llama model and use its hidden states for search. Those models are optimized for next-token prediction, not for producing vectors where similar texts are close together.

For semantic search, we need models specifically trained for similarity.

The standard library for this is Sentence Transformers. It wraps Hugging Face models and provides a simple `encode` method that handles tokenization, the forward pass, and pooling in one call.

A basic example looks like this:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(["cat on mat", "kitten on rug"])
```

Popular embedding models include `all-MiniLM-L6-v2` and larger, higher-quality models.

Embedding models are usually much smaller than generation models. Some are around 80 megabytes, while larger ones may be around 1.3 gigabytes. Embedding is generally cheap and fast. In a RAG pipeline, the expensive part is usually LLM generation, not embedding.

## Vector Databases

Once we have embeddings, we need somewhere to store them.

If we only have a thousand documents, we can compare a query against every document in a loop. But if we have a million documents, that becomes too slow.

Vector databases solve this by using approximate nearest neighbor algorithms, also called ANN algorithms. These algorithms find the closest vectors without checking every single one.

Instead of scanning every shelf in a library, the algorithm organizes vectors into neighborhoods. When a query comes in, it jumps to the right neighborhood and searches there.

It might miss a slightly better match far away, but it is much faster and more practical.

## FAISS

For this project, we use FAISS, which stands for Facebook AI Similarity Search.

FAISS is a Python library that can store and search vectors efficiently. It is a good fit for a small semantic search project.

Other vector database options include Chroma, Pinecone, and Weaviate.

FAISS can search very large vector collections extremely quickly. Our One Piece dataset only has 1,154 episode synopses, so searching it will be nearly instant.

## Retrieval-Augmented Generation

Embeddings become especially powerful when combined with RAG.

RAG stands for retrieval-augmented generation.

Large language models have two major limitations:

1. They only know what was in their training data.
2. They have limited context windows.

RAG helps with both problems by retrieving relevant documents at question time and injecting them into the prompt.

## How RAG Works

Suppose the user asks:

```text
Which episode of One Piece had the hook hand guy?
```

The RAG pipeline works like this:

1. Embed the query using the same embedding model.
2. Search the vector database for the closest episode vectors.
3. Retrieve the matching episode synopses.
4. Inject those synopses into the LLM prompt as context.
5. Ask the LLM to answer based on the retrieved context.

The LLM is no longer answering only from memory. It is answering from the retrieved episode data.

## Why Not Fine-Tune Instead?

Fine-tuning bakes knowledge into the model weights permanently.

If the data changes, the model must be retrained. Fine-tuning can also require significant GPU time and compute. It can also cause catastrophic forgetting, where the model loses or distorts knowledge it previously had.

RAG does not modify the model. It only updates the vector database.

This makes RAG better for systems where the knowledge base changes often. We can add, update, or remove documents without retraining the model.

Fine-tuning is still useful for certain tasks, but it is not the right tool for every knowledge problem.

## Retrieval Quality Matters

The entire RAG system depends on retrieval quality.

If the embedding model does not understand that “hook hand guy” relates to episodes with Crocodile, the wrong documents will be retrieved. Then the LLM will answer using the wrong context.

This is why choosing a good embedding model matters. The LLM can only answer well if the retrieval step gives it useful evidence.

## Project Overview

In the practical section, we build a semantic search engine and RAG pipeline using the One Piece synopsis dataset.

The system should be able to take vague queries and search the vector database for relevant episodes.

The project has three main steps:

1. Embed the dataset.
2. Build semantic search.
3. Add RAG with an LLM.

## Step 1: Embedding the Dataset

The first script embeds the One Piece synopsis dataset.

We start by loading the synopsis data. Then we load the embedding model:

```python
all-MiniLM-L6-v2
```

This is a lightweight embedding model that works well for a small dataset.

The script first embeds a few sample sentences so we can inspect what embeddings look like. For example:

```text
Luffy fights a powerful enemy.
The crew discovers a new island.
A sad farewell between friends.
```

Each sentence is converted into a vector. The script prints the first few values of each vector so we can see that the text has been turned into numbers.

Then it calculates cosine similarity between the sample sentences.

A sentence compared with itself gets a score of 1.0. Different sentences get lower scores depending on how related they are.

After that, the full corpus is embedded. In this example, all 1,154 episode synopses are embedded in around two seconds.

The script then builds the FAISS index.

Before storing the vectors, it normalizes them so that inner product search is equivalent to cosine similarity. Then all 1,154 vectors are added to the index and saved for later use.

## Step 2: Semantic Search

The second script performs semantic search over the episode synopses.

It loads the saved embeddings and FAISS index from step 1. Then it defines a search function.

The search function does three things:

1. Embed the query.
2. Normalize the query vector.
3. Search the FAISS index for the closest vectors.

The sample queries include:

```text
The guy with the hook hand
Luffy gets a new crew member
Cooking competition
The crew gets separated
Underwater adventure
```

Because the search is semantic, it does not need exact keyword matches.

For example, the query “the crew gets separated” returns a result where Usopp splits the crew into two teams. The word “separated” may not appear, but the meaning is close.

Another example is:

```text
Episode about that big whale at the entrance of the Grand Line
```

The search retrieves results about Laboon, even though the query does not mention Laboon by name. This shows how semantic search can connect vague descriptions to relevant text.

## Keyword Search vs Semantic Search

The script also compares keyword search with semantic search.

For the query:

```text
The rubber man stretches to fight
```

A keyword search only looks for exact words like “rubber” or “stretches.” It may find results that mention those words, but not necessarily the best fighting-related episode.

Semantic search looks for the meaning of the query. It can retrieve episodes about Luffy fighting even if the exact words are different.

This is the main advantage of embeddings. They let us search by meaning instead of only by text overlap.

## Step 3: Building the RAG Pipeline

The third script adds a real language model to the retrieval system.

The model used is:

```text
Qwen 2.5 3B Instruct
```

The script loads the search components, loads the LLM, defines a search function, defines a generation function, and then defines the full RAG function.

The RAG function works by:

1. Searching for relevant episodes.
2. Building context from the retrieved synopses.
3. Sending the context and question to the LLM.
4. Generating an answer grounded in the retrieved data.

## Without RAG

First, the script asks the LLM a question without retrieval:

```text
Which episode does Captain Kuro appear in and what happens?
```

Without RAG, the model guesses from its training data.

It incorrectly says Captain Kuro is also known as Blackbeard and appears in episode 846. This is wrong. Blackbeard is a different character, and Captain Kuro appears much earlier.

This shows the problem with relying only on the model’s memory.

## With RAG

With RAG enabled, the system first retrieves relevant episode synopses from the vector database.

The retrieved context includes episode 12, where Captain Kuro appears.

Using that context, the LLM correctly answers that Captain Kuro appears in episode 12 and describes what happens in the synopsis.

This shows the value of RAG. The LLM is no longer guessing. It is answering from the data we provided.

## Results

The RAG system performs better than the model alone, but it is not perfect.

Some questions work well. For example, questions about Captain Kuro or Sanji cooking retrieve relevant episodes and produce useful answers.

Other questions are less successful. For example, the system struggles with the question about when Luffy first meets Zoro.

This could improve with better data, better chunking, a stronger embedding model, or better retrieval settings.

Even with a small dataset and a lightweight embedding model, the system demonstrates the basic pattern:

1. Embeddings find relevant documents.
2. The vector database retrieves them quickly.
3. The LLM turns the retrieved evidence into a natural language answer.

Together, these pieces create a question-answering system over custom data.

## Key Takeaways

Embeddings are vectors of numbers that represent meaning. Similar text produces similar vectors, which makes semantic search possible.

We have already seen embeddings inside transformer models as token vectors and hidden states. In this episode, we use models trained specifically to make the final vector useful.

Pooling collapses multiple token vectors into one sentence vector. Mean pooling is one of the most common methods.

Cosine similarity measures the angle between vectors and is the standard way to compare embeddings.

Vector databases like FAISS store and search embeddings efficiently. They make it possible to search large collections of vectors quickly.

RAG combines embeddings, vector search, and LLM generation. It retrieves relevant documents and feeds them to the model so the answer can be grounded in external data.

## Closing

This episode showed how embeddings can be used to build a semantic search engine and a RAG pipeline.

The One Piece example demonstrates the core idea: even vague natural language queries can retrieve relevant documents by meaning, not just by exact keywords.

In the next episode, the focus will shift to fine-tuning, where knowledge and behavior are baked more directly into the model weights.

Fine-tuning is a deeper topic with many methods and tradeoffs, so the next episode will start with the basics and foundations.
