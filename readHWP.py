import win32com.client as win32

def newHWPFile():
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")

    return hwp


def openHWPFile(pathFileName):
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(pathFileName, "HWP", "forceopen:true")

    return hwp


def findText(hwp, findWord):
    print(hwp.HAction.GetDefault("RepeatFind",hwp.HParameterSet.HFindReplace.HSet))
    option = hwp.HParameterSet.HFindReplace
    option.FindString = findWord
    option.IgnoreMessage = 1 # 0 : 팝업창 띄우기 1 : 팝업창 안띄우기
    option.Direction = hwp.FindDir("AllDoc") # AllDoc : 문서전체탐색 , Forward : 앞에서탐색 , backward : 뒤에서탐색
    res = hwp.HAction.Execute("RepeatFind",hwp.HParameterSet.HFindReplace.HSet) # res = True : 해당 단어 존재 , False : 해당 단어 존재하지않음

def open_and_findtext(file_path, findWord):
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(file_path, "HWP", "forceopen:true")
    hwp.HAction.GetDefault("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)
    option = hwp.HParameterSet.HFindReplace
    option.FindString = findWord
    option.IgnoreMessage = 1 # 0 : 팝업창 띄우기 1 : 팝업창 안띄우기
    option.Direction = hwp.FindDir("AllDoc") # AllDoc : 문서전체탐색 , Forward : 앞에서탐색 , backward : 뒤에서탐색
    res = hwp.HAction.Execute("RepeatFind",hwp.HParameterSet.HFindReplace.HSet) # res = True : 해당 단어 존재 , False : 해당 단어 존재하지않음
    hwp.Quit()

    return res
