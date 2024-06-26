import tkinter as tk

global result_dict
result_dict = {}

global keyword_list
keyword_list = {
    "digital": [], # 数电
    "practical": [], # 生电
    "storage": [],# 储电
    "mechanical": [],# 械电
    "humorous": [],# 沙雕红石
    "tutorial": [],# 教程
    "other": []}# 其他

global relation_list
relation_list = []
def annotation_data(video_dict, page):

    class Data:
        def relation(self, relation):
            result_dict = {
                    "title": video_dict['content'][page]['title'],
                    "description": video_dict['content'][page]['description'],
                    "relation": relation
                }
            print(result_dict)
            relation_list.append(result_dict)
        def add_keyword(self, type):
            keyword_list[type].append(keyword_entry.get())
            print(keyword_list)

    annotation_window = tk.Tk()
    annotation_window.title('数据标注 : ' + str(page + 1) + '/' + str(len(video_dict['content'])))
    annotation_window.geometry('800x600')

    info_box = tk.Text(annotation_window, width=80, height=20)
    info_box.place(x=0, y=0, width=800, height=200)

    info_box.insert(tk.END, video_dict['content'][page]['title'] + '\n' + video_dict['content'][page]['description'])

    relation_button = tk.Button(annotation_window, text='有相关性', command=lambda: Data().relation(True))
    relation_button.place(x=50, y=200, width=300, height=50)

    no_relation_button = tk.Button(annotation_window, text='无相关性', command=lambda: Data().relation(False))
    no_relation_button.place(x=450, y=200, width=300, height=50)

    keyword_entry = tk.Entry(annotation_window)
    keyword_entry.place(x=50, y=300, width=700, height=50)

    digital_button = tk.Button(annotation_window, text='数电', command=lambda: Data().add_keyword('digital'))
    digital_button.place(x=50, y=400, width=100, height=50)

    practical_button = tk.Button(annotation_window, text='生电', command=lambda: Data().add_keyword('practical'))
    practical_button.place(x=150, y=400, width=100, height=50)

    storage_button = tk.Button(annotation_window, text='储电', command=lambda: Data().add_keyword('storage'))
    storage_button.place(x=250, y=400, width=100, height=50)

    mechanical_button = tk.Button(annotation_window, text='械电', command=lambda: Data().add_keyword('mechanical'))
    mechanical_button.place(x=350, y=400, width=100, height=50)

    tutorial_button = tk.Button(annotation_window, text='教程', command=lambda: Data().add_keyword('tutorial'))
    tutorial_button.place(x=450, y=400, width=100, height=50)

    humorous_button = tk.Button(annotation_window, text='沙雕红石', command=lambda: Data().add_keyword('humorous'))
    humorous_button.place(x=550, y=400, width=100, height=50)

    other_button = tk.Button(annotation_window, text='其他', command=lambda: Data().add_keyword('other'))
    other_button.place(x=650, y=400, width=100, height=50)

    next_button = tk.Button(annotation_window, text='下一页', command=annotation_window.destroy)
    next_button.place(x=50, y=500, width=700, height=50)

    annotation_window.mainloop()

#获取pending_data目录下的所有以-original.json结尾的文件
import os
import json

pending_data_dict = {"content":[]}

pending_data_dir = 'pending_data'

for file_name in os.listdir(pending_data_dir):
    if file_name.endswith('-original.json'):
        with open(os.path.join(pending_data_dir, file_name), 'r', encoding='utf-8') as f:
            video_dict = json.load(f)

            print(len(video_dict['content']))

            for data in video_dict['content']:
                pending_data_dict["content"].append(data)

print(len(pending_data_dict['content']))

for page in range(len(pending_data_dict['content'])):
    annotation_data(pending_data_dict, page)

#保存标注结果
with open('annotation_result.json', 'w', encoding='utf-8') as f:
    json.dump(relation_list, f, ensure_ascii=False, indent=4)

with open('keyword_list.json', 'w', encoding='utf-8') as f:
    json.dump(keyword_list, f, ensure_ascii=False, indent=4)

"""def update_text():
    input_text = entry.get()
    text.insert(tk.END, input_text + '\n')
    entry.delete(0, tk.END)


# 创建主窗口
root = tk.Tk()
root.title('Tkinter 示例')
# 设置窗口大小
root.geometry('800x600')  # 宽度x高度
# 创建输入框
entry = tk.Entry(root)
entry.place(x=50, y=50, width=200, height=25)  # x, y坐标，宽度和高度
# 创建按钮
button = tk.Button(root, text='更新文本', command=update_text)
button.place(x=260, y=50, width=80, height=25)
# 创建文本框
text = tk.Text(root)
text.place(x=50, y=100, width=300, height=150)
# 启动事件循环
root.mainloop()"""

