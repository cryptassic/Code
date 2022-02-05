from make_form import FormMaker
import requests
import configparser

from solve_captcha import LOGGER

def load_resume(filepath):
    with open(filepath,'rb') as resume_file:
        resume_data = resume_file.read()
    
    return resume_data

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    oxy_config = config['Oxy']
    user_config = config['USER']
    
    encoded_resume = load_resume('Resume.pdf')
    name = user_config['name']
    email = user_config['email']
    phone = user_config['phone']
    profile_url = user_config['profile_url']
    comment_section = user_config['comment']

    fm = FormMaker(pageurl=oxy_config['pageurl'],sitekey=oxy_config['sitekey'])

    prebuilt_form = fm.get_form(
        resume=encoded_resume,
        name=name,
        email=email,
        phone=phone,
        profile_urls=profile_url,
        comments=comment_section
    )
    
    #Burp Suite
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.post(url="http://google.com",files=prebuilt_form,proxies=proxies)
    
    # response = requests.post(url=oxy_config['pageurl'],files=prebuilt_form)
    
    if response.status_code == 200:
        LOGGER.info("Success!")
    else:
        LOGGER.error("Failed!")
    

if __name__ == "__main__":
    main()
