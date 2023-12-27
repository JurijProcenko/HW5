import aiohttp
import asyncio
import platform
import sys
import datetime


class Connect_To:
    def __init__(self, url: str):
        self.url = url

    async def get_data(self, day: datetime):
        result = {}
        day = day.strftime("%d.%m.%Y")
        session = aiohttp.ClientSession()
        try:
            response = await session.get(self.url + day)
            if response.status == 200:
                temp = await response.json()
                result[str(day)] = {}
                exchange_list = temp["exchangeRate"]
                for currency in exchange_list:
                    if currency["currency"] in ("USD", "EUR"):
                        result[str(day)][currency["currency"]] = {
                            "sale": f'{currency["saleRate"]:0.2f}',
                            "purchase": f'{currency["purchaseRate"]:0.2f}',
                        }

        except aiohttp.ClientConnectorError as err:
            result = f"Connection error: {url}, {err}"
        finally:
            response.close()
        await session.close()
        return result


now = datetime.datetime.now()
url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date="
# url += now.strftime("%d.%m.%Y")


def form_date(i: int) -> datetime:
    return now - datetime.timedelta(days=i)


async def main(days: int):
    connect = Connect_To(url)
    exchanges = []
    for i in range(days):
        result = await connect.get_data(form_date(i))
        if isinstance(result, dict):
            exchanges.append(result)
        else:
            print(result)
    for date in exchanges:
        print(date)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        try:
            days = int(sys.argv[1])
            if days < 0 or days > 10:
                days = 1
                print("Number of day must be in range [1..10]")
            asyncio.run(main(days))

        except:
            print("Number of day must be digits")
