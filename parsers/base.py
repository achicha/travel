from abc import ABCMeta, abstractmethod


class BaseParser(metaclass=ABCMeta):
    
    @abstractmethod
    def _create_url(self, origin_airport, destination_airport, depart_start, depart_end):
        """Create link
        :return: url
        """
        pass
    
    @abstractmethod
    def _fetch(self, url):
        """
        Create response to the server
        :param url: links
        :return: fetched response
        """
        pass

    @abstractmethod
    def _parse_data(self, *args):
        pass

    def get_data(self, origin_airport, destination_airport, depart_start, depart_end, price):
        """
        Public method to download data

        :param origin_airport: airport of departure
        :param destination_airport: airport of arrival
        :param depart_start: date when your trip will starts
        :param depart_end: date when your trip will ends
        :param price: maximum ticket price
        :return: parsed data
        """
        url = self._create_url(origin_airport, destination_airport, depart_start, depart_end)
        resp = self._fetch(url)
        if resp.status_code == 200:
            data = self._parse_data(resp, origin_airport, destination_airport, price)
            return data
        else:
            return 'reason: {}, code: {}'.format(resp.reason, resp.status_code)

