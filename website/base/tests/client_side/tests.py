from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class ClientSideTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.selenium.quit()

    def test_menus(self):
        import logging
        logging.debug("test")
        test_cases = [
            {
                "path": "/",
                "tag_location": '//*[@id="my-top-nav-list"]//a[@href="/"]'
            },
            {
                "path": "",
                "tag_location": '//*[@id="my-top-nav-list"]//a[@href="/"]'
            },
            {
                "path": "/projects",
                "tag_location": '//*[@id="my-top-nav-list"]//a[@href="/projects"]'
            },
            {
                "path": "/blog",
                "tag_location": '//*[@id="my-top-nav-list"]//a[@href="/blog"]'
            },
            {
                "path": "/about",
                "tag_location": '//*[@id="my-top-nav-list"]//a[@href="/about"]'
            },
            {
                "path": "/contact",
                "tag_location": '//*[@id="my-top-nav-list"]//a[@href="/contact"]'
            },
        ]
        for case in test_cases:
            self.selenium.get("%s%s" % (self.live_server_url, case["path"]))
            element = self.selenium.find_element_by_xpath(case["tag_location"])
            parent = element.find_element_by_xpath("..")
            classes = parent.get_attribute("class")
            self.assertIs("active" in classes, True)