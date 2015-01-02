#!/usr/bin/env python3
import argparse, json, string
import xml.etree.ElementTree as ET

akcja = []
spiker = None

def uosobienie(o):
    uo = ""
    for char in o:
        if char in string.ascii_letters:
            uo = uo + char
    return uo

def didaskalia(e):
    if len(e) > 0:
        akcja.append("didaskalia::%s" % e.text)
        for el in e:
            if el.tag == "osoba":
                akcja.append("dzialanie::%s::%s" % (el.text,el.tail))
    else:
        akcja.append("didaskalia::%s" % e.text)

def kwestia(e):
    outt = ""
    for strofa in e.findall("strofa"):
        outt = "%s%s" %(outt, strofa.text or "")
        for wers in strofa:
            outt = "%s%s" %(outt, wers.text or "")
            outt = "%s%s" %(outt, wers.tail or "")
    for wers in outt.split("/"):
        akcja.append("kwestia::%s::%s" % (spiker, wers))
    

parser = argparse.ArgumentParser()
parser.add_argument("lektura", type=str)
args = parser.parse_args()
dramat = ET.parse(args.lektura).find("dramat_wierszowany_l")
lista_osob = dramat.find("lista_osob")
if lista_osob is not None:
    for osoba in lista_osob.findall(".//osoba"):
        akcja.append("osoba::%s" % uosobienie(osoba.text))
for i in range(0,25):
    elem = dramat[i]
    if elem.tag in ["miejsce_czas","naglowek_akt","naglowek_scena"]:
        akcja.append("didaskalia::%s" % elem.text)
    if elem.tag in ["didaskalia"]:
        didaskalia(elem)
    if elem.tag == "naglowek_osoba":
        spiker = uosobienie(elem.text)
    if elem.tag == "kwestia":
        kwestia(elem)
print(json.dumps(akcja, indent=4))
with open("sztuka.json", 'w') as file:
    file.write(json.dumps(akcja, indent=4))
