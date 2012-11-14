#!/usr/bin/python
# -*- coding: UTF-8
# Author: David Acacio
# Email: dacacioa@gmail.com

#import propios de python
import re,sys,os

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

#Bloque de programa


def cabecera():
	server = str(os.popen("hostname").readlines())
	server = server.replace("['","")
	server = server.replace("\\n\']","")
	os.system("clear")
	print "OpMenu"
	print "ServerName -- > "+bcolors.WARNING + server + bcolors.ENDC
	print "========================================================================================================================"
	
def titulo(texto):
	print bcolors.OKBLUE + "Menu: " + bcolors.HEADER +  texto + bcolors.ENDC + "\n"

def opcion(numero, texto):
	print bcolors.FAIL + "\t" +numero + "  "+bcolors.ENDC +  texto 
	
def executa(opciones):
	seleccio = raw_input("Choose option -> ")
	
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
					#print ("Ejecutamos " + opciones[int(seleccio)])
					#print os.system (opciones[int(seleccio)])
					os.system (opciones[int(seleccio)])
					#print os.popen(opciones[int(seleccio)]).readlines()
					#raw_input ("Presioni INTRO per continuar")
				readfile(n.getMenu())

	except ValueError:

		raw_input("Opci� no v�lida. Pulsi Intrada per continuar... ")
		readfile(n.getMenu())

	except IndexError:

		raw_input("Opci� no v�lida. Pulsi Intrada per continuar... ")
                readfile(n.getMenu())

def readfile(fichero):
#lee fichero .mnu 	

	try:
		menufile = file(str(fichero))
		printmenu(menufile)

	except IOError:
		exit

def printmenu(menu):
#printa menu
	orden = 0
	opciones =[]
	cabecera()
	for line in menu:
		linea = line.replace("\n","")
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
				if linea.find("q per ") == -1:
					#print ("Opcion " + str(orden) + " " + linea)
					#if linea.find(":") == -1:
					opcion (str(orden),linea)
					orden = orden + 1
	print ("\nPremi q per Sortir")
	print "========================================================================================================================"
	
	executa(opciones)

n = navegacion()
n.addMenu('main.mnu')
readfile(n.getMenu())

