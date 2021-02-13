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

departamento = [
'AMAZONAS',
'ANCASH',
'APURIMAC',
'AREQUIPA',
'AYACUCHO',
'CALLAO',
'CAJAMARCA',
'CUSCO',
'HUANCAVELICA',
'HUANUCO',
'ICA',
'JUNIN',
'LA LIBERTAD',
'LAMBAYEQUE',
'LIMA',
'LORETO',
'MADRE DE DIOS',
'MOQUEGUA',
'PASCO',
'PIURA',
'PUNO',
'SAN MARTIN',
'TACNA',
'TUMBES',
'UCAYALI'
]

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
N1 = N1.rename(columns=N1.iloc[4])
N1 = N1.drop([0,1,2,3,4,5])
N1.columns = [
'vacia',
'establecimiento_penitenciario',
'total',
'total_hombres',
'total_mujeres',
'total_procesados',
'procesados_hombres',
'procesados_mujeres',
'sentenciados_total',
'sentenciados_hombres',
'sentenciados_mujeres']
N1 = N1.drop('vacia',axis=1)

#Delete row with values Regional Office
delete_row = []

for index,row in N1.iterrows():
    if row['establecimiento_penitenciario'] in departamento:
        delete_row.append(index)
    else:
        continue
        
N1 = N1.drop(delete_row)

#Change DataType
N1[['establecimiento_penitenciario']] = N1[['establecimiento_penitenciario']].astype('category')
N1[['total','total_hombres','total_mujeres','total_procesados','procesados_hombres','procesados_mujeres','sentenciados_total','sentenciados_hombres','sentenciados_mujeres']] = N1[['total','total_hombres','total_mujeres','total_procesados','procesados_hombres','procesados_mujeres','sentenciados_total','sentenciados_hombres','sentenciados_mujeres']].astype('int')

#Formating column EP

c1 = {}
c2 = {}
c3 = {}
c4 = {}
c5 = {}

for index,row in N1.iterrows():
    a = row['establecimiento_penitenciario']
    
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
all_casesDF = pd.DataFrame.from_dict(all_cases, orient='index',columns=['establecimiento_penitenciario'])
N1.update(all_casesDF)

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
print('Conectando con los servicios..!')

#item_fs = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
item_fs = gis.content.get("10daa287ecc5449a9a78cb4353c860bc") #Service PROD
fs_lyr = item_fs.tables[5]
N1_service = fs_lyr.query().sdf

#get geo ep
#item_ep = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
item_ep = gis.content.get("10daa287ecc5449a9a78cb4353c860bc") #Service PROD
geo_ep = item_ep.layers[0]
ep_service = geo_ep.query().sdf

#Desfinir actualización Geo EP.

ep_service_upd = ep_service[['OBJECTID','ID','pob_penalEX']]
ep_service_upd = ep_service_upd.where(pd.notnull(ep_service_upd), 0)
ep_service_upd = ep_service_upd[['OBJECTID','ID','pob_penalEX']].astype(int)

templae_upd = ep_service[['OBJECTID','pob_penalEX']]

n1_join = N1_Done[['ID','total']]

n1_join_done = pd.merge (n1_join,ep_service_upd, on='ID')

# Create dict format for update service

ep_service_update = []
n2_template = templae_upd.to_dict('index')[0].copy()

for row in n1_join_done.iterrows():
          
    n2_template_update = n2_template.copy()
    
    n2_template_update['OBJECTID']=row[1]['OBJECTID']    
    n2_template_update['pob_penalEX']=row[1]['total']
                       
    ep_service_update.append({"attributes":n2_template_update})
    
else:
    pass  


# Create dict format for update service

N1_update = []
N1_template = N1_Done.to_dict('index')[0].copy()

for row in N1_Done.iterrows():
          
    template_append = N1_template.copy()

    template_append['establecimiento_penitenciario'] = row[1]['establecimiento_penitenciario']
    template_append['total'] = row[1]['total']
    template_append['total_hombres'] = row[1]['total_hombres']
    template_append['total_mujeres'] = row[1]['total_mujeres']
    template_append['total_procesados'] = row[1]['total_procesados']
    template_append['procesados_hombres'] = row[1]['procesados_hombres']
    template_append['procesados_mujeres'] = row[1]['procesados_mujeres']
    template_append['sentenciados_total'] = row[1]['sentenciados_total']
    template_append['sentenciados_hombres'] = row[1]['sentenciados_hombres']
    template_append['sentenciados_mujeres'] = row[1]['sentenciados_mujeres']
    template_append['año'] = row[1]['año']
    template_append['mes'] = row[1]['mes']
    template_append['OBJECTID'] = row[1]['OBJECTID']
    template_append['Departamento'] = row[1]['Departamento']
    template_append['Provincia'] = row[1]['Provincia']
    template_append['Distrito'] = row[1]['Distrito']
    template_append['Oficina_Regional'] = row[1]['Oficina_Regional']
    template_append['ID'] = row[1]['ID']
    template_append['label_EP'] = row[1]['label_EP']       
       
    N1_update.append({"attributes":template_append})

else:
    pass

print('')
print('Impactando servicio...')

fs_lyr.edit_features(adds = N1_update)

print('Actualizando capa de Establecimientos Penales...')
geo_ep.edit_features(updates = ep_service_update)

print('Proceso finalizado')
print('Se ha actualizado los datos: Población Extranjera por Establecimiento Penal {} {}'.format(mes,año))
