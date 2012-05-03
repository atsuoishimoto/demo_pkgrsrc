import os
import pkg_resources
from flask import Flask, helpers, render_template
from jinja2 import loaders

class ZippedFlask(Flask):
    PACKAGENAME = "demo_pkgrsrc"
    static_resource = "static"
    
    @helpers.locked_cached_property
    def jinja_loader(self):
        return loaders.PackageLoader(self.PACKAGENAME)

    def send_static_file(self, filename):
        filename = helpers.safe_join(self.static_resource, filename)
        f = pkg_resources.resource_stream(self.PACKAGENAME, filename)
        return helpers.send_file(f)
            
app = ZippedFlask(__name__)

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    app.run()
