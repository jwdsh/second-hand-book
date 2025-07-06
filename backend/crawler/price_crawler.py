class PriceCrawler:
    @staticmethod
    async def fetch_prices(isbn: str) -> dict:
        """获取当当网价格"""
        # 目前只支持当当网价格获取
        # 可以根据需要扩展其他平台
        return {
            "当当": 45.6
        }