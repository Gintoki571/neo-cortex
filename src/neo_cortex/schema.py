"""Idempotent index setup for a tenant graph."""
DIM = 768

_VECTOR = [("Memory", "emb"), ("Chunk", "emb"), ("Entity", "emb")]
_RANGE = [(l, "id") for l in ("Memory", "Chunk", "Entity", "Document", "Session", "Agent", "Person")] + [
    ("Entity", "key"), ("Memory", "created_at"), ("Memory", "valid_from")]


def _run(graph, cypher):
    try:
        graph.query(cypher)
    except Exception as e:  # falkordb raises ResponseError; match on message only
        if "already indexed" not in str(e).lower():
            raise


def ensure_schema(graph) -> None:
    for label, prop in _VECTOR:
        _run(graph, f"CREATE VECTOR INDEX FOR (n:{label}) ON (n.{prop}) "
                    f"OPTIONS {{dimension:{DIM}, similarityFunction:'cosine'}}")
    _run(graph, "CREATE FULLTEXT INDEX FOR (n:Entity) ON (n.name)")
    for label, prop in _RANGE:
        _run(graph, f"CREATE INDEX FOR (n:{label}) ON (n.{prop})")
