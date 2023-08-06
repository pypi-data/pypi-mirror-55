import pkg_resources,os

def get_filepath(fn):
    fn=os.path.join('data',fn)
    return pkg_resources.resource_filename('wpkit',fn)
def get_data(fn):
    fn = os.path.join('data', fn)
    fn=pkg_resources.resource_filename('wpkit',fn)
    with open(fn,'r',encoding='utf-8') as f:
        return f.read()