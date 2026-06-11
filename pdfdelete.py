from pypdf import PdfReader,  PdfWriter
import os

def delete_pdf(pdf_file):
    
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)
    
    writer = PdfWriter()
    
    if total_pages < 2:
        print("2ページ以上のPDFを指定してください")
        return
    
    print(f"\n総ページ数：{total_pages}")
    try:
        delete_page = int(input("削除したいページ数を入力してください："))
    except ValueError:
        print("数字を入力してください")
        return
    
    if delete_page < 1 or delete_page > total_pages:
        print("存在しないページです")
        return
    
    for i, page in enumerate(reader.pages, start= 1):
        if i != delete_page:
            writer.add_page(page)
    
    output_file = input("出力ファイル名を入力してください（例：page_delete.pdf):")
    if not output_file.lower().endswith(".pdf"): 
        output_file += ".pdf"
        
    with open(output_file, "wb") as output:
            writer.write(output)   
        
    print(f"{output_file}を作成しました")
    print("\n削除完了！")
     
def main():
    print("===PDF削除ツール===")
    file_path = input("PDFファイル名を入力してください\n（入力が終わったらEnter）：")
    if not file_path.lower().endswith(".pdf"):
        file_path += ".pdf"
    
    if not os.path.exists(file_path):
        print("ファイルが存在しません")
        return
    
    if not file_path.lower().endswith(".pdf"):
        print("PDFファイルを指定してください")
        return
    
    delete_pdf(file_path)
        
if __name__ == "__main__":
    main()