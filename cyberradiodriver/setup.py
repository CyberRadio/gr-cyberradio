#!/usr/bin/env python
###############################################################
# setup.py
#
# Distutils setup script for CyberRadioDriver module
#
# Author: DA
# Company: CyberRadio Solutions, Inc.
# Copyright: Copyright (c) 2015 CyberRadio Solutions, Inc.  All 
#    rights reserved.
#
# NOTES
# -----
# Under Win32, we can use the py2exe package to create a Windows 
# executable from the Python code.  To do this, specify "py2exe" 
# as an argument to the script.  We can also build an MSI installer
# using the built-in "bdist_msi" argument.
#
# Under Linux, use the script argument to determine how to package 
# it (tarball using "bdist_dumb" or RPM using "bdist_rpm").  RPM 
# packages can be made into Debian (Ubuntu) installers using the 
# third-party "alien" utility.  Alternatively, if the source 
# folder contains a "debian" sub-directory, the Debian package-
# building tools can be used to build a package that installs all 
# of the files that this script would if it was executed as
# "python setup.py install".
#
###############################################################

import CyberRadioDriver
from distutils.core import setup
from distutils.sysconfig import get_python_lib
import sys, os, glob


# Configuration information for this application.  This should be consistent 
# across platforms, though there may be exceptions.
VERSION=CyberRadioDriver.version
NAME=CyberRadioDriver.name
DESCRIPTION=CyberRadioDriver.description
AUTHOR='CyberRadio Solutions, Inc.'
EMAIL='sales@cyberradiosolutions.com'
PACKAGE_LIST=[ \
               'CyberRadioDriver', \
               'CyberRadioDriver.radios', \
               'CyberRadioDriver.radios.internal', \
              ]
if sys.platform == 'win32':
    SCRIPT_LIST=[]
    # Installing configuration files not supported under Windows right now
    # Installing init script files not supported under Windows right now
    # Automatic document generation not supported under Windows right now
else:
    SCRIPT_LIST=['apps/ndr_dataport_config']
    CONF_FILE_LIST=[]
    INIT_SCRIPT_LIST=[]
    DOXY_FILE_LIST=['CyberRadioDriver.doxyfile']
    DESKTOP_FILE_LIST=['CyberRadioDriver.desktop']
PACKAGE_DIR_LIST={}
PACKAGE_DATA_LIST={}
DATA_FILE_LIST=[]
PACKAGE_DATA_LIST={}
README_LIST=[ \
             ]
WINDOWS_ZIPPKG_LIST=[ \
                     ]
WINDOWS_WXPYTHON_SUPPORT=False
WINDOWS_PYWIN32_SUPPORT=False
WINDOWS_MATPLOTLIB_SUPPORT=False

