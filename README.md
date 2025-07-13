# PDF2TEXT

這是一個簡單的 GUI 工具，可將 PDF 轉換為純文字檔案。

## 特色
- 支援多頁 PDF 轉換
- 可自訂輸出資料夾與檔名
- 會記錄上次使用的 PDF 路徑與輸出資料夾

## 安裝相依套件
```bash
pip install -r requirements.txt
```

## 執行方式
```bash
python pdf2txt_gui.py
```

## 需求
- Python 3.7 以上
- tkinter
- PyMuPDF (fitz)

## 注意事項
- 輸出預設為使用者下載資料夾
- 若遇到權限問題請以管理員身分執行
