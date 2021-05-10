import pprint
import csv

# this class is for setting the default settings
class Settings:

    def __init__(self):
        self.current_settings = {}
        self.availableSettings = """
        n  = no formatting
        wl = wikilink
        ml = markdown link
        hl = highlight
        it = italics
        bo = bold
        st = strike-through
        co = inline code
        cb = code block
        h1 = heading 1
        h2 = heading 2
        h3 = heading 3
        h4 = heading 4
        h5 = heading 5
        h6 = heading 6
        wlem = wiki link embed
        mlem = markdown link embed
        ul = unordered list
        ol = ordered list
        bq = block quote
        ut = unchecked task
        ct = checked task
        ma = inline math
        mb = math block
        oc = obsidian comments
        ta = tag
        """

        self.availableSettingsList = ["n", "wl", "ml", "hl", "it", "bo", "st", "co", "cb", "h1", "h2", "h3", "h4", "h5", "h6", "wlem", "mlem", "ul", "ol", "bq", "ut", "ct", "ma", "mb", "oc", "ta"]


    def setGeneralSettings(self):

        # checks if the user wants to add the contents as YAML metadata
        while True: 
            addYAML = input("Do you want to have all the entries as YAML metadata? Enter \"y\" for yes and \"n\" for no: ")
            addYAML = addYAML.lower().strip()
            if addYAML != "y" and addYAML != "n":
                print("You didn't enter \"y\" or \"n\"")
            elif addYAML == "y":
                self.current_settings["addYAML"] = "y"
                break
            elif addYAML == "n":
                self.current_settings["addYAML"] = "n"
                break
                        
        # set the delimiter
        while True: 
            delimiter = input("What delimiter do your CSV files have? (tab, comma, semicolon, colon, pipe, space) ")
            delimiter = delimiter.lower().strip()
            if delimiter != "tab" and delimiter != "comma" and delimiter != "semicolon" and delimiter != "colon" and delimiter != "pipe" and delimiter != "space":
                print("You didn't enter a valid delimiter")
            elif delimiter == "tab":
                self.current_settings["delimiter"] = "\t"
                break
            elif delimiter == "comma":
                self.current_settings["delimiter"] = ","
                break
            elif delimiter == "semicolon":
                self.current_settings["delimiter"] = ";"
                break
            elif delimiter == "colon":
                self.current_settings["delimiter"] = ":"
                break
            elif delimiter == "pipe":
                self.current_settings["delimiter"] = "|"
                break
            elif delimiter == "space":
                self.current_settings["delimiter"] = " "
                break

        while True: 
            fileNameLength = input("How long should the file name be at maximum? Please enter a number. This excludes the .md ending. ")
            fileNameLength = fileNameLength.strip()
            try:
                fileNameLength = int(fileNameLength)
                self.current_settings["fileNameLength"] = fileNameLength
                break
            except:
                print("The length was not an integer. Please try again.")

        while True: 
            fileNameCol = input("From which column should the file name be generated? (The first column has the number 1) ")
            fileNameCol = fileNameCol.strip()
            try:
                fileNameCol = int(fileNameCol)
                # decrement value by one to match index
                self.current_settings["fileNameCol"] = fileNameCol - 1
                break
            except:
                print("The column was not an integer. Please try again.")
        
        # to this the formattings of each column will be added
        self.current_settings["column"] = {}
        
        # returns the inputted settings so that they can be loaded by .choices() of GetInput class
        return self.current_settings



    def saveSettings(self, settings):
        name = input("Which name should your saved settings have? ")
        with open("saved_settings.py", "a") as f:
            f.write(f"{name.lower()} = " + pprint.pformat(settings) + "\n\n")
