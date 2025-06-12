python -m pip install --upgrade pip
pip install aiogram
pip install stegano
pip install cryptography

https://docs.aiogram.dev/en/latest/
@BotFather

https://pypi.org/project/aiosqlite/

pip install aiosqlite


async def create_tables():
    async with aiosqlite.connect("MyDB.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mytable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                info_data TEXT UNIQUE)""")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS table_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text_content TEXT)""")
        await db.commit()

async def add_to_db(username, tg_id):
    async with aiosqlite.connect("MyDB.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO mytable (name, info_data) VALUES (?, ?)",
            (username, tg_id)
        )
        await db.commit()
