import sys
import os
import re

headline = ['#', '##', '###', '####', '#####', '######']
title_sign_list = []
"""用于判断标题产生环境"""
titles_added_number = []
"""保存嵌入了编号的标题，用于产生新编号"""
is_continue = 'n'


def add_number_for_line(line_which_is_title, title_sign):
    """给某一行添加编号"""

    global is_continue
    global title_sign_list
    global titles_added_number

    title_sign_list.append(title_sign)
    if len(title_sign_list) == 1:  # 如果line_which_is_title是第一个标题
        titles_added_number.append(line_which_is_title.replace(title_sign + ' ', title_sign + ' 1. '))
        return titles_added_number[0]
    else:
        # 当标题级别为一级(需要标号为1.,2.,3.,...)
        for title in titles_added_number[::-1]:
            number = title.lstrip().split(' ')[1]
            sign = title.lstrip().split(' ')[0]
            if number.count('.') == 1:  # 如果发现一级标题(序号为1.,2.,3.,...)
                if len(title_sign) == len(sign):  # 如果line_which_is_title是一级标题（与发现的一级标题title级别相同）
                    titles_added_number.append(
                        line_which_is_title.replace(title_sign + ' ',
                                                    title_sign + ' ' + str(int(number[:-1]) + 1) + '. '))
                    return titles_added_number[-1]
                elif len(title_sign) < len(sign):  # 如果line_which_is_title是一级标题（比发现的第一个一级标题级别更高）
                    if is_continue != 'y':
                        print(
                            'Markdown文件中的：\n' + title.strip() + '或\n' + line_which_is_title + "\n不规范\n建议将Markdown文件中的标题分级、规范地写好后再继续")
                        is_continue = input('是否忽略此类警告并继续？（y/n）')
                    if is_continue.strip().lower() == 'y':
                        titles_added_number.append(line_which_is_title.replace(title_sign + ' ', title_sign + ' ' + str(
                            int(number[:-1]) + 1) + '. '))
                        return titles_added_number[-1]
                    elif is_continue.strip().lower() == 'n':
                        os._exit(0)
                    else:
                        print('接收到y/n以外的输入，默认退出')
                        os._exit(0)
                else:
                    break
        # 当标题级别不是一级(序号不是1.,2.,3.,...)
        number = titles_added_number[-1].lstrip().split(' ')[1]
        if number.count('.') == 1:  # 如果line_which_is_title的上一级标题为一级标题(序号为1.,2.,3.,...)
            titles_added_number.append(
                line_which_is_title.replace(
                    title_sign + ' ', title_sign + ' ' + number + '1' + '. '))
            return titles_added_number[-1]
        elif len(title_sign_list[-1]) > len(title_sign_list[-2]):  # 如果line_which_is_title的上一个标题比它更高
            number = re.search('(.*\\.\\d+)[^\\d]?$', number)
            if number is not None:
                number = number.group(1)
                titles_added_number.append(
                    line_which_is_title.replace(
                        title_sign + ' ', title_sign + ' ' + number + '.1' + '. '))
            return titles_added_number[-1]
        elif len(title_sign_list[-1]) == len(title_sign_list[-2]):  # 如果line_which_is_title与上一个标题等级别
            number_suf = re.search('(.*\\.)(\\d+)[^\\d]?$', number)
            if number_suf is not None:
                number_suf = number_suf.group(2)
            number_pre = re.search('(.*\\.)(\\d+)[^\\d]?$', number)
            if number_pre is not None:
                number_pre = number_pre.group(1)
            if number_suf is not None and number_pre is not None:
                titles_added_number.append(
                    line_which_is_title.replace(
                        title_sign + ' ', title_sign + ' ' + number_pre + str(int(number_suf) + 1) + '. '))
            return titles_added_number[-1]
        elif len(title_sign_list[-1]) < len(title_sign_list[-2]):  # 如果line_which_is_title的上一个标题比它更低
            for title in titles_added_number[::-1]:
                number = title.lstrip().split(' ')[1]
                sign = title.lstrip().split(' ')[0]
                if len(number) == 2 and number.count('.') == 1:  # 如果先发现一级标题
                    if is_continue != 'y':
                        print(
                            'Markdown文件中的：\n' + title.strip() + '\n或\n' + line_which_is_title + "\n不规范\n建议将Markdown文件中的标题分级、规范地写好后再继续")
                        is_continue = input('是否忽略此类警告并继续？（y/n）')
                    if is_continue.strip() == 'y':
                        titles_added_number.append(line_which_is_title.replace(title_sign + ' ', title_sign + ' ' + str(
                            int(number[:-1]) + 1) + '. '))
                        return titles_added_number[-1]
                    elif is_continue.strip() == 'n':
                        os._exit(0)
                    else:
                        print('接收到y/n以外的输入，默认退出')
                        os._exit(0)
                if len(sign) == len(title_sign):  # 如果找到等级别标题
                    number_suf = re.search('(.*\\.)(\\d+)[^\\d]?$', number)
                    if number_suf is not None:
                        number_suf = number_suf.group(2)
                    number_pre = re.search('(.*\\.)(\\d+)[^\\d]?$', number)
                    if number_pre is not None:
                        number_pre = number_pre.group(1)
                    if number_suf is not None and number_pre is not None:
                        titles_added_number.append(
                            line_which_is_title.replace(
                                title_sign + ' ', title_sign + ' ' + number_pre + str(int(number_suf) + 1) + '. '))
                    return titles_added_number[-1]


