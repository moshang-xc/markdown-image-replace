import re
import os
import requests


# Markdown中图片语法 ![](url)
img_patten = r'!\[.*?\]\((.*?)\)'
img_index = 1
img_dict = {}
# 源md文件路径
file_path = 'D:/xxx/xxx'
# 替换路径后输出文件路径
file_out_path = 'D:/xxx/xxx/out'
# 替换路径后图片文件存储地址
img_path = './imgs/'

def get_files_list(dir):
    """
    获取一个目录下所有文件列表，包括子目录
    :param dir:
    :return:
    """
    files_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list

def get_pics_and_replace(md_file):
    with open(md_file, 'r',encoding='utf-8') as f: #使用utf-8 编码打开
        post = f.read()
        matches = re.compile(img_patten).findall(post)
        file_base_name = os.path.basename(md_file)
        global img_index
        if matches and len(matches)>0 :
            # 多个group整合成一个列表
            for match in matches :
                if match and len(match)>0 :
                    filename = os.path.basename(match)
                    filename = filename[filename.index('.'):filename.index('#')]
                    filename = f'{img_path}{img_index}{filename}'
                    img_dict[filename] = match
                    post = post.replace(match, filename)
                    img_index = img_index + 1

        # 如果有内容的话，就直接覆盖写入当前的markdown文件
        if post :
            open(os.path.join(file_out_path,file_base_name), 'w', encoding='utf-8').write(post)

def download_pics(url, key, file):
    img_data = requests.get(url).content

    with open(os.path.join(file, key), 'w+') as f:
        f.buffer.write(img_data)


if __name__ == '__main__':
    files_list = get_files_list(file_path)

    if not os.path.exists(file_out_path):
        os.mkdir(file_out_path)

    for file in files_list:
        print(f'正在处理：{file}')

        get_pics_and_replace(file)

    targer_dir = os.path.join(file_out_path, img_path)
    if not os.path.exists(targer_dir):
        os.mkdir(targer_dir)

    for key in img_dict:
        print(f'正在下载图片 {key} ...')
        download_pics(img_dict[key], key, file_out_path)
    print(f'处理完成。')
