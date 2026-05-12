from psycopg2 import pool
from contextlib import contextmanager

_pool = None

def init_pool():
    global _pool
    if _pool is None:
        _pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=5,
            user="postgres",
            password="0000",
            host="localhost",
            database="Marzorati"
        )
        print("Pool criado!")

@contextmanager
def get_conn():
    global _pool
    if _pool is None:
        raise Exception("Pool não inicializado.")
    
    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)
