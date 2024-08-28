##############################################################################
# COPYRIGHT Ericsson AB 2016
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

from litp.core.model_type import ItemType, Property, PropertyType
from litp.core.extension import ModelExtension


class ExampleExtension(ModelExtension):
    """
    Example Model Extension.
    """

    def define_property_types(self):
        """
        Define any property types you need here, core-plugin has alot defined
        already.
        """
        property_types = list()
        property_types.append(PropertyType("conf_file_name",
                                           regex=r"^[a-zA-Z0-9\-\._]+$"))
        return property_types

    def define_item_types(self):
        item_types = list()
        item_types.append(
            ItemType(
                "example-conf",
                 extend_item='software-item',
                 item_description="This item type represents a example-conf",
                 name=Property("conf_file_name",
                               prop_description="Name of the example-conf",
                               required=True)
                )
        )
        return item_types
