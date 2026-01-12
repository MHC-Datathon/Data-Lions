import urllib.parse
import pandas as pd
from typing import Literal


class SOQL_Querying:
    """
    A helper class to construct SOQL query URLs for New York Open Data APIs.

    Attributes
    ----------
    routes_url : str
        The base URL for the MTA routes dataset.
    violations_url : str
        The base URL for the traffic violations dataset.
    ridership_url : str
        The base URL for the transit ridership dataset.
    """

    def __init__(self):
        """
        Initialize the SOQL_Querying class with predefined resource URLs.
        """
        self.routes_url = "https://data.ny.gov/resource/ki2b-sg5y.csv"
        self.violations_url = "https://data.ny.gov/resource/kh8p-hcbm.csv"
        self.ridership_url = "https://data.ny.gov/resource/kv7t-n8in.csv"
        self.ridership_2025_url = "https://data.ny.gov/resource/gxb3-akrn.csv"

    def clean(self, query: str):
        """
        Remove newlines from a query string and URL-encode the result.

        Parameters
        ----------
        query : str
            The raw SOQL query string, potentially containing newlines.

        Returns
        -------
        str
            A URL-encoded version of the cleaned query string.
        """
        while "\n" in query:
            query = query.replace("\n", " ")
        parsed_query = urllib.parse.quote(query)

        return parsed_query

    def query(
        self,
        api: Literal["routes", "violations", "ridership", "ridership-2025"],
        query: str,
    ):
        """
        Construct a full API request URL based on the selected dataset.

        Parameters
        ----------
        api : str
            The identifier for the target dataset ('routes', 'violations', 'ridership', or 'ridership-2025').
        query : str
            The SOQL query logic to be appended to the URL.

        Returns
        -------
        str or None
            The complete URL for the CSV request, or None if the API selection is invalid.
        """
        encoded_query = self.clean(query)
        choice = api.strip().lower()
        prefix = "?$query="
        if choice == "routes":
            return self.routes_url + prefix + encoded_query
        if choice == "violations":
            return self.violations_url + prefix + encoded_query
        if choice == "ridership":
            return self.ridership_url + prefix + encoded_query
        if choice == "ridership-2025":
            return self.ridership_2025_url + prefix + encoded_query
        else:
            print("INVALID API SELECTED!")

    def pipeline(
        self,
        api: Literal["routes", "violations", "ridership", "ridership-2025"],
        query: str,
    ):
        response = self.query(api=api, query=query)
        df = pd.read_csv(response)  # type: ignore
        return df
