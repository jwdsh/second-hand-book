class PriceCrawler:
    @staticmethod
    async def fetch_prices(isbn: str) -> dict:
        """模拟价格爬虫"""
        return {
            "当当": 45.6,
            "京东": 52.3,
            "孔夫子": 38.9
        }