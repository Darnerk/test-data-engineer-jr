import requests
import json
import pandas as pd
pd.set_option('display.max_rows', None)

r_pasajeros_2016 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/3689da48-d557-5e5f-8347-006ced354939?format=json")
r_pasajeros_2017 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/2a323bb8-0a6d-5bd5-8366-90041c4f1c8c?format=json")
r_vuelos_2016 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/2743ebad-f1e2-5eff-8c4d-f8c5191d1775?format=json")
r_vuelos_2017 = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/a6960833-d5a3-56dc-b125-da9e4e1fce69?format=json")
r_lineas_aereas = requests.get(url="https://analytics.deacero.com/api/teenus/get-data/fed214f3-332d-522c-97ac-da395a066dba?format=json")

pasajeros_2016 = json.loads(r_pasajeros_2016.text)
pasajeros_2017 = json.loads(r_pasajeros_2017.text)
vuelos_2016 = json.loads(r_vuelos_2016.text)
vuelos_2017 = json.loads(r_vuelos_2017.text)
lineas_aereas = json.loads(r_lineas_aereas.text)

df_pasajeros_2016  = pd.DataFrame(pasajeros_2016)
df_pasajeros_2016 ['Año']=2016
df_pasajeros_2017  = pd.DataFrame(pasajeros_2017)
df_pasajeros_2017 ['Año']=2017

df_vuelos_2016  = pd.DataFrame(vuelos_2016)
df_vuelos_2016 ['Año']=2016
df_vuelos_2017  = pd.DataFrame(vuelos_2017)
df_vuelos_2017 ['Año']=2017

df_lineas_aereas = pd.DataFrame(lineas_aereas)


pasajeros_sin_duplicados_2016 = df_pasajeros_2016.drop_duplicates('ID_Pasajero', ignore_index=True)
pasajeros_sin_duplicados_2017 = df_pasajeros_2017.drop_duplicates('ID_Pasajero', ignore_index=True)

pasajeros = pd.concat([pasajeros_sin_duplicados_2016, pasajeros_sin_duplicados_2017], ignore_index=True)
pasajeros_sin_duplicados = pasajeros.drop_duplicates('ID_Pasajero', ignore_index=True)

vuelos = pd.concat([df_vuelos_2016, df_vuelos_2017], ignore_index=True)

pasajeros_vuelos = pd.merge(pasajeros_sin_duplicados,vuelos, left_on='ID_Pasajero', right_on='Cve_Cliente')
pasajeros_vuelos_aero_lineas = pd.merge(pasajeros_vuelos, df_lineas_aereas, left_on='Cve_LA', right_on='Code', how="left")
pasajeros_vuelos_aero_lineas.fillna('Otra', inplace=True)

fecha = pasajeros_vuelos_aero_lineas[['Viaje']]
fecha[['Mes', 'Dia', 'Año']] = fecha['Viaje'].str.split('/', expand=True)
fecha = fecha[['Mes', 'Dia', 'Año']]

pasajeros_vuelos_aero_lineas_fecha = pd.merge(pasajeros_vuelos_aero_lineas, fecha, left_index=True, right_index=True)

pasajeros_vuelos_aero_lineas_fecha['Mes'] = pasajeros_vuelos_aero_lineas_fecha['Mes'].astype(int)
pasajeros_vuelos_aero_lineas_fecha_primer_semestre = pasajeros_vuelos_aero_lineas_fecha[pasajeros_vuelos_aero_lineas_fecha['Mes'] <= 6]
pasajeros_vuelos_aero_lineas_fecha_segundo_semestre = pasajeros_vuelos_aero_lineas_fecha[pasajeros_vuelos_aero_lineas_fecha['Mes'] >= 7]

print('\nPromedios del primer semestre')
año = pasajeros_vuelos_aero_lineas_fecha_primer_semestre[['Año', 'Precio']]
promedio_año = año.groupby(['Año']).mean()
print(promedio_año)

clase = pasajeros_vuelos_aero_lineas_fecha_primer_semestre[['Clase', 'Precio']]
promedio_clase = clase.groupby(['Clase']).mean()
print(promedio_clase)

ruta = pasajeros_vuelos_aero_lineas_fecha_primer_semestre[['Ruta', 'Precio']]
promedio_ruta = ruta.groupby(['Ruta']).mean()
print(promedio_ruta)

linea_aerea = pasajeros_vuelos_aero_lineas_fecha_primer_semestre[['Linea_Aerea', 'Precio']]
promedio_linea_aerea = linea_aerea.groupby(['Linea_Aerea']).mean()
print(promedio_linea_aerea)

print('\nPromedios del segundo semestre')
año = pasajeros_vuelos_aero_lineas_fecha_segundo_semestre[['Año', 'Precio']]
promedio_año = año.groupby(['Año']).mean()
print(promedio_año)

clase = pasajeros_vuelos_aero_lineas_fecha_segundo_semestre[['Clase', 'Precio']]
promedio_clase = clase.groupby(['Clase']).mean()
print(promedio_clase)

ruta = pasajeros_vuelos_aero_lineas_fecha_segundo_semestre[['Ruta', 'Precio']]
promedio_ruta = ruta.groupby(['Ruta']).mean()
print(promedio_ruta)

linea_aerea = pasajeros_vuelos_aero_lineas_fecha_segundo_semestre[['Linea_Aerea', 'Precio']]
promedio_linea_aerea = linea_aerea.groupby(['Linea_Aerea']).mean()
print(promedio_linea_aerea)