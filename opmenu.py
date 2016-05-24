#!/usr/bin/python
# -*- coding: UTF-8
# Author: David Acacio
# Email: dacacioa@gmail.com

## Contributions:
# Author: Jose Luis Bermudez
# Email: jl.bermudez@gmail.com
# 
# * Check logfile exist and create it if not.
# * Translate all non english literals.
# * Adding and check actionlog.

#import python class library
import re,sys,os,subprocess,commands,logging,i18n,getpass


# INTERNACIONALIZACIÓN.
reload(sys)
#sys.setdefaultencoding("utf-8")

_ = i18n.language.ugettext #use ugettext instead of getttext to avoid unicode errors

INSTALL_PATH = os.getcwd()+'/' #by default the current working directory. Modify string value if you want to change it
USER = getpass.getuser()

## Check logfile, if don´t exist create it.

#LOGDIR='/logs/system/gomenu'	## not standard path.

LOGDIR='/var/log'    ## dir location compatible all linux distributions.
LOGFILE=LOGDIR + '/opmenu.%s.log' % USER
bLog = True

try:
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)

    if os.path.isfile(LOGFILE): 
        print _("File exists")
    else:
        with open(LOGFILE,'a') as filelog:
    	    filelog.close();

except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    LOGDIR='/tmp'	# Alternative to the log directory, users without permissions can not generate log in /var/log.
    LOGFILE=LOGDIR + '/opmenu.%s.log' % USER
    with open(LOGFILE,'a') as filelog:
        filelog.close();
except:
    print _("Unknown error")
    bLog = False

## End check logfile.

if bLog:
    logger = logging.getLogger('opmenu')
    hdlr = logging.FileHandler(LOGFILE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

#own classes

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

#Print columns 

def generateColumns():
	rows, columns = os.popen('stty size', 'r').read().split()
	print "=" * int(columns)
	
#Bloque de programa


def cabecera():
	server = str(os.popen("hostname").readlines())
	server = server.replace("['","")
	server = server.replace("\\n']","")
	mapa = n.printruta().replace(".mnu","")
	os.system("clear")
	print "PyOpeMenu"
	print _("Server") + " --> " +bcolors.WARNING + server + bcolors.ENDC
	print _("Map") + " --> " + bcolors.OKGREEN + mapa + bcolors.ENDC
	generateColumns()	
	
def titulo(texto):
	print
	print bcolors.OKBLUE + "Menu: " + bcolors.HEADER +  texto + bcolors.ENDC
	print

def opcion(numero, texto):
	print bcolors.FAIL + "\t" +numero + "\t"+bcolors.ENDC +  texto 
	
def executa(opciones):
	seleccio = raw_input( _("Please select an option.") + " -> ")
	
	runcomand = False
	
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
					runcommand = False
					comando = str((opciones[int(seleccio)]))
					if ( comando.find("requestconfirm") != -1 ):
						comando = comando.replace('requestconfirm','')
						if ( query_yes_no( _("Are you sure?") , "no") ):
							runcomand = True
					else:
						runcomand = True
				
					if ( runcomand ):
						if bLog:
							logger.info (os.getenv('SSH_CLIENT','') + ' ' + os.getenv('USER','') + ' ' + comando)
						os.system (comando)

				readfile(n.getMenu())

	except ValueError:
		if bLog:
		    logger.warning (os.getenv('SSH_CLIENT','') + ' ' + os.getenv('USER','') + ' ' + _("Invalid value option. Enter to continue...") )
		raw_input( _("Invalid value option. Enter to continue... ") )
		readfile(n.getMenu())

	except IndexError:
		if bLog:
		    logger.warning (os.getenv('SSH_CLIENT','') + ' ' + os.getenv('USER','') + ' ' + _("Invalid index option. Enter to continue... ") )
		raw_input( _("Invalid index option. Enter to continue... ") )
                readfile(n.getMenu())

def readfile(fichero):
#lee fichero .mnu 	

	try:
		menufile = file(INSTALL_PATH + str(fichero))
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
		linea = linea.replace( _("Press \"q\" to exit.\n") ,"")
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
	print ( _("Press \"q\" to exit.\n") )
	generateColumns()
	print
	
	executa(opciones)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError( _("invalid default answer:") + " '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write( _("Please respond with 'yes' or 'no' ") + "(or 'y' or 'n').\n")

try:
	if bLog:
        	logger.info(os.getenv('SSH_CLIENT','') + ' ' + os.getenv('USER','') + ' ' + _("Entering the opmenu") )
	n = navegacion()
	n.addMenu('main.mnu')
	readfile(n.getMenu())
	if bLog:
		logger.info(os.getenv('SSH_CLIENT','') + ' ' + os.getenv('USER','') + ' ' + _("Leaving the opmenu") )

except KeyboardInterrupt:
	if bLog:
        	logger.info(os.getenv('SSH_CLIENT','') + ' ' + os.getenv('USER','') + ' ' + _("Leaving the opmenu (Interrupt)") )
	print _("Bye")
