import requests

class Dengue():

    def __init__(self):
        self.base_url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports"
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "X-PowerBI-ResourceKey": "c429283b-e400-4888-bb54-87939c5b3c87",
        }

    def dados(self, estado: str = None, ano: str = '2024'):
        
        url = self.base_url + "/querydata?synchronous=true"

        payload = {
            "version": "1.0.0",
            "queries": [
                {
                    "Query": {
                        "Commands": [
                            {
                                "SemanticQueryDataShapeCommand": {
                                    "Query": {
                                        "Version": 2,
                                        "From": [
                                            {"Name": "e", "Entity": "iMEDIDAS", "Type": 0},
                                            {"Name": "d", "Entity": "dEVOLUCAO", "Type": 0},
                                            {"Name": "f", "Entity": "fBD_DENV_CHIKV_ZIKV_FULL", "Type": 0},
                                            {"Name": "d1", "Entity": "dANO_SE_SINTOMAS", "Type": 0},
                                            {"Name": "d2", "Entity": "dMUNICIPIO", "Type": 0}
                                        ],
                                        "Select": [
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Casos prováveis de Dengue"}},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Óbitos em investigação - DENV"}},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Óbitos por Dengue"}},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Incidência (DENV)"}},
                                        ],
                                        "Where": [
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "CRITERIO"}}],"Values": [[{"Literal": {"Value": "1D"}}],[{"Literal": {"Value": "2D"}}],[{"Literal": {"Value": "3D"}}],[{"Literal": {"Value": "0D"}}]]}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d1"}}, "Property": "SINTOMAS_ANO"}}],"Values": [[{"Literal": {"Value": f"{ano}L"}}]]}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "ID_AGRAVO"}}],"Values": [[{"Literal": {"Value": "'A90'"}}]]}}},
                                        ],
                                    },
                                }
                            }
                        ]
                    }
                }
            ],
            "modelId": 3127714
        }
        
        if estado:
            select = {"Column": {"Expression":  {"SourceRef": {"Source": "d2"}}, "Property": "UF_NOME"}}
            where = {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d2"}}, "Property": "UF_PARSED"}}],"Values": [[{"Literal": {"Value": f"'{estado}'"}}]]}}}
            payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Select'].append(select)
            payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Where'].append(where)

        response = requests.post(url = url, headers = self.headers, json = payload)

        data = response.json()['results'][0]['result']['data']['dsr']['DS'][0]['PH']

        return data[1]['DM1'][0]['C'] if estado else data[0]['DM0'][0]['C']

    def custom_query(self, query_shape: str):

        url = self.base_url + "/querydata?synchronous=true"

        payload = {
            "version": "1.0.0",
            "queries": [
                {
                    "Query": {
                        "Commands": [
                            {
                                "SemanticQueryDataShapeCommand": query_shape
                            }
                        ]
                    }
                }
            ],
            "modelId": 3127714
        }

        response = requests.post(url = url, headers = self.headers, json = payload)

        return response.json()['results'][0]['result']['data']['dsr']['DS']

    def database_schema(self):

        url = self.base_url + "/conceptualschema"

        payload = {"modelIds":[3127714]}

        response = requests.post(url = url, headers = self.headers, json = payload)

        return response.json()['schemas'][0]['schema']['Entities']
    
if __name__ == "__main__":
    pass