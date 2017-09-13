#importing wx files
import wx
import wx.lib.agw.aui as aui
import wx.adv

#import the GUI file after editing out deprecated functions
# Read in the file
with open('gui.py', 'r', encoding="utf8") as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('SetToolTipString', 'SetToolTip')

# Write the file out again
with open('gui.py', 'w', encoding="utf8") as file:
  file.write(filedata)
import gui

#import matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap

# import spatial modules
import geopandas as gpd
from descartes import PolygonPatch
import shapely

#import system helper modules
import os
import pandas
import numpy
import networkx as nx
import threading
import json


# import MarxanConnect python module
import marxanconpy


# define wildcards
wc_MarCon = "Marxan with Connectivity Project (*.MarCon)|*.MarCon|" \
            "All files (*.*)|*.*"

class MarxanConnectGUI(gui.MarxanConnectGUI):
    
    def __init__(self,parent):
        """
        initialize parent class (the entire GUI)
        """
        gui.MarxanConnectGUI.__init__(self,parent)
        
        # set the icon
        icons = wx.IconBundle()
        for sz in [16, 32, 48, 96, 256]: 
            try: 
                icon = wx.Icon(os.path.join(os.getcwd(),'icon_bundle.ico'), wx.BITMAP_TYPE_ICO, desiredWidth=sz, desiredHeight=sz)
                icons.AddIcon(icon) 
            except: 
                pass 
                self.SetIcons(icons)
        
        # launch a blank new project
        self.on_new_project(event=None, launch = True)
        
        # launch Getting started window
#        frame = getting_started(parent=self)
#        frame.Show()
        
        # set opening tab to SPatial Input (0)
        self.m_auinotebook1.ChangeSelection(2)
    
###########################  project managment functions ######################        
    def on_new_project( self, event, launch = False):
        """
        open a new project and name/save a new project file
        """
        # create project list to store project specific data
        self.project = {}
        self.project['workingdirectory'] = os.path.join(os.environ['USERPROFILE'], "Documents")
        self.project['filepaths'] = {}
        
        # set default file paths
        if(os.path.isdir(os.path.join(os.environ['ProgramFiles(x86)'], "MarxanConnect"))):
            pfdir = os.path.join(os.environ['ProgramFiles(x86)'], "MarxanConnect")
        else:
            pfdir = os.path.join(os.environ['ProgramFiles'], "MarxanConnect")
        self.project['filepaths']['pu_filepath'] = os.path.join(pfdir,"data","shapefiles","marxan_pu.shp")
        self.project['filepaths']['cu_filepath'] = os.path.join(pfdir,"data","shapefiles","connectivity_grid.shp")
        self.project['filepaths']['cm_filepath'] = os.path.join(pfdir,"data","grid_connectivity_matrix.csv")
        self.project['filepaths']['pucm_filepath'] = os.path.join(os.environ['USERPROFILE'], "Documents","PU_connectivity_matrix.csv")
        self.project['filepaths']['cf_filepath'] = os.path.join(os.environ['USERPROFILE'], "Documents","puvspr.dat")
        self.project['filepaths']['spec_filepath'] = os.path.join(os.environ['USERPROFILE'], "Documents","PU_connectivity_matrix.csv")
        self.project['filepaths']['bd_filepath'] = os.path.join(os.environ['USERPROFILE'], "Documents","PU_connectivity_matrix.csv")
        
        # if called at launch time, no need to ask users to create a new project file right away
        if(not launch):
            dlg = wx.FileDialog(self, "Create a new project file:",style=wx.FD_SAVE,wildcard=wc_MarCon)
            if dlg.ShowModal() == wx.ID_OK:
                self.project['filepaths']['projfile'] = dlg.GetPath()
                self.project['filepaths']['projfilename'] = dlg.GetFilename()
                self.project['workingdirectory'] = dlg.GetDirectory() 
                with open(self.project['filepaths']['projfile'], 'w') as fp:
                    json.dump(self.project, fp, indent=4, sort_keys=True)
                frame.SetTitle('Marxan with Connectivity (Project: '+self.project['filepaths']['projfilename']+')')
            dlg.Destroy()       
        
    def on_load_project(self, event):
        """
        Create and show the Open FileDialog to load a project
        """
        self.project = {}
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.project['workingdirectory'], 
            defaultFile="",
            wildcard=wc_MarCon,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.project['filepaths']['projfile'] = dlg.GetPath()
            with open(self.project['filepaths']['projfile'], 'r') as fp:
                self.project=json.loads(fp.read())
        dlg.Destroy()
        frame.SetTitle('Marxan with Connectivity (Project: '+self.project['filepaths']['projfilename']+')')

 
    def on_save_project_as(self, event):
        """
        Create and show the Open FileDialog to save a project
        """
        dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=self.project['workingdirectory'], 
            defaultFile="", wildcard=wc_MarCon, style=wx.FD_SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.project['filepaths']['projfile'] = dlg.GetPath()
            self.project['filepaths']['projfilename'] = dlg.GetFilename()
            self.project['workingdirectory'] = dlg.GetDirectory()
            with open(self.project['filepaths']['projfile'], 'w') as fp:
                json.dump(self.project, fp, indent=4, sort_keys=True)
        dlg.Destroy()
        frame.SetTitle('Marxan with Connectivity (Project: '+self.project['filepaths']['projfilename']+')')
	
    def on_save_project( self, event ):
        """
        save a project, but call 'on_save_project_as' if project file has not previously been defined
        """
        if 'projfile' in self.project['filepaths']:
            with open(self.project['filepaths']['projfile'], 'w') as fp:
                json.dump(self.project, fp, indent=4, sort_keys=True)
        else:
            self.on_save_project_as(event=None)

