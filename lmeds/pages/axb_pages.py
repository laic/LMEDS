'''
Created on Jun 10, 2015

@author: tmahrt

Pages in here all some sort of variant of tasks where a stimuli is presented
and users choose one of a limited number of options.
'''

import types
from os.path import join

from lmeds.pages import abstractPages

from lmeds import survey
from lmeds import constants
from lmeds import html
from lmeds import loader
from lmeds import audio
from lmeds import utils

# Can be used for axb or ab page validation
abValidation = """
var y=document.forms["languageSurvey"];
if (checkBoxValidate(y["axb"])==true)
  {
  alert("%s");
  return false;
  }
return true;
"""


class SameDifferentBeepPage(abstractPages.AbstractPage):
    
    sequenceName = "same_different_beep"
    
    def __init__(self, audioName1, minPlays, maxPlays, *args, **kargs):
        super(SameDifferentBeepPage, self).__init__(*args, **kargs)
        
        self.audioName1 = audioName1
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir

        self.submitProcessButtonFlag = False
        self.nonstandardSubmitProcessList = [('widget', "same_different_beep"),
                                             ]

        # Variables that all pages need to define
        self.numAudioButtons = 1
        self.processSubmitList = []
        
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="same_different_beep" '
                       'value="%(id)s" id="%(id)s" /> \n'
                       '<label for="%(id)s">.</label>'
                       '</p>\n'
                       )
        
        htmlTxt = ('<br /><br />%%s<br /><br />\n'
                   '<table class="center">\n'
                   '<tr><td>%%s</td><td>%%s</td><td>%%s</td></tr>\n'
                   '<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                   '</table>\n'
                   )
        
        return htmlTxt % (radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'},)
    
    def getValidation(self):
        txt = loader.getText('error select same or different')
        txt = txt.replace('"', "'")
        retPage = abValidation % txt
        
        return retPage
    
    def getNumOutputs(self):
        return 3
        
    def getHTML(self):
        '''
        Listeners hear two files and decide if they are the same or different
        '''
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        aHTML = audio.generateAudioButton(self.audioName1, 0, 0, False)
        
        description = loader.getText("same_different text")
        
        sameTxt = loader.getText("same_different same")
        differentTxt = loader.getText("same_different different")
        beepTxt = loader.getText("same_different beep")
        
        htmlText = description + self._getHTMLTxt()
        htmlText %= (aHTML, sameTxt, differentTxt, beepTxt)
    
        embedTxt = audio.getPlaybackJS(True, 1, self.maxPlays, self.minPlays)
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir, self.audioName1)

        return htmlText, pageTemplate, {'embed': embedTxt}
    
    
class SameDifferentPage(abstractPages.AbstractPage):
    
    sequenceName = "same_different"
    
    def __init__(self, audioName1, audioName2, minPlays,
                 maxPlays, *args, **kargs):
        super(SameDifferentPage, self).__init__(*args, **kargs)
        
        self.audioName1 = audioName1
        self.audioName2 = audioName2
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir

        # Variables that all pages need to define
        self.numAudioButtons = 2
        self.processSubmitList = []
        
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="same_different"'
                       'value="%(id)s" id="%(id)s" />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        htmlTxt = ('<br /><br />%%s %%s<br /><br />\n'
                   '<table class="center">\n'
                   '<tr><td>%%s</td><td>%%s</td></tr>\n'
                   '<tr><td>%s</td><td>%s</td></tr>\n'
                   '</table>\n'
                   )
        
        return htmlTxt % (radioButton % {'id': '0'},
                          radioButton % {'id': '1'})
    
    def getValidation(self):
        txt = loader.getText('error select same or different')
        txt = txt.replace('"', "'")
        retPage = abValidation % txt
        
        return retPage
    
    def getNumOutputs(self):
        return 2
        
    def getHTML(self):
        '''
        Listeners hear two files and decide if they are the same or different
        '''
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        aHTML = audio.generateAudioButton(self.audioName1, 0, 0, False)
        bHTML = audio.generateAudioButton(self.audioName2, 1, 0, False)
        
        description = loader.getText("same_different text")
        
        sameTxt = loader.getText("same_different same")
        differentTxt = loader.getText("same_different different")
        
        htmlText = description + self._getHTMLTxt()
        htmlText %= (aHTML, bHTML, sameTxt, differentTxt)
    
        embedTxt = audio.getPlaybackJS(True, 2, self.maxPlays, self.minPlays)
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir,
                                                 [self.audioName1,
                                                  self.audioName2])
    
        return htmlText, pageTemplate, {'embed': embedTxt}


