# Dancing Evaluation based on [Google MediaPipe](https://github.com/google/mediapipe)

[![](doc/rris_database.gif)](https://www.nature.com/articles/s41597-020-00627-7?sf237508323=1)

In this project, we used [MediaPipe](https://opensource.google/projects/mediapipe) to extract dancers' 3D skeleton data for dancing evaluation. The total evaluation contains three parts:

* Pose Accuracy Evaluation
* Rhythm Matching Evaluation
* Exercise Effect Evaluation

## Environment Setting
You might need Anaconda and Pycharm to do the following steps:
### Create virtual env and active
```
conda create -n mp python=3.8.10

activate mp
```
### install package
```
pip install -i https://pypi.doubanio.com/simple/ --upgrade numpy==1.20.3  --trusted-host pypi.douban.com

pip install -i https://pypi.doubanio.com/simple/ --upgrade open3d==0.12.0  --trusted-host pypi.douban.com

 or pip install  open3d==0.12.0 (if have http error)
 
pip install -i https://pypi.doubanio.com/simple/ --upgrade mediapipe==0.8.9.1  --trusted-host pypi.douban.com

pip install -i https://pypi.doubanio.com/simple/ --upgrade opencv-python==4.5.2.54  --trusted-host pypi.douban.com

pip install -i https://pypi.doubanio.com/simple/ --upgrade opencv-contrib-python==4.5.2.54  --trusted-host pypi.douban.com

pip uninstall protobuf

pip install -i https://pypi.doubanio.com/simple/ --upgrade protobuf==3.19.0  --trusted-host pypi.douban.com
```
### Get the path of envs (copy current env path to pycharm)
```
conda info --envs (You can simply copy the envs path to Pycharm or just run the file in "C:\")
```
### Other libraries
You should also install the libraries below to avoid errors:
* Scipy
* Librosa
* tkinter and ttkbootstrap
* moviepy
* dtaidistance


## GUI overview
Remind: The file path in "GUI.py" might need to change, you should check your file path first. Here assume you put file in "D:\"

The video you want to evaluate can be put in the folder "D:\DancingScoring\mediapipe_3d\google-mediapipe-main\data"

The output 3D skeleton data file can be found in the folder "D:\DancingScoring\mediapipe_3d\google-mediapipe-main\out"

Run "GUI.py", you should see the Tkinter interface.

### "User Info" frame: 
Enter your personal information. You can change your information anytime, it will only affect the name of the recording file and calories calculation.

### "Dancing song selection" frame :
The database has four preprocessed dancing standards now, you can select among these dances or upload a video by yourself.

You can update the database by adding code (You should run the new dance video first): 
```
Menu_song.add_radiobutton(label='songname', variable=self.Var1, value=int_number)
```
before this line:
```
Menu_btn["menu"] = Menu_song
```
Notice that the int_number cannot be the same as the number that exists. Then, change the name of "songname.txt" in the output folder to "int_number.txt" and "songname.wav" file in the code file to "int_number.wav". 

### "My dance" frame:
You can upload your video or record by webcam (we don't recommend using this, you will not get the rhythm-matching score if you use this)

### "Evaluation" frame:
You can click the buttons to view your score. Remember to finish the information in "Dancing song selection" and "My dance". Even you can still get the rhythm-matching evaluation score if only upload the standard video.

### "Vital Info" frame:
You can select the file "512.log" in the code file to see how it works. You might not want to use this...


