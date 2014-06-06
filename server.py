#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.escape
import json

class GenAsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        ld = {}
        td = {'EU':0,'US':0,'AU':0}
        for p in range(1,6):
            try:
                response = yield http_client.fetch("http://api.whelp.gg/corporation/98182803?page="+str(p))
                j = tornado.escape.json_decode(response.body)
            except tornado.httpclient.HTTPError as err:
                if err.code == 404:
                    break
                else:
                    raise
            for i in j['kills']:
                ld.setdefault(i['system_name'],0)
                ld[i['system_name']] += 1
            for i in j['kills']:
                c = int(str(i['kill_time'])[11:13])
                if c >= 0 and c < 8:
                    td['US']+=1
                elif c >= 8 and c < 16:
                    td['AU']+=1
                elif c >= 16:
                    td['EU']+=1
        sd = sorted(list(ld.items()), key=lambda p: -p[1])
        st = sorted(list(td.items()), key=lambda p: -p[1])
        ws="Kill Systems\n" + str(sd) + "Kill TZ\n" + str(st)
        self.render("template.html",sd=sd,st=st)
        

application = tornado.web.Application([
    (r"/", GenAsyncHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
