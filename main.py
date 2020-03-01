from selenium import webdriver
from time import sleep
from secrets import username, password

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)

        # go to home page
        self.driver.get("http://instagram.com/")
        # click log in button
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[2]/p/a")\
            .click()
        # enter username
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")\
            .send_keys(username)
        # enter password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        # click submit button
        self.driver.find_element_by_xpath("//button[@type='submit']")\
            .click()
        # click 'Not Now' to get rid of pop up
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()

    def _get_names(self):
        # Find scroll box and scroll until all users are loaded
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            # need to wait for the next users to load
            sleep(1)    # need to improve this in the future, it adds the most time to this program
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)

        # capture all usernames and put them into a list
        links = scroll_box.find_elements_by_tag_name("a")
        names = [name.text for name in links if name.text != ""]    # this also adds a lot of time to program... improve in future?
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()

        return names

    def get_unfollowers(self):
        # open logged-in user's profile page and open their 'following'
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/following')]".format(self.username)).click()
        print()
        print("Capturing following...")
        following = self._get_names()
        print("Following captured")
        print()

        # open their 'followers'
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers')]".format(self.username)).click()
        print("Capturing followers...")
        followers = self._get_names()
        print("Followers captured")
        print()

        # return usernames of people who don't follow you back
        return [name for name in following if name not in followers]

    def shut_down(self):
        self.driver.quit()

if __name__ == "__main__":
    mybot = InstaBot(username, password)
    print(mybot.get_unfollowers())
    mybot.shut_down()