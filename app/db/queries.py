class UserQueries:
    JOURNAL_MODE = "PRAGMA journal_mode=WAL;"
    
    CREATE_TABLE = """
            CREATE TABLE IF NOT EXISTS users(
            id TEXT PRIMARY KEY NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """

    REGISTER_USER = """
                INSERT INTO users(
                id, 
                username, 
                email, 
                password_hash) 
                VALUES (?, ?, ?, ?);
            """

    GET_ID = """
                SELECT id
                FROM users
                WHERE email = ?;
            """
    VERIFY_ID = """
                SELECT id
                FROM users
                WHERE id = ?;
            """

    GET_HASH = """
                SELECT password_hash
                FROM users
                WHERE email = ?;
            """