class SameDifferentStream(abstractPages.AbstractPage):
    
    sequenceName = "same_different_stream"
    
    def __init__(self, pauseDuration, minPlays, maxPlays,
                 audioList, *args, **kargs):
        super(SameDifferentStream, self).__init__(*args, **kargs)
        
        self.pauseDuration = pauseDuration
        self.audioList = audioList
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir

        self.submitProcessButtonFlag = False
        self.nonstandardSubmitProcessList = [('widget',
                                              "same_different_stream")]

        # Variables that all pages need to define
        self.numAudioButtons = 1
        self.processSubmitList = ["verifyAudioPlayed", ]
    
    def checkResponseCorrect(self, responseList, correctResponse):
        '''
        Same: index=0, Different: index=1
        '''
        return abstractPages.checkResponseCorrectByIndex(responseList, 
                                                         correctResponse)
    
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="same_different_stream" '
                       'value="%(id)s" id="%(id)s" disabled /> \n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        htmlTxt = ('<br /><br />%%s<br /><br />\n'
                   '<table class="center">\n'
                   '<tr><td>%%s</td><td>%%s</td></tr>\n'
                   '<tr><td>%s</td><td>%s</td></tr>\n'
                   '</table>\n'
                   )
        
        return htmlTxt % (radioButton % {'id': '0'},
                          radioButton % {'id': '1'})
    
    def getValidation(self):
        txt = loader.getText('error select same or different')
        txt = txt.replace('"', "'")
        retPage = abValidation % txt
        
        return retPage
    
    def getNumOutputs(self):
        return 2
        
    def getHTML(self):
        '''
        Listeners hear two files and decide if they are the same or different
        '''
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        availableFunctions = ('<script>\n'
                              'function enable_checkboxes() {\n'
                              'document.getElementById("0").disabled=false;\n'
                              'document.getElementById("1").disabled=false;\n'
                              '}\n'
                              'function disable_checkboxes() {\n'
                              'document.getElementById("0").disabled=true;\n'
                              'document.getElementById("1").disabled=true;\n'
                              '}\n'
                              '</script>\n'
                              )
        
        embedTxt = audio.getPlaybackJS(True, 1, self.maxPlays, self.minPlays,
                                       runOnFinish="enable_checkboxes();")
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir,
                                                 list(set(self.audioList)))
        embedTxt += "\n\n" + availableFunctions
        
        description = loader.getText("same_different_question")
        
        sameTxt = loader.getText("same_different_same")
        differentTxt = loader.getText("same_different_different")
               
        audioButtonHTML = audio.generateAudioButton(self.audioList, 0,
                                                    self.pauseDuration, False)
        htmlText = description + self._getHTMLTxt()
        htmlText %= (audioButtonHTML + "<br />", sameTxt, differentTxt)
    
        return htmlText, pageTemplate, {'embed': embedTxt}
    

