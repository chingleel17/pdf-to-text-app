import os
import fitz
from pdf2txt_gui import pdf_to_text


def test_pdf_to_text():
    # 測試 PDF 轉 TXT
    sample_pdf = '/test/sample.pdf'
    sample_txt = '/test/sample.txt'
    # 建立一個簡單 PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello, PDF2TEXT 測試！")
    doc.save(sample_pdf)
    doc.close()
    # 執行轉換
    pdf_to_text(sample_pdf, sample_txt)
    # 驗證內容
    with open(sample_txt, encoding='utf-8') as f:
        content = f.read()
    assert "Hello, PDF2TEXT 測試！" in content
    # 清理
    os.remove(sample_pdf)
    os.remove(sample_txt)
    print("測試通過！")


if __name__ == "__main__":
    test_pdf_to_text()
