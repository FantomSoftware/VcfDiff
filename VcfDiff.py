#-*-coding:utf8;-*-
#qpy:3
#qpy:console

# Script compares two VCF contact lists and create a diff.vcf as output
# Script is searching for phone numbers and use it for removing duplicities

#CONFIG:
vcfFile1 = "./Smaller.vcf"
vcfFile2 = "./Larger.vcf"
vcfOutFile ="./Diff.vcf"

#---------- program --------

import sys
import os

output_phoneNumber_prefix = 'TEL:'
fullname_prefix = 'FN:'
partialName_prefix = 'N:'
version_prefix = 'VERSION:'
vcf_phoneNumber_prefix_list = ['TEL;', output_phoneNumber_prefix]

#set current working dir on skript dir - for e.q.android
os.chdir(os.path.split(sys.argv[0])[0])

#should be talky?
verb = (len(sys.argv)>1 and sys.argv[1]=="-v")

# the real program starts here 

try: 
   vcf1 = open(vcfFile1, "r")
except IOError: 
   print ("Error: can\'t find file "+vcfFile1) 
   quit()

try: 
   vcf2 = open(vcfFile2, "r")
except IOError: 
   print ("Error: can\'t find file "+vcfFile2) 
   vcf2.close()
   quit()

def unifyNumber(tel):
    cleantel = ""
    tel = tel.replace("-", "")
    tel = tel.replace("(", "")
    tel = tel.replace(")", "")
    tel = tel.replace(" ", "")
    return tel

#scan for phone numbers and unify their format
#return list of them, possible with contact name, vcf version, part name and number type as line prefix
def scanForNumbers(oFile, fullItem):
    last_fullname = ''
    phoneList = []
    for line in oFile:
        if (line.startswith(fullname_prefix)):
            last_fullname = line
        if (line.startswith(partialName_prefix)):
        	   last_partialname = line
        if (line.startswith(version_prefix)):
            last_version = line
        if (any(substring in line for substring in vcf_phoneNumber_prefix_list)):
            if (line.find(":") > 0):
                last_number_tmp = line[line.find(":")+1:]
                last_number = unifyNumber(last_number_tmp)
                if (verb and last_number_tmp!=last_number):
                    print("Reformating "+last_number_tmp[:-1]+" to "+last_number[:-1])
                full_prefix = line[:line.find(":")]
                phoneList.append([last_number, last_fullname, full_prefix, last_partialname, last_version])
                if verb:
                    print(last_fullname, end='')
                    print(output_phoneNumber_prefix+last_number, end='')
    return phoneList

#scan in first and second file for contacts
list1 = scanForNumbers(vcf1, False)
if verb:
    print("Scanned "+vcfFile1+": "+str(len(list1))+" contacts")
list2 = scanForNumbers(vcf2, False)
if verb:
    print("Scanned "+vcfFile2+": "+str(len(list2))+" contacts")

vcf1.close()
vcf2.close()

#get key from single or list item - if list, then first single item
def getKey(item):
    if isinstance(item, (list,)):
        if (len(item)<1):
            return ""
        return getKey(item[0])
    else:
        return item

#make a diff of 2 lists - if more level list, compare by the first items
def diffLists(first, second):
    rList = []
    for item in first:
        new = True
        key1 = getKey(item)
        for item2 in second:
            key2 = getKey(item2)
            if len(key1)<9:
                if (key1 == getKey(item2)):
                    new = False
            else:
                if key1 in key2:
                    new = False
                if (len(key2)>8 and key2 in key1):
                    new = False
        if new:
            rList.append(item)
    return rList

def printVcf(vcfList):
    #[last_number, last_fullname, full_prefix, last_partialname, last_version])
    try: 
       vcfOut = open(vcfOutFile, "w")
    except IOError: 
       print ("Error: can\'t create file "+vcfOutFile) 
       quit()
    for item in vcfList:
        vcfOut.write("BEGIN:VCARD"+os.linesep)
        vcfOut.write(item[4][:-1]+os.linesep) 
        vcfOut.write(item[3][:-1]+os.linesep)
        vcfOut.write(item[1][:-1]+os.linesep)
        vcfOut.write(item[2]+":"+item[0][:-1]+os.linesep)
        vcfOut.write("END:VCARD"+os.linesep)
    vcfOut.close()

ld = diffLists(list2, list1)
printVcf(ld)

if verb:
    print(len(ld))
