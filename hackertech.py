import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os, uuid
from image_process import dirty_percentage


__UPLOADS__ = "./uploads/"

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        #print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        #print fileinfo['body']

        result=dirty_percentage("uploads/"+cname)
        self.add_header("Access-Control-Allow-Origin", "*")
        self.render("result.html", result = result)



application = tornado.web.Application([
        (r"/", Userform),
        (r"/upload", Upload),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': "./"}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path': "./"}),
        ], debug=False)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)

    tornado.ioloop.IOLoop.instance().start()