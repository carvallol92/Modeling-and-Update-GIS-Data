
print('Importando librerias y componentes...')

import pandas as pd
import requests
import json
import ast
from arcgis import features
from arcgis import GIS    

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


def Longin():
    
    global gis,delitos_ext,delitos_extrajeros
    
    #Acceder a cuenta AGOL

    print('Ingrese las credenciales de acceso')
    print('')

    portal = "https://www.arcgis.com"
    user = input('Usuario:  ')
    password = input('Contraseña:  ')    

    print('')
    print('Conectando...')    
    
    gis = GIS(portal, user, password)
    
    
    item_ep = gis.content.get("d5e38adb9e9942698fda10b95b34efbf") #Service PROD
    delitos_ext0 = item_ep.tables[0] # Index PROD
    delitos_ext = delitos_ext0.query().sdf
    
    
    delitos_extrajeros = []
    
    for row in delitos_ext.iterrows():
        
        de_ext = row[1]['Delitos_Extranjeros']
                    
        delitos_extrajeros.append(de_ext)
             
    
    print('Conexión establecida')
    
    IntoInputs(delitos_extrajeros)
    

def IntoInputs(delitos_extrajeros):
    
    global año,mes
    
    print('')    
    print(' - - - Comenzamos  - - - ')
    print('') 

       
    n_input = input('Nombre de la planilla: ').upper()   
    año = input('Año de carga: ')
    mes = input('Mes de carga: ').capitalize()

    n_inputF = n_input+'.xlsx'
    N1 = pd.read_excel('1_entrada/'+n_inputF)   
    
        
    if mes in list_month and len(año) == 4:
        
        ProcesingDataFrame(N1,año,mes,n_input,delitos_extrajeros)
    
    else:
        
        print('')
        print('Hay errores en la carga de Mes o Año, por favor vuelve a intentarlo...')
        
        IntoInputs(delitos_extrajeros)           
 

def ProcesingDataFrame(N1,año,mes,n_input,delitos_extrajeros):    
    
    print('Procesando datos...')

    #Eliminate origen format
    N1 = N1.rename(columns=N1.iloc[4])
    N1 = N1.drop([0,1,2,3,4,5])
    N1.columns = [
    'delito',
    'pais',
    'total',
    'total_hombres',
    'total_mujeres',
    'total_procesados',
    'procesados_hombres',
    'procesados_mujeres',
    'sentenciados_total',
    'sentenciados_hombres',
    'sentenciados_mujeres']

    #Format Delitos and Delete

    delitos = {}

    for index,row in N1.iterrows():

        if row['pais'] in delitos_extrajeros:
            delitos.update([(index+1,row['pais'])])

        else:
            continue  

    temporal_delito = {}
    delitos_row = {}

    for index,row in N1.iterrows():

        if row['pais'] in delitos_extrajeros:
            temporal_delito.update([(index,row['pais'])])

        else:
            a = list(temporal_delito.values())
            a = a[-1]
            delitos_row.update([(index,a)])

    updateDelito = pd.DataFrame.from_dict(delitos_row, orient='index',columns=['delito'])

    N1.update(updateDelito)
    N1 = N1.drop(temporal_delito)

    N1[['delito','pais']] = N1[['delito','pais']].astype('category')
    N1[['total','total_hombres','total_mujeres','total_procesados','procesados_hombres',
    'procesados_mujeres','sentenciados_total','sentenciados_hombres','sentenciados_mujeres']] = N1[['total','total_hombres','total_mujeres','total_procesados','procesados_hombres','procesados_mujeres','sentenciados_total','sentenciados_hombres','sentenciados_mujeres']].astype('int')

    N1['año'] = int(año)
    N1['mes'] = mes
    N1['id_mes'] = ReclassMes(mes)
    N1['fecha'] = ReclassFecha(mes,año)

    print('')
    print('Generando planilla procesada...')

    N1.to_excel('2_salida/'+n_input+'_procesado.xlsx', sheet_name='data')

    print('')
    print('Listo..!')
    print('')
    
    GetService(gis,N1,año,mes)


