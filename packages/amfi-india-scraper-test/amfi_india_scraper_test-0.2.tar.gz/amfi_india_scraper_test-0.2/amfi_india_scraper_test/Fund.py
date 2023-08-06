import requests
from bs4 import BeautifulSoup
from MF_House import MF_House

class Fund:
    house = None
    url = None
    # headers =

    def __init__(self):
        self.house = MF_House()
        self.url = 'https://www.amfiindia.com/modules/NAVList'

        # print(self.house.getAllHouseCodes())

    def extractDetailsFromTable(self, content):
        details = []
        soup = BeautifulSoup(content, 'html.parser')
        table_rows = soup.find_all("tr")
        # print(data_tags)
        for item in table_rows:
            row_data = item.find_all("td")
            if(len(row_data) == 5):
                record = {}
                record["fund_name"] = row_data[0].text
                record["isin"] = row_data[1].text
                record["isin_reinvest"] = row_data[2].text
                record["value"] = row_data[3].text
                record["date"] = row_data[4].text
                details.append(record)

        # print(details)

        return details

    def getFundDetails(self, house=""):

        code = self.house.getHouseCode(house.upper())

        payload = {
            'MFName': code,
            'OpenScheme': '',
            'CloseScheme': '',
            'IntervalFund': ''
        }

        api_res = requests.post(
            self.url,
            data=payload)

        fund_details = self.extractDetailsFromTable(api_res.text)
        return fund_details

if __name__ == '__main__':
    f = Fund()
    hsbc_fund = f.getFundDetails(house="HSBC Mutual Fund")
