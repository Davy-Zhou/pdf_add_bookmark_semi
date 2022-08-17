import sys
from pikepdf import Pdf, OutlineItem
from colorama import init 
import os
from yaml import safe_load
from pywinauto.application import Application
from time import sleep
from chardet import detect
import subprocess
import re
from warnings import simplefilter
from traceback import print_exc


def auto_fetch_bookmark(file_name,ssid):
    #ok TODO file_name解析
    path = "书签获取小工具2015.05.05【晴天软件】.exe"
    app = Application(backend='win32').start(path)
    # 连接软件的主窗口
    dlg_spec = app.window(title_re='书签获取小工具2015.05.05  【晴天软件】*', class_name_re='WTWindow*')
    # 设置焦点，使其处于活动状态
    dlg_spec.set_focus()
    dlg_spec['Edit2'].set_edit_text(ssid)
    # UIA 一直无dlg_spec['Edit'].window_text()
    #ok TODO 注意没书签超时情况
    while dlg_spec['Edit'].window_text()=='' or dlg_spec['Edit'].window_text()[:5]=='【话痨：】':
        pass
    if dlg_spec['Edit'].window_text()[:11]=='没有查询到此SS的书签':
        print("\n没有查询到此SS的书签,请手动获取书签\n")
        print("\033[0;32;40m按Enter键退出！\033[0m\n")
        input()
        sys.exit()

    sleep(1)
    # 获取文本框数据
    with open(file_name,'w+',encoding='utf-8') as f:
        f.write(dlg_spec['Edit'].window_text())
    
    return dlg_spec
    # 关闭窗口
    # dlg_spec.close()    
    

# def parse_params():
    #cancel TODO 参数解析 getopt



# pdf为打开的pdf对象
def recognize_page_offset(pdf):
    #ok TODO 页偏移识别
    content_page=page_offset=None
    for index in range(len(pdf.pages)):
        if pdf.pages[index].label =='i':
            # 目录页码
            content_page=index+1
        elif pdf.pages[index].label =='1':
            # 页偏移
            page_offset=index
            break
        elif index>50:
            # 非标准PDF,无法识别页偏移
            break
    return content_page, page_offset


def format_bookmark():
    config_path=sys.argv[0]
    txt_filename=sys.argv[1].replace('.pdf','.txt')
    page_offset_number=sys.argv[2]
    if len(sys.argv)==4 :
        directory_number=sys.argv[3]
#    print('打开config.yaml','\n')
#    input('调试\n')
    with open(config_path+'\\Config\\config.yaml','r',encoding='utf-8') as f:
#        print(config_path+'\\Config\\config.yaml'+'\n')
#        input('调试\n')
        config=safe_load(f)                                      
#        检测编码GB18030、utf-8
        with open(txt_filename,'rb') as f:
            data = f.read()
            file_encoding = detect(data)['encoding']
            with open(str(txt_filename), 'r', encoding=file_encoding, errors = 'ignore') as f:
                str_list = f.read()
#                书签格式化
                for i in range(len(config['rules'])) :
                    for j in range(len(config['rules'][i]['rule'])):
                        regex_search=config['rules'][i]['rule'][j]['regex_search']
                        regex_repalce=config['rules'][i]['rule'][j]['regex_repalce']
                        if config['rules'][i]['rule'][j]['loaded'] and regex_search!=None and regex_repalce!=None:
                            regex_compiled = re.compile(regex_search, re.M)
                            str_list_re = regex_compiled.sub(regex_repalce, str_list)
                            str_list = str_list_re
#                    加页偏移，后面有页偏移是动态变量加不进yaml
                regex_page_offset = re.compile(r'(\d+)$', re.M)
                str_list = regex_page_offset.sub(r'\1\t+'+str(page_offset_number),str_list)
#                    路径保留空格
                filename=str(txt_filename).split('\\')[-1]
                path_name=str(txt_filename).split(filename)[0]
