
import csv
import re
from settings import Settings
import os

if os.path.isfile("saved_settings.py"):
    print("saved_settings.py is already present")
else:
    with open("saved_settings.py", "w", encoding='utf-8') as f:
        f.write( "\"\"\"This is your settings file.\"\"\"\n\n")

from saved_settings import *

class GetInput:
    def __init__(self):
        self.settings:dict = {}


    def choices(self):
        # check if the user wants to load settings
        self.loadSettings:str = ""
        while True:
            self.loadSettings = input("Do you want to load saved settings? Enter \"y\" for yes and \"n\" for no: ")
            self.loadSettings = self.loadSettings.lower().strip()
            if self.loadSettings == "y":
                choice = input("Which settings do you want to choose? Please enter the name of the dictionary in saved_settings.py: ")
                choice = choice.lower().strip()
                # this will load the dictionary from saved_settings.py to the current settings
                # this works because we import everything from saved_settings
                self.settings = eval(choice)
                print(f"These are your selected settings: {self.settings}")
                break
            elif self.loadSettings == "n":
               instantiateSettings = Settings()
               # set the settings and load them
               # it calls the setGeneralSettings method in settings.py and lets the user choose all
               # the settings which are not related to the formatting of the content
               generalSettings = instantiateSettings.setGeneralSettings()
               self.settings = generalSettings
               print(f"These are your current general settings: {self.settings}")
               break
        self.mdChoices()


    def mdChoices(self):
        if self.settings["addYAML"] == "y":
            # instantiate ReadCreate for reading the CSV files
            instanceFile = ReadCreate(self.settings, True)
            if self.loadSettings == "n":
                print("Now you will set the formatting for all of the columns one by one.")
                instanceFile.getCellSettings()
            instanceFile.getYamlKeys()
            # creates the md files
            instanceFile.makeMdFiles()
        else:
            # instantiates the ReadCreate class and finds the csv files
            instanceFile = ReadCreate(self.settings, False)
            if self.loadSettings == "n":
                print("Now you will set the formatting for all of the columns one by one.")
                instanceFile.getCellSettings()
            # creates the md files
            instanceFile.makeMdFiles()
            

