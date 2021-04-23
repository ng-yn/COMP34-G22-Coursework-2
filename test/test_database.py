
def test_empty_db(client):
    """Start with a blank database."""
    c = client.get('/')
    assert b'No entries here so far' in c.data