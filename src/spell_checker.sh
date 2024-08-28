#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

ERROR_EXCLUSIONS = [
    " '' ",
    " '4' ",
    " 'HA ",
    " 'c1' ",
    " 'cluster' ",
    " 'ha ",
    " 'haManager1' ",
    " 'id' ",
    " 'properties' ",
    " 'type' ",
    " 'vcs' ",
    " 3PP ",
    " API ",
    " APIs ",
    " ATs ",
    " AddCollection ",
    " AddProperty ",
    " AddRefCollection ",
    " BaseMigration ",
    " BaseOperation ",
    " CDS ",
    " CLI ",
    " CRA ",
    " CSA ",
    " CXP ",
    " CallbackApi ",
    " CallbackTask ",
    " CardinalityError ",
    " ChildNotAllowedError ",
    " Ciaran ",
    " Config ",
    " ConfigTask ",
    " ConfigTasks ",
    " DeprecationWarning ",
    " DirectoryExistValidator ",
    " ENM ",
    " ERIClitpcore ",
    " ERIClitpexample ",
    " ERIClitpnewmodelextension ",
    " ERIClitpnewplugin ",
    " Ericsson ",
    " EriDoc ",
    " FILLME ",
    " FOSS ",
    " ForRemoval ",
    " FuturePropertyValue ",
    " Gemfile ",
    " Gerrit ",
    " HeaderNotAcceptableError ",
    " IPAddressValidator ",
    " IPV4 ",
    " IPv4 ",
    " IPv6 ",
    " IPv6AddressAndMaskValidator ",
    " IntRangeValidator ",
    " IntValidator ",
    " InternalServerError ",
    " InvalidChildTypeError ",
    " InvalidLocationError ",
    " InvalidReferenceError ",
    " InvalidRequestError ",
    " InvalidTypeError ",
    " IsNotDigitValidator ",
    " ItemExistsError ",
    " ItemType ",
    " ItemTypes ",
    " ItemValidator ",
    " ItemValidators ",
    " JSON ",
    " JIRA ",
    " LITP ",
    " LITP2 ",
    " LMI ",
    " LitpScript ",
    " MCO ",
    " MCollective ",
    " MethodNotAllowedError ",
    " MissingRequiredItemError ",
    " MissingRequiredPropertyError ",
    " ModelExtension ",
    " ModelItem ",
    " ModelItems ",
    " ModelManager ",
    " NetworkValidator ",
    " NetworkValidatorV6 ",
    " NotEmptyStringValidator ",
    " OrderedPhase ",
    " OrderedTaskList ",
    " PXE ",
    " PluginApiContext ",
    " PropertyLengthValidator ",
    " PropertyNotAllowedError ",
    " PropertyType ",
    " PropertyTypes ",
    " PropertyValidator ",
    " PropertyValidators ",
    " QueryItem ",
    " QueryItems ",
    " README ",
    " RHEL ",
    " RPMs ",
    " RefCollection ",
    " Regex ",
    " RegexValidator ",
    " RemoteExecutionTask ",
    " RemoteExecutionTasks ",
    " RemoveProperty ",
    " RenameItemType ",
    " RenameProperty ",
    " RestrictedPropertiesValidator ",
    " SDK ",
    " SVG ",
    " ServerUnavailableError ",
    " Sinéad ",
    " Subclasses ",
    " UML ",
    " URI ",
    " UnallocatedPropertyError ",
    " Unauthorised ",
    " Unencrypted ",
    " Unprocessable ",
    " UpdateCollectionType ",
    " UserProfile ",
    " VCS ",
    " VM ",
    " ValidationError ",
    " Validator ",
    " Validators ",
    " Versioning ",
    " ViewError ",
    " VirtualBox ",
    " Workflow ",
    " XID ",
    " XSD ",
    " XSDs ",
    " ZeroAddressValidator ",
    " Z0 ",
    " api ",
    " assertErrorMessage ",
    " assertProperty ",
    " ats ",
    " behaviour ",
    " bmc ",
    " bom ",
    " bool ",
    " boolean ",
    " bootmgr ",
    " br ",
    " bundler ",
    " cba ",
    " cmd ",
    " conf ",
    " config ",
    " configmanager ",
    " configmanagerapi ",
    " createLITPProject ",
    " createrepo ",
    " crypto ",
    " dep ",
    " deployment1 ",
    " desc ",
    " devel ",
    " dhcpservice ",
    " distro ",
    " dnsclient ",
    " doesn ",
    " epsjse ",
    " epsjseapi ",
    " filenames ",
    " filesystems ",
    " groupapi ",
    " groupplugin ",
    " hostname ",
    " http ",
    " hyperics ",
    " hyperlinked ",
    " init ",
    " ip ",
    " ipmi ",
    " ipv4 ",
    " ipv6 ",
    " isn ",
    " iterable ",
    " json ",
    " kwargs ",
    " libvirt ",
    " libxml2 ",
    " libxslt ",
    " linuxfirewall ",
    " litp ",
    " litpd ",
    " logrotate ",
    " lv ",
    " manager' ",
    " mcollective ",
    " modeldeployment ",
    " mvn ",
    " n1 ",
    " nas ",
    " node1 ",
    " ntp ",
    " os ",
    " passw0rd ",
    " postgresql ",
    " pre ",
    " prepend ",
    " prop1 ",
    " py ",
    " regex ",
    " repo ",
    " reponame ",
    " rubygems ",
    " runats ",
    " san ",
    " sanitisation ",
    " snapshotting ",
    " src ",
    " str ",
    " subclasses ",
    " sysparams ",
    " task1 ",
    " task2 ",
    " task3 ",
    " templating ",
    " tuple ",
    " txt ",
    " updatable ",
    " uri ",
    " userapi ",
    " username ",
    " userplugin ",
    " v1 ",
    " validator ",
    " validators ",
    " value1 ",
    " vcs ",
    " versantmanagement ",
    " versioning ",
    " virtualisation ",
    " volmgr ",
    " vpath ",
    " workflow ",
    " xsd ",
    " zA ",
    " zookeeperapi ",
    " DHCPv4 ",
    " DHCPv6 ",
    " DNS ",
    " LVM ",
    " NAS ",
    " NTP ",
    " RPC ",
    " VxVM ",
    " ddl ",
    " eg ",
    " filename ",
    " ie ",
    " lifecycle ",
    " mco ",
    " mysql ",
    " opendj ",
    " rb ",
    " td ",
    " CXP1234567 ",
    " CredentialsNotFoundError ",
    " DoNothingPlanError ",
    " ERIClitpbar ",
    " ERIClitpfooapi ",
    " EXTRlitppuppetfirewall ",
    " FILESYSTEM ",
    " InvalidXMLError ",
    " LMS ",
    " LUN ",
    " LUNs ",
    " MaxValueValidator ",
    " OnePropertyValidator ",
    " PRE ",
    " SANITISATION ",
    " SnapshotModelApi ",
    " Unsetting ",
    " VXVM ",
    " capitalised ",
    " checksum ",
    " classname ",
    " dps ",
    " elasticsearch ",
    " extensibility ",
    " filepath ",
    " keyring ",
    " login ",
    " ruleset ",
    " timestamp ",
    " queryable ",
]

