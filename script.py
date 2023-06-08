from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.keys import Keys
import json
import time
import random


# determine if quest is already complete
# RETURN: Boolean
def quest_complete(method, data):
    if (driver.find_element(method, data).get_attribute('class') == 'mee-icon mee-icon-SkypeCircleCheck'):
        return True
    else:
        return False

# quickly find if an element exists on the page
# RETURN: Boolean
def element_exist(method, data):
    try:
        driver.find_element(method, data)
        return True
    except:
        return False
    
def wait_long():
    time.sleep(random.uniform(3.7, 6.8))
    
def wait_short():
    time.sleep(random.uniform(1.4, 3.5))

# logs in from the rewards page which is for some reason necessary if running program right after pc startup
def initial_login():
    # click "SIGN IN"
    driver.find_element(By.XPATH, '//*[@id="raf-signin-link-id"]').click()
    
    # load username
    with open('username.txt') as u:
        username = u.readlines()
    
    # wait for username field to exist
    WebDriverWait(driver, 15).until(e_c.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
    time.sleep(random.uniform(0.7, 1.3))
    
    # type username and hit enter
    element1 = driver.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(username)
    time.sleep(random.uniform(0.2, 0.9))
    element1.send_keys(Keys.ENTER)
    u.close()
    
    
    # load password
    with open('password.txt') as p:
        password = p.readlines()
    
    # wait for password field to exist
    WebDriverWait(driver, 15).until(e_c.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
    time.sleep(random.uniform(0.7, 1.3))
        
    # type password and hit enter
    element2 = driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(password)
    time.sleep(random.uniform(0.2, 0.9))
    element2.send_keys(Keys.ENTER)
    p.close()
    
    wait_short()
    
    # might be a 'remember me for next time' page so make sure were not already at the rewards page before just hitting enter again
    if not element_exist(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[1]/div/card-content/mee-rewards-daily-set-item-content/div/a'):
        e = driver.switch_to.active_element() #idk if these parenthesis need to be there
        e.send_keys(Keys.ENTER)
        wait_short()
    
# random(?) login prompt usually when clicking a questcard
def r_login():
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/span/a').click()

# traces down a flowcart to find what type of quest we are dealing with here
# automatically completes whateverquest is up on the current active tab
def do_quest():
    if(element_exist(By.XPATH, '//*[@id="QuestionPane0"]/div[1]/div[2]/a[1]')):
        print('page quiz')
        do_quiz()
    elif(element_exist(By.XPATH, '//*[@id="btoption0"]')):
        print('poll')
        do_poll()
    elif(element_exist(By.XPATH, '//*[@id="rqStartQuiz"]')):
        print('start button')
        driver.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        wait_short()
        if(element_exist(By.XPATH, '//*[@id="rqAnswerOption2"]')):
            print('multianswer')
            do_multianswer()
        else:
            print('tot')
            do_tot()
    else:
        print('search')


def do_tot():
    wait_short()
    while (element_exist(By.XPATH, '//*[@id="rqAnswerOption0"]')):
        driver.find_element(By.XPATH, '//*[@id="rqAnswerOption' + str(random.randint(0, 1)) + '"]').click()
        time.sleep(random.uniform(5.7, 6.9))

# def num_answers():
#     nai = 9
#     while True:
#         if (element_exist(By.XPATH, '//*[@id="rqAnswerOption' + str(nai) + '"]')):
#             return nai
#         nai -= 1

def num_answers():
    i = 0
    while True:
        if not (element_exist(By.XPATH, '//*[@id="rqAnswerOption' + str(i + 1) + '"]')):
            return i
        else:
            i += 1

def do_multianswer():
    wait_short()
    max = num_answers()
    
    mi = 0
    #sometimes there is less than 8 options, its very rare and idek know what that type of quest is called
    try:
        while True:
            driver.find_element(By.XPATH, '//*[@id="rqAnswerOption' + str(mi) + '"]').click()
            time.sleep(random.uniform(5.8, 6.9))
            if mi == max - 1:
                mi = 0
            else:
                mi += 1
    except:
        print('exiting multianswer')
    
    # while (element_exist(By.XPATH, '//*[@id="rqAnswerOption' + str(mi) + '"]')):
    #     driver.find_element(By.XPATH, '//*[@id="rqAnswerOption' + str(mi) + '"]').click()
    #     time.sleep(random.uniform(5.8, 6.9))
    #     if mi == num_answers():
    #         mi = 0
    #     else:
    #         mi += 1

def do_quiz():
    wait_short()
    index = 0
    while element_exist(By.XPATH, '//*[@id="QuestionPane' + str(index) + '"]/div[1]/div[2]/a[1]'):
        driver.find_element(By.XPATH, '//*[@id="QuestionPane' + str(index) + '"]/div[1]/div[2]/a[1]').click()
    
        WebDriverWait(driver, 10).until(e_c.presence_of_element_located((By.XPATH, '//*[@id="nextQuestionbtn' + str(index) + '"]')))
        wait_short()
        driver.find_element(By.XPATH, '//*[@id="nextQuestionbtn' + str(index) + '"]').click()
        # Note: 2/11/2023 - they changed the XPATH of the next button, so i guess that will just happen sometimes
        index += 1
        time.sleep(random.uniform(3.7, 4.3))

def do_poll():
    wait_short()
    driver.find_element(By.XPATH, '//*[@id="btoption' + str(random.randint(0, 1)) + '"]').click()
    time.sleep(random.uniform(5.9, 7.4))


#-------------------------------------------------------------------------------------------------------------------------#
                                                   #-------MAIN-------#
#-------------------------------------------------------------------------------------------------------------------------#

# load 34 words into a list to be searched later for all 170 search points
file = open('wordle_answers.json')
words = json.load(file)
wordlist = random.sample(words["data"], 34)

# run msedgedriver (start up edge)
driver = webdriver.Edge(service = Service('edgedriver_win64/msedgedriver.exe'))
driver.set_window_size(1820, 980)

wait = WebDriverWait(driver, 15)    
    
# go to the rewards page & wait for first card to
# something causes the page to sometimes give slenium an aneurysm so multiple tries are needed. intrestingly it seems it always works first
# or second try. I tried googling the issue and it seems like a recent issue with selenium, not really anything I can do ab it
for x in range(1, 3):
    try:
        driver.get('https://rewards.bing.com/')
        WebDriverWait(driver, 15).until(e_c.presence_of_element_located((By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[1]/div/card-content/mee-rewards-daily-set-item-content/div/a')))
        print('rewards page attempt ' + str(x) + ' successful! continuing...')
        break
    except:
        if element_exist(By.XPATH, '//*[@id="raf-signin-link-id"]'):
            print('logging in...')
            initial_login()
            print('logged in!')
        else:
            print('rewards page attempt ' + str(x) + ' unsuccessful')

wait_long()

# save rewards page as a tab
rewards_page = driver.current_window_handle
    
# reap daily sets
for i in range(1, 4): # loop thrice
    # check for any other windows that may be open
    assert len(driver.window_handles) == 1
    
    # click on quest if not already complete
    # NOTE: should be no reason to check for existance of checkmark/plussign field, but if there is an error in the future double check this
    if not quest_complete(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(i) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]'):
        driver.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(i) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    
        # wait for tab to load
        wait.until(e_c.number_of_windows_to_be(2))
        
        # find new tab and switch to it
        for window_handle in driver.window_handles:
            if window_handle != rewards_page:
                driver.switch_to.window(window_handle)
                break
        
        # dont get banned
        wait_long()
        
        # sometimes for some reason you need to login again idk why maybe its a antibot type thing who knows
        if element_exist(By.XPATH, '/html/body/div[2]/div[2]/span/a'):
            r_login()
            wait_long()

        # determine quest type and go into specific route to complete it
        do_quest()

        # close tab
        driver.close()
        
        # switch the driver back to the rewards page
        driver.switch_to.window(rewards_page)
        
        # dont get banned
        wait_short()


# more activities
mai = 1
while (element_exist(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(mai) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a')):
    # check for any other windows that may be open
    assert len(driver.window_handles) == 1
    
    # click on quest if not already complete and it's actually a quest (i.e. has a + or a checkmark on the top right corner of the card)
    if element_exist(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(mai) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a/mee-rewards-points/div/div/span[1]'):
        if not quest_complete(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(mai) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a/mee-rewards-points/div/div/span[1]'):
            driver.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(mai) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
            
            # wait for tab to load
            wait.until(e_c.number_of_windows_to_be(2))
            
            # find new tab and switch to it
            for window_handle in driver.window_handles:
                if window_handle != rewards_page:
                    driver.switch_to.window(window_handle)
                    break
            
            # dont get banned
            wait_long()
            
            # sometimes for some reason you need to login again idk why maybe its a antibot type thing who knows
            if element_exist(By.XPATH, '/html/body/div[2]/div[2]/span/a'):
                r_login()
                wait_long()
                
            # find type of quest and complete it
            do_quest()
            
            # close tab
            driver.close()
            
            # switch the driver back to the rewards page
            driver.switch_to.window(rewards_page)
        
            # dont get banned
            wait_short()

    # increment more activities index (MAI)
    mai += 1


# Complete Daily Searches
driver.get('https://www.bing.com')
wait_short()

for i in wordlist:
    element = driver.find_element(By.ID, 'sb_form_q')
    element.clear()
    element.send_keys(i)
    time.sleep(random.uniform(0.94, 1.67))
    element.submit()
    
    wait_long()
    
time.sleep(4)
print('Exited Successfully! :-)')
driver.quit()