from Scraper import Scraper
import logging

logging.getLogger().setLevel(logging.INFO)
if __name__ == '__main__':

    logging.info("Running Driver")
    try:
        logging.info("Initializing Scraper Object")
        scraper = Scraper("https://www.coursera.org/")
        logging.info("Scraper Initialized")

        logging.info("Logging In to the account")
        scraper.login()
        logging.info("Logged In Successfully!")

        logging.info("Logging out of the account!")
        scraper.logout()
        logging.info("Logged out and closed the driver!")

    except Exception as e:
        logging.error("Exception Thrown")
        logging.critical(str(e))


