from selenium import webdriver
from time import sleep
from secrets import username, password

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.get("http://instagram.com/")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(1)

    def _get_names(self):
        sleep(2)    # wait for loading
        # Find scroll box and scroll until all users are loaded
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        sleep(1)

        # capture all usernames and put them into a list
        links = scroll_box.find_elements_by_tag_name("a")
        names = [name.text for name in links if name.text != ""]
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()

        return names

    def get_unfollowers(self):
        # open logged-in user's profile page and open their 'following'
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/following')]".format(self.username)).click()
        print()
        print("Capturing following...")
        following = self._get_names()
        print("Following captured")
        print()

        # open logged-in user's profile page and open their 'followers'
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