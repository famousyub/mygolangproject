import os
import urllib2
import base64
import socket
import logging
import ConfigParser
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template, session, redirect, url_for, escape
#createStandardAccountJAMFAPI
# API functions:
# https://myjss.com:8443/api/

# Parse Config File
config = ConfigParser.RawConfigParser()
# If file exists
if os.path.exists('mdmtools.cfg'):
    # Logging config
    config.read('mdmtools.cfg')
    secretkey = config.get('server', 'sercretkey')
    grouppass = config.get('server', 'grouppass')
    username = config.get('jss', 'username')
    password = config.get('jss', 'password')
    server = config.get('jss', 'server')
else:
    # Creating new configuration file
    config.add_section("server")
    config.set('server',"sercretkey")
    config.set('server',"grouppass")
    config.add_section('jss')
    config.set('jss',"username")
    config.set('jss',"password")
    config.set('jss',"server")
    with open('mdmtools.cfg', 'wb') as configfile:
        config.write(configfile)
    print ("Config File Created. Please edit mdmtools.cfg and run again.")
    exit(0)
# https://bryson3gps.wordpress.com/2014/03/30/the-jss-rest-api-for-everyone/
# Function to communicate with jamf
def jamfcall(resource, username, password, method = '', data = None):
    # create a new request object with resource URL
    request = urllib2.Request(resource)
    # Add auth header
    request.add_header('Authorization', 'Basic ' + base64.b64encode(username + ':' + password))
    # add get_method if request is a post, put, or delete
    if method.upper() in ('POST', 'PUT', 'DELETE'):
        request.get_method = lambda: method
    # add content type if request is post, put and there is data
    if method.upper() in ('POST', 'PUT') and data:
        # Add in content type header
        request.add_header('Content-Type', 'text/xml')
        # send request with data and return results
        response = urllib2.urlopen(request, data)
        # Convert response to text
        computerxml = response.read()
        print (response.code)
        # Create new Element Tree with computer xml
        root = ET.fromstring(computerxml)
        return root
    else:
        # send request and return results
        response = urllib2.urlopen(request)
        # Convert response to text
        computerxml = response.read()
        print (response.code)
        # Create new Element Tree with computer xml
        root = ET.fromstring(computerxml)
        return root
        

userName = "testuser"
fullName = "Test User"
emailAddress = "testuser@email.com"
defaultPassword = "abc1234"