class ABNPage(abstractPages.AbstractPage):
    
    sequenceName = "abn"
    
    VALIDATION_STRING = "validation_string"
    
    textStringList = [VALIDATION_STRING, ]
    
    def __init__(self, audioName, minPlays, maxPlays, *args, **kargs):
        super(ABNPage, self).__init__(*args, **kargs)
        
        self.audioName = audioName
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir
        
        self.submitProcessButtonFlag = False
        self.nonstandardSubmitProcessList = [('widget', "abn")]
        
        # Variables that all pages need to define
        self.numAudioButtons = 1
        self.processSubmitList = []
    
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="abn" value="%(id)s" \n'
                       'id="%(id)s" disabled />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n')
        
        htmlTxt = ('%%s\n'
                   '<table class="center">\n'
                   '<tr><td>%%s</td><td>%%s</td><td>%%s</td></tr>\n'
                   '<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                   '</table>\n'
                   )
        
        return htmlTxt % (radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'})
        
    def getValidation(self):
        abnValidation = ('var y=document.forms["languageSurvey"];\n'
                         'if (checkBoxValidate(y["abn"])==true)\n'
                         '{\n'
                         'alert("%s");\n'
                         'return false;\n'
                         '}\n'
                         'return true;\n'
                         )
#         #'Error.  Select one of the three options'
#         retPage = abnValidation % loader.getText(self.VALIDATION_STRING)
        
        return ""
    
    def getNumOutputs(self):
        return 3
    
    def getHTML(self):
        '''
        Listeners hear one file and mark one of three options
        
        Options are "textA", "textB" or "None"
        '''
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        aHTML = audio.generateAudioButton(self.audioName, 0, 0, False)
        
        description = loader.getText("abn text")
        
        a = loader.getText("abn a")
        b = loader.getText("abn b")
        n = loader.getText("abn n")
        
        availableFunctions = ('<script>\n'
                              'function enable_checkboxes() {\n'
                              'document.getElementById("0").disabled=false;\n'
                              'document.getElementById("1").disabled=false;\n'
                              'document.getElementById("2").disabled=false;\n'
                              '}\n'
                              'function disable_checkboxes() {\n'
                              'document.getElementById("0").disabled=true;\n'
                              'document.getElementById("1").disabled=true;\n'
                              'document.getElementById("2").disabled=true;\n'
                              '}\n'
                              '</script>\n'
                              )
        
        htmlText = description + "<br />" + self._getHTMLTxt()
        htmlText %= (aHTML, a, b, n)
        
        embedTxt = audio.getPlaybackJS(True, 1, self.maxPlays, self.minPlays,
                                       runOnFinish="enable_checkboxes();")
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir, [self.audioName])
        embedTxt += "\n\n" + availableFunctions
    
        return htmlText, pageTemplate, {'embed': embedTxt}


class ABN(abstractPages.AbstractPage):
    
    A_STR = loader.TextString("abn_stream_a")
    B_STR = loader.TextString("abn_stream_b")
    N_STR = loader.TextString("abn_stream_n")
    DESCRIPTION_STR = loader.TextString("abn_stream_description")
    NO_ITEM_SELECTED_STR = loader.TextString('error_select_a_b_or_n')
    
    def __init__(self, pauseDuration, minPlays, maxPlays,
                 beepOption, *args, **kargs):
        super(ABN, self).__init__(*args, **kargs)
        
        self.pauseDuration = pauseDuration
        self.beepOption = beepOption.lower() == "true"
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir

        self.submitProcessButtonFlag = False

        self.validationErrorTxt = loader.getText(self.NO_ITEM_SELECTED_STR)

        # Variables that all pages need to define
#         self.numAudioButtons = 3
        self.processSubmitList = ["verifyAudioPlayed", ]
    
    def checkResponseCorrect(self, responseList, correctResponse):
        '''
        A: index=0, B: index=1, N: index=2
        '''
        return abstractPages.checkResponseCorrectByIndex(responseList,
                                                         correctResponse)
    
    def _getHTMLTxt(self):
        raise NotImplementedError("Should have implemented this")
    
    def getValidation(self):
        txt = self.validationErrorTxt
        txt = txt.replace('"', "'")
        retPage = abValidation % txt
        
        return retPage
    
    def getNumOutputs(self):
        return 4
    
    def getUniqueAudioFiles(self):
        raise NotImplementedError("Should have implemented this")
        
    def getHTML(self):
        '''
        Listeners hear two files and decide if they are the same or different
        '''
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        if self.beepOption is True:
            jsFuncs = ('<script>\b'
                       'function enable_checkboxes() {\n'
                       'document.getElementById("0").disabled=false;\n'
                       'document.getElementById("1").disabled=false;\n'
                       'document.getElementById("2").disabled=false;\n'
                       'document.getElementById("3").disabled=false;\n'
                       '}\n'
                       'function disable_checkboxes() {\n'
                       'document.getElementById("0").disabled=true;\n'
                       'document.getElementById("1").disabled=true;\n'
                       'document.getElementById("2").disabled=true;\n'
                       'document.getElementById("3").disabled=true;\n'
                       '}\n'
                       '</script>\n'
                       )
            
        else:
            jsFuncs = ('<script>\n'
                       'function enable_checkboxes() {\n'
                       'document.getElementById("0").disabled=false;\n'
                       'document.getElementById("1").disabled=false;\n'
                       'document.getElementById("2").disabled=false;\n'
                       '}\n'
                       'function disable_checkboxes() {\n'
                       'document.getElementById("0").disabled=true;\n'
                       'document.getElementById("1").disabled=true;\n'
                       'document.getElementById("2").disabled=true;\n'
                       '}\n'
                       '</script>\n'
                       )
        
        embedTxt = audio.getPlaybackJS(True, self.numAudioButtons,
                                       self.maxPlays, self.minPlays,
                                       runOnFinish="enable_checkboxes();")
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir,
                                                 self.getUniqueAudioFiles())
        embedTxt += "\n\n" + jsFuncs
        
        description = loader.getText(self.DESCRIPTION_STR)
        
        aTxt = loader.getText(self.A_STR)
        bTxt = loader.getText(self.B_STR)
        nTxt = loader.getText(self.N_STR)
        
        htmlText = description + self._getHTMLTxt()
        htmlText %= (aTxt, bTxt, nTxt)
    
        return htmlText, pageTemplate, {'embed': embedTxt}
    

