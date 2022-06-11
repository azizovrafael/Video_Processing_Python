import sys
import threading
import os
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import cv2
import PySimpleGUI as sg
import time


class App:
    """
    TODO: change slider resolution based on vid length
    TODO: make top menu actually do something :P    """

    def __init__(self):
        # sg.theme('DarkBlack')
        # ------ App states ------ #
        self.stop_frame = None
        self.play = True  # Is the video currently playing?
        self.delay = 0.023  # Delay between frames - not sure what it should be, not accurate playback
        self.frame = 1  # Current frame
        self.frames = None  # Number of frames
        # ------ Other vars ------ #
        self.vid = None
        self.photo = None
        self.next = "1"
        # ------ Menu Definition ------ #
        menu_def = [['&File', ['&Open', '&Save', '---', 'Properties', 'E&xit']],
                    ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                    ['&Help', '&About...']]

        layout = [[sg.Menu(menu_def)],
                  [sg.Text('Select video')], [sg.Input(key="_FILEPATH_"), sg.Button("Browse")],
                  [sg.Canvas(size=(200, 200), key="canvas", background_color="white", expand_x=True, expand_y=True)],
                  [sg.Button('Last frame'),
                   sg.Slider(size=(30, 20), range=(0, 100), resolution=10, key="slider", orientation="h",
                             enable_events=True), sg.Button('Next frame'), sg.Text("Frame: "),
                   sg.T("0", key="counter", size=(10, 1))],

                  [sg.Text("Duration (S) | (M:S) ")], [sg.T("", key="duration_display", size=(10, 1)),
                                                       sg.T("", key="duration_min_display", size=(10, 1))],

                  [sg.Button("Pause", key="Play", size=(7, 1), button_color=('white', 'red')), sg.Button('Exit')],

                  [sg.Text("Start Duration | End Duration | Converted Format | File Adı( Sonluqsuz )")],
                  [sg.Button('Start Duration', image_filename="icobut.png"), sg.Button('End Duration')],
                  [sg.InputText(key="_Start_Duration_", size=(10, 1)),
                   sg.InputText(key="_End_Duration_", size=(10, 1)),
                   sg.Combo([".mp4", ".mkv", ".avi", ".mpeg", ".flv", ".ts",
                             ".webm", ".mov", ".mjpeg", ".m4v"],
                            key="_converted_format_"), sg.InputText(key="_save_as_filename_", size=(10, 1)), ],

                  [sg.Text("New File Name"), sg.FolderBrowse(key="_save_as_folder_path_")],
                  [sg.Button("Save")]]

        self.window = sg.Window('XezerTV BIRainy', layout, size=(500, 600)).Finalize()
        # set return_keyboard_events=True to make hotkeys for video playback
        # Get the tkinter canvas for displaying the video
        canvas = self.window.Element("canvas")
        self.canvas = canvas.TKCanvas

        # Start video display thread
        self.load_video()

        while True:  # Main event Loop
            event, values = self.window.Read()

            # print(event, values)
            if event is None or event == 'Exit':
                """Handle exit"""
                break

            if event == "Save":
                print(values)
                if values.get("_FILEPATH_") == '':
                    print("No File Selected Bala.")
                else:
                    if values.get("_Start_Duration_") and values.get("_End_Duration_") and values.get(
                            "_converted_format_"):
                        print("Start: ", values.get("_Start_Duration_"))
                        print("End: ", values.get("_End_Duration_"))
                        print("Video: ", values.get("_FILEPATH_"))

                        cap = cv2.VideoCapture(values.get("_FILEPATH_"))
                        fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
                        # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                        start_frame_count = int(values.get("_Start_Duration_")) * int(fps)
                        end_frame_count = int(values.get("_End_Duration_")) * int(fps)

                        start_frame_count = start_frame_count // 1000
                        end_frame_count = end_frame_count // 1000

                        start_frame_count = time.strftime('%H:%M:%S', time.gmtime(start_frame_count))
                        end_frame_count = time.strftime('%H:%M:%S', time.gmtime(end_frame_count))

                        print("Start Frame Count: ", start_frame_count)
                        print("End Frame Count: ", end_frame_count)
                        print("Converted Format: ", values.get("_converted_format_"))
                        print("Save As Video Path: ", values.get("_save_as_folder_path_"))

                        filename = str(values.get("_save_as_folder_path_")) + "/" + str(
                            values.get("_save_as_filename_")) + str(values.get("_converted_format_"))
                        print("File Name: ", filename)
                        os.system(
                            f"ffmpeg -i {values.get('_FILEPATH_')} "
                            f"-ss {start_frame_count} "
                            f"-t {end_frame_count} "
                            f"-async 1 {filename}")
                        sg.Popup("Proses Yerine Yetirildi!")

            if event == "Browse":
                """Browse for files when the Browse button is pressed"""
                # Open a file dialog and get the file path
                video_path = None
                try:
                    video_path = sg.filedialog.askopenfile().name
                except AttributeError:
                    print("no video selected, doing nothing")

                if video_path:
                    print(video_path)
                    # Initialize video
                    self.vid = MyVideoCapture(video_path)
                    # Calculate new video dimensions
                    self.vid_width = 500
                    self.vid_height = int(self.vid_width * self.vid.height / self.vid.width)
                    print("old par: %f" % (self.vid.width / self.vid.height))
                    print("new par: %f" % (self.vid_width / self.vid_height))
                    # GEt Duration
                    cap = cv2.VideoCapture(video_path)
                    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                    # def get_video_duration(path_video):
                    #     import re
                    #     from subprocess import check_output
                    #     '''Get the duration of a video.
                    #
                    #     Parameter:
                    #         path_video <str> - The path of the input video.
                    #
                    #     Return:
                    #         duration <str> - The duration of the input video formatted as 'hh:mm:ss.msec'.
                    #     '''
                    #     # Create the command for getting the information of the input video via ffprobe.
                    #     global duration
                    #     cmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', path_video]
                    #     # Get the information of the input video via ffprobe command.
                    #     info_byte = check_output(cmd)  # <bytes>
                    #     # Decode the information.
                    #     info_str = info_byte.decode("utf-8")  # <str>
                    #     # Split the information.
                    #     info_list = re.split('[\n]', info_str)
                    #
                    #     # Get the duration of the input video.
                    #     for info in info_list:
                    #         if 'duration' in info:
                    #             # E.g., 'info' = 'duration=0:00:01.860000'.
                    #             duration = re.split('[=]', info)[1]
                    #     print("[+] ", duration.split('.')[0])
                    #     return duration.split('.')[0]

                    if int(frame_count) > 0:
                        print("Rafael Fr/C: ", frame_count)
                    # else:
                    #     sec = get_video_duration(video_path)
                    #     frame_count = int(sec) * int(fps)

                    print("Rafael Fps: ", fps)
                    duration = int(frame_count / fps)
                    print('duration (S) = ' + str(duration))
                    minutes = int(duration / 60)
                    seconds = duration % 60
                    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
                    self.display_duration = duration
                    self.display_min_duration = str(minutes) + ':' + str(seconds)

                    print("Video frames: ", int(self.vid.frames))
                    self.frames = int(self.vid.frames)

                    # Update slider to match amount of frames
                    self.window.Element("slider").Update(range=(0, int(self.frames)), value=0)
                    # Update right side of counter
                    self.window.Element("counter").Update("0/%i".format(self.frames))
                    # change canvas size approx to video size
                    self.canvas.config(width=self.vid_width, height=self.vid_height)
                    # Reset frame count
                    self.frame = 0
                    self.delay = 1 / self.vid.fps

                    # Update the video path text field
                    self.window.Element("_FILEPATH_").Update(video_path)

            if event == "Play":
                if self.play:
                    #self.play = False
                    cv2.waitKey(0)
                    self.window.Element("Play").Update("Play")
                    print(" --- ", self.stop_frame)
                else:
                    #self.play = True

                    self.window.Element("Play").Update("Pause")
            # if event ==

            if event == 'Next frame':
                # Jump forward a frame TODO: let user decide how far to jump
                self.set_frame(self.frame + 1)

            if event == 'Last frame':
                # Jump forward a frame TODO: let user decide how far to jump
                self.set_frame(self.frame - 1)

            if event == "slider":
                # self.play = False
                self.set_frame(int(values["slider"]))
                # print(values["slider"])
        # Exiting
        print("Allah Kurtarsin :)")
        self.window.Close()
        sys.exit()

    #################
    # Video methods #
    #################
    def load_video(self):
        """Start video display in a new thread"""
        thread = threading.Thread(target=self.update, args=())
        thread.daemon = 1
        thread.start()

    def update(self):
        """Update the canvas element with the next video frame recursively"""
        start_time = time.time()
        if self.vid:
            if self.play:

                # Get a frame from the video source only if the video is supposed to play
                ret, frame = self.vid.get_frame()

                if ret:
                    self.photo = PIL.ImageTk.PhotoImage(
                        image=PIL.Image.fromarray(frame).resize((self.vid_width, self.vid_height), Image.NEAREST)
                    )
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

                    self.frame += 1
                    self.update_counter(self.frame)

            # Uncomment these to be able to manually count fps
                #print(str(self.next) + " It's " + str(time.ctime()))
            # self.next = int(self.next) + 1
        # The tkinter .after method lets us recurse after a delay without reaching recursion limit. We need to wait
        # between each frame to achieve proper fps, but also count the time it took to generate the previous frame.
        self.canvas.after(abs(int((self.delay - (time.time() - start_time)) * 1000)), self.update)

    def set_frame(self, frame_no):
        """Jump to a specific frame"""
        if self.vid:
            # Get a frame from the video source only if the video is supposed to play
            ret, frame = self.vid.goto_frame(frame_no)
            self.frame = frame_no
            self.update_counter(self.frame)

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(
                    image=PIL.Image.fromarray(frame).resize((self.vid_width, self.vid_height), Image.NEAREST))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def update_counter(self, frame):
        """Helper function for updating slider and frame counter elements"""
        self.window.Element("slider").Update(value=frame)
        self.window.Element("counter").Update("{}/{} ".format(frame, self.frames))
        self.window.Element("duration_display").Update("{}".format(str(self.display_duration)))
        self.window.Element("duration_min_display").Update("{}".format(str(self.display_min_duration)))
        # print(frame," --- ",self.frames)
        self.stop_frame = frame


class MyVideoCapture:
    """
    Defines a new video loader with openCV
    Original code from https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
    Modified by me
    """

    def __init__(self, video_source):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        """
        Return the next frame
        """
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return 0, None

    def goto_frame(self, frame_no):
        """
        Go to specific frame
        """
        if self.vid.isOpened():
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)  # Set current frame
            ret, frame = self.vid.read()  # Retrieve frame
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return 0, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


if __name__ == '__main__':
    App()
