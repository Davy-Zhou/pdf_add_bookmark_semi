import subprocess
import re
import sys
#import os
from yaml import safe_load
from chardet import detect

# example
# input: python duxiu_regex.py C语言大学实用教程第4版.txt 17 12
# 3个参数 书签内容文件名 正文页偏移 目录页码

def format_bookmark():
    config_path=sys.argv[0]
    txt_filename=sys.argv[1]
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
                        if config['first_letter_lower']:
                            fw.write('目录\t'+str(directory_number)+'\n'+str_list.lower())
                        else:
                            fw.write('目录\t'+str(directory_number)+'\n'+str_list)
                    elif len(sys.argv)==3:
                        if config['first_letter_lower']:
                            fw.write(str_list.lower())
                        else:
                            fw.write(str_list)
#               初次格式化完书签，再次使用Notepad3编辑修正
                print("\n书签部分格式化完成，请在打开的编辑器修正书签文件，并\033[0;31;40m修正完后关闭编辑器！\033[0m\n")
                if config['enable_editor']:
                    editor_path=(config['editor_path'] if ':'  in config['editor_path'] else config_path+config['editor_path'])
                    subprocess.run([editor_path,add_bookmark_filename])

if __name__ == "__main__":
    format_bookmark()