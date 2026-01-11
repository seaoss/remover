import os
import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Entry, messagebox
from PIL import Image, ImageDraw
import webbrowser

def browse_file():
    file_path = filedialog.askopenfilename()
    return file_path

def save_image(image, file_path):
    save_path = os.path.join(os.path.dirname(file_path), "output.png")
    image.save(save_path)

def high_quality_matting(image):
    # 将PIL图像转换为OpenCV图像
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 使用GrabCut算法进行抠图
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (0, 0, image.shape[1] - 1, image.shape[0] - 1)
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # 创建一个新的掩码，将前景和可能的前景像素设置为True
    new_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # 使用新的掩码从原始图像中提取前景
    result = image * new_mask[:, :, np.newaxis]

    # 将OpenCV图像转换回PIL图像
    result = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

    return result

def open_website():
    webbrowser.open("http://mail.seaoss.com")

def main():
    root = Tk()
    root.title("图片抠图")

    file_path_label = Label(root, text="图片地址：")
    file_path_label.pack()
    file_path_entry = Entry(root)
    file_path_entry.pack()

    def browse_file_button_clicked():
        file_path = browse_file()
        file_path_entry.delete(0, 'end')
        file_path_entry.insert(0, file_path)

    browse_file_button = Button(root, text="浏览文件", command=browse_file_button_clicked)
    browse_file_button.pack()

    def matting_button_clicked():
        file_path = file_path_entry.get()
        if not file_path:
            print("未选择图片")
            return
        image = Image.open(file_path)
        matted_image = high_quality_matting(image)
        save_image(matted_image, file_path)
        print("抠图成功，已保存到：", os.path.join(os.path.dirname(file_path), "output.png"))

    matting_button = Button(root, text="一键抠图", command=matting_button_clicked)
    matting_button.pack()

    def author_homepage_button_clicked():
        open_website()

    author_homepage_button = Button(root, text="作者主页", command=author_homepage_button_clicked)
    author_homepage_button.pack()

    # 设置窗口居中显示和自适应大小
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

    root.mainloop()

if __name__ == "__main__":
    main()
