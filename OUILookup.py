import getopt
import sys

try:
  import requests
  from getmac import get_mac_address
except:
  print("Error when importing necessary libraries  to make the program work, it will proceed to start the intallation of these\n")
  import subprocess
  subprocess.call(['pip', 'install', "-r","requeriments.txt"])
  print("Libraries were installed to execute the program\n")
  sys.exit("Please restart the program")

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
        print("\nError: Incorrect parameters.")
        uso()

    for opt, arg in options:
        if opt in ('--help'):
            uso()
        if opt in ('--ip'):
            argIpInput = arg
        elif opt in ('--mac'):
            argMacInput = arg
     
    if(argIpInput and argMacInput):
        print(f"Please, enter only one IP or MAC parameter")
    elif(argIpInput == None and argMacInput == None):
        uso()
    else:    
        if(argIpInput):
            mac_address_output = get_mac_address(ip = argIpInput)
            if(mac_address_output):
                vendorName = findByMac(fileName, mac_address_output)#BUSCAN EL VENDOR EN ARCHIVO MAC
                print(f"MAC address : {mac_address_output}\nVendor : {vendorName}")
            else:
                print(f"Error: ip({argIpInput}) is outside the host network")
        elif(argMacInput):     
            vendorName = findByMac(fileName, argMacInput)
            print(f"MAC address : {argMacInput}\nVendor : {vendorName}")

def fileVerification(fileName):#se verifica si el archivo de entrada ingresado existe, en caso contrario se descarga.
    try:
        inputFile = open(fileName)
        inputFile.close()
    except:
        print("File OUILookup.txt not found")
        print(" Executing request to download the file...\n")
        try:
            OuiLookUpResponse = requests.get('https://gitlab.com/wireshark/wireshark/-/raw/master/manuf')
            createFile = open(fileName, "w", encoding="utf8")
            createFile.write(OuiLookUpResponse.text)
            createFile.close()
            print("OUILookup.txt file downloaded successfully\n")
        except:    
            sys.exit("Error when downloading the file, may be occasionated due there is no internet connection\nor there's a problem with the file's provider website")

def findByMac(fileName, macAddress):#Funcion para buscar una macAddress en el archivo o en el sitio web(o base de datos) de direcciones mac
    if(len(macAddress) > 8):#Se ve si la longitud de la mac es mayor a 8 debido a que tendria mas de 6 digitos(contando los separadores ":")
        macAddressNetId = (macAddress[:8]).upper()
    else: macAddressNetId = (macAddress).upper()

    try:#se hace un request para poder obtener el contenido mas actualizado de las direcciones mac
        OuiLookUpResponse = requests.get('https://gitlab.com/wireshark/wireshark/-/raw/master/manuf')
        contenedor = OuiLookUpResponse.text.split("\n")
    except:#en caso de fallar el request se utiliza el archivo OUILookup.txt para realizar la busqueda del fabricante   
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
    print("\nUse in Windowns: OUILookup.py" + " --ip <ip address> | --mac <mac address> [--help] ")
    print("\nUse in Linux/Mac: ./OUILookup.py" + " --ip <ip address> | --mac <mac address> [--help] ")
    print("\nParameters:")
    print("     --ip: specify the IP of the host to query(ej: OUILookup.py --ip 192.168.0.6)")
    print("     --mac: specify the MAC address to query(ej: OUILookup.py --mac f8:28:19:46:2f:b9)")
    print("     --help: Display these instructions and finish")
    exit(1)

main()