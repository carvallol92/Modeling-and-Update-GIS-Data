#!/usr/bin/env python
# coding: utf-8

#Acceder a cuenta AGOL

print('Ingrese las credenciales de acceso')
print('')

portal = "https://www.arcgis.com"
user = input('Usuario:  ')
password = input('Contraseña:  ')

print('')
print('Conectando...')

from arcgis import GIS

gis = GIS(portal, user, password)
print('Conexión establecida')


print('')
print('Importando librerias y funciones...')

import pandas as pd
import requests
import json
import ast
from arcgis import GIS
from arcgis import features

def ReclassMes(mes):
    if mes=="Enero":
        return "0"
    elif mes=="Febrero":
        return "1"
    elif mes =="Marzo":
        return "2"
    elif mes == "Abril":
        return "3"
    elif mes == "Mayo":
        return "4"
    elif mes == "Junio":
        return "5"
    elif mes == "Julio":
        return "6"
    elif mes == "Agosto":
        return "7"
    elif mes == "Septiembre":
        return "8"
    elif mes == "Octubre":
        return "9"
    elif mes == "Noviembre":
        return "10"
    elif mes == "Diciembre":
        return "11"
    
def ReclassFecha(mes,año):
    if mes=="Enero":
        return "01/02/"+ año + " 12:00:00"
    elif mes=="Febrero":
        return "02/02/"+ año + " 12:00:00"
    elif mes =="Marzo":
        return "03/02/"+ año + " 12:00:00"
    elif mes == "Abril":
        return "04/02/"+ año + " 12:00:00"
    elif mes == "Mayo":
        return "05/02/"+ año + " 12:00:00"
    elif mes == "Junio":
        return "06/02/"+ año + " 12:00:00"
    elif mes == "Julio":
        return "07/02/"+ año + " 12:00:00"
    elif mes == "Agosto":
        return "08/02/"+ año + " 12:00:00"
    elif mes == "Septiembre":
        return "09/02/"+ año + " 12:00:00"
    elif mes == "Octubre":
        return "10/02/"+ año + " 12:00:00"
    elif mes == "Noviembre":
        return "11/02/"+ año + " 12:00:00"
    elif mes == "Diciembre":
        return "12/02/"+ año + " 12:00:00"
    
EP = ['PUNO',
  'LAMPA',
  'JULIACA',
  'CHALLAPALCA',
  'HUANCAYO',
  'MUJERES DE CONCEPCIÓN',
  'CHANCHAMAYO',
  'JAUJA',
  'TARMA',
  'LA OROYA',
  'RIO NEGRO',
  'HUANCAVELICA',
  'AYACUCHO',
  'HUANTA',
  'HUARAZ',
  'CHIMBOTE',
  'CALLAO',
  'CEREC - BASE NAVAL',
  'MUJERES DE CHORRILLOS',
  'ANEXO DE MUJERES DE CHORRILLOS',
  'LURIGANCHO',
  'MIGUEL CASTRO CASTRO',
  'VIRGEN DE FÁTIMA',
  'ANCÓN I',
  'BARBADILLO',
  'ANCÓN II',
  'HUACHO',
  'CAÑETE',
  'HUARAL',
  'ICA',
  'CHINCHA',
  'MOYOBAMBA',
  'JUANJUI',
  'TARAPOTO',
  'SANANGUILLO',
  'IQUITOS',
  'MUJERES DE IQUITOS',
  'YURIMAGUAS',
  'CHACHAPOYAS',
  'BAGUA GRANDE',
  'TUMBES',
  'PIURA',
  'SULLANA',
  'CHICLAYO',
  'TRUJILLO',
  'MUJERES DE TRUJILLO',
  'PACASMAYO',
  'CAJAMARCA',
  'CHOTA',
  'JAEN',
  'SAN IGNACIO',
  'HUÁNUCO',
  'CERRO DE PASCO',
  'COCHAMARCA',
  'PUCALLPA',
  'AREQUIPA',
  'MUJERES DE AREQUIPA',
  'CAMANÁ',
  'MOQUEGUA',
  'TACNA',
  'MUJERES DE TACNA',
  'ABANCAY',
  'ANDAHUAYLAS',
  'CUSCO',
  'MUJERES DE CUSCO',
  'SICUANI',
  'QUILLABAMBA',
  'PUERTO MALDONADO'  
  ]

print('')
print('Ingrese los valores solicitados:')
print('')
n_input = input('Nombre de la planilla: ').upper()
año = input('Año de carga: ')
mes = input('Mes de carga: ').capitalize()
print('')
print('Cargando planilla...')
print('')

#Reading data
n_inputF = n_input+'.xlsx'
N1 = pd.read_excel('1_entrada/'+n_inputF)
table_id = pd.read_excel('table_id.xls')

print('Procesando datos...')

