const fs = require('fs');
const {navigators, tabLength} = require('./const');
const {getFile, getIndent} = require("./helpers");


const processFile = async (file) => {
    const data = await getFile(file)
    const lines = data.split('\n')
    let error = []
    const result = {}
    let navigators_list = []
    let currentIndex = 0;
    let currentIndent = 0;
    let currentNavigator = 0;
    let lastIndent = 0;
    lines.every((line, index) => {
        let indent = getIndent(line) / tabLength
        let name = line.trim()
        console.log(indent,name)
        let isNavigator = navigators.includes(name)
        if (index === 0 && !isNavigator) {
            error.push('First line must be a navigator')
            return false
        }
        if (isNavigator) {
            navigators_list.push(`${name}-${indent}-${index}`)
        }
        if (index === 0)
            result[navigators_list[0]] = []
        else {
            if(lastIndent > indent)
                currentNavigator--
            result[navigators_list[currentNavigator]].push(isNavigator ? `${name}-${indent}-${index}` : name)
            if (isNavigator) {
                let newObj = {}
                result[`${name}-${indent}-${index}`] = []
                currentIndex = index
                currentIndent = indent
                currentNavigator = navigators_list.indexOf(`${name}-${indent}-${index}`)
            }
            lastIndent = indent
        }
        return true
    })
    if (error.length > 0)
        return error
    else
        return result
}
processFile('layout.yaml').then(result => {
    console.log(result)
})
//{Drawer-0-0 : [],Stack-1-1 : [IsLogged,AddComplaint,Login,Register],Bottom-2-5 : [Complaints,Home],Stack-1-9 : [Test]}
//{Drawer00 : [Stack-1-1,Stack-1-9]}