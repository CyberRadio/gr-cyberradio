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


# VERSION: Version string for this application
VERSION=CyberRadioDriver.version
# NAME: Name of the application
NAME=CyberRadioDriver.name
# DESCRIPTION: Description of the application
DESCRIPTION=CyberRadioDriver.description
# AUTHOR: Author of the application
AUTHOR='CyberRadio Solutions, Inc.'
# EMAIL: E-mail address for the maintainer of the application
EMAIL='sales@cyberradiosolutions.com'
# MODULE_LIST: List of Python modules to install
MODULE_LIST=[ ]
# PACKAGE_LIST: List of Python packages to install
PACKAGE_LIST=[ \
               'CyberRadioDriver', \
               'CyberRadioDriver.radios', \
              ]
# SCRIPT_LIST: List of script files to install
SCRIPT_LIST=['apps/ndr_dataport_config']
# CONF_FILE_LIST: List of configuration files to install 
CONF_FILE_LIST=[]
# INIT_SCRIPT_LIST: List of system initialization scripts to install.
# If a script has the extension ".init", the extension is stripped
# upon installation. 
INIT_SCRIPT_LIST=[]
# DOXY_FILE_LIST: List of Doxygen files to process for automatic 
# generation of documentation.
DOXY_FILE_LIST=['CyberRadioDriver.doxyfile']
# DESKTOP_FILE_LIST: List of Open Desktop Specification files
# to use for generating menu shortcuts in the session manager.
DESKTOP_FILE_LIST=['CyberRadioDriver.desktop']
# EXTERNALS_INFO: Describes external C/C++ programs that need to be 
# built and installed as part of the installation procedure.
# 
# This is a nested dictionary.  The keys are executable names, 
# and the values are dictionaries with the following key-value pairs:
# * "sources": List of source files
# * "include_dirs": List of include file directories
# * "library_dirs": List of link library directories
# * "libraries": List of libraries to link against (each minus any 
#   "lib" prefix)
# * "compiler_options": List of extra options to add to the compiler
#   command line 
# * "linker_options": List of extra options to add to the linker
#   command line 
EXTERNALS_INFO={}
# PACKAGE_DIR_LIST: Package directory information dictionary.  This is
# a dictionary where the keys are package names and the values are 
# relative directory names where the package files are found.
PACKAGE_DIR_LIST={}
# PACKAGE_DATA_LIST: Package data information dictionary.  This is
# a dictionary where the keys are package names and the values are 
# lists of file specifications indicating which files should be 
# installed as package data.
PACKAGE_DATA_LIST={}
# DATA_FILE_LIST: Data file information.  This is a list of 2-tuples:
# (install directory, list of data files).
DATA_FILE_LIST=[]
# The following parameters have meaning only under Windows
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
    # Custom classes that handle "python setup.py build" and 
    # "python setup.py install" commands for us
    # -- LinuxDistribution extends the default distribution handling
    #    to handle special types of files (configuration files, daemon 
    #    init files, Doxygen scripts, desktop files).
    # -- LinuxBuildDocs adds a custom command ("python setup.py build_docs")
    #    that generate documentation using Doxygen if Doxygen configuration 
    #    files are provided. The resulting documentation is assumed to be in
    #    the "docs" directory.
    # -- LinuxBuild extends the default build procedure to call LinuxBuildDocs
    #    as an extra subcommand.
    # -- LinuxInstall extends the default installation procedure:
    #    -- Installs configuration files to /etc or ${prefix}/etc, depending
    #       on the "prefix" setting
    #    -- Installs init scripts to /etc/init.d
    #     -- Automatically generates documentation using Doxygen if Doxygen 
    #          configuration files are provided
    # -- Installs desktop files to /usr/share/applications
    import distutils.dist
    import distutils.cmd
    import distutils.command.build
    import distutils.command.build_scripts
    import distutils.command.install
    import distutils.ccompiler
    import distutils.log
    import tarfile
    
    ##
    # LinuxDistribution implements the entire distribution.
    class LinuxDistribution(distutils.dist.Distribution):
        
        # OVERRIDE
        # -- Exposes "conf_files", "init_files", "doxy_files", "desktop_files", 
        #    and "externals_info"
        def __init__ (self, attrs=None):
            self.conf_files = None
            self.init_files = None
            self.doxy_files = None
            self.desktop_files = None
            self.externals_info = None
            distutils.dist.Distribution.__init__(self, attrs)
                        
    ##
    # LinuxBuildDocs implements the "build_docs" command.
    class LinuxBuildDocs(distutils.cmd.Command):
        description = "build documentation using Doxygen"
        user_options = []
        
        # OVERRIDE
        def initialize_options(self):
            pass
        
        # OVERRIDE
        def finalize_options(self):
            pass
        
        # OVERRIDE
        def run(self):
            # Execute Doxygen on each Doxyfile
            for doxy_file in self.distribution.doxy_files:
                if os.access(doxy_file, os.F_OK):
                    # Execute Doxygen
                    self.executeDoxygen(doxy_file)
            # Create a tar archive containing the generated docs
            tarName = "%s-%s-docs.tar.gz" % ( self.distribution.get_name(), 
                                              self.distribution.get_version() )
            self.distribution.announce("generating tar archive %s for docs" % tarName)
            tarFile = tarfile.open(name=tarName, mode="w:gz")
            for f in glob.iglob("docs/*"):
                tarFile.add(f, f.replace("docs/", "", 1), True)
            tarFile.close()
            pass
    
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
        
    ##
    # LinuxBuildScripts extends "build_scripts" to build external programs as well
    # as executable Python scripts.
    class LinuxBuildScripts(distutils.command.build_scripts.build_scripts):

        # OVERRIDE
        def initialize_options(self):
            distutils.command.build_scripts.build_scripts.initialize_options(self)
            self.externals_info = self.distribution.externals_info
            
        # OVERRIDE
        def finalize_options(self):
            distutils.command.build_scripts.build_scripts.finalize_options(self)
            
        # OVERRIDE
        def run (self):
            # Compile and link external executables, adding them to the list
            # of scripts.
            if self.externals_info != {}:
                comp = distutils.ccompiler.new_compiler()
                for external_name in self.externals_info:
                    external_info = self.externals_info[external_name]
                    external_srcs = external_info.get("sources", [])
                    external_incdirs = external_info.get("include_dirs", [])
                    external_libdirs = external_info.get("library_dirs", [])
                    external_libs = external_info.get("libraries", [])
                    external_compopts = external_info.get("compiler_options", [])
                    external_linkopts = external_info.get("linker_options", [])
                    distutils.log.info("building external program %s", external_name)
                    external_objs = comp.compile(sources=external_srcs, 
                                                include_dirs=external_incdirs,
                                                extra_preargs=external_compopts)
                    comp.link_executable(objects=external_objs, 
                                         output_progname=external_name, 
                                         libraries=external_libs,
                                         library_dirs=external_libdirs,
                                         extra_preargs=external_linkopts)
                    self.scripts.append(external_name)
            # Execute base-class version to handle all "scripts"
            distutils.command.build_scripts.build_scripts.run(self)
    
    ##
    # LinuxBuild simply extends the subcommand list so that it runs the
    # "build_docs" command as part of the standard "build" command.
    class LinuxBuild(distutils.command.build.build):
        
        # OVERRIDE -- Need to override for the subcommand list
        def has_pure_modules(self):
            return distutils.command.build.build.has_pure_modules(self)
    
        # OVERRIDE -- Need to override for the subcommand list
        def has_c_libraries(self):
            return distutils.command.build.build.has_c_libraries(self)
    
        # OVERRIDE -- Need to override for the subcommand list
        def has_ext_modules(self):
            return distutils.command.build.build.has_ext_modules(self)
    
        # OVERRIDE -- Need to override for the subcommand list
        def has_scripts(self):
            return distutils.command.build.build.has_scripts(self)
    
        # EXTENSION
        def has_doxyfiles(self):
            return ( self.distribution.doxy_files is not None and \
                     len(self.distribution.doxy_files) > 0 )
        
        sub_commands = [('build_py',      has_pure_modules),
                        ('build_clib',    has_c_libraries),
                        ('build_ext',     has_ext_modules),
                        ('build_scripts', has_scripts),
                        ('build_docs',    has_doxyfiles),
                       ]

    ##
    # LinuxInstall extends the standard "install" command to handle special
    # types of files.
    class LinuxInstall(distutils.command.install.install):
        
        # OVERRIDE
        def initialize_options(self):
            distutils.command.install.install.initialize_options(self)
            self.conf_prefix = ''
            self.init_prefix = '/etc/init.d'
            self.desktop_prefix = '/usr/share/applications'
            self.docs_prefix = '/usr/share/doc'

        # OVERRIDE
        def finalize_options(self):
            distutils.command.install.install.finalize_options(self)
            # At this point, self.install_data is the best indicator of
            # whether files are being installed into local storage.
            # -- Typical installations through setup.py will install
            #    into local storage (/usr/local tree).
            # -- Debian package builds will install into system storage
            #    (/usr and /etc trees).
            # Use self.install_data as the base for where custom stuff gets
            # installed.
            # -- NOTE: the base-class version sets self.install_data based  
            #    on the --root option (if provided), so none of our install
            #    code needs to worry about the root setting.
            if self.install_data.endswith("/local"):
                self.conf_prefix = os.path.join(self.install_data, 'etc')
            else:
                self.conf_prefix = self.install_data.replace("/usr", "/etc")
            self.init_prefix = os.path.join(self.conf_prefix, "init.d")
            self.desktop_prefix = os.path.join(self.install_data, "share", 
                                               "applications")
            self.docs_prefix = os.path.join(self.install_data, "share", "doc", 
                                            self.distribution.get_name())

        # EXTENSION
        def ensurePathToFileExists(self, filename):
            dirname = os.path.dirname(os.path.normpath(filename))
            if not os.access(dirname, os.F_OK):
                self.distribution.announce("creating %s" % dirname)
                os.makedirs(dirname)
            
        # EXTENSION
        def fileListFromSpecs(self, filespecs):
            newspecs = []
            newfiles = []
            tmpspecs = filespecs
            if isinstance(filespecs, str):
                tmpspecs = [filespecs]
            for spec in tmpspecs:
                newspecs += glob.glob(spec)
            for spec in newspecs:
                if os.path.isdir(spec):
                    for direc, subdirs, files in os.walk(spec):
                        for fname in files:
                            pth = os.path.join(direc, fname)
                            newfiles.append(pth)             
                else:
                    newfiles.append(spec)
            newfiles = list(set(newfiles))
            return sorted(newfiles)

        # OVERRIDE
        def run(self):
            # Run base-class installation procedure
            distutils.command.install.install.run(self)
            # Install configuration files
            for conf_file in self.distribution.conf_files:
                if os.access(conf_file, os.F_OK):
                    dst = os.path.join(
                            self.conf_prefix,
                            os.path.basename(conf_file)
                        )
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (conf_file, dst))
                    self.copy_file(conf_file, dst)
            # Install init scripts
            for init_file in self.distribution.init_files:
                if os.access(init_file, os.F_OK):
                    # If init file name ends with ".init", then strip this 
                    # ending off of the filename
                    tmp = init_file.replace(".init", "")
                    dst = os.path.join(
                            self.init_prefix,
                            os.path.basename(tmp)
                        )
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (init_file, dst))
                    self.copy_file(init_file, dst)
                    # Make the destination file executable
                    self.distribution.announce("changing mode of %s to 755" % dst)
                    os.chmod(dst, 0755)
            # Install docs
            if os.access("docs", os.F_OK):
                for docs_file in self.fileListFromSpecs("docs/*"):
                    dst = os.path.join(
                            self.docs_prefix,
                            docs_file.replace("docs/", "", 1)
                        )
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (docs_file, dst))
                    self.copy_file(docs_file, dst)
                pass
            # Install desktop files
            for desktop_file in self.distribution.desktop_files:
                if os.access(desktop_file, os.F_OK):
                    dst = os.path.join(
                            self.desktop_prefix,
                            os.path.basename(desktop_file)
                        )
                    self.ensurePathToFileExists(dst)
                    self.distribution.announce("copying %s -> %s" % (desktop_file, dst))
                    self.copy_file(desktop_file, dst)
    
    # Under Linux, use the script argument to determine how to package it (tarball using
    # "bdist_dumb" or RPM using "bdist_rpm").  RPM packages can be made into Debian (Ubuntu)
    # installers using the "alien" utility.
    setup(distclass = LinuxDistribution, \
          cmdclass = {
                'build_docs': LinuxBuildDocs,
                'build': LinuxBuild, 
                'install': LinuxInstall
            },
          name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          author=AUTHOR,
          author_email=EMAIL,
          packages=PACKAGE_LIST,
          scripts=SCRIPT_LIST,
          package_dir=PACKAGE_DIR_LIST,
          package_data=PACKAGE_DATA_LIST,
          data_files=DATA_FILE_LIST,
          conf_files=CONF_FILE_LIST,
          init_files=INIT_SCRIPT_LIST,
          doxy_files=DOXY_FILE_LIST,
          desktop_files=DESKTOP_FILE_LIST,
          externals_info=EXTERNALS_INFO,
         )
    
      
print "PLATFORM: ", sys.platform

