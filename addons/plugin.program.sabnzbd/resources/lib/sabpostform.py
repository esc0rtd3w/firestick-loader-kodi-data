# http://www.doughellmann.com/PyMOTW/urllib2/
import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib2

import sabutils


def post(path, apikey, url, **kwargs):
    output = kwargs.get('output', 'xml')
    cat = kwargs.get('cat', 'Default')
    priority = kwargs.get('priority', '-100')
    pp = kwargs.get('pp', '-1')
    nzbname = kwargs.get('nzbname', '')
    form = MultiPartForm() 
    nzb_data = sabutils.read(path, 'rb')
    form.add_field('apikey', apikey)
    form.add_field('mode', 'addfile')
    form.add_field('output', output)
    form.add_field('cat', cat)
    form.add_field('priority', priority)
    form.add_field('pp', pp)
    form.add_field('nzbname', nzbname)
    form.add_file('nzbfile', path, fileHandle=StringIO(nzb_data))
    req = urllib2.Request(url)
    body = str(form)
    req.add_header('Content-type', form.get_content_type())
    req.add_header('Content-length', len(body))
    req.add_data(body)
    # Dont care about the response
    sabutils.load_url(url, req, "SABnzbd failed posting data")
    return "ok"

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return
    
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return
    
    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
        
        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
        
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)