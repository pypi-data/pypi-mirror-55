import requests, json


class APIService():

    def __init__(self):
        self.authUrl = 'http://asweb-qa.payoda.com:83/api/'
        # self.authUrl = 'https://is.alternativesoft.com/api/'
        # self.apiUrl = 'https://api.alternativesoft.com/api/'
        self.apiUrl = 'http://asweb-qa.payoda.com:81/api/'
        self.loginParams = {
            "grant_type": "password",
            "client_id": "api",
            "client_secret": "secret",
            "scope": "as.web.api",
            "username": "hariprasad.k@payoda.com",
            "Password": "Alter@123"
        }
        self.assetParams = {
            "FundName": "JPMorgan Funds - Emerging Markets Strategic Bond Fund C (acc) - USD",
            "InfoFields": "Manager Name"
        }
        self.assetNameParams = {
            "id": "JPMorgan Funds - Emerging Markets Strategic Bond Fund C (acc) - USD",
            "idType": "asset name",
            "userID": 131
        }
        self.assetSearchParams = {
            "search": "Adi",
            "currentID": 0,
            "userID": 0
        }
        self.timeframeParams = {
            "assetName": "JPMorgan Funds - Emerging Markets Strategic Bond Fund C (acc) - USD",
            "assetSeriesType": "ROR",
            "seriesFrequency": "M",
            "startDate": "2017-06-01T10:14:20.055Z",
            "endDate": "2019-08-30T10:14:20.055Z",
            "userID": 1
        }
        self.statisticParams = {
            "assetName": "Aditya Birla Sun Life Equity Fund Growth",
            "statisticName": "",
            "benchmark1": "Aditya Birla Sun Life Index Fund Growth",
            "benchmark2": "Aditya Birla Sun Life Index Fund Growth",
            "riskFree": "",
            "seriesFrequency": "M",
            "statisticStartDate": "1998-09-30T00:00:00Z",
            "statisticEndDate": "2019-04-30T00:00:00Z",
            "userID": 0,
            "dateRangeRequired": "true"
        }
        self.assetStatisticVectorParams = {
            "assetName": "Aditya Birla Sun Life Equity Fund Growth",
            "statisticName": "",
            "benchmark1": "Aditya Birla Sun Life Index Fund Growth",
            "benchmark2": "Aditya Birla Sun Life Index Fund Growth",
            "riskFree": "",
            "seriesFrequency": "M",
            "statisticStartDate": "2019-10-29T07:54:21.783Z",
            "statisticEndDate": "2019-10-29T07:54:21.783Z",
            "userID": 0,
            "dateRangeRequired": "true"
        }
        self.statsListParams = {
            "asInfoFieldRequest": "true"
        }
        self.assetDetailsVectorParams = {
            "assetName": "Aditya Birla Sun Life Equity Fund Growth",
            "statName": "",
            "userID": 0
        }
        self.assetRORVectorParams = {
            "assetName": "Aditya Birla Sun Life Equity Fund Growth",
            "seriesFrequency": "M",
            "startDate": "2019-10-29T09:24:39.398Z",
            "endDate": "2019-10-29T09:24:39.398Z",
            "userID": 0
        }
        self.assetUnderwaterVectorParams = {
            "AssetName": "Aditya Birla Sun Life Equity Fund Growth",
            "BenchmarkNames": "null",
            "Statistics": 0, "Percentiles": [0.01, 0.05, 0.5, 0.95],
            "AreaGraphDrawdownCount": 5,
            "StartDate": "1998-09-30T00:00:00Z",
            "EndDate": "2019-04-30T00:00:00Z"
        }
        self.assetRollingStatisticVectorParams = {
            "AssetName": "Aditya Birla Sun Life Equity Fund Growth",
            "BenchmarkNames": "null",
            "StartDate": "1998-09-30T00:00:00Z",
            "EndDate": "2019-04-30T00:00:00Z",
            "Statistics": "null",
            "RollingWindowLength": 0,
            "StatisticsName": "RollingSharpeRatio",
            "SeriesFrequency": "M",
            "RollingWindow": 40,
            "Benchmark1": "Aditya Birla Sun Life Index Fund Growth",
            "Benchmark2": "Aditya Birla Sun Life Index Fund Growth",
            "userID": 0
        }

    def login(self):
        """
        Login Url for Signing in
        """
        loginUrl = self.authUrl + 'account/signin'
        print("URL :" + loginUrl)
        loginResponse = requests.post(loginUrl, json=self.loginParams)
        return loginResponse

    def token(self):
        """
        Token URL if the user is already logged in
        """
        tokenUrl = self.authUrl + 'Account/resetToken'
        print("URL :" + tokenUrl)
        tokenResponse = requests.post(tokenUrl, json=self.loginParams)
        return tokenResponse

    def getAsset(self, token):
        """
        Get Asset
        """
        assetUrl = self.apiUrl + 'ExcelAPI/ASAssetInfo'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + assetUrl)
        AssetResponse = requests.post(assetUrl, json=self.assetParams, headers=headers)
        print(type(AssetResponse))
        return AssetResponse

    def getAssetName(self, token):
        """
        Get Asset Name
        """
        assetNameUrl = self.apiUrl + 'ExcelAPI/AsGetAssetName'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + assetNameUrl)
        AssetNameResponse = requests.post(assetNameUrl, json=self.assetNameParams, headers=headers)
        print(type(AssetNameResponse))
        return AssetNameResponse

    def getAssetSearch(self, token):
        """
        Get Asset by Searching

        """
        AUrl = self.apiUrl + 'ExcelAPI/AssetSearch'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + AUrl)
        AssetSearchResponse = requests.post(AUrl, json=self.assetSearchParams, headers=headers)
        print(type(AssetSearchResponse))
        return AssetSearchResponse

    def getTimeSeries(self, token):  # response
        """
        Get Timeseries
        """
        TSUrl = self.apiUrl + 'ExcelAPI/ASAssetTSVector'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + TSUrl)
        TimeframeResponse = requests.post(TSUrl, json=self.timeframeParams, headers=headers)
        print(type(TimeframeResponse))
        return TimeframeResponse

    def getAssetStatistics(self, token):
        """
        Get Statistics
        """
        ASUrl = self.apiUrl + 'ExcelAPI/ASAssetStatistic'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + ASUrl)
        AssetStatisticsResponse = requests.post(ASUrl, json=self.statisticParams, headers=headers)
        print(type(AssetStatisticsResponse))
        return AssetStatisticsResponse

    def getAssetStatisticVector(self, token):  # response
        """
        Get Asset Statistics Vector
        """
        ASVUrl = self.apiUrl + 'ExcelAPI/ASAssetStatisticVector'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + ASVUrl)
        AssetStatisticVectorResponse = requests.post(ASVUrl, json=self.assetStatisticVectorParams, headers=headers)
        print(type(AssetStatisticVectorResponse))
        return AssetStatisticVectorResponse

    def getStatsList(self, token):  # response
        """
        Get Statistics name list
        """
        SLUrl = self.apiUrl + 'ExcelAPI/AsGetInfoFields'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + SLUrl)
        StatsListResponse = requests.post(SLUrl, json=self.statsListParams, headers=headers)
        print(type(StatsListResponse))
        return StatsListResponse

    def getAssetDetailsVector(self, token):
        """
        Get Asset Detail Vector
        """
        ADVUrl = self.apiUrl + 'ExcelAPI/ASAssetDetailsVector'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + ADVUrl)
        AssetDetailsVectorResponse = requests.post(ADVUrl, json=self.assetDetailsVectorParams, headers=headers)
        print(type(AssetDetailsVectorResponse))
        return AssetDetailsVectorResponse

    def getAssetCumulativeRORVector(self, token):
        """
        Get AssetCumulativeRORVector
        """
        RORUrl = self.apiUrl + 'ExcelAPI/ASAssetCumulativeRORVector'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + RORUrl)
        AssetCumulativeRORVectorResponse = requests.post(RORUrl, json=self.assetRORVectorParams, headers=headers)
        print(type(AssetCumulativeRORVectorResponse))
        return AssetCumulativeRORVectorResponse

    def getAssetUnderwaterVector(self, token):
        """
        Get AssetUnderwaterVector
        """
        UWUrl = self.apiUrl + 'ExcelAPI/ASAssetUnderwaterVector'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + UWUrl)
        AssetUnderwaterVectorResponse = requests.post(UWUrl, json=self.assetUnderwaterVectorParams, headers=headers)
        print(type(AssetUnderwaterVectorResponse))
        return AssetUnderwaterVectorResponse

    def getAssetRollingStatisticVector(self, token):
        """
        Get AssetRollingStatisticVector
        """
        UWUrl = self.apiUrl + 'ExcelAPI/ASAssetRollingStatisticVector'
        headers = {
            'authorization': 'Bearer ' + token
        }
        print("URL :" + UWUrl)
        AssetUnderwaterVectorResponse = requests.post(UWUrl, json=self.assetRollingStatisticVectorParams,
                                                      headers=headers)
        print(type(AssetUnderwaterVectorResponse))
        return AssetUnderwaterVectorResponse


