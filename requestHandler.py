import requests

class Request:

    def __init__(self,url):
        self.url = url
        if "https://" not in self.url:
            self.url = "https://" + self.url

    def sndreq(self,reqtype,headers={},payload={}):
        response = requests.request(reqtype,url=self.url,headers=headers,data=payload)
        return response.status_code,response.headers



# req = Request("www.google.com")
# hd = dict("{'Cookie': 'NID=204=XBWS-nnoVMRGwvvV6C41rm8QoTinHDPtlnJAmZO1eRG-aedeq0pubo0SlVfbjV7-L8KmpcBtM1qFXbm6adkuXgtfD_-IgihpgQX1GkXWiJsopWfVJd1vn5hTAvivT5bxYuWOEf47aac9aUqSOibtT3TmyvVlt0hz5zr-bAnzyqk'}")
# print(req.sndreq(reqtype="GET",headers=hd))