# Package building code (platform-dependent)
if sys.platform == 'win32':
    # Under Win32, we can use the py2exe package to create a Windows executable from the
    # Python code.  To do this, specify "py2exe" as an argument to the script.
    py2exeOpts = {}
    if "py2exe" in sys.argv:
        py2exeOpts = {'py2exe': {'bundle_files': 1, \
                                 "dll_excludes": ["mswsock.dll", "MSWSOCK.dll"], \
                              }}
        if WINDOWS_WXPYTHON_SUPPORT:
            sys.path.append("C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")
            DATA_FILE_LIST += [("Microsoft.VC90.CRT", glob.glob(r'C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
        if WINDOWS_PYWIN32_SUPPORT:
            pywin32path = os.path.join(get_python_lib(), "pythonwin")
            sys.path.append(pywin32path)
            DATA_FILE_LIST += [("Microsoft.VC90.MFC", glob.glob(os.path.join(pywin32path, "*.dll")))]
            DATA_FILE_LIST += [("Microsoft.VC90.MFC", glob.glob(os.path.join(pywin32path, "*.manifest")))]
        if WINDOWS_MATPLOTLIB_SUPPORT:
            from distutils.filelist import findall
            import matplotlib
            matplotlibdatadir = matplotlib.get_data_path()
            matplotlibdata = findall(matplotlibdatadir)
            for f in matplotlibdata:
                dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
                DATA_FILE_LIST.append((os.path.split(dirname)[0], [f]))
            py2exeOpts['py2exe']['packages'] = ['matplotlib', 'numpy', 'pytz']
            #py2exeOpts['py2exe']['includes'] = 'matplotlib.numerix.random_array'
            py2exeOpts['py2exe']['excludes'] = ['_gtkagg', '_tkagg']
            py2exeOpts['py2exe']['dll_excludes'].extend(['libgdk-win32-2.0-0.dll', \
                                                         'libgdk_pixbuf-2.0-0.dll', \
                                                         'libgobject-2.0-0.dll'])
        try:
            import py2exe
        except:
            raise RuntimeError("Cannot build executable using py2exe because the package is not installed")
    # We can also build an MSI installer by specifying "bdist_msi" as an argument to the script.
    # This is built-in functionality.
    setup(name=NAME, \
          version=VERSION, \
          description=DESCRIPTION, \
          author=AUTHOR, \
          author_email=EMAIL, \
          packages=PACKAGE_LIST, \
          scripts=SCRIPT_LIST, \
          console=SCRIPT_LIST, \
          package_dir=PACKAGE_DIR_LIST, \
          package_data=PACKAGE_DATA_LIST, \
          data_files=DATA_FILE_LIST, \
          options=py2exeOpts, \
          zipfile=None, \
         )
    # Automatically package the results as a version-tagged ZIP archive, if desired
    if len(WINDOWS_ZIPPKG_LIST) > 0:
        import zipfile, os, shutil
        ziptarget = os.path.join("dist", "%s-%s.zip" % (NAME, VERSION))
        print "Packaging archive:", ziptarget
        for fname in README_LIST:
            shutil.copy(fname, os.path.join("dist", fname))
        zfs = zipfile.ZipFile(ziptarget, "w", zipfile.ZIP_DEFLATED)
        for fname in WINDOWS_ZIPPKG_LIST:
            zfs.write(os.path.join("dist", fname), fname)
        zfs.close()
else:
    # Linux
    # Custom classes that handle "python setup.py install" command for us
    # -- Installs configuration files to /etc or ${prefix}/etc, depending
    #    on the "prefix" setting
    # -- Installs init scripts to /etc/init.d
    # -- Automatically generates documentation using Doxygen if Doxygen 
    #    configuration files are provided
    # -- Installs desktop files to /usr/share/applications
    import distutils.dist
    import distutils.command.install
    
    class LinuxDistribution(distutils.dist.Distribution):
        
        # OVERRIDE
        # -- Exposes "conf_files", "init_files", "doxy_files", and
        #    "desktop_files"
        def __init__ (self, attrs=None):
            self.conf_files = None
            self.init_files = None
            self.doxy_files = None
            self.desktop_files = None
            distutils.dist.Distribution.__init__(self, attrs)
                        
            
    class LinuxInstall(distutils.command.install.install):
        
        # OVERRIDE
        def initialize_options(self):
            distutils.command.install.install.initialize_options(self)
            self.conf_prefix = ''
            self.init_prefix = '/etc/init.d'
            self.desktop_prefix = '/usr/share/applications'

        # OVERRIDE
        def finalize_options(self):
            distutils.command.install.install.finalize_options(self)
            if self.prefix == '/usr':
                self.conf_prefix = '/etc'
            else:
                self.conf_prefix = os.path.join(self.prefix, 'etc')
            
        # EXTENSION
        def ensurePathToFileExists(self, filename):
            dirname = os.path.dirname(os.path.normpath(filename))
            if not os.access(dirname, os.F_OK):
                self.distribution.announce("creating %s" % dirname)
            os.makedirs(dirname)
            
        # EXTENSION
        def executeDoxygen(self, doxy_file):
            # (1) Update the configuration file with the correct application name
            #     and version number
            self.distribution.announce("updating Doxygen file %s with name and version" % doxy_file)
            ifs = open(doxy_file, "r")
            lines = ifs.readlines()
            ifs.close()
            for i in xrange(0, len(lines), 1):
                if "PROJECT_NAME = " in lines[i]:
                    lines[i] = "PROJECT_NAME = " + self.distribution.get_name() + "\n"
                if "PROJECT_NUMBER = " in lines[i]:
                    lines[i] = "PROJECT_NUMBER = " + self.distribution.get_version() + "\n"
            ofs = open(doxy_file, "w")
            ofs.writelines(lines)
            ofs.close()
            # (2) Execute Doxygen to generate the docs.
            self.distribution.announce("executing Doxygen on file %s" % doxy_file)
            self.spawn(["doxygen", doxy_file])
        
        # OVERRIDE
        def run(self):
            # Run base-class installation procedure
            distutils.command.install.install.run(self)
            # Install configuration files
            for conf_file in self.distribution.conf_files:
                if os.access(conf_file, os.F_OK):
                    # os.path.join() drops the root path if the conf_prefix contains
                    # a leading slash
                    dstComponents = []
                    dstComponents.append("/" if self.root is None \
                                         else self.root)
                    dstComponents.append(self.conf_prefix[1:] if \
                                         self.conf_prefix.startswith("/") \
                                         else self.conf_prefix)
                    dstComponents.append(os.path.basename(conf_file))
                    dst = os.path.join(*dstComponents)
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (conf_file, dst))
                    self.copy_file(conf_file, dst)
            # Install init scripts
            for init_file in self.distribution.init_files:
                if os.access(init_file, os.F_OK):
                    # If init file name ends with ".init", then strip this 
                    # ending off of the filename
                    tmp = init_file.replace(".init", "")
                    # os.path.join() drops the root path if the init_prefix contains
                    # a leading slash
                    dstComponents = []
                    dstComponents.append("/" if self.root is None \
                                         else self.root)
                    dstComponents.append(self.init_prefix[1:] if \
                                         self.init_prefix.startswith("/") \
                                         else self.init_prefix)
                    dstComponents.append(os.path.basename(tmp))
                    dst = os.path.join(*dstComponents)
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (init_file, dst))
                    self.copy_file(init_file, dst)
                    # Make the destination file executable
                    self.distribution.announce("changing mode of %s to 755" % dst)
                    os.chmod(dst, 755)
            # Execute Doxygen
            for doxy_file in self.distribution.doxy_files:
                if os.access(doxy_file, os.F_OK):
                    # Execute Doxygen
                    self.executeDoxygen(doxy_file)
            # Install desktop files
            for desktop_file in self.distribution.desktop_files:
                if os.access(desktop_file, os.F_OK):
                    # os.path.join() drops the root path if the desktop_prefix contains
                    # a leading slash
                    dstComponents = []
                    dstComponents.append("/" if self.root is None \
                                         else self.root)
                    dstComponents.append(self.desktop_prefix[1:] if \
                                         self.desktop_prefix.startswith("/") \
                                         else self.desktop_prefix)
                    dstComponents.append(os.path.basename(desktop_file))
                    dst = os.path.join(*dstComponents)
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (desktop_file, dst))
                    self.copy_file(desktop_file, dst)
    
    # Under Linux, use the script argument to determine how to package it (tarball using
    # "bdist_dumb" or RPM using "bdist_rpm").  RPM packages can be made into Debian (Ubuntu)
    # installers using the "alien" utility.
    setup(distclass = LinuxDistribution, \
          cmdclass = {'install': LinuxInstall}, \
          name=NAME, \
          version=VERSION, \
          description=DESCRIPTION, \
          author=AUTHOR, \
          author_email=EMAIL, \
          packages=PACKAGE_LIST, \
          scripts=SCRIPT_LIST, \
          package_dir=PACKAGE_DIR_LIST, \
          package_data=PACKAGE_DATA_LIST, \
          data_files=DATA_FILE_LIST, \
          conf_files=CONF_FILE_LIST, \
          init_files=INIT_SCRIPT_LIST, \
          doxy_files=DOXY_FILE_LIST, \
          desktop_files=DESKTOP_FILE_LIST, \
         )
    
      
print "PLATFORM: ", sys.platform

