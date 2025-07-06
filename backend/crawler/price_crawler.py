import asyncio
from .crawler import DangDangCrawler
from pathlib import Path
from config import INPUT_FILE


class PriceService:
    @staticmethod
    async def fetch_prices(isbn: str) -> float:
        """通过ISBN获取平均价格（与之前结果一致）"""
        # 写入ISBN到输入文件
        with open(INPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(isbn)

        # 运行爬虫
        crawler = DangDangCrawler()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, crawler.run)

        return crawler.get_processed_price()

    @staticmethod
    async def fetch_prices_by_title(title: str) -> float:
        """通过书名获取平均价格（与之前结果一致）"""
        # 写入书名到输入文件
        with open(INPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(title)

        # 运行爬虫
        crawler = DangDangCrawler()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, crawler.run)

        return crawler.get_processed_price()
