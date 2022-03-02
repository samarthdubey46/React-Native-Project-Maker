const {tabLength} = require('./const.js');
const fs = require("fs");


module.exports.getFile = async (file) => {
    try {
        const data = fs.readFileSync(file, 'utf8')
        return data
    } catch (err) {
        console.error(err)
        return 'error'
    }
}
module.exports.isFloat = (n) => {
    return Number(n) === n && n % 1 !== 0;
}
module.exports.getIndent = (str) => {
    let indent = 0;
    for (let i = 0; i < str.length; i++) {
        if (str[i] === '\t') {
            indent += tabLength;
        } else if (str[i] === ' ') {
            indent++;
        } else {
            isWhiteSpace = false;
        }
    }
    return indent;
};