###########################  html pop-up functions ################################

    def on_glossary( self, event ):
        wx.LaunchDefaultBrowser("glossary.html")
	
    def on_tutorial( self, event ):
        wx.LaunchDefaultBrowser("tutorial.html")
	
    def on_github( self, event ):
        wx.LaunchDefaultBrowser("https://github.com/remi-daigle/MarxanConnect/issues")
	
    def on_contributing( self, event ):
        wx.LaunchDefaultBrowser("contributing.html")

    def on_license( self, event ):
        with open('LICENSE', 'r', encoding="utf8") as file :
            filedata = file.read()
        dlg = wx.MessageBox(message = filedata, caption = "Marxan with Connectivity License", style=wx.OK)
        dlg.Destroy()
    
    def on_about( self, event ):
        dlg = wx.MessageBox(message = "Version: v0.0.2\n(C) 2017 Remi Daigle\n", caption = "About Marxan with Connectivity", style=wx.OK)
        dlg.Destroy()

    def on_getting_started( self, event ):
        # insert getting started tab and hyperlinks (wxFormBuilder can't handle hyperlinks)
        frame = getting_started()
        frame.Show()
     
###########################  warning functions ################################
    def warn_dialog(self, message, caption = "Warning!"):
        """
        Warning
        """
        dlg = wx.MessageBox(message, caption, style=wx.OK | wx.ICON_WARNING)
        dlg.Destroy()

