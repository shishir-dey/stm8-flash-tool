import urllib.request

try:
    c = urllib.request.urlopen("http://139.59.27.234:8070/prog?mcu=3k3&product=erd&status=OK").read()
    print(c)
except Exception:
    print("Error")