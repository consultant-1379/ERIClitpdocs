# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

from litp.core.plugin import Plugin
from litp.core.execution_manager import ConfigTask, CallbackTask
from litp.core.rpc_commands import RpcExecutionException
from litp.core.litp_logging import LitpLogger

#Initialise the Litplogger
log = LitpLogger()


class ExamplePlugin(Plugin):
    """
    The example plugin shows the following functionality:
      - ConfigTask: Calls a method defined in puppet to copy the example-conf
        item type to /tmp on the ms and the node(s).
       - Callback task: Calls an mcollective agent to run mcollective command
         on the node(s), for this example its "df -k /tmp"

    Please check the puppet directory to see the puppet and mcollective
    functionality.
    """

    def create_configuration(self, plugin_api_context):
        """
        To implement this plugin, add the following to the model:

        **Example CLI for this plugin**

        .. code-block:: bash

            litp create -t example-conf -p /software/items/test -o
            name=test
            litp inherit -p /deployments/d1/clusters/c1/nodes/n1/items/test \
            -s /software/items/test
            litp inherit -p /deployments/d1/clusters/c1/nodes/n2/items/test \
            -s /software/items/test

        """
        #Goes through the model looking all item types of type node
        #Returns a list of the node item_types
        all_nodes = plugin_api_context.query("node")

        tasks = []
        for node in all_nodes:
            #Goes through the model looking all item types of type example-conf
            #on a per node basis
            #Returns a list of the example-conf item_types
            for package in node.query('example-conf'):
                #All item types have a state, here we are checking
                #for Initial or update state.
                if package.is_initial() or package.is_updated():
                    log.trace.info('Creating config task to install file '
                    '"{0}".conf on node "{1}"'.format(package.name,
                    node.hostname))
                    #Create a Config task and append it to the task list.
                    #Config task will call a puppet resource.
                    # node: The node the Config task will run on
                    # package: Item type affected by the task
                    # test_example::test_example: name of the puppet resouce
                    # type used by this Config Task
                    # call_id: Unique identifier for this Config Task
                    # filename: Arg for the puppet resource
                    # ensure: Arg for the puppet resource
                    tasks.append(ConfigTask(
                            node,
                            package,
                            'Install %s on node %s' \
                             % (package.name, node.hostname),
                            "test_example::test_example",
                            call_id=str(package.item_id),
                            filename=str(package.name),
                            file_ensure="present"
                    ))
                #All item types have a state, here we are checking
                #for removal state.
                if package.is_for_removal():
                    log.trace.info('Creating config task to remove file '
                    '"{0}".conf on node "{1}"'.format(package.name,
                    node.hostname))
                    tasks.append(ConfigTask(
                            node,
                            package,
                            'Remove %s on node %s' \
                             % (package.name, node.hostname),
                            "test_example::test_example",
                            call_id=str(package.item_id),
                            filename=str(package.name),
                            file_ensure="absent"
                    ))

        #Take the first cluster from the query for clusters in the model
        cluster = plugin_api_context.query('cluster')[0]
        nodes = plugin_api_context.query("node")
        for n in nodes:
            for package in n.query('example-conf'):
                if package.is_initial() or package.is_updated():
                    log.trace.info('Creating Callback task to run mcollective '
                               'agent "example" and command "check_dir_space" '
                                'on node '
                               '"{0}"'.format(n.hostname))
                    # Create a Callback task and append it to the task list.
                    # Callback task will call a mco agent.
                    # cluster: Litp item affected by this callback task
                    # self._check_dir_space: The method that the callback
                    # task will execute. The method is defined below.
                    # [n.hostname]: args for the call back task. Ie args
                    # pass to the check_dir_space method
                    tasks.append(CallbackTask(
                            cluster,
                            'Mcollective check_file_exist command to run '
                            'on %s' % n.hostname,
                           self._check_file_exist,
                           [n.hostname],
                           filename=package.name
                        ))
        return tasks

    #callback_api is passed thru via the callback_task
    def _check_file_exist(self, callback_api, node, filename):
        """
        Calls the rpc_command via the callback api.
        Raises an exception if rpc_command fails
        """
        #All rpc methods MUST be called via a callback_api
        #This command calls the mco agent "example", executes the method
        #"check_dir_space" with the arguments in an dictionary "{'path':
        # '/tmp'}" on the node passed to the method.
        try:
            result = callback_api.rpc_command(node, 'example',
                                         'check_file_exist',
                                         {'path': '/tmp/' + filename})
        except RpcExecutionException as e:
            log.trace.error(
                '_check_dir_space rpc Exception: ' + e)
        self._process_results(result, filename)

    def _process_results(self, results, filename):
        log.trace.debug("processing results: {0}".format(results))
        for node, response in results.iteritems():
            data = response["data"]
            if 'retcode' in data:
                if data['retcode'] == 0:
                    if len(data['out']):
                        log.trace.debug('File "{0}" is present on node: "{0}"'
                                        .format(filename, node))
                        return True
                    else:
                        log.trace.debug('File "{0}" is not present on node: '
                                        '"{0}"'.format(filename, node))
                    return False
            else:
                log.event.error("No retcode information for  {0}".format(node))
            return False
