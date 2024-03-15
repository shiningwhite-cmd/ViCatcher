import asyncio
from Action.SearchInWiki import WikiSearchAndSummarize

async def main():
    wiki = WikiSearchAndSummarize()
    rsp = await wiki.run("Beatles", "Beatles")
    print(rsp)

if __name__ == "__main__":
    asyncio.run(main())
