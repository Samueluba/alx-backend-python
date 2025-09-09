import aiosqlite
import asyncio

DB_NAME = "users.db"

class ExecuteQuery:
    def __init__(self, query: str, params: tuple):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results = None

    async def __aenter__(self):
        self.connection = await aiosqlite.connect(DB_NAME)
        self.cursor = await self.connection.execute(self.query, self.params)
        self.results = await self.cursor.fetchall()
        return self.results

    async def __aexit__(self, exc_type, exc, tb):
        if self.cursor:
            await self.cursor.close()
        if self.connection:
            await self.connection.close()

# Example usage
async def main():
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    async with ExecuteQuery(query, params) as result:
        print("Users older than 25:")
        for row in result:
            print(row)

if __name__ == "__main__":
    asyncio.run(main())

