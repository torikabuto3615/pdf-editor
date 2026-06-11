from pypdf import PdfReader, PdfWriter
import os

# pdfを分割する関数
def split_pdf(pdf_file):
    
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)
    
    if total_pages < 2:
        print("2ページ以上のPDFを指定してください")
        return
    
    print(f"\n総ページ数：{total_pages}")
    
    for page_num in range(total_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        
        base_name = os.path.splitext(pdf_file)[0]
        output_file = f"{base_name}_{page_num + 1}.pdf"
        
        with open(output_file, "wb") as output:
            writer.write(output)   
        
        print(f"{output_file}を作成しました")
    print("\n分割完了！")

def main():
    print("===PDF分割ツール===")
    file_path = input("PDFファイル名を入力してください\n（入力が終わったらEnter）：")
    
    if not file_path.lower().endswith(".pdf"):
        file_path += ".pdf"
    
    if not os.path.exists(file_path):
        print("ファイルが存在しません")
        return
    
    if not file_path.lower().endswith(".pdf"):
        print("PDFファイルを指定してください")
        return
    
    split_pdf(file_path)
    
if __name__ == "__main__":
    main()
        