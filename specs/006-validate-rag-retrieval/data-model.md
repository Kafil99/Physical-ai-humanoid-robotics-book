# Data Model: RAG Retrieval Validation

This feature does not define new data models to be stored. Instead, it documents the structure of the data it expects to **retrieve** from the Qdrant vector database. The data is based on the `ContentChunk` entity defined in the `005-rag-content-pipeline` feature.

## Retrieved Entity: `ScoredPoint`

The `qdrant_client.search()` method returns a list of `ScoredPoint` objects. Each `ScoredPoint` contains the information about a retrieved document.

### Fields

| Field Name     | Data Type             | Description                                                                                             | Example                                             |
|----------------|-----------------------|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `id`           | `UUID` (string)       | The unique identifier of the point in Qdrant.                                                           | `"a1b2c3d4-e5f6-7890-1234-567890abcdef"`              |
| `version`      | `integer`             | The version of the point.                                                                               | `1`                                                 |
| `score`        | `float`               | The similarity score between the query vector and the retrieved point's vector.                         | `0.87345`                                           |
| `payload`      | `dict`                | A dictionary containing the metadata associated with the vector.                                        | `{'text': '...', 'source_url': '...', 'chunk_index': 0}` |
| `vector`       | `list[float]` or `None`| The vector of the point. This is only returned if requested.                                            | `[0.123, -0.456, ...]`                              |

### Payload Structure

The `payload` dictionary within the `ScoredPoint` is expected to have the following structure, matching the data that was ingested.

| Payload Key    | Data Type  | Description                                        |
|----------------|------------|----------------------------------------------------|
| `text`         | `string`   | The raw text content of the original chunk.        |
| `source_url`   | `string`   | The URL of the page from which the chunk was extracted. |
| `chunk_index`  | `integer`  | The sequential index of the chunk within its page. |
