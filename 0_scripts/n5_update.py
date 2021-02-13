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
from arcgis import features

delitos_extrajeros = ['ABORTO AGRAVADO',
 'ABORTO AGRAVADO POR LA CUALIFICACION DEL SUJETO ACTIVO',
 'ACTOS CONTRA EL PUDOR',
 'ACTOS CONTRA EL PUDOR EN MENORES DE 14 AÑOS',
 'ACTOS DE CONVERSION Y TRANSFERENCIA',
 'ACTOS DE OCULTAMIENTO Y TENENCIA',
 'ADMINISTRACION FRAUDULENTA',
 'ADQUISICION POSESION ACONDICIONAMIENTO Y TRANSPORTE DE CLORHIDRATO DE COCAINA CON FINES DE COMERCIAL',
 'AGRESIONES CONTRA LA MUJER o INTEGRANTES DEL GRUPO FAMILIAR',
 'AGRESIONES CONTRA LA MUJER O INTEGRANTES DEL GRUPO FAMILIAR',
 'APROPIACION ILICITA COMUN',
 'ASOCIACION ILICITA PARA DELINQUIR',
 'ATENTADO A LA INTEGRIDAD DE DATOS INFORMATICOS',
 'AUTO-ABORTO',
 'BANDA  CRIMINAL',
 'BANDA CRIMINAL',
 'CIRCULACION MONEDA FALSA',
 'COACCION',
 'COHECHO PASIVO PROPIO',
 'COLUSION AGRAVADA',
 'CONCUSION',
 'CONDUCCION EN ESTADO DE EBRIEDAD O DROGADICCION',
 'CONSPIRACION Y OFRECIMIENTO PARA EL DELITO DE SICARIATO',
 'CONTRABANDO',
 'CONTRABANDO AGRAVADO',
 'CORRUPCION DE FUNCIONARIOS',
 'DAÑO SIMPLE ',
 'DEFRAUDACION TRIBUTARIA',
 'DELITO DE TERRORISMO',
 'DISTURBIOS',
 'ESTAFA',
 'ESTAFA AGRAVADA',
 'EXHIBICIONES Y PUBLICACIONES OBSCENAS',
 'EXHIBICIONES Y PUBLICACIONES OBSCENAS - PORNOGRAFIA INFANTIL',
 'EXPLOTACION SEXUAL',
 'EXPLOTACION SEXUAL DE NIÑAS, NIÑOS Y ADOLESCENTES',
 'EXTORSION',
 'EXTORSION AGRAVADA',
 'EXTORSION EN GRADO DE TENTATIVA',
 'FABRICACION ILEGAL DE ARMAS Y MUNICIONES ',
 'FABRICACION Y FALSIFICACION DE MONEDA DE CURSO LEGAL',
 'FABRICACION Y TENENCIA ILEGAL DE ARMAS, MUNICIONES Y EXPLOSIVOS ',
 'FABRICACION, COMERCIALIZACION, USO O PORTE DE ARMAS',
 'FALSIFICACION DE BILLETES O MONEDAS',
 'FALSIFICACION DE BILLETES O MONEDAS ',
 'FALSIFICACION DE DOCUMENTO',
 'FAVORECIMIENTO A LA PROSTITUCION',
 'FAVORECIMIENTO A LA PROSTITUCION-FORMA AGRAVADA',
 'FEMINICIDIO',
 'FEMINICIDIO - FORMA  AGRAVADA',
 'FEMINICIDIO GRADO DE TENTATIVA',
 'FORMAS AGRAVADAS DE LA TRATA DE PERSONAS',
 'FORMAS AGRAVADAS DEL TRAFICO ILICITO DE MIGRANTES',
 'FRAUDE EN LA ADMINISTRACION DE PERSONAS JURIDICAS',
 'FRAUDE EN REMATES, LICITACIONES Y CONCURSOS PUBLICOS ',
 'FRAUDE INFORMATICO',
 'FRAUDE INFORMATICO-AGRAVADA',
 'FRAUDE PROCESAL',
 'HOMICIDIO CALIFICADO - ASESINATO',
 'HOMICIDIO CALIFICADO - ASESINATO GRADO TENTATIVA',
 'HOMICIDIO CALIFICADO - GRADO TENTATIVA',
 'HOMICIDIO CULPOSO',
 'HOMICIDIO POR EMOCION VIOLENTA',
 'HOMICIDIO SIMPLE',
 'HOMICIDIO SIMPLE GRADO DE TENTATIVA',
 'HURTO AGRAVADO',
 'HURTO AGRAVADO - GRADO TENTATIVA',
 'INCUMPLIMIENTO DE LA OBLIGACION ALIMENTARIA',
 'INGRESO ILEGAL AL TERRITORIO NACIONAL DE RESIDUOS PELIGROSOS O TOXICOS',
 'INGRESO INDEBIDO DE MATERIALES O COMPONENETES CON FINES DE ELABORACION DE EQUIPOS DE COMUNICACION EN CENTROS DE DETENCIO',
 'INSOLVENCIA FRAUDULENTA',
 'LAVADO DE ACTIVOS',
 'LESIONES CULPOSAS',
 'LESIONES CULPOSAS GRAVES',
 'LESIONES GRAVES',
 'LESIONES GRAVES (SEGUIDAS DE MUERTE)',
 'LESIONES GRAVES POR VIOLENCIA FAMILIAR',
 'LESIONES LEVES',
 'MALVERSACION DE FONDOS',
 'MARCAJE o REGLAJE',
 'MARCAJE O REGLAJE',
 'MICROCOMERCIALIZACION O MICROPRODUCCION',
 'OMISION DE SOCORRO Y EXPOSICION A PELIGRO',
 'ORGANIZACIÓN CRIMINAL',
 'OTROS DELITOS',
 'PARRICIDIO',
 'PARRICIDIO - GRADO DE TENTATIVA',
 'PELIGRO COMUN',
 'POSESION INDEBIDA DE TELEFONOS CELULARES O ARMAS, MUNICIONES O MATERIALES EXPLOSIVOS, INFLAMABLES, ASFIXIANTES O TOXICOS',
 'POSESION INDEBIDA DE TELEFONOS CELULARES O, ARMAS, MUNICIONES O MATERIALES EXPLOSIVOS, INFLAMABLES, ASFIXIANTES O TOXICOS EN ESTABLECIMIENTOS PENITENCIARIOS',
 'POSESION INDEBIDA DE TELEFONOS CELULARES O, ARMAS, MUNICIONES O MATERIALES EXPLOSIVOS, INFLAMABLES, ASFIXIANTES O TOXICOS EN ESTABLECIMIETNOPS PENITENCIARIOS',
 'PRODUCCION DE PELIGRO COMUN CON MEDIOS CATASTROFICOS',
 'PROMOCION O FAVORECIMIENTO AL TRAFICO ILICITO DE DROGAS',
 'PROPOSICIONES SEXUALES A NIÑOS, NIÑAS Y ADOLECENTES',
 'RECEPTACION',
 'RECEPTACION - FORMAS AGRAVADAS ',
 'RESISTENCIA Y DESOBEDIENCIA A LA AUTORIDAD',
 'ROBO',
 'ROBO AGRAVADO',
 'ROBO AGRAVADO GRADO TENTATIVA',
 'ROBO DE GANADO',
 'ROBO GRADO TENTATIVA',
 'SECUESTRO',
 'SECUESTRO - GRADO TENTATIVA',
 'SECUESTRO AGRAVADO',
 'SICARIATO',
 'TENENCIA ILEGAL DE ARMAS',
 'TENENCIA ILEGAL DE MUNICIONES',
 'TOCAMIENTOS, ACTOS DE CONNOTACIÓN SEXUAL O ACTOS LIBIDINOSOS EN AGRAVIO DE MENORES',
 'TOCAMIENTOS, ACTOS DE CONNOTACIÓN SEXUAL O ACTOS LIBIDINOSOS EN AGRAVIO DE MENORES EN GRADO DE TENTATIVA',
 'TOCAMIENTOS, ACTOS DE CONNOTACIÓN SEXUAL O ACTOS LIBIDINOSOS SIN CONSENTIMIENTO',
 'TRAFICO DE MERCANCIAS PROHIBIDAS O RESTRINGIDAS',
 'TRAFICO DE MONEDAS Y BILLETES FALSOS',
 'TRAFICO ILEGAL DE ARMAS',
 'TRAFICO ILICITO DE DROGA',
 'TRAFICO ILICITO DE DROGAS',
 'TRAFICO ILICITO DE DROGAS - FORMAS AGRAVADAS',
 'TRAFICO ILICITO DE MIGRANTES',
 'TRATA DE PERSONAS',
 'USURPACION AGRAVADA',
 'VIOLACION A PERSONA EN ESTADO DE INCONSCIENCIA O EN LA IMPOSIBILIDAD DE RESISTIR',
 'VIOLACION DE MEDIDAS SANITARIAS',
 'VIOLACION DE PERSONA EN ESTADO DE INCONSCIENCIA O EN LA IMPOSIBILIDAD DE RESISTIR',
 'VIOLACION DE PERSONA EN ESTADO DE INCONSCIENCIA O EN LA IMPOSIBILIDAD DE RESISTIR-FORMA AGRAVADA',
 'VIOLACION EN GRADO DE TENTATIVA',
 'VIOLACION SEXUAL',
 'VIOLACION SEXUAL DE MENOR DE EDAD',
 'VIOLACION SEXUAL DE MENOR DE EDAD EN GRADO DE TENTATIVA',
 'VIOLACION SEXUAL DE PERSONA EN ESTADO DE INCONSCIENCIA O EN LA IMPOSIBILIDAD DE RESISTIR',
 'VIOLACION SEXUAL DE PERSONA EN ESTADO DE INCONSCIENCIA O EN LA IMPOSIBILIDAD DE RESISTIR-FORMA AGRAVADA',
 'VIOLACION SEXUAL EN GRADO DE TENTATIVA',
 'VIOLENCIA CONTRA LA AUTORIDAD PARA IMPEDIR EL EJERCICIO DE SUS FUNCIONES',
 'VIOLENCIA CONTRA UN FUNCIONARIO PUBLICO']

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

# Create dict format for update service

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
