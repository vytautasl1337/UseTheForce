import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import scipy.io as sio
import os,numpy,os.path
from collections import defaultdict
import matplotlib.pyplot as plt

class singleForceUser(tk.Toplevel):
    #-----------------------------------#
    from functions.plots.saveFig import saveFig
    from functions.conditions.high_reward import highR
    from functions.conditions.low_reward import lowR
    from functions.conditions.males import on_males
    from functions.conditions.females import on_females
    from functions.conditions.all_grips_clust import all_grips_clust
    from functions.conditions.all_grips import all_grips
    from functions.conditions.ITIs import plotITI
    from functions.plots.plot_runs import plotRuns
    from functions.conditions.happy import happy_emo
    from functions.conditions.sad import sad_emo
    from functions.conditions.neutral import neutral_emo
    from functions.getVars import getVar
    #-----------------------------------#
    def __init__(self, parent):
        self.getVar(exp_info,folder_single)
        global fig
        super().__init__(parent)
        self.title('Single subject analysis')
        self.resizable(width=True, height=True)
        self.original_frame = parent
        self.attributes('-fullscreen',True)
        ###################################
        self.info_frame = ttk.LabelFrame(self, text = 'Participant info', height = 100)
        self.info_frame.pack(side='top', fill='both',padx=20, pady=10)
        self.sbj_info = ["Directory: ", "Subject ID: ", "Age: ", "Sex: ", "Errors: ", "Reward: "]
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="lime")
        style.configure('BW.TButton', foreground = "grey")
        style.map('BW.TButton',
                foreground=[('disabled', 'grey'),
                            ('!disabled', 'white')])

        self.label1=ttk.Label(self.info_frame, text=self.sbj_info[0], style = "BW.TLabel",font =50)
        self.label1.grid(row=0, column = 0, padx=10, pady=30, sticky="nsew")
        self.label1=ttk.Label(self.info_frame, text=("/".join(folder_single.split('/')[-3:])), font =50)
        self.label1.grid(row=0, column = 1, padx=30, pady=30, sticky="nsew")

        self.label1=ttk.Label(self.info_frame, text=self.sbj_info[1], style = "BW.TLabel",font =50)
        self.label1.grid(row=0, column = 2, padx=10, pady=30, sticky="nsew")
        self.label1=ttk.Label(self.info_frame, text=(str(exp_info['ParticipantID']).strip("['']")),font =50)
        self.label1.grid(row=0, column = 3, padx=30, pady=30, sticky="nsew")

        self.label1=ttk.Label(self.info_frame, text=self.sbj_info[2], style = "BW.TLabel",font =50)
        self.label1.grid(row=0, column = 4, padx=30, pady=30, sticky="nsew")
        self.label1=ttk.Label(self.info_frame, text=int(exp_info['Age']),font =50)
        self.label1.grid(row=0, column = 5, padx=30, pady=30, sticky="nsew")

        self.label1=ttk.Label(self.info_frame, text=self.sbj_info[3], style = "BW.TLabel",font =50)
        self.label1.grid(row=0, column = 6, padx=30, pady=30, sticky="nsew")
        self.label1=ttk.Label(self.info_frame, text=(str(exp_info['Gender']).strip("['']")),font =50)
        self.label1.grid(row=0, column = 7, padx=30, pady=30, sticky="nsew")

        self.label1=ttk.Label(self.info_frame, text=self.sbj_info[4], style = "BW.TLabel",font =50)
        self.label1.grid(row=0, column = 8, padx=30, pady=30, sticky="nsew")
        self.label1=ttk.Label(self.info_frame, 
            text=numpy.squeeze(numpy.column_stack(merged_data['Correct'])).size-numpy.count_nonzero(numpy.squeeze(numpy.column_stack(merged_data['Correct']))),font =50)
        self.label1.grid(row=0, column = 9, padx=30, pady=30, sticky="nsew")

        self.label1=ttk.Label(self.info_frame, text=self.sbj_info[5], style = "BW.TLabel",font =50)
        self.label1.grid(row=0, column = 10, padx=30, pady=30, sticky="nsew")
        self.label1=ttk.Label(self.info_frame, text=(numpy.squeeze(numpy.column_stack(merged_data['Money_after_run'])))[-1],font =50)
        self.label1.grid(row=0, column = 11, padx=30, pady=30, sticky="nsew")
        #####################################

        self.plot_frame = ttk.LabelFrame(self, text = 'Output', height = 800, width=1420)
        self.plot_frame.pack(side='right', fill='both',padx=20, pady=10)
        self.widgets_frame = ttk.LabelFrame(self, text='Quality check',padding=(20,10), height = 200)
        self.widgets_frame.pack(side='top', fill='x',padx=20, pady=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side='top',fill='x',padx=20,pady=0)
        self.grip_frame = ttk.Frame(self.notebook,padding=(20,10), height = 200)
        #self.grip_frame.pack(side='top', fill='x',padx=20, pady=20)
        self.notebook.add(self.grip_frame, text="Grip conditions")
        self.tab_2 = ttk.Frame(self.notebook,padding=(20,10), height = 200)
        self.notebook.add(self.tab_2, text="Event contrasts")

        self.close_frame = ttk.LabelFrame(self, text='Options',padding=(20,10), height = 200)
        self.close_frame.pack(side='top', fill='x',padx=20, pady=10)
        self.tool_frame = ttk.LabelFrame(self, text='Toolbar',padding=(20,10), height = 100)
        self.tool_frame.pack(side='top', fill='x',padx=20, pady=10)

        self.button = ttk.Button(self.widgets_frame, text="Runs",command = lambda: self.plotRuns(exp_info,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.widgets_frame, text="Average ITIs", command = lambda: self.plotITI(merged_data,exp_info,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.widgets_frame, text="Grip responses", command = lambda: self.all_grips(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.widgets_frame, text="Clustered responses", command = lambda: self.all_grips_clust(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #TAB1
        self.button = ttk.Button(self.grip_frame, text="High reward", width = 33, command = lambda: self.highR(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.grip_frame, text="Low reward", width = 33, command = lambda: self.lowR(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.grip_frame, text="Sad faces", width = 33, command = lambda: self.sad_emo(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.grip_frame, text="Neutral faces", width = 33, command = lambda: self.neutral_emo(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.grip_frame, text="Happy faces", width = 33, command = lambda: self.happy_emo(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.grip_frame, text="Male faces", width = 33, command = lambda: self.on_males(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        self.button = ttk.Button(self.grip_frame, text="Female faces", width = 33, command = lambda: self.on_females(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
        #TAB2
        self.combo_list1 = ["--", "High reward", "Low reward", "Sad faces", "Happy faces", "Neutral faces", "Male faces", "Female faces"]
        self.contrast1 = ttk.Combobox(
            self.tab_2, state="readonly", values=self.combo_list1,width=1
        )
        self.contrast1.current(0)
        self.contrast1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.contrast2 = ttk.Combobox(
            self.tab_2, state="readonly", values=self.combo_list1, width=1
        )
        self.contrast2.current(0)
        self.contrast2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.combo_list2 = ["Reaction time", "Area under the curve", "Acceleration", "Max peak"]
        self.contrast3 = ttk.Combobox(
            self.tab_2, state="readonly", values=self.combo_list2, width=20
        )
        self.contrast3.current(0)
        self.contrast3.grid(row=1, column=0, columnspan = 2, padx=10, pady=10, sticky="nsew")

        self.button = ttk.Button(self.tab_2, text="Plot", width = 33, command = lambda: self.highR(merged_data,left,right,times,list_of_blocks,runs,fig))
        self.button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        self.button = ttk.Button(self.close_frame, text="Back", command = self.onBack)
        self.button.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")

        self.button = ttk.Button(self.close_frame, text="Close", command = root.destroy)
        self.button.grid(row=1, column=1, padx=30, pady=10, sticky="nsew")

        self.button_save = ttk.Button(self.close_frame, text="Save figure", command = lambda: self.saveFig(plt), state='disabled', style='BW.TButton')
        self.button_save.grid(row=0, column=1, padx=30, pady=10, sticky="nsew")

        self.button = ttk.Button(self.close_frame, text="Export events", command = lambda: self.getVar(exp_info,folder_single))
        self.button.grid(row=0, column=0, padx=30, pady=10, sticky="nsew")


    def onBack(self):
        self.destroy()
        self.original_frame.show()
        
class groupForceUser(tk.Toplevel):
    #-----------------------------------#
    from functions.plots.saveFig import saveFig
    from functions.conditions.high_reward import highR
    from functions.conditions.low_reward import lowR
    from functions.conditions.males import on_males
    from functions.conditions.females import on_females
    from functions.conditions.all_grips_clust import all_grips_clust
    from functions.conditions.all_grips import all_grips
    from functions.conditions.ITIs import plotITI
    from functions.plots.plot_runs import plotRuns
    from functions.conditions.happy import happy_emo
    from functions.conditions.sad import sad_emo
    from functions.conditions.neutral import neutral_emo
    from functions.getVars_group import getVar_group
    #-----------------------------------#
    def __init__(self, parent):
        self.getVar_group(folder_group) 
      
class USETHEFORCE_App(ttk.Frame):
        def __init__(self):
            super().__init__()
            ttk.Frame.__init__(self)

            for index in [0, 1, 2]:
                self.columnconfigure(index=index, weight=1)
                self.rowconfigure(index=index, weight=1)
            self.setup_widgets()
            
        def setup_widgets(self):
            style = ttk.Style()
            style.configure('TButton', font =
                ('calibri', 12, 'bold'),
                    borderwidth = '2')
            style.map('TButton', foreground = [('active', '!disabled', 'cyan')])

            self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
            self.widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
            self.widgets_frame.columnconfigure(index=0, weight=1)

            # Label
            self.label = ttk.Label(self.widgets_frame,text="USE THE FORCE\n"
                                                            "toolbox",justify="center",font=("-size", 15, "-weight", "bold"),)
            self.label.grid(row=1, column=0, pady=10, columnspan=2)
            
            # Button
            self.button = ttk.Button(self.widgets_frame, text="Load individual data", style = 'W.TButton', width = 30, command = self.browse_single)
            self.button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
            # Button
            self.button = ttk.Button(self.widgets_frame, text="Load group data", style = 'W.TButton', width = 30, command = self.browse_group)
            self.button.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
            # Button
            self.button = ttk.Button(self.widgets_frame, text="Close", width = 30, command = root.destroy)
            self.button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        
        def hide(self):
            root.withdraw()

        def browse_single(self):
            global folder_single, merged_data, exp_info, runs, left, right, times, list_of_blocks, fig
            folder_single = filedialog.askdirectory(title = 'Select a single subject folder')
            if (len(folder_single) == 0): 
                print('No folder selected')
            else:
                print('Folder selected: ',folder_single)
                data,exp_info = [],[]
                for file in sorted(os.listdir(folder_single)):
                    if file.endswith('.mat'):
                        print('Loading data from: ',folder_single+'/'+file)
                        if file.startswith('data'):
                            data.append(sio.loadmat((folder_single+'/'+file)))
                        elif file.startswith('ExpInfo'):
                            exp_info=sio.loadmat((folder_single+'/'+file))
                merged_data = defaultdict(list)
                for d in data:
                    for k, v in d.items():
                        merged_data[k].append(v)
                runs=int(exp_info['Runs'])
                left = numpy.squeeze(numpy.column_stack(merged_data['Block_data_left']))
                right = numpy.squeeze(numpy.column_stack(merged_data['Block_data_right']))
                times = numpy.squeeze(numpy.column_stack(merged_data['Block_time']))
                list_of_blocks = [x for x in range(int(runs*exp_info['Blocks_in_run'])) if x % int(exp_info['Blocks_in_run']) == 0]
                list_of_blocks.append(int(numpy.shape(left)[0]))
                fig = None
                self.hide()
                singleForceUser(self)

        def browse_group(self):
            global folder_group
            folder_group = filedialog.askdirectory(title = 'Select source folder')
            if (len(folder_group) == 0):
                print('No folder selected')
            else:
                print('Folder selected: ',folder_group)
                self.hide()
                groupForceUser(self)
            #return folder_group, data
        
        def show(self):
            root.update()
            root.deiconify()
            
     
if __name__ == "__main__":
    #ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    load= Image.open("pic.jpg")
    load1=load.resize((280, 200), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load1)
    img = tk.Label(root,image=render)
    img.pack()

    #root.iconbitmap('circuit.ico')

    root.title("UTF Toolbox")
    root.resizable(width=False, height=False)

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = USETHEFORCE_App()
    app.pack(fill="both", expand=True)
    app.pack_propagate(False)
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    root.mainloop()