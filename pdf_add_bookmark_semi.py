import sys
import format_bookmark as fbk
from pikepdf import Pdf, OutlineItem
from colorama import init 
import os

def pike_add_bookmark():
    txt_filename=sys.argv[1]
    pdf_name = str(txt_filename).split('.txt')[0]+"."+"pdf"
    filename=str(txt_filename).split('\\')[-1]
    path_name=str(txt_filename).split(filename)[0]
    bookmark_filename = path_name+filename.replace(' ', '').split(
        '.txt')[0]+r"(Bookmark)"+"."+filename.replace(' ', '').split('.')[-1]

    with Pdf.open(pdf_name,allow_overwriting_input=True) as pdf:
        with pdf.open_outline() as outline:
            with open(bookmark_filename, 'r', encoding='utf-8-sig') as fb:
                for line in fb.readlines():          
                    txt_line = line.split('\t')
                    offset=''
                    if len(txt_line)>1:
                        offset = ((int(txt_line[-2]) + int(txt_line[-1]))
                                if txt_line[-2].isdigit() else  int(txt_line[-1]))-1
                    # 一级书签
                    # Page counts are zero-based
                    if txt_line[0] != '':
                        L1_item = OutlineItem(txt_line[0], offset)
                        outline.root.append(L1_item)
                    # 二级书签
                    elif txt_line[1] != '':
                        L2_item = OutlineItem(txt_line[1], offset)
                        L1_item.children.append(L2_item)
                    # 三级书签
                    elif txt_line[2] != '':
                        L3_item = OutlineItem(txt_line[2], offset)
                        L2_item.children.append(L3_item)
#                    四级书签
                    elif txt_line[3] != '':
                        L4_item = OutlineItem(txt_line[3], offset)
                        L3_item.children.append(L4_item)
        pdf.save(pdf_name)

if __name__ == "__main__":
#    方便双击使用
    init()
    if len(sys.argv)==1:
        print("\n请按格式输入：  \033[0;32;40m书签内容文件名 正文页偏移 目录页码(参数可选)\033[0m\n")
        print("使用示例:  \033[0;32;40m\"C语言大学实用教程第4版.txt\" 10 7 \033[0m\n\n")
        params =input("请输入： ").split('\"')
#        print(params,'\n')
#        input('调试\n')
        py_dirname, py_name = os.path.split(os.path.abspath(sys.argv[0]))
        sys.argv.clear()
        sys.argv.extend([py_dirname])
        sys.argv.extend([params[1]])
        sys.argv.extend(params[-1].split())
#        print(sys.argv,'\n')
#        input('调试\n')
    else:
        py_dirname, py_name = os.path.split(os.path.abspath(sys.argv[0]))
        sys.argv[0]=py_dirname
    filename=str(sys.argv[1]).split('\\')[-1].replace('txt','pdf')
#    print(filename,'\n')
#    input('调试\n')
    if len(sys.argv)<3 :
       print("\n错误：参数不足\n使用示例:  \"C语言大学实用教程第4版.txt\" 17 12\n或者:  \"C语言大学实用教程第4版.txt\" 17\n")
       sys.exit()
#    print('进入format_bookmark','\n')
#    input('调试\n')
    fbk.format_bookmark()
    print("是否给《\033[0;32;40m"+filename+"\033[0m》加书签(Y/N)?\n")
    is_add_Bookmark=input()
    if is_add_Bookmark.lower() != 'y':
        print("\n仅完成书签部分格式化！\n")
        print("\033[0;32;40m按Enter键退出！\033[0m\n")
        input()
        sys.exit()
    pike_add_bookmark()
    print("\n\033[0;32;40m"+filename+"\033[0m 加书签完成！\n\n")
    print("\033[0;32;40m按Enter键退出！\033[0m\n")
    input()