FILE_EXCLUSIONS = [
#    "_type",
    "_plugin",
    "_extension",
    "modules",
    "genindex",
]

LANG_DICTIONARY = "en_US"

def spellcheck_site(site_path):
    site_files = get_site_files(site_path)
    print '### Found Spelling Errors: ####'
    for site_file in site_files:
        if not is_exclusion(site_file, FILE_EXCLUSIONS):
            spellcheck_file(site_file)


def get_site_files(site_path):
    cmd = '/usr/bin/find %s -name \*.html -type f | grep -v type' % (site_path)
    files = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    return files


def spellcheck_file(site_file):
    cmd = 'hunspell -d %s -u %s' % (LANG_DICTIONARY, site_file)
    errors = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    for error in errors:
        if not is_exclusion(error, ERROR_EXCLUSIONS):
            print "%s : %s" % (site_file.strip(), error.strip())


def is_exclusion(error, exclusions):
    for exclusion in exclusions:
        if exclusion in error:
            return True
    return False


def add_misspelled_words(site_file, misspelled_words):
    cmd = 'hunspell -d %s -l %s' % (LANG_DICTIONARY, site_file)
    words = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    for word in words:
        misspelled_words.add(" " + word.strip() + " ")


def print_misspelled_words(site_path):
    site_files = get_site_files(site_path)
    misspelled_words = set()
    print '### Found Mis-spelling: ####'
    for site_file in site_files:
        if not is_exclusion(site_file, FILE_EXCLUSIONS):
            add_misspelled_words(site_file, misspelled_words)
    for word in sorted(misspelled_words):
        if not is_exclusion(word, ERROR_EXCLUSIONS):
            print '    "%s",' % (word)
    

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        site_path = sys.argv[1]
    else:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        site_path = current_dir + '/../target/site'
        print "Using site_path: " + site_path
    spellcheck_site(site_path)
    print_misspelled_words(site_path)
