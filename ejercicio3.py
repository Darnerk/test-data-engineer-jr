import requests
import json
import pandas as pd
pd.set_option('display.max_rows', None)

r_pasajeros_2016 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/3689da48-d557-5e5f-8347-006ced354939?format=json")
r_pasajeros_2017 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/2a323bb8-0a6d-5bd5-8366-90041c4f1c8c?format=json")
r_vuelos_2016 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/2743ebad-f1e2-5eff-8c4d-f8c5191d1775?format=json")
r_vuelos_2017 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/a6960833-d5a3-56dc-b125-da9e4e1fce69?format=json")

pasajeros_2016 = json.loads(r_pasajeros_2016.text)
pasajeros_2017 = json.loads(r_pasajeros_2017.text)
vuelos_2016 = json.loads(r_vuelos_2016.text)
vuelos_2017 = json.loads(r_vuelos_2017.text)

df_pasajeros_2016  = pd.DataFrame(pasajeros_2016)
df_pasajeros_2017  = pd.DataFrame(pasajeros_2017)

df_vuelos_2016  = pd.DataFrame(vuelos_2016)
df_vuelos_2017  = pd.DataFrame(vuelos_2017)

pasajeros_sin_duplicados_2016 = df_pasajeros_2016.drop_duplicates('ID_Pasajero', ignore_index=True)
pasajeros_sin_duplicados_2017 = df_pasajeros_2017.drop_duplicates('ID_Pasajero', ignore_index=True)

pasajeros = pd.concat([pasajeros_sin_duplicados_2016, pasajeros_sin_duplicados_2017], ignore_index=True)
pasajeros_sin_duplicados = pasajeros.drop_duplicates('ID_Pasajero', ignore_index=True)

vuelos = pd.concat([df_vuelos_2016, df_vuelos_2017], ignore_index=True)

pasajeros_vuelos = pd.merge(pasajeros_sin_duplicados,vuelos, left_on='ID_Pasajero', right_on='Cve_Cliente')
print(pasajeros_vuelos)