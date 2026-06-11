from pypdf import PdfWriter
import os

from pdfmerge import main as merge_main
from pdfsplit import main as split_main
from pdfdelete import main as delete_main
    
def menu():
    while True:
        
        print("\n===PDF編集ツール===")
        print("1.PDF結合")
        print("2.PDF分割")
        print("3.PDF削除")
        print("4.終了")
        
        choice = input("番号を入力してください：")
        
        if choice == "1":
            merge_main()       
        elif choice == "2":
            split_main()
        elif choice == "3":
            delete_main()    
        elif choice == "4":
            print("終了します")
            break
        else:
            print("1～4の数字を入力してください")
if __name__ == "__main__":
    menu()