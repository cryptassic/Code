
import json
from requests import Response
import requests 
import configparser

from prep_payload import PayloadMaterials, PayloadBuilder
from solve_captcha import LOGGER


def load_resume(filepath):
    with open(filepath, 'rb') as resume_file:
        resume_data = resume_file.read()

    return resume_data


class LazyResume:
    def __init__(self,debug=False):
        self.debug_mode = debug
        self.__oxy_config = None
        self.__user_config = None
        self.__cookies = None
        self.__headers = None

        self.__load_config()

    def __load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.__oxy_config = config['Oxy']
        self.__user_config = config['USER']

        self.__cookies = json.loads(self.__oxy_config['cookies'])
        self.__headers = json.loads(self.__oxy_config['headers'])

        assert self.__cookies is not None, "Cookies not set"
        assert self.__headers is not None, "Headers not set"

    def __get_payload_materials(self) -> PayloadMaterials:
        payload_build_materials = None
        try:
            payload_build_materials = PayloadMaterials(
                target_pageurl=self.__oxy_config['pageurl'],
                target_sitekey=self.__oxy_config['sitekey'],
                encoded_resume=('Python_Resume.pdf', load_resume(
                    'Resume.pdf'), "application/pdf"),
                name=self.__user_config['name'],
                email=self.__user_config['email'],
                phone=self.__user_config['phone'],
                profile_url=self.__user_config['profile_url'],
                comment_section=self.__user_config['comment'])
        except Exception as e:
            LOGGER.error(e)
        
        return payload_build_materials
    
    def __handle_response(self,response:Response) -> bool:
        if response.status_code == 200:
            LOGGER.info("Success!")
            return 1
        else:
            LOGGER.error("Failed!")
            return 0
    
    def run(self):
        payload_materials = self.__get_payload_materials()
        
        payload = PayloadBuilder.make_payload(build_materials=payload_materials)
        
        self.__headers.update({"Content-Type": payload.content_type})
        
        proxies = {}
        target_url = self.__oxy_config['pageurl']
        
        if self.debug_mode:
            proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
            target_url = "http://google.com"
        
        try:
            response = requests.post(url=target_url, data=payload, headers=self.__headers, cookies=self.__cookies,proxies=proxies)
        except Exception as e:
            LOGGER.error(e)
        else:
            self.__handle_response(response)


def main():
    lazy_dev = LazyResume()
    lazy_dev.run()

if __name__ == "__main__":
    main()
