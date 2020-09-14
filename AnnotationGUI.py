import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas
import numpy as np
import os
import pathlib
import cv2
from LoadCT import *
from Consts import *
from Utils import *
import six
# import PIL
import PIL.ImageTk
from PIL import ImageTk


class LabelingGUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        # 画面作成
        self.root.geometry(WINDOW_SIZE)
        self.root.title(WINDOW_NAME)
        # self.root.bind('<Configure>', self.change_size)

        # ctのディレクトリ
        self.ct_dir = ''
        # raw画像のパス
        self.raw_path = ''

        # メニューバーの作成
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.menu_file = tk.Menu(root)

        # ボタン作成
        self.btn_region_growing = tk.Button(text=BTN_REGION["text"],
                                            command=lambda: self.callback_change_mode(BTN_REGION["text"]))
        self.btn_brush = tk.Button(text=BTN_BRUSH["text"],
                                   command=lambda: self.callback_change_mode(BTN_BRUSH["text"]))
        self.btn_closing = tk.Button(text=BTN_CLOSING["text"],
                                     command=lambda: self.callback_change_mode(BTN_CLOSING["text"]))
        self.btn_eraser = tk.Button(text=BTN_ERASER["text"],
                                    command=lambda: self.callback_change_mode(BTN_ERASER["text"]))

        self.btn_color_R = tk.Button(text=BTN_R["text"], bg="red",
                                     command=lambda: self.callback_change_color(BTN_R["text"]))
        self.btn_color_G = tk.Button(text=BTN_G["text"], bg="green",
                                     command=lambda: self.callback_change_color(BTN_G["text"]))
        self.btn_color_B = tk.Button(text=BTN_B["text"], bg="blue",
                                     command=lambda: self.callback_change_color(BTN_B["text"]))
        self.btn_color_Y = tk.Button(text=BTN_Y["text"], bg="yellow",
                                     command=lambda: self.callback_change_color(BTN_Y["text"]))

        # 各モードで必要なパラメータのスライダーを作成
        self.slider_for_slice = ''
        self.slider_for_brush_width = tk.Scale(label=SLIDER_FOR_BRUSH["title"],
                                               from_=SLIDER_FOR_BRUSH["min"],
                                               to_=SLIDER_FOR_BRUSH["max"],
                                               orient=tk.HORIZONTAL, command=self.callback_mode_slicer)
        self.slider_for_region = tk.Scale(label=SLIDER_FOR_REGION["title"],
                                          from_=SLIDER_FOR_BRUSH["min"],
                                          to_=SLIDER_FOR_REGION["max"],
                                          orient=tk.HORIZONTAL, command=self.callback_mode_slicer)

        # Canvas作成
        self.image_tk = ''
        self.ct_images = ''
        self.mask_images = ''
        self.canvas = ''

        # スライスインデックスに関する変数
        self.slice_index = 0
        self.num_slice = 0

        # マウスの座標
        self.sx = ROW/2
        self.sy = COL/2

        # 色の指定
        # TODO 三色程度選べるようにする
        self.color = COLOR["red"]

        self.window_scale = (1, 1)
        self.interval_for_window_changed = 0

        self.scale = 1
        self.interval_for_zoom = 0
        self.interval_for_brush = 0

        # モード選択
        self.mode = ''

        self.image_history = []

    def change_size(self, event):

        # Main Window以外のイベントは無視
        if (event.type != 'configure') and (event.widget != self.root):
            return

        # サイズが変わっていなかったら無視
        if event.width == self.window_scale[0] * WINDOW_WIDTH:
            if event.height == self.window_scale[1] * WINDOW_HEIGHT:
                return
        # サイズが変わってなかった無視
        # グローバル変数を更新
        self.window_scale = (event.width/WINDOW_WIDTH, event.height/WINDOW_HEIGHT)
        self.interval_for_window_changed += 1

        if self.interval_for_window_changed % 5 == 0 and type(self.ct_images) is not str:
            self.build_canvas()

    def build_menu(self):
        self.menu.add_cascade(label="file", menu=self.menu_file)
        self.menu_file.add_command(label="Open dicom file",
                                   command=lambda: self.callback_open_file(FILE_TYPE["dicom"]))
        self.menu_file.add_command(label="Open raw file",
                                   command=lambda: self.callback_open_file(FILE_TYPE["raw"]))
        self.menu_file.add_command(label="Save raw file",
                                   command=self.execute_save)

    def build_file_dialog(self, file_type):
        if file_type == FILE_TYPE["dicom"]:
            fTyp = [("", "*")]
            iDir = DEFAULT_DIR
            messagebox.showinfo(WINDOW_NAME, 'Dicomファイルを選択してください')
            self.ct_dir = filedialog.askdirectory(initialdir=iDir)
        elif file_type == FILE_TYPE["raw"]:
            fTyp = [("", "*.raw")]
            iDir = DEFAULT_DIR
            messagebox.showinfo(WINDOW_NAME, 'rawファイルを選択してください')
            self.raw_path = filedialog.askopenfilename(initialdir=iDir, filetypes=fTyp)

    def build_layout(self):
        # ボタンを配置
        self.btn_region_growing.place(relx=BTN_REGION["relx"], rely=BTN_REGION["rely"], relwidth=BTN_REGION["relwidth"])
        self.btn_brush.place(relx=BTN_BRUSH["relx"], rely=BTN_BRUSH["rely"], relwidth=BTN_BRUSH["relwidth"])
        self.btn_closing.place(relx=BTN_CLOSING["relx"], rely=BTN_CLOSING["rely"], relwidth=BTN_CLOSING["relwidth"])
        self.btn_eraser.place(relx=BTN_ERASER["relx"], rely=BTN_ERASER["rely"], relwidth=BTN_ERASER["relwidth"])

        self.btn_color_R.place(relx=BTN_R["relx"], rely=BTN_R["rely"], relwidth=BTN_R["relwidth"])
        self.btn_color_G.place(relx=BTN_G["relx"], rely=BTN_G["rely"], relwidth=BTN_G["relwidth"])
        self.btn_color_B.place(relx=BTN_B["relx"], rely=BTN_B["rely"], relwidth=BTN_B["relwidth"])
        self.btn_color_Y.place(relx=BTN_Y["relx"], rely=BTN_Y["rely"], relwidth=BTN_Y["relwidth"])

        # インデックスのスライダーを配置
        self.slider_for_slice = tk.Scale(label=SLIDER_FOR_INDEX["title"], from_=SLIDER_FOR_INDEX["min"],
                                         to_=self.num_slice - 1, orient=tk.HORIZONTAL,
                                         command=self.callback_change_index)

        self.slider_for_slice.place(relx=SLIDER_FOR_INDEX["relx"], rely=SLIDER_FOR_INDEX["rely"],
                                    relwidth=SLIDER_FOR_INDEX["relwidth"])

        self.slider_for_brush_width.set(SLIDER_FOR_BRUSH["default"])
        self.slider_for_region.set(SLIDER_FOR_REGION["default"])

    def build_canvas(self):
        # CT画像とマスク画像から表示用の画像を作成
        ct_image = self.ct_images[self.slice_index, :, :, :]
        mask_image = self.mask_images[self.slice_index, :, :, :]
        show_image = build_show_image(ct_image, mask_image)

        # scale = self.window_scale[0] if self.window_scale[0] < self.window_scale[1] else self.window_scale[1]
        self.canvas = tk.Canvas(width=int(COL*self.window_scale[0]),
                                height=int(ROW*self.window_scale[1]))
        image = PIL.Image.fromarray(show_image)
        # image = image.resize((int(ROW*self.scale), int(COL*self.scale)))
        image = image.resize((int(ROW * self.scale * self.window_scale[0]),
                              int(COL * self.scale * self.window_scale[1])))
        crop_rect = (int(COL*(self.scale - 1)*0.5), int(ROW*(self.scale - 1)*0.5),
                     int(COL*(self.scale + 1)*0.5), int(ROW*(self.scale + 1)*0.5),)
        image = image.crop(crop_rect)
        self.image_tk = PIL.ImageTk.PhotoImage(image)

        # Canvasを作成し, 表示する
        # scale = self.window_scale[0] if self.window_scale[0] < self.window_scale[1] else self.window_scale[1]
        self.canvas = tk.Canvas(width=int(COL * self.window_scale[0]),
                                height=int(ROW * self.window_scale[1]))
        self.canvas.create_image(0, 0, image=self.image_tk, anchor='nw')
        self.canvas.place(relx=CANVAS_FOR_IMAGE["relx"], rely=CANVAS_FOR_IMAGE["rely"])

        # bindを再度定義する
        self.canvas.bind("<ButtonPress-1>", self.callback_pressed_on_canvas)
        self.canvas.bind("<B1-Motion>", self.callback_dragged_on_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.callback_released_on_canvas)
        self.canvas.bind("<B3-MouseWheel>", self.callback_zoom_in_out)
        self.canvas.bind("<MouseWheel>", self.callback_wheeled_on_canvas)
        self.canvas.bind("<Double 3>", lambda event: self.callback_undo(event))

    def callback_change_color(self, color):
        if color == BTN_R["text"]:
            self.color = COLOR["red"]
        elif color == BTN_G["text"]:
            self.color = COLOR["green"]
        elif color == BTN_B["text"]:
            self.color = COLOR["blue"]
        elif color == BTN_Y["text"]:
            self.color = COLOR["yellow"]

    def callback_open_file(self, file_type):
        if file_type == FILE_TYPE["dicom"]:
            while True:
                self.build_file_dialog(file_type)
                self.ct_images = load_ct(self.ct_dir)
                if type(self.ct_images) is not int:
                    break

            if type(self.mask_images) is str:
                self.num_slice = self.ct_images.shape[0]
                self.mask_images = np.zeros(self.ct_images.shape, dtype='uint8')
            elif self.mask_images.shape != self.ct_images:
                self.mask_images = np.zeros(self.ct_images.shape, dtype='uint8')
                print("raw画像とdicom画像が対応していません")

            self.build_layout()
            self.image_history.append(self.mask_images[0].copy())
            self.build_canvas()

        elif file_type == FILE_TYPE["raw"]:
            # TODO rawファイルを読み込む
            # TODO CT画像とsuperimposeする
            while True:
                self.build_file_dialog(file_type)
                self.mask_images = load_raw(self.raw_path)
                if type(self.ct_images) is str:
                    self.num_slice = self.mask_images.shape[0]
                    self.ct_images = np.zeros(self.mask_images.shape, dtype='uint8')
                    break
                elif self.ct_images.shape == self.mask_images.shape:
                    break
                else:
                    print("dicom画像と一致しないrawファイルです")

            print("loaded raw image")
            self.build_layout()
            self.image_history.append(self.mask_images[0].copy())

            self.build_canvas()

    def callback_mode_slicer(self, x):
        if self.mode == BTN_BRUSH["text"]:
            self.slider_for_brush_width.set(x)
        elif self.mode == BTN_REGION["text"]:
            self.slider_for_region.set(x)
        elif self.mode == BTN_CLOSING["text"]:
            pass
        elif self.mode == BTN_ERASER["text"]:
            pass

    def callback_change_index(self, x):
        self.slice_index = int(x)
        self.image_history.clear()
        self.image_history.append(self.mask_images[self.slice_index, :, :, :].copy())
        self.build_canvas()

    def callback_change_mode(self, mode):
        if self.mode == BTN_BRUSH["text"]:
            self.slider_for_brush_width.place_forget()
        elif self.mode == BTN_REGION["text"]:
            self.slider_for_region.place_forget()
        elif self.mode == BTN_CLOSING["text"]:
            pass
        elif self.mode == BTN_ERASER["text"]:
            self.slider_for_brush_width.place_forget()

        self.mode = mode

        if self.mode == BTN_BRUSH["text"]:
            self.slider_for_brush_width.place(relx=SLIDER_FOR_BRUSH["relx"],
                                              rely=SLIDER_FOR_BRUSH["rely"],
                                              relwidth=SLIDER_FOR_BRUSH["relwidth"])
        elif self.mode == BTN_REGION["text"]:
            self.slider_for_region.place(relx=SLIDER_FOR_REGION["relx"],
                                         rely=SLIDER_FOR_REGION["rely"],
                                         relwidth=SLIDER_FOR_REGION["relwidth"])
        elif self.mode == BTN_CLOSING["text"]:
            self.execute_closing()
        elif self.mode == BTN_ERASER["text"]:
            self.slider_for_brush_width.place(relx=SLIDER_FOR_BRUSH["relx"],
                                              rely=SLIDER_FOR_BRUSH["rely"],
                                              relwidth=SLIDER_FOR_BRUSH["relwidth"])

    def callback_pressed_on_canvas(self, event):
        if self.mode == BTN_BRUSH["text"]:
            self.execute_brush(event, mouse_mode=MOUSE_MODE["press"])
        elif self.mode == BTN_REGION["text"]:
            self.execute_region_growing(event)
        elif self.mode == BTN_CLOSING["text"]:
            pass
        elif self.mode == BTN_ERASER["text"]:
            self.execute_erasing(event, mouse_mode=MOUSE_MODE["press"])

    def callback_dragged_on_canvas(self, event):
        if self.mode == BTN_BRUSH["text"]:
            self.execute_brush(event, mouse_mode=MOUSE_MODE["drag"])
        elif self.mode == BTN_REGION["text"]:
            pass
        elif self.mode == BTN_CLOSING["text"]:
            pass
        elif self.mode == BTN_ERASER["text"]:
            self.execute_erasing(event, mouse_mode=MOUSE_MODE["drag"])

    def callback_released_on_canvas(self, event):
        if self.mode == BTN_BRUSH["text"]:
            self.execute_brush(event, mouse_mode=MOUSE_MODE["release"])
        elif self.mode == BTN_REGION["text"]:
            pass
        elif self.mode == BTN_CLOSING["text"]:
            pass
        elif self.mode == BTN_ERASER["text"]:
            self.execute_erasing(event, mouse_mode=MOUSE_MODE["release"])

    def callback_wheeled_on_canvas(self, event):
        if event.delta > 0 and self.slice_index < self.num_slice-1:
            self.slice_index += 1
        elif event.delta < 0 and self.slice_index > 0:
            self.slice_index -= 1

        self.slider_for_slice.set(self.slice_index)
        self.build_canvas()

    def callback_undo(self, event):
        if len(self.image_history) > 1:
            print("Undo")
            a = self.image_history.pop(-1)
            self.mask_images[self.slice_index, :, :, :] = self.image_history[-1].copy()
            self.build_canvas()

    def callback_zoom_in_out(self, event):
        self.scale = self.scale + 0.1 if event.delta > 0 else self.scale - 0.1
        self.build_canvas()

    def execute_brush(self, event, mouse_mode):
        if mouse_mode == MOUSE_MODE["press"]:
            self.interval_for_zoom = 0
            self.sx = event.x
            self.sy = event.y
        elif mouse_mode == MOUSE_MODE["drag"]:
            pre_x = int((self.sx - COL*0.5)/self.scale + COL * 0.5)
            pre_y = int((self.sy - ROW*0.5)/self.scale + ROW * 0.5)
            x = int((event.x - COL*0.5)/self.scale + COL * 0.5)
            y = int((event.y - ROW*0.5)/self.scale + ROW * 0.5)

            if x < 0 or y < 0 or x > COL or y > ROW:
                return

            self.sx = event.x
            self.sy = event.y
            cv2.line(self.mask_images[self.slice_index, :, :, :], (pre_x, pre_y), (x, y),
                     self.color, self.slider_for_brush_width.get())

            if self.interval_for_brush % 3 == 0:
                self.build_canvas()

            self.interval_for_brush += 1

        elif mouse_mode == MOUSE_MODE["release"]:
            self.build_canvas()
            self.image_history.append(self.mask_images[self.slice_index, :, :, :].copy())

    def execute_closing(self):
        kernel = np.ones((5, 5), np.uint8)
        temp = self.mask_images[self.slice_index, :, :, :]
        self.mask_images[self.slice_index, :, :, :] = cv2.morphologyEx(temp,
                                                                       cv2.MORPH_CLOSE, kernel)
        self.build_canvas()
        self.image_history.append(self.mask_images[self.slice_index, :, :, :].copy())
        self.callback_change_mode(BTN_BRUSH["text"])

    def execute_region_growing(self, event):
        self.sy = int((event.x - COL * 0.5) / self.scale + COL * 0.5)
        self.sx = int((event.y - ROW * 0.5) / self.scale + ROW * 0.5)

        if self.sx < 0 or self.sy < 0 or self.sx > COL or self.sy > ROW:
            return

        region_threshold = self.slider_for_region.get()
        # ここを変更すれば領域拡張法の対象がマスクかCtに変更
        ct_image = self.ct_images[self.slice_index, :, :, 0]
        # ct_image = self.mask_images[self.slice_index, :, :, 0].copy()
        segment_image = np.zeros(ct_image.shape, dtype='bool')

        seed = (self.sx, self.sy)
        seed_points = [seed]

        i = 0
        while seed_points:
            temp = seed_points.pop()
            x = temp[0]
            y = temp[1]

            if segment_image[x, y]:
                continue

            i += 1
            segment_image[x, y] = True
            # 右
            if x < ct_image.shape[0] - 1 and abs(int(ct_image[x+1, y]) - int(ct_image[self.sx, self.sy])) <= region_threshold:
                if not segment_image[x+1, y]:
                    seed_points.append((x+1, y))
            # 左
            if x > 0 and abs(int(ct_image[x-1, y]) - int(ct_image[self.sx, self.sy])) <= region_threshold:
                if not segment_image[x-1, y]:
                    seed_points.append((x-1, y))
            # 上
            if y < ct_image.shape[1] - 1 and abs(int(ct_image[x, y+1]) - int(ct_image[self.sx, self.sy])) <= region_threshold:
                if not segment_image[x, y+1]:
                    seed_points.append((x, y+1))
            # 下
            if y > 0 and abs(int(ct_image[x, y-1]) - int(ct_image[self.sx, self.sy])) <= region_threshold:
                if not segment_image[x, y-1]:
                    seed_points.append((x, y-1))

        # TODO 出力用rawデータに書き込む

        # canvasに書き込む
        X, Y = np.where(segment_image)
        for i in range(len(X)):
            x = X[i]
            y = Y[i]
            # なぜかxとyが逆
            self.mask_images[self.slice_index, x, y, :] = self.color

        print("seed ｄｄｄｄ({}, {})".format(self.sx, self.sy))
        self.build_canvas()
        self.image_history.append(self.mask_images[self.slice_index, :, :, :].copy())

    def execute_save(self):
        # マスク画像をraw形式に変換(パレッド的な)
        index = self.mask_images.shape[0]
        row = self.mask_images.shape[1]
        col = self.mask_images.shape[2]
        # TODO さすがにきもいので後で直す

        raw_images = np.zeros(shape=(index, row, col), dtype='uint8')
        for i, mask_image in enumerate(self.mask_images):
            raw_image = np.where(self.mask_images[i, :, :, 0] == COLOR["red"][0],
                                 COLOR_PLATTE_FOR_RAW["red"][0], mask_image[:, :, 0])
            raw_image = np.where(self.mask_images[i, :, :, 1] == COLOR["green"][1],
                                 COLOR_PLATTE_FOR_RAW["green"][1], raw_image)
            raw_image = np.where(self.mask_images[i, :, :, 2] == COLOR["blue"][2],
                                 COLOR_PLATTE_FOR_RAW["blue"][2], raw_image)
            raw_image = np.where(self.mask_images[i, :, :, 2] == COLOR["yellow"][0],
                                 COLOR_PLATTE_FOR_RAW["yellow"][0], raw_image)

            raw_images[i] = raw_image

        raw_images = raw_images.reshape(row*col*index)
        # 保存先のパスを指定する
        initial_dir = pathlib.Path(self.ct_dir).parent
        raw_filename = pathlib.Path(self.ct_dir).name

        raw_file_path = filedialog.asksaveasfilename(initialdir=initial_dir, title=SAVE_MESSAGE,
                                                     filetypes=RAW_FILE)
        raw_images.tofile(raw_file_path + ".raw")

        img_for_show = cv2.cvtColor(self.mask_images[self.slice_index, :, :, :], cv2.COLOR_RGB2BGR)
        cv2.imshow("Mask Image", img_for_show)

    def execute_erasing(self, event, mouse_mode):
        if mouse_mode == MOUSE_MODE["press"]:
            self.interval_for_zoom = 0
            self.sx = event.x
            self.sy = event.y
            x = int((event.x - COL * 0.5) / self.scale + COL * 0.5)
            y = int((event.y - ROW * 0.5) / self.scale + ROW * 0.5)
            cv2.circle(self.mask_images[self.slice_index, :, :, :], center=(x, y),
                       radius=int(self.slider_for_brush_width.get()/2),  thickness=-1,
                       color=COLOR["black"])

        elif mouse_mode == MOUSE_MODE["drag"]:
            pre_x = int((self.sx - COL*0.5)/self.scale + COL * 0.5)
            pre_y = int((self.sy - ROW*0.5)/self.scale + ROW * 0.5)
            x = int((event.x - COL*0.5)/self.scale + COL * 0.5)
            y = int((event.y - ROW*0.5)/self.scale + ROW * 0.5)

            if x < 0 or y < 0 or x > COL or y > ROW:
                return

            self.sx = event.x
            self.sy = event.y
            cv2.line(self.mask_images[self.slice_index, :, :, :], (pre_x, pre_y), (x, y),
                     COLOR["black"], self.slider_for_brush_width.get())

            if self.interval_for_brush % 3 == 0:
                self.build_canvas()

            self.interval_for_brush += 1

        elif mouse_mode == MOUSE_MODE["release"]:
            self.build_canvas()
            self.image_history.append(self.mask_images[self.slice_index, :, :, :].copy())

    def run(self):
        self.build_menu()


def main():
    root = tk.Tk()
    ob = LabelingGUI(root)
    ob.run()
    ob.mainloop()


if __name__ == '__main__':
    main()