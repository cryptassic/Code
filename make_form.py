

from dataclasses import dataclass
from solve_captcha import CaptchaDestroyer
import configparser

@dataclass
class Form:
    resume:str
    name:str
    email:str
    phone:str
    profile_urls:str
    comments:str
    g_recaptcha_response:str
    h_captcha_response:str
    consent:str
    
    def get_form(self):
        return {
            "resume": self.resume,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "org":"",
            "urls[Link to your profile (Linkedin/Github etc.) ]":self.profile_urls, 
            "comments":self.comments, 
            "accountId": "1767d813-f82b-4225-9f32-c942726e3f76",
            "linkedInData":"", 
            "origin":"",
            "referer": "",
            "socialReferralKey":"",
            "source":"", 
            "consent[marketing]": self.consent,
            "g-recaptcha-response": self.g_recaptcha_response,
            "h-captcha-response": self.h_captcha_response
        }
        
class FormMaker:
    def __init__(self,pageurl:str,sitekey:str):
        config = configparser.ConfigParser()
        config.read('config.ini')
    
        captch_config = config['reCaptch']
        
        self.__solver = CaptchaDestroyer(api_key=captch_config['api_key'])
        self.__pageurl = pageurl
        self.__sitekey = sitekey
    
    def get_form(self,resume:str,name:str,email:str,phone:str,profile_urls:str,comments:str):
        
        form = None
        resolved_key = self.__solver.solve_hCaptcha(pageurl=self.__pageurl,data_sitekey=self.__sitekey)
        
        if resolved_key:
            form = Form(
                resume=resume,
                name=name,
                email=email,
                phone=phone,
                profile_urls=profile_urls,
                comments=comments,
                g_recaptcha_response=resolved_key,
                h_captcha_response=resolved_key,
                consent="0").get_form()
        
        return form
