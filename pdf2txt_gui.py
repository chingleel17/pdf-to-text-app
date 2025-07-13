import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import os
import configparser

# 配置文件路徑
config_file = 'config.ini'


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        config['DEFAULT'] = {
            'LastPDFPath': '',
            'LastOutputDir': os.path.expanduser('~/Downloads')
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    return config


def save_config(pdf_path, output_dir):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'LastPDFPath': pdf_path, 'LastOutputDir': output_dir}
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def pdf_to_text(pdf_path, txt_path):
    try:
        # 展開 ~ 為完整路徑
        pdf_path = os.path.expanduser(pdf_path)
        txt_path = os.path.expanduser(txt_path)
        # 確保目錄存在
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        # 打開 PDF 文件
        pdf_document = fitz.open(pdf_path)
        # 創建一個空的文本文件
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # 遍歷每一頁
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text()
                txt_file.write(text)
        messagebox.showinfo("成功", "PDF 轉換為文本成功！")
    except Exception as e:
        messagebox.showerror("錯誤", f"轉換失敗: {e}")


def select_pdf_file():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, pdf_path)
        # 預設輸出檔案名為輸入檔案名
        default_txt_name = os.path.splitext(
            os.path.basename(pdf_path))[0] + ".txt"
        txt_entry.delete(0, tk.END)
        txt_entry.insert(0, default_txt_name)


def select_output_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, output_dir)


def generate_unique_filename(directory, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
    return new_filename


def convert_pdf_to_text():
    pdf_path = pdf_entry.get()
    output_dir = output_dir_entry.get()
    txt_name = txt_entry.get()
    if pdf_path and output_dir and txt_name:
        txt_name = generate_unique_filename(output_dir, txt_name)
        txt_path = os.path.join(output_dir, txt_name)
        pdf_to_text(pdf_path, txt_path)
        save_config(pdf_path, output_dir)
    else:
        messagebox.showwarning("警告", "請選擇 PDF 檔案、輸出位置和輸出檔案名")


# 創建主窗口
root = tk.Tk()
root.title("PDF 轉換為文本 v1.0")

# 加載配置
config = load_config()

# PDF 檔案選擇
tk.Label(root, text="選擇 PDF 檔案:").grid(row=0, column=0, padx=10, pady=10)
pdf_entry = tk.Entry(root, width=50)
pdf_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="瀏覽", command=select_pdf_file).grid(row=0,
                                                         column=2,
                                                         padx=10,
                                                         pady=10)
pdf_entry.insert(0, os.path.dirname(config['DEFAULT']['LastPDFPath']))

# 輸出位置選擇
tk.Label(root, text="選擇輸出位置:").grid(row=1, column=0, padx=10, pady=10)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="瀏覽", command=select_output_directory).grid(row=1,
                                                                 column=2,
                                                                 padx=10,
                                                                 pady=10)
output_dir_entry.insert(0, config['DEFAULT']['LastOutputDir'])

# 輸出檔案名
tk.Label(root, text="輸出檔案名:").grid(row=2, column=0, padx=10, pady=10)
txt_entry = tk.Entry(root, width=50)
txt_entry.grid(row=2, column=1, padx=10, pady=10)

# 轉換按鈕
tk.Button(root, text="轉換", command=convert_pdf_to_text).grid(row=3,
                                                             column=0,
                                                             columnspan=3,
                                                             pady=20)

# 運行主循環
root.mainloop()
