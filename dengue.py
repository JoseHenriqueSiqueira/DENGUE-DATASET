import requests

class Dengue():

    def __init__(self):
        self.base_url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports"

        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "X-PowerBI-ResourceKey": "c429283b-e400-4888-bb54-87939c5b3c87",
        }
        
    def casos(self, estado:str = None):

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
                                            {"Name": "d", "Entity": "dMUNICIPIO", "Type": 0},
                                            {"Name": "d1", "Entity": "dANO_SE_SINTOMAS", "Type": 0},
                                            {"Name": "f", "Entity": "fBD_DENV_CHIKV_ZIKV_FULL", "Type": 0}
                                        ],
                                        "Select": [
                                            {"Column": {"Expression": {"SourceRef": {"Source": "d"}},"Property": "UF_NOME"},"Name": "dMUNICIPIO.UF_NOME","NativeReferenceName": "Unidade Federada1"},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}},"Property": "Incidência (DENV)"},"Name": "iMEDIDAS.Incidência SE > 202226","NativeReferenceName": "Coeficiente de incidência"},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}},"Property": "Casos prováveis de Dengue"},"Name": "iMEDIDAS.Casos prováveis de Dengue","NativeReferenceName": "Casos prováveis"},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}},"Property": "Titulo: Mapa"},"Name": "iMEDIDAS.Titulo: Mapa"}
                                        ],
                                        "Where": [
                                            {"Condition": {"Not": {"Expression": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}},"Property": "UF_NOME"}}],"Values": [[{"Literal": {"Value": "null"}}],[{"Literal": {"Value": "'Ignorado/sem informação'"}}]]}}}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d1"}},"Property": "SINTOMAS_ANO"}}],"Values": [[{"Literal": {"Value": "2024L"}}]]}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}},"Property": "ID_AGRAVO"}}],"Values": [[{"Literal": {"Value": "'A90'"}}]]}}}
                                        ],
                                        "OrderBy": [{"Direction": 2,"Expression": {"Measure": {"Expression": {"SourceRef": {"Source": "e"}},"Property": "Incidência (DENV)"}}}]
                                    },
                                    "Binding": {
                                        "Primary": {"Groupings": [{"Projections": [0,1,2]}]},
                                        "Projections": [3],
                                        "DataReduction": {"DataVolume": 3,"Primary": {"Window": {"Count": 500}}},
                                        "Aggregates": [{"Select": 1,"Aggregations": [{"Min": {}},{"Max": {}}]}],
                                        "Version": 1
                                    },
                                    "ExecutionMetricsKind": 1
                                }
                            }
                        ]
                    }
                }
            ],
            "modelId": 3127714
        }

        if estado:
            condition = {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}},"Property": "UF_PARSED"}}],"Values": [[{"Literal": {"Value": f"'{estado}'"}}]]}}}
            payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Where'].append(condition)

        response = requests.post(url = url, headers = self.headers, json = payload)

        result = response.json()['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

        data = [{"Estado": value['C'][0], "Casos": value['C'][2], "Coeficiente de incidencia": value['C'][1]} for value in result]

        return data
    
    def obitos(self, estado:str = None):

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
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Óbitos em investigação - DENV"}, "Name": "iMEDIDAS.Óbitos em investigação - DENV", "NativeReferenceName": "Óbitos em investigação - DENV"},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Óbitos por Dengue"}, "Name": "iMEDIDAS.Óbitos por Dengue", "NativeReferenceName": "Óbitos por Dengue"},
                                            {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "EVOLUCAO"}, "Name": "dEVOLUCAO.EVOLUCAO", "NativeReferenceName": "EVOLUCAO1"},
                                            {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Titulo: Evoluçao dos casos"}, "Name": "iMEDIDAS.Titulo: Evoluçao dos casos"}
                                        ],
                                        "Where": [
                                            {"Condition": {"Not": {"Expression": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "EVOLUCAO"}}],"Values": [[{"Literal": {"Value": "null"}}],[{"Literal": {"Value": "'Cura'"}}],[{"Literal": {"Value": "'Ignorado'"}}],[{"Literal": {"Value": "'Não informado'"}}],[{"Literal": {"Value": "'Óbito por outras causas'"}}]]}}}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "CRITERIO"}}],"Values": [[{"Literal": {"Value": "1D"}}],[{"Literal": {"Value": "2D"}}],[{"Literal": {"Value": "3D"}}],[{"Literal": {"Value": "0D"}}]]}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d1"}}, "Property": "SINTOMAS_ANO"}}],"Values": [[{"Literal": {"Value": "2024L"}}]]}}},
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "ID_AGRAVO"}}],"Values": [[{"Literal": {"Value": "'A90'"}}]]}}},
                                        ],
                                        "OrderBy": [{"Direction": 2, "Expression": {"Measure": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": "Óbitos em investigação - DENV"}}}]
                                    },
                                    "Binding": {
                                        "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
                                        "Projections": [3],
                                        "DataReduction": {"DataVolume": 3, "Primary": {"Top": {}}},
                                        "Version": 1
                                    },
                                    "ExecutionMetricsKind": 1
                                }
                            }
                        ]
                    }
                }
            ],
            "modelId": 3127714
        }

        if estado:
            condition = {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d2"}}, "Property": "UF_PARSED"}}],"Values": [[{"Literal": {"Value": f"'{estado}'"}}]]}}}
            payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Where'].append(condition)

        response = requests.post(url = url, headers = self.headers, json = payload)

        result = response.json()['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

        return result

    def test(self, estado:str = None):
        
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
                                            {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d1"}}, "Property": "SINTOMAS_ANO"}}],"Values": [[{"Literal": {"Value": "2024L"}}]]}}},
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

        if(estado):
            column = {"Column": {"Expression":  {"SourceRef": {"Source": "d2"}}, "Property": "UF_NOME"}},
            condition = {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d2"}}, "Property": "UF_PARSED"}}],"Values": [[{"Literal": {"Value": f"'{estado}'"}}]]}}},
            payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Select'].append(column)
            payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Where'].append(condition)
        
        print(payload['queries'][0]['Query']['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Where'])
        response = requests.post(url = url, headers = self.headers, json = payload)

        return response.json()['results'][0]['result']['data']['dsr']['DS']

    def custom_query(self, query_shape:str):

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

        result = response.json()['schemas'][0]['schema']['Entities']

        return result

if __name__ == "__main__":

    dengue = Dengue()

    obitos = dengue.test('Minas gerais')

    print(obitos)