from csvmng.csvmng import CSVManager 


print("\n***** Creo un oggetto che processa il mio file *****")
CSV_mng = CSVManager("file.csv")

print("\n***** Stampo il data frame ottenuto con pandas *****")
print(CSV_mng.getData())

print("\n***** Stampo la colonna \"Hire Date\" del data frame *****")
print(CSV_mng.getDataByProperty("Hire Date"))

print("\n***** Stampo il primo elemento della colonna \"Hire Date\" *****")
print(CSV_mng.getDataByProperty("Hire Date")[0])


print("\n***** Stampo l'intero dataframe come una lista *****")
print(CSV_mng.getDataAsList())

print("\n***** Stampo la colonna \"Hire Date\" come una lista *****")
print(CSV_mng.getDataByPropertyAsList("Hire Date"))

print("\n***** Stampo la colonna \"Hire Date\" come una lista usando un ciclo for *****")
list = CSV_mng.getDataByPropertyAsList("Hire Date")
for i in list:
	print(i)
