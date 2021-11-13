# from statistics import mean
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import pyautogui as pg
import time
import webbrowser as web
import sqlite3


app = Flask(__name__)
# from Nuevo_tp import alertando

CORS(app)
# resources = {r"/buscando/*": {"origins": "http://localhost"}})


# from flask_restful import Resource, Api
# from sqlalchemy import create_engine


@app.route('/consultas', methods = ['GET'])
def consultar():
    import sqlite3
    conexion = sqlite3.connect("consultaprecios.db")
    cursor = conexion.cursor()
    sentenciaSQL = cursor.execute("SELECT precioalerta FROM tablaclientes")
    resultado = cursor.fetchall()
    for resultadox in resultado:
        print(resultadox)
    conexion.commit()
    return jsonify("Lo minimo que la gente esta dispuesta a pagar por una propiedad es:", min(resultado))


#Examen 05/07/21 - EJERCICIO 3

@app.route('/borrados', methods = ['DELETE'])
def borrar(nombre):
    import sqlite3
    conexion = sqlite3.connect("consultaprecios.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tablaclientes where clientes = (?)", nombre )
    conexion.commit()
    return jsonify("El cliente ha sido eliminado de la base de datos")

@app.route('/buscando', methods = ['POST'])
def alertando_post():
    nombre = request.json["nombre"]
    link_cliente = request.json["link"]
    precio_alerta = request.json["precioalerta"]
    whatsapp = request.json["numero"]
    #Aca va el nombre que le pusimos al formulario en el front
    alertando(nombre, link_cliente, precio_alerta, whatsapp)

    return jsonify("Funciona")

def alertando(nombre, link_cliente, precio_alerta, whatsapp):
    url = requests.get(link_cliente)
    soup = BeautifulSoup(url.content,"html.parser")
    resultado = soup.find("span", {"class":"price-tag-fraction"}) #la posta
    precioInicio_text = resultado.text
    precioInicial = float(precioInicio_text)
    # whatsapp = float(whatsapp)
    '''Esto lo estamos haciendo en particular para meli pq el precio lo da en numeros con coma chicos'''
    precioInicial = precioInicial * 1000
    precio_alerta = float(precio_alerta)
#----------------
    url2 = "https://api-dolar-argentina.herokuapp.com/api/dolarblue"
    r = requests.get(url2)
    datos = r.json()
    precio_dolar_compra = datos['compra']
    precio_dolar_venta = datos['venta']
    # print(precio_dolar_compra)
    # print(precio_dolar_venta)
    ''' Aca estamos transformando de str a float el precio de el dolar para poder manipularlo'''
    a = precio_dolar_compra
    float(a)
    dolar_compra_float = int(float(a))
    b = precio_dolar_venta
    float(b)
    dolar_venta_float = int(float(b))
#--------------

    '''Aca estamos conviertiendo el precio que nos dio en cliente en pesos a dolares y lo redondemos a dos decimales'''
    precio_whatsapp = round((precioInicial * dolar_venta_float),2)
    '''Aca estamos pasando el precio del cliente convertido en dolares a str para poder concatenarlo en el mensaje de wapp'''
    a2= precio_whatsapp
    str(a2)
    preciowappstr = str(a2)
# Scrapping para mandar mensaje de whatsapp
    if precioInicial < precio_alerta:
        phone_no= str(whatsapp)
        parsedMessage=("Hola " + nombre + ", soy Carla de Yo te aviso." '\n'"Tu casa bajo de precio, el precio en pesos es $"+ preciowappstr + " . No dudes mas, compralo YA!" '\n'+ link_cliente)
        web.open('https://web.whatsapp.com/send?phone='+'+549'+phone_no+'&text='+parsedMessage)
        time.sleep(8)
        for i in range(2):
            pg.write('')
            pg.press('enter')
            print('Mensaje #'+str(i+1)+' enviado')
            pass
    else:
        print("Por el momento no bajo del precio esperado")

    conexion = sqlite3.connect("consultaprecios.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO tablaclientes VALUES (?,?,?,?)", (nombre, link_cliente, precio_alerta, whatsapp))
    conexion.commit()












if __name__ == '__main__':
    app.run(debug= True, port=4000)







