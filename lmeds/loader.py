# -*- coding: utf-8 -*-
'''
Created on Mar 28, 2013

@author: timmahrt
'''


import codecs

from lmeds import utils


class BadlyFormattedTextError(Exception):
    '''
    A generic error that is used whenever a string in the text dictionary is
    improperly formatted.
    '''
    
    def __init__(self, errorTxt, txtKey):
        super(BadlyFormattedTextError, self).__init__()
        
        self.errorTxt = errorTxt
        self.txtKey = txtKey
        self.dictionaryFN = textDict.sourceFN
        
    def __str__(self):
        prefixStr = "For text key <<%s>> in dictionary file <<%s>>: "
        prefixStr %= (self.txtKey, self.dictionaryFN)
        
        return prefixStr + self.errorTxt


class SpaceInKeyError(Exception):
    
    def __init__(self, key):
        super(SpaceInKeyError, self).__init__()
        
        self.key = key
        
    def __str__(self):
        errorStr = ("Spaces not allowed in dictionary keys.  "
                    "Space found in key '%s'")
        
        return errorStr % self.key


class TextNotInDictionaryException(Exception):
    
    def __init__(self, txtKey):
        super(TextNotInDictionaryException, self).__init__()
        self.txtKey = txtKey
        self.dictionaryFN = textDict.sourceFN
        
    def __str__(self):
        errorTxt = ("Text key <<%s>> not in dictionary file <<%s>\n\n"
                    "Please add text key to dictionary and try again.")
        
        return errorTxt % (self.txtKey, self.dictionaryFN)
    

def loadTxtFile(fn):
    txt = codecs.open(fn, "rU", encoding="utf-8").read()
    txtList = txt.splitlines()
    
    # Removes redundant whitespace
    txtList = [" ".join(txt.split()) for txt in txtList]
    
    # Remove empty rows
    txtList = [row for row in txtList if row != ""]

    return txtList


def loadTxtFileWHTML(fn):
    txt = codecs.open(fn, "rU", encoding="utf-8").read()
    
    lineEnding = utils.detectLineEnding(txt)
    if lineEnding is None:  # Should be only a single line
        txtList = [txt, ]
    else:
        txtList = txt.split(lineEnding)
    
    newTxtList = []
    for row in txtList:
        if row == "":
            continue
        if row[0] == "<":
            newTxtList.append(row)
        else:
            newTxtList.extend(" ".join(row.split()))
    txtList = newTxtList
    
    txtList = [row for row in txtList if row != ""]  # Remove empty rows

    return txtList


def getNumWords(fnFullPath):
    '''
    Get number of words in a transcript
    '''
    wordList = loadTxtFile(fnFullPath)
    numOutputs = 0
    for line in wordList:
        numOutputs += len(line.split(" "))

    return numOutputs


class TextString(object):

    def __init__(self, wordString):
        self.wordString = wordString

    def __repr__(self):
        return self.wordString


class TextDict(object):
    
    def __init__(self, fn):
        self.sourceFN = fn
        self.textDict = self._parse()
    
    def _parse(self):
            
        data = codecs.open(self.sourceFN, "rU", encoding="utf-8").read()
        testItemList = data.splitlines()
        
        keyValueList = self._findSections(testItemList, "-")
        
        parsedTextDict = {}
        for key, subList in keyValueList.items():
            subKeyValueList = self._findSections(['', ] + subList, "=")
            parsedTextDict.update(subKeyValueList)
             
        for key, textList in parsedTextDict.items():
            parsedTextDict[key] = "\n".join(textList).strip()
            
        return parsedTextDict
    
    def _isSeparatingString(self, text):
        '''
        Returns false if there is at least one alphanumeric character
        '''
        isComment = True
        for char in text:
            isComment &= not char.isalnum()
            
        return isComment
    
    def _findSections(self, textList, demarcator):
        
        def newSection(key, valueList, someDict):
            if key is not None:
                someDict[key] = valueList
                valueList = []
                
        def safeCheck(stringList, i, char):
                
            retValue = False
            if i < len(stringList):
                string = stringList[i]
                if len(string) > 0:
                    if string[0] == char:
                        retValue = True
            
            return retValue
        
        lastKey = None
        lastList = []
        
        i = 0
        sectionDictionary = {}
        while i < len(textList):
            
            # New section
            firstCheck = safeCheck(textList, i, demarcator)
            if firstCheck and safeCheck(textList, i + 2, demarcator):
                newSection(lastKey, lastList, sectionDictionary)
                lastKey = textList[i + 1]
                lastList = []
                i += 3
            # Still on old section
            else:
                lastList.append(textList[i])
                i += 1
        
        newSection(lastKey, lastList, sectionDictionary)
            
        return sectionDictionary
        
    def getText(self, key):
        return self.textDict[str(key)]


textDict = None  # textDict singleton


def initTextDict(fn):
    global textDict
    textDict = TextDict(fn)
    

def getText(key):
    if " " in key:
        raise SpaceInKeyError(key)
    
    try:
        returnText = textDict.getText(key)
    except KeyError:
        raise TextNotInDictionaryException(key)
    
    return returnText


def batchGetText(keyList):
    retDict = {}
    for key in keyList:
        retDict[key] = getText(key)
    
    return retDict