class ReadCreate:

    def __init__(self, settings:dict, yaml:bool=False):
        # will be populated with the contents of the first row of the first csv file as the values
        # the key is `yaml_keys`
        self.keyList:list = []
        self.yaml:bool = yaml
        self.csvFiles:list= [] 
        # instantiate appSettings with the GetInput class to get access to the user settings
        self.settings = settings


        # find the csv files in the current working directory
        for dirpath, dirnames, files in os.walk("."):
            #print(f"Found directory: {dirnames}, located here:{dirpath}")
            for file_name in files:
                if file_name.endswith(".csv"):
                    normalised_path = os.path.normpath(dirpath + "/" + file_name)
                    print(f"Found file: {file_name}")
                    # append each found csv file to the list of csv files
                    self.csvFiles.append(normalised_path)


    def getYamlKeys(self):
        self.keys:list = []
        with open(self.csvFiles[0], "r", encoding='utf-8') as csvFile:
            csvFileReader = csv.reader(csvFile, delimiter=self.settings["delimiter"])
            for row in csvFileReader:
                # puts all of the  keys for each file in a list
                # checks for the first row because that contains the names of the columns
                # should be redundant because I break after the first row anyway
                if csvFileReader.line_num == 1:
                    # is needed to make sure that the list of all available options is only shown for the first column of the first row
                    for el in range(len(row)):
                        self.keys.append(row[el])
                    # break so that it doesn't loop again
                    break

    def getCellSettings(self):
        # this method will add a key to self.settings 
        # the key is "column", the value is a dictionary that contains the column in index form as its key
        # and the formatting as its value in a list
        # the first value is the formatting; if the cell in the csv file contains a list (multiple values that should get the
        # formatting individually), the second element is "y" for yes and the third the separator for the list

        # needed for showing and checking the chosen formatting option for each cell
        # needed for saving the entered settings
        addMdSetting = Settings()
        with open(self.csvFiles[0], "r", encoding='utf-8') as csvFile:
            csvFileReader = csv.reader(csvFile, delimiter=self.settings["delimiter"])
            for row in csvFileReader:
                # checks for the first row because that contains the names of the columns
                # should be redundant because the first row is the first in the iterator and I break after the first row
                if csvFileReader.line_num == 1:
                    # is needed to make sure that the list of all available options is only shown for the first column of the first row
                    showOptions:int = 0
                    for el in range(len(row)):

                        # this indented part gets the settings for all of the columns
                        # only set the settings for the first csv file (assume that the others follow the same scheme)
                        cellFormatting:str = ""
                        inCellList:str = ""
                        separator:str = ""
                        # only show the options for the first element
                        if showOptions == 0:
                            print(addMdSetting.availableSettings)
                            print(f"The file used for setting the format for all csv files in the current working directory is \"{self.csvFiles[0]}\".")
                            showOptions += 1

                        # set the formatting of each cell
                        while True:
                            cellFormatting = input(f"How should the column \"{row[el]}\" be formatted? ")
                            cellFormatting = cellFormatting.lower().strip()
                            # check if the chosen formatting is valid
                            if cellFormatting in addMdSetting.availableSettingsList:
                                break
                        # asks whether a cell contains multiple elements that should be separately formatted
                        while True:
                            # don't ask whether the cell contains multiple values if there's no formatting to be applied
                            if cellFormatting == "n":
                                break
                            inCellList = input("Does this cell contain multiple values which should be separately formatted? \"y\" for yes and \"n\" for no: ")
                            if inCellList.lower() == "n":
                                break
                            elif inCellList.lower() == "y":
                                separator = input("How is your list separated? Please enter the character: ")
                                break
                            
                        # adds the formatting to self.settings with "column" as key
                        # the value is a dictionary, whose key is the index of the column and the cell formatting as string in a list as its value
                        if len(inCellList) > 0 and len(separator) > 0:
                            self.settings["column"][el] = [cellFormatting, inCellList, separator]
                        else:
                            self.settings["column"][el] = [cellFormatting]

                    # ask the user whether they want to save their settings in saved_settings.py
                    while True:
                        save_settings = input("Do you want to save these settings? Enter \"y\" for yes and \"n\" for no: ")
                        if save_settings.lower().strip() == "y":
                            addMdSetting.saveSettings(self.settings)
                            break
                        elif save_settings.lower().strip() == "n":
                            break
                        
                    # stop after the first row, so that it doesn't keep checking all the other rows after it
                    break
            

    def makeMdFiles(self):
        # create the data subdirectory to create the .md files there
        try:
            if not os.path.exists("./data/"):
                os.makedirs("./data/")
        except OSError:
            print ("Error: Creating directory.: ./data/")

        # loop through all of the csv files in the current directory and subdirectories
        for file in self.csvFiles:
            # open the current file in read mode
            with open(file, "r", encoding='utf-8') as currentFile:
                fileReader = csv.reader(currentFile, delimiter=self.settings["delimiter"])
                # goes through each row in the currently open file and applies the md settings, creates a md file for each row
                for row in fileReader:
                    # exlude the first row as it only includes the heading names
                    if fileReader.line_num != 1:
                        # contains all the formatted text which will be written to the md file
                        lst:list= []
                        # needed if YAML frontmatter is chosen to be written to the md files
                        unformattedLst:list = []
                        for el in range(len(row)):
                            # append the unformatted values to the list so that they can become 
                            # the YAML values
                            if self.yaml == True:
                                unformattedLst.append(row[el].strip("\"'"))

                            # retrieve the formatted strings for the main text
                            # checks if the current cell contains multiple values
                            if len(self.settings["column"][el]) > 1:
                                # split the list at the given separator and return their unique values
                                sublist:list = row[el].split(self.settings["column"][el][2])
                                # apply the formatting to each unique element
                                splitSublist:str = self.splitSubList(sublist, self.settings["column"][el][0])
                                lst.append(splitSublist)
                            else:
                                formattedText:list = self.returnFormatting(row[el], self.settings["column"][el][0])
                                # don't append empty cells
                                if formattedText != None:
                                    lst.append(formattedText)


                        # accesses the column that was selected for the file name
                        fileName:str = str(row[self.settings["fileNameCol"]])
                        # limit the file name to the specified length 
                        fileName = fileName[:self.settings["fileNameLength"]]
                        # create the final file name
                        fileName = "./data/" + re.sub(r"<|>|:|\"|/|\\|\||\?|\*|\[|\]", "", fileName)
                        
                        # checks whether there is already a file with the same file name
                        if os.path.isfile(fileName):
                            fileName = fileName + "_1"
                            while True:
                                counter:int = 2
                                if os.path.isfile(fileName):
                                    fileName = fileName[:-1] + str(counter)
                                    counter += 1
                                else:
                                    break

                        fileName += ".md"

                        try:
                            # creates a .md file in the data folder in append mode
                            with open (fileName, "a", encoding='utf-8') as f:
                                if self.yaml == True:
                                    yamlLst:list = []
                                    for idx, key in enumerate(self.keys):
                                        # replace UTF-8 BOM, should be handled better/perhaps with user option to specify the encoding of the csv file
                                        key = key.replace("\ufeff", "")
                                        # unpack if list and make separate values for the key in the YAML
                                        if len(self.settings["column"][idx]) > 1:
                                            yamlSubLst:list = unformattedLst[idx].split(self.settings["column"][idx][2])
                                            yamlSubStr:str = ""
                                            for el in yamlSubLst:
                                                if len(el) == 0:
                                                    continue
                                                else:
                                                    yamlSubStr += f"\"{el.strip()}\", "
                                            yamlSubStr = yamlSubStr.strip(", ")
                                            yamlLst.append(f"{key}: [{yamlSubStr}]")
                                        else:
                                            # make value null if there is no value for the key
                                            if len(unformattedLst[idx]) == 0:
                                                yamlLst.append(f"{key}: null")
                                            else:
                                                yamlLst.append(f"{key}: [\"{unformattedLst[idx]}\"]")
                                    f.write("---\n")
                                    f.write("\n".join(yamlLst))
                                    f.write("\n---\n")
                                    # write the rest of the file
                                    f.write("\n\n".join(lst))
                                # if YAML is not selected to be written, only the main content will be written
                                else:
                                    f.write("\n\n".join(lst))
                        except:
                            # remove the file that was erroneously created
                            if os.path.isfile(fileName):
                                os.remove(fileName)
                            # log the error to log.txt
                            with open("log.txt", "a", encoding='utf-8') as m:
                                m.write(fileName + " -- The contents of this file could not be written.\n")

    def splitSubList(self, sublist, formatting):
        sublist_str:str = ""
        for el in sublist:
            if len(el) == 0:
                continue
            else:
                sublist_str += self.returnFormatting(el.strip("\"' "), formatting) + "\n"
        return sublist_str.strip("\n")


    def returnFormatting(self, string, formatting):
        if len(string) > 0:
            if formatting == "n":
                return f"{string}"
            elif formatting == "wl":
                return f"[[{string}]]"
            elif formatting == "ml":
                return f"[{string}]({string})" 
            elif formatting == "hl":
                return f"=={string}=="
            elif formatting == "it":
                return f"*{string}*"
            elif formatting == "bo":
                return f"**{string}**"
            elif formatting == "st":
                return f"~~{string}~~"
            elif formatting == "co":
                return f"`{string}`"
            elif formatting == "cb":
                return f"```\n{string}\n```"
            elif formatting == "h1":
                return f"# {string}"
            elif formatting == "h2":
                return f"## {string}"
            elif formatting == "h3":
                return f"### {string}"
            elif formatting == "h4":
                return f"#### {string}"
            elif formatting == "h5":
                return f"##### {string}"
            elif formatting == "h6":
                return f"###### {string}"
            elif formatting == "wlem":
                return f"![[{string}]]"
            elif formatting == "mlem":
                return f"![{string}]({string})"
            elif formatting == "ul":
                return f"- {string}"
            elif formatting == "ol":
                return f"1. {string}"
            elif formatting == "bq":
                return f">{string}"
            elif formatting == "ut":
                return f"- [ ] {string}"
            elif formatting == "ct":
                return f"- [x] {string}"
            elif formatting == "ma":
                return f"${string}$"
            elif formatting == "mb":
                return f"$$\n{string}\n$$"
            elif formatting == "oc":
                return f"%%{string}%%"
            elif formatting == "ta":
                return f"#{string}"
        # return None if the passed cell value is empty
        else:
            return None





# instantiate GetInput class to start the script

startScript = GetInput()
startScript.choices()
print("The program has now finished. Check log.txt to see if there are any errors.")