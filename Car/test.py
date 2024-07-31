# Imports
import sys
from lib import LIB
import PySimpleGUI as sg
import os
import pandas as pd

TITLE = "RS1 algorithm based on RST"

# File for exporting results
EXPORT_FILE = ''

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
                row[3] = str(row[3])
                row[4] = str(row[4])
                row[5] = str(row[5])
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
        [sg.Text('<Buying, Maint, Doors, Persons, Lug_boot, Safety>, decision value: Class(unacc/acc/good/vgood)')],
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
            # Selecting the fiel path
            if not file_path:
                sg.popup_error('Select file path')
                continue
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
            if (len(decision_value)) == 0:
                sg.popup_error('You didn\'t specify a decisive attribute')
                continue    
            if text != []:
                window['-OUTPUT-'].update('')
                Test_dt = LIB(text,["Buying","Maint","Doors","Persons", "Lug_boot","Safety"])
                output_res = ''
                print("Please standby\nThe RS1 algorithm is being launched ...")
                print('-' * 150)
                output_res += "U => " + str(Test_dt.getU()) + "\n"
                output_res += "X={x| Class(x)=" + str(f"<{decision_value}>") + "}" + " => " + str(Test_dt.getX(decision_value)) + "\n"
                output_res += "Va(Buying)" + str(Test_dt.getVa("Buying")) + "\n"
                output_res += "Va(Maint)" + str(Test_dt.getVa("Maint")) + "\n"
                output_res += "Va(Doors)" + str(Test_dt.getVa("Doors")) + "\n"
                output_res += "Va(Persons)" + str(Test_dt.getVa("Persons")) + "\n"
                output_res += "Va(Lug_boot)" + str(Test_dt.getVa("Lug_boot")) + "\n"
                output_res += "Va(Safety)" + str(Test_dt.getVa("Safety")) + "\n"
                output_res += "Vd" + str(Test_dt.getVd()) + "\n"
                output_res += "Va" + str(Test_dt.getVa()) + "\n"
                output_res += "IND(A)" + str(Test_dt.getIND()) + "\n"
                output_res += "Object\'s of LowerXA =>" + str(Test_dt.getLowerAX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "Object\'s of UpperXA =>" + str(Test_dt.getUpperAX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "POS(X)" + str(Test_dt.getPOSX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "BND(X)" + str(Test_dt.getBNDX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
                output_res += "NEG(X)" + str(Test_dt.getNEGX(Test_dt.getX(decision_value),Test_dt.getIND())) + "\n"
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