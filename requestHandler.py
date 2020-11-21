import requests

class Request:

    def __init__(self,url):
        self.url = url
        if "http://" not in self.url and "https://" not in self.url:
            self.url = "https://" + self.url
    def sndreq(self,reqtype,headers={},payload={}):
        response = requests.request(reqtype,url=self.url,headers=headers,data=payload)
        try : a = response.json()
        except : return response.status_code,response.headers,response.text
        else : return response.status_code,response.headers,response.json()



# req = Request("www.google.com")
# print(req.sndreq(reqtype="GET"))