#                    文件名去空格？
                add_bookmark_filename = path_name+filename.replace(' ', '').split(
                    '.txt')[0]+r"(Bookmark)"+"."+filename.replace(' ', '').split('.')[-1]
                with open(add_bookmark_filename, 'w+', encoding='utf-8-sig') as fw:
                    if len(sys.argv) == 4:
                        if config['options']['bookmark_options']['first_letter_lower']:
                            fw.write('目录\t'+str(directory_number)+'\n'+str_list.lower())
                        else:
                            fw.write('目录\t'+str(directory_number)+'\n'+str_list)
                    elif len(sys.argv)==3:
                        if config['options']['bookmark_options']['first_letter_lower']:
                            fw.write(str_list.lower())
                        else:
                            fw.write(str_list)
#               初次格式化完书签，再次使用Notepad3编辑修正
                print("\n书签部分格式化完成，请在打开的编辑器修正书签文件，并\033[0;31;40m修正完后关闭编辑器！\033[0m\n")
                if config['options']['global_options']['enable_editor']:
                    editor_path=(config['options']['global_options']['editor_path'] if ':'  in config['options']['global_options']['editor_path'] else config_path+config['options']['global_options']['editor_path'])
                    # print(editor_path,'\n')
                    subprocess.run([editor_path,add_bookmark_filename])


def pike_add_bookmark():
    config_path=sys.argv[0]
    txt_filename=sys.argv[1].replace('.pdf','.txt')
    pdf_name = str(txt_filename).split('.txt')[0]+"."+"pdf"
    filename=str(txt_filename).split('\\')[-1]
    path_name=str(txt_filename).split(filename)[0]
    bookmark_filename = path_name+filename.replace(' ', '').split(
        '.txt')[0]+r"(Bookmark)"+"."+filename.replace(' ', '').split('.')[-1]
    with open(config_path+'\\Config\\config.yaml','r',encoding='utf-8') as f:
        config=safe_load(f)
        with Pdf.open(pdf_name,allow_overwriting_input=True) as pdf:
            with pdf.open_outline() as outline:
                # 是否清空原PDF书签
                if config['options']['bookmark_options']['clear_origin_bookmark']:
                    outline.root.clear()
                    # 记得改先前config[]
                with open(bookmark_filename, 'r', encoding='utf-8-sig') as fb:
                    for line in fb.readlines():          
                        txt_line = line.split('\t')
                        offset=''
#                        判断页偏移是否存在
                        if len(txt_line)>1 and txt_line[-1].strip().strip('+').isdigit():
                            offset = ((int(txt_line[-2]) + int(txt_line[-1]))
                                    if txt_line[-2].isdigit() else  int(txt_line[-1]))-1
                        # 一级书签
                        # Page counts are zero-based
                        if txt_line[0] != '':
                            L1_item = OutlineItem(txt_line[0], offset)
                            outline.root.append(L1_item)
                        # 二级书签
                        # TODO 书签层级不连续
                        elif 'L1_item' in locals() and txt_line[1] != '':
                            L2_item = OutlineItem(txt_line[1], offset)
                            L1_item.children.append(L2_item)
                        # 三级书签
                        elif 'L2_item' in locals() and txt_line[2] != '':
                            L3_item = OutlineItem(txt_line[2], offset)
                            L2_item.children.append(L3_item)
#                        四级书签
                        elif 'L3_item' in locals() and txt_line[3] != '':
                            L4_item = OutlineItem(txt_line[3], offset)
                            L3_item.children.append(L4_item)
                        else:
                            print("\n\033[0;31;40m该书签和上级书签层级不连续，麻烦手动调整:\033[0m"+"\033[0;32;40m"+line+"\033[0m\n")
                            print("\033[0;32;40m按Enter键退出！\033[0m\n")
                            input()
                            sys.exit()
            pdf.save(pdf_name)