account = ET.Element('account')
accountID = ET.SubElement(account, 'id')
accountID.text = "0"
accountName = ET.SubElement(account, 'name')
accountName.text = userName
accountDirUser = ET.SubElement(account, 'directory_user')
accountDirUser.text = "false"
accountFullName = ET.SubElement(account, 'full_name')
accountFullName.text = fullName
accountEmail = ET.SubElement(account, 'email')
accountEmail.text = emailAddress
accountEmailAddress = ET.SubElement(account, 'email_address')
accountEmailAddress.text = emailAddress
accountPass = ET.SubElement(account, 'password')
accountPass.text = defaultPassword
accountEnabled = ET.SubElement(account, 'enabled')
accountEnabled.text = "Enabled"
forcePassChange = ET.SubElement(account, 'force_password_change')
forcePassChange.text = "true"
accessLevel = ET.SubElement(account, 'access_level')
accessLevel.text = "Full Access"
privilegeSet = ET.SubElement(account, 'privilege_set')
privilegeSet.text = "Administrator"
privileges = ET.XML('''<privileges>
    <jss_objects>
      <privilege>Create Advanced Computer Searches</privilege>
      <privilege>Read Advanced Computer Searches</privilege>
      <privilege>Update Advanced Computer Searches</privilege>
      <privilege>Delete Advanced Computer Searches</privilege>
      <privilege>Create Advanced Mobile Device Searches</privilege>
      <privilege>Read Advanced Mobile Device Searches</privilege>
      <privilege>Update Advanced Mobile Device Searches</privilege>
      <privilege>Delete Advanced Mobile Device Searches</privilege>
      <privilege>Create Advanced User Searches</privilege>
      <privilege>Read Advanced User Searches</privilege>
      <privilege>Update Advanced User Searches</privilege>
      <privilege>Delete Advanced User Searches</privilege>
      <privilege>Create Advanced User Content Searches</privilege>
      <privilege>Read Advanced User Content Searches</privilege>
      <privilege>Update Advanced User Content Searches</privilege>
      <privilege>Delete Advanced User Content Searches</privilege>
      <privilege>Create AirPlay Permissions</privilege>
      <privilege>Read AirPlay Permissions</privilege>
      <privilege>Update AirPlay Permissions</privilege>
      <privilege>Delete AirPlay Permissions</privilege>
      <privilege>Create Allowed File Extension</privilege>
      <privilege>Read Allowed File Extension</privilege>
      <privilege>Delete Allowed File Extension</privilege>
      <privilege>Create Attachment Assignments</privilege>
      <privilege>Read Attachment Assignments</privilege>
      <privilege>Update Attachment Assignments</privilege>
      <privilege>Delete Attachment Assignments</privilege>
      <privilege>Create Buildings</privilege>
      <privilege>Read Buildings</privilege>
      <privilege>Update Buildings</privilege>
      <privilege>Delete Buildings</privilege>
      <privilege>Create Categories</privilege>
      <privilege>Read Categories</privilege>
      <privilege>Update Categories</privilege>
      <privilege>Delete Categories</privilege>
      <privilege>Create Classes</privilege>
      <privilege>Read Classes</privilege>
      <privilege>Update Classes</privilege>
      <privilege>Delete Classes</privilege>
      <privilege>Create Computer Enrollment Invitations</privilege>
      <privilege>Read Computer Enrollment Invitations</privilege>
      <privilege>Update Computer Enrollment Invitations</privilege>
      <privilege>Delete Computer Enrollment Invitations</privilege>
      <privilege>Create Computer PreStage Enrollments</privilege>
      <privilege>Read Computer PreStage Enrollments</privilege>
      <privilege>Update Computer PreStage Enrollments</privilege>
      <privilege>Delete Computer PreStage Enrollments</privilege>
      <privilege>Create Computers</privilege>
      <privilege>Read Computers</privilege>
      <privilege>Update Computers</privilege>
      <privilege>Delete Computers</privilege>
      <privilege>Create Configurations</privilege>
      <privilege>Read Configurations</privilege>
      <privilege>Update Configurations</privilege>
      <privilege>Delete Configurations</privilege>
      <privilege>Create Departments</privilege>
      <privilege>Read Departments</privilege>
      <privilege>Update Departments</privilege>
      <privilege>Delete Departments</privilege>
      <privilege>Create Device Enrollment Program Instances</privilege>
      <privilege>Read Device Enrollment Program Instances</privilege>
      <privilege>Update Device Enrollment Program Instances</privilege>
      <privilege>Delete Device Enrollment Program Instances</privilege>
      <privilege>Create Device Name Patterns</privilege>
      <privilege>Read Device Name Patterns</privilege>
      <privilege>Update Device Name Patterns</privilege>
      <privilege>Delete Device Name Patterns</privilege>
      <privilege>Create Directory Bindings</privilege>
      <privilege>Read Directory Bindings</privilege>
      <privilege>Update Directory Bindings</privilege>
      <privilege>Delete Directory Bindings</privilege>
      <privilege>Create Disk Encryption Configurations</privilege>
      <privilege>Read Disk Encryption Configurations</privilege>
      <privilege>Update Disk Encryption Configurations</privilege>
      <privilege>Delete Disk Encryption Configurations</privilege>
      <privilege>Create Disk Encryption Institutional Configurations</privilege>
      <privilege>Read Disk Encryption Institutional Configurations</privilege>
      <privilege>Update Disk Encryption Institutional Configurations</privilege>
      <privilege>Delete Disk Encryption Institutional Configurations</privilege>
      <privilege>Create Dock Items</privilege>
      <privilege>Read Dock Items</privilege>
      <privilege>Update Dock Items</privilege>
      <privilege>Delete Dock Items</privilege>
      <privilege>Create eBooks</privilege>
      <privilege>Read eBooks</privilege>
      <privilege>Update eBooks</privilege>
      <privilege>Delete eBooks</privilege>
      <privilege>Create Enrollment Profiles</privilege>
      <privilege>Read Enrollment Profiles</privilege>
      <privilege>Update Enrollment Profiles</privilege>
      <privilege>Delete Enrollment Profiles</privilege>
      <privilege>Create Computer Extension Attributes</privilege>
      <privilege>Read Computer Extension Attributes</privilege>
      <privilege>Update Computer Extension Attributes</privilege>
      <privilege>Delete Computer Extension Attributes</privilege>
      <privilege>Create Patch External Source</privilege>
      <privilege>Read Patch External Source</privilege>
      <privilege>Update Patch External Source</privilege>
      <privilege>Delete Patch External Source</privilege>
      <privilege>Create File Attachments</privilege>
      <privilege>Read File Attachments</privilege>
      <privilege>Update File Attachments</privilege>
      <privilege>Delete File Attachments</privilege>
      <privilege>Create Distribution Points</privilege>
      <privilege>Read Distribution Points</privilege>
      <privilege>Update Distribution Points</privilege>
      <privilege>Delete Distribution Points</privilege>
      <privilege>Create Push Certificates</privilege>
      <privilege>Read Push Certificates</privilege>
      <privilege>Update Push Certificates</privilege>
      <privilege>Delete Push Certificates</privilege>
      <privilege>Create iBeacon</privilege>
      <privilege>Read iBeacon</privilege>
      <privilege>Update iBeacon</privilege>
      <privilege>Delete iBeacon</privilege>
      <privilege>Create Infrastructure Managers</privilege>
      <privilege>Read Infrastructure Managers</privilege>
      <privilege>Update Infrastructure Managers</privilege>
      <privilege>Delete Infrastructure Managers</privilege>
      <privilege>Create Accounts</privilege>
      <privilege>Read Accounts</privilege>
      <privilege>Update Accounts</privilege>
      <privilege>Delete Accounts</privilege>
      <privilege>Create JDS</privilege>
      <privilege>Read JDS</privilege>
      <privilege>Update JDS</privilege>
      <privilege>Delete JDS</privilege>
      <privilege>Create JSON Web Token Configuration</privilege>
      <privilege>Read JSON Web Token Configuration</privilege>
      <privilege>Update JSON Web Token Configuration</privilege>
      <privilege>Delete JSON Web Token Configuration</privilege>
      <privilege>Create Keystore</privilege>
      <privilege>Read Keystores</privilege>
      <privilege>Update Keystores</privilege>
      <privilege>Delete Keystores</privilege>
      <privilege>Create LDAP Servers</privilege>
      <privilege>Read LDAP Servers</privilege>
      <privilege>Update LDAP Servers</privilege>
      <privilege>Delete LDAP Servers</privilege>
      <privilege>Create Licensed Software</privilege>
      <privilege>Read Licensed Software</privilege>
      <privilege>Update Licensed Software</privilege>
      <privilege>Delete Licensed Software</privilege>
      <privilege>Create Mac Applications</privilege>
      <privilege>Read Mac Applications</privilege>
      <privilege>Update Mac Applications</privilege>
      <privilege>Delete Mac Applications</privilege>
      <privilege>Create macOS Configuration Profiles</privilege>
      <privilege>Read macOS Configuration Profiles</privilege>
      <privilege>Update macOS Configuration Profiles</privilege>
      <privilege>Delete macOS Configuration Profiles</privilege>
      <privilege>Create Maintenance Pages</privilege>
      <privilege>Read Maintenance Pages</privilege>
      <privilege>Update Maintenance Pages</privilege>
      <privilege>Delete Maintenance Pages</privilege>
      <privilege>Create Managed Preference Profiles</privilege>
      <privilege>Read Managed Preference Profiles</privilege>
      <privilege>Update Managed Preference Profiles</privilege>
      <privilege>Delete Managed Preference Profiles</privilege>
      <privilege>Create Mobile Device Applications</privilege>
      <privilege>Read Mobile Device Applications</privilege>
      <privilege>Update Mobile Device Applications</privilege>
      <privilege>Delete Mobile Device Applications</privilege>
      <privilege>Create iOS Configuration Profiles</privilege>
      <privilege>Read iOS Configuration Profiles</privilege>
      <privilege>Update iOS Configuration Profiles</privilege>
      <privilege>Delete iOS Configuration Profiles</privilege>
      <privilege>Create Mobile Device Enrollment Invitations</privilege>
      <privilege>Read Mobile Device Enrollment Invitations</privilege>
      <privilege>Update Mobile Device Enrollment Invitations</privilege>
      <privilege>Delete Mobile Device Enrollment Invitations</privilege>
      <privilege>Create Mobile Device Extension Attributes</privilege>
      <privilege>Read Mobile Device Extension Attributes</privilege>
      <privilege>Update Mobile Device Extension Attributes</privilege>
      <privilege>Delete Mobile Device Extension Attributes</privilege>
      <privilege>Create Mobile Device Managed App Configurations</privilege>
      <privilege>Read Mobile Device Managed App Configurations</privilege>
      <privilege>Update Mobile Device Managed App Configurations</privilege>
      <privilege>Delete Mobile Device Managed App Configurations</privilege>
      <privilege>Create Mobile Device PreStage Enrollments</privilege>
      <privilege>Read Mobile Device PreStage Enrollments</privilege>
      <privilege>Update Mobile Device PreStage Enrollments</privilege>
      <privilege>Delete Mobile Device PreStage Enrollments</privilege>
      <privilege>Create Mobile Devices</privilege>
      <privilege>Read Mobile Devices</privilege>
      <privilege>Update Mobile Devices</privilege>
      <privilege>Delete Mobile Devices</privilege>
      <privilege>Create NetBoot Servers</privilege>
      <privilege>Read NetBoot Servers</privilege>
      <privilege>Update NetBoot Servers</privilege>
      <privilege>Delete NetBoot Servers</privilege>
      <privilege>Create Network Integration</privilege>
      <privilege>Read Network Integration</privilege>
      <privilege>Update Network Integration</privilege>
      <privilege>Delete Network Integration</privilege>
      <privilege>Create Network Segments</privilege>
      <privilege>Read Network Segments</privilege>
      <privilege>Update Network Segments</privilege>
      <privilege>Delete Network Segments</privilege>
      <privilege>Create Packages</privilege>
      <privilege>Read Packages</privilege>
      <privilege>Update Packages</privilege>
      <privilege>Delete Packages</privilege>
      <privilege>Create Patch Management Software Titles</privilege>
      <privilege>Read Patch Management Software Titles</privilege>
      <privilege>Update Patch Management Software Titles</privilege>
      <privilege>Delete Patch Management Software Titles</privilege>
      <privilege>Create Patch Policies</privilege>
      <privilege>Read Patch Policies</privilege>
      <privilege>Update Patch Policies</privilege>
      <privilege>Delete Patch Policies</privilege>
      <privilege>Create Peripheral Types</privilege>
      <privilege>Read Peripheral Types</privilege>
      <privilege>Update Peripheral Types</privilege>
      <privilege>Delete Peripheral Types</privilege>
      <privilege>Create Personal Device Configurations</privilege>
      <privilege>Read Personal Device Configurations</privilege>
      <privilege>Update Personal Device Configurations</privilege>
      <privilege>Delete Personal Device Configurations</privilege>
      <privilege>Create Personal Device Profiles</privilege>
      <privilege>Read Personal Device Profiles</privilege>
      <privilege>Update Personal Device Profiles</privilege>
      <privilege>Delete Personal Device Profiles</privilege>
      <privilege>Create Policies</privilege>
      <privilege>Read Policies</privilege>
      <privilege>Update Policies</privilege>
      <privilege>Delete Policies</privilege>
      <privilege>Create PreStages</privilege>
      <privilege>Read PreStages</privilege>
      <privilege>Update PreStages</privilege>
      <privilege>Delete PreStages</privilege>
      <privilege>Create Printers</privilege>
      <privilege>Read Printers</privilege>
      <privilege>Update Printers</privilege>
      <privilege>Delete Printers</privilege>
      <privilege>Create Provisioning Profiles</privilege>
      <privilege>Read Provisioning Profiles</privilege>
      <privilege>Update Provisioning Profiles</privilege>
      <privilege>Delete Provisioning Profiles</privilege>
      <privilege>Create Push Certificates</privilege>
      <privilege>Read Push Certificates</privilege>
      <privilege>Update Push Certificates</privilege>
      <privilege>Delete Push Certificates</privilege>
      <privilege>Create Removable MAC Address</privilege>
      <privilege>Read Removable MAC Address</privilege>
      <privilege>Update Removable MAC Address</privilege>
      <privilege>Delete Removable MAC Address</privilege>
      <privilege>Create Restricted Software</privilege>
      <privilege>Read Restricted Software</privilege>
      <privilege>Update Restricted Software</privilege>
      <privilege>Delete Restricted Software</privilege>
      <privilege>Create Scripts</privilege>
      <privilege>Read Scripts</privilege>
      <privilege>Update Scripts</privilege>
      <privilege>Delete Scripts</privilege>
      <privilege>Create Self Service Bookmarks</privilege>
      <privilege>Read Self Service Bookmarks</privilege>
      <privilege>Update Self Service Bookmarks</privilege>
      <privilege>Delete Self Service Bookmarks</privilege>
      <privilege>Create Sites</privilege>
      <privilege>Read Sites</privilege>
      <privilege>Update Sites</privilege>
      <privilege>Delete Sites</privilege>
      <privilege>Create Smart Computer Groups</privilege>
      <privilege>Read Smart Computer Groups</privilege>
      <privilege>Update Smart Computer Groups</privilege>
      <privilege>Delete Smart Computer Groups</privilege>
      <privilege>Create Smart Mobile Device Groups</privilege>
      <privilege>Read Smart Mobile Device Groups</privilege>
      <privilege>Update Smart Mobile Device Groups</privilege>
      <privilege>Delete Smart Mobile Device Groups</privilege>
      <privilege>Create Smart User Groups</privilege>
      <privilege>Read Smart User Groups</privilege>
      <privilege>Update Smart User Groups</privilege>
      <privilege>Delete Smart User Groups</privilege>
      <privilege>Create Software Update Servers</privilege>
      <privilege>Read Software Update Servers</privilege>
      <privilege>Update Software Update Servers</privilege>
      <privilege>Delete Software Update Servers</privilege>
      <privilege>Create Static Computer Groups</privilege>
      <privilege>Read Static Computer Groups</privilege>
      <privilege>Update Static Computer Groups</privilege>
      <privilege>Delete Static Computer Groups</privilege>
      <privilege>Create Static Mobile Device Groups</privilege>
      <privilege>Read Static Mobile Device Groups</privilege>
      <privilege>Update Static Mobile Device Groups</privilege>
      <privilege>Delete Static Mobile Device Groups</privilege>
      <privilege>Create Static User Groups</privilege>
      <privilege>Read Static User Groups</privilege>
      <privilege>Update Static User Groups</privilege>
      <privilege>Delete Static User Groups</privilege>
      <privilege>Create User Extension Attributes</privilege>
      <privilege>Read User Extension Attributes</privilege>
      <privilege>Update User Extension Attributes</privilege>
      <privilege>Delete User Extension Attributes</privilege>
      <privilege>Create User</privilege>
      <privilege>Read User</privilege>
      <privilege>Update User</privilege>
      <privilege>Delete User</privilege>
      <privilege>Create VPP Administrator Accounts</privilege>
      <privilege>Read VPP Administrator Accounts</privilege>
      <privilege>Update VPP Administrator Accounts</privilege>
      <privilege>Delete VPP Administrator Accounts</privilege>
      <privilege>Create VPP Assignment</privilege>
      <privilege>Read VPP Assignment</privilege>
      <privilege>Update VPP Assignment</privilege>
      <privilege>Delete VPP Assignment</privilege>
      <privilege>Create VPP Invitations</privilege>
      <privilege>Read VPP Invitations</privilege>
      <privilege>Update VPP Invitations</privilege>
      <privilege>Delete VPP Invitations</privilege>
      <privilege>Create Webhooks</privilege>
      <privilege>Read Webhooks</privilege>
      <privilege>Update Webhooks</privilege>
      <privilege>Delete Webhooks</privilege>
    </jss_objects>
    <jss_settings>
      <privilege>Read Activation Code</privilege>
      <privilege>Update Activation Code</privilege>
      <privilege>Read Apache Tomcat Settings</privilege>
      <privilege>Update Apache Tomcat Settings</privilege>
      <privilege>Read Apple Configurator Enrollment</privilege>
      <privilege>Update Apple Configurator Enrollment</privilege>
      <privilege>Read Education Settings</privilege>
      <privilege>Update Education Settings</privilege>
      <privilege>Read Mobile Device App Maintenance Settings</privilege>
      <privilege>Update Mobile Device App Maintenance Settings</privilege>
      <privilege>Read Automatic Mac App Updates Settings</privilege>
      <privilege>Update Automatic Mac App Updates Settings</privilege>
      <privilege>Read Autorun Imaging</privilege>
      <privilege>Update Autorun Imaging</privilege>
      <privilege>Read Cache</privilege>
      <privilege>Update Cache</privilege>
      <privilege>Read Change Management</privilege>
      <privilege>Update Change Management</privilege>
      <privilege>Read Computer Check-In</privilege>
      <privilege>Update Computer Check-In</privilege>
      <privilege>Read Cloud Distribution Point</privilege>
      <privilege>Update Cloud Distribution Point</privilege>
      <privilege>Read Clustering</privilege>
      <privilege>Update Clustering</privilege>
      <privilege>Read Computer Inventory Collection</privilege>
      <privilege>Update Computer Inventory Collection</privilege>
      <privilege>Read Customer Experience Metrics</privilege>
      <privilege>Update Customer Experience Metrics</privilege>
      <privilege>Read GSX Connection</privilege>
      <privilege>Update GSX Connection</privilege>
      <privilege>Read Patch Internal Source</privilege>
      <privilege/>
      <privilege>Read Jamf Imaging</privilege>
      <privilege>Update Jamf Imaging</privilege>
      <privilege>Read JSS URL</privilege>
      <privilege>Update JSS URL</privilege>
      <privilege>Read Limited Access Settings</privilege>
      <privilege>Update Limited Access Settings</privilege>
      <privilege>Read Retention Policy</privilege>
      <privilege>Update Retention Policy</privilege>
      <privilege>Read Microsoft Intune Integration</privilege>
      <privilege>Update Microsoft Intune Integration</privilege>
      <privilege>Read Mobile Device Inventory Collection</privilege>
      <privilege>Update Mobile Device Inventory Collection</privilege>
      <privilege>Read Password Policy</privilege>
      <privilege>Update Password Policy</privilege>
      <privilege>Read Patch Management Settings</privilege>
      <privilege>Update Patch Management Settings</privilege>
      <privilege>Read PKI</privilege>
      <privilege>Update PKI</privilege>
      <privilege>Read Re-enrollment</privilege>
      <privilege>Update Re-enrollment</privilege>
      <privilege>Read Computer Security</privilege>
      <privilege>Update Computer Security</privilege>
      <privilege>Read Self Service</privilege>
      <privilege>Update Self Service</privilege>
      <privilege>Read Mobile Device Self Service</privilege>
      <privilege>Update Mobile Device Self Service</privilege>
      <privilege>Read SSO Settings</privilege>
      <privilege>Update SSO Settings</privilege>
      <privilege>Read SMTP Server</privilege>
      <privilege>Update SMTP Server</privilege>
      <privilege>Read User-Initiated Enrollment</privilege>
      <privilege>Update User-Initiated Enrollment</privilege>
    </jss_settings>
    <jss_actions>
      <privilege>Allow User to Enroll</privilege>
      <privilege>Enroll Computers and Mobile Devices</privilege>
      <privilege>Change Password</privilege>
      <privilege>View License Serial Numbers</privilege>
      <privilege>Send Email to End Users via JSS</privilege>
      <privilege>Send Computer Remote Lock Command</privilege>
      <privilege>Send Computer Remote Wipe Command</privilege>
      <privilege>Send Computer Unmanage Command</privilege>
      <privilege>Send Computer Unlock User Account Command</privilege>
      <privilege>Send Computer Delete User Account Command</privilege>
      <privilege>View Disk Encryption Recovery Key</privilege>
      <privilege>View Activation Lock Bypass Code</privilege>
      <privilege>Flush Policy Logs</privilege>
      <privilege>Send Inventory Requests to Mobile Devices</privilege>
      <privilege>Send Mobile Device Remote Lock Command</privilege>
      <privilege>Send Mobile Device Remove Passcode Command</privilege>
      <privilege>Send Mobile Device Remove Restrictions Password Command</privilege>
      <privilege>Send Mobile Device Remote Wipe Command</privilege>
      <privilege>Unmanage Mobile Devices</privilege>
      <privilege>Send Mobile Device Managed Settings Command</privilege>
      <privilege>Send Mobile Device Mirroring Command</privilege>
      <privilege>Send Mobile Device Set Wallpaper Command</privilege>
      <privilege>Send Blank Pushes to Mobile Devices</privilege>
      <privilege>Send Mobile Device Enable Voice Roaming Command</privilege>
      <privilege>Send Mobile Device Disable Voice Roaming Command</privilege>
      <privilege>Send Mobile Device Enable Data Roaming Command</privilege>
      <privilege>Send Mobile Device Disable Data Roaming Command</privilege>
      <privilege>Send Mobile Device Set Device Name Command</privilege>
      <privilege>Send Mobile Device Remote Command to Download and Install iOS Update</privilege>
      <privilege>Send Computer Remote Command to Download and Install OS X Update</privilege>
      <privilege>Send Mobile Device Lost Mode Command</privilege>
      <privilege>View Mobile Device Lost Mode Location</privilege>
      <privilege>Send Mobile Device Shared iPad Commands</privilege>
      <privilege>Send Mobile Device Diagnostics and Usage Reporting and App Analytics Commands</privilege>
      <privilege>Send Mobile Device Restart Device Command</privilege>
      <privilege>View JSS Information</privilege>
      <privilege>Send Messages to Self Service Mobile</privilege>
      <privilege>View Event Logs</privilege>
      <privilege>Dismiss Notifications</privilege>
      <privilege>Send Update Passcode Lock Grace Period Command</privilege>
      <privilege>Send Mobile Device Shut Down Command</privilege>
    </jss_actions>
    <recon>
      <privilege>Add Computers Remotely</privilege>
      <privilege>Create QuickAdd Packages</privilege>
    </recon>
    <casper_admin>
      <privilege>Use Casper Admin</privilege>
      <privilege>Save With Casper Admin</privilege>
    </casper_admin>
    <casper_remote>
      <privilege>Use Casper Remote</privilege>
      <privilege>Install/Uninstall Software Remotely</privilege>
      <privilege>Run Scripts Remotely</privilege>
      <privilege>Map Printers Remotely</privilege>
      <privilege>Add Dock Items Remotely</privilege>
      <privilege>Manage Local User Accounts Remotely</privilege>
      <privilege>Change Management Account Remotely</privilege>
      <privilege>Bind to Active Directory Remotely</privilege>
      <privilege>Set Open Firmware/EFI Passwords Remotely</privilege>
      <privilege>Reboot Computers Remotely</privilege>
      <privilege>Perform Maintenance Tasks Remotely</privilege>
      <privilege>Search for Files/Processes Remotely</privilege>
      <privilege>Enable Disk Encryption Configurations Remotely</privilege>
      <privilege>Screen Share with Remote Computers</privilege>
      <privilege>Screen Share with Remote Computers Without Asking</privilege>
    </casper_remote>
    <casper_imaging>
      <privilege>Use Casper Imaging</privilege>
      <privilege>Customize a Configuration</privilege>
      <privilege>Store Autorun Data</privilege>
      <privilege>Use PreStage Imaging and Autorun Imaging</privilege>
    </casper_imaging>
  </privileges>''')
