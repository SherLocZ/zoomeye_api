#coding=utf-8
import requests
import json


class zoomeye():
    #定义一个zoomeye对象
    def __init__(self):
        #初始化定义header HTTP头方便后续的使用
        self._headers = {
            "Authorization": "JWT %s" % self.get_token(),
            "Content-Type": "application/json"
        }

    def get_token(self):
        #获取所需要的token值
        url = "https://api.zoomeye.org/user/login"
        data = {
            "username":"799843458@qq.com",
            "password":"sher10ck"
        }
        r = requests.post(url,data=json.dumps(data))
        # access_token = json.loads(r.content)['access_token']
        # print json.loads(r.content)
        return json.loads(r.content)['access_token']

    def get_content(self,keywords,searchtype="web",page="1"):
        url = "https://api.zoomeye.org/%s/search?query=%s&page=%s" %(searchtype,keywords,page)
        # print(url)
        r = requests.get(url,headers=self._headers)
        # print(r.content)
        page_content = json.loads(r.content)
        return page_content

    def write_in_file(self,filename,list):
        with open(filename,"a+") as f:
            for ip in list:
                f.write(str(ip) + "\r\n")
            f.close()

    def search(self,keywords,searchtype="web",page="1"):
        url = "https://api.zoomeye.org/%s/search?query=%s&page=%s" % (searchtype, keywords, page)
        page = self.get_page(url)
        print("[+]A total of {0} page".format(page))
        for i in range(1,page):
            ip_list = []
            page_content = self.get_content(keywords,searchtype,i)
            print(page_content)
            for j in range(20):
                print(page_content['matches'][j]['ip'][0])
                ip_list.append(page_content['matches'][j]['ip'][0].encode('utf-8'))
            print(ip_list)
            self.write_in_file("ip_list.txt",ip_list)


    def get_page(self,url):
        r = requests.get(url, headers=self._headers)
        page_content = json.loads(r.content)
        total = page_content['total']
        print("[+]Search keywords total :" + str(total))
        page = total / 20
        if page % 20 == 0:
            return (page)
        return (page + 1)

if __name__ == '__main__':
    zoomeye = zoomeye()
    print "[+]Your access_token is :" + zoomeye.get_token()
    #这里输入关键字
    zoomeye.search("weblogic",searchtype="web")
