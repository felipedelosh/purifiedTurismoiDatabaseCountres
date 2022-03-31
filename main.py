"""

This software is programed by felipedelosh 2022

To compatibilite between databases of turismoi... cactch a .txt with countries info
and output

1 -> All registers formated ()
2 -> Individual contries formated
3 -> Mauricio outputs (my boss)

"""
from tkinter import *
import os
from os import scandir


class Software:
    def __init__(self) -> None:
        self.screem = Tk()
        self.canvas = Canvas(self.screem, height=480, width=720, bg="snow")
        self.lblSoftware = Label(self.canvas, text="Este es el software para generar los datos de paises de Turismoi")
        self.lblChargeDataCountries = Label(self.canvas, text="1 -> Por favor cargue la informacion de los paises.")
        self.btnChargeDataCountries = Button(self.canvas, text="Load Countries", command=self.chargeInfoCountries)
        self.lblChargeDataCountriesStatus = Label(self.canvas, text="No se ha cargado la data")
        self.lblLoadInfoCity = Label(self.canvas, text="2 -> Por favor cargue la informacion de los paises.")
        self.btnLoadInfoCity  = Button(self.canvas, text="Load Cities", command=self.loadCityData)
        self.lblLoadInfoCityStatus = Label(self.canvas, text="No se ha cargado la data")
        self.lblFinalMessage = Label(self.canvas, text="Aun no se ha procesado la información")
        self.btnSAVEOUTPUT = Button(self.canvas, text="SAVE THE GAME", command=self.export_data)

        """System vars"""
        self.originalCountryData = ""
        self.originalCountryData2 = ""
        self.countryData = {}
        self.countryData2 = {}
        self.cityData = {}
        self.output = {} # A result of program
        self.specifed_mauricio_output = {}
        self.readyToSave = False
        self.txtFinalMessage = ""

        self.viewAndConfigure()

    def viewAndConfigure(self):
        self.screem.title("Data paises Turismoi")
        self.screem.geometry("720x480")

        self.canvas.place(x=0, y=0)

        self.lblSoftware.place(x=20, y=20)
        self.lblChargeDataCountries.place(x=20, y=50)
        self.btnChargeDataCountries.place(x=20, y=80)
        self.lblChargeDataCountriesStatus.place(x=180, y=85)
        self.lblLoadInfoCity.place(x=20, y=120)
        self.btnLoadInfoCity.place(x=20, y=150)
        self.lblLoadInfoCityStatus.place(x=180, y=155)
        self.lblFinalMessage.place(x=100, y=220)
        self.btnSAVEOUTPUT.place(x=200, y=400)
        

        self.screem.mainloop()

    def chargeInfoCountries(self):
        """Only load a txt"""
        print("Cargando info de los paises")
        try:
            path = os.getcwd() + "/DATA/paises.txt"
            f = open(path, 'r', encoding='UTF-8')
            self.originalCountryData = f.read()
            f.close()
  
            path = os.getcwd() + "/DATA/paises_host.txt"
            g = open(path, 'r', encoding='UTF-8')
            self.originalCountryData2 = g.read()
            g.close()

            self.lblChargeDataCountriesStatus['text'] = "Info cargada"
            self.lblChargeDataCountriesStatus['bg'] = "green"
            self._chargeInfoCountries()
        except:
            self.lblChargeDataCountriesStatus['text'] = "Error de INFO"
            self.lblChargeDataCountriesStatus['bg'] = "red"

    def _chargeInfoCountries(self):
        """
        The country data is save in dic
        """
        for i in self.originalCountryData.split("\n"):
            if len(str(i)) != 0:
                # Cacth a name of country
                country_name = str(i).split("|")[2].replace("\"", "")
                country_name = country_name.lower()
                # Add id to dictionary key country
                if not country_name in self.countryData:
                    # Save a DATA in country key
                    self.countryData[country_name] = i

        for i in self.originalCountryData2.split("\n"):
            if len(str(i)) != 0:
                country_id = str(i).split("|")[1]

                # Add id to dictionary key country
                if not country_id in self.countryData2:
                    # Save a DATA in country key
                    self.countryData2[country_id] = str(i).split("|")[3].lower()

    def loadCityData(self):
        print("Cargando los datos de las cuidades")
        try:
        
            if len(self.countryData) > 0:
                self.lblLoadInfoCityStatus['bg'] = "green"

                all_city_files = self._loadAllCityFileNames() # save al archive names of cities

                if len(all_city_files) > 0:
                    print("Se cargaron los namefiles de ciudades...")
                    self._loadCityData(all_city_files)
                else:
                    self.lblLoadInfoCityStatus['text'] = "Error fatal..."
                    self.lblLoadInfoCityStatus['bg'] = "red"


            else:
                self.lblLoadInfoCityStatus['text'] = "Carga primero los paises"
                self.lblLoadInfoCityStatus['bg'] = "yellow"

            
        except:
            self.lblLoadInfoCityStatus['text'] = "Error fatal"
            self.lblLoadInfoCityStatus['bg'] = "red"


    def _loadAllCityFileNames(self):
        path = os.getcwd() + "/DATA/DATAPAISES"
        filesNames = []
        for i in scandir(path):
            if i.is_file():
                if ".txt" in i.name:
                    filesNames.append(i.name)

        return filesNames

    def _loadCityData(self, filesNames):
        """
        Prepare data to output
        """
        for i in filesNames:
            if i != "otros.txt":
                country_name = str(i).replace(".txt", "")
                dic_keys = self.countryData.keys()
    
                if country_name in dic_keys:
                    self.txtFinalMessage = self.txtFinalMessage + "Cargada la info de: " + country_name + "\n"
                
                    # Charge all city data in country
                    try:
                        path = os.getcwd() + "/DATA/DATAPAISES/" + i
                        temp = open(path, 'r', encoding='UTF-8')
                        for j in temp.read().split("\n"):
                            if str(j) != "":
                                country_info = self.countryData[country_name]
                                city_info = j
                                # add this info to result
                                self.add_info_to_output(country_name, country_info, city_info)

                        temp.close()
                    except:
                        self.txtFinalMessage = self.txtFinalMessage + "Error cargando la data en : " + country_name + "\n"
                    
                else:
                    self.txtFinalMessage = self.txtFinalMessage + "Error en: " + country_name + "\n"
            else:
                try:
                    path = os.getcwd() + "/DATA/DATAPAISES/" + i
                    temp = open(path, 'r', encoding='UTF-8')
                    for j in temp.read().split("\n"):
                        if str(j) != "":
                            # Purified data
                            reg = j.split("|")
                            id_city = str(reg[1]).strip()
                            name_city = str(reg[2])
                            name_city = name_city.rstrip()
                            name_city = name_city.lstrip()
                            slug_city = str(reg[3])
                            slug_city = slug_city.rstrip()
                            slug_city = slug_city.lstrip()
                            latitude_city = str(reg[4]).strip()
                            longitude_city = str(reg[5]).strip()
                            region_id_city = str(reg[6]).strip()
                            city_state_id = str(reg[7]).strip()
                            district_city = str(reg[8]).strip()
                            
                            # Cacth country name
                            country_id = str(reg[9]).strip()
                            country_id = self.countryData2[country_id]

                            # Cacth city info
                            info = id_city+"|"+name_city+"|"+slug_city+"|"+latitude_city+"|"+longitude_city+"|"+region_id_city+"|"+city_state_id+"|"+district_city

                            try:
                                # Save info 
                                self.add_info_to_output(country_id, self.countryData[country_id], info)
                            except:
                                if country_id == "panamá":
                                    self.add_info_to_output(country_id, self.countryData['panama'], info)
                                
                                if country_id == "república dominicana":
                                    self.add_info_to_output(country_id, self.countryData['dominican republic'], info)
                                    
                                if country_id == "belice":
                                    self.add_info_to_output(country_id, self.countryData['belize'], info)

                                if country_id == "sudafrica":
                                    self.add_info_to_output(country_id, self.countryData['south africa'], info)
                            

                                print("advertencia en ", country_id)


            


                    self.txtFinalMessage = self.txtFinalMessage + "Cargada la info de los otros paises"+ "\n"
                    temp.close()
                except:
                    self.txtFinalMessage = self.txtFinalMessage + "Error en: OTROS" "\n"


        self.readyToSave = True
        self.lblFinalMessage['text'] = self.txtFinalMessage

    def add_info_to_output(self, key_country, country_info, city_info):
        # Personal output
        if key_country not in self.output:
            self.output[key_country] = []
            self.output[key_country].append(country_info+city_info)
        else:
            self.output[key_country].append(country_info+city_info)

        if key_country not in self.specifed_mauricio_output:
            self.specifed_mauricio_output[key_country] = []
            self.specifed_mauricio_output[key_country].append(city_info)
        else:
            self.specifed_mauricio_output[key_country].append(city_info)

        


    def export_data(self):
        "Generate a output in txt"
        if self.readyToSave:
            try:
                

                # Save all in .txt
                output = ""

                for i in self.output:
                    for j in self.output[i]:
                        output = output + j + "\n"

                allReg = open('allReg.txt', 'w', encoding='UTF-8')
                allReg.write(output)
                allReg.close()
            
                # Save all individual .txt
                for i in self.output:
                    tempSAVE = ""
                    for j in self.output[i]:
                        tempSAVE = tempSAVE + j + "\n"

                    path = os.getcwd() + "/allCountries"
                    tempFile = open(path+"/"+i+".txt", 'w', encoding='UTF-8')
                    tempFile.write(tempSAVE)
                    tempFile.close()

                # Save all to mauricio
                for i in self.specifed_mauricio_output:
                    tempSAVE = ""
                    for j in self.specifed_mauricio_output[i]:
                        tempSAVE = tempSAVE + j + "\n"
                    path = os.getcwd() + "/paraMauricio"
                    tempFile = open(path+"/"+i+".txt", 'w', encoding='UTF-8')
                    tempFile.write(tempSAVE)
                    tempFile.close()


                
            except:
                pass
        else:
            pass



s = Software()