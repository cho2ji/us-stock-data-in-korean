"""This module handles logic of choosing which stock exchange to search."""
from datetime import datetime
import pandas as pd
from typing import Optional
from financialdatapy.cik import CikList
from financialdatapy.exception import NotAvailable
from financialdatapy.usfinancials import UsFinancials
from financialdatapy.korfinancials import KorFinancials
from financialdatapy.price import UsMarket
from financialdatapy.price import KorMarket


class Market:
    """This class represents a stock exchange.

    :param country_code: Country where the stock is listed.
    :type country_code: str
    """

    def __init__(self, country_code: str):
        """Initialize Market."""
        self.country_code = country_code.upper()

    def financial_statement(
                self,
                symbol: str,
                financial: str,
                period: str,
                web: bool,
                type_of_financial: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get financial statements.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param financial: Which financial statement to retrieve.
        :type financial: str
        :param period: Either 'annual' or 'quarter.
        :type period: str
        :param web: Option for opening filings in a web browser.
        :type web: bool
        :param type_of_financial: Pass 'standard' for the method to return
            standard financials. If empty, finanicials as reported will be
            returned, defaults to None.
        :type type_of_financial: Optional[str], optional
        :raises NotAvailable: If the symbol is not listed in the
            stock exchange.
        :return: Either financials as reported or standard financials.
        :rtype: pandas.DataFrame
        """
        if self.country_code == 'USA':
            cik_list = CikList()
            comp_cik = cik_list.search_cik(symbol)
            market = UsFinancials(symbol, comp_cik, financial, period)

            if type_of_financial == 'standard':
                return market.get_standard_financials()

            if not web:
                return market.get_financials()
            market.open_report()
        elif self.country_code == 'KOR':
            market = KorFinancials(symbol, financial, period)

            if type_of_financial == 'standard':
                return market.get_standard_financials()

            if not web:
                return market.get_financials()
            market.open_report()
        else:
            raise NotAvailable()

    def historical_price(self, symbol: str,
                         start: datetime, end: datetime) -> pd.DataFrame:
        """Get historical stock price data.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param start: Start date to query.
        :type start: `datetime.datetime`
        :param end: End date to query.
        :type end: `datetime.datetime`
        :raises NotAvailable: If the symbol is not listed in the
            stock exchange.
        :return: Historical stock price data.
        :rtype: pandas.DataFrame
        """
        if self.country_code == 'USA':
            return UsMarket(symbol, start, end)
        elif self.country_code == 'KOR':
            return KorMarket(symbol, start, end)
        else:
            raise NotAvailable()
