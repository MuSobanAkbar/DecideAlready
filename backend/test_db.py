from types import SimpleNamespace

import db


class FakeQuery:
    """Pretends to be a Supabase query. Writes down every call, returns fixed rows."""

    def __init__(self, rows):
        self.rows = rows
        self.calls = []

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.calls.append((name, args))
            return self
        return record

    def execute(self):
        return SimpleNamespace(data=self.rows)


def use_fake(monkeypatch, rows):
    query = FakeQuery(rows)
    monkeypatch.setattr(db, "get_client", lambda: SimpleNamespace(table=lambda name: query))
    return query


def test_saved_ids_returns_a_set(monkeypatch):
    use_fake(monkeypatch, [{"tmdb_id": 27205}, {"tmdb_id": 155}])

    assert db.saved_tmdb_ids("user-1") == {27205, 155}

def test_saved_ids_only_reads_that_users_rows(monkeypatch):
    query = use_fake(monkeypatch, [])

    db.saved_tmdb_ids("user-1")

    assert ("eq", ("user_id", "user-1")) in query.calls