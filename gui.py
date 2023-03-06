import sys
import tkinter as tk
from tkinter import messagebox

import main as prog

DEF_RES = '700x700'
DEF_BUT_WIDTH = 30
DEF_PADX = 10
DEF_PADy = 5


class windows(tk.Tk):
    varNameList = []
    # system = prog.System
    variables = []
    fuzzySet = []
    fuzzySetNameList = []
    rules = []
    inVars = []
    outVars = []
    weightedAvg = []
    varLowerList = []
    varUpperList = []
    varTypeList = []
    system = ''

    def startPageInput(self):
        sysName = self.inputtxt1.get('1.0', 'end-1c')
        sysDesc = self.inputtxt2.get('1.0', 'end-1c')
        self.system = prog.System(sysName, sysDesc)
        print(sysName)
        print(sysDesc)
        self.newWindow.destroy()
        self.mainMenu()

    def saveVariable(self):
        varName = self.varNameText.get('1.0', 'end-1c')
        if varName in self.varNameList:
            messagebox.showerror("Error", "Variable Name Already Exists!")
        else:
            self.varNameList.append(varName)
            varType = self.varType.get()
            lower = self.lowerText.get('1.0', 'end-1c')
            upper = self.upperText.get('1.0', 'end-1c')
            if not lower.isnumeric() or not upper.isnumeric():
                messagebox.showerror("Error", "Upper or Lower are not integers")
            else:
                self.variables.append(prog.Variable(varName, varType, int(lower), int(upper)))
                self.varLowerList.append(lower)
                self.varUpperList.append(upper)
                self.varTypeList.append(varType)
                list1 = tk.StringVar(value=self.varNameList)
                list2 = tk.StringVar(value=self.varLowerList)
                list3 = tk.StringVar(value=self.varUpperList)
                list4 = tk.StringVar(value=self.varTypeList)
                self.lst1 = tk.Listbox(self.frame,
                                       listvariable=list1)
                self.lst2 = tk.Listbox(self.frame,
                                       listvariable=list2)
                self.lst3 = tk.Listbox(self.frame,
                                       listvariable=list3)
                self.lst4 = tk.Listbox(self.frame,
                                       listvariable=list4)

                self.lst1.grid(column=0, row=4)
                self.lst2.grid(column=0, row=5)
                self.lst3.grid(column=1, row=5)
                self.lst4.grid(column=1, row=4)

                print(varName + " " + varType + " " + lower + " " + upper)

    def addNewFuzzySetTri(self):
        setName = self.setNameText.get('1.0', 'end-1c')
        self.fuzzySetNameList.append(setName)
        setType = "TRI"
        one = self.firstText.get('1.0', 'end-1c')
        two = self.secondText.get('1.0', 'end-1c')
        three = self.thirdText.get('1.0', 'end-1c')
        if not one.isnumeric() or not two.isnumeric() or not three.isnumeric():
            messagebox.showerror("Error", "One of the parameters is not integers")
        else:
            self.fuzzySet.append(prog.FuzzySet(setName, setType, [int(one), int(two), int(three)]))
            var = prog.searchForVariableByName(self.varName.get(), self.variables)
            var.appendFuzzySet(self.fuzzySet[-1])
            print(setName + ": " + setType + " " + self.varName.get())

    def addNewFuzzySetTrap(self):
        setName = self.setNameText.get('1.0', 'end-1c')
        self.fuzzySetNameList.append(setName)
        setType = "TRAP"
        one = self.firstText.get('1.0', 'end-1c')
        two = self.secondText.get('1.0', 'end-1c')
        three = self.thirdText.get('1.0', 'end-1c')
        four = self.fourthText.get('1.0', 'end-1c')
        if not one.isnumeric() or not two.isnumeric() or not three.isnumeric() or not four.isnumeric():
            messagebox.showerror("Error", "One of the parameters is not integers")
        else:
            self.fuzzySet.append(prog.FuzzySet(setName, setType, [int(one), int(two), int(three), int(four)]))
            prog.searchForVariableByName(self.varName.get(), self.variables).appendFuzzySet(
                prog.FuzzySet(setName, setType, [int(one), int(two), int(three), int(four)]))
            print(setName + ": " + setType + " " + self.varName.get())

    def startSimulation(self):
        self.crispValues = []
        isNum = True
        for entry in self.entryList:
            if not entry.get().isnumeric():
                isNum = False
        if isNum:
            for entry in self.entryList:
                self.crispValues.append(int(entry.get()))
            # call fuzz function
            print(self.crispValues)
            prog.fuzz(self.inVars, self.crispValues)
            prog.inference(self.rules)
            for outVar in self.outVars:
                self.weightedAvg.append(prog.defuzz(outVar))
            # self.weightedAvg = prog.defuzz(self.outVars)
            i = 0
            self.newWindow = tk.Toplevel(self.master)
            self.frame = tk.Frame(self.newWindow)
            self.newWindow.geometry(DEF_RES)
            for w in self.weightedAvg:
                tk.Label(self.frame, text="Weighted Average = " + str(w), font=("Arial", 16)).grid(column=0, row=i)
                i += 1
        else:
            messagebox.showerror("Error", "One of the crisp values is not integers")
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def showSys(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)
        self.label = tk.Label(self.frame, text="System Name: " + self.system.name, font=("Arial", 16))
        self.label2 = tk.Label(self.frame, text="Brief description: " + self.system.description, font=("Arial", 16))
        self.closeWindowButton = tk.Button(self.frame,
                                           text="Close",
                                           command=self.newWindow.destroy
                                           , width=DEF_BUT_WIDTH
                                           )
        self.label.grid(column=0, row=0, padx=DEF_PADX, pady=DEF_PADy)
        self.label2.grid(column=0, row=1, padx=DEF_PADX, pady=DEF_PADy)
        self.closeWindowButton.grid(column=0, row=2, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.geometry(DEF_RES)
        self.button1 = tk.Button(self.frame, text='New Fuzzy Logic System', width=DEF_BUT_WIDTH, command=self.startPage)
        self.button2 = tk.Button(self.frame, text='Quit', width=DEF_BUT_WIDTH, command=self.master.destroy)
        self.button1.pack(padx=DEF_PADX, pady=DEF_PADy)
        self.button2.pack(padx=DEF_PADX, pady=DEF_PADy)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def startPage(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)
        self.label = tk.Label(self.frame, text="System Name")
        self.label2 = tk.Label(self.frame, text="Brief description")
        self.inputtxt1 = tk.Text(self.frame,
                                 height=1,
                                 width=DEF_BUT_WIDTH)
        self.inputtxt2 = tk.Text(self.frame,
                                 height=5,
                                 width=DEF_BUT_WIDTH)
        self.takeInputButton = tk.Button(self.frame,
                                         text="Save",
                                         command=self.startPageInput,
                                         width=DEF_BUT_WIDTH
                                         )
        self.label.pack()
        self.inputtxt1.pack(pady=DEF_PADy)
        self.label2.pack()
        self.inputtxt2.pack(pady=DEF_PADy)
        self.takeInputButton.pack()
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def mainMenu(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)
        self.addVariableButton = tk.Button(self.frame,
                                           text="Add variables",
                                           command=self.addVariables,
                                           width=DEF_BUT_WIDTH
                                           )
        self.addFuzzySetButton = tk.Button(self.frame,
                                           text="Add fuzzy sets to an existing variable",
                                           command=self.addFuzzySet
                                           , width=DEF_BUT_WIDTH

                                           )
        self.addRulesButton = tk.Button(self.frame,
                                        text="Add rules",
                                        command=self.addRules
                                        , width=DEF_BUT_WIDTH
                                        )
        self.runSimulationButton = tk.Button(self.frame,
                                             text="Run the simulation on crisp values",
                                             command=self.runTheSimulation
                                             , width=DEF_BUT_WIDTH
                                             )
        self.showSysButton = tk.Button(self.frame,
                                       text="Show Fuzzy Logic System Info",
                                       command=self.showSys
                                       , width=DEF_BUT_WIDTH
                                       )
        self.addVariableButton.pack(pady=DEF_PADy)
        self.addFuzzySetButton.pack(pady=DEF_PADy)
        self.addRulesButton.pack(pady=DEF_PADy)
        self.runSimulationButton.pack(pady=DEF_PADy)
        self.showSysButton.pack(pady=DEF_PADy)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def addVariables(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)

        self.varType = tk.StringVar(value="IN")
        values = ['IN', 'OUT']
        self.label1 = tk.Label(self.frame, text="Enter the variable’s name")
        self.varNameText = tk.Text(self.frame,
                                   height=1,
                                   width=DEF_BUT_WIDTH)
        i = 0
        self.checkButton = tk.Checkbutton(self.frame, text="IN\OUT",
                                          variable=self.varType,
                                          onvalue="IN",
                                          offvalue="OUT")
        self.label2 = tk.Label(self.frame, text="Enter the range")
        self.lowerText = tk.Text(self.frame,
                                 height=1,
                                 width=5)
        self.upperText = tk.Text(self.frame,
                                 height=1,
                                 width=5)
        self.addButton = tk.Button(self.frame,
                                   text="Add Variable",
                                   command=self.saveVariable
                                   , width=DEF_BUT_WIDTH
                                   )
        self.closeWindowButton = tk.Button(self.frame,
                                           text="Close",
                                           command=self.newWindow.destroy
                                           , width=DEF_BUT_WIDTH
                                           )
        list1 = tk.StringVar(value=self.varNameList)
        list2 = tk.StringVar(value=self.varLowerList)
        list3 = tk.StringVar(value=self.varUpperList)
        list4 = tk.StringVar(value=self.varTypeList)
        self.lst1 = tk.Listbox(self.frame,
                               listvariable=list1)
        self.lst2 = tk.Listbox(self.frame,
                               listvariable=list2)
        self.lst3 = tk.Listbox(self.frame,
                               listvariable=list3)
        self.lst4 = tk.Listbox(self.frame,
                               listvariable=list4)

        self.lst1.grid(column=0, row=4)
        self.lst2.grid(column=0, row=5)
        self.lst3.grid(column=1, row=5)
        self.lst4.grid(column=1, row=4)
        self.label1.grid(column=0, row=0, pady=DEF_PADy)
        self.varNameText.grid(column=1, row=0, pady=DEF_PADy)
        self.checkButton.grid(column=1, row=1, pady=DEF_PADy)
        self.label2.grid(column=0, row=2, pady=DEF_PADy)
        self.lowerText.grid(column=1, row=2, pady=DEF_PADy)
        self.upperText.grid(column=2, row=2, pady=DEF_PADy)
        self.addButton.grid(column=0, row=3, pady=DEF_PADy)
        self.closeWindowButton.grid(column=1, row=3, pady=DEF_PADy)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def addFuzzySet(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)
        i = 0
        self.varName = tk.StringVar()
        vars = []
        for n in self.varNameList:
            vars.append(n)
        self.chooseVarLable = tk.Label(self.frame, text="Choose Variable: ")
        self.varName.set(vars[0])
        self.varDrop = tk.OptionMenu(self.frame, self.varName, *vars)
        self.doneButton = tk.Button(self.frame,
                                    text="Proceed",
                                    command=self.addFuzySettoVar
                                    , width=DEF_BUT_WIDTH
                                    )

        self.closeWindowButton = tk.Button(self.frame,
                                           text="Close",
                                           command=self.newWindow.destroy
                                           , width=DEF_BUT_WIDTH
                                           )
        self.chooseVarLable.grid(column=0, row=0, pady=DEF_PADy)
        self.varDrop.grid(column=1, row=0, pady=DEF_PADy)
        self.doneButton.grid(column=0, row=2, pady=DEF_PADy, padx=DEF_PADX)
        self.closeWindowButton.grid(column=1, row=2, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def addFuzySettoVar(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)

        self.triButton = tk.Button(self.frame,
                                   text="TRI",
                                   command=self.addFuzySettoVarTRI
                                   , width=DEF_BUT_WIDTH
                                   )
        self.trapButton = tk.Button(self.frame,
                                    text="TRAP",
                                    command=self.addFuzySettoVarTRAP
                                    , width=DEF_BUT_WIDTH
                                    )
        self.triButton.grid(column=1, row=0, pady=DEF_PADy)
        self.trapButton.grid(column=1, row=1, pady=DEF_PADy)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

        # print(self.name)

    def addFuzySettoVarTRI(self):
        self.newWindow.destroy()
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)
        self.newWindow.geometry(DEF_RES)
        self.newWindow.title("TRI")
        self.setNameLable = tk.Label(self.frame, text="Enter the fuzzy set name")
        self.setNameText = tk.Text(self.frame,
                                   height=1,
                                   width=10)
        self.setValueLable = tk.Label(self.frame, text="Enter the fuzzy set numbers")
        self.firstText = tk.Text(self.frame,
                                 height=1,
                                 width=5)
        self.secondText = tk.Text(self.frame,
                                  height=1,
                                  width=5)
        self.thirdText = tk.Text(self.frame,
                                 height=1,
                                 width=5)
        self.saveButton = tk.Button(self.frame,
                                    text="SAVE",
                                    command=self.addNewFuzzySetTri
                                    , width=DEF_BUT_WIDTH
                                    )
        self.closeButton = tk.Button(self.frame,
                                     text="Close",
                                     command=self.newWindow.destroy
                                     , width=DEF_BUT_WIDTH
                                     )
        self.setNameLable.grid(column=0, row=1, pady=DEF_PADy)
        self.setNameText.grid(column=1, row=1, pady=DEF_PADy)
        self.setValueLable.grid(column=0, row=2, pady=DEF_PADy)
        self.firstText.grid(column=0, row=3, pady=DEF_PADy)
        self.secondText.grid(column=1, row=3, pady=DEF_PADy)
        self.thirdText.grid(column=2, row=3, pady=DEF_PADy)
        self.saveButton.grid(column=0, row=4, pady=DEF_PADy, padx=DEF_PADX)
        self.closeButton.grid(column=1, row=4, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)
        print("TRI")

    def addFuzySettoVarTRAP(self):
        self.newWindow.destroy()
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)
        self.newWindow.geometry(DEF_RES)
        self.newWindow.title("TRAP")
        self.setNameLable = tk.Label(self.frame, text="Enter the fuzzy set name")
        self.setNameText = tk.Text(self.frame,
                                   height=1,
                                   width=10)
        self.setValueLable = tk.Label(self.frame, text="Enter the fuzzy set numbers")
        self.firstText = tk.Text(self.frame,
                                 height=1,
                                 width=5)
        self.secondText = tk.Text(self.frame,
                                  height=1,
                                  width=5)
        self.thirdText = tk.Text(self.frame,
                                 height=1,
                                 width=5)
        self.fourthText = tk.Text(self.frame,
                                  height=1,
                                  width=5)
        self.saveButton = tk.Button(self.frame,
                                    text="Save",
                                    command=self.addNewFuzzySetTrap
                                    , width=DEF_BUT_WIDTH
                                    )
        self.closeButton = tk.Button(self.frame,
                                     text="Close",
                                     command=self.newWindow.destroy
                                     , width=DEF_BUT_WIDTH
                                     )
        self.setNameLable.grid(column=0, row=1, pady=DEF_PADy)
        self.setNameText.grid(column=1, row=1, pady=DEF_PADy)
        self.setValueLable.grid(column=0, row=2, pady=DEF_PADy)
        self.firstText.grid(column=0, row=3, pady=DEF_PADy)
        self.secondText.grid(column=1, row=3, pady=DEF_PADy)
        self.thirdText.grid(column=0, row=4, pady=DEF_PADy)
        self.fourthText.grid(column=1, row=4, pady=DEF_PADy)
        self.saveButton.grid(column=0, row=5, pady=DEF_PADy, padx=DEF_PADX)
        self.closeButton.grid(column=1, row=5, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)
        print("TRAP")

    def addRules(self):
        self.setInVarList()
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry(DEF_RES)
        self.frame = tk.Frame(self.newWindow)
        self.newWindow.title("Rules")
        self.chooseVar1Lable = tk.Label(self.frame, text="Choose First Variable")
        self.chooseVar2Lable = tk.Label(self.frame, text="Choose Second Variable")
        self.chooseVar3Lable = tk.Label(self.frame, text="Choose OUT Variable")
        inVar = ['none']
        outVar = ['none']
        for varName in self.varNameList:
            print(varName)
            var = prog.searchForVariableByName(varName, self.variables)
            if var.variable_type == "IN":
                inVar.append(varName)
            else:
                outVar.append(varName)
        self.clickedFirst = tk.StringVar()
        self.clickedSecond = tk.StringVar()
        self.clickedThird = tk.StringVar()
        self.clickedFirst.set("none")
        self.clickedSecond.set("none")
        self.clickedThird.set("none")
        self.inDropFirst = tk.OptionMenu(self.frame, self.clickedFirst, *inVar)
        self.inDropSecond = tk.OptionMenu(self.frame, self.clickedSecond, *inVar)
        self.outDrop = tk.OptionMenu(self.frame, self.clickedThird, *outVar)
        self.doneButton = tk.Button(self.frame,
                                    text="Proceed",
                                    command=self.addCondition
                                    , width=DEF_BUT_WIDTH
                                    )
        self.close = tk.Button(self.frame,
                               text="Close",
                               command=self.newWindow.destroy
                               , width=DEF_BUT_WIDTH
                               )
        self.inDropFirst.grid(column=0, row=0, pady=DEF_PADy, padx=DEF_PADX)
        self.inDropSecond.grid(column=1, row=0, pady=DEF_PADy, padx=DEF_PADX)
        self.outDrop.grid(column=2, row=0, pady=DEF_PADy, padx=DEF_PADX)
        self.close.grid(column=2, row=2, pady=DEF_PADy, padx=DEF_PADX)
        self.doneButton.grid(column=0, row=2, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def addCondition(self):
        self.newWindow.destroy()
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)
        self.newWindow.geometry(DEF_RES)
        firstSet = []
        secondSet = []
        outSet = []
        self.condition = ['and', 'or', 'and_not', 'or_not']
        firstVariable = prog.searchForVariableByName(self.clickedFirst.get(), self.variables)
        secondVariable = prog.searchForVariableByName(self.clickedSecond.get(), self.variables)
        outVariable = prog.searchForVariableByName(self.clickedThird.get(), self.variables)
        for fl in firstVariable.fsList:
            firstSet.append(fl.name)
        for fl in secondVariable.fsList:
            secondSet.append(fl.name)
        for fl in outVariable.fsList:
            outSet.append(fl.name)
        self.firstSetVal = tk.StringVar()
        self.secondSetVal = tk.StringVar()
        self.outSetVal = tk.StringVar()
        self.conditionVal = tk.StringVar()
        self.firstSetVal.set("none")
        self.secondSetVal.set("none")
        self.outSetVal.set("none")
        self.conditionVal.set("and")
        self.firstSetLable = tk.Label(self.frame, text=self.clickedFirst.get() + ": ")
        self.conditionSetLable = tk.Label(self.frame, text="Condition: ")
        self.secondSetLable = tk.Label(self.frame, text=self.clickedSecond.get() + ": ")
        self.outSetLable = tk.Label(self.frame, text=self.clickedThird.get() + ": ")
        self.firstSetDrop = tk.OptionMenu(self.frame, self.firstSetVal, *firstSet)
        self.conditionDrop = tk.OptionMenu(self.frame, self.conditionVal, *self.condition)
        self.secondSetDrop = tk.OptionMenu(self.frame, self.secondSetVal, *secondSet)
        self.outSetDrop = tk.OptionMenu(self.frame, self.outSetVal, *outSet)
        self.proceedButton = tk.Button(self.frame,
                                       text="Proceed",
                                       command=self.addRule
                                       , width=DEF_BUT_WIDTH
                                       )
        self.close = tk.Button(self.frame,
                               text="Close",
                               command=self.newWindow.destroy
                               , width=DEF_BUT_WIDTH
                               )
        self.firstSetLable.grid(column=0, row=0, pady=DEF_PADy)
        self.conditionSetLable.grid(column=0, row=1, pady=DEF_PADy)
        self.secondSetLable.grid(column=0, row=2, pady=DEF_PADy)
        self.outSetLable.grid(column=0, row=3, pady=DEF_PADy)
        self.firstSetDrop.grid(column=1, row=0, pady=DEF_PADy)
        self.conditionDrop.grid(column=1, row=1, pady=DEF_PADy)
        self.secondSetDrop.grid(column=1, row=2, pady=DEF_PADy)
        self.outSetDrop.grid(column=1, row=3, pady=DEF_PADy)
        self.proceedButton.grid(column=0, row=4, pady=DEF_PADy, padx=DEF_PADX)
        self.close.grid(column=2, row=4, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def addRule(self):
        rule = self.clickedFirst.get() + " " + self.firstSetVal.get() + " " + self.conditionVal.get() + " " + self.clickedSecond.get() + " " + self.secondSetVal.get() + " => " + self.clickedThird.get() + " " + self.outSetVal.get()
        print(rule)
        self.rules.append(prog.Rule(str(rule)))

    def runTheSimulation(self):
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)

        self.newWindow.geometry(DEF_RES)
        self.newWindow.title("Simulation")
        tk.Label(self.frame, text="Enter the crisp").grid(column=0, row=0)
        self.entryList = []
        i = 1
        self.inVars = []
        self.outVars = []
        for varName in self.varNameList:
            var = prog.searchForVariableByName(varName, self.variables)
            if var.variable_type == "IN":
                self.entryList.append(tk.Entry(self.frame))
                self.entryList[-1].grid(column=1, row=i, pady=DEF_PADy, padx=DEF_PADX)
                tk.Label(self.frame, text=varName).grid(column=0, row=i, pady=DEF_PADy, padx=DEF_PADX)
                self.inVars.append(var)
                i += 1
            else:
                self.outVars.append(var)
        tk.Button(self.frame,
                  text="Start",
                  command=self.startSimulation
                  , width=DEF_BUT_WIDTH
                  ).grid(column=0, row=i + 1, pady=DEF_PADy, padx=DEF_PADX)
        tk.Button(self.frame,
                  text="Close",
                  command=self.newWindow.destroy
                  , width=DEF_BUT_WIDTH).grid(column=1, row=i + 1, pady=DEF_PADy, padx=DEF_PADX)
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def setInVarList(self):
        for varName in self.varNameList:
            var = prog.searchForVariableByName(varName, self.variables)
            if var.variable_type == "IN":
                self.inVars.append(var)
            else:
                self.outVars.append(var)
        prog.inList = self.inVars
        prog.outList = self.outVars


def main():
    root = tk.Tk()
    try:
        app = windows(root)
    except:
        messagebox.showerror("Error", sys.exc_info()[0])
    root.mainloop()


if __name__ == '__main__':
    main()