#Eliminate origen format
N1 = N1.rename(columns=N1.iloc[3])
N1 = N1.drop([0,1,2,3,4])
N1.columns = [
'establecimiento_penitenciario',
'vacia',
'delito',
'total',
'hombres',
'mujeres',
]
N1 = N1.drop('vacia',axis=1)

#Formating column EP

c1 = {}
c2 = {}
c3 = {}
c4 = {}
c5 = {}

for index,row in N1.iterrows():
    a = row['delito']
    
    if 'E.P. DE' in a:     
        c1.update([(index,a)])
    elif 'E.P DE' in a:
        c2.update([(index,a)])
    elif 'E.P. ' in a:
        c3.update([(index,a)])
    elif 'E.P ' in a:
        c4.update([(index,a)])
    else:
        c5.update([(index,a)])
        continue   

ctotal = len(c1) + len(c2) + len(c3) + len(c4) + len(c5)

if len(N1) == ctotal:
    print('')
    print('Formato de EP sin problemas!')
else:
    print('')
    print('Alerta..!!! hubo alguna incosistencia.')

for key, values in c1.items():
    c1_v = values.replace('E.P. DE','').replace('  ',' ').strip()
    c1.update([(key,c1_v)])
    
for key, values in c2.items():
    c2_v = values.replace('E.P DE','').replace('  ',' ').strip()
    c2.update([(key,c2_v)]) 
    
for key, values in c3.items():
    c3_v = values.replace('E.P.','').replace('  ',' ').strip()
    c3.update([(key,c3_v)]) 
    
for key, values in c4.items():
    c4_v = values.replace('E.P','').replace('  ',' ').strip()
    c4.update([(key,c4_v)])
    
#Compilate all cases and update DF
all_cases = {**c1, **c2, **c3, **c4, **c5}
all_casesDF = pd.DataFrame.from_dict(all_cases, orient='index',columns=['delito'])
N1.update(all_casesDF)

#Formato de dos columnas

ep_row = {}

for index,row in N1.iterrows():
        
    if row['delito'] in EP:
        ep_row.update([(index,row['delito'])])
                       
    else:
        continue

temporal_delito = {}
delitos_row = {}

for index,row in N1.iterrows():
        
    if row['delito'] in EP:
        temporal_delito.update([(index,row['delito'])])
        
    else:
        a = list(temporal_delito.values())
        a = a[-1]
        delitos_row.update([(index,a)])

updateDelito = pd.DataFrame.from_dict(delitos_row, orient='index',columns=['establecimiento_penitenciario'])

N1.update(updateDelito)   
N1 = N1.drop(ep_row)

N1[['establecimiento_penitenciario','delito']] = N1[['establecimiento_penitenciario','delito']].astype('category')
N1[['total','hombres','mujeres',]] = N1[['total','hombres','mujeres',]].astype('int')

N1['año'] = int(año)
N1['mes'] = mes
N1['id_mes'] = ReclassMes(mes)
N1['fecha'] = ReclassFecha(mes,año)

# Merge de Tablas
N1_Done = pd.merge (N1,table_id, on='establecimiento_penitenciario')

if N1_Done.isnull().values.sum() == 0:
    
    print('')
    print('Unión de tablas sin problemas!')
    
else:
    
    print('')
    print('Alerta..!! se encontraron nulos en la union de tabla')
    print('')

print('Generando planilla procesada...')

N1_Done.to_excel('2_salida/'+n_input+'_procesado.xlsx', sheet_name='data')


print('')
print('Listo..!')
print('')

print('Accediendo a servicio en AGOL')

#item_fs = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
#fs_lyr = item_fs.tables[6]
item_fs = gis.content.get("d229559d280843088eedb819e937bfbd") #Service PROD
fs_lyr = item_fs.tables[0]
N1_service = fs_lyr.query().sdf

N1_update = []
N1_template = N1_Done.to_dict('index')[0].copy()

for row in N1.iterrows():
          
    template_append = N1_template.copy()

    template_append['establecimiento_penitenciario'] = row[1]['establecimiento_penitenciario']
    template_append['delito'] = row[1]['delito']
    template_append['total'] = row[1]['total']
    template_append['hombres'] = row[1]['hombres']
    template_append['mujeres'] = row[1]['mujeres']   
    template_append['año'] = row[1]['año']
    template_append['mes'] = row[1]['mes']
    
    #template_append['OBJECTID'] = row[1]['OBJECTID']
    #template_append['Departamento'] = row[1]['Departamento']
    #template_append['Provincia'] = row[1]['Provincia']
    #template_append['Distrito'] = row[1]['Distrito']
    #template_append['Oficina_Regional'] = row[1]['Oficina_Regional']
    #template_append['ID'] = row[1]['ID']
    #template_append['label_EP'] = row[1]['label_EP']  
    
    N1_update.append({"attributes":template_append})

else:
    pass


print('')
print('Impactando servicio...')

fs_lyr.edit_features(adds = N1_update)

print('Proceso finalizado!!')
print('Se ha actualizado los datos: Egreso {} {}'.format(mes,año))

