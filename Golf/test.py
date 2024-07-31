# Imports
import sys
from lib import LIB
import PySimpleGUI as sg
import os
import pandas as pd

TITLE = "RS1 algorithm based on RST"

# File for exporting results
EXPORT_FILE = ''

#Input the dataset from a input.txt file
def ConsoleTest():
    flag = False
    while not flag:
        file_path = input("Please enter the complete correct file path of the dataset: \n")
        ch = (input("Press 'Y' to confirm \nPress 'N' to enter file path again \n")).upper()
        if ch == 'Y':
            flag = True
        elif ch == 'N':
            flag = False

    f = open(file_path, 'r', encoding='utf-8')
    rows = []
    for line in f:
        row = line.split()
        row[0] = str(row[0])
        row[1] = str(row[1])
        row[2] = str(row[2])
        rows.append(row)
    print (rows)

# Reading data from a text file
def read_text_from_file(file_path):
    try:
        with open(file_path) as f:
            rows = []
            for line in f:
                row = line.split()
                row[0] = str(row[0])
                row[1] = str(row[1])
                row[2] = str(row[2])
                rows.append(row)
            return rows
    except:
        print(f'Error reading file {file_path}')
        return ''

# GUI implementation
def main_window():
    sg.theme('SandyBeach')
    layout = [
        [sg.Text(TITLE, justification='center', font=("Helvetica", 24))],
        [sg.Text('_' * 92)],
        [sg.Text('Choose the file (.txt)', font=("Helvetica", 16))],
        [sg.InputText(size=(45, 1), key='file_path'), sg.FileBrowse('Open folder'), sg.Submit('Load data')],
        [sg.Text('<Weather, Temperature, Wind>, decision value: Play golf(Yes/No)')],
        [sg.Multiline(size=(90, 10), key='text')],
        [sg.Text('_' * 92)],
        [sg.Text('Please enter the value of the decisive attribute of dataset: '), sg.InputText(size=(42, 1), key='decision')],
        [sg.Button('Run the algorithm', button_color='ForestGreen', size = (80, 2))],
        [sg.Output(size=(90, 15), key='-OUTPUT-')],
        [sg.Text('_' * 92)],
        [sg.Text('Enter file name to export results: '), sg.InputText(size=(38, 1), key = 'export_file'), sg.Button('Export', size=(19, 1))],
        [sg.Cancel('Exit', button_color='OrangeRed', size = (80, 2))]
    ]

# Implementation of the program in response to user actions
    window = sg.Window(TITLE, layout)
    text = []
    df_flag = False
    export_text = ''
    decision_value = ''
    decisions = ['Yes', 'No']
    while True:
        event, values = window.read(timeout=400)
        # Implementation of closing program
        if event in (None, 'Exit', sg.WIN_CLOSED):
            sg.popup_ok("The program was closed\nSee you!")
            window.close()
            return None
        # Implementation of loading data into the program
        if event == 'Load data':
            df_flag = False
            window['text'].update('')
            window['-OUTPUT-'].update('')
            file_path = values.get('file_path')
            # Selecting the file path
            if not file_path:
                sg.popup_error('Select file path')
                continue
            # Checking for loading an empty file
            isempty = os.stat(file_path).st_size != 0
            if isempty == 0:
                sg.popup_error("Error! Loading an empty file!")
                continue
            # Dataset loading
            if file_path.endswith('.txt'):
                text = read_text_from_file(file_path)
                tmp = ''
                for i in range (len(text)):
                    tmp = tmp + str(text[i]) + "\n"
                window['text'].update(tmp)
                print("Dataset received")
            else:
                sg.popup_error('Only .txt format is supported!')
        
        # Implementation of algorythm RS1
        if event == 'Run the algorithm':
            decision_value = values.get('decision')
            # Checking for the input of a decisive attribute
            if (len(decision_value)) == 0:
                sg.popup_error('You didn\'t specify a decisive attribute')
            # Checking for the correctness of the input of the decisive attribute
            elif (values.get('decision') not in decisions):
                sg.popup_error("Incorrect input decision value! Try again")
                continue
            if text != []:
                window['-OUTPUT-'].update('')
                Test_dt = LIB(text,["Weather","Temperature","Wind"])
                output_res = ''
                print("Please standby\nThe RS1 algorithm is being launched ...")
                print('-' * 150)
                output_res += "U => " + str(Test_dt.getU()) + "\n"
                output_res += "X={x| Recruit(x)=" + str(f"<{decision_value}>") + "}" + " => " + str(Test_dt.getX(decision_value)) + "\n"
                output_res += "Va(Weather)" + str(Test_dt.getVa("Weather")) + "\n"
                output_res += "Va(Temperature)" + str(Test_dt.getVa("Temperature")) + "\n"
                output_res += "Va(Wind)" + str(Test_dt.getVa("Wind")) + "\n"
                output_res += "Vd" + str(Test_dt.getVd()) + "\n"
                output_res += "Va" + str(Test_dt.getVa()) + "\n"
                output_res += "IND(A)" + str(Test_dt.getIND()) + "\n"
                output_res += "Object\'s of LowerXA =>" + str(Test_dt.getLowerAX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "Object\'s of UpperXA =>" + str(Test_dt.getUpperAX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "POS(X)" + str(Test_dt.getPOSX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "BND(X)" + str(Test_dt.getBNDX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "NEG(X)" + str(Test_dt.getNEGX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += '-' * 150 + "\n"
                output_res += "Accuracy of Approximation: " + str(Test_dt.precision(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "Quality of classification: " + str(Test_dt.quality(Test_dt.getX(decision_value),Test_dt.getIND())) + " %" + "\n"
                output_res += "Roughness: " + str(Test_dt.roughness(Test_dt.getX(decision_value),Test_dt.getIND())) + " %" + "\n"
                output_res += '-' * 150 + "\n"
                output_res += "" + "\n"
                output_res += "Production rules for positive region for decision value: " + str(f"<{decision_value}>") + "\n"
                output_res += str(Test_dt.getRules(Test_dt.getPOSX(Test_dt.getX(decision_value),Test_dt.getIND()))) + "\n"
                output_res += "\nProduction rules for negative region for decision value: " + str(f"<{decision_value}>") + "\n"
                output_res += str(Test_dt.getRules(Test_dt.getNEGX(Test_dt.getX(decision_value),Test_dt.getIND()))) + "\n"
                output_res += "\nProduction rules for boundry region for decision value: " + str(f"<{decision_value}>") + "\n"
                output_res += str(Test_dt.getRules(Test_dt.getBNDX(Test_dt.getX(decision_value),Test_dt.getIND()))) + "\n"
                output_res += "" + "\n"
                output_res += "Reduction:" + str(Test_dt.getReduct())
                print(output_res)
            else:
                sg.popup_error('Enter input data!')
                continue

        if event == 'Export':
            if output_res == '':
                sg.popup_error('First, load/process the dataset')
                continue
            try:
                with open(values.get('export_file'), 'w') as f:
                    f.write(output_res)
            except:
                sg.popup_error(f'Error saving to file {EXPORT_FILE}')
            else:
                sg.popup_ok(f"The result is saved in " + values.get('export_file'))

if __name__ == "__main__":
    # ConsoleTest()
    main_window()
    sys.exit()