class ABNOneAudio(ABN):

    sequenceName = "abn_one_audio"

    BEEP_STR = loader.TextString("beep")
    
    def __init__(self, pauseDuration, minPlays, maxPlays, beepOption,
                 audioList, *args, **kargs):
        super(ABNOneAudio, self).__init__(pauseDuration, minPlays, maxPlays,
                                          beepOption, *args, **kargs)
        self.audioList = audioList

        self.nonstandardSubmitProcessList = [('widget', "abn_one_audio")]
        
        # Variables that all pages need to define
        self.numAudioButtons = 1
        
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="abn_one_audio" '
                       'value="%(id)s" id="%(id)s" disabled />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        if self.beepOption is False:
            inputTuple = (audio.generateAudioButton(self.audioList, 0,
                                                    self.pauseDuration, False),
                          radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'},
                          )
            
            htmlTxt = ('%s\n'
                       '<table class="center">\n'
                       '<tr><td>%%s</td><td>%%s</td><td>%%s</td></tr>\n'
                       '<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                       '</table>\n'
                       )
            
            htmlTxt %= inputTuple
        else:
            inputTuple = (audio.generateAudioButton(self.audioList, 0,
                                                    self.pauseDuration, False),
                          loader.getText(self.BEEP_STR),
                          radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'},
                          radioButton % {'id': '3'}
                          )
            
            htmlTxt = ('%s\n'
                       '<table class="center">\n'
                       '<tr>  <td>%%s</td>  <td>%%s</td>    '
                       '<td>%%s</td>  <td>%s</td>  </tr>\n'
                       '<tr>  <td>%s</td>  <td>%s</td>    '
                       '<td>%s</td>  <td>%s</td>  </tr>\n'
                       '</table>\n'
                       )
            
            htmlTxt %= inputTuple

        return htmlTxt
    
    def getUniqueAudioFiles(self):
        return self.audioList
    