def main():
    init()
    simplefilter('ignore', category=UserWarning)
    os.system("title " + "pdf_add_bookmark_semi@DavyZhou v0.52")
    print("代码更新请访问："+"\033[0;32;40m https://github.com/Davy-Zhou/pdf_add_bookmark_semi \033[0m"+"\n")
    if len(sys.argv)==1:
        # 这段代码方便双击使用
        print("新增自动化获取书签和识别PDF页偏移功能，\033[0;32;40m直接拖入需要加书签的pdf即可,pdf文件名务必加ssid号还有双引号\033[0m\n")
        print("使用示例:  \033[0;32;40m\"C语言大学实用教程第4版_14133899.pdf\" \033[0m\n")
        print("无法自动获取书签请按以下格式输入：  \033[0;32;40m书签txt文件名(务必加双引号) 正文页偏移 目录页码(参数可选)\033[0m\n")
        print("使用示例:  \033[0;32;40m\"C语言大学实用教程第4版.txt\" 10 7 \033[0m\n")
        params =input("请输入： ").split('\"')
        # 拿到代码文件路径，得配置文件绝对路径
        py_dirname, py_name = os.path.split(os.path.abspath(sys.argv[0]))
        sys.argv.clear()
        sys.argv.extend([py_dirname])
        # 判断是否自动获取书签
        if params[1].lower().endswith('pdf',len(params[1])-3,len(params[1])):
            sys.argv.extend([params[1]])
        elif params[1].lower().endswith('txt',len(params[1])-3,len(params[1])):
            # 兼容命令行模式
            sys.argv.extend([params[1]])
            sys.argv.extend(params[-1].split())
        else:
            print("\033[0;31;40m 拖入文件必须是txt或pdf文件 \033[0m\n\n")
            print("\033[0;32;40m按Enter键退出！\033[0m\n")
            input()
            sys.exit()

    else:
        # 适配命令行模式
        py_dirname, py_name = os.path.split(os.path.abspath(sys.argv[0]))
        sys.argv[0]=py_dirname
    pdf_filename=str(sys.argv[1]).split('\\')[-1].replace('txt','pdf')

    if len(sys.argv)<3 and sys.argv[1].lower().endswith('txt',len(sys.argv[1])-3,len(sys.argv[1])) :
       print("\n错误：参数不足\n使用示例:  \"C语言大学实用教程第4版.txt\" 17 12\n或者:  \"C语言大学实用教程第4版.txt\" 17\n")
       sys.exit()

    # 解析ssid
    if sys.argv[1].lower().endswith('pdf',len(sys.argv[1])-3,len(sys.argv[1])):
        #ok TODO自动获取书签，并返回主窗口,前面命令行参数都得改
        bookmark_filename=str(sys.argv[1]).replace('pdf','txt')
        ssid=re.findall('\d{8}',str(sys.argv[1]).split('\\')[-1])
        if ssid==[]:
            print("\n 无法识别SSID,请手动添加SSID到pdf文件名上面\n")
            print("\033[0;32;40m按Enter键退出！\033[0m\n")
            input()
            sys.exit()
        dlg_spec=auto_fetch_bookmark(bookmark_filename,ssid[0])
        dlg_spec.close()
        sleep(1)
        with Pdf.open(str(sys.argv[1]),allow_overwriting_input=True) as pdf:
            content_page, page_offset=recognize_page_offset(pdf)
            if page_offset==None or page_offset==0:
                print("\n 无法识别页偏移,请使用第二种模式手动计算页偏移加书签\n")
                print("\033[0;32;40m按Enter键退出！\033[0m\n")
                input()
                sys.exit()
            sys.argv.append(page_offset)
            if content_page!=None:
                sys.argv.append(content_page)

    format_bookmark()
    print("是否给《\033[0;32;40m"+pdf_filename+"\033[0m》加书签(Y/N)?\n")
    is_add_bookmark=input()
    if is_add_bookmark.lower() != 'y':
        print("\n仅完成书签部分格式化！\n")
        print("\033[0;32;40m按Enter键退出！\033[0m\n")
        input()
        sys.exit()
    pike_add_bookmark()
    print("\n\033[0;32;40m"+pdf_filename+"\033[0m 加书签完成！\n\n")
    print("\033[0;32;40m按Enter键退出！\033[0m\n")
    input()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('\n')
        print_exc()
        print("\n\033[0;32;40m程序运行有问题，记录出错信息，按enter键退出\033[0m\n")
        input()
