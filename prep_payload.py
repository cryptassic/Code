import random
import string
from dataclasses import dataclass

from make_form import Form,FormMaker
from requests_toolbelt import MultipartEncoder


@dataclass
class PayloadMaterials:
    target_pageurl: str
    target_sitekey: str
    encoded_resume: bytes
    name: str
    email: str
    phone: str
    profile_url: str
    comment_section: str
    
class PayloadBuilder:
       
       @classmethod
       def make_payload(cls,build_materials: PayloadMaterials):
              fm = FormMaker(pageurl=build_materials.target_pageurl,
                            sitekey=build_materials.target_sitekey)

              form = fm.get_form(
                     resume=build_materials.encoded_resume,
                     name=build_materials.name,
                     email=build_materials.email,
                     phone=build_materials.phone,
                     profile_urls=build_materials.profile_url,
                     comments=build_materials.comment_section
              )

              payload = cls.__encode_form_to_webkit(form=form)

              return payload

       def __encode_form_to_webkit(self,form:Form):
              boundary = '----WebKitFormBoundary' \
                     + ''.join(random.sample(string.ascii_letters + string.digits, 16))
              
              return MultipartEncoder(fields=form, boundary=boundary)    