def create_lines_with_number(lines_in_file):
    """给传入内容添加编号"""

    for i in range(len(lines_in_file)):
        title_sign = lines_in_file[i].lstrip().split(' ')
        if title_sign[0] in headline:
            origin_line = lines_in_file[i]
            lines_in_file[i] = add_number_for_line(origin_line, title_sign[0])
            print(lines_in_file[i])
    return lines_in_file


def create_markdown_file_with_number(f):
    """生成添加了标题编号的文件"""

    lines_in_file = f.readlines()
    f.close()
    lines_in_file_with_number = create_lines_with_number(lines_in_file)
    # 根据原文件名生成标题添加了序号的文件的文件名
    markdown_file_with_number = f.name[::-1].split('.', 1)[1][::-1] + '_withNum.md'
    if not os.path.exists(markdown_file_with_number):
        with open(markdown_file_with_number, 'w+', encoding='utf-8') as f:
            for line in lines_in_file_with_number:
                f.write(line)
            print('文件已生成: %s' % markdown_file_with_number)
    else:
        if input('文件已存在，是否覆盖 ' + markdown_file_with_number + ' (y/n)').lower() == 'y':
            with open(markdown_file_with_number, 'w+', encoding='utf-8') as f:
                for line in lines_in_file_with_number:
                    f.write(line)
                print('文件已生成: %s' % markdown_file_with_number)
        else:
            print('程序退出')


file_name = ''
# 如果未传入文件，则查找当前目录是否有Markdown文件
if len(sys.argv) < 2:
    path = os.getcwd()
    file_and_dir = os.listdir(path)
    md_file = []
    for item in file_and_dir:
        if item.split('.')[-1].lower() in ['md', 'mdown', 'markdown'] and os.path.isfile(item):
            md_file.append(item)
    if len(md_file) != 0:
        print('当前目录下的Markdown文件：')
        for file in md_file:
            print(file)
        file_name = input('请输入文件名(含后缀)或回车选择第一个文件\n')
        if not file_name:
            file_name = md_file[0]
    else:
        print('该目录下无Markdown文件')
        os._exit(0)
else:
    file_name = sys.argv[1]
if os.path.exists(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        create_markdown_file_with_number(f)
else:
    msg = "未找到文件"
    print(msg)
