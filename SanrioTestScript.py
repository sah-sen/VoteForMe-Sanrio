from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementNotInteractableException
import time
from selenium.webdriver.common.action_chains import ActionChains
import random

#This project is for fun and learning purposes only and is not to be abused. Please vote according to the rules
#You can vote for as many characters as you like per day according to the sanrio website
#Vote for your favourite characters from your python terminal! You don't have to do it yourself :)

#_________________________________________________________________________________________________
#Override variables, edit these to skip the text entry
ageValue = "20-29 years old"
sexValue = "Other"
expValue = "I've voted in the Character Ranking before."
regionValue = "United Kingdom"
characterList = ['HANAMARUOBAKE','U・SA・HA・NA','LLOROMANNIC','Pompompurin','Aggretsuko', 'SHOW BY ROCK!!', 'KUROMI']

overrideControls = input("Do you want to use the override variables?(y/n)")

driver = webdriver.Firefox()
driver.maximize_window()

def enterInitialDetails(age,sex,exp,region):
    if (elementOnScreen("//select[@id='age']")):
        selectAge = Select(driver.find_element(By.XPATH,"//select[@id='age']"))
        time.sleep(1)
        selectAge.select_by_visible_text(str(age))
        selectSex = Select(driver.find_element(By.XPATH,"//select[@id='gender']"))
        driver.implicitly_wait(2)
        selectSex.select_by_visible_text(str(sex))
        selectRegion = Select(driver.find_element(By.XPATH,"//select[@id='prefecture']"))
        driver.implicitly_wait(2)
        selectRegion.select_by_visible_text(str(region))
        selectExp = Select(driver.find_element(By.XPATH,"//select[@id='experience']"))
        driver.implicitly_wait(2)
        selectExp.select_by_visible_text(str(exp))
        driver.find_element(By.XPATH,"//button[@type='submit' and text()='Agree']").click()


def getCharacterVoteStr(charName):
    return f"//img[contains(@alt,'{charName}')]//ancestor::li//button"


def verifyVote(charName):
    tYForVoteStr = "//h1[text()='Thank you for voting!']"
    charImgStr = f"//img[@alt='{charName}']"
    waitForElement((By.XPATH, tYForVoteStr))
    assert elementOnScreen(tYForVoteStr) is True
    assert elementOnScreen(charImgStr) is True
    if(elementOnScreen(tYForVoteStr)):
         print("voted for "+charName)
    else:
        print("vote failed for "+ charName+", you may have already voted for this character today.") 
    return (elementOnScreen(charImgStr) and elementOnScreen(tYForVoteStr))

def adaptiveVote(charName):
    tYForVoteStr = "//h1[text()='Thank you for voting!']"
    waitForElement((By.XPATH,tYForVoteStr))

    if(elementOnScreen(tYForVoteStr)):
        driver.find_element(By.XPATH,"//button[@class='header-nav']").click()
        waitForClickable((By.XPATH,"//a[text()='Character Entries']"))
        driver.find_element(By.XPATH,"//a[text()='Character Entries']").click()      

  
    firstVoteButton = "(//strong[text()='Vote'])[1]"
    waitForElement((By.XPATH,firstVoteButton))
    charLocatorStr = getCharacterVoteStr(charName)
    charElem = driver.find_element(By.XPATH,charLocatorStr)
    location = charElem.location
    y,x = location['y'],location['x']
    y=y-100
    driver.execute_script(f"window.scrollTo(0, {y})")
    time.sleep(1)
   # waitForClickable(charElem)
    charElem.click()
   

def elementOnScreen (elementStr):
    myList = driver.find_elements(By.XPATH,elementStr)
    onScreen = len(myList)
    if (onScreen>0):
        return True
    else:
        return False
    
def waitForElement(elementBy):
    try:
        element_present = EC.presence_of_element_located(elementBy)
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print ("Element didn't load in 5 seconds")

def waitForClickable(elementBy):
    try:
        element_present = EC.element_to_be_clickable(elementBy)
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print ("Element didn't become clickable in 5 seconds")
  
