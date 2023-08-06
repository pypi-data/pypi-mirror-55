import requests
from bs4 import BeautifulSoup


class MF_House:
    url = None
    headers = None
    house_code = {}

    def __init__(self):

        # print("Setting Up -> url,header")
        self.url = "https://www.amfiindia.com/modules/LoadModules/navreports"
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'www.amfiindia.com',
            'Referer': 'https://www.amfiindia.com/net-asset-value'
        }

        api_res = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(api_res.text, 'html.parser')

        house_tag = soup.find_all('option')

        # removing zero valued options
        for tag in soup.find_all('option', {"value": ""}):
            # print(tag)
            house_tag.remove(tag)

        for house in house_tag:
            # print(house)
            self.house_code[house.text.upper()] = house['value']

        # print(self.house_code)

    def getHouseCode(self, house):
        return self.house_code[house.upper()]

    def getAllHouseCodes(self):
        return self.house_code


if __name__ == '__main__':
    print("Inside main function of MF_House.py")
    house = MF_House()
    # print(house.getHouseCode("L&T MUTUAL FUND"))
    print(house.getAllHouseCodes())
