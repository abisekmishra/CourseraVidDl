from Scraper import Scraper
import logging
import os


logging.getLogger().setLevel(logging.INFO)
if __name__ == '__main__':

    logging.info("Running Driver")
    scraper = None
    try:
        logging.info("Initializing Scraper Object")
        scraper = Scraper()
        logging.info("Scraper Initialized")

        logging.info("Logging In to the account")
        scraper.login()
        logging.info("Logged In Successfully!")

        logging.info("Getting Enrolled Courses")
        courses_dict = scraper.search_available_courses()
        logging.info("Succefully found courses")

        print("You are enrolled following courses")
        for course in courses_dict.items():
            print(course)


    except Exception as e:
        logging.error("Exception Thrown")
        logging.critical(e)
        raise e

    finally:
        logging.info("Logging out of the account!")
        scraper.logout()
        logging.info("Logged out and closed the driver!")
