##############################################################################
# COPYRIGHT Ericsson AB 2016
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################


import unittest
from example_extension.example_extension import ExampleExtension


class TestExampleExtension(unittest.TestCase):

    def setUp(self):
        self.ext = ExampleExtension()

    def test_property_types_registered(self):
        # Assert that only extension's property types
        # are defined.
        prop_types_expected = ['conf_file_name']
        prop_types = [pt.property_type_id for pt in
                      self.ext.define_property_types()]
        self.assertEquals(prop_types_expected, prop_types)

    def test_item_types_registered(self):
        # Assert that only extension's item types
        # are defined.
        item_types_expected = ['example-conf']
        item_types = [it.item_type_id for it in
                      self.ext.define_item_types()]
        self.assertEquals(item_types_expected, item_types)

if __name__ == '__main__':
    unittest.main()
