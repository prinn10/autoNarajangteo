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

def advanced_open_and_findtext(file_path, findWord):
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(file_path, "HWP", "forceopen:true")
    hwp.HAction.GetDefault("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)

    res = []
    for word in findWord:
        option = hwp.HParameterSet.HFindReplace
        option.FindString = word
        option.IgnoreMessage = 1 # 0 : 팝업창 띄우기 1 : 팝업창 안띄우기
        option.Direction = hwp.FindDir("AllDoc") # AllDoc : 문서전체탐색 , Forward : 앞에서탐색 , backward : 뒤에서탐색
        res.append(hwp.HAction.Execute("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)) # res = True : 해당 단어 존재 , False : 해당 단어 존재하지않음

    hwp.Quit()
    return res

def announcement_doc_crawling(file_path, findWord = None):
    # 해당 공고문에서 낙찰하한율, 범위 찾는 함수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(file_path, "HWP", "forceopen:true")
    hwp.HAction.GetDefault("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)

    res = []
    for word in findWord:
        option = hwp.HParameterSet.HFindReplace
        option.FindString = word
        option.IgnoreMessage = 1 # 0 : 팝업창 띄우기 1 : 팝업창 안띄우기
        option.Direction = hwp.FindDir("AllDoc") # AllDoc : 문서전체탐색 , Forward : 앞에서탐색 , backward : 뒤에서탐색
        res.append(hwp.HAction.Execute("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)) # res = True : 해당 단어 존재 , False : 해당 단어 존재하지않음

    txt = hwp.GetTextFile("TEXT","")
    # print(txt[txt.find('±'):txt.find('±')+3])
    # print(txt[txt.find('낙찰하한율'):txt.find('낙찰하한율')+8])

    for word, r in zip(findWord, res):
        if r == True: # word가 공고문에서 존재할 때
            if word == '±': # range
                range = txt[txt.find('±')+1:txt.find('±')+2]
            elif word == '낙찰하한율': # min_value
                min_value = txt[txt.find('낙찰하한율')+6:txt.find('낙찰하한율')+8]
        else:
            if word == '±':  # range
                range = ''
            elif word == '낙찰하한율':  # min_value
                min_value = ''

    hwp.Quit()
    return range, min_value

if __name__ == '__main__':
    announcement_doc_crawling()



