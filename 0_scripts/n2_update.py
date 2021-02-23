#!/usr/bin/env python
# coding: utf-8

# In[1]:


print('Importando librerias y componentes...')

import pandas as pd
import requests
import json
import ast
from arcgis import features
from arcgis import GIS    


# In[2]:


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
    
list_month = ['Enero','Febrero','Marzo','Abril',
            'Mayo','Junio','Julio','Agosto',
            'Septiembre','Octubre','Noviembre','Diciembre'         
           ]

regional_office = ['ALTIPLANO - PUNO',
                   'CENTRO - HUANCAYO',
                   'LIMA - LIMA',
                   'NOR ORIENTE - SAN MARTIN',
                   'NORTE - CHICLAYO','ORIENTE - HUANUCO',
                   'SUR - AREQUIPA','SUR ORIENTE - CUSCO']


# In[3]:


def Longin():
    
    global gis
    
    #Acceder a cuenta AGOL

    print('Ingrese las credenciales de acceso')
    print('')

    portal = "https://www.arcgis.com"
    user = input('Usuario:  ')
    password = input('Contraseña:  ')

    print('')
    print('Conectando...')
    
    gis = GIS(portal, user, password)
                
    
    print('Conexión establecida')
    
    IntoInputs()
    


# In[4]:


def IntoInputs():
    
    print('')    
    print(' - - - Comenzamos  - - - ')
    print('') 

       
    n_input = input('Nombre de la planilla: ').upper()   
    año = input('Año de carga: ')
    mes = input('Mes de carga: ').capitalize()

    n_inputF = n_input+'.xlsx'
    N2 = pd.read_excel('1_entrada/'+n_inputF)
    table_id = pd.read_excel('table_id.xls')
    
        
    if mes in list_month and len(año) == 4:
        
        ProcesingDataFrame(N2,año,mes,n_input,table_id)
    
    else:
        
        print('')
        print('Hay errores en la carga de Mes o Año, por favor vuelve a intentarlo...')
        
        IntoInputs()           
    
    


# In[5]:


def ProcesingDataFrame(N2,año,mes,n_input,table_id):
    
    print('Procesando datos...')

    #Eliminate origen format
    N2 = N2.rename(columns=N2.iloc[3])
    N2 = N2.drop([0,1,2,3,4])
    N2.columns = [
    'vacia',
    'vacia',
    'establecimiento_penitenciario',
    'capacidad_albergue', 
    'poblacion_penal',
    'ocupacion_porcentaje',
    'sobrepoblacion',
    'sobrepoblacion_porcentaje',
    'hacinamiento',
    'vacia',
    'vacia',
    ]
    N2 = N2.drop('vacia',axis=1)

    #Delete row with values Regional Office
    delete_row = []

    for index,row in N2.iterrows():
        if row['establecimiento_penitenciario'] in regional_office:
            delete_row.append(index)
        else:
            continue

    N2 = N2.drop(delete_row)

    #Format porcentaje

    p1 = {}
    p2 = {}

    for index,row in N2.iterrows():
        b = row['ocupacion_porcentaje']
        c = row['sobrepoblacion_porcentaje']

        p1.update([(index,b)])
        p2.update([(index,c)])

    for key, values in p1.items():
        p1_v = values.replace('%','').replace(' %','').strip()
        p1.update([(key,p1_v)]) 

    for key, values in p2.items():
        p2_v = values.replace('%','').replace(' %','').strip()
        p2.update([(key,p2_v)]) 


    p1_DF = pd.DataFrame.from_dict(p1, orient='index',columns=['ocupacion_porcentaje'])
    N2.update(p1_DF)

    p2_DF = pd.DataFrame.from_dict(p2, orient='index',columns=['sobrepoblacion_porcentaje'])
    N2.update(p2_DF)


    #Format Column EP

    c1 = {}
    c2 = {}
    c3 = {}
    c4 = {}
    c5 = {}

    for index,row in N2.iterrows():
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

    if len(N2) == ctotal:
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

    #Change DataType

    N2[['establecimiento_penitenciario']] = N2[['establecimiento_penitenciario']].astype('category')
    N2[['capacidad_albergue','poblacion_penal','ocupacion_porcentaje','sobrepoblacion','sobrepoblacion_porcentaje']].astype('int')


    #Compilate all cases and update DF
    all_cases = {**c1, **c2, **c3, **c4, **c5}
    all_casesDF = pd.DataFrame.from_dict(all_cases, orient='index',columns=['establecimiento_penitenciario'])
    N2.update(all_casesDF)

    N2['año'] = int(año)
    N2['mes'] = mes
    N2['id_mes'] = ReclassMes(mes)
    N2['fecha'] = ReclassFecha(mes,año)

    # Merge de Tablas
    N2_done = pd.merge (N2,table_id, on='establecimiento_penitenciario')

    if N2_done.isnull().values.sum() == 0:
        print('')
        print('Unión de tablas sin problemas, no hay nulos!')

    else:
        print('')
        print('Alerta..!! se encontraron nulos en la union de tabla')

    print('')
    print('Generando planilla procesada...')

    N2_done.to_excel('2_salida/'+n_input+'_procesado.xlsx', sheet_name='data')

    print('')
    print('Listo!')
    print('')
    
    GetUpdateService(gis,N2,año,mes,N2_done)