###########################  map plotting functions ###########################
    def on_plot_map_button(self, event):
        """
        Initiates map plotting. Creates a 'Plot' tab, plots the basemap (if desired) and calls 'draw_shapefiles' to plot up to 2 other shapefiles
        """
        if not hasattr(self, 'plot'):
            self.plot = wx.Panel(self.m_auinotebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.m_auinotebook1.AddPage(self.plot, u"Plot", False, wx.NullBitmap)
        self.plot.figure = plt.figure()
        self.plot.axes = self.plot.figure.gca()
        self.plot.canvas = FigureCanvas(self.plot, -1, self.plot.figure)
        self.plot.sizer = wx.BoxSizer(wx.VERTICAL)
        self.plot.sizer.Add(self.plot.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.plot.SetSizer(self.plot.sizer)
        self.plot.Fit()
        
        pu = gpd.GeoDataFrame.from_file(self.project['filepaths']['pu_filepath'])
        cu = gpd.GeoDataFrame.from_file(self.project['filepaths']['cu_filepath'])
        
        lonmin, lonmax, latmin, latmax = marxanconpy.buffer_shp_corners([pu,cu],float(self.bmap_buffer.GetValue()))


        self.plot.map = Basemap(llcrnrlon=lonmin, llcrnrlat=latmin, urcrnrlon=lonmax, urcrnrlat=latmax,
                                resolution='i', projection='tmerc', lat_0=(latmin+latmax)/2, lon_0=(lonmin+lonmax)/2)

        #plot basemap
        if(self.bmap_plot_check.GetValue()):
            self.plot.map.drawmapboundary(fill_color=tuple(c/255 for c in self.bmap_oceancol.GetColour()))
            self.plot.map.fillcontinents(color=tuple(c/255 for c in self.bmap_landcol.GetColour()),
                                         lake_color=tuple(c/255 for c in self.bmap_lakecol.GetColour()))
            self.plot.map.drawcoastlines()
        else:
            self.plot.map.drawmapboundary(fill_color='white')
        
        #plot first layer
        if(self.lyr1_plot_check.GetValue()):
            if(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection()==0):
                metric = self.get_metric(type = 'pu')
                self.draw_shapefiles(sf = pu, metric = metric, lowcol = self.pu_metric_lowcol.GetColour(),
                                     hicol = self.pu_metric_hicol.GetColour(), trans = self.pu_metric_alpha.GetValue()/100, legend = self.pu_metric_legend.GetCurrentSelection())
            elif(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection()==1):
                metric = self.get_metric(type = 'cu')
                self.draw_shapefiles(sf = cu, metric = metric, lowcol = self.cu_metric_lowcol.GetColour(),
                                     hicol = self.cu_metric_hicol.GetColour(), trans = self.cu_metric_alpha.GetValue()/100, legend = self.cu_metric_legend.GetCurrentSelection())
            elif(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection()==2):
                self.draw_shapefiles(sf = pu, colour = self.pu_poly_col.GetColour(), trans = self.pu_poly_alpha.GetValue()/100)
            else:
                self.draw_shapefiles(sf = cu, colour = self.cu_poly_col.GetColour(), trans = self.cu_poly_alpha.GetValue()/100)
        
        #plot second layer
        if(self.lyr2_plot_check.GetValue()):
            if(self.lyr2_choice.GetChoiceCtrl().GetCurrentSelection()==0):
                metric = self.get_metric(type = 'pu')
                self.draw_shapefiles(sf = pu, metric = metric, lowcol = self.pu_metric_lowcol1.GetColour(),
                                     hicol = self.pu_metric_hicol1.GetColour(), trans = self.pu_metric_alpha1.GetValue()/100, legend = self.pu_metric_legend1.GetCurrentSelection())
            elif(self.lyr2_choice.GetChoiceCtrl().GetCurrentSelection()==1):
                metric = self.get_metric(type = 'cu')
                self.draw_shapefiles(sf = cu, metric = metric, lowcol = self.cu_metric_lowcol1.GetColour(),
                                     hicol = self.cu_metric_hicol1.GetColour(), trans = self.cu_metric_alpha1.GetValue()/100, legend = self.cu_metric_legend1.GetCurrentSelection())
            elif(self.lyr2_choice.GetChoiceCtrl().GetCurrentSelection()==2):
                self.draw_shapefiles(sf = pu, colour = self.pu_poly_col1.GetColour(), trans = self.pu_poly_alpha1.GetValue()/100)
            else:
                self.draw_shapefiles(sf = cu, colour = self.cu_poly_col1.GetColour(), trans = self.cu_poly_alpha1.GetValue()/100)
        
        #change selection to plot tab
        for i in range(self.m_auinotebook1.GetPageCount()):
            if self.m_auinotebook1.GetPageText(i) == "Plot":
                self.m_auinotebook1.ChangeSelection(i)

    def draw_shapefiles(self, sf, colour = None, trans = None, metric = None, lowcol = None, hicol = None, legend = None):
        """
        Draws the desired shapefile on the plot created by 'on_plot_map_button'
        """
        if(metric==None):
            patches = []
            colour=tuple(c/255 for c in tuple(c/255 for c in colour))
            for poly in sf.geometry:
                mpoly = shapely.ops.transform(self.plot.map, poly)
                patches.append(PolygonPatch(mpoly))
            self.plot.axes.add_collection(PatchCollection(patches, match_original=True, color=colour, alpha=trans))
        else:
            patches = []
            #define colormap
            c1=tuple(c/255 for c in lowcol)
            c2=tuple(c/255 for c in hicol)
            
            seq = [(None,) * 4, 0.0] + list((c1,c2)) + [1.0, (None,) * 4]
            cdict = {'red': [], 'green': [], 'blue': []}
            for i, item in enumerate(seq):
                if isinstance(item, float):
                    r1, g1, b1, a = seq[i - 1]
                    r2, g2, b2, a = seq[i + 1]
                    cdict['red'].append([item, r1, r2])
                    cdict['green'].append([item, g1, g2])
                    cdict['blue'].append([item, b1, b2])
            cmap = matplotlib.colors.LinearSegmentedColormap('CustomMap', cdict)
                    
            norm = matplotlib.colors.Normalize(min(metric), max(metric))
            bins = numpy.linspace(min(metric), max(metric), 10)
            color_producer = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
            for poly, evc in zip(sf.geometry, metric):
                rgba = color_producer.to_rgba(evc)
                mpoly = shapely.ops.transform(self.plot.map, poly)
                patches.append(PolygonPatch(mpoly,color=rgba))
    
            self.plot.axes.add_collection(PatchCollection(patches, match_original=True, alpha=trans))
            if(legend==0):
                self.plot.ax_legend = self.plot.figure.add_axes([0.415, 0.8, 0.2, 0.04], zorder=3)
                self.plot.cb = matplotlib.colorbar.ColorbarBase(self.plot.ax_legend, cmap=cmap, ticks=bins, boundaries=bins, orientation='horizontal')
                self.plot.cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])
            elif(legend==1):
                self.plot.ax_legend = self.plot.figure.add_axes([0.415, 0.15, 0.2, 0.04], zorder=3)
                self.plot.cb = matplotlib.colorbar.ColorbarBase(self.plot.ax_legend, cmap=cmap, ticks=bins, boundaries=bins, orientation='horizontal')
                self.plot.cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])
                

