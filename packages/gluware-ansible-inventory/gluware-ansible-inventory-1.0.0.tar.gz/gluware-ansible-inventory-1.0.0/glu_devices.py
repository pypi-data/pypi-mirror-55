#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Gluware Inc.

# Gluware Ansible Inventory Plugin

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['released'],
                    'supported_by': 'Gluware Inc'}

DOCUMENTATION = '''
    name: glu_devices
    plugin_type: inventory
    short_description: Gluware Control Inventory Source
    description:
        - Get inventory from Device Manager in Gluware Control.
        - Uses a YAML configuration file that ends with C(glu_devices.yml) for the host of the Gluware Control system and the userName and password to that Gluware Control system.
        - If just the environment variables are used then specify '-i @glu_devices_env' to the ansible command line.
        - If there are any Gluware Control custom fields with values on the devices that start with 'ansible_var_' then those variables will be added to the host (minus the 'ansible_var_' part).
        - If there is a Gluware Control custom field of 'ansible_connection' on the device then that will be the connection for that host.  Otherwise 'network_cli' will be the connection.
        - If there is a Gluware Control custom field of 'ansible_network_os' on the device then that will be the 'ansible_network_os' for that hose.  Otherwise 'discoveredOs' (if available) will be the 'ansible_network_os' for that host.
    version_added: '2.8'
    author:
        - John Anderson
    options:
        plugin:
            description: This tells ansible (through the auto inventory plugin) this is a source file for the glu_devices plugin.
            env:
                - name: ANSIBLE_INVENTORY_ENABLED
            required: True
            choices: ['glu_devices']
        host:
            description: The network address or name of your Gluware Control system host.
            type: string
            env:
                - name: GLU_CONTROL_HOST
            required: True
        username:
            description: The user used to access devices (inventories) from the Gluware Control system.
            type: string
            env:
                - name: GLU_CONTROL_USERNAME
            required: True
        password:
            description: The password for the username of the Gluware Control system.
            type: string
            env:
                - name: GLU_CONTROL_PASSWORD
            required: True
        trust_any_host_https_certs:
            description: Specify whether Ansible should verify the SSL certificate of https calls on the Control Gluware system host.  This is used for self-signed Gluware Control Systems.
            type: bool
            default: False
            env:
                - name: GLU_CONTROL_TRUST_ANY_HOST_HTTPS_CERTS
            required: False
            aliases: [ verify_ssl ]
        variable_map:
            description: Dictionary where the keys are variable names of fields in Gluware Control devices (including custom fields).  The values of the dictionary are strings that specify the variable names on the host.
            type: complex
            required: false
'''

EXAMPLES = r'''
    #
    # Configuration for *glu_devices.yml files
    plugin: glu_devices
    host: 'https://10.0.0.1'
    username: <user name in Gluware Control system for device API calls>
    password: <password for user name>
    trust_any_host_https_certs: False
    variable_map:
        discoveredSerialNumber: serial_num

    #
    # For using the just the environment variables without a *glu_devices.yml file specify '-i @glu_devices_env'

'''

import re
import json
import pprint

from ansible.module_utils.urls import Request, urllib_error, ConnectionError, socket, httplib
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.inventory import BaseInventoryPlugin

# Python 2/3 Compatibility
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

# Mapping between the discoveredOs variable and ansible_network_os    
DiscoveredOSToAnsibleNetworkOS = {
    'NX-OS' : 'nxos',
    'IOS/IOS XE' : 'ios',
}  
  
class InventoryModule(BaseInventoryPlugin):
  NAME = 'glu_devices'

  env_config_only = False

  @staticmethod  
  def _convertGroupName(groupName):
      '''
        Convert group names to valid characters that can be a directory on a file system.
      '''
      groupName = re.sub('[^a-zA-Z0-9]', '_', groupName)
      return groupName

  def _api_call(self, requestHandler, api_url, api_url_2):
    '''
        Make the api call for the api_url with the requestHandler and on success return object with data.
        If api_url fails then try api_url_2.
    '''
    # Make the actual api call.
    try:
        response = requestHandler.get(api_url)
    except (ConnectionError, httplib.HTTPException, socket.error) as e:
        errorMsg = 'Gluware Control call failed: {msg}'.format(msg=e)
        raise AnsibleError(to_native(errorMsg))
    except urllib_error.URLError:
        # If the first call returns a URL error then try this second call.
        try:
            response = requestHandler.get(api_url_2)
        except (ConnectionError, httplib.HTTPException, socket.error, urllib_error.URLError) as e2:
            errorMsg = 'Gluware Control call2 failed: {msg}'.format(msg=e2)
            raise AnsibleError(to_native(errorMsg))

    
    # Read in the JSON response to a object.
    try: 
        readResponse = response.read()
        objResponse = json.loads(readResponse)
        return objResponse
    except (valueError, TypeError) as e:
        errorMsg = 'Gluware Control call response failed to be parsed as JSON: {msg}'.format(msg=e)
        raise AnsibleError(to_native(errorMsg))

  def _updateInventoryObj(self, gluDevices):
    '''
        Take the gluDevices object and update the self.inventory object
    '''
    # pprint.pprint(gluDevices)

    # Default ansible_connection to 'network_cli'.  This if for paramiko (used in Ansible Networking) instead of the default 'ssh' (used in normal Ansible)
    self.inventory.set_variable('all', 'ansible_connection', 'network_cli')

    for deviceObj in gluDevices:
        deviceName = deviceObj.get('name')
        groupsStr = deviceObj.get('Groups')

        # Try to used the discoveredOs from the device. 
        #   If that is not found the try to use the ansible_network_os on the device.
        networkOS = ''
        discoveredOS = deviceObj.get('discoveredOs')
        # print "DiscoveredOS: ", discoveredOS
        if discoveredOS: networkOS = DiscoveredOSToAnsibleNetworkOS.get(discoveredOS)
        if not networkOS:
            networkOS = deviceObj.get('ansible_network_os')
        if not networkOS:
            # Since there was no mapping or overriding ansible_network_os property use the discoveredOS directly.
            # The idea behind this logic is maybe the discoveredOS will adopt the ansible convention of network os id.
            networkOS = discoveredOS

        # print "networkOS: ", networkOS
    
        # In case the ansible connection is overridden.
        ansibleConnection = deviceObj.get('ansible_connection')
        if deviceName:
            connectionInfoObj = deviceObj.get('connectionInformation')
            if connectionInfoObj:
                connectIp = connectionInfoObj.get('ip')
                connectPort = connectionInfoObj.get('port')
                connectUsername = connectionInfoObj.get('userName')
                connectPassword = connectionInfoObj.get('password')
                connectEnablePassword = connectionInfoObj.get('enablePassword')

                # Special logic if password and enable password is not available.
                if not connectPassword: connectPassword = deviceObj.get('x_word')
                if not connectEnablePassword: connectEnablePassword = deviceObj.get('x_e_word')

                # TODO: add logic for proxy objects. Paramiko might support proxy logic.

                # Check that that the device is not already added by some other inventory plugin.
                if not self.inventory.get_host(deviceName):
                    # If there is a networkOS then use that as a group and assign that host to the group.
                    group = None
                    if networkOS:
                        group = self._convertGroupName(networkOS)
                        self.inventory.add_group(group)
                    host = self.inventory.add_host(deviceName, group, connectPort)

                    # Set the ansible_network_os no matter what.  This is so it is not undefined in the playbook.
                    self.inventory.set_variable(host,'ansible_network_os', networkOS)
                    
                    if connectIp: self.inventory.set_variable(host, 'ansible_host', connectIp)
                    if connectUsername: self.inventory.set_variable(host,'ansible_user', connectUsername)
                    if connectPassword: self.inventory.set_variable(host,'ansible_password', connectPassword)
                    if ansibleConnection: self.inventory.set_variable(host,'ansible_connection', ansibleConnection)

                    # For any deviceObj properties that start with 'ansible_var_' add that variable (minus the 'ansible_var_' part) to the host.
                    for propName, propVal in deviceObj.items():
                        if propName.startswith('ansible_var_'):
                            ansibleVar = propName[len('ansible_var_'):]
                            if ansibleVar: self.inventory.set_variable(host, ansibleVar, propVal)

                    # If there is a variable_map then look for the variable in the deviceObj and assign it to the ansibleVarName to the host.
                    variableMap = self.get_option('variable_map')
                    if variableMap:
                        for gluPropName, ansibleVarName in variableMap.items():
                            devicePropVal = deviceObj.get(gluPropName)
                            if devicePropVal: self.inventory.set_variable(host, ansibleVarName, devicePropVal)
                            
    # Finalize inventory
    self.inventory.reconcile_inventory()


  def verify_file(self, path):
    '''
        Called by ansible first to verify if the path is valid for this inventory plugin.
    '''
    if (path == '@glu_devices_env'):
        self.env_config_only = True
        return True
    if super(InventoryModule, self).verify_file(path):
        # base class verifies that file exists and is readable by current user
        if path.endswith('glu_devices.yml'):
            return True
    return False


  def parse(self, inventory, loader, path, cache=True):
    '''
        Called by ansible second to fill in the passed inventory object for the specified path.
        The self.verify_file() was called first so state could have been set on the self object there
        that can be used here.
    '''

    # Use the super classes functionality to setup the self object correcly.
    super(InventoryModule, self).parse(inventory, loader, path)
    if not self.env_config_only:
        self._read_config_data(path)

    # Setup for the API call for the data for the inventory.    
    apiHost = self.get_option('host')
    if not re.match('(?:http|https)://', apiHost):
        apiHost = 'https://{host}'.format(host=apiHost)

    # This api call is for Gluware Control 3.6 and greater.
    apiURL_1 = urljoin(apiHost, '/api/devices?showPassword=true')
    # This api call is for Gluware Control 3.5.
    apiURL_2 = urljoin(apiHost, '/api/devices')
    
    apiUser = self.get_option('username')
    apiPassword = self.get_option('password')
    apiTrustHttps = self.get_option('trust_any_host_https_certs')

    requestHandler = Request(url_username=apiUser, 
                            url_password=apiPassword, 
                            validate_certs=not(apiTrustHttps), 
                            force_basic_auth=True)

    # Make the API Call for the data for the inventory.
    gluDevices = self._api_call(requestHandler, apiURL_1, apiURL_2)

    # Process the API data into the inventory object.
    self._updateInventoryObj(gluDevices)

