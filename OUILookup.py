import getopt
import sys
import requests
from getmac import get_mac_address

def main():#Funcion main en donde se iniciara toda la logica del codigo

    fileName = "OUILookup.txt"
    argIpInput = None
    argMacInput = None
    fileVerification(fileName)

    try:
        #para tener opciones largas, es necesario colocar las opciones cortas respectivas,
        #aunque no se utilicen. En este caso: -r y -m
        options, args = getopt.getopt(sys.argv[1:],"i,m",['ip=','mac=','help'])
    except:
        print("Error: Parametros incorrectos.")
        uso()

    for opt, arg in options:
        if opt in ('--help'):
            uso()
        if opt in ('--ip'):
            argIpInput = arg
        elif opt in ('--mac'):
            argMacInput = arg

    if(argIpInput and argMacInput):
        print(f"Ingrese solo un parametro IP o MAC porfavor")
    elif(argIpInput == None and argMacInput == None):
        print(f"Debe ingresar un parametro IP o MAC, para más informacion usar el comando [OUILookup.py --help] en consola")    
    else:    
        if(argIpInput):
            mac_address_output = get_mac_address(ip = argIpInput)
            if(mac_address_output):
                vendorName = findByMac(mac_address_output)
                print(f"MAC address : {mac_address_output}\nVendor : {vendorName}")#BUSCAN EL VENDOR EN ARCHIVO MAC
            else:
                print(f"Error: ip({argIpInput}) is outside the host network")
        elif(argMacInput):     
            vendorName = findByMac(argMacInput)
            print(f"MAC address : {argMacInput}\nVendor : {vendorName}")

def fileVerification(fileName):#se verifica si el archivo de entrada ingresado existe, en caso contrario se descarga.
    try:
        inputFile = open(fileName)
        inputFile.close()
    except:
        print("Archivo OUILookup.txt no encontrado")
        print("Solicitando request para descargar el archivo...\n")
        try:
            OuiLookUpResponse = requests.get('https://gitlab.com/wireshark/wireshark/-/raw/master/manuf')
            createFile = open(fileName, "w", encoding="utf8")
            createFile.write(OuiLookUpResponse.text)
            createFile.close()
            print("Archivo OUILookup.txt descargado exitosamente\n")
        except:    
            sys.exit("Error al descargar el archivo, esto puede ser producto de que no hay una conexion a internet\no que existan problemas con la pagina proveedora del archivo")

def findByMac(macAddress):#Funcion para buscar una macAddress en el archivo(o base de datos) de direcciones mac
    if(len(macAddress) > 8):
        macAddressNetId = (macAddress[:8]).upper()
    else: macAddressNetId = (macAddress).upper()

    try:
        OuiLookUpResponse = requests.get('https://gitlab.com/wireshark/wireshark/-/raw/master/manuf')
        contenedor = OuiLookUpResponse.text.split("\n")
    except:    
        OuiLookUpFile = open(fileName , "r", encoding="utf8")
        contenedor =  OuiLookUpFile.readlines()
        OuiLookUpFile.close()

    for i in contenedor:
        i = i.strip("\n")
        aux_1 = i.split('\t')
        if(str(aux_1[0]) == str(macAddressNetId)):
            return aux_1[2] 

    return "Not found"  

def uso():#Funcion para usar con el comando --help y mostrar como funcionan los parametros
    print("Uso: " + sys.argv[0] + " --ip <ip address> || --mac <mac address> [--help] ")
    print("\nParametros:")
    print("     --ip: specify the IP of the host to query(ej: OUILookup.py --ip 192.168.0.6)")
    print("     --mac: specify the MAC address to query(ej: OUILookup.py --mac f8:28:19:46:2f:b9)")
    print("     --help: muestra esta pantalla y termina. Opcional")
    exit(1)

main()