class ABNTwoAudio(ABN):
    
    sequenceName = "abn_two_audio"
    
    BEEP_STR = loader.TextString("beep")
    
    def __init__(self, pauseDuration, minPlays, maxPlays, beepOption,
                 audioList1, audioList2, *args, **kargs):
        super(ABNTwoAudio, self).__init__(pauseDuration, minPlays, maxPlays,
                                          beepOption, *args, **kargs)
        
        self.audioList1 = audioList1
        self.audioList2 = audioList2
        
        self.nonstandardSubmitProcessList = [('widget', "abn_two_audio")]
        
        # Variables that all pages need to define
        self.numAudioButtons = 2
    
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="abn_two_audio" '
                       'value="%(id)s" id="%(id)s" disabled />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        audioButton1 = audio.generateAudioButton(self.audioList1, 0,
                                                 self.pauseDuration, False)
        audioButton2 = audio.generateAudioButton(self.audioList2, 1,
                                                 self.pauseDuration, False)
        
        if self.beepOption is False:
            htmlTxt = ('<table class="center">\n'
                       '<tr><td>%s</td><td>%s</td></tr>\n'
                       '<tr><td>%%s</td><td>%%s</td><td>%%s</td></tr>\n'
                       '<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                       '</table>\n'
                       )
            
            inputTuple = (audioButton1,
                          audioButton2,
                          radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'},)
            
            htmlTxt %= tuple(inputTuple)
        else:
            htmlTxt = ('<table class="center">\n'
                       '<tr>  <td>%s</td>  <td>%s</td><td></td>  </tr>\n'
                       '<tr>  <td>%%s</td>  <td>%%s</td>  <td>%%s</td> '
                       '<td>%s</td>  </tr>\n'
                       '<tr>  <td>%s</td>  <td>%s</td> <td>%s</td> '
                       '<td>%s</td>  </tr>\n'
                       '</table>\n'
                       )
            
            inputTuple = (audioButton1,
                          audioButton2,
                          loader.getText(self.BEEP_STR),
                          radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'},
                          radioButton % {'id': '3'})
            
            htmlTxt %= inputTuple

        return htmlTxt
    
    def getUniqueAudioFiles(self):
        return list(set(self.audioList1 + self.audioList2))
    
    
class ABNThreeAudio(ABN):
    
    sequenceName = "abn_three_audio"
    
    BEEP_STR = loader.TextString("beep")
    
    def __init__(self, pauseDuration, minPlays, maxPlays, beepOption,
                 audioList1, audioList2, audioList3, *args, **kargs):
        super(ABNThreeAudio, self).__init__(pauseDuration, minPlays, maxPlays,
                                            beepOption, *args, **kargs)
        
        self.audioList1 = audioList1
        self.audioList2 = audioList2
        self.audioList3 = audioList3
        
        self.nonstandardSubmitProcessList = [('widget', "abn_three_audio")]
        
        # Variables that all pages need to define
        self.numAudioButtons = 3
    
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="abn_three_audio" '
                       'value="%(id)s" id="%(id)s" disabled />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        audioButton1 = audio.generateAudioButton(self.audioList1, 0,
                                                 self.pauseDuration, False)
        audioButton2 = audio.generateAudioButton(self.audioList2, 1,
                                                 self.pauseDuration, False)
        audioButton3 = audio.generateAudioButton(self.audioList3, 2,
                                                 self.pauseDuration, False)
        
        if self.beepOption is False:
            htmlTxt = ('<table class="center">\n'
                       '<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                       '<tr><td>%%s</td><td>%%s</td><td>%%s</td></tr>\n'
                       '<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n'
                       '</table>\n'
                       )
            
            inputTuple = (audioButton1,
                          audioButton2,
                          audioButton3,
                          radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'})
            
            htmlTxt %= tuple(inputTuple)
        else:
            htmlTxt = ('<table class="center">\n'
                       '<tr>  <td>%s</td>  <td>%s</td>  '
                       '<td>%s</td>  <td></td>  </tr>\n'
                       '<tr>  <td>%%s</td>  <td>%%s</td>  '
                       '<td>%%s</td>  <td>%s</td>  </tr>\n'
                       '<tr>  <td>%s</td>  <td>%s</td>  '
                       '<td>%s</td>  <td>%s</td>  </tr>\n'
                       '</table>\n'
                       )
            
            inputTuple = (audioButton1,
                          audioButton2,
                          audioButton3,
                          loader.getText(self.BEEP_STR),
                          radioButton % {'id': '0'},
                          radioButton % {'id': '1'},
                          radioButton % {'id': '2'},
                          radioButton % {'id': '3'})
            
            htmlTxt %= inputTuple

        return htmlTxt
    
    def getUniqueAudioFiles(self):
        return list(set(self.audioList1 + self.audioList2 + self.audioList3))


class ABPage(abstractPages.AbstractPage):
    
    sequenceName = "ab"
    
    def __init__(self, audioName, minPlays, maxPlays, *args, **kargs):
        super(ABPage, self).__init__(*args, **kargs)
        
        self.audioName = audioName
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir

        # Variables that all pages need to define
        self.numAudioButtons = 1
        self.processSubmitList = ["validateForm", ]
        
    def _getHTMLTxt(self):
        
        radioButton = ('<p>\n'
                       '<input type="radio" name="ab" value="%(id)s" '
                       'id="%(id)s" />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        htmlTxt = ('Write statement about how the user should select '
                   '(A) or (B).<br /><br />\n'
                   '<table class="center">\n'
                   '<tr><td>A</td><td>B</td></tr>\n'
                   '<tr><td>%%s</td><td>%%s</td></tr>\n'
                   '<tr><td>%s</td><td>%s</td></tr>\n'
                   '</table>\n'
                   )
        htmlTxt %= (radioButton % {'id': '0'},
                    radioButton % {'id': '1'})
        
        return htmlTxt
    
    def getValidation(self):
        txt = loader.getText('error select a or b')
        txt = txt.replace('"', "'")
        retPage = abValidation % txt
        
        return retPage
    
    def getNumOutputs(self):
        return 2
    
    def getHTML(self):
        '''
        Listeners hear one file and decide if its one of three choices
        
        The choices are "textA", "textB" or "None"
        '''
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        aHTML = audio.generateAudioButton(self.audioName, 0, 0, False)
        
        description = loader.getText("abn text")
        
        a = loader.getText("abn a")
        b = loader.getText("abn b")
        n = loader.getText("abn n")
        
        htmlText = description + "<br />" + self.getHTML()
        htmlText %= (aHTML, a, b, n)
        
        embedTxt = audio.getPlaybackJS(True, 1, self.maxPlays, self.minPlays)
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir, [self.audioName])
    
        return htmlText, pageTemplate, {'embed': embedTxt}


