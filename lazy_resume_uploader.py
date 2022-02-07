from dataclasses import dataclass
from make_form import FormMaker
from prep_payload import get_payload
import requests
import configparser
import json
from solve_captcha import LOGGER

@dataclass
class PayloadMaterials:
    target_pageurl:str
    target_sitekey:str
    encoded_resume:bytes
    name:str
    email:str
    phone:str
    profile_url:str
    comment_section:str


def load_resume(filepath):
    with open(filepath,'rb') as resume_file:
        resume_data = resume_file.read()
    
    return resume_data


def make_payload(build_materials:PayloadMaterials):
    fm = FormMaker(pageurl=build_materials.target_pageurl,sitekey=build_materials.target_sitekey)

    form = fm.get_form(
        resume=build_materials.encoded_resume,
        name=build_materials.name,
        email=build_materials.email,
        phone=build_materials.phone,
        profile_urls=build_materials.profile_url,
        comments=build_materials.comment_section
    )
    
    payload = get_payload(form=form)
    
    return payload
    
def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    oxy_config = config['Oxy']
    user_config = config['USER']
    
    cookies = json.loads(oxy_config['cookies'])
    headers = json.loads(oxy_config['headers'])
    
    payload_build_materials = PayloadMaterials(
        target_pageurl = oxy_config['pageurl'],
        target_sitekey = oxy_config['sitekey'],
        encoded_resume =('Python_Resume.pdf', load_resume('Resume.pdf'), "application/pdf") ,
        name = user_config['name'],
        email = user_config['email'],
        phone = user_config['phone'],
        profile_url = user_config['profile_url'],
        comment_section = user_config['comment'])
    
    
    payload = make_payload(build_materials=payload_build_materials)
    headers.update({"Content-Type": payload.content_type})
    
    #Burp Suite
    # proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    # response = requests.post(url="http://google.com",data=payload,headers=headers,proxies=proxies,cookies=cookies)
    
    response = requests.post(url=oxy_config['pageurl'],headers=headers,data=payload,cookies=cookies)
    
    if response.status_code == 200:
        LOGGER.info("Success!")
    else:
        LOGGER.error("Failed!")
    

if __name__ == "__main__":
    main()
