"""Guard: the suite must never touch the user's graph. Fails when the conftest isolation
fixture is removed, because a bare env means NEO_HOME ~/.neo-cortex, NEO_PORT 6390 (the
dogfood daemon's DB) and NEO_DAEMON_URL unset (cli.DEFAULT_URL, port 8765)."""
import os
from pathlib import Path

from neo_cortex import cli


def test_no_test_process_reaches_the_defaults():
    assert Path(os.environ["NEO_HOME"]).expanduser() != Path("~/.neo-cortex").expanduser()
    assert os.environ.get("NEO_PORT") != "6390"
    assert cli.daemon_url() != cli.DEFAULT_URL
