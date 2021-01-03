## React Native Project Maker


**What is React Native Project Maker**
	We all know as a react-native developer how frustrating it can be to make all the navigation and screens over and over again, so to speed up the process you can use this, you just have to type the layout of your app, and the python script will make the whole app, either for expo or for vanilla react-native using react-navigation v5

**Requirements**

 - React-Native or expo accroding to your use
 - Python 3+
 - tkinter

**How To Get Started**

 1. Install Python
 2. Install tkinter 
 3. Clone the repository
 4. Start editing the layout file and the react_native_project.py script
 5. After that you may see a dialog box for selecting the file location, select the location then your project will be ready for starting
 
 **How to write the layout file**
 Here is an example layout.yaml file
 The indent is 4 spaces

    Drawer
		Stack=>screenOptions={headerBackTitle:'s'}
			IsLogged-
			@Bottom=>screenOptions={unmountOnBlur:true}
				Screen1=>tabBarIcon=name:newspaper,type:FontAwesome5;title='sa'
				Screen2=>tabBarIcon=name:ios-fitness,type:Ionicons
				Screen3=>tabBarIcon=name:cricket,type:MaterialCommunityIcons
				Screen4=>tabBarIcon=name:my-location,type:MaterialIcons
			endif
			Login=>animationEnabled=true
			Register

**Basics**
The Drawer,Stack And Bottom Are the navigators. You can stack navigators inside each other, and the file has to indented with 4 spaces, if the indentation is wrong you may not get the desired result. 
whatever you type after => in a navigator name, this will passed as a prop wrapped with curly braces.
but in the case of a screen whatever you type will be passed to the options to the the navigator screen component. you have to type the key, and the a equal to sign, then the value.
If want to type a string, you should use single or double quotes. in case you want to type an icon. you can type it as same as given in the example.
After compliting a field. you have to use a colon (;). but not when you have to type a single field.(only for screens)

**If Else**
If you want to render screens using an if condition.you can type the name of the variable and a dash (-) at the end. and then type the screens. and when you want to end the if. you can type endif. In the case of the example in the Stack navigator. the bottom navigator will be rendered only in  IsLogged is True. other wise the other screens will be rendered.

**Bottom Stack**
if you wanna have a stack navigator for every screen in a bottom navigator. you can use *at the rate of @* before typing bottom.

**Thanks**
**react native project maker** © 2021+, Samarth Dubey. Released under the [MIT](http://mit-license.org/) License.  
Authored and maintained by Samarth Dubey with help from contributors 