def GetService(gis,N1,año,mes):
    
    global fs_lyr,geo_ep
            
    
    print('')
    print('Accediendo a los servicios..!')
    print('')

    #get table N5
    #item_fs = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
    item_fs = gis.content.get("10daa287ecc5449a9a78cb4353c860bc") #Service PROD
    fs_lyr = item_fs.tables[4]
    N1_service = fs_lyr.query().sdf

    #get geo ep
    #item_ep = gis.content.get("e7a668dd8f7a4de9a059bb9bab7d1d17") #Service Test
    item_ep = gis.content.get("d5a3fcb74ff04dbb9fc34164d90f43e5") #Service PROD
    #geo_ep = item_ep.layers[1]  # Index test
    geo_ep = item_ep.layers[0] # Index PROD
    ep_service = geo_ep.query().sdf
      

    #Desfinir macth de ID
    serv_paises = ep_service[['Pais_1','OBJECTID']]
    serv_paises.columns = ['pais','OBJECTID']

    #Desfinir campos a actualizar
    update_paises = ep_service[['OBJECTID','total','total_procesados','total_sentenciados','ano','mes']]

    #Desfinir actualización Geo EP.

    NT = N1[['pais','total','total_procesados','sentenciados_total']]
    NT_group = NT.groupby(by=["pais"]).sum()
    NT_join = pd.merge (NT_group,serv_paises, on='pais')

    #Add mes y año
    NT_join['año'] = int(año)
    NT_join['mes'] = mes
    
    
    print('Listo, Servicios cargados y validados...!')
    
    
    MakeDicct(N1,NT_join,update_paises)
    Control(ep_service,N1)



def MakeDicct(N1,NT_join,update_paises): 
    
    global N1_update, ep_service_update
    
    # Create dict format for update service
    
    print('')
    print('Preparando Datos para impactar...')
    print('')

    ep_service_update = []
    n2_template = update_paises.to_dict('index')[0].copy()

    for row in NT_join.iterrows():

        n2_template_update = n2_template.copy()

        n2_template_update['OBJECTID']=row[1]['OBJECTID']    
        n2_template_update['total']=row[1]['total']
        n2_template_update['total_procesados']=row[1]['total_procesados']
        n2_template_update['total_sentenciados']=row[1]['sentenciados_total']
        n2_template_update['ano']=row[1]['año']
        n2_template_update['mes']=row[1]['mes']

        ep_service_update.append({"attributes":n2_template_update})

    else:
        pass   


    #Create dict format for update service
    N1 = N1.reset_index()
    N1_update = []
    N1_template = N1.to_dict('index')[0].copy()

    for row in N1.iterrows():

        template_append = N1_template.copy()

        template_append['delito'] = row[1]['delito']
        template_append['pais'] = row[1]['pais']
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

        N1_update.append({"attributes":template_append})

    else:
        pass
    
    print('')
    print('Listo..!')
    print('')
        


def Control(ep_service,N1):  
    
           
    country_lry = []
    report = []

    for row in ep_service.iterrows():

        a = row[1]['Pais_1']

        country_lry.append(a)

    for row in N1.iterrows():

        country = row[1]['pais']

        if country not in country_lry:
            
            report.append(country)
                    
        else:            
            continue
    
    if len(report) > 0:
        
        print("""No se pueden vincular los siguiente elementos,
              {}
              
              Comunicarse con el administrador para actualizar la base
        """.format(report))
        
        print('')
        print('Proceso de Carga Cancelado')
        print('')
    
    else:
        
        ImpactServices(fs_lyr,N1_update,geo_ep,ep_service_update,mes,año)
            


def ImpactServices(fs_lyr,N1_update,geo_ep,ep_service_update,mes,año):   

    print('')
    print('Impactando servicio...')

    fs_lyr.edit_features(adds = N1_update)

    print('Proceso finalizado!!')

    print('')
    print('Actualizando capa de Paises...')
    geo_ep.edit_features(updates = ep_service_update)

    print('Proceso finalizado!!')
    print('Se ha actualizado los datos: Población Extranjera por Paises {} {}'.format(mes,año))
    print('')
    print('')


Longin()