import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import sys
import time




def create_project(name,isExpo:bool):
    to_be_installed = [
            "@react-native-community/masked-view",
            "@react-navigation/bottom-tabs",
            "@react-navigation/drawer",
            "@react-navigation/native",
            "@react-navigation/stack",
            "react-native-dynamic-vector-icons",
            "react-native-gesture-handler",
            "react-native-reanimated",
            "react-native-safe-area-context",
            "react-native-screens",
            "react-native-vector-icons"
        ]
    


    if not isExpo:

        os.system(f'react-native init {name}')

    if isExpo:
        os.system(f'expo init {name}')
        to_be_installed.remove('react-native-vector-icons')
        to_be_installed.append('@expo/vector-icons')

    path = os.path.join(os.getcwd(),name) 
    if not isExpo:
        gradle_copied = '\napply from: "../../node_modules/react-native-vector-icons/fonts.gradle"'
        android_path = os.path.join(path,os.path.join('android','app'))
        gradle_path = os.path.join(android_path,'build.gradle')
        with open(gradle_path,'a') as file:
            file.write(gradle_copied)
    src_path = os.path.join(path,'src')
    os.mkdir(src_path)
    files = [
        "navigation_template.js",
        "navigation_maker.py",
        "template.js",
        'layout.yaml'
    ]
    for i in files:
        os.system(f'cp {i} {src_path}')
    os.chdir(src_path)
    os.system(f'python3 navigation_maker.py {"1" if isExpo else "0"}')
    for i in files:
        os.system(f'rm {i}')
    os.chdir(path)
    sd = ""
    for i in to_be_installed:
        sd += i + " "
    print(sd)
    if isExpo:
        os.system(f'expo install {sd} ')
    else:
        os.system(f'yarn add {sd} ')
    print("Made A React Native Project")
if(len(sys.argv) == 3):
    name = sys.argv[1]
    isExpo = False
    isdds = sys.argv[2]
    if isdds == "expo":
        isExpo = True   
    create_project(name,isExpo)
else:
    name = input("Enter The Name Of The App ")
    isExpo = False
    isdds = input("expo or react-native ")
    if isdds == "expo":
        isExpo = True
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    print(file_path)
    files = [
        "navigation_template.js",
        "navigation_maker.py",
        "template.js",
        'layout.yaml',
        'react_native_project.py'
    ]
    if(file_path != os.getcwd()):
        for i in files:
            os.system(f'cp {i} {file_path}')
        os.chdir(file_path)
        os.system(f'python3 react_native_project.py {name} {isdds}')
        for i in files:
            os.system(f'rm {i}')
    else:
        os.system(f'python3 react_native_project.py {name} {isdds}')

