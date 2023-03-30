import json
import tkinter as tk
from tkinter import ttk

# 读取json文件中的数据
with open('../data/items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取需要的数据
data = [str(item['LocalizedNames']['ZH-CN']) for item in data if item['LocalizedNames'] is not None and 'ZH-CN' in item['LocalizedNames']]
print(data)

def fuzzy_search(pattern, data):
    if not isinstance(data, list):
        return []
    matches = [x for x in data if x and pattern in x]
    if not matches:
        return data
    return matches


def add_item():
    item = combo.get()
    if item and item not in lst.get(0, tk.END):
        lst.insert(tk.END, item)

def search_item():
    pattern = search_box.get()
    matches = fuzzy_search(pattern, lst.get(0, tk.END))
    result_box.delete('1.0', tk.END)
    for item in lst.get(0, tk.END):
        if item in matches:
            result_box.insert(tk.END, item+'\n')

def on_focus_in(event):
    if search_box.get() == '请输入内容':
        search_box.delete(0, tk.END)
        search_box.config(foreground='black')

def on_focus_out(event):
    if search_box.get() == '':
        search_box.insert(0, '请输入内容')
        search_box.config(foreground='grey')

def on_delete(event):
    pattern = search_box.get()
    matches = fuzzy_search(pattern, data)
    combo['values'] = matches or data

root = tk.Tk()
root.title('Fuzzy Search')

# Add a search box to filter the combobox items
search_box_var = tk.StringVar(value='请输入内容')
search_box = ttk.Entry(root, textvariable=search_box_var, foreground='grey')
search_box.pack(pady=10)
search_box.bind('<FocusIn>', on_focus_in)
search_box.bind('<FocusOut>', on_focus_out)
search_box.bind('<KeyRelease>', on_delete)

# Add a combobox with fuzzy search capabilities
combo_var = tk.StringVar()
combo = ttk.Combobox(root, textvariable=combo_var, values=data, postcommand=lambda: combo.configure(values=fuzzy_search(search_box.get(), data)))
combo.pack(pady=10)

# Add a button to add selected item to listbox
add_button = ttk.Button(root, text='添加', command=add_item)
add_button.pack(pady=10)

# Add a listbox to display selected items
lst = tk.Listbox(root, height=5)
lst.pack(pady=10)

# Add a button to search selected items
search_button = ttk.Button(root, text='查询', command=search_item)
search_button.pack(pady=10)

# Add a textbox to display search results
result_box = tk.Text(root, height=5)
result_box.pack(pady=10)

root.mainloop()
