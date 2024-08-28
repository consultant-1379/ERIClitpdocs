import pydot

from litp.core.model_type import ItemType
from litp.core.model_type import Property
from litp.core.model_type import View
from litp.core.model_type import Child
from litp.core.model_type import Reference
from litp.core.model_type import Collection
from litp.core.model_type import RefCollection


class ClassDiagram(object):
    '''
    Helper class used to generate a class diagram of item types registered
    by a plugin.
    '''

    def generate_data_model_graph(self, items, plugin_id=None, item_type=None):
        '''
        Generates a graph of item and property types using graphviz.
        @param plugin_id: The ID of the plugin for which to generate a data
        model graph. If None, a graph is generated for all plugins that have
        been parsed by this instance of SphinxGenerator
        @type plugin_id: str
        @return None
        '''

        nodes = {}
        graph = pydot.Dot()
        graph.set_nodesep(1.5)
        graph.set_ranksep(1)

        all_items = set()
        if plugin_id:
            all_items = set(items.get(plugin_id, []))
        else:
            for plugin in items:
                for item in items[plugin]:
                    if item_type:
                        if item.item_type_id == item_type:
                            all_items.add(item)
                    else:
                        all_items.add(item)

        # We need to create all itemtype nodes in a first pass, we'll connect
        # them later
        for item in all_items:
            node_name = item.item_type_id
            if node_name == 'node':
                node_name = '"node"'
            item_node = pydot.Node(
                name=node_name,
                shape='Mrecord',
                URL=self.get_url(item.item_type_id, plugin_id)
            )
            nodes[item.item_type_id] = item_node
            graph.add_node(item_node)

        for item in all_items:
            if item.extend_item:
                extension_edge = pydot.Edge(
                    item.item_type_id,
                    item.extend_item,
                    arrowhead="empty"
                )
                graph.add_edge(extension_edge)
                if item.extend_item not in nodes.keys():
                    graph.add_node(self.get_node(item.extend_item, plugin_id))

            if not item.structure:
                nodes[item.item_type_id].set(
                    'label',
                    self._gen_label(item.item_type_id, True)[0]
                )
                continue

            item_attributes = self._gen_label("'" + item.item_type_id + "'",
                                              True)

            for structure_element in item.structure:
                is_link = True
                structure_item = item.structure[structure_element]

                if isinstance(structure_item, Collection):
                    coll_edge = pydot.Edge(
                        self._gen_port_name(structure_item.item_type_id),
                        self._gen_port_name(
                            item.item_type_id,
                            structure_element
                        ),
                        arrowhead='ediamond'
                    )
                    graph.add_edge(coll_edge)
                    if item_type:
                        graph.add_node(
                            self.get_node(structure_item.item_type_id,
                                          plugin_id)
                        )

                elif isinstance(structure_item, Reference):
                    arrowhead = 'none'
                    if isinstance(structure_item, RefCollection):
                        arrowhead = 'ediamond'

                    ref_edge = pydot.Edge(
                        self._gen_port_name(
                            item.item_type_id,
                            structure_element
                        ),
                        self._gen_port_name(structure_item.item_type_id),
                        arrowhead=arrowhead,
                        style='dashed'
                    )
                    graph.add_edge(ref_edge)
                    if item_type:
                        graph.add_node(
                            self.get_node(structure_item.item_type_id,
                                          plugin_id)
                        )

                elif isinstance(structure_item, Child):
                    child_edge = pydot.Edge(
                        self._gen_port_name(
                            item.item_type_id,
                            structure_element
                        ),
                        self._gen_port_name(structure_item.item_type_id),
                        arrowhead='tee',
                        style='solid'
                    )
                    graph.add_edge(child_edge)
                    if item_type:
                        graph.add_node(
                            self.get_node(structure_item.item_type_id,
                                          plugin_id)
                        )

                elif (isinstance(structure_item, Property) or
                        isinstance(structure_item, View)):
                    is_link = False

                else:
                    raise TypeError(
                        "Attribute {} of {} is unknown type {}".format(
                            (structure_element,
                            item.item_type_id,
                            structure_item.__class__.__name__)
                        )
                    )

                if is_link:
                    item_attributes.extend(
                        self._gen_label(structure_element, True)
                    )
                    # Add the type of relationship
                    item_attributes[-1] += ' (' + \
                        structure_item.__class__.__name__ + ')'
                else:
                    # Only include properties when generating a class
                    # diagram for an individual plugin or item type,
                    # else it gets too busy
                    if plugin_id or item_type:
                        item_attributes.extend([structure_element + \
                            ' (' + structure_item.prop_type_id + ')'])

            # Sort properties according to their name
            if len(item_attributes) > 1:
                item_attributes = [item_attributes[0]] + \
                    sorted(item_attributes[1:])

            nodes[item.item_type_id].set('label', ('{' + \
                ' | '.join(item_attributes) + '}'))

        #graph.write(file_name)
        return graph.to_string()

    def _gen_port_name(self, dst_name, port_name=None):
        if not port_name:
            port_name = dst_name

        if dst_name == 'node':
            return '"node":"node"'
        return '"' + dst_name + '":"' + port_name + '"'

    def _gen_label(self, label, has_port=False):
        if has_port:
            return ['<' + label + '> ' + label]
        else:
            return [label]

    @staticmethod
    def get_url(item_type_id, is_plugin=False):
        url_prefix = './'
        if is_plugin:
            url_prefix = '../../item_types/'
        item_type_str = item_type_id.lower().replace('-', '_')
        return url_prefix + item_type_str + ".html"

    def get_node(self, item_type_id, is_plugin):
        return pydot.Node(name='"' + item_type_id + '"',
                          URL=self.get_url(item_type_id, is_plugin))
