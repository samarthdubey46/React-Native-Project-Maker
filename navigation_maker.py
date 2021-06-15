import os
import sys
import copy

keyWords = [
    "Bottom",
    "Drawer",
    "Stack",
]
if_template = ['if (name) {\n', '\n', '    return (\n', '        <Navigator.Navigator>\n', '\n', '\n',
               '        </Navigator.Navigator>\n', '    )\n', '}']

with_stack_template = [ '\n', 'const Feed_ = (props) => {\n', '\treturn(\n', '\t\t<Stack.Navigator>\n', '\n', '\t\t</Stack.Navigator>\n', '\t)\n', '}\n']
stack_temp__ = 'let Stack = createStackNavigator()\n'
def getIns(name):
    return f"() => navigation.navigate('{name}')"

def returnWithQuotes(string:dict):
    return f"'{string['name']}'"

def make_dirs(s, screen_path, templateFile, under_stack):
    lasd = []
    cwd = os.getcwd()
    lines = []
    with open(templateFile, 'r') as file:
        lines = file.readlines()
    for i in s:
        if not os.path.exists(os.path.join(screen_path, i)):
            os.makedirs(os.path.join(screen_path, i))
        lasd.append(os.path.join(screen_path, i))
    for i in range(len(lasd)):
        with open(os.path.join(lasd[i], 'index.js'), 'w') as file1:
            lines[3] = f"const {s[i]} = ({'{' + 'navigation,route' + '}'}) => {'{'}\n"
            lines[-1] = f"export default {s[i]}"
            lines[6] = f"\t\t\t<Text>{s[i]}</Text>\n"
            # for j in under_stack:
            #     if j != s[i]:
            #         lines.insert(7,f'\t\t\t<Button title="{j}" onPress={"{" +  getIns(j) + "}"} />\n')

            for i in lines:
                file1.write(i)
            with open(templateFile, 'r') as file:
                lines = file.readlines()


def getWhite_Spaces(string: str):
    spaces = 0
    for i in string.rstrip():
        if i == " ":
            spaces += 1
    return spaces


