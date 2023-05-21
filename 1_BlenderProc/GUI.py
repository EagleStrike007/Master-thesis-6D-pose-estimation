import tkinter as tk
from tkinter import *
from tkinter import TclError, ttk, messagebox, filedialog
from tkinter.filedialog import askopenfilename
import numpy as np
import os
import subprocess
import pickle


class Window():

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Programma')
        self.root.geometry("1000x700")
        self.root.resizable(0, 0)
        try:
            # windows only (remove the minimize/maximize button)
            self.root.attributes('-toolwindow', True)
        except TclError:
            print('Not supported on your platform')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.init_var()

        tk.Label(self.root, text="BlenderProc Setup", font=('Arial bold', 24))\
            .grid(column=0, row=0, columnspan=3, sticky=tk.W+tk.E)

        frame_1_1 = self.place_background_inputs(self.root)
        frame_1_2 = self.place_point_light_inputs(self.root)
        frame_1_3 = self.place_camera_run_inputs(self.root)
        frame_2 = self.place_path_inputs(self.root)
        frame_3 = self.place_start_blendeproc(self.root)
        frame_1_1.grid(column=0, row=1)
        frame_1_2.grid(column=1, row=1)
        frame_1_3.grid(column=2, row=1)
        frame_2.grid(column=0, row=2, columnspan=3, sticky=tk.W)
        frame_3.grid(column=0, row=3, columnspan=3, sticky=tk.W)

        for widget in self.root.winfo_children():
            widget.grid(padx=5, pady=5)

        self.root.mainloop()

    @staticmethod
    def callback(self, input):
        if input == "":
            return True
        try:
            float(input)
            return True
        except ValueError:
            return False

    def place_background_inputs(self, container):
        frame = ttk.Frame(container)

        tk.Label(frame, text="Background", font=('Arial bold', 14)).grid(column=0, row=1, sticky=tk.W)
        tk.Label(frame, text="Lenght side:").grid(column=0, row=2, sticky=tk.E)

        reg = frame.register(self.callback)
        self.entry_it = tk.Entry(frame, textvariable=self.var_BG_it)
        self.entry_it.config(validate="all", validatecommand=(reg, '%P'))

        tk.Checkbutton(frame, text='Use background', variable=self.var_BG_Use, onvalue=1, offvalue=0)\
            .grid(column=0, row=3, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame, text='Change background', variable=self.var_BG, onvalue=1, offvalue=0, command=lambda:\
            self.enable_entry(self.entry_it, self.var_BG)).grid(column=0, row=4, columnspan=1, sticky=tk.W)
        tk.Checkbutton(frame, text='Change ground plane', variable=self.var_BG_GP, onvalue=1, offvalue=0)\
            .grid(column=0, row=5, columnspan=2, sticky=tk.W)

        tk.Label(frame, text="Color plane", font=('Arial bold', 14)).grid(column=0, row=6, sticky=tk.W)
        tk.Label(frame, text="Min intensity:").grid(column=0, row=7, sticky=tk.E)
        tk.Label(frame, text="Max intensity:").grid(column=0, row=8, sticky=tk.E)
        tk.Label(frame, text="Color 1:").grid(column=0, row=9, sticky=tk.E)
        tk.Label(frame, text="Color 2:").grid(column=0, row=10, sticky=tk.E)

        # padding
        tk.Label(frame, text="").grid(column=0, row=11, sticky=tk.E)
        tk.Label(frame, text="").grid(column=0, row=12, sticky=tk.E)

        e1 = tk.Entry(frame, textvariable=self.var_side)
        e2 = tk.Entry(frame, textvariable=self.var_LP_min_int)
        e3 = tk.Entry(frame, textvariable=self.var_LP_max_int)
        e4 = tk.Entry(frame, textvariable=self.var_LP_color_1)
        e5 = tk.Entry(frame, textvariable=self.var_LP_color_2)

        e1.grid(column=1, row=2, sticky=tk.W + tk.E)
        e2.grid(column=1, row=7, sticky=tk.W + tk.E)
        e3.grid(column=1, row=8, sticky=tk.W + tk.E)
        e4.grid(column=1, row=9, sticky=tk.W + tk.E)
        e5.grid(column=1, row=10, sticky=tk.W + tk.E)

        e1.config(validate="all", validatecommand=(reg, '%P'))
        e2.config(validate="all", validatecommand=(reg, '%P'))
        e3.config(validate="all", validatecommand=(reg, '%P'))
        e4.config(validate="all", validatecommand=(reg, '%P'))
        e5.config(validate="all", validatecommand=(reg, '%P'))

        for widget in self.root.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def place_point_light_inputs(self, container):
        frame = ttk.Frame(container)

        tk.Label(frame, text="Point light", font=('Arial bold', 14)).grid(column=0, row=1, sticky=tk.W)
        tk.Label(frame, text="Max intensity:").grid(column=0, row=2, sticky=tk.E)
        tk.Label(frame, text="Min intensity:").grid(column=0, row=3, sticky=tk.E)
        tk.Label(frame, text="Max elevation:").grid(column=0, row=4, sticky=tk.E)
        tk.Label(frame, text="Min elevation:").grid(column=0, row=5, sticky=tk.E)

        # padding
        tk.Label(frame, text="").grid(column=0, row=9, sticky=tk.E)
        tk.Label(frame, text="").grid(column=0, row=11, sticky=tk.E)

        reg = frame.register(self.callback)
        e1 = tk.Entry(frame, textvariable=self.var_PL_max_int)
        e2 = tk.Entry(frame, textvariable=self.var_PL_min_int)
        e3 = tk.Entry(frame, textvariable=self.var_PL_max_ele)
        e4 = tk.Entry(frame, textvariable=self.var_PL_min_ele)

        e1.grid(column=1, row=2, sticky=tk.W + tk.E)
        e2.grid(column=1, row=3, sticky=tk.W + tk.E)
        e3.grid(column=1, row=4, sticky=tk.W + tk.E)
        e4.grid(column=1, row=5, sticky=tk.W + tk.E)

        e1.config(validate="all", validatecommand=(reg, '%P'))
        e2.config(validate="all", validatecommand=(reg, '%P'))
        e3.config(validate="all", validatecommand=(reg, '%P'))
        e4.config(validate="all", validatecommand=(reg, '%P'))

        tk.Checkbutton(frame, text='Random placing', variable=self.var_PL_placing, onvalue=1, offvalue=0)\
            .grid(column=0, row=6, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame, text='Random intensity', variable=self.var_PL_intensity, onvalue=1, offvalue=0)\
            .grid(column=0, row=7, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame, text='Random color', variable=self.var_PL_color, onvalue=1, offvalue=0)\
            .grid(column=0, row=8, columnspan=2, sticky=tk.W)

        tk.Checkbutton(frame, text='Project ground', variable=self.var_R_proj, onvalue=1, offvalue=0,\
                       command=lambda: self.enable_entry2(self.var_R_proj)).grid(column=0, row=10, columnspan=2, sticky=tk.W)

        for widget in self.root.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def place_camera_run_inputs(self, container):
        frame = ttk.Frame(container)

        tk.Label(frame, text="Run settings", font=('Arial bold', 14)).grid(column=0, row=1, sticky=tk.W)
        tk.Label(frame, text="Number of poses:").grid(column=0, row=2, sticky=tk.E)
        tk.Label(frame, text="Camera position:").grid(column=0, row=3, sticky=tk.E)
        tk.Label(frame, text="Max dis. to cam.:").grid(column=0, row=4, sticky=tk.E)
        tk.Label(frame, text="Min dis. to cam.:").grid(column=0, row=5, sticky=tk.E)
        tk.Label(frame, text="Max dis. obj. place:").grid(column=0, row=6, sticky=tk.E)
        tk.Label(frame, text="Min dis. obj. place:").grid(column=0, row=7, sticky=tk.E)
        tk.Label(frame, text="Output settings", font=('Arial bold', 14)).grid(column=0, row=8, sticky=tk.W)

        tk.Checkbutton(frame, text='Output coco', variable=self.var_output_coco, onvalue=1, offvalue=0)\
            .grid(column=0, row=9, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame, text='Output hdf5', variable=self.var_output_hdf5, onvalue=1, offvalue=0)\
            .grid(column=0, row=10, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame, text='Output bop', variable=self.var_output_bop, onvalue=1, offvalue=0)\
            .grid(column=0, row=11, columnspan=2, sticky=tk.W)

        tk.Checkbutton(frame, text='One object anno', variable=self.one_object_anno, onvalue=1, offvalue=0) \
            .grid(column=0, row=12, columnspan=2, sticky=tk.W)

        tk.Checkbutton(frame, text='m2mm', variable=self.m_or_mm, onvalue=1, offvalue=0) \
            .grid(column=0, row=13, columnspan=2, sticky=tk.W)

        reg = frame.register(self.callback)

        e = tk.Entry(frame, textvariable=self.one_object_anno_id)

        e.grid(column=1, row=12, sticky=tk.W + tk.E)
        e.config(validate="all", validatecommand=(reg, '%P'))

        e1 = tk.Entry(frame, textvariable=self.var_R_NP)
        e2 = tk.Entry(frame, textvariable=self.var_R_CP)

        self.entry_max_C = tk.Entry(frame, textvariable=self.var_R_max_C)
        self.entry_min_C = tk.Entry(frame, textvariable=self.var_R_min_C)

        e3 = tk.Entry(frame, textvariable=self.var_R_max_obj_place)
        e4 = tk.Entry(frame, textvariable=self.var_R_min_obj_place)

        e1.grid(column=1, row=2, sticky=tk.W + tk.E)
        e2.grid(column=1, row=3, sticky=tk.W + tk.E)
        e3.grid(column=1, row=6, sticky=tk.W + tk.E)
        e4.grid(column=1, row=7, sticky=tk.W + tk.E)

        e1.config(validate="all", validatecommand=(reg, '%P'))
        e2.config(validate="all", validatecommand=(reg, '%P'))
        e3.config(validate="all", validatecommand=(reg, '%P'))
        e4.config(validate="all", validatecommand=(reg, '%P'))
        self.entry_max_C.config(validate="all", validatecommand=(reg, '%P'))
        self.entry_min_C.config(validate="all", validatecommand=(reg, '%P'))

        for widget in self.root.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def place_path_inputs(self, container):
        frame = ttk.Frame(container)

        tk.Button(frame, text='Find BOP parent path', width=20, command=lambda: self.open_location(self.bop_parent_path))\
            .grid(column=0, row=1)
        tk.Button(frame, text='BOP dataset name', width=20, command=lambda: self.open_location(self.bop_dataset_name), state=DISABLED)\
            .grid(column=0, row=2)
        tk.Button(frame, text='Find cc-texture path', width=20, command=lambda: self.open_location(self.cc_textures_path))\
            .grid(column=0, row=3)
        tk.Button(frame, text='Find Output dir', width=20, command=lambda: self.open_location(self.output_dir))\
            .grid(column=0, row=4)
        tk.Button(frame, text='Find external model', width=20, command=lambda: self.open_location(self.clock_model))\
            .grid(column=0, row=5)

        tk.Label(frame, textvariable=self.bop_parent_path).grid(column=1, row=1, columnspan=2, sticky=tk.W)
        tk.Entry(frame, textvariable=self.bop_dataset_name).grid(column=1, row=2, columnspan=1, sticky=tk.W)
        tk.Label(frame, text='Object number(s)').grid(column=3, row=2, columnspan=1, sticky=tk.W)
        tk.Entry(frame, textvariable=self.list_object).grid(column=4, row=2, columnspan=1, sticky=tk.W)
        tk.Label(frame, textvariable=self.cc_textures_path).grid(column=1, row=3, columnspan=2, sticky=tk.W)

        tk.Label(frame, text='Texture(s)').grid(column=3, row=3, columnspan=1, sticky=tk.W)
        tk.Entry(frame, textvariable=self.list_background).grid(column=4, row=3, columnspan=1, sticky=tk.W)

        tk.Label(frame, textvariable=self.output_dir).grid(column=1, row=4, columnspan=2, sticky=tk.W)
        tk.Label(frame, textvariable=self.clock_model).grid(column=1, row=5, columnspan=2, sticky=tk.W)

        tk.Checkbutton(frame, text='Use external object', variable=self.ex_obj, onvalue=1, offvalue=0) \
            .grid(column=3, row=5, columnspan=2, sticky=tk.W)

        for widget in self.root.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def place_start_blendeproc(self, container):
        frame = ttk.Frame(container)

        tk.Label(frame, text='Run blenderproc', font=('Arial bold', 14)).grid(column=0, row=1, sticky=tk.W)

        tk.Button(frame, text='RUN', width=20, command=lambda: self.start())\
            .grid(column=0, row=2, sticky=tk.W+tk.E)
        tk.Button(frame, text='Save', width=20, command=lambda: self.save()) \
            .grid(column=1, row=2, sticky=tk.W + tk.E)
        tk.Button(frame, text='Load', width=20, command=lambda: self.load()) \
            .grid(column=2, row=2, sticky=tk.W + tk.E)
        tk.Button(frame, text='Tools', width=20, command=lambda: self.openNewWindow()) \
            .grid(column=3, row=2, sticky=tk.W + tk.E)

        tk.Label(frame, text="Optional - If the BOP-Toolkit is not recognized by Python")\
            .grid(column=0, row=3, columnspan=2, sticky=tk.E)

        tk.Checkbutton(frame, text='', variable=self.addBOPToolkit_bool, onvalue=1, offvalue=0) \
            .grid(column=2, row=3, columnspan=2, sticky=tk.W)

        tk.Button(frame, text='Add Path to BOP-toolkit', width=20, command=lambda: self.open_location(self.addBOPToolkit)) \
            .grid(column=0, row=4)
        tk.Label(frame, textvariable=self.addBOPToolkit).grid(column=1, row=4, columnspan=2, sticky=tk.W)

        for widget in self.root.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def init_var(self):
        """
        Function to initilizes the variable in the GUI
        """
        self.bop_parent_path = tk.StringVar()
        self.bop_parent_path.set("Select path")
        self.bop_dataset_name = tk.StringVar()
        self.bop_dataset_name.set("Name Dataset")
        self.cc_textures_path = tk.StringVar()
        self.cc_textures_path.set("Select path")
        self.output_dir = tk.StringVar()
        self.output_dir.set("Select path")
        self.clock_model = tk.StringVar()
        self.clock_model.set("Select path")

        self.list_object = tk.StringVar()

        self.var_PL_placing = tk.DoubleVar()
        self.var_PL_intensity = tk.DoubleVar()
        self.var_PL_color = tk.DoubleVar()
        self.var_BG_Use = tk.DoubleVar()
        self.var_BG = tk.DoubleVar()
        self.var_BG_GP = tk.DoubleVar()
        self.var_BG_it = tk.DoubleVar()

        self.var_side = tk.DoubleVar()
        self.var_LP_min_int = tk.DoubleVar()
        self.var_LP_max_int = tk.DoubleVar()
        self.var_LP_color_1 = tk.DoubleVar()
        self.var_LP_color_2 = tk.DoubleVar()

        self.var_PL_max_int = tk.DoubleVar()
        self.var_PL_min_int = tk.DoubleVar()
        self.var_PL_max_ele = tk.DoubleVar()
        self.var_PL_min_ele = tk.DoubleVar()

        self.var_R_NP = tk.DoubleVar()
        self.var_R_CP = tk.IntVar()
        self.var_R_proj = tk.DoubleVar()
        self.var_R_max_C = tk.DoubleVar()
        self.var_R_min_C = tk.DoubleVar()

        self.var_R_max_obj_place = tk.DoubleVar()
        self.var_R_min_obj_place = tk.DoubleVar()

        self.var_output_coco = tk.DoubleVar()
        self.var_output_hdf5 = tk.DoubleVar()
        self.var_output_bop = tk.DoubleVar()

        self.ex_obj = tk.DoubleVar()
        self.list_background = tk.StringVar()

        self.addBOPToolkit = tk.StringVar()
        self.addBOPToolkit_bool = tk.DoubleVar()

        self.one_object_anno = tk.IntVar()
        self.one_object_anno_id = tk.IntVar()

        self.m_or_mm = tk.IntVar()

    def open_location(self, label):
        """
        Function to open a directory/location
        """
        filepath = filedialog.askdirectory()
        if not filepath:
            return
        self.changeText(label, filepath)

    def open_file(self, label):
        """
        Function to open a folder
        """
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        self.changeText(label, filepath)

    def changeText(self, label, string):
        """
        Function to change the text of a label
        Parameters:
            label:          label
            string (str):   text
        """
        label.set("{}".format(string))

    def enable_entry(self, entry, var):
        """
        Function to (dis)able an entry
        Parameters:
            entry:          entry
            var (str):      tkinter variable
        """
        if var.get() == 1:
            entry.grid(column=1, row=4, sticky=tk.E)
        else:
            entry.grid_remove()
            self.var_BG_it.set(0)

    def enable_entry2(self, var):
        """
        Function to make an entry (in)visible
        Parameters:
            entry:          entry
        """
        if var.get() == 1:
            self.entry_max_C.grid(column=1, row=4, sticky=tk.W + tk.E)
            self.entry_min_C.grid(column=1, row=5, sticky=tk.W + tk.E)
        else:
            self.entry_max_C.grid_remove()
            self.entry_min_C.grid_remove()

    def start(self):
        """
        Function to run the model.py in cmd
        """
        print("start program")
        self.save_settings("Original")

        absolute_path = os.path.dirname(__file__)
        path = os.path.join(absolute_path + "/model.py")
        os.system('blenderproc run "{}"'.format(path))

    def save(self):
        """
        Function to save the settings
        """
        answer = tk.messagebox.askyesno(title='Save settings', message='Do you want to save the current settings?')
        if answer:
            self.save_settings("saved_settings")

    def control_path_not_empty(self, path):
        """
        Function to check if path exist
        """
        if path == "Select path":
            messagebox.showerror('Python Error', 'Path is no path')
        if os.path.exists(path):
            return path
        else:
            messagebox.showerror('Python Error', 'Path is no path')

    def int_to_bool(self, integer):
        if integer == 1:
            return True
        elif integer == 0:
            return False
        else:
            return False

    def string_to_list(self, text):
        if text == '':
            return []
        else:
            return list(map(int, text.split(',')))

    def string_to_list2(self, text):
        if text == '':
            return []
        else:
            return text.split(',')

    def list_to_string(self, list_):
        string = ""
        for i in range(len(list_)):
            if i == 0:
                string = str(list_[i])
            else:
                string = string + ", " + str(list_[i])
        return string

    def save_settings(self, name):
        """
        Function to save the settings
        """
        dict1 = {'bop_parent_path': self.control_path_not_empty(self.bop_parent_path.get()),
                 'bop_dataset_name': self.bop_dataset_name.get() if self.bop_dataset_name.get() != 'Name Dataset'\
                     else messagebox.showerror('Python Error', 'Datasetname!'),
                 'cc_textures_path': self.control_path_not_empty(self.cc_textures_path.get()),
                 'output_dir': self.control_path_not_empty(self.output_dir.get()),
                 'clock_model': self.control_path_not_empty(self.clock_model.get()) if self.ex_obj.get() == True\
                     else self.clock_model.get(),
                 'list_bop_objects': self.string_to_list(self.list_object.get()),
                 'side': self.var_side.get(),
                 'min_intensity': self.var_LP_min_int.get(),
                 'max_intensity': self.var_LP_max_int.get(),
                 'color_1': self.var_LP_color_1.get(),
                 'color_2': self.var_LP_color_2.get(),
                 'random_placing': self.int_to_bool(self.var_PL_placing.get()),
                 'random_intensity': self.int_to_bool(self.var_PL_intensity.get()),
                 'random_color': self.int_to_bool(self.var_PL_color.get()),
                 'point_light_intensity_min': self.var_PL_min_int.get(),
                 'point_light_intensity_max': self.var_PL_max_int.get(),
                 'min_elevation': self.var_PL_min_ele.get(),
                 'max_elevation': self.var_PL_max_ele.get(),
                 'use_backgrond': self.int_to_bool(self.var_BG_Use.get()),
                 'change_background': self.int_to_bool(self.var_BG.get()),
                 'change_ground_plane': self.int_to_bool(self.var_BG_GP.get()),
                 'number_of_it': self.var_BG_it.get(),
                 'backgrounds': self.string_to_list2(self.list_background.get()), # ["PavingStones", "Bricks", "Rocks", "Wood", "Asphalt"],
                 'number_of_poses': self.var_R_NP.get(),
                 'camera_position': self.var_R_CP.get(),
                 'projection_ground': self.int_to_bool(self.var_R_proj.get()),
                 'max_distance_to_cam': self.var_R_max_C.get(),
                 'min_distance_to_cam': self.var_R_min_C.get(),
                 'min_distance': self.var_R_min_obj_place.get(),
                 'max_distance': self.var_R_max_obj_place.get(),
                 'output_coco': self.int_to_bool(self.var_output_coco.get()),
                 'output_hdf5': self.int_to_bool(self.var_output_hdf5.get()),
                 'output_bop_data': self.int_to_bool(self.var_output_bop.get()),
                 'external_obj': self.int_to_bool(self.ex_obj.get()),
                 'BOP-Tookit_Path': self.addBOPToolkit.get(),
                 'BOP-Tookit_Path_bool': self.int_to_bool(self.addBOPToolkit_bool.get()),
                 'one_object_anno': self.int_to_bool(self.one_object_anno.get()),
                 'one_object_anno_id': self.one_object_anno_id.get(),
                 'm_or_mm': self.int_to_bool(self.m_or_mm.get())
                 }

        file1 = open("{}.txt".format(name), "wb")
        pickle.dump(dict1, file1)
        file1.close

    def load(self):
        """
        Function to load the settings
        """
        file = open('saved_settings.txt', 'rb')
        data = pickle.load(file)
        file.close()

        self.bop_parent_path.set(data["bop_parent_path"])
        self.bop_dataset_name.set(data["bop_dataset_name"])
        self.cc_textures_path.set(data["cc_textures_path"])
        self.output_dir.set(data["output_dir"])
        self.clock_model.set(data["clock_model"])
        self.list_object.set(self.list_to_string(data["list_bop_objects"]))
        self.var_side.set(data["side"])
        self.var_LP_min_int.set(data["min_intensity"])
        self.var_LP_max_int.set(data["max_intensity"])
        self.var_LP_color_1.set(data["color_1"])
        self.var_LP_color_2.set(data["color_2"])
        self.var_PL_placing.set(data["random_placing"])
        self.var_PL_intensity.set(data["random_intensity"])
        self.var_PL_color.set(data["random_color"])
        self.var_PL_min_int.set(data["point_light_intensity_min"])
        self.var_PL_max_int.set(data["point_light_intensity_max"])
        self.var_PL_min_ele.set(data["min_elevation"])
        self.var_PL_max_ele.set(data["max_elevation"])
        self.var_BG_Use.set(data["use_backgrond"])
        self.var_BG.set(data["change_background"])
        self.var_BG_GP.set(data["change_ground_plane"])
        self.var_BG_it.set(data["number_of_it"])
        self.var_R_NP.set(data["number_of_poses"])
        self.var_R_CP.set(data["camera_position"])
        self.var_R_proj.set(data["projection_ground"])
        self.var_R_max_C.set(data["max_distance_to_cam"])
        self.var_R_min_C.set(data["min_distance_to_cam"])
        self.var_R_min_obj_place.set(data["min_distance"])
        self.var_R_max_obj_place.set(data["max_distance"])
        self.var_output_coco.set(data["output_coco"])
        self.var_output_hdf5.set(data["output_hdf5"])
        self.var_output_bop.set(data["output_bop_data"])
        self.ex_obj.set(data["external_obj"])
        self.list_background.set(self.list_to_string(data["backgrounds"]))
        self.addBOPToolkit.set(data["BOP-Tookit_Path"])
        self.addBOPToolkit_bool.set(data["BOP-Tookit_Path_bool"])
        self.one_object_anno.set(data["one_object_anno"])
        self.one_object_anno_id.set(data["one_object_anno_id"])
        self.m_or_mm.set(data["m_or_mm"])

        if self.var_BG.get():
            self.enable_entry(self.entry_it, self.var_BG)
        if self.var_R_proj.get():
            self.enable_entry2(self.var_R_proj)

    def openNewWindow(self):
        newWindow = Toplevel(self.root)
        newWindow.title("Writer mask(s)")
        newWindow.geometry("300x300")
        tk.Label(newWindow, text="Make sure there are hdf5 containers in the output path! \n "
                                 "Segmentation masks are created from all hdf5 containers in the output. ").pack()
        tk.Button(newWindow, text='Make mask(s)', width=20, command=lambda: self.write_mask()).pack()

        tk.Label(newWindow, text="====================").pack()

        tk.Label(newWindow, text="Write binary mask. Give object id!").pack()

        self.obj_id = tk.IntVar()
        reg = newWindow.register(self.callback)
        e = tk.Entry(newWindow, textvariable=self.obj_id)
        e.pack()
        e.config(validate="all", validatecommand=(reg, '%P'))

        tk.Button(newWindow, text='Make mask(s)', width=20, command=lambda: self.write_binary_mask()).pack()

        tk.Label(newWindow, text="====================").pack()

        tk.Label(newWindow, text="Convert txt-file to yaml-file").pack()
        self.input_path = tk.StringVar()
        tk.Button(newWindow, text='Path', width=20, command=lambda: self.open_file(self.input_path)) \
            .pack()
        tk.Label(newWindow, textvariable=self.input_path).pack()
        tk.Button(newWindow, text='Convert', width=20, command=lambda: self.convert_txt_2_yml()).pack()

    def convert_txt_2_yml(self):
        import yaml
        import json
        path = self.input_path.get()
        drive, file_ = os.path.split(path)
        with open(path, 'r') as file:
            configuration = json.load(file)
        path_file_yml = str(drive) + '/' + str(os.path.splitext(file_)[0]) + '.yml'
        with open(path_file_yml, 'w') as yaml_file:
            yaml.dump(configuration, yaml_file)

    def count_hdf5_files(self, path):
        count = 0
        for root_dir, cur_dir, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == ".hdf5":
                    count = count + 1
        return count

    def write_binary_mask(self):
        import h5py
        from PIL import Image

        if not self.control_path_not_empty(self.output_dir.get()):
            return 0

        path = self.output_dir.get() + "/train_pbr/000000/mask"
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
            print("Folder already exist")

        for k in range(self.count_hdf5_files(self.output_dir.get())):
            filename = self.output_dir.get() + "/{}.hdf5".format(k)
            with h5py.File(filename, "r") as f:
                group = f["class_segmaps"]

                image = np.zeros((480, 640))
                image[group[:,:] == self.obj_id.get()] = 255
                im = Image.fromarray(image[:, :])

                new_str = str(k)
                im = im.convert("L")
                im.save(os.path.join(path + '/' + new_str.zfill(6) + ".png"))

    def write_mask(self):
        import h5py
        from PIL import Image

        if self.control_path_not_empty(self.output_dir.get()) == False:
            return 0

        path = self.output_dir.get() + "/train_pbr/000000/mask"
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
            print("Folder already exist")

        for i in range(self.count_hdf5_files(self.output_dir.get())):
            filename = self.output_dir.get() + "/{}.hdf5".format(i)
            with h5py.File(filename, "r") as f:
                group = f["class_segmaps"]
                array_im = group[:, :].copy()
                im = Image.fromarray(array_im[:, :])
                new_str = str(i)
                im.save(os.path.join(path + '/' + new_str.zfill(6) + ".png"))


if __name__ == "__main__":
    Window()