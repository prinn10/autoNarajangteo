import win32com.client as win32
import os
import tools
from time import sleep
import re

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
    print(file_path)
    # 해당 공고문에서 낙찰하한율, 범위 찾는 함수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(file_path, "HWP", "forceopen:true")
    hwp.HAction.GetDefault("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)
    range = ''
    res = []
    for word in findWord:
        option = hwp.HParameterSet.HFindReplace
        option.FindString = word
        option.IgnoreMessage = 1 # 0 : 팝업창 띄우기 1 : 팝업창 안띄우기
        option.Direction = hwp.FindDir("AllDoc") # AllDoc : 문서전체탐색 , Forward : 앞에서탐색 , backward : 뒤에서탐색
        res.append(hwp.HAction.Execute("RepeatFind",hwp.HParameterSet.HFindReplace.HSet)) # res = True : 해당 단어 존재 , False : 해당 단어 존재하지않음

    txt = hwp.GetTextFile("TEXT","")
    print(findWord, res)
    min_value = ''

    for word, r in zip(findWord, res):
        if r == True: # word가 공고문에서 존재할 때
            if word == '±': # range
                range_txt = txt[txt.find('±')-5:txt.find('±')+6]
                print(range_txt)
                range = tools.extract_number(range_txt)[0]
                print('range', range)
            else:
                if min_value == '':
                    while txt.find(word) != -1:
                        txt = txt[txt.find(word)+len(word):]
                        substr = txt[:50]
                        numbers = tools.extract_number(substr)
                        print('substr : ', substr)
                        print('number : ', numbers)
                        if numbers != None:
                            for number in numbers:
                                if number >= 80 and number <= 95:
                                    print('checked')
                                    min_value = number
                                    break
                            if min_value != '':
                                break

    print('res ', range, min_value)
    hwp.Quit()
    sleep(1)
    if min_value == '':
        tools.move_file(file_path)
    else:
        os.remove(file_path)  # 확인 후 해당 파일 삭제
    return range, min_value

if __name__ == '__main__':
    download_path = 'C:\\Users\\정희운\\Downloads'
    for file_name in os.listdir(download_path):
        announcement_doc_crawling(os.path.join(download_path, file_name), ['±', '낙찰 하한율', '낙찰하한율', '예정가격'])