###########################  graph plotting functions #########################
    def on_plot_graph_button(self, event):
        """
        Initiates graph plotting. Creates a 'Plot' tab, and call 'on_draw_graph' to plot the graph
        """
        if not hasattr(self, 'plot'):
            self.plot = wx.Panel(self.m_auinotebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.m_auinotebook1.AddPage(self.plot, u"Plot", False, wx.NullBitmap)
        self.plot.figure = plt.figure()
        self.plot.axes = self.plot.figure.gca()
        self.plot.canvas = FigureCanvas(self.plot, -1, self.plot.figure)
        self.plot.sizer = wx.BoxSizer(wx.VERTICAL)
        self.plot.sizer.Add(self.plot.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.plot.SetSizer(self.plot.sizer)
        self.plot.Fit()
        self.on_draw_graph(pucm_filedir=self.project['filepaths']['pucm_filedir'], pucm_filename=self.project['filepaths']['pucm_filename'])
        for i in range(self.m_auinotebook1.GetPageCount()):
            if self.m_auinotebook1.GetPageText(i) == "Plot":
                self.m_auinotebook1.ChangeSelection(i)
        

    def on_draw_graph(self,pucm_filedir, pucm_filename):
        """
        Draws the desired graph on the plot created by 'on_plot_graph_button'
        """
        pucm_filepath = os.path.join(pucm_filedir, pucm_filename)
        conmat = pandas.read_csv(pucm_filepath, index_col=0)
        g1 = nx.from_numpy_matrix(conmat.as_matrix())
        mapping = dict(zip(g1.nodes(), conmat.index))
        g1 = nx.relabel_nodes(g1, mapping)
        nx.draw_networkx(g1,with_labels=True,edge_color='lightgray')

###########################  file management functions ########################
    def on_PU_file(self, event):
        """
        Defines Planning Unit file path
        """
        self.project['filepaths']['pu_filepath'] = self.PU_file.GetPath()

    def on_CU_file(self, event):
        """
        Defines Connectivity Unit file path
        """
        self.project['filepaths']['cu_filepath']=self.CU_file.GetPath()

    def on_CM_file(self, event ):
        """
        Defines Connectivity Matrix file path
        """
        self.project['filepaths']['cm_filepath'] = self.CM_file.GetPath()

    def on_PUCM_file(self, event):
        """
        Defines Planning Unit scaled Connectivity Matrix file path
        """
        self.project['filepaths']['pucm_filepath'] = self.PUCM_file.GetPath()
        
    def on_FA_file(self, event):
        """
        Defines Focus Areas file path
        """
        self.project['filepaths']['fa_filepath'] = self.FA_file.GetPath()
        
    def on_CF_file(self, event):
        """
        Defines Focus Areas file path
        """
        self.project['filepaths']['cf_filepath'] = self.CF_file.GetPath()
        
    def on_SPEC_file(self, event):
        """
        Defines Focus Areas file path
        """
        self.project['filepaths']['spec_filepath'] = self.SPEC_file.GetPath()
        
    def on_BD_file(self, event):
        """
        Defines Focus Areas file path
        """
        self.project['filepaths']['BD_filepath'] = self.BD_file.GetPath()

###########################  GUI 'wiring' functions ###########################
    def on_rescaleRadioBox(self, event):
        """
        Hides unnecessary options if rescaling is not necessary
        """
        if(self.CU_def.Enabled==True):
            self.CU_def.Enable(enable = False)
            self.CU_filetext.Enable(enable = False)
            self.CU_file.Enable(enable = False)
            self.PUCM_outputtext.Enable(enable = False)
            self.PUCM_def.Enable(enable = False)
            self.PUCM_filetext.Enable(enable = False)
            self.PUCM_file.Enable(enable = False)
            self.rescale_button.Enable(enable = False)
        else:
            self.CU_def.Enable(enable = True)
            self.CU_filetext.Enable(enable = True)
            self.CU_file.Enable(enable = True)
            self.PUCM_outputtext.Enable(enable = True)
            self.PUCM_def.Enable(enable = True)
            self.PUCM_filetext.Enable(enable = True)
            self.PUCM_file.Enable(enable = True)
            self.rescale_button.Enable(enable = True)
            
    def on_rescale_button(self, event):
        """
        Rescales the connectivity matrix to match the scale of the planning units
        """
        threading.Thread(
                marxanconpy.rescale_matrix(self.project['filepaths']['pu_filepath'], self.project['filepaths']['cu_filepath'], self.project['filepaths']['cm_filepath'], self.project['filepaths']['pucm_filepath'])
                ).start()

###########################  metric related functions #########################
    def on_calc_metrics(self, event):
        """
        calculates the selected metrics
        """
        if not 'connectivityMetrics' in self.project:
            self.project['connectivityMetrics']={}
        if not 'spec' in self.project['connectivityMetrics']:
            self.project['connectivityMetrics']['spec']={}
            self.customize_spec.Enable(enable=True)
            
        # choose matrix
        if(self.calc_metrics_type.GetCurrentSelection()==0):
            if(os.path.isfile(self.project['filepaths']['pucm_filepath'])):
                self.conmat = pandas.read_csv(self.project['filepaths']['pucm_filepath'],index_col= 0)
                self.project['connectivityMetrics']['pucm_conmat'] = self.conmat.to_json(orient='split')
            else:
                self.warn_dialog(message="File not found: "+self.project['filepaths']['pucm_filepath'])
            type='pu'
        elif(self.calc_metrics_type.GetCurrentSelection()==1):
            if(os.path.isfile(self.project['filepaths']['pucm_filepath'])):
                self.conmat = pandas.read_csv(self.project['filepaths']['cm_filepath'],index_col= 0)
                self.project['connectivityMetrics']['cm_conmat'] = self.conmat.to_json(orient='split')
            else:
                self.warn_dialog(message="File not found: "+self.project['filepaths']['cm_filepath'])
            type='cu'
            
        #calculate
        if(self.cf_demo_vertex_degree.GetValue()):
            self.project['connectivityMetrics']['spec']['vertexdegree'+type] = marxanconpy.conmat2vertexdegree(self.conmat)

        if(self.cf_demo_between_cent.GetValue()):
            self.project['connectivityMetrics']['spec']['betweencent'+type] = marxanconpy.conmat2betweencent(self.conmat)

        if(self.cf_demo_eig_vect_cent.GetValue()):
            self.project['connectivityMetrics']['spec']['eigvectcent'+type] = marxanconpy.conmat2eigvectcent(self.conmat)

        if(self.cf_demo_self_recruit.GetValue()):
            self.project['connectivityMetrics']['spec']['selfrecruit'+type] = marxanconpy.conmat2selfrecruit(self.conmat)

        if(self.bd_demo_conn_boundary.GetValue()):
            
            self.project['connectivityMetrics']['conn_boundary_dat'] = marxanconpy.conmat2connboundary(self.conmat)
            
    def get_metric(self, type):
        """
        returns the pre-calculated metric for plotting
        """
        #choose metric
        if(type=='pu'):
            metricindex = self.pu_metric_choice.GetCurrentSelection()
        elif(type=='cu'):
            metricindex = self.cu_metric_choice.GetCurrentSelection()

        #get metric
        if(metricindex==0):
            metric = self.project['connectivityMetrics']['spec']['vertexdegree'+type]
        elif(metricindex==1):
            metric = self.project['connectivityMetrics']['spec']['betweencent'+type]
        elif(metricindex==2):
            metric = self.project['connectivityMetrics']['spec']['eigvectcent'+type]
        elif(metricindex==3):
            metric = self.project['connectivityMetrics']['spec']['selfrecruit'+type]
            
        return(metric)

###########################  spec grid popup functions #########################

    def on_customize_spec( self, event ):
        spec_frame=spec_customizer(parent=self)
        spec_frame.keys = list(self.project['connectivityMetrics']['spec'])
        
        for i in range(len(spec_frame.keys)):
            spec_frame.spec_grid.InsertRows(i)
            spec_frame.spec_grid.SetCellValue(i,0,str(i+1))
            spec_frame.spec_grid.SetCellValue(i,1,str(sum(self.project['connectivityMetrics']['spec'][spec_frame.keys[i]])))
            spec_frame.spec_grid.SetCellValue(i,2,str(1000))
            spec_frame.spec_grid.SetCellValue(i,3,spec_frame.keys[i])
            w,h = spec_frame.GetClientSize()
            print(w)
            print(h)
            spec_frame.SetSize((w+16, h+39+20))
            spec_frame.Layout()
        spec_frame.Show()
        

class spec_customizer (gui.spec_customizer):
    def __init__( self, parent ):
        gui.spec_customizer.__init__(self,parent)
        self.parent = parent
        
    def on_spec_ok( self, event ): 
        self.parent.project['spec_dat'] = pandas.DataFrame(numpy.full((self.spec_grid.GetNumberCols(),self.spec_grid.GetNumberRows()),None))
        self.parent.project['spec_dat'].columns = ["id","target","spf","name"]

        for c in range(self.spec_grid.GetNumberCols()):
            for r in range(self.spec_grid.GetNumberRows()):
                self.parent.project['spec_dat'].iloc[r,c] = self.spec_grid.GetCellValue(r,c)
        self.parent.project['spec_dat'] = self.parent.project['spec_dat'].to_json()
        self.Destroy()
	
    def on_spec_cancel( self, event ):
        self.Destroy()

###########################  getting started popup functions #########################
class getting_started(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Marxan with Connectivity: Getting Started",pos = wx.DefaultPosition, size = wx.Size( 900,700 ),style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT)
        self.gettingStarted = wx.Panel(self)
        self.Center()
        # set the icon
        icons = wx.IconBundle()
        for sz in [16, 32, 48, 96, 256]: 
            try: 
                icon = wx.Icon(os.path.join(os.getcwd(),'icon_bundle.ico'), wx.BITMAP_TYPE_ICO, desiredWidth=sz, desiredHeight=sz)
                icons.AddIcon(icon) 
            except: 
                pass 
                self.SetIcons(icons)
        
        startMainSizer = wx.FlexGridSizer( 3, 1, 0, 0 )
        startMainSizer.AddGrowableRow( 0 )
#        startMainSizer.AddGrowableRow( 1 )
#        startMainSizer.AddGrowableRow( 2 )
        startMainSizer.SetFlexibleDirection( wx.VERTICAL )
        startMainSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
        sizer02 = wx.BoxSizer( wx.HORIZONTAL )
		
        self.gettingstartedtxt = wx.StaticText( self.gettingStarted, wx.ID_ANY, u"Welcome to Marxan with Connectivity!\n\nMarxan with Connectivity (henceforth the \"app\") is a Graphical User Interface (GUI) to help conservationists include “connectivity” in their protected area network planning.\n\nThe term \"connectivity\" has a variety of definitions (i.e. larval connectivity, genetic connectivity, landscape connectivity, etc) and protected area networks can be optimized for various connectivity objectives. The app is intended to guide conservationists through the process of identifying important aspects of connectivity for their conservation scenarios as well as highlighting the necessary data.\n\nThe app also includes be a fully functional python module (in progress) that is operated via command line that can be used to reproduce an analysis using the project file generated by the GUI.\n\nTo use this software, please visit the Tutorial and the Glossary which can be accessed under the help menu, or the links below (in progress). Otherwise, if you would just like to get started, please proceed through all the tabs from left to right starting the \"Spatial Input\". After calculating the \"Connectivity Metrics\", you can choose to conduct a Marxan analysis in the app (maybe), export the connectivity metrics for use in a standalone custom Marxan analysis, or you can visualize the Connectivity Metrics using the \"Plotting Options\" tab\n\nIf you would like to report any bugs or request a missing feature, please post an issue on the GitHub repository which is available in the help menu, or the link below.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gettingstartedtxt.Wrap( -1 )
        sizer02.Add( self.gettingstartedtxt, 0, wx.ALL|wx.EXPAND, 5 )
		
        startMainSizer.Add( sizer02, 1, wx.EXPAND, 5 )
		
        hyperlinksizer = wx.BoxSizer( wx.VERTICAL )
        self.tutoriallink = wx.adv.HyperlinkCtrl( self.gettingStarted, wx.ID_ANY, u"Tutorial", u"tutorial.html", wx.DefaultPosition, wx.DefaultSize)
        hyperlinksizer.Add( self.tutoriallink, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    		
        self.glossarylink = wx.adv.HyperlinkCtrl( self.gettingStarted, wx.ID_ANY, u"Glossary", u"glossary.html", wx.DefaultPosition, wx.DefaultSize)
        hyperlinksizer.Add( self.glossarylink, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    		
        self.githublink = wx.adv.HyperlinkCtrl( self.gettingStarted, wx.ID_ANY, u"GitHub Issues", u"https://github.com/remi-daigle/MarxanConnect/issues", wx.DefaultPosition, wx.DefaultSize)
        hyperlinksizer.Add( self.githublink, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        startMainSizer.Add( hyperlinksizer, 1, wx.EXPAND, 5 )
        
        iconsizer = wx.BoxSizer( wx.VERTICAL )
		
        self.m_bitmap1 = wx.StaticBitmap( self.gettingStarted, wx.ID_ANY, wx.Bitmap( u"icon_bundle.ico", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        iconsizer.Add( self.m_bitmap1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
        startMainSizer.Add( iconsizer, 1, wx.EXPAND, 5 )
        
        self.gettingStarted.SetSizer( startMainSizer )
        self.gettingStarted.Layout()
        startMainSizer.Fit( self.gettingStarted )        



###############################################################################################################################
###########################  run the GUI ######################################
app = wx.App(False)
 
#create an object of CalcFrame
frame = MarxanConnectGUI(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()

#stop the app
app.Destroy()
