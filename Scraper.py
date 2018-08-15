import os
from selenium import webdriver
from bs4 import BeautifulSoup

class Scraper:

    driver = None
    src_dict = None

    def __init__(self,cera_url=None):

        self.src_dict = dict()
        #self.src_dict['Home_Page'] = "/home/abisek/Python/CourseraVidDl/sources/Home_Page.html"
        # Connect to the Chrome Driver. This opens the browser window and establishes connection
        # Better to maximize the window as dynamic pages change their layout when window size varies
        # Opens the coursera page
        if not cera_url==None:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()

            self.driver.get(cera_url)
            self._savePageSrc("Login_Page",self.driver.page_source)
            while self.driver.current_url == cera_url:pass


    def _savePageSrc(self,pg_name,pg_src):

        file_abs_path = os.path.join("/home/abisek/Python/CourseraVidDl","sources",(pg_name+".html"))
        with open(file_abs_path,'w') as file:
            file.write(str(pg_src))

        self.src_dict[pg_name] = file_abs_path


    def login(self):


        # Switch to the LOG IN tab
        self.driver.find_element_by_link_text("LOG IN").click()


        #Search for the respective input form and find the fields to enter email and password and the submit button
        form = self.driver.find_element_by_xpath("//form[@name='login']")
        email_field = form.find_element_by_xpath("//input[@id='emailInput-input']")
        pass_field = form.find_element_by_xpath("//input[@id='passwordInput-input']")
        submit_btn = form.find_element_by_tag_name("button")

        # Feed email and password to the respective field and submit the form
        email_field.send_keys("avisektalks@gmail.com")
        pass_field.send_keys("Avisek@4326")
        submit_btn.click()

        self._savePageSrc("Home_Page",self.driver.page_source)




    def search_available_courses(self):

        #Save the page source and open it in beautiful soup to fetch all the courses the user is enrolled in
        #Courses are divided into 3 categories - Last Active, Inactive and Completed
        #If inactive courses are directly opened they will switch to active.Those courses better not be opened in the current window

        course_hrefs = []

        #Finding last active courses from My Coursera page
        soup = BeautifulSoup(open(self.src_dict['Home_Page'],'r'),'html.parser')
        self._get_courses(soup,course_hrefs)

        soup = BeautifulSoup(open(self.src_dict['Inactive_courses_Page'],'r'),'html.parser')
        self._get_courses(soup,course_hrefs)

        soup = BeautifulSoup(open(self.src_dict['Completed_courses_Page'],'r'),'html.parser')
        self._get_courses(soup,course_hrefs)

        return course_hrefs



    def _get_courses(self,soup,course_hrefs):

        section_list = soup.find_all('section', attrs={"class": ["rc-CourseCard", "with-padding"]})
        if len(section_list) == 0: return None

        for section in section_list:

            enroll_option = section.find('span', attrs={"class": ["headline-1-text", "enroll-text"]})

            if enroll_option == None or enroll_option.text == "Go to Course":
                name = section.find('h4', attrs={"class": "headline-1-text"}).text
                href_link = section.find("a", href=True)['href']
                course_hrefs[name] = href_link

        return


    def _get_weeks(self):
        pass



    def _get_videos_per_week(self):
        pass





    def logout(self):

        try:
            #Click the dropdown list on the extreme right and log off the account
            self.driver.find_element_by_xpath("//button[@id='right-nav-dropdown-btn']").click()
            self.driver.find_element_by_xpath("//ul[@id='c-ph-aai-dropdown']//li//form//button").click()

        except:
            self.driver.refresh()
            self.driver.find_element_by_xpath("//button[@id='right-nav-dropdown-btn']").click()
            self.driver.find_element_by_xpath("//ul[@id='c-ph-aai-dropdown']//li//form//button").click()

        finally:
            self.driver.close()
