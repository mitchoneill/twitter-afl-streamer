from tweepy import Stream, OAuthHandler, streaming
import os
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.websocket
import tornado.httpserver
from jinja2 import Environment, FileSystemLoader
import json

keys = ['CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_TOKEN', 'ACCESS_SECRET']
settings = {key: os.environ[key] for key in keys}

subscribers = set()

template_env = Environment(loader=FileSystemLoader("templates"))


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(streaming.StreamListener):
    @tornado.gen.coroutine
    def on_data(self, data):
        print('received')
        data = json.loads(data)
        print(data['text'])
        for sub in subscribers:
            print('sending')
            sub.write_message({'text': data['text']})

    @tornado.gen.coroutine
    def on_error(self, status):
        print(status)

class MainHandler(tornado.web.RequestHandler): #Class that renders login page
    @tornado.gen.coroutine
    def get(self):
        home_template = template_env.get_template("home.html")
        self.write(home_template.render())

@tornado.gen.coroutine
def twitter_listener():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(settings['CONSUMER_KEY'], settings['CONSUMER_SECRET'])
    auth.set_access_token(settings['ACCESS_TOKEN'], settings['ACCESS_SECRET'])
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#AFLGF'], async=True)


class WSocketHandler(tornado.websocket.WebSocketHandler): #Tornado Websocket Handler

    def check_origin(self, origin):
        return True

    def open(self):
        self.stream.set_nodelay(True)
        subscribers.add(self) #Join client to our league

    def on_close(self):
        if self in subscribers:
            subscribers.remove(self) #Remove client

if __name__ == "__main__":
    # Define tornado application
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_dir, 'static')
    tornado_app = tornado.web.Application([
        ('/', MainHandler),  # For Landing Page
        (r'/ws', WSocketHandler),  # For Sockets
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_folder})
        # Define static folder
    ])

    # Start the server
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8000)  # Bind port 8888 to server
    tornado.ioloop.IOLoop.current().add_callback(twitter_listener)
    tornado.ioloop.IOLoop.instance().start()