# In[6]:


def GetUpdateService(gis,n2,año,mes,n2_done):
    
    print('Preparando proceso para actualizar servicios, espere unos segundos...')

    #get table N2
    #item_n2 = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
    item_n2 = gis.content.get("10daa287ecc5449a9a78cb4353c860bc") #Service PROD
    tb_n2 = item_n2.tables[1]
    N2_service = tb_n2.query().sdf

    #get geo ep
    #item_ep = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
    item_ep = gis.content.get("10daa287ecc5449a9a78cb4353c860bc") #Service PROD
    geo_ep = item_ep.layers[0]
    ep_service = geo_ep.query().sdf

    #Desfinir actualización Geo EP.
    ep_service_upd = ep_service[['OBJECTID','capacidad','pob_penal','haciamiento']]
    ep_service_merge = ep_service[['OBJECTID','ID']].astype('int')
    n2_join = n2_done[['ID','capacidad_albergue','poblacion_penal','hacinamiento','año','mes']]

    n2_join_done = pd.merge (n2_join,ep_service_merge, on='ID')


    # Create dict format for update service

    ep_service_update = []
    n2_template = ep_service_upd.to_dict('index')[0].copy()

    for row in n2_join_done.iterrows():

        n2_template_update = n2_template.copy()

        n2_template_update['OBJECTID']=row[1]['OBJECTID']    
        n2_template_update['capacidad']=row[1]['capacidad_albergue']
        n2_template_update['pob_penal']=row[1]['poblacion_penal']
        n2_template_update['haciamiento']=row[1]['hacinamiento']
        n2_template_update['ano']=row[1]['año']
        n2_template_update['mes']=row[1]['mes']


        ep_service_update.append({"attributes":n2_template_update})

    else:
        pass      

    # Create dict format for update service
    n2_update = []
    n2_template = n2_done.to_dict('index')[0].copy()

    for row in n2_done.iterrows():

        template_append = n2_template.copy()

        template_append['establecimiento_penitenciario'] = row[1]['establecimiento_penitenciario']
        template_append['capacidad_albergue'] = row[1]['capacidad_albergue']
        template_append['poblacion_penal'] = row[1]['poblacion_penal']
        template_append['ocupacion_porcentaje'] = row[1]['ocupacion_porcentaje']
        template_append['sobrepoblacion'] = row[1]['sobrepoblacion']
        template_append['sobrepoblacion_porcentajes'] = row[1]['sobrepoblacion_porcentaje']
        template_append['hacinamiento'] = row[1]['hacinamiento']
        template_append['año'] = row[1]['año']
        template_append['mes'] = row[1]['mes']
        template_append['OBJECTID'] = row[1]['OBJECTID']
        template_append['Departamento'] = row[1]['Departamento']
        template_append['Provincia'] = row[1]['Provincia']
        template_append['Distrito'] = row[1]['Distrito']
        template_append['Oficina_Regional'] = row[1]['Oficina_Regional']
        template_append['ID'] = row[1]['ID']
        template_append['label_EP'] = row[1]['label_EP']       

        n2_update.append({"attributes":template_append})

    else:
        pass

    # Impacto de Servicios

    print('')
    print('Impactando servicio...')

    tb_n2.edit_features(adds = n2_update)

    print('Actualizando capa de Establecimeintos Penales...')
    geo_ep.edit_features(updates = ep_service_update)

    print('El proceso ha finalizado!')
    print('Se ha actualizado los datos: Capacidad y Hacinamiento {} {}'.format(mes,año))


# In[7]:


Longin()