def getInput(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    return lines


def inKeyWord(string: str):
    res = ''.join([i for i in string if not i.isdigit()])
    # print(res)
    return res in keyWords


def NotinKeyWord(string: str):
    res = ''.join([i for i in string if not i.isdigit()])
    # print(res)
    return res not in keyWords


def checkIfInStack(screens, navigators):
    temp = []
    for i in screens:
        if navigators[i['inside']] == "Stack" and NotinKeyWord(i['name']):
            temp.append(i['name'])
    return temp


def getOnlyScreens(screens):
    temp = []
    for i in screens:
        if NotinKeyWord(i['name']):
            temp.append(i['name'])
    return temp


def returnWithCurlyBraces(string: str):
    return "{" + string + "}"


def ShouldReturnIconType(IconType: str, isExpo: bool):
    if isExpo:
        return ''
    return f"type='{IconType}'"


def returnIconType_name(string: str = "", isExpo: bool = False, Icons=set()):
    Icon_Options = string.split(',')
    Options = {}
    for i in Icon_Options:
        key, value = i.split(':')
        Options[key] = value
    # IconName = Icon_Options[0]
    # IconType = Icon_Options[1]
    IconName = Options['name']
    IconType = Options['type']
    color = "color" if 'color' not in Options.keys() else Options['color']
    size = "size" if "size" not in Options.keys() else Options['size']
    Icons.add(IconType)
    s = '{focused,color,size}'
    return_str = f'({s}) => <{IconType if isExpo else "Icon"} name="{IconName}" {ShouldReturnIconType(IconType, isExpo)}  color={"{" + color + "}"} size={"{" + size + "}"} />'
    return return_str


Special_Options = {'tabBarIcon': returnIconType_name}


def ObjectToString(object: dict):
    string = ""
    for key, value in object.items():
        tempString = f"{key} : {value},"
        string += tempString
    return returnWithCurlyBraces(string)


def GetScreenOptions(string: str, isExpo: bool, navigator: str, Icons: set = set()):
    # Home=>icon=name:heart,type:AntDesign;title=green
    string = string.strip()
    Icon = 'none'
    Type = 'none'
    ScreenName = 'none'
    Options = string.split("=>")
    if len(Options) == 1:
        return Options.pop(0), 'none'
    ScreenName = Options.pop(0)
    Options = Options[0].split(';')
    Final_Options = {}
    for option in Options:
        name, value = option.split('=')
        Final_Options[name] = value if name not in Special_Options.keys() else Special_Options[name](value, isExpo,
                                                                        Icons)
    return ScreenName, Final_Options


def GetNavigator_Import_Name(Navigator_name_without_digit):
    Navigator_Name = ''
    if Navigator_name_without_digit == "Stack":
        Navigator_Name = "let Navigator = createStackNavigator()\n"
    if Navigator_name_without_digit == "Bottom":
        Navigator_Name = "let Navigator = createBottomTabNavigator()\n"
    if Navigator_name_without_digit == 'Drawer':
        Navigator_Name = "let Navigator = createDrawerNavigator()\n"
    return Navigator_Name


def make_navigation(screenPath, templatePath, isExpo):
    # InitialLizing Variables
    Screen_Names = []
    Final_Screen_Objects = []
    Navigators = []
    Levels = []
    Current_Level = 0
    Navigator_Stack = [0]
    # Getting Input
    lines = getInput('layout.yaml')
    Options_Screens = []
    Options_Nav = []
    Icons = set()
    States = []
    FinalStates = {}
    CurrentState = 'none'
    With_Stack = []
    # Getting Levels,Screen,Navigaotrs
    for index, single_line_ in enumerate(lines):
        single_line = single_line_.replace('@','')
        spaces = getWhite_Spaces(single_line)
        name_without_spaces = single_line.strip()
        count = str(Navigators.count(name_without_spaces))
        if name_without_spaces[-1] == '-':
            CurrentState = name_without_spaces
            # continue
        if name_without_spaces == 'endif':
            CurrentState = 'none'
            # continue
        ScreenName_temp, Options1 = GetScreenOptions(name_without_spaces, isExpo, 'none', Icons)
        Options = 'none'
        if Options1 != 'none':
            Options = ObjectToString(Options1)
        if ScreenName_temp in Navigators:
            ScreenName_temp += count
        if index != 0:
            Options_Screens.append(Options)
            Screen_Names.append(ScreenName_temp)
            Levels.append(spaces)
            States.append(CurrentState)
        if inKeyWord(ScreenName_temp):
            Options_Nav.append(Options1)
            Navigators.append(ScreenName_temp)
            With_Stack.append(True if single_line != single_line_ and ScreenName_temp.replace(count,'') == "Bottom" else False)

    nav_index = 1

    # Debugging
    # for LevelName,ScreenName in zip(Levels,Screen_Names):
    #     print(f"{ScreenName} => {LevelName}")

    # Making The Final Screens List
    for LevelNumber, ScreenName, Options_Screen, State in zip(Levels, Screen_Names, Options_Screens, States):

        while Current_Level > LevelNumber:
            Navigator_Stack.pop()
            Current_Level -= 4
        path = f"../Screens/{ScreenName}"
        if inKeyWord(ScreenName):
            path = f"./{ScreenName}"
        if ScreenName == "endif":
            continue
        # ScreenName_from_object_func,objects = GetScreenOptions()
        if ScreenName in States:
            FinalStates[ScreenName.replace('-', "")] = Navigator_Stack[-1]
            continue
        Screen_Object_To__Be_appended = {'name': ScreenName, 'inside': Navigator_Stack[-1], 'path': path,
                                         'options': Options_Screen, 'inState': State}
        Final_Screen_Objects.append(Screen_Object_To__Be_appended)
        if inKeyWord(ScreenName):
            Navigator_Stack.append(nav_index)
            nav_index += 1

        Current_Level = LevelNumber
    States_Lines_To_Be_Written = {i: [] for i in range(len(Navigators))}
    States_Names_With_Navigator_Index = {i: [] for i in range(len(Navigators))}
    Navigators_Names = {i: '' for i in Navigators}
    for i, j in zip(Navigators_Names.keys(), Options_Nav):
        line = '\t\t<Navigator.Navigator'
        if j != 'none':
            for z, k in j.items():
                line += f" {z}={returnWithCurlyBraces(k)}"
        line += '>\n'
        Navigators_Names[i] = line

    for key, value in FinalStates.items():
        States_Names_With_Navigator_Index[value].append(key)
        States_Lines_To_Be_Written[value].append(f'\tconst [{key},change{key}] = useState(false)\n')
    for j, i in enumerate(Final_Screen_Objects):
        if i['inState'] != 'none' and i['inState'].replace('-', "") not in States_Names_With_Navigator_Index[
            i['inside']]:
            Final_Screen_Objects[j]['inState'] = 'none'

    # Can Comment Below TO Stop Work

    # Making The Screens
    underStack = checkIfInStack(Final_Screen_Objects, Navigators)
    onlyScreens = getOnlyScreens(Final_Screen_Objects)
    make_dirs(onlyScreens, screen_path, templateFile, underStack)

    # Making Navigation Folder
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, 'navigation')):
        os.mkdir(os.path.join(current_dir, 'navigation'))
    OriginalNavigation_Lines = []
    with open('navigation_template.js') as navigation_templapte_file:
        Navigation_Template_Lines = navigation_templapte_file.readlines()
    # Making The Navigation Files
    for navigator_index, Single_Navigator in enumerate(Navigators):
        Navigator_name_without_digit = ''.join([i for i in Single_Navigator if not i.isdigit()])
        Navigator_Import_Line = GetNavigator_Import_Name(Navigator_name_without_digit)
        Navigator_Component_Name = f"const {Single_Navigator} = (props) => {'{'}\n"
        FinalExportLine = f"export default {Single_Navigator}"
        Imports = []
        Components = []
        Should_Add_Screens_With_Stack = With_Stack[navigator_index]
        With_Stack_Lines = ''
        Component_With_If = {i: [] for i in States_Names_With_Navigator_Index[navigator_index]}
        # Looping Through Every Screen Object Which Is Inside The Current Navigator
        for ScreenIndex, ScreenObject in enumerate(Final_Screen_Objects):
            if ScreenObject['inside'] != navigator_index:
                continue
            import_Line = f"import {ScreenObject['name']} from '{ScreenObject['path']}'\n"
            Component_To_Written_Line = f'\t\t\t\t<Navigator.Screen options={returnWithCurlyBraces(ScreenObject["options"])} name="{ScreenObject["name"]}" component={returnWithCurlyBraces(ScreenObject["name"] if not Should_Add_Screens_With_Stack else ScreenObject["name"] + "_")}/>\n\n'
            if ScreenObject['inState'] == 'none':
                if ScreenObject['options'] != 'none':
                    Component_To_Written_Line = f'\t\t\t\t<Navigator.Screen name="{ScreenObject["name"]}" options={returnWithCurlyBraces(ScreenObject["options"])} component={returnWithCurlyBraces(ScreenObject["name"] if not Should_Add_Screens_With_Stack else ScreenObject["name"] + "_" )}/>\n\n'
                Components.append(Component_To_Written_Line)
            else:
                # pass
                if ScreenObject['inState'].replace('-', "") in Component_With_If.keys():
                    Component_With_If[ScreenObject['inState'].replace('-', "")].append(Component_To_Written_Line)
            Imports.append(import_Line)
            if Should_Add_Screens_With_Stack:
                with_stack_template[1] = f"const {ScreenObject['name']}_ = (props) => {'{'}\n"
                with_stack_template[4] = f'\t\t\t<Stack.Screen component={returnWithCurlyBraces(ScreenObject["name"])} name="{ScreenObject["name"]}_" options={"{" + returnWithCurlyBraces(f"title:{returnWithQuotes(ScreenObject)}") + "}"}/>\n'
                With_Stack_Lines += '\t'.join(with_stack_template)
        IfLines = ''
        for key, value in Component_With_If.items():
            if_template_copy = copy.deepcopy(if_template)
            if_template_copy[3] = Navigators_Names[Single_Navigator]
            if_template_copy[0] = f'\tif ({key}) {"{"}\n'
            line_ind = 5
            for component in value:
                if_template_copy.insert(line_ind, component)
            IfLines += '\t'.join(if_template_copy) + '\n'

        # Writing In Final Navigation_Template_List
        If_ElseStatements_Line = 16 
        Stack_Lines_Number =  10
        Imports_Writing_Number = 3
        States_Writing_Line_No = 15
        Component_Writing_Number = 23
        Navigation_Template_Lines[19] = Navigators_Names[Single_Navigator]
        Navigation_Template_Lines[-1] = FinalExportLine
        Navigation_Template_Lines[12] = Navigator_Component_Name
        Navigation_Template_Lines[8] = Navigator_Import_Line
        if Should_Add_Screens_With_Stack:
            Navigation_Template_Lines[9] = f'\t{stack_temp__}'
        Navigation_Template_Lines.insert(If_ElseStatements_Line, IfLines)
        Navigation_Template_Lines.insert(Stack_Lines_Number,With_Stack_Lines)

        for State_Line in States_Lines_To_Be_Written[navigator_index]:
            Navigation_Template_Lines.insert(States_Writing_Line_No, State_Line)
            States_Writing_Line_No += 1
        if isExpo:
            Navigation_Template_Lines[1] = f"import {returnWithCurlyBraces(','.join(Icons))} from '@expo/vector-icons'\n"
        for ComponentLine in Components:
            Navigation_Template_Lines.insert(Component_Writing_Number, ComponentLine)
            Component_Writing_Number += 1
        for ImportLine in Imports:
            Navigation_Template_Lines.insert(Imports_Writing_Number, ImportLine)
            Imports_Writing_Number += 1

        # Writing It To The File
        with open(os.path.join(current_dir, os.path.join('navigation', Single_Navigator + '.js')), 'w') as file:
            file.writelines(Navigation_Template_Lines)

        with open('navigation_template.js') as navigation_templapte_file:
            Navigation_Template_Lines = navigation_templapte_file.readlines()
    To_Be_Written_In_App = ["import React from 'react'\n", "import { View, Text, Dimensions } from 'react-native'\n",
                            "import { NavigationContainer } from '@react-navigation/native'\n",
                            f"import Main from './src/navigation/{Navigators[0]}'\n", 'const App = (props) => {\n',
                            '  \n', '  return (\n', '    <NavigationContainer>\n', '      <Main/>\n',
                            '    </NavigationContainer>\n', '  )\n', '}\n', 'export default App']
    with open('../App.js', 'w') as file:
        file.writelines(To_Be_Written_In_App)


templateFile = os.path.join(os.getcwd(), 'template.js')
screen_path = os.path.join(os.getcwd(), 'Screens')
IsExpo = sys.argv[1]
if (IsExpo.strip() == "0"):
    IsExpo = False
elif IsExpo.strip() == "1":
    IsExpo = True
make_navigation(screen_path, templateFile, IsExpo)
# print()