Service = APIService()
loginResponse = Service.login()
if loginResponse.status_code == 200:
    loginData = json.loads(loginResponse.content)
    if loginData['token'] == None:
        print("====================token=========================")
        tokenResponse = Service.token()
        if tokenResponse.status_code == 200:
            tokenData = json.loads(tokenResponse.content)
            print(type(tokenData))
            print(tokenData)
            print("==========================================================")
            if tokenData['token'] is not None:
                print("====================Asset=========================")
                AssetResponse = Service.getAsset(tokenData['token'])
                if tokenResponse.status_code == 200:
                    AssetData = json.loads(AssetResponse.content)
                    print(type(AssetData))
                    print(AssetData)
                    print("==========================================================")
                else:
                    print("====================Error in Asset =========================")

                print("====================AssetName=========================")
                AssetNameResponse = Service.getAssetName(tokenData['token'])
                if AssetNameResponse.status_code == 200:
                    AssetNameData = json.loads(AssetNameResponse.content)
                    print(type(AssetNameData))
                    print(AssetNameData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetName =========================")

                print("====================AssetSearch=========================")
                AssetSearchResponse = Service.getAssetSearch(tokenData['token'])
                if AssetSearchResponse.status_code == 200:
                    AssetSearchData = json.loads(AssetSearchResponse.content)
                    print(type(AssetSearchData))
                    print(AssetSearchData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetSearch =========================")

                print("====================TimeSeries=========================")
                TimeSeriesResponse = Service.getTimeSeries(tokenData['token'])
                if TimeSeriesResponse.status_code == 200:
                    TimeseriesData = json.loads(TimeSeriesResponse.content)
                    print(TimeseriesData)
                    print("==========================================================")
                else:
                    print("====================Error in Timeseries =========================")

                print("====================AssetStatictics=========================")
                AssetStatisticsResponse = Service.getAssetStatistics(tokenData['token'])
                if AssetStatisticsResponse.status_code == 200:
                    AssetStatisticsData = json.loads(AssetStatisticsResponse.content)
                    print(type(AssetData))
                    print(AssetStatisticsData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetStatistics =========================")

                print("====================AssetStatisticVector=========================")
                AssetStatisticVectorResponse = Service.getAssetStatisticVector(tokenData['token'])
                if AssetStatisticVectorResponse.status_code == 200:
                    AssetStatisticVectorData = json.loads(AssetStatisticVectorResponse.content)
                    print(type(AssetStatisticVectorData))
                    print(AssetStatisticVectorData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetStatisticVector =========================")

                print("====================StatsList=========================")
                StatsListResponse = Service.getStatsList(tokenData['token'])
                if StatsListResponse.status_code == 200:
                    StatsListData = json.loads(StatsListResponse.content)
                    print(type(StatsListData))
                    print(StatsListData)
                    print("==========================================================")
                else:
                    print("====================Error in StatisList =========================")

                print("====================AssetDetailsVector=========================")
                AssetDetailsVectorResponse = Service.getAssetDetailsVector(tokenData['token'])
                if AssetDetailsVectorResponse.status_code == 200:
                    AssetDetailsVectorData = json.loads(AssetDetailsVectorResponse.content)
                    print(type(AssetDetailsVectorData))
                    print(AssetDetailsVectorData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetDetailsVector =========================")

                print("====================ASAssetCumulativeRORVector=========================")
                AssetCumulativeRORVectorResponse = Service.getAssetCumulativeRORVector(tokenData['token'])
                if AssetCumulativeRORVectorResponse.status_code == 200:
                    AssetCumulativeRORVectorData = json.loads(AssetCumulativeRORVectorResponse.content)
                    print(type(AssetCumulativeRORVectorData))
                    print(AssetCumulativeRORVectorData)
                    print("==========================================================")
                else:
                    print("====================Error in ASAssetCumulativeRORVector =========================")

                print("====================AssetUnderwaterVector=========================")
                AssetUnderwaterVectorResponse = Service.getAssetUnderwaterVector(tokenData['token'])
                if AssetUnderwaterVectorResponse.status_code == 200:
                    AssetUnderwaterVectorData = json.loads(AssetUnderwaterVectorResponse.content)
                    print(type(AssetUnderwaterVectorData))
                    print(AssetUnderwaterVectorData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetUnderwaterVector =========================")

                print("====================AssetRollingStatisticVector=========================")
                AssetRollingStatisticVectorResponse = Service.getAssetRollingStatisticVector(tokenData['token'])
                if AssetRollingStatisticVectorResponse.status_code == 200:
                    AssetRollingStatisticVectorData = json.loads(AssetRollingStatisticVectorResponse.content)
                    print(type(AssetRollingStatisticVectorData))
                    print(AssetRollingStatisticVectorData)
                    print("==========================================================")
                else:
                    print("====================Error in AssetRollingStatisticVector =========================")

        else:
            print("====================Error in Token=========================")
else:
    print("====================Error in Login=========================")