#!/usr/bin/python
# -*- coding: UTF-8
# Author: David Acacio
# Email: dacacioa@gmail.com

#Bloque de login

import logging
	
logger = logging.getLogger('opmenu')
hdlr = logging.FileHandler('/logs/system/gomenu/opmenu.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


#import propios de python
import re,sys,os,subprocess,commands

#clases propias

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class navegacion:
	menu = []
	
	def addMenu(self,opcion):
	#guarda opcion de menu en el array para poder guardar el menu de navegacion
		self.menu.append(str(opcion))	

	def getMenu(self):
		return str(self.menu[len(self.menu)-1])
	
	def getMenuAnt(self):
		try:
			anterior= self.menu.pop()
			return str(self.menu[len(self.menu)-1])
		except IndexError:
			return 1
	def printruta(self):
		ruta = ""
		contador = 0
		for i in self.menu:
			if (ruta == ""):
				ruta = str(self.menu[contador])
			else:
				ruta = ruta + " -> " + str(self.menu[contador])
			contador = contador + 1
		return str(ruta)
			
#Bloque de programa


def cabecera():
	server = str(os.popen("hostname").readlines())
	server = server.replace("['","")
	server = server.replace("\\n']","")
	mapa = n.printruta()
	os.system("clear")
	print "PyOpeMenu"
	print "Server --> " +bcolors.WARNING + server + bcolors.ENDC
	print "Mapa --> " + bcolors.OKGREEN + mapa + bcolors.ENDC
	print "========================================================================================================================"
	
def titulo(texto):
	print
	print bcolors.OKBLUE + "Menu: " + bcolors.HEADER +  texto + bcolors.ENDC
	print

def opcion(numero, texto):
	print bcolors.FAIL + "\t" +numero + "\t"+bcolors.ENDC +  texto 
	
def executa(opciones):
	seleccio = raw_input("Si us plau, tria una opció -> ")
	try:	
		if (seleccio == "q"):
			
			readfile(n.getMenuAnt())
		

		else:
			if ( seleccio != "0"):
				seleccio = int(seleccio) - 1
				tipo = opciones[int(seleccio)].split(".")
				if str(tipo[-1]).find("mnu") != -1:
					n.addMenu(opciones[int(seleccio)])
					#print tipo[-1]
					#raw_input (n.getMenu())
					#readfile(n.getMenu())
				else:
					comando = str((opciones[int(seleccio)])) 
					#print comando
					os.system (comando)
				readfile(n.getMenu())

	except ValueError:

		raw_input("Opció no vàlida. Pulsi Intrada per continuar... ")
		readfile(n.getMenu())

	except IndexError:

		raw_input("Opció no vàlida. Pulsi Intrada per continuar... ")
                readfile(n.getMenu())

def readfile(fichero):
#lee fichero .mnu 	

	try:
		menufile = file(str(fichero))
		printmenu(menufile)

	except IOError:
		#raw_input (str(fichero))
		if (str(fichero) == "1"):
			os.system("clear")
			exit
		else:
			readfile(n.getMenuAnt())	

def printmenu(menu):
#printa menu
	orden = 0
	opciones =[]
	cabecera()
	for line in menu:
		linea = str(line)
		linea = linea.replace("Premi q per Sortir\n","")
		linea = linea.replace(":", "")
		linea = linea.replace("\n","")
		if linea.find("MENU ") != -1:
			#print ("Opcion de menu" + line)			
			palabras = linea.split(" ")
			opciones.append(palabras[-1])
		elif (linea.find("sudo") != -1) or (linea.find(".sh") != -1):
			opciones.append(linea)
		else:
			if (orden==0):
				#print ("Titulo " + linea)
				titulo (linea)
				orden = orden + 1
			else:
				#print ("Opcion " + str(orden) + " " + linea)
				if len(linea) > 0:
					opcion (str(orden),linea)
					orden = orden + 1
	print
	print ("Premi q per Sortir")
	print "========================================================================================================================"
	print
	
	executa(opciones)

try:
	n = navegacion()
	n.addMenu('main.mnu')
	readfile(n.getMenu())

except KeyboardInterrupt:

	print "Bye"
