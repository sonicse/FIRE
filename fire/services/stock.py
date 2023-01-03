import yfinance as yf


class StockService:
    def __init__(self, http_client):
        self.http_client = http_client

    async def info(self, ticker: str):
        ticker_obj = yf.Ticker(ticker, self.http_client)
        return ticker_obj.info

    async def history(self, ticker: str, period: str, start: str, end: str):
        ticker_obj = yf.Ticker(ticker, self.http_client)
        end = None if not end else end
        return ticker_obj.history(period=period, start=start, end=end).to_dict()

    async def actions(self, ticker: str):
        ticker_obj = yf.Ticker(ticker, self.http_client)
        return ticker_obj.actions

    async def quarterly_financials(self, ticker: str):
        ticker_obj = yf.Ticker(ticker, self.http_client)
        return ticker_obj.quarterly_financials

    async def recommendations(self, ticker: str):
        ticker_obj = yf.Ticker(ticker, self.http_client)
        return ticker_obj.recommendations
