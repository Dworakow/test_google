#DESCRIPTION
#TEST FOR GOOGLE.COM
#This module contains class with methods testion the simplest aspects of google.com search page.
#There are some things that should be mentioned to upgrade this code in later time.
#0. All test should be extended to all object from each type. For purposes of this project only examples were used.
#1. time.sleep(1) this is used as python is faster than real actions so program need to wait at least this second to catch up. It is preferable to use 'wait for element' to avoid not necessary delays.
#2. find_element_by should be used in more common way to let use this program for other search pages. In this one particular element is hardcoded. Maybe API provided by google services would help.
#3. Labels should be checked with documentation, so probably it would be always hardcoded.
#4. Print from console should be stored in console and in file in the same time. Here we can use one of them.
#5. Language version - in next version of program element responsible for language should be located and set as constant to let find correct labels.
#6. Problem with many google chrome windows might be avoided by closing window after test. But somehow it affect test result so it is bypassed.


import unittest #this library provides many helpfull features. Easy test releasig is one of them.
from selenium import webdriver
import logging
from selenium.webdriver.common.keys import Keys
import time
import os
import sys

log_file_path = 'google_test.log'                                                                                       #this is implemented before class to let change of file and path easier and avoid searching in code.
console_prints_path = 'console_prints.log'

