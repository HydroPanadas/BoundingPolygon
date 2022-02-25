from tkinter import *
from idlelib.ToolTip import *
from tkinter import ttk
from tkinter import filedialog
from os import mkdir, chdir, listdir, path, walk, startfile, getcwd, rename
import subprocess as S


owd = getcwd()
Caris = ('C:/Program Files/CARIS/BASE Editor/4.4/bin')
QGIS = ('')
GRASS = ('')


class Application(Frame):

    def __init__(self, master):
        """ Initialize the Frames for Application """

        Frame.__init__(self, master)
        self.grid()
        self.app_widgets()

    def Search_CSAR_Dir(self):
        """This Function allows the user to choose the
        Surfaces dir, then updates the
        Surfaces dir entry box with the selected path"""

        csar = self.CSAR_DIR.get()

        Csar_dir= filedialog.askdirectory(initialdir = csar, title='Select Surface directory ')
        self.CSAR_DIR.set(str(Csar_dir))
        tip_CSAR = ToolTip(self.CSAR_dir, (self.CSAR_DIR.get()))

    def app_widgets(self):

        ## Create Main Menu Bar
        menu.add_cascade(label = "File", menu = submenu)


        ## Help Submenu
        submenu.add_command(label = "Help", command = self.Help)

        ## Close Submenu
        submenu.add_command(label = "Close Application", command = self.close)

        ## Process Data
        self.Button_P = Button(self, text="RUN", height=0,
                                   command=self.Polygon_Tools)
        self.Button_P.grid(row=0, column=2, sticky=W, padx=2)

        self.Polygon_Tools = LabelFrame(self, text="Downsize Res, Export Geotiff", foreground="blue")
        self.Polygon_Tools.grid(row=0, column=0, sticky=W)

        self.CSAR_DIR = StringVar()
        self.CSAR_dir = Entry(self.Polygon_Tools, width=32, textvariable=self.CSAR_DIR)
        self.CSAR_dir_text = Label(self.Polygon_Tools, text="CSAR Folder")
        self.CSAR_dir_text.grid(row=0, column=0, sticky=W)
        self.CSAR_dir.grid(row=0, column=1, sticky=W)
        self.ButtonCSAR= Button(self.Polygon_Tools, text="...", height=0,
                                command=self.Search_CSAR_Dir)
        self.ButtonCSAR.grid(row=0, column=2, sticky=W, padx=2)

##        self.GRID_METH = StringVar()
##        grid_meth = ['BASIC',
##                     'TPU',
##                     'SHOAL',
##                     'SHOAL_TRUE']
##
##        self.GRID_METH_op = ttk.Combobox(self.Polygon_Tools, values=grid_meth, width=32, textvariable=self.GRID_METH)
##        self.GRID_METH_text = Label(self.Polygon_Tools, text="Choose Gridding Method")
##        self.GRID_METH_text.grid(row=1, column=0, sticky=W)
##        self.GRID_METH_op.grid(row=1, column=1, sticky=W+E, padx=0)

        self.GRID_RES = StringVar()
        self.GRID_res = Entry(self.Polygon_Tools, width=5, textvariable=self.GRID_RES)
        self.GRID_res_text = Label(self.Polygon_Tools, text="Gridding Resolution")
        self.GRID_res_text.grid(row=2, column=0, sticky=W)
        self.GRID_res.grid(row=2, column=1, sticky=W)


        
    def Polygon_Tools(self):
        """ This Function runs processing steps based on user inputs"""

        CSARS = self.CSAR_DIR.get()
        Gridding_Method = 'SHOAL'
        ListCSAR = listdir(CSARS)
        Gridding_Resolution = self.GRID_RES.get()
    

        with open("Downsize_Export.bat", "w") as Import:
                Import.write('@ECHO OFF' + '\n')
                Import.write('cd '+ Caris + '\n')
                Import.write('@ECHO Downsizing Surface Resolutions and Exporting Geotiffs' + '\n')

                for file in ListCSAR:
                    if file.endswith(".csar"):
                        File_Name = file.replace(".csar", "")
                        Import.write('carisbatch --run ImportPoints --input-format CSAR' +
                                     ' --gridding-method ' + str(Gridding_Method) +
                                     ' --resolution ' + Gridding_Resolution + 'm' +
                                     ' --include-band ALL ' + CSARS + '/' + file +
                                     '  ' + CSARS + '/'  + File_Name +
                                     '_' + str(Gridding_Resolution) + 'm.csar'+ '\n')
                        Import.write('carisbatch --run ExportRaster  --output-format GEOTIFF --include-band Depth ' +
                                      CSARS + '/' + file +  ' '  + CSARS + '/'  + File_Name +
                                     '_' + str(Gridding_Resolution) + 'm.tiff' + '\n')

        p = S.check_call("Downsize_Export.bat", stdin=None, stdout=None, stderr=None, shell=False)
                                    

    def Help(self):
        return

    def close(self):
        self.Exit = 'True'

root = Tk()
root.title("Downsize/Export Geotiffs")
root.geometry("500x100")
menu = Menu(root)
root.config(menu=menu)
submenu = Menu(menu)
app = Application(root)
root.mainloop()
