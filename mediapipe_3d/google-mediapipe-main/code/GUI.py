import datetime
import pathlib
from queue import Queue
from threading import Thread
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
from tkcalendar import Calendar, DateEntry
import os
import correlation
import rhythm
import skeleton_3D_coors
import record_skeleton_3D_coors
import VitalInfoExtract

class DancingScoring(ttk.Frame):

    queue = Queue()
    searching = False

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        # application variables
        _path = pathlib.Path().absolute().as_posix()
        self.path_var = ttk.StringVar(value=_path)
        self.name_var = ttk.StringVar(value='')
        self.bd_var = ttk.StringVar(value='')
        self.height_var = ttk.IntVar(value=168)
        self.weight_var = ttk.IntVar(value=50)
        self.file_var = ttk.StringVar(value=_path)
        self.pose_score = ttk.StringVar(value='click button to view your score')
        self.rhythm_score = ttk.StringVar(value='click button to view your score')
        self.txtfile_var = ttk.StringVar(value=_path)
        self.greeting_var = ttk.StringVar(value='Hi! Honey.')
        self.cal_info = ttk.StringVar(value='Start Dancing now!')
        self.hr = ttk.StringVar(value='')
        # self.p_list = np.ndarray
        # self.q_list = np.ndarray
        # output txt file (raw)
        self.out1 = ttk.StringVar(value='')
        self.out2 = ttk.StringVar(value='')
        self.recorded = ttk.IntVar(value=0) # whether use record


        # two columns
        for i in range(2):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

        # column 1
        col1 = ttk.Frame(self, padding=10)
        col1.grid(row=0, column=0, sticky=NSEW)

        # user info
        user_info = ttk.LabelFrame(col1, text="User Info", padding=10)
        user_info.pack(side=TOP, fill=BOTH, expand=YES)

        # up frame of user info (contain name and bd entry)
        user_info_header = ttk.Frame(user_info, padding=5)
        user_info_header.pack(fill=X)

        # middle frame of user info (contain name and bd entry)
        user_info_middle = ttk.Frame(user_info, padding=5)
        user_info_middle.pack(fill=X)

        # name
        name_lbl = ttk.Label(user_info_header, text='Name', width=8)
        name_lbl.pack(side=LEFT, padx=(15,0))

        name_ent = ttk.Entry(user_info_header, textvariable=self.name_var,bootstyle=DARK)
        name_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # birthday
        bd_lbl = ttk.Label(user_info_header, text='Birthday', width=8)
        bd_lbl.pack(side=LEFT, padx=(15,0))

        bd_ent = ttk.Entry(user_info_header, textvariable=self.bd_var, bootstyle=DARK)
        bd_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # self.bd_ent = ttk.DateEntry(user_info_header,bootstyle=DARK,width=16)
        # self.bd_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # height
        height_lbl = ttk.Label(user_info_middle, text='Height', width=8)
        height_lbl.pack(side=LEFT, padx=(15, 0))

        height_ent = ttk.Entry(user_info_middle, textvariable=self.height_var,bootstyle=DARK)
        height_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # weight
        weight_lbl = ttk.Label(user_info_middle, text='Weight', width=8)
        weight_lbl.pack(side=LEFT, padx=(15, 0))

        weight_ent = ttk.Entry(user_info_middle, textvariable=self.weight_var,bootstyle=DARK)
        weight_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # Select your gender
        gender_lbl = ttk.Label(user_info, text='Select your gender', width=18)
        gender_lbl.pack(side=LEFT, padx=(15, 0))

        # Menu Button
        Menu_btn0 = ttk.Menubutton(user_info, text='Gender', bootstyle=(OUTLINE, DARK))
        self.Var0 = ttk.IntVar(value=1)
        Menu_gender = ttk.Menu(Menu_btn0, tearoff=0)
        Menu_gender.add_radiobutton(label='Female', variable=self.Var0, value=1)
        Menu_gender.add_radiobutton(label='Male', variable=self.Var0, value=2)
        Menu_gender.add_radiobutton(label='Others', variable=self.Var0, value=3)
        Menu_gender.add_radiobutton(label='Cat', variable=self.Var0, value=4)
        Menu_btn0["menu"] = Menu_gender
        Menu_btn0.pack(side=LEFT, fill=X, expand=YES)

        # confirm button
        confirm_btn = ttk.Button(
            master=user_info,
            text="Confirm",
            bootstyle=(OUTLINE,DARK),
            command=self.retrieve,
            width = 8
        )
        confirm_btn.pack(padx=10, fill=X)

        # Dancing song selection
        song_select = ttk.LabelFrame(col1, text="Dancing song selection", padding=10)
        song_select.pack(side=TOP, fill=BOTH, expand=YES)

        # up frame of DSS
        database_row = ttk.Frame(song_select, padding=5)
        database_row.pack(fill=X)

        # middle frame of DSS
        upload_row = ttk.Frame(song_select, padding=5)
        upload_row.pack(fill=X)

        # Select from Database
        select_lbl = ttk.Label(database_row, text='Select from Database', width=20)
        select_lbl.pack(side=LEFT, padx=(15, 0))

        # Menu Button
        Menu_btn = ttk.Menubutton(database_row, text='Dance Song', bootstyle=(OUTLINE,PRIMARY))
        self.Var1 = ttk.IntVar(value=0)
        Menu_song = ttk.Menu(Menu_btn, tearoff = 0)
        Menu_song.add_radiobutton(label='Chicken u so beautiful', variable=self.Var1, value=1)
        Menu_song.add_radiobutton(label='Man of the year', variable=self.Var1, value=2)
        Menu_song.add_radiobutton(label='Pick me pick me up', variable=self.Var1, value=3)
        Menu_song.add_radiobutton(label='nonsense', variable=self.Var1, value=4)
        Menu_btn["menu"] = Menu_song
        Menu_btn.pack(side=LEFT,fill=X, expand=YES)

        # upload
        upload_lbl = ttk.Label(upload_row, text='Upload', width=8)
        upload_lbl.pack(side=LEFT, padx=(15, 0))

        # path entry
        path_ent = ttk.Entry(upload_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # browse button
        browse_btn = ttk.Button(
            master=upload_row,
            text="Browse",
            command=self.on_browse,
            width=8,
            bootstyle=(OUTLINE, PRIMARY)
        )
        browse_btn.pack(side=LEFT, padx=5)

        # progress bar
        pb = ttk.Progressbar(song_select, value=66,bootstyle= 'primary')
        pb.pack(fill=X, pady=5, padx=5)
        ttk.Label(pb, text='66%', bootstyle=(PRIMARY, INVERSE)).pack()

        # My dance
        my_dance = ttk.LabelFrame(col1, text="My dance", padding=10)
        my_dance.pack(side=TOP, fill=BOTH, expand=YES)

        # up frame of my dance
        select_row = ttk.Frame(my_dance, padding=5)
        select_row.pack(fill=X)

        # middle frame of my dance
        record_row = ttk.Frame(my_dance, padding=5)
        record_row.pack(fill=X)

        # Select label
        upload1_lbl = ttk.Label(select_row, text='Upload', width=8)
        upload1_lbl.pack(side=LEFT, padx=(15, 0))

        # file entry
        file_ent = ttk.Entry(select_row, textvariable=self.file_var)
        file_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)


        # browse1 button
        browse1_btn = ttk.Button(
            master=select_row,
            text="Browse",
            command=self.on_browse1,
            width=8,
            bootstyle=(OUTLINE,INFO)
        )
        browse1_btn.pack(side=LEFT, padx=5)

        # record label
        record_lbl = ttk.Label(record_row, text='Record', width=8)
        record_lbl.pack(side=LEFT, padx=(15, 0))

        # start button
        start_btn = ttk.Button(
            master=record_row,
            text="Start",
            command=self.start_recording,
            width=8,
            bootstyle=(OUTLINE,INFO)
        )
        start_btn.pack(side=LEFT, padx=5)

        # stop notice label
        stop_lbl = ttk.Label(record_row, text="Long press 'q' to stop recording", width=25,bootstyle=INFO)
        stop_lbl.pack(side=LEFT, padx=(15, 0))
        # stop_btn = ttk.Button(
        #     master=record_row,
        #     text="Stop",
        #     command=self.stop_recording,
        #     width=8,
        #     bootstyle=(OUTLINE,'info')
        # )
        # stop_btn.pack(side=LEFT, padx=5)

        # Column 2
        col2 = ttk.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky=NSEW)

        # Evaluation
        evaluation = ttk.LabelFrame(col2, text="Evaluation", padding=10)
        evaluation.pack(side=TOP, fill=BOTH, expand=YES)

        # pose row
        pose_row = ttk.Frame(evaluation, padding=5)
        pose_row.pack(fill=X)

        # rhythm row
        rhythm_row = ttk.Frame(evaluation, padding=5)
        rhythm_row.pack(fill=X)

        # pose label
        pose_lbl = ttk.Label(pose_row, text="Pose Accuracy:", width=16)
        pose_lbl.pack(side=LEFT, padx=(15, 0))

        # pose score output
        pose_score_lbl = ttk.Label(pose_row, textvariable=self.pose_score, width=25)
        pose_score_lbl.pack(side=LEFT)

        # view score button
        score1_btn = ttk.Button(
            master=pose_row,
            text="View my score",
            command=self.generate_score1,
            width=13,
            bootstyle=(SOLID,SECONDARY)
        )
        score1_btn.pack(side=LEFT, padx=5)

        # rhythm label
        rhythm_lbl = ttk.Label(rhythm_row, text="Rhythm Matching:", width=16)
        rhythm_lbl.pack(side=LEFT, padx=(15, 0))

        # pose score output
        rhythm_score_lbl = ttk.Label(rhythm_row, textvariable=self.rhythm_score, width=25)
        rhythm_score_lbl.pack(side=LEFT)

        # view score button
        score2_btn = ttk.Button(
            master=rhythm_row,
            text="View my score",
            command=self.generate_score2,
            width=13,
            bootstyle=(SOLID,SECONDARY)
        )
        score2_btn.pack(side=LEFT, padx=5)



        # Vital Info
        vital_info = ttk.LabelFrame(col2, text="Vital Info", padding=10)
        vital_info.pack(side=TOP, fill=BOTH, expand=YES)

        # up frame
        vital_info_header = ttk.Frame(vital_info, padding=5)
        vital_info_header.pack(fill=X)

        # middle frame
        vital_info_middle = ttk.Frame(vital_info, padding=5)
        vital_info_middle.pack(fill=X)

        # Select text file
        vital_file_lbl = ttk.Label(vital_info_header, text="Select Bracelet File", width=16)
        vital_file_lbl.pack(side=LEFT, padx=(15, 0))

        # file entry
        txt_ent = ttk.Entry(vital_info_header, textvariable=self.txtfile_var)
        txt_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # browse button2
        browse2_btn = ttk.Button(
            master=vital_info_header,
            text="Browse",
            command=self.on_browse2,
            width=8,
            bootstyle=(SOLID,WARNING)
        )
        browse2_btn.pack(side=LEFT, padx=5)

        # Calories label1: hi! (username)
        cal_lbl1 = ttk.Label(vital_info_middle, textvariable=self.greeting_var, width=16)
        cal_lbl1.pack(side=LEFT, padx=(15, 0))


        # Calories label2: You have burned xxx calories
        cal_lbl2 = ttk.Label(vital_info_middle, textvariable=self.cal_info, width=30)
        cal_lbl2.pack(side=LEFT, padx=(15, 0))

        # cal_calories button
        cal_btn = ttk.Button(
            master=vital_info_middle,
            text="Analysis",
            command=self.cal_calories,
            width=8,
            bootstyle=(SOLID, WARNING)
        )
        cal_btn.pack(side=RIGHT, padx=5)

        # heart rate
        hr_lbl1 = ttk.Label(vital_info, textvariable=self.hr, width=50)
        hr_lbl1.pack(side=LEFT, padx=(15,0))

    def on_browse(self):
        """Callback for directory browse"""
        # standard dance file
        file = askopenfilename(filetypes=(("video files","*.mp4"),("all files", "*.*")))
        if file:
            self.path_var.set(file)

    def on_browse1(self):
        """Callback for directory browse"""
        # your dance video file
        file = askopenfilename(filetypes=(("video files","*.mp4"),("all files", "*.*")))
        if file:
            self.file_var.set(file)
        self.recorded.set(0)

    def on_browse2(self):
        """Callback for directory browse"""
        # Heyue's txt file
        file = askopenfilename(filetypes=(("Log files","*.log"),("all files", "*.*")))
        if file:
            self.txtfile_var.set(file)

    def cal_calories(self):
        # print("here")
        # h = self.height_var.get()
        # print(self.weight_var.get())
        # print(self.name_var.get())
        # f = 'D:/mediapipe_3d/google-mediapipe-main/out/1.txt'
        # q_j_list = correlation.preprocess(f)
        # time = len(q_j_list) / 30  # unit of second
        # print(time)
        # cal = 10000 * time / 3600 * self.weight_var.get()
        # self.greeting_var.set('Hi,' + self.name_var.get())
        # self.cal_info.set('You have burned ' + str(cal) + ' calories')
        # file = self.txtfile_var.get()
        try:
            # heart rate
            txtfile = self.txtfile_var.get()
            signals, bpms, bpm_mean = VitalInfoExtract.read_vital(txtfile)

            posefile = self.out2.get()
            # print(posefile)
            q_j_list = correlation.preprocess(posefile)
            time = len(q_j_list) / 30  # unit of second

            #time = 100
            W = int(self.weight_var.get())
            BD = self.bd_var.get()
            year = BD[:4]
            print(year)
            A = 2023 - int(year)
            print(A)

            # Female
            if self.Var0.get() == 1:
                print('female')
                cal = ((-55.0969 + (0.6309 * bpm_mean) + (0.1988 * W) + (0.2017 * A)) / 4.184) * 60 * time/3600
                self.greeting_var.set('Hi,' + self.name_var.get() + '!')
                self.cal_info.set("You have burned %.2f calories." % cal)
                self.hr.set("Your average heart rate is " + str(bpm_mean))
            if self.Var0.get() == 2:
                print('male')
                cal = ((-20.4022 + (0.4472 * bpm_mean) - (0.1263 * W) + (0.074 * A)) / 4.184) * 60 * time / 3600
                self.greeting_var.set('Hi,' + self.name_var.get() + '!')
                self.cal_info.set("You have burned %.2f calories." % cal)
                self.hr.set("Your average heart rate is " + str(bpm_mean))
            if self.Var0.get() == 4:
                print('cat')
                cal = 'Meow'
                self.greeting_var.set('Meow!')
                self.cal_info.set("Meow MeoMeow Meow!")
                self.hr.set("Meow MeoMeow Meow? MeoMeow Meow.")
            if self.Var0.get() == 3:
                print('others')
                cal1 = ((-55.0969 + (0.6309 * bpm_mean) + (0.1988 * W) + (0.2017 * A)) / 4.184) * 60 * time/3600
                cal2 = ((-20.4022 + (0.4472 * bpm_mean) - (0.1263 * W) + (0.074 * A)) / 4.184) * 60 * time / 3600
                cal = (cal1+cal2)/2
                self.greeting_var.set('Hi,' + self.name_var.get() + '!')
                self.cal_info.set("You have burned %.2f calories." % cal)
                self.hr.set("Your average heart rate is " + str(bpm_mean))

            print(cal)

        except:
            self.cal_info.set("Record or upload a video first.")

        return 0

    def start_recording(self):
        self.recorded.set(1)
        record_skeleton_3D_coors.record(str(self.name_var.get()))
        self.file_var.set(str(self.name_var.get()) + '.mp4')
        self.out2.set(str(self.name_var.get()) + '.txt')
        return 0 # fill

    # pose accuracy score
    def generate_score1(self):
        try:
            # standard video output
            print(self.Var1.get())
            if self.Var1.get() != 0:
                outfile1 = 'D:/mediapipe_3d/google-mediapipe-main/out/'+str(self.Var1.get()) + '.txt'
            else:
                infile1 = self.path_var.get()
                (filepath1, filename1) = os.path.split(infile1)
                (name1, suffix1) = os.path.splitext(filename1)
                outfile1 = name1 + '.txt'
                outfile1 = skeleton_3D_coors.extract_pose(infile1, 'D:/mediapipe_3d/google-mediapipe-main/out/'+outfile1)
            self.out1.set(outfile1)

            # users' video output
            if self.recorded.get() == 1:
                outfile2 = self.out2.get()
            else:
                infile2 = self.file_var.get()
                (filepath2, filename2) = os.path.split(infile2)
                (name2, suffix2) = os.path.splitext(filename2)
                outfile2 = name2 + '.txt'
                outfile2 = skeleton_3D_coors.extract_pose(infile2, 'D:/mediapipe_3d/google-mediapipe-main/out/'+outfile2)
            self.out2.set(outfile2)

            p_j_list = correlation.preprocess(outfile1)
            # self.p_list = p_j_list
            q_j_list = correlation.preprocess(outfile2)
            # self.q_list = q_j_list

            score1 = correlation.correlation(p_j_list, q_j_list)
            #print(score1)
            # if score1 < 0.5:
            #     score1 = score1*2
            self.pose_score.set(str(score1*100)+'/100')
        except:
            self.pose_score.set("Pls upload dance files first")
        ###############################################################
        # infile1 = self.path_var.get()
        # infile2 = self.file_var.get()
        # # get the filename
        # (filepath1, filename1) = os.path.split(infile1)
        # (name1, suffix1) = os.path.splitext(filename1)
        # (filepath2, filename2) = os.path.split(infile2)
        # (name2, suffix2) = os.path.splitext(filename2)
        # # generate output file name
        # outfile1 = name1 + '.txt'
        # outfile2 = name2 + '.txt'
        #
        # # run skeleton: skeleton_3D_coors
        # txtfile1 = skeleton_3D_coors.extract_pose(infile1,'D:/mediapipe_3d/google-mediapipe-main/out/'+outfile1)
        # p_j_list = correlation.preprocess('D:/mediapipe_3d/google-mediapipe-main/out/'+outfile1)
        # # save output filename to self.var
        # self.out1.set(txtfile1)
        #
        # txtfile2 = skeleton_3D_coors.extract_pose(infile2,'D:/mediapipe_3d/google-mediapipe-main/out/'+outfile2)
        # q_j_list = correlation.preprocess('D:/mediapipe_3d/google-mediapipe-main/out/'+outfile2)
        # # save output filename to self.var
        # self.out2.set(txtfile2)
        #
        # score1 = correlation.correlation(p_j_list, q_j_list)
        # self.pose_score.set(score1)
        # return 0

    # rhythm matching score
    def generate_score2(self):
        if self.recorded.get() == 1:
            self.rhythm_score.set("No score with live stream :(")
            return 0
        txtfile1 = self.out1.get()
        videofile1 = self.path_var.get()
        filenum = 0
        try:
            p_j_list = correlation.preprocess(txtfile1)
            filenum += 1
        except:
            pass

        txtfile2 = self.out2.get()
        videofile2 = self.file_var.get()
        try:
            q_j_list = correlation.preprocess(txtfile2)
            filenum += 3
        except:
            pass

        if filenum == 0:
            self.rhythm_score.set("Pls upload your dance file first")
            return 0
        if filenum == 1:
            if self.Var1.get() != 0:
                score2 = rhythm.rhythm_matching(txtfile1,str(self.Var1.get())+'.wav', 0.25, 30)
            else:
                audio1 = rhythm.audio_converter(videofile1,'wav')
                score2 = rhythm.rhythm_matching(txtfile1, 'D:/mediapipe_3d/google-mediapipe-main/code/'+audio1, 0.25, 30)
            self.rhythm_score.set(str(score2*100)+'/100')
        if filenum == 3:
            audio2 = rhythm.audio_converter(videofile2, 'wav')
            score2 = rhythm.rhythm_matching(txtfile2, 'D:/mediapipe_3d/google-mediapipe-main/code/'+audio2, 0.25, 30)
            self.rhythm_score.set(str(score2*100)+'/100')
        if filenum == 4:
            # if self.Var1.get() != 0:
            #     ba1 = rhythm.rhythm_matching(txtfile1,str(self.Var1.get())+'.wav', 0.25, 30)
            # else:
            #     audio1 = rhythm.audio_converter(videofile1, 'wav')
            #     ba1 = rhythm.rhythm_matching(txtfile1, 'D:/mediapipe_3d/google-mediapipe-main/code/'+audio1, 0.25, 30)
            audio2 = rhythm.audio_converter(videofile2, 'wav')
            ba2 = rhythm.rhythm_matching(txtfile2, 'D:/mediapipe_3d/google-mediapipe-main/code/'+audio2, 0.25, 30)
            # if ba1 >= ba2:
            #     score2 = ba2/ba1*100
            # else:
            #     score2 = 100
            self.rhythm_score.set(str(ba2*100)+'/100')

        return 0 # fill


    # for testing
    def retrieve(self):
        print(self.name_var.get())
        print(self.bd_var.get())
        print(self.height_var.get())
        print(self.weight_var.get())
        print(self.Var0.get())


if __name__ == '__main__':
    app = ttk.Window("Dancing Scoring App", 'minty')
    DancingScoring(app)
    app.mainloop()