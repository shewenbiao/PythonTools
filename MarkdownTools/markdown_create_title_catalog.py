import sys
import os

headline = ['#', '##', '###', '####', '#####', '######']
lines_in_file = []


def create_catalog_line(line, headline_mark, i):
    """生成目录列表中的某一项"""

    if headline_mark == '#':
        return '* <a href="#' + str(i) + '">' + line[2:-1] + "</a>  \n"
    elif headline_mark == '##':
        return '   * <a href="#' + str(i) + '">' + line[3:-1] + "</a>  \n"
    elif headline_mark == '###':
        return '      * <a href="#' + str(i) + '">' + line[4:-1] + "</a>  \n"
    elif headline_mark == '####':
        return '         * <a href="#' + str(i) + '">' + line[5:-1] + "</a>  \n"
    elif headline_mark == '#####':
        return '            * <a href="#' + str(i) + '">' + line[6:-1] + "</a>  \n"
    elif headline_mark == '######':
        return '               * <a href="#' + str(i) + '">' + line[7:-1] + "</a>  \n"


def create_catalog(f):
    """生成目录列表"""

    i = 0
    catalog_list = ['## <a name="index">Index </a> \n']
    for line in f:
        lines_in_file.append(line)
    f.close()
    length = len(lines_in_file)
    for j in range(length):
        split_line = lines_in_file[j].lstrip().split(' ')
        if split_line[0] in headline:
            # 如果为最后一行且末尾无换行（防最后一个字被去除）
            if j == length - 1 and lines_in_file[j][-1] != '\n':
                catalog_list.append(create_catalog_line(lines_in_file[j] + '\n', split_line[0], i) + '\n')
                lines_in_file[j] = lines_in_file[j].replace(split_line[0] + ' ',
                                                            split_line[0] + ' ' + '<a name="' + str(i) + '">')[
                                   :] + '</a><a style="float:right;text-decoration:none;" href="#index"> [Top]</a>' + "\n"
                i = i + 1
            else:
                catalog_list.append(create_catalog_line(lines_in_file[j], split_line[0], i))
                lines_in_file[j] = lines_in_file[j].replace(split_line[0] + ' ',
                                                            split_line[0] + ' ' + '<a name="' + str(i) + '">')[
                                   :-1] + '</a><a style="float:right;text-decoration:none;" href="#index"> [Top]</a>' + "\n"
                i = i + 1
    return catalog_list


def create_file_with_catalog(f):
    """生成带目录列表的文件"""

    catalog = create_catalog(f)
    file_with_catalog = f.name[::-1].split('.', 1)[1][::-1] + '_withCatalog.md'
    if not os.path.exists(file_with_catalog):
        with open(file_with_catalog, 'w+', encoding='utf-8') as f:
            for catalog_line in catalog:
                f.write(catalog_line)
            for line in lines_in_file:
                f.write(line)
            print('文件已生成:%s ' % file_with_catalog)
    else:
        if input('文件已存在，是否覆盖 ' + file_with_catalog + ' (y/n)').lower() == 'y':
            with open(file_with_catalog, 'w+', encoding='utf-8') as f:
                for catalog_line in catalog:
                    f.write(catalog_line)
                for line in lines_in_file:
                    f.write(line)
                print('文件已生成:%s ' % file_with_catalog)
        else:
            print('程序退出')


if __name__ == '__main__':
    file_name = ''
    # 如果未传入文件名, 则查找当前目录是否有Markdown文件
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
            file_name = input('请输入文件名(含后缀)\n')
        else:
            print('该目录下无Markdown文件')
            os._exit(0)
    else:
        file_name = sys.argv[1]
    if os.path.exists(file_name) and os.path.isfile(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            create_file_with_catalog(f)
    else:
        msg = "未找到Markdown文件"
        print(msg)
