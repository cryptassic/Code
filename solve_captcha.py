import sys
import coloredlogs, logging

from twocaptcha import TwoCaptcha

LOGGER = logging.getLogger(__name__)
coloredlogs.install(fmt='%(asctime)s,%(msecs)03d %(levelname)s %(message)s')


class CaptchaDestroyer:
    def __init__(self,api_key:str):
        self.solver = TwoCaptcha(api_key)
        LOGGER.info(f"2Captcha Balance: {self.solver.balance()} $")

    def solve_hCaptcha(self,data_sitekey:str,pageurl:str):
        try:
            LOGGER.info(f"Solving hCaptcha...")
            result = self.solver.hcaptcha(sitekey=data_sitekey,url=pageurl)
        except Exception as e:
            LOGGER.error(f"{e}")
            sys.exit()
        else:
            LOGGER.info(f"OK ID:{result['captchaId']}")
            return result['code']
        
