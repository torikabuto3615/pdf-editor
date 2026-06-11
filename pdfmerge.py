from pypdf import PdfWriter
import os
print("★★★★★最新版★★★★★")

# pdfを結合する関数
def merge_pdfs(pdf_files, output_file):
    
    merger = PdfWriter()
    
    for pdf in pdf_files:
        merger.append(pdf)
    
    merger.write(output_file)
    merger.close()
    
    print(f"\n結合完了！")
    print(f"保存先:{output_file}")

def main():
    
    print("===PDF結合ツール===")
    
    pdf_files = []
    
    while True:
        file_path = input("PDFファイル名を入力してください\n（入力が終わったらEnter）:")
        print(f"DEBUG:[{file_path}]")
        
        if file_path == "":
            break
        
        if "." not in file_path:
            file_path += ".pdf"
        
        if not os.path.exists(file_path):
            print("ファイルが存在しません")
            continue
        
        if not file_path.lower().endswith(".pdf"):
            print("PDFファイルを指定してください")
            continue
        
        pdf_files.append(file_path)
        print(f"{len(pdf_files)}件登録しました")
    
    if len(pdf_files) < 2:
        print("結合には２つ以上のPDFが必要です")
        return
    
    output_file = input("出力ファイル名を入力してください（例：merged.pdf):")
    if not output_file.lower().endswith(".pdf"):
        output_file += ".pdf"
    
    merge_pdfs(pdf_files, output_file)

if __name__ == "__main__":
    main()
        