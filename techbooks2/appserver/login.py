import urllib3
import urllib
from .utility import load_json

def login_server(Guests, id, pw):
    if admin_login(id[1:], pw):
        return '{"result_msg" : "Y", "role_info" : "admin"}'
    if id.startswith('guest_'):
        try:
            return guest_login(Guests, id[1:], pw)
        except:
            return '{"result_msg" : "N", "role_info" : "guest", "Msg" : "no id"'
    else:
        url = ''#removed for security reason.
        url = url + id
        url = url + '&password='
        url = url + urllib.parse.quote(pw)
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        response = response.data.decode("utf-8")
        response = load_json(response)
    return '{"result_msg": "' + response.get('Result') + '", "role_info" : "innocean"}'


def guest_login(Guests, id, pw):
    guest = Guests.objects.get(id=id)
    if guest.pw == pw:
        guest.view_count_up()
        return '{"return_msg" : "Y", "role_info" : "guest"}'
    return '{"return_msg" : "N", "role_info" : "guest", "Msg" : "password error"}'


def admin_login(id, pw):
    if id == "creativealpha" and pw == "alpha@16f":
        return True
    return False
