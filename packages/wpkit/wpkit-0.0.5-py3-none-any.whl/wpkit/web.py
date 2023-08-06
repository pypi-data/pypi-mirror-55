import flask
from flask import Flask
import pkg_resources

from flask import Flask, request, Blueprint, abort, send_file
from jinja2 import Environment
from . import piu
import os, glob, uuid

def render(s, *args, **kwargs):
    env = Environment()
    tem = env.from_string(s)
    return tem.render(*args, **kwargs)

def join_path(*args):
    path = []
    for i, s in enumerate(args):
        if s.strip() == '':
            continue
        if i == 0:
            path.append(s.rstrip('/'))
        elif i == len(args) - 1:
            path.append(s.lstrip('/'))
        else:
            path.append(s.strip('/'))
    path = '/'.join(path).replace('//', '/')
    return path

class App(Flask):
    def __init__(self, import_name ,dbpath='./data/db'):
        super().__init__(import_name)
        self.default_templates = {
            'welcome': pkg_resources.resource_filename('wpkit', 'data/templates/welcome.html'),
            'files': pkg_resources.resource_filename('wpkit', 'data/templates/files.html'),
            'board': pkg_resources.resource_filename('wpkit', 'data/templates/board.html')
        }
        self.db=piu.Piu(dbpath)
    def get_default_template_string(self,tem):
        return open(self.default_templates[tem],'r',encoding='utf-8').read()
    def add_default_route(self):
        @self.route('/')
        def do_root():
            temf = self.default_templates['welcome']
            return render(open(temf, 'r', encoding='utf-8').read())
        @self.route('/board')
        def do_board():
            data=self.db.get('board_data','')
            return render(self.get_default_template_string('board'),content=data)
        @self.route('/board/post',methods=['POST'])
        def do_board_post():
            data=request.get_json()
            print('board data:%s'%(data))
            self.db.add('board_data',data['content'])
            return 'success'
    def add_multi_static(self, dic):
        for k, v in dic.items():
            self.add_static(k, v)

    def add_static(self, url_prefix, static_dir, template=None, name=None):
        name = 'static_bp_' + uuid.uuid4().hex if not name else name
        bp = self.static_bp(url_prefix=url_prefix,static_dir=static_dir, template=template, name=name)
        self.register_blueprint(bp)

    def static_bp(self,url_prefix, static_dir, template=None, name='static_bp'):
        template = self.default_templates['files'] if not template else template
        bp = Blueprint(name=name, import_name=__name__,url_prefix=url_prefix)

        @bp.route('/', defaults={'req_path': ''})
        @bp.route(join_path('/', '<path:req_path>'))
        def dir_listing(req_path):
            BASE_DIR = static_dir
            abs_path = os.path.join(BASE_DIR, req_path)
            if not os.path.exists(abs_path):
                return abort(404)
            if os.path.isfile(abs_path):
                return send_file(abs_path)
            if os.path.isdir(abs_path):
                fns = os.listdir(abs_path)
                fps = [join_path(url_prefix, req_path, f) for f in fns]
                return render(open(template, 'r', encoding='utf-8').read(), files=zip(fps, fns))

        return bp
def start_simple_http_server(import_name,host='127.0.0.1',port=80,static={'/fs':'./'}):
    app = App(import_name=import_name)
    app.add_default_route()
    app.add_multi_static(static)
    print(app.url_map)
    app.run(host=host,port=port)

if __name__ == '__main__':
    start_simple_http_server(__name__)