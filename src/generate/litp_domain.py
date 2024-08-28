def setup(app):
    app.add_crossref_type('item-type', 'itype', 'Item Types; %s')
    app.add_crossref_type('property-type', 'ptype', 'Property Types; %s')
    app.add_crossref_type('model-extension', 'mextension',
                          'Model Extensions; %s')
    app.add_crossref_type('litp-plugin', 'lplugin', 'Plugins; %s')
