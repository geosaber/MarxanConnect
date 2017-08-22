#importing wx files
import wx
import wx.lib.agw.aui as aui

#import the newly created GUI file
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
import sys
import pandas
import numpy
import networkx as nx
import threading

# import MarxanConnectPy from https://github.com/remi-daigle/MarxanConnectPy
# MarxanConnectPy and MarxanConnectGUI must be in the same folder (i.e. Github/MarxanConnectPy/ and Github/MarxanConnectGUI/)
sys.path.append('../MarxanConnectPy/')
import marxanconpy

# define current working directory
cwd = os.getcwd()


#inherit from the MainFrame created in wxFowmBuilder and create CalcFrame
class MarxanConnectGUI(gui.MarxanConnectGUI):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        gui.MarxanConnectGUI.__init__(self,parent)
        icons = wx.IconBundle()
        for sz in [16, 32, 48, 96, 256]: 
            try: 
                icon = wx.Icon(os.path.join(cwd,'icon_bundle.ico'), wx.BITMAP_TYPE_ICO, desiredWidth=sz, desiredHeight=sz)
                icons.AddIcon(icon) 
            except: 
                pass 
                self.SetIcons(icons)

        # set default file paths

        if(os.path.isdir(os.path.join(os.environ['ProgramFiles(x86)'], "MarxanConnect"))):
            pfdir = os.path.join(os.environ['ProgramFiles(x86)'], "MarxanConnect")
        else:
            pfdir = os.path.join(os.environ['ProgramFiles'], "MarxanConnect")

        self.pu_filepath = os.path.join(pfdir,"data","shapefiles","marxan_pu.shp")
        self.cu_filepath = os.path.join(pfdir,"data","shapefiles","connectivity_grid.shp")
        self.cm_filepath = os.path.join(pfdir,"data","grid_connectivity_matrix.csv")
        self.pucm_filename = self.PUCM_filename.GetLabelText()
        self.pucm_filedir = os.path.join(os.environ['USERPROFILE'], "My Documents")



    def on_plot_map_button(self, event):
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
        
        pu = gpd.GeoDataFrame.from_file(self.pu_filepath)
        cu = gpd.GeoDataFrame.from_file(self.cu_filepath)
        
        
        lonmin, lonmax, latmin, latmax = marxanconpy.buffer_shp_corners([pu,cu],1)


        self.plot.map = Basemap(llcrnrlon=lonmin, llcrnrlat=latmin, urcrnrlon=lonmax, urcrnrlat=latmax,
                                resolution='i', projection='tmerc', lat_0=(latmin+latmax)/2, lon_0=(lonmin+lonmax)/2)

        #plot basemap
        if(self.bmap_plot_check.GetValue()):
            self.plot.map.drawmapboundary(fill_color=tuple(c/255 for c in self.bmap_oceancol.GetColour()))
            self.plot.map.fillcontinents(color=tuple(c/255 for c in self.bmap_landcol.GetColour()), lake_color=tuple(c/255 for c in self.bmap_lakecol.GetColour()))
            self.plot.map.drawcoastlines()
        else:
            self.plot.map.drawmapboundary(fill_color='white')
        
        #plot first layer
        if(self.lyr1_plot_check.GetValue()):
            if(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection()==0):
                self.draw_shapefiles(sf = pu, metric = self.connectivityMetrics.eigvectcent,lowcol = self.pu_metric_lowcol.GetColour(), hicol = self.pu_metric_hicol.GetColour(), trans = self.pu_poly_alpha.GetValue()/100)
            elif(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection()==1):
                #metric = self.cu_metric_choice.GetCurrentSelection()
                self.draw_shapefiles(sf = cu, metric = self.connectivityMetrics.eigvectcent,lowcol = self.cu_metric_lowcol.GetColour(), hicol = self.cu_metric_hicol.GetColour(), trans = self.cu_poly_alpha.GetValue()/100)
            elif(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection()==2):
                self.draw_shapefiles(sf = pu, colour = self.pu_poly_col.GetColour(), trans = self.pu_poly_alpha.GetValue()/100)
            else:
                self.draw_shapefiles(sf = cu, colour = self.cu_poly_col.GetColour(), trans = self.cu_poly_alpha.GetValue()/100)
        
        #plot second layer
        if(self.lyr2_plot_check.GetValue()):
            if(self.lyr2_choice.GetChoiceCtrl().GetCurrentSelection()==0):
                self.draw_shapefiles(sf = pu, metric = self.connectivityMetrics.eigvectcent,lowcol = self.pu_metric_lowcol1.GetColour(), hicol = self.pu_metric_hicol1.GetColour(), trans = self.pu_poly_alpha1.GetValue()/100)
            elif(self.lyr2_choice.GetChoiceCtrl().GetCurrentSelection()==1):
                #metric = self.cu_metric_choice.GetCurrentSelection()
                self.draw_shapefiles(sf = cu, metric = self.connectivityMetrics.eigvectcent,lowcol = self.cu_metric_lowcol1.GetColour(), hicol = self.cu_metric_hicol1.GetColour(), trans = self.cu_poly_alpha1.GetValue()/100)
            elif(self.lyr2_choice.GetChoiceCtrl().GetCurrentSelection()==2):
                self.draw_shapefiles(sf = pu, colour = self.pu_poly_col1.GetColour(), trans = self.pu_poly_alpha1.GetValue()/100)
            else:
                self.draw_shapefiles(sf = cu, colour = self.cu_poly_col1.GetColour(), trans = self.cu_poly_alpha1.GetValue()/100)
        
        #change selection to plot tab
        for i in range(self.m_auinotebook1.GetPageCount()):
            if self.m_auinotebook1.GetPageText(i) == "Plot":
                self.m_auinotebook1.ChangeSelection(i)

    def on_plot_graph_button(self, event):
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
        self.on_draw_graph(pucm_filedir=self.pucm_filedir, pucm_filename=self.pucm_filename)
        for i in range(self.m_auinotebook1.GetPageCount()):
            if self.m_auinotebook1.GetPageText(i) == "Plot":
                self.m_auinotebook1.ChangeSelection(i)

    def draw_shapefiles(self, sf, colour = None, trans = 0.5, metric = None, lowcol = None, hicol = None):
        print(lowcol)
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
                    
            #cmap = matplotlib.cm.get_cmap('OrRd')
            norm = matplotlib.colors.Normalize(min(metric), max(metric))
            bins = numpy.linspace(min(metric), max(metric), 10)
            color_producer = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
            for poly, evc in zip(sf.geometry, metric):
                rgba = color_producer.to_rgba(evc)
                mpoly = shapely.ops.transform(self.plot.map, poly)
                patches.append(PolygonPatch(mpoly,color=rgba))
    
            self.plot.axes.add_collection(PatchCollection(patches, match_original=True, alpha=trans))
            self.plot.ax_legend = self.plot.figure.add_axes([0.415, 0.15, 0.2, 0.04], zorder=3)
            self.plot.cb = matplotlib.colorbar.ColorbarBase(self.plot.ax_legend, cmap=cmap, ticks=bins, boundaries=bins, orientation='horizontal')
            self.plot.cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])


        

    def on_draw_graph(self,pucm_filedir, pucm_filename):
        pucm_filepath = os.path.join(pucm_filedir, pucm_filename)
        conmat = pandas.read_csv(pucm_filepath, index_col=0)
        g1 = nx.from_numpy_matrix(conmat.as_matrix())
        mapping = dict(zip(g1.nodes(), conmat.index))
        g1 = nx.relabel_nodes(g1, mapping)
        nx.draw_networkx(g1,with_labels=True,edge_color='lightgray')

        
    def on_PU_file( self, event ):
        self.pu_filepath = self.PU_file.GetPath()
        print(self.pu_filepath)

    def on_rescaleRadioBox(self, event):
        if(self.CU_def.Hide()==True):
            self.CU_def.Hide()
            self.CU_filetext.Hide()
            self.CU_file.Hide()
        else:
            self.CU_def.Show()
            self.CU_filetext.Show()
            self.CU_file.Show()

    def on_CU_file(self, event):
        self.cu_filepath=self.CU_file.GetPath()
        print(self.cu_filepath)

    def on_CM_file( self, event ):
        self.cm_filepath = self.CM_file.GetPath()
        print(self.cm_filepath)

    def on_PUCM_filedir(self, event):
        self.pucm_filedir=self.PUCM_filedir.GetPath()
        print(self.pucm_filedir)

    def on_PUCM_filenameTextEnter(self, event):
        self.pucm_filename = self.PUCM_filenameTextEnter.GetPath()
        print(self.pucm_filename)

    def on_rescale_button(self, event):
        print(self.pu_filepath, self.cu_filepath, self.cm_filepath, self.pucm_filedir, self.pucm_filename)
        threading.Thread(marxanconpy.rescale_matrix(self.pu_filepath, self.cu_filepath, self.cm_filepath, self.pucm_filedir, self.pucm_filename)).start()

        print("rescaling!")

    def on_calc_metrics(self, event):
        self.pucm_filepath = os.path.join(self.pucm_filedir, self.pucm_filename)
        if self.ct_demo_vertex_degree.GetValue():
            self.connectivityMetrics.vertexdegree = marxanconpy.conmat2vertexdegree(self.pucm_filepath)

        if self.ct_demo_between_cent.GetValue():
            self.connectivityMetrics.betweencent = marxanconpy.conmat2betweencent(self.pucm_filepath)

        if self.ct_demo_eig_vect_cent.GetValue():
            self.connectivityMetrics.eigvectcent = marxanconpy.conmat2eigvectcent(self.pucm_filepath)

        if self.ct_demo_self_recruit.GetValue():
            self.connectivityMetrics.selfrecruit = marxanconpy.conmat2selfrecruit(self.pucm_filepath)

        if self.bd_demo_conn_boundary.GetValue():
            self.connectivityMetrics.conmat = pandas.read_csv(os.path.join(self.pucm_filedir, self.pucm_filename))
            self.connectivityMetrics.boundary_dat = self.connectivityMetrics.conmat.melt(id_vars=['puID'])
            self.connectivityMetrics.boundary_dat.columns = ['id1', 'id2', 'boundary']
            
    def testcolourbox(self, event):
        print(self.lyr1_choice.GetChoiceCtrl().GetCurrentSelection())

app = wx.App(False)
 
#create an object of CalcFrame
frame = MarxanConnectGUI(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()

#make; echo "testing exemake"; ./dist/MarxanConnectGUI/MarxanConnectGUI.exe