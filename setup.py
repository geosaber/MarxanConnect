#import modules
import sys
import os
from cx_Freeze import setup, Executable

if os.name=='nt':
    # editing out deprecated functions in gui.py
    # Read in the file
    with open('gui.py', 'r', encoding="utf8") as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('wx.HyperlinkCtrl', 'wx.adv.HyperlinkCtrl')
    filedata = filedata.replace('wx.HL_DEFAULT_STYLE', 'wx.adv.HL_DEFAULT_STYLE')

    # Write the file out again
    with open('gui.py', 'w', encoding="utf8") as file:
      file.write(filedata)

    # prep for cx_Freeze
    os.environ['TCL_LIBRARY'] = os.path.join(os.environ['LOCALAPPDATA'],'Programs','Python','Python35','tcl','tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(os.environ['LOCALAPPDATA'],'Programs','Python','Python35','tcl','tk8.6')

    # define additional modules (those not automatically found)
    build_exe_options = {'includes': ['numpy.core._methods', 'numpy.lib.format','matplotlib.backends.backend_qt5agg',
                                      'matplotlib.backends.backend_tkagg','tkinter','tkinter.filedialog','igraph',
                                      'igraph.vendor.texttable'],
                         'include_files': ['data/','gui.py','glossary.html','tutorial.html','contributing.html',
                                           'index.html','site_libs/',
                                           os.path.join(os.environ['LOCALAPPDATA'],
                                                        'Programs','Python','Python35','DLLs','tcl86t.dll'),
                                           os.path.join(os.environ['LOCALAPPDATA'],
                                                        'Programs','Python','Python35','DLLs','tk86t.dll'),
                                           os.path.join(sys.path[0],'images','icon_bundle.ico'),'images/'],
                         'namespace_packages': ['mpl_toolkits'] }

    base = None
    if sys.platform == 'win32':
        base = 'Win32GUI'

    setup(name = 'MarxanConnectGUI' ,
          version = '0.0.4' ,
          description = '' ,
          options = {'build_exe': build_exe_options},
          executables = [Executable('MarxanConnectGUI.py', base=base, icon=os.path.join(sys.path[0],'images','icon_bundle.ico'))])
else:
    # define additional modules (those not automatically found)
    build_exe_options = {'includes': ['numpy.core._methods','packaging.version','packaging.specifiers',
                                      'packaging.requirements','igraph.vendor.texttable'],
                         'include_files': ['data/', 'gui.py', 'glossary.html', 'tutorial.html', 'contributing.html',
                                           os.path.join(sys.path[0], 'icon_mac.icns')],
                         }

    mac_options = {'iconfile': os.path.join(sys.path[0], 'icon_mac.icns')}

    setup(name='MarxanConnectGUI',
          version='0.0.4',
          description='',
          options={'build_exe': build_exe_options,
                   'bdist_mac': mac_options},
          executables=[Executable('MarxanConnectGUI.py')])