def userChooseFromList(validValuesList, question):
    while True:
        answer = input(question)
        for val in validValuesList:
            if(val.lower() == answer.lower()):
                confirmation = input(f"Confirm (y/n) you have chosen '{val}': ")
                if(confirmation =="y" or confirmation == "Y"):
                    return val
                else:
                    break

            temp = val
            temp = temp.replace("・","").replace("!","").replace("-","")
            if("・" in val or "!" in val or "-" in val):
                if(temp.lower() == answer.lower()):
                    confirmation = input(f"Confirm (y/n) you have chosen '{val}': ")
                    if(confirmation =="y"):
                         return val
                    else:
                         break
                    
            if(jaccardSimilarity(temp.lower(),answer.lower())>0.7):
                confirmation = input(f"Confirm (y/n) you have chosen '{val}': ")
                if(confirmation =="y"):
                    return val
                else:
                    break   

        print("Please enter a valid answer")        


def selectRandomOptionFromList(optionsList):
        size = len(optionsList)
        number = random.randint(1, size-1)
        return optionsList[number]

def getAllOptionsFromSelect(selectLocatorStr):
       selectElem = driver.find_element(By.XPATH,selectLocatorStr)
       selectObj = Select(selectElem)
       optionsList = selectObj.options
       textOnlyList = []
       extractedText = ''
       for i in range (len(optionsList)):
           extractedText = optionsList[i].text
           textOnlyList.append(extractedText)
       return textOnlyList

#get all values in those attributes
def getAllAttrbutesInLocator(genericXpathStr, reqAttribute):
    valuesList=[]
    if(elementOnScreen(genericXpathStr)):
        charsOnPage = driver.find_elements(By.XPATH,genericXpathStr)
        for x in range(1,len(charsOnPage)):
          locatorAtNumber= (f"({genericXpathStr})[{x}]")
          value = driver.find_element(By.XPATH,locatorAtNumber).get_attribute(reqAttribute)
          valuesList.append(value)
        return valuesList
    else:
        print("couldn't find element "+genericXpathStr)        

def jaccardSimilarity(string1,string2):
    set1 = set(string1)
    set2 = set(string2)
    result = len(set1 & set2) / len(set1 | set2)
    return result

#_________________________________________________________________________________________________
#Open Sanrio Ranking website    

driver.get("https://ranking.sanrio.co.jp/en/characters/")
waitForElement((By.XPATH,"//header//img[contains(@alt,'Sanrio Character Ranking')]"))

#handle closed votes
if(elementOnScreen(("//p[contains(text(),'closed!')]"))):
    str = driver.find_element(By.XPATH,"//p[contains(text(),'closed!')]").text
    print(str)

else:
    if(overrideControls =='y' or overrideControls =='Y'):

        adaptiveVote(characterList[0])
        enterInitialDetails(ageValue,sexValue,expValue,regionValue)
        verifyVote(characterList[0])
        for i in range(1,len(characterList)):
            adaptiveVote(characterList[i])
            verifyVote(characterList[i])
        print ("Thanks for voting!")

    else:
        firstVoteButton = "(//strong[text()='Vote'])[1]"
        waitForElement((By.XPATH,firstVoteButton))

        genericCharStrLocator = "//img[contains(@src,'characters')]"

        #Get list of all character names
        characters = getAllAttrbutesInLocator(genericCharStrLocator,"alt")
        voteButtonOne = driver.find_element(By.XPATH,firstVoteButton).click()
        waitForElement((By.ID, "age"))
        ages = getAllOptionsFromSelect("//select[@id='age']")
        genders =getAllOptionsFromSelect("//select[@id='gender']")
        experiences = getAllOptionsFromSelect("//select[@id='experience']")
        regions = getAllOptionsFromSelect("//select[@id='prefecture']")

        ageValue = selectRandomOptionFromList(ages)
        sexValue = selectRandomOptionFromList(genders)
        expValue = selectRandomOptionFromList(experiences)

        driver.find_element(By.XPATH,"//button[@class='modal-close']").click()

        regionValue = userChooseFromList(regions,"Which Country are you from?")

        character = userChooseFromList(characters,"Which Character are you voting for?")

        adaptiveVote(character)
        enterInitialDetails(ageValue,sexValue,expValue,regionValue)
        verifyVote(character)

        while True:
            newChar = input("Do you want to vote for another character?(y/n)")
            if (newChar =='y' or newChar == 'Y'):
                    character = userChooseFromList(characters,"Which Character are you voting for?")
                    adaptiveVote(character)
                    verifyVote(character)
            else:
                print("Thanks for voting!")
                break     
                    
driver.close()