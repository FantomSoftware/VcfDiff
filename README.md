# VcfDiff
Script compares two VCF contact lists and create a diff.vcf as output with diff
Script is searching for phone numbers and use it for removing duplicities

Search for CONFIG section at the begining of the script to setup it.

#CONFIG:
vcfFile1 = "./Smaller.vcf"
vcfFile2 = "./Larger.vcf"
vcfOutFile ="./Diff.vcf"

Script support -v parametr to be verbous
