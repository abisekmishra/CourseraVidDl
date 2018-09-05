import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Scraper:

    driver = None
    src_dict = None
    CURR_PATH = os.getcwd()
    cera_url = "https://www.coursera.org"
    course_hrefs = {}

    def __init__(self):

        self.src_dict = dict()
        #self.src_dict['Home_Page'] = "/home/abisek/Python/CourseraVidDl/sources/Home_Page.html"
        # Connect to the Chrome Driver. This opens the browser window and establishes connection
        # Better to maximize the window as dynamic pages change their layout when window size varies
        # Opens the coursera page
        if not self.cera_url==None:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.implicitly_wait(5)
            self.driver.get(self.cera_url)
            self._savePageSrc("Login_Page",self.driver.page_source)


    def login(self,debug = False):

        if debug == True: return self.driver
        # Switch to the LOG IN tab

        if self.driver.find_element_by_link_text("LOG IN") != None:
            self.driver.find_element_by_link_text("LOG IN").click()
        else:
            self.driver.find_element_by_link_text("Log In").click()

        #Search for the respective input form and find the fields to enter email and password and the submit button
        form = self.driver.find_element_by_xpath("//form[@name='login']")
        email_field = form.find_element_by_xpath("//input[@name='email']")
        pass_field = form.find_element_by_xpath("//input[@name='password']")
        submit_btn = form.find_element_by_tag_name("button")

        # Feed email and password to the respective field and submit the form
        email_field.send_keys("avisektalks@gmail.com")
        pass_field.send_keys("Avisek@4326")
        submit_btn.click()

        #Save all course pages source
        self._click_more_chevron()
        self._savePageSrc("Home_Page", self.driver.page_source)

        self.driver.execute_script("window.scrollTo(0,0)")
        self.driver.find_element_by_link_text('Inactive').click()
        self._click_more_chevron()
        time.sleep(2)
        self._savePageSrc("Inactive_courses_Page", self.driver.page_source)

        self.driver.execute_script("window.scrollTo(0,0)")
        self.driver.find_element_by_link_text('Completed').click()
        self._click_more_chevron()
        time.sleep(2)
        self._savePageSrc("Completed_courses_Page", self.driver.page_source)


        #Returning Driver for debugging purposes
        return self.driver


    def search_available_courses(self):

        #Save the page source and open it in beautiful soup to fetch all the courses the user is enrolled in
        #Courses are divided into 3 categories - Last Active, Inactive and Completed
        #If inactive courses are directly opened they will switch to active.Those courses better not be opened in the current window


        for filename in ['Home_Page','Inactive_courses_Page','Completed_courses_Page']:
            soup = BeautifulSoup(open(self.src_dict[filename],'r'),'html.parser')
            return_val = self._get_courses(soup,self.course_hrefs)
            course_hrefs = return_val if return_val!=None else self.course_hrefs


        '''#Finding last active courses from My Coursera page
        soup = BeautifulSoup(open(self.src_dict['Home_Page'],'r'),'html.parser')
        self._get_courses(soup,course_hrefs)
        print(course_hrefs)

        soup = BeautifulSoup(open(self.src_dict['Inactive_courses_Page'],'r'),'html.parser')
        self._get_courses(soup,course_hrefs)
        print(course_hrefs)

        soup = BeautifulSoup(open(self.src_dict['Completed_courses_Page'],'r'),'html.parser')
        self._get_courses(soup,course_hrefs)
        print(course_hrefs)'''

        return course_hrefs


    def _savePageSrc(self,pg_name,pg_src):

        file_abs_path = os.path.join(self.CURR_PATH,"sources",(pg_name+".html"))
        with open(file_abs_path,'w') as file:
            file.write(pg_src)

        self.src_dict[pg_name] = file_abs_path


    def _click_more_chevron(self):
        more_chevrons = self.driver.find_elements_by_xpath(
            "//button[@class='nostyle dropdown']")
        if len(more_chevrons) != 0:
            for more_chevron in more_chevrons:
                more_chevron.click()


    def _get_courses(self,soup,course_hrefs):

        tmp_dict = course_hrefs
        section_list = soup.find_all('section', attrs={"class": ["rc-CourseCard", "with-padding"]})
        modified_section_list = soup.find_all('section',attrs={"class":"rc-CourseCard with-padding card-rich-interaction".split()})

        section_list = list(set(section_list+modified_section_list))

        if len(section_list) == 0: return None

        for section in section_list:

            check_enrollment = section.find('div',attrs={"class":"rc-CourseEnrollButton"})
            #print(check_enrollment)
            enroll_text = check_enrollment.find('span').text if check_enrollment!=None else 'None'

            if enroll_text != 'Enroll':
                name = section.find('h4', attrs={"class": "headline-1-text"}).text
                href_link = section.find("a", href=True)['href']
                tmp_dict[name] = href_link

        return tmp_dict


    def _get_weeks(self,course_name):

        course_url = self.cera_url + self.course_hrefs[course_name]
        self.driver.get(course_url)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        div_weeks = soup.find('div',attrs={'class':'rc-NavigationDrawer'})
        weeks = div_weeks.find_all('a',attrs={'class' : "rc-NavigationDrawerLink headline-1-text horizontal-box \
                                                   rc-WeekNavigationItem".split()})

        return len(weeks)


    def search_videos_per_week(self,week):

        lecture_hrefs = {}

        self.driver.execute_script('window.scrollTo(0,0)')
        old_url = self.driver.current_url
        #week_url = course_url+"/week/"+week
        self.driver.find_element_by_link_text("Week "+str(week)).click()

        while self.driver.current_url == old_url:pass
        soup = BeautifulSoup((self.driver.page_source),'html.parser')
        lesson_divs = soup.find_all('div',attrs={'class':'rc-NamedItemList'})

        lessons = []
        for div in lesson_divs:
            if div.find('h4').text != "Review":
                for li in div.find_all('li'):
                    lessons.append(li)

        c=1
        for lesson in lessons:
            lesson_div = lesson.find('div',attrs={'class':'rc-WeekItemName headline-1-text'.split()})
            lesson_div.find('span').replace_with('')
            lecture_link = lesson.find('a')['href']
            if "/lecture/" in lecture_link:
                lecture_name = lesson_div.text
                lecture_hrefs[(str(c)+". "+lecture_name)] = cera_url + lecture_link
                c+=1

        return lecture_hrefs


    def _get_videos(self,lecture_hrefs):
        vid_links = []
        for key,value in lecture_hrefs.items():
            self.driver.get(value)
            soup = BeautifulSoup(self.driver.page_source)
            vid_links.append([key,soup.find('video').find('source')['src']])
            _download_videos(vid_links)


    def _download_videos(self,vid_links):
        for vid in vid_links:
            print("Downloading {}".format(vid[0]))
            with open(str(vid[0])+'.mp4','wb') as f:
                video = requests.get(vid[1],stream=True)
                f.write(video.content)


    def logout(self,close=False):

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
            for file in os.listdir(os.path.join(self.CURR_PATH,"sources")):
                os.remove(os.path.join(self.CURR_PATH,"sources",file))
