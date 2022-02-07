import random
import string
from make_form import Form
from requests_toolbelt import MultipartEncoder

def get_payload(form:Form):
    boundary = '----WebKitFormBoundary' \
           + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return MultipartEncoder(fields=form, boundary=boundary)