# privilegeXML = ET.SubElement(account, 'privileges')
# privilegeXML.extend(privileges)


# Check for account num
def accountCheck(name = ''):
    """docstring for accountCheck"""    
    responsexml = jamfcall('https://' + server + '/JSSResource/accounts', username, password, method='GET')
    number = 0
    # print name
    # For each account in the list
    for account in responsexml.find('users'):
        accountNum = int(account.find('id').text)
        accountName = account.find('name').text
        # print accountNum
        # print accountName
        if accountName == name:
            number = accountNum
    return number

# print "Existing Account Num: " + str(accountCheck(userName))

if accountCheck(userName) != 0:
    print ("User account already exists")
    # newAccountID = accountCheck(userName)
    # 
    # responsexml = jamfcall('https://' + server + '/JSSResource/accounts/userid/' + str(newAccountID), username, password, method='GET')
    # # print ET.tostring(responsexml)
    # oldPass = responsexml.find('password_sha256')
    # responsexml.remove(oldPass)
    # # responsexml.remove(responsexml.findall('password_sha256'))
    # accountPass = ET.SubElement(responsexml, 'password')
    # accountPass.text = defaultPassword
    # print ET.tostring(responsexml)
    
    
else:
    # Create account
    # print ET.tostring(account)
    responsexml = jamfcall('https://' + server + '/JSSResource/accounts/userid/0', username, password, method='POST', data = ET.tostring(account))
    # print responsexml.text
    # Get account ID
    newAccountID = accountCheck(userName)
    # print newAccountID
    # Get account XML
    currentuserxml = jamfcall('https://' + server + '/JSSResource/accounts/userid/' + str(newAccountID), username, password, method='GET')
    # print responsexml.text
    # Find and remove the sha256 password
    oldPass = currentuserxml.find('password_sha256')
    currentuserxml.remove(oldPass)
    # responsexml.remove(responsexml.findall('password_sha256'))
    accountPass = ET.SubElement(currentuserxml, 'password')
    accountPass.text = defaultPassword
    print (ET.tostring(currentuserxml))
    # Post back to JAMF
    responsexml = jamfcall('https://' + server + '/JSSResource/accounts/userid/' + str(newAccountID), username, password, method='PUT',data = ET.tostring(currentuserxml))
    print (responsexml.text)

exit(0)