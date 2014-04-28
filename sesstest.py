import web


urls = (
    '/', 'index'
)
app = web.application(urls, globals())
class index:
    def GET(self):
        s = web.ctx.session
        s.start()

        try:
            s.click += 1
        except AttributeError:
            s.click = 1

        print 'click: ', s.click
        s.save()

if __name__ == '__main__':
    app.run(urls, globals(), web.reloader)