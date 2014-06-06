#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.escape
import json

class Homepage(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("homepage.html")

class SearchHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http_client=tornado.httpclient.AsyncHTTPClient()
        query = self.get_query_argument('query')
        response = yield http_client.fetch("http://api.whelp.gg/search?q="+tornado.escape.url_escape(query, plus=False))
        j = tornado.escape.json_decode(response.body)
        self.render('search.html',j=j,query=query)

class ProfilePage(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, profile_type, profile_id):
        http_client=tornado.httpclient.AsyncHTTPClient()
        system_dic = {}
        timezone_dic = {'EU':0,'US':0,'AU':0}
        for p in range(1,6):
            try:
                response = yield http_client.fetch("http://api.whelp.gg/"+profile_type+"/"+profile_id+"?page="+str(p))
                j = tornado.escape.json_decode(response.body)
            except tornado.httpclient.HTTPError as err:
                if err.code == 404:
                    break
                else:
                    raise
            for i in j['kills']:
                system_dic.setdefault(i['system_name'],0)
                system_dic[i['system_name']] += 1
            for i in j['kills']:
                c = int(i['kill_time'][11:13])
                if c >= 0 and c < 8:
                    timezone_dic['US']+=1
                elif c >= 8 and c < 16:
                    timezone_dic['AU']+=1
                elif c >= 16:
                    timezone_dic['EU']+=1
        sorted_systems = sorted(list(system_dic.items()), key=lambda p: -p[1])
        sorted_timezone = sorted(list(timezone_dic.items()), key=lambda p: -p[1])
        j = tornado.escape.json_decode((yield http_client.fetch("http://api.whelp.gg/"+profile_type+"/"+profile_id)).body)
        name = j['stats'][profile_type+'_name']
        self.render("profile_page.html",sd=sorted_systems,st=sorted_timezone,name=name)
        

application = tornado.web.Application([
    (r"/", Homepage),
    (r"/search",SearchHandler),
    (r"/(character|corporation|alliance)/(\d+)",ProfilePage)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
