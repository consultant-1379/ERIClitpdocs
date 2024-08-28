#!/usr/bin/python:

import argparse
import os
import subprocess
import socket

from ConfigParser import ConfigParser
from sphinx.restructuredtext import SphinxGenerator


def get_dependencies(rpm_dir, ext_files, plugin_files):
    rpms_info = get_rpms_info(rpm_dir)
    dependencies = {}
    rpm_mappings = get_rpm_mappings(rpms_info, ext_files, plugin_files)
    for rpm_name, rpm_info in rpms_info.items():
        if rpm_name in rpm_mappings.keys():
            name = rpm_mappings[rpm_name]
            dependencies[name] = []
            for required_rpm in rpm_info['requires']:
                if required_rpm in rpm_mappings.keys():
                    required_name = rpm_mappings[required_rpm]
                    dependencies[name].append(required_name)
            print_require_warnings(name, dependencies[name])
    return dependencies


def print_require_warnings(name, requires):
    if not name[0].startswith('core_'):
        if len(requires) == 0:
            print "Warning: %s has 0 dependencies." % (str(name))
        if ('core_extension', 'extension') not in requires:
            print ("Warning: " + str(name) + " has no dependencies "
                   "on ERIClitpcore_CXP9030418.")
        plugin_deps = [r for r in requires if r[1] == 'plugin']
        if name[1] == 'plugin' and len(plugin_deps) > 0:
            print "Warning: plugin to plugin dependencies: " + \
                  (str(name)) + " -> " + str(plugin_deps)


def get_reversed_deps(deps):
    reversed_deps = {}
    for key in deps.keys():
        reversed_deps[key] = []
    for name, requires in deps.items():
        for require in requires:
            reversed_deps[require].append(name)
    print_required_by_warnings(reversed_deps)
    return reversed_deps


def print_required_by_warnings(rev_deps):
    for name, require_by in rev_deps.items():
        if name[1] == "extension" and len(require_by) == 0:
            print ("Warning: extension " + str(name) + " is not required by "
                   "any plugins.")


def get_rpm_mappings(rpms_info, ext_files, plugin_files):
    rpm_mappings = {}
    for rpm_name, rpm_info in rpms_info.items():
        for plugin_file, plugin_name in plugin_files:
            if plugin_file in rpm_info['conf_files']:
                rpm_mappings[rpm_name] = (plugin_name, 'plugin')
        for ext_file, ext_name in ext_files:
            if ext_file in rpm_info['conf_files']:
                rpm_mappings[rpm_name] = (ext_name, 'extension')
    return rpm_mappings


def get_rpms_info(rpm_dir):
    rpms_info = {}
    for filename in os.listdir(rpm_dir):
        if filename.endswith(".rpm"):
            rpm_name = filename[:filename.find('-')]
            rpms_info[rpm_name] = {
                'requires': get_rpm_requires(rpm_dir + filename),
                'conf_files': get_rpm_files(rpm_dir + filename)
            }
    return rpms_info


def get_rpm_requires(rpm_path):
    cmd = '/bin/rpm --requires -qp %s' % (rpm_path)
    requires = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    eric_requires = []
    for req in requires:
        if req.startswith('ERIC'):
            if ' ' in req:
                req = req[:req.find(' ')]
            eric_requires.append(req.strip())
    return eric_requires


def get_rpm_files(rpm_path):
    cmd = '/bin/rpm -qpl %s' % (rpm_path)
    files = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    litp_files = [f[(f.rfind('/') + 1):].strip() for f in files \
                  if f.strip().endswith('.conf')]
    return litp_files


def generate_sphinx_doc(docroot, pluginconf):
    generator = SphinxGenerator(docroot)

    extensions = []
    extension_files = []
    for filename in os.listdir(pluginconf + "/extensions"):
        if filename.endswith(".conf") and \
            not (filename.startswith("mock_") \
               or filename.startswith("example")):
            print "Extension file:" + filename
            config = ConfigParser()
            config.read(pluginconf + "/extensions/" + filename)
            extension_name = config.get("extension", "name")
            extension_version = config.get("extension", "version")
            classname = config.get("extension", "class")
            extension_class = _create(classname)
            extensions.append(
                    (extension_name, extension_version, extension_class)
                    )
            extension_files.append((filename, extension_name))

    generator.create_item_type_hierarchy(extensions)

    plugins = []
    plugin_files = []
    for filename in os.listdir(pluginconf + "/plugins"):
        if filename.endswith(".conf") and not (filename.startswith("mock_") \
                or filename.startswith("example")):
            print "Plugin file:" + filename
            config = ConfigParser()
            config.read(pluginconf + "/plugins/" + filename)
            plugin_name = config.get("plugin", "name")
            plugin_version = config.get("plugin", "version")
            classname = config.get("plugin", "class")
            plugin_class = _create(classname)
            plugins.append(
                    (plugin_name, plugin_version, plugin_class)
                    )
            plugin_files.append((filename, plugin_name))

    rpm_dir = docroot + "/../target/deps/litp/"
    deps = get_dependencies(rpm_dir, extension_files, plugin_files)
    generator.requires = deps
    reversed_deps = get_reversed_deps(deps)
    generator.required_by = reversed_deps

    for extension_tup in extensions:
        print "Generating Sphinx docs for extension: %s" % (extension_tup[0])
        generator.generate_ext(*extension_tup)
        print "Generated Sphinx docs for extension: %s" % (extension_tup[0])

    for plugin_tup in plugins:
        print "Generating Sphinx docs for plugin: %s" % (plugin_tup[0])
        generator.generate_plugin(*plugin_tup)
        print "Generated Sphinx docs for plugin: %s" % (plugin_tup[0])

    core_validators = "litp.core.validators"
    validators_module = _create(core_validators)
    generator.generate_validators_doc(validators_module)

    core_operations = "litp.migration.operations"
    operations_module = _create(core_operations)
    generator.generate_operations_doc(operations_module)
    generator.generate_index_doc()
    print "Generated Sphinx index docs"


def _create(classname):
    strList = classname.split('.')
    classname1 = strList[-1]
    moduleList = strList[:-1]
    modules = ".".join(moduleList)
    _actual_gethostname = socket.gethostname
    if modules:
        try:
            socket.gethostname = lambda: "ms1"
            module = __import__(modules)
        finally:
            _actual_gethostname = socket.gethostname
        components = modules.split('.')
        for comp in components[1:]:
            module = getattr(module, comp)
        classitem = getattr(module, classname1)
        if hasattr(classitem, '__call__'):
            return classitem()
        return classitem
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docroot", "-d",
                        help="Root of docs to write files to.")
    parser.add_argument("--pluginconf", "-p",
                        help="Folder where plugin .conf files are kept.",
                        default="/opt/ericsson/nms/litp/etc")
    args = parser.parse_args()

    generate_sphinx_doc(args.docroot, args.pluginconf)
