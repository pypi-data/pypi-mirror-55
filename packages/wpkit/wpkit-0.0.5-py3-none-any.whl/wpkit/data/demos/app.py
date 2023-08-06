import wpkit
from wpkit.web import App
def demo():
    app = App(__name__)
    app.add_default_route()
    app.add_multi_static({
        '/fs': './',
        '/root': 'd:/'
    })
    print(app.url_map)
    app.run(host='127.0.0.1', port=80)

if __name__ == '__main__':
    demo()