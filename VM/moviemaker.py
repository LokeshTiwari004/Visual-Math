import subprocess
import pathlib
import os

import pygame


class MovieMaker:

    def __init__(self, img_seq, movie_name, movie_format='.mp4', framerate=30):
        self.framerate = framerate
        self.current_dir = str(pathlib.Path(__file__).parent.absolute())
        self.input_imgSequence_path = self.current_dir + '\img_sequence\\' + str(img_seq)
        self.output_file_path = os.path.dirname(self.current_dir) + '\\few_animations\\' + movie_name + movie_format

    def make_movie(self):
        # cmd = f'ffmpeg -r {self.framerate} -f image2 -s 1920x1080 -i "{self.input_imgSequence_path}" -vcodec libx264 -crf 15 -pix_fmt yuv420p "{self.output_file_path}"'
        cmd = f'ffmpeg -r 30 -i "{self.input_imgSequence_path}" -y "{self.output_file_path}"'
        subprocess.check_output(cmd, shell=True)

    def del_img_seq(self):
        subprocess.check_output('rmdir /s /q ' + self.current_dir + '\img_sequence', shell=True)
        subprocess.check_output('mkdir ' + self.current_dir + '\img_sequence', shell=True)


def del_img_seq():
    current_dir =  str(pathlib.Path(__file__).parent.absolute())
    subprocess.check_output('rmdir /s /q ' + current_dir + '\img_sequence', shell=True)
    subprocess.check_output('mkdir ' + current_dir + '\img_sequence', shell=True)


class FrameHandler:

    def __init__(self, screen, name='anim', scene=1, padding_digits=5, img_format='.png'):
        self.screen = screen
        self.img_format = img_format
        self.name = name
        self.scene = scene
        self.padding_digits = padding_digits

        self.frame_num = 1
        self.frame_skeleton = self.name + '.' + str(self.scene) + '.'
        self.frame_name = self.frame_skeleton + (self.padding_digits-1)*'0' + str(self.frame_num) + self.img_format
        self.frame_sequence = self.name + '.' + str(self.scene) + '.' + '%' + str(self.padding_digits) + 'd' + self.img_format

    def handle_frame_name(self):
        self.frame_num += 1
        digits_in_frame_num = len(str(self.frame_num))
        self.frame_name = self.frame_skeleton + (self.padding_digits - digits_in_frame_num) * '0' + str(self.frame_num) + self.img_format


    def save_frame(self):
        pygame.image.save(self.screen, 'img_sequence/' + self.frame_name)
        self.handle_frame_name()
