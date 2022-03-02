import os
import subprocess

# req = os.system("ping 192.158.2.4")


DNULL = open(os.devnull, 'w')
def ping(host):
    response = os.system("ping " + host)
    if response == 0:
        return True
    else:
        return False


ping("google.com")