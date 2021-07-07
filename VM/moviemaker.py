import subprocess
import pathlib
import os


class MovieMaker:

    def __init__(self, movie_name, movie_format='.mp4', framerate=60):
        self.movie_name = movie_name
        self.movie_format = movie_format
        self.framerate = framerate
        self.current_dir = str(pathlib.Path(__file__).parent.absolute())
        self.input_imgSequence_path = self.current_dir + "\img_sequence\\anim.001.%04d.png"
        self.output_file_path = os.path.dirname(self.current_dir) + '\\few_animations\\' + self.movie_name + self.movie_format

    def makeMovie(self):
        input_seq = self.input_imgSequence_path
        output = self.output_file_path
        cmd = f'ffmpeg -r {self.framerate} -f image2 -s 1920x1080 -i "{input_seq}" -vcodec libx264 -crf 8 -pix_fmt yuv420p "{output}"'
        subprocess.check_output(cmd, shell=True)

    def del_img_seq(self):
        subprocess.check_output('rmdir /s /q ' + self.current_dir + '\img_sequence', shell=True)
        subprocess.check_output('mkdir ' + self.current_dir + '\img_sequence', shell=True)

