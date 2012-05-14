import os
import pkg_resources
from flask import Flask, helpers, render_template, Blueprint
from jinja2 import loaders

class ResourceMixin(object):
    PACKAGENAME = "demo_pkgrsrc"
    
    @helpers.locked_cached_property
    def jinja_loader(self):
        return loaders.PackageLoader(self.PACKAGENAME, self.template_folder)

    def send_static_file(self, filename):
        fname = helpers.safe_join(self._static_folder, filename)
        f = pkg_resources.resource_stream(self.PACKAGENAME, fname)
        return helpers.send_file(f, attachment_filename=filename)


class ZippedFlask(ResourceMixin, Flask):
    pass


class ZippedBlueprint(ResourceMixin, Blueprint):
    pass

            
app = ZippedFlask(__name__)

blueprint = ZippedBlueprint('blueprint_test', __name__, template_folder='templates2', static_folder='blueprint_static', static_url_path='/static2') 

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@blueprint.route('/blueprint/')
@blueprint.route('/blueprint/<name>')
def hello2(name=''):
    return render_template('hello2.html', name=name+" blueprint")

app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
