"""
Contains database functions.
"""
import logging
import pathlib
import sqlite3

from bot.db_config import SCHEMA_VERSION
from bot.settings import DATABASE_URI

log = logging.getLogger(__name__)

try:
    conn = sqlite3.connect(DATABASE_URI)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
except sqlite3.OperationalError:
    log.error("Unable to open database")
    exit(1)


def init_db():
    """Initialize database tables migrations directory schema"""
    version = conn.execute("SELECT * FROM meta").fetchone()
    if version is not None:
        version = version["version"]
    else:
        version = 0
    if version > SCHEMA_VERSION:
        log.error(
            f"Database version {version} is newer than version {SCHEMA_VERSION} supported by this version. This bot does not support downgrading database versions. Please update."
        )
        exit()
    for v in range(0, SCHEMA_VERSION + 1):
        if version < v:
            log.info(f"Updating database to schema version {v}")
            with open(
                    f"{pathlib.Path().absolute()}/migrations/v{v}.sqlite", "r"
            ) as schema_file:
                schema = schema_file.read()
            conn.executescript(schema)
    conn.commit()
    log.info(f"Database initialized (Version {SCHEMA_VERSION})")
