class PricingStrategy:
    @staticmethod
    def calculate_price(prices: dict, score: float) -> float:
        """定价策略"""
        avg_price = sum(prices.values()) / len(prices)
        return round(avg_price * score, 2)