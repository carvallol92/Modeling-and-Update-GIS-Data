#!/usr/bin/env python
# coding: utf-8

print('Importando librerias, por favor espere...')

import pandas as pd
import requests
import json
import ast

from arcgis import GIS
from arcgis import features

list_month = ['Enero','Febrero','Marzo','Abril',
            'Mayo','Junio','Julio','Agosto',
            'Septiembre','Octubre','Noviembre','Diciembre'         
           ]

           
def delete_data(input_user,table,year,month):
    
    global Nx_service
    
    from arcgis import GIS
    from arcgis import features
           
    print('')
    print('Ingresar credenciales de acceso:')
    print('')
    
    portal = "https://www.arcgis.com"
    user = input('Usuario:  ')
    password = input('Contraseña:  ')
    
    print('')
    print('Conectando...')

    gis = GIS(portal, user, password)
    print('Conexión establecida')
            
    print('Accediendo a servicios en AGOL...')
    
    # Lógica para tablas N8 y N9
    
    if table in ('N1','N2','N3','N5','N6','N7'):
        
        n_dict = {'N1':0,'N2':1,'N3':2,'N4':3,'N5':4,'N6':5,'N7':6}
        
        from arcgis import GIS
    
        item_fs = gis.content.get("10daa287ecc5449a9a78cb4353c860bc")       
                
        for n,inx in n_dict.items():
            
            if n == table:
                inx_table = inx                
                fs_lyr = item_fs.tables[inx]
                Nx_service = fs_lyr.query(where="año ='{}' AND mes = '{}'".format(year,month)).sdf               
            
                                                
    # Lógica para tablas N8 y N9
    
    elif table in ('N8','N9'):
                    
        if table == 'N8':
            item_fs = gis.content.get("d229559d280843088eedb819e937bfbd")
            fs_lyr = item_fs.tables[0]
            Nx_service = fs_lyr.query(where="año='{}' AND mes='{}'".format(year,month)).sdf
            
        elif table == 'N9':
            item_fs = gis.content.get("d229559d280843088eedb819e937bfbd")
            fs_lyr = item_fs.tables[1]
            Nx_service = fs_lyr.query(where="año='{}' AND mes='{}'".format(year,month)).sdf            
            
           
      
    print('Borrando {} registros, por favor espere...'.format(len(Nx_service)))
    
    for row in Nx_service.iterrows():        
          
        value_delete = row[1]['OBJECTID']
    
        fs_lyr.edit_features(deletes=str(value_delete))    
        
              
    print('Proceso Finalizado')           
    

def donwload_data():
    
    global Nx_service
    
    from arcgis import GIS
    from arcgis import features
    
    
    print('')
    print('Ingresar credenciales de acceso:')
    print('')
    
    portal = "https://www.arcgis.com"
    user = input('Usuario:  ')
    password = input('Contraseña:  ')
    
    print('')
    print('Conectando...')

    gis = GIS(portal, user, password)
    print('Conexión establecida')
            
    print('Accediendo a servicios en AGOL...')
    print('')
    
    
    #Exportar primer lote
        
    n_dict1 = {'N1':0,'N2':1,'N3':2,'N5':4,'N6':5,'N7':6}        
        
    item_fs1 = gis.content.get("10daa287ecc5449a9a78cb4353c860bc")       
                
    for n,inx in n_dict1.items():
            
        inx_table = inx                
        fs_lyr = item_fs1.tables[inx]
        Nx_service = fs_lyr.query().sdf 
        
        print('Exportado backup para {}'.format(n))
        
        Nx_service.to_excel('3_backup/'+n+'_backup.xlsx', sheet_name='data')
        
                
    #Exportar segundo lote
   
    n_dict2 = {'N8':0,'N9':1}
    
    item_fs2 = gis.content.get("d229559d280843088eedb819e937bfbd") 
    
    for n,inx in n_dict2.items():
            
        inx_table = inx                
        fs_lyr = item_fs2.tables[inx]
        Nx_service = fs_lyr.query().sdf 
        
        print('Exportado backup para {}'.format(n))
        
        Nx_service.to_excel('3_backup/'+n+'_backup.xlsx', sheet_name='data')        
        
        
    #Exportar capas Geo
    
    item_fs3 = gis.content.get("10daa287ecc5449a9a78cb4353c860bc") 
    fs_lyr = item_fs3.layers[0]
    Nx_service = fs_lyr.query().sdf
    
    print('Exportado backup para Establecimientos Penitenciarios')
        
    Nx_service.to_excel('3_backup/'+'Nx_establecimientos_penitenciarios'+'_backup.xlsx', sheet_name='data')
    
    item_fs3 = gis.content.get("d5a3fcb74ff04dbb9fc34164d90f43e5") 
    fs_lyr = item_fs3.layers[0]
    Nx_service = fs_lyr.query().sdf    
    
    print('Exportado backup para Paises')
        
    Nx_service.to_excel('3_backup/'+'Nx_paises'+'_backup.xlsx', sheet_name='data') 
    
    print("")
    print("")
    print('Listo, proceso de exportación finalizado')
    print("")
    print("")        
    

def user_operation():                 
             
    print('')
    print('Definir la operación que desea realizar:')
        
    input_user = input('''
                        [1] Borrar registros
                        [2] Descargar Respaldo
                ''')  
    
    if input_user == '1':
    
        print('')
        print('Usted ha seleccionado Borrar Registros')
        delete_table = input('''Indique el código sobre la tabla que desea borrar [Nx]
    
                                    Tablero de Establecimientos Penitenciarios

                                    [N1] Situación Jurídica, Edad y Sexo
                                    [N2] Capacidad y Estado de Hacinamiento
                                    [N3] Rango de Edad
                                    [N7] Nivel Académico

                                    Tablero de Población Penal

                                    [N5] Población Penal por Paises
                                    [N6] Población Penal Extranjera

                                    Tablero de Egresos e Ingresos

                                    [N8] Egresos
                                    [N9] Ingresos            
    
                                    ''')
          
        delete_year = input('Ingrese año que desea borrar: ')
        delete_month = input('Ingrese mes que desea borrar: ')
        
        if delete_month in list_month and len(delete_year) == 4:
        
            delete_data(input_user,delete_table,delete_year,delete_month)
    
        else:
        
            print('')
            print('Hay errores en la carga de Mes o Año, por favor vuelve a intentarlo...')
            
            user_operation()           
                                  
                                   
    elif input_user == '2':
    
        print('')
        print('Usted ha seleccionado Decargar Respaldo')
            
        donwload_data()                    
       
    else:
        print('El valor ingresado no es correcto, cierre la ventana y vuelva a comenzar')
        
        user_operation()                   
    
user_operation()