class AXBPage(abstractPages.AbstractPage):
    
    sequenceName = "axb"

    def __init__(self, sourceNameX, compareNameA, compareNameB,
                 minPlays, maxPlays, *args, **kargs):
        
        super(AXBPage, self).__init__(*args, **kargs)
        
        self.sourceNameX = sourceNameX
        self.compareNameA = compareNameA
        self.compareNameB = compareNameB
        self.minPlays = minPlays
        self.maxPlays = maxPlays
        
        self.wavDir = self.webSurvey.wavDir

        # Variables that all pages need to define
        self.numAudioButtons = 3
        self.processSubmitList = ["verifyAudioPlayed", "validateForm", ]
    
    def _getHTMLTxt(self):
    
        radioButton = ('<p>\n'
                       '<input type="radio" name="axb" value="%(id)s" '
                       'id="%(id)s" />\n'
                       '<label for="%(id)s">.</label>\n'
                       '</p>\n'
                       )
        
        htmlTxt = ('%s<br /><br /><br />\n'
                   '%s<br /> <br />\n'
                   '%%s<br /> <br />\n'
                   '<table class="center">\n'
                   '<tr><td>%s</td><td>%s</td></tr>\n'
                   '<tr><td>%%s</td><td>%%s</td></tr>\n'
                   '<tr><td>%s</td><td>%s</td></tr>\n'
                   '</table>\n'
                   )
        htmlTxt %= (loader.getText("axb query"),
                    loader.getText("axb x"),
                    loader.getText("axb a"),
                    loader.getText("axb b"),
                    radioButton % {'id': '0'},
                    radioButton % {'id': '1'})
        
        return htmlTxt
    
    def getValidation(self):
        txt = loader.getText('error select a or b')
        txt = txt.replace('"', "'")
        retPage = abValidation % txt
        
        return retPage
    
    def getNumOutputs(self):
        return 2
    
    def getHTML(self):
        pageTemplate = join(constants.htmlDir, "axbTemplate.html")
        
        xHTML = audio.generateAudioButton(self.sourceNameX, 0, 0, False)
        aHTML = audio.generateAudioButton(self.compareNameA, 1, 0, False)
        bHTML = audio.generateAudioButton(self.compareNameB, 2, 0, False)
        
        htmlText = self._getHTMLTxt()
        htmlText %= (xHTML, aHTML, bHTML)
        
        audioNameList = [self.sourceNameX, self.compareNameA,
                         self.compareNameB]
        embedTxt = audio.getPlaybackJS(True, 3, self.maxPlays, self.minPlays)
        embedTxt += "\n\n" + audio.generateEmbed(self.wavDir, audioNameList)
        
        htmlText = html.makeNoWrap(htmlText)
        
        return htmlText, pageTemplate, {'embed': embedTxt}