class Test_Methods(unittest.TestCase):

    def setUp(self):                                                                                                    #preconditions
        print('\n-----------------precondition started-----------------')
        logging.basicConfig(filename=log_file_path, filemode='a', level=logging.DEBUG, format='%(asctime)s %(message)s')#settings of logs, each test is opening log file again so it is important to have append option on.
        # sys.stdout = open(console_prints_path, 'w')                                                                   #if you comment it then all prints will be shown to console. Without comment it will be save to file.
        print('connecting...')
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\dworakow\pcodes\chromedriver\chromedriver.exe")      #chrome driver with local path
        self.browser.get('http://www.google.pl')                                                                        #open tested page/search
        print('Precondition is finished.')

    def test_links_label(self):                                                                                         #verification of links
        print("\n-----------------assert if links are present-----------------")
        all_elements = []
        browser = self.browser                                                                                          #to simplify code lets make browser as class object
        time.sleep(1)
        for element in browser.find_elements_by_class_name('gb_g'):                                                     #here should be more general query to find all needed objects. something like find all links. Finding "href" should be an option.
            all_elements.append(element.text)                                                                           #creating list of text element. This will be werified if current name is provided correctly. Launguage depended.
        print(all_elements)
                                                                                                                        #This part (Gmail, Images) is hardcoded and is dependend on version language. Next step would be find information about
                                                                                                                        # version and select suited one.
        assert "Gmail" in all_elements                                                                                  #assert if element is correctly provided. This should be get from documentation.
        assert "Images" in all_elements
        print('Links are present and label is correct')
        print('OK')

    def test_links_clickable(self):                                                                                     #checking if links can be clicked
        print("\n-----------------assert if links are working-----------------")                                        #part of clicking links
        browser = self.browser
        time.sleep(1)                                                                                                   #wait 1sec as code is faster than real action. More preferable to set wait for key element which when is present then whole page is ready to parse.
        table = ['Gmail', 'Images']                                                                                     #examples of phrase to assert
        for i in range(len(table)):
            browser.find_element_by_partial_link_text(table[i]).click()                                                 #find element from table and click it.
            browser.back()                                                                                              #back to previous page
            assert "google.pl" in browser.current_url                                                                   #assert if page back to main.
        print('Links are working correctly')
        print('OK')
    #
    def test_results(self):
        print("\n-----------------test results werification-----------------")
        search_phrase = 'java'                                                                                          #lets create variable as it is used more than once
        browser = self.browser
        time.sleep(1)                                                                                                   #wait 1sec as code is faster than real action.
        elem = browser.find_element_by_name('q')  # Find the search box
        elem.send_keys(search_phrase + Keys.RETURN)
        URL = browser.current_url
        print('URL page with test results: \n'+URL)

        print("\n---------------------checking headers---------------------")
        counter = 0
        count_head = len(browser.find_elements_by_class_name('S3Uucc'))
        for elements in browser.find_elements_by_class_name('S3Uucc'):
            if search_phrase in elements.text:
                counter = counter + 1
                assert search_phrase in elements.text
                print('%s element asserts and exist  in: \n      %s ' % (search_phrase, elements.text))
        print('amount of headers asserted succesfuly is %i' % counter)

        print("\n---------------------checking part of text---------------------")
        counter1 = 0
        count_text = len(browser.find_elements_by_class_name('s'))
        for elements in browser.find_elements_by_class_name('s'):
            if search_phrase in elements.text:
                counter1 = counter1 + 1
                assert search_phrase in elements.text
                print('%s element asserts and exist  in:\n      %s ' % (search_phrase, elements.text))
        print('amount of texts asserted succesfuly is %i' % counter1)

        print("\n---------------------checking addressese---------------------")
        counter2 = 0
        count_add = len(browser.find_elements_by_class_name('TbwUpd'))
        for elements in browser.find_elements_by_class_name('TbwUpd'):
            if search_phrase in elements.text:                                                                          #ussing if is equal to use verify so assert without breaking the program.
                counter2 = counter2 + 1
                assert search_phrase in elements.text
                print('%s element asserts and exist  in: \n      %s ' % (search_phrase, elements.text))
        print('amount of headers asserted succesfuly is %i' % counter2)
        assert counter >= count_head                                                                                    #using counters we check all steps an asserting test at the end. In prints from console we have detailed information what failed.
        assert counter1 >= count_text
        assert counter2 >= count_add
        print('All elements have been asserted correctly')
        print('OK')

    def test_simple_performance(self):                                                                                  #using element from google which counts time of search and amount of results
        print('\n-----------------testing simple performance with google stats-----------------')
        browser = self.browser
        table = ['cat', 'taylor swift', 'dezoksyrybonuklein']                                                           #table of examples
        for i in range(len(table)):
            elem = browser.find_element_by_name('q')                                                                    #Find the search box
            elem.send_keys(table[i] + Keys.RETURN)                                                                      #sending element from table and click enter
            print(table[i])
            time.sleep(1)                                                                                               #wait 1sec as code is faster than real action.
            element = browser.find_element_by_id('appbar')                                                              #element with time and amount of findings
            print(element.text)
            browser.find_element_by_name('q').clear()                                                                   #clearing the search field
        print('Performance stats have been printed')
        print('OK')

    def test_no_result(self):                                                                                           #checking if particular information is provided to user
        print('\n-----------------testing no result use case-----------------')
        browser=self.browser
        elem = browser.find_element_by_name('q')                                                                        #Find the search box
        elem.send_keys('>>>>' + Keys.RETURN)                                                                            #sending element from table and click enter
        element = browser.find_element_by_tag_name('em')                                                                #this element contains information about which characters wasn't find.
        assert '>>>>' in element.text                                                                                   #assert if element has been found
        browser.back()                                                                                                  #back to previous page
        print('No result information has been shown')
        print('OK')

    def test_advert(self):                                                                                              #checking if advertising is present
        print("\n-----------------testing advert presence-----------------")
        browser=self.browser
        elem = browser.find_element_by_name('q')                                                                        #Find the search box
        elem.send_keys('aspirin' + Keys.RETURN)
        element = browser.find_element_by_class_name('VqFMTc.NceN9e')                                                   #this element contains Ad object.
        assert 'Ad' in element.text                                                                                     #assert if Ad is indeed present
        browser.back()
        print('Ad has been found')
        print('OK')

    def test_tips_drop_down_list(self):                                                                                 #checking what tips are shown for user when providing particular word. Tips will be wrote to console.
        print('\n-----------------testing tips-----------------')
        search_phrase = 'java'
        browser=self.browser
        elem = browser.find_element_by_name('q')  # Find the search box
        elem.send_keys(search_phrase)
        time.sleep(1)
        tips_amount = len(browser.find_elements_by_class_name('sbct'))-1                                                #last element of this class is empty. So it is bypassed.
        assert tips_amount >= 10                                                                                        #tips_amount should be at least 10 by it might be zero. Then fail the test as there is no tips.
        for element in browser.find_elements_by_class_name('sbct')[:-1]:                                                #last element from this class is always empty so we don't use is to assertion
            print(element.text)
            assert search_phrase in element.text                                                                        #assert if tips have main word in it. If not then fail test.
        print('Amount of successfully asserted tips is: %d' % tips_amount)                                              #print amount of tips
        print('OK')

    def TearDown(self):                                                                                                 #postconditions
        time.sleep(1)
        self.browser.quit()                                                                                             #Close all opened windows.
        print('Test have been finished you can find logs in: %s/%s' % (os.getcwd(), log_file_pat))


if __name__ == '__main__':                                                                                              #standard way of bypassing problem when module will be imported. In this way __name__ won't be __main__ and program won't run
    open(console_prints_path, 'w').close()                                                                              #file needs to be cleared before another round of test.
    open(log_file_path, 'w').close()                                                                                    #file needs to be cleared before another round of test.
    unittest.main()                                                                                                     #This will run all methods which start from "test".
