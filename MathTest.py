#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# PROCESSOR made in 2012
# This program allows dynamic mathematical processing.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from rabbit.all import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class tester(mathbase):
    """Implements The Math Tester."""
    def __init__(self, cancalc=True, debug=False):
        """Initializes The Math Tester."""
        self.debug = bool(debug)
        self.startup()
        self.cancalc = bool(cancalc)
        self.root = Tkinter.Tk()
        rootbind(self.root, self.complete)
        self.root.title("Math Tester")

        self.frameA = Tkinter.Frame(self.root, height=36, width=60)
        self.frameA.pack(side="left")
        self.main = console(self.frameA, "Enter The Name Of A Problem Set:", height=34, width=60)
        self.main.dobind()
        self.mainbox = entry(self.main, width=60)
        self.mainbox.dobind(self.answerer)
        self.stats = console(self.frameA, "Loading Records...", height=1, width=60, side="top")
        self.stats.dobind()

        self.frameB = Tkinter.Frame(self.root, height=36, width=40)
        self.frameB.pack(side="right")
        self.app = console(self.frameB, "Enter A Calculator Command:", width=40)
        self.app.dobind()
        self.box = entry(self.app, width=40)
        self.box.dobind(self.screen)

        self.interface = None
        self.module = ""
        self.populator()
        self.printdebug(": ON")
        self.records = getfile("Records.txt")
        self.header = ""
        self.alldata = {"":(0,0)}
        for line in readfile(self.records).split("\n"):
            if line.startswith("#"):
                self.header += line+"\n"
            elif line != "":
                k, v = line.split(":")
                v = delspace(v).replace("+","").split("-")
                self.alldata[k] = int(v[0]),int(v[1])

    def getrecords(self):
        """Retreives Records From The File."""
        if self.module == "":
            self.stats.display("Module Has Been Unloaded.")
        elif self.module in self.alldata:
            self.stats.display("Records For "+str(self.module)+" Loaded Succesfully.")
        else:
            self.alldata[self.module] = 0, 0
            self.stats.display("No Records Were Found For "+str(self.module)+".")

    def norecord(self):
        """Clears The Records."""
        self.alldata[self.module] = 0, 0
        self.upstats()

    def upstats(self):
        """Updates The Statistics Display Box."""
        n, t = self.alldata[self.module]
        if n+t == 0:
            self.stats.display("Number Correct: 0  --  Percent Correct: 0.0%  --  Total Score: 0.0")
        else:
            p = 100.0*float(n)/float(n+t)
            s = int(round(float(n)*p))
            p = round(p, 2)
            self.stats.display("Number Correct: "+str(n)+"  --  Percent Correct: "+str(p)+"%  --  Total Score: "+str(s))

    def complete(self, event=None):
        """Saves And Closes."""
        out = self.header
        for k in self.alldata:
            if k != "":
                a,b = self.alldata[k]
                out += str(k)+": +"+str(a)+" -"+str(b)+"\n"
        writefile(self.records, out)
        self.records.close()
        self.root.destroy()

    def screen(self, event=None):
        """Checks To See If The Calculator Is Enabled."""
        if self.cancalc:
            self.handler(event)
        else:
            self.main.display("The Calculator Is Currently Disabled.")

    def disable(self):
        """Disables The Calculator."""
        if self.cancalc:
            self.main.display("The Calculator Has Been Disabled.")
            self.cancalc = False

    def enable(self):
        """Enables The Calculator."""
        if not self.cancalc:
            self.main.display("The Calculator Has Been Reenabled.")
            self.cancalc = True

    def answerer(self, event=None):
        """Handles A Return Event."""
        original = basicformat(self.mainbox.output())
        if original == "clear":
            self.norecord()
        elif original == "exit":
            self.interface = None
            self.main.display("Enter The Name Of A Problem Set:")
            self.module = ""
            self.getrecords()
        elif self.interface == None:
            if original != "":
                try:
                    impclass = dirimport(original).interface
                except IOError:
                    self.main.display("Please Enter A Valid Problem Set.")
                else:
                    impclass.Hook = self
                    self.interface = impclass()
                    self.main.display("Problem Set Loaded Successfully.")
                    self.module = original
                    self.getrecords()
                    self.ask()
        elif self.interface.check(original):
            self.main.display("Correct!")
            a,b = self.alldata[self.module]
            self.alldata[self.module] = a+1,b
            self.ask()
        else:
            self.main.display("Incorrect; Try Again.")
            a,b = self.alldata[self.module]
            self.alldata[self.module] = a,b+1
            self.upstats()
                
    def ask(self):
        """Asks A Question."""
        self.upstats()
        self.main.display("\n"+str(self.interface.new()))

if __name__ == "__main__":
    tester().start()
