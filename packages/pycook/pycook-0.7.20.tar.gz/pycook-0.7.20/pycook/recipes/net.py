#* Imports
import re
import pycook.elisp as el
sc = el.sc

#* Functions
def this_ip():
    out = el.sc("ip route get 1.1.1.1")
    ms = re.findall("src ([0-9.]+)", out)
    assert(len(ms) == 1)
    return ms[0]

#* Recipes
def ip(recipe):
    print(this_ip())

def ipp(recipe):
    # install dnsutils on Debian
    print(el.sc("dig +short myip.opendns.com @resolver1.opendns.com"))
