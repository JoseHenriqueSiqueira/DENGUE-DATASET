## class Dengue:
### def __init\__ ():
Declares the base URL from where the data is extracted
   
### def dados(estado: str = None, ano: str = '2024'):
This method is responsible for returning information on 'probable cases', 'deaths under investigation', 'dengue deaths', 'Incidence coefficient' in a given Brazilian state or the whole of Brazil.
| Parameter   | type       | Description                                   |
| :---------- | :--------- | :------------------------------------------ |
| `estado`| `string` | **Optional**.  Indicates from which Brazilian state the data will be returned.|
| `ano`| `string` | **Optional**.  Indicates from which year the data will be returned.|

|Return| type       | Description                                   |
|-------| :--------- | :------------------------------------------ |
|`data`| `list` | Returns specific data for the Brazilian state or the entire country.|

### def custom_query(query_shape: str):
This method is used to build custom queries on top of the data source.
| Parameter   | type       | Description                                   |
| :---------- | :--------- | :------------------------------------------ |
| `query_shape`| `string` | **Mandatory**.  SemanticQueryDataShapeCommand Power BI.|

|Return| type       | Description                                   |
|-------| :--------- | :------------------------------------------ |
|`response`| `dict` | Returns data based on the custom query.|

### def database_schema():
This method is responsible for returning the database schema used in this repository.

|Return| type       | Description                                   |
|-------| :--------- | :------------------------------------------ |
|`response`| `dict` | Returns the tables used to build PowerBI.|

