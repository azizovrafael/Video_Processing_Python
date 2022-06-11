import re
from subprocess import check_output


def get_video_duration(path_video):
    '''Get the duration of a video.

    Parameter:
        path_video <str> - The path of the input video.

    Return:
        duration <str> - The duration of the input video formatted as 'hh:mm:ss.msec'.
    '''
    # Create the command for getting the information of the input video via ffprobe.
    global duration
    cmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', path_video]
    # Get the information of the input video via ffprobe command.
    info_byte = check_output(cmd)  # <bytes>
    # Decode the information.
    info_str = info_byte.decode("utf-8")  # <str>
    # Split the information.
    info_list = re.split('[\n]', info_str)

    # Get the duration of the input video.
    for info in info_list:
        if 'duration' in info:
            # E.g., 'info' = 'duration=0:00:01.860000'.
            duration = re.split('[=]', info)[1]
    print("[+] ", duration.split('.')[0])
    return duration.split('.')[0]


a = get_video_duration("9.hevc")
print(a)