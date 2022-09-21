import glob
import os
import shutil

import cv2
from PIL import Image, ImageDraw, ImageFont

CHARS_STR = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
CHARS_REDUCED = [CHARS_STR[c] for c in range(len(CHARS_STR)) if c % 3 == 0]
CHARS_ARR = CHARS_REDUCED + [" " for i in range(len(CHARS_REDUCED) // 2)]
CHARS_ARR_R = list(reversed(CHARS_ARR))
IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "webp"]
VIDEO_EXTENSIONS = ["mp4", "avi", "webm"]
FONT_PATH = r"source\RobotoMono-Medium.ttf"


class Frame:
    def __init__(self, fullPath, image) -> None:
        try:
            self.canvas = cv2.imread(fullPath) if image else fullPath
        except Exception as e:
            print(e)

    def prepare(self, width):
        self.canvas = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        height = round((width / self.canvas.shape[1]) * self.canvas.shape[0])
        self.canvas = cv2.resize(
            self.canvas, (width, height), interpolation=cv2.INTER_AREA
        )
        self.dim = self.canvas.shape
        self.canvas = self.canvas.flatten()


class ProcessImage:
    def __init__(self, name, width, image) -> None:
        self.width = width
        self.main_frame = Frame(name, image)
        self.main_frame.prepare(width)

    def run(self, charArray):
        as_text = [
            charArray[pixel * len(charArray) // 255] for pixel in self.main_frame.canvas
        ]
        as_text = "".join(as_text)
        as_text = [
            as_text[w: w + self.width + 1] for w in range(0, len(as_text), self.width)
        ]
        return as_text


class ProcessVideo:
    def __init__(self, path, width) -> None:
        self.video = cv2.VideoCapture(path)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        if not self.video.isOpened():
            print("Error, video could not be opened")
            exit()

    def run(self, counter, charArray, width):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, counter)
        ret, frame = self.video.read()
        if ret:
            frame_proc = ProcessImage(frame, width, False)
            return frame_proc.run(charArray)


class ExportPhoto:
    def __init__(self, as_text, font_path, font_size=16) -> None:
        self.as_text = as_text
        self.row_count = len(as_text)
        self.font_in_px = font_size
        self.font = ImageFont.truetype(font_path, font_size)
        self.row_dimensions = self.font.getbbox(self.as_text[0])

    def save_as_image(self, dest_path, name="export", format="png"):
        image = Image.new(
            "RGB", (self.row_dimensions[2] + 2, (self.row_count * self.font_in_px) + 2)
        )
        draw = ImageDraw.Draw(image)
        y = 1
        for row in self.as_text:
            draw.text((1, y), row, fill=(255, 255, 255), font=self.font)
            y += self.font_in_px
        file_name = name + "." + format
        image.save(os.path.join(dest_path, file_name))

    def print_in_terminal(self):
        print(*self.as_text, sep="\n")

    def save_as_text(self, dest_path, file_name="export.txt"):
        text_file = os.path.join(dest_path, file_name)
        with open(text_file, "w") as f:
            for row in self.as_text:
                f.write(row + "\n")


class ExportVideo:
    def __init__(self, proc_video) -> None:
        self.proc_video = proc_video

    def prep_frame_array(self, width, chars):
        frame_array = list()
        video_proc = self.proc_video
        f_counter = 0
        while f_counter < video_proc.frame_count:
            frame_string = "\n".join(video_proc.run(f_counter, chars, width))
            frame_array.append(frame_string)
            f_counter = f_counter + 3
        return frame_array

    def save_as_video(self, dest_path, width, chars):
        saveVideo = SaveVideo(self.proc_video, dest_path)
        saveVideo.run(chars, width)


class SaveVideo:
    def __init__(self, proc_video, dest_path, save_name="export") -> None:
        self.proc_video = proc_video
        self.save_name = os.path.join(dest_path, save_name + ".mp4")

    def run(self, chars, width):
        frame_counter = 0
        self.total_frames = 0
        os.mkdir("frames")
        os.system("attrib +h frames")
        while frame_counter < self.proc_video.frame_count:
            frame_as_text = self.proc_video.run(frame_counter, chars, width)
            export_photo = ExportPhoto(frame_as_text, FONT_PATH)
            frame_counter = frame_counter + 3
            self.total_frames = self.total_frames + 1
            export_photo.save_as_image(name=str(self.total_frames), dest_path="frames")
        sample_frame = "frames/" + str(self.total_frames) + ".png"
        with Image.open(sample_frame) as img:
            dimensions = img.size
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(self.save_name, fourcc, 10, dimensions)
        frame_path = os.getcwd() + "/frames/*.png"
        for filename in glob.glob(frame_path):
            img = cv2.imread(filename)
            writer.write(img)
        writer.release()
        shutil.rmtree("frames")
