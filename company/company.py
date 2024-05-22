import math

import aiohttp
import pandas
from aiohttp import ClientSession
from pydantic import BaseModel
from settings import Settings, get_settings
from utils import create_ssl_context


class Company(BaseModel):
    balance: dict | None
    settings: Settings = get_settings()

    def get_z2_altman_score(self, year: str) -> float:
        liabilities = self.__get_liabilities__(year)
        loan_capital = self.__get_loan_capital__(year)
        current_liquidity = self.__get_liquidity__().get('CL').get(year)

        return round(-0.3877 - 1.0736 * float(current_liquidity) + 0.579 * (loan_capital / liabilities), 2)

    def get_z4_altman_score(self, year: str) -> float:
        x1, x2, x3, x4 = (
            self.__get_x1_for_z4z5_altman__(year),
            self.__get_x2_for_z4z5_altman__(year),
            self.__get_x3_for_z4z5_altman__(year),
            self.__get_x4_for_z4z5_altman__(year)
        )

        return round(6.56*x1+3.26*x2+6.72*x3+1.05*x4, 2)

    def get_z5_altman_score(self, year: str) -> float:
        x1, x2, x3, x4, x5 = (
            self.__get_x1_for_z4z5_altman__(year),
            self.__get_x2_for_z4z5_altman__(year),
            self.__get_x3_for_z4z5_altman__(year),
            self.__get_x4_for_z4z5_altman__(year),
            self.__get_x5_for_z5_altman__(year)
        )

        return round(0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.42 * x4 + 0.998 * x5, 2)

    def get_fulmer_score(self, year: str) -> float:
        x1, x2, x3, x4, x5, x6, x7, x8, x9 = (
            self.__get_x1_for_fulmer__(year),
            self.__get_x2_for_fulmer__(year),
            self.__get_x3_for_fulmer__(year),
            self.__get_x4_for_fulmer__(year),
            self.__get_x5_for_fulmer__(year),
            self.__get_x6_for_fulmer__(year),
            self.__get_x7_for_fulmer__(year),
            self.__get_x8_for_fulmer__(year),
            self.__get_x9_for_fulmer__(year)
        )

        return round(
            5.528 * x1 + 0.212 * x2 + 0.073 * x3
            + 1.27 * x4 - 0.12 * x5 + 2.335 * x6 + 0.575 * x7 + 1.083 * x8 - 6.075 + 0.894*x9,
            2)

    def get_balance(self):
        return self.balance

    async def __call__(self):
        await self.__fill_balance__()

    async def __fill_balance__(self, settings: Settings = get_settings()):
        session_client = ClientSession(
            base_url=settings.fns_api_url,
            raise_for_status=False,
            connector=aiohttp.TCPConnector(ssl=create_ssl_context(
                cert_str=settings.cert,
                key_str=settings.key)
            )
        )

        response = await session_client.get(url='/api/bo', params={'req': self.settings.company_inn,
                                                                   'key': settings.token})

        balance = await response.json()
        self.balance = balance.get(self.settings.company_inn)

        await session_client.close()

    def __get_liquidity__(self) -> dict:
        df = pandas.read_csv(self.settings.liquidity_file, index_col='Ratio')
        return {
            'AL': df.loc['AL'].to_dict(),
            'CL': df.loc['CL'].to_dict(),
            'FL': df.loc['FL'].to_dict()
        }

    def __get_liabilities__(self, year: str) -> int:
        balance = self.balance.get(year)
        liabilities = (int(balance.get('1300'))
                       + int(balance.get('1410'))
                       + int(balance.get('1510') or 0)
                       + int(balance.get('1520')))

        return liabilities

    def __get_loan_capital__(self, year: str) -> int:
        balance = self.balance.get(year)
        loan_capital = (int(balance.get('1410'))
                        + int(balance.get('1510') or 0)
                        + int(balance.get('1520')))

        return loan_capital

    def __get_x1_for_z4z5_altman__(self, year: str) -> float:
        balance = self.balance.get(year)
        x1 = ((int(balance.get('1210') or 0)
               + int(balance.get('1230'))
               + int(balance.get('1250'))
               - int(balance.get('1510') or 0)
               - int(balance.get('1520')))) / int(balance.get('1600'))

        return x1

    def __get_x2_for_z4z5_altman__(self, year: str) -> float:
        balance = self.balance.get(year)
        x2 = int(balance.get('2400')) / int(balance.get('1600'))

        return x2

    def __get_x3_for_z4z5_altman__(self, year: str) -> float:
        balance = self.balance.get(year)
        x3 = ((int(balance.get('2400')) +
               int(balance.get('2410'))) /
              int(balance.get('1600')))

        return x3

    def __get_x4_for_z4z5_altman__(self, year: str) -> float:
        balance = self.balance.get(year)
        x4 = int(balance.get('1300')) / self.__get_loan_capital__(year)

        return x4

    def __get_x5_for_z5_altman__(self, year: str) -> float:
        balance = self.balance.get(year)
        x5 = int(balance.get('2110')) / int(balance.get('1600'))

        return x5

    def __get_x1_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x1 = int(balance.get('1300')) / int(balance.get('1600'))

        return x1

    def __get_x2_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x2 = int(balance.get('2110')) / int(balance.get('1600'))

        return x2

    def __get_x3_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x3 = ((int(balance.get('2400'))
               + int(balance.get('2410')))
              / int(balance.get('1300')))

        return x3

    def __get_x4_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x4 = int(balance.get('2400')) / self.__get_loan_capital__(year)

        return x4

    def __get_x5_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x5 = int(balance.get('1410')) / int(balance.get('1600'))

        return x5

    def __get_x6_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x6 = int(balance.get('1510') or 0) / int(balance.get('1600'))

        return x6

    def __get_x7_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)

        other_current_assets = 0
        match year:
            case '2020':
                other_current_assets = 4791
            case '2021':
                other_current_assets = 4583
            case '2022':
                other_current_assets = 0

        x7 = (int(balance.get('1600')) -
              int(balance.get('1150')) -
              int(balance.get('1210') or 0) -
              other_current_assets)

        return math.log10(x7) if x7 > 0 else 0

    def __get_x8_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x8 = ((int(balance.get('1210') or 0)
               + int(balance.get('1230'))
               + int(balance.get('1250'))
               - int(balance.get('1510') or 0)
               - int(balance.get('1520')))) / self.__get_loan_capital__(year)

        return x8

    def __get_x9_for_fulmer__(self, year: str) -> float:
        balance = self.balance.get(year)
        x9 = (int(balance.get('2400'))
              + int(balance.get('2410'))
              + int(balance.get('2350'))) / int(balance.get('2350'))

        return math.log10(x9) if x9 > 0 else 0
