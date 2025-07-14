import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import re

class JSONEditor:
    def __init__(self, root):
        # 主窗口设置
        self.root = root
        self.root.title("JSON 编辑器")
        self.root.geometry("800x700")
        
        # 数据存储
        self.data = {}
        self.current_type = ""
        
        # 创建界面组件
        self.create_widgets()
    
    def create_widgets(self):
        """创建所有界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部框架 - 类型操作
        top_frame = tk.LabelFrame(main_frame, text="类型操作", padx=5, pady=5)
        top_frame.pack(fill=tk.X, pady=(0,10))
        
        # 类型添加部分
        tk.Label(top_frame, text="添加新类型:").grid(row=0, column=0, sticky=tk.W)
        self.type_entry = tk.Entry(top_frame, width=25)
        self.type_entry.grid(row=0, column=1, padx=5)
        
        add_type_btn = tk.Button(top_frame, text="添加", width=8, command=self.add_type)
        add_type_btn.grid(row=0, column=2, padx=5)
        
        # 类型选择下拉框
        tk.Label(top_frame, text="当前类型:").grid(row=1, column=0, sticky=tk.W)
        self.type_combobox = ttk.Combobox(top_frame, width=28, state="readonly")
        self.type_combobox.grid(row=1, column=1, padx=5)
        self.type_combobox.bind("<<ComboboxSelected>>", self.on_type_select)
        
        # 中间框架 - 键值对操作
        middle_frame = tk.LabelFrame(main_frame, text="键值对操作", padx=5, pady=5)
        middle_frame.pack(fill=tk.X, pady=(0,10))
        
        # 键值对输入
        tk.Label(middle_frame, text="键:").grid(row=0, column=0, sticky=tk.W)
        self.key_entry = tk.Entry(middle_frame, width=25)
        self.key_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(middle_frame, text="值:").grid(row=0, column=2, sticky=tk.W)
        self.value_entry = tk.Entry(middle_frame, width=25)
        self.value_entry.grid(row=0, column=3, padx=5)
        
        add_pair_btn = tk.Button(middle_frame, text="添加键值对", width=12, command=self.add_pair)
        add_pair_btn.grid(row=0, column=4, padx=5)
        
        # 底部框架 - 数据操作
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧批量处理面板
        left_panel = tk.LabelFrame(bottom_frame, text="批量处理", padx=5, pady=5)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))
        
        tk.Label(left_panel, text="输入格式: 键 值 或 键,值 或 键;值").pack(anchor=tk.W)
        self.batch_input = tk.Text(left_panel, wrap=tk.WORD)
        self.batch_input.pack(fill=tk.BOTH, expand=True, pady=5)
        
        process_btn = tk.Button(left_panel, text="处理数据", command=self.process_batch_direct)
        process_btn.pack(pady=5)
        
        # 右侧数据展示面板
        right_panel = tk.LabelFrame(bottom_frame, text="数据展示", padx=5, pady=5)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5,0))
        
        self.data_text = tk.Text(right_panel, wrap=tk.NONE)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(right_panel, command=self.data_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.data_text.config(yscrollcommand=scrollbar.set)
        
        # 底部按钮栏
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10,0))
        
        # 操作按钮
        sort_btn = tk.Button(btn_frame, text="一键排序", width=10, command=self.sort_data)
        sort_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(btn_frame, text="保存JSON", width=10, command=self.save_json)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(btn_frame, text="加载JSON", width=10, command=self.load_json)
        load_btn.pack(side=tk.LEFT, padx=5)
    
    def add_type(self):
        """添加新类型"""
        new_type = self.type_entry.get().strip()
        if not new_type:
            messagebox.showwarning("警告", "类型名称不能为空")
            return
            
        if new_type in self.data:
            messagebox.showwarning("警告", "该类型已存在")
            return
            
        self.data[new_type] = {}
        self.update_type_combobox()
        self.type_entry.delete(0, tk.END)
        messagebox.showinfo("成功", f"类型 '{new_type}' 已添加")
    
    def update_type_combobox(self):
        """更新类型下拉框"""
        types = list(self.data.keys())
        self.type_combobox['values'] = types
        if types:
            self.type_combobox.current(0)
            self.current_type = types[0]
    
    def on_type_select(self, event):
        """类型选择事件处理"""
        self.current_type = self.type_combobox.get()
        self.display_data()
    
    def add_pair(self):
        """添加键值对"""
        if not self.current_type:
            messagebox.showwarning("警告", "请先选择或创建一个类型")
            return
            
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()
        
        if not key or not value:
            messagebox.showwarning("警告", "键和值都不能为空")
            return
            
        self.data[self.current_type][key] = value
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.display_data()
    
    def display_data(self):
        """显示当前数据"""
        self.data_text.delete(1.0, tk.END)
        if self.current_type and self.current_type in self.data:
            formatted_json = json.dumps(self.data, indent=2, ensure_ascii=False)
            self.data_text.insert(tk.END, formatted_json)
    
    def sort_data(self):
        """一键排序功能"""
        if not self.data:
            return
            
        for type_name in self.data:
            # 分离数字键和字符串键
            numeric_keys = []
            string_keys = []
            
            for key in self.data[type_name].keys():
                if re.match(r'^\d+$', str(key)):
                    numeric_keys.append(key)
                else:
                    string_keys.append(key)
            
            # 数字键按数值排序
            numeric_keys_sorted = sorted(numeric_keys, key=lambda x: int(x))
            # 字符串键按拼音排序
            string_keys_sorted = sorted(string_keys, key=lambda x: x.lower())
            
            # 合并排序后的键
            sorted_keys = numeric_keys_sorted + string_keys_sorted
            
            # 创建新的有序字典
            sorted_dict = {}
            for key in sorted_keys:
                sorted_dict[key] = self.data[type_name][key]
            
            self.data[type_name] = sorted_dict
        
        self.display_data()
        messagebox.showinfo("成功", "数据已排序")
    
    def open_batch_window(self):
        """打开批量处理窗口"""
        if not self.current_type:
            messagebox.showwarning("警告", "请先选择或创建一个类型")
            return
            
        batch_window = tk.Toplevel(self.root)
        batch_window.title("批量处理")
        batch_window.geometry("500x300")
        
        tk.Label(batch_window, text="输入批量数据 (每行一对键值，用逗号、空格或分号分隔):").pack(pady=10)
        
        self.batch_text = tk.Text(batch_window, height=10)
        self.batch_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        process_btn = tk.Button(batch_window, text="处理", command=lambda: self.process_batch(batch_window))
        process_btn.pack(pady=10)
    
    def process_batch(self, window):
        """处理批量数据"""
        text = self.batch_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入批量数据")
            return
            
        lines = text.split('\n')
        added_count = 0
        
        for line in lines:
            # 使用正则表达式分割键值对
            parts = re.split(r'[,;\s]+', line.strip())
            if len(parts) >= 2:
                key = parts[0].strip()
                value = ' '.join(parts[1:]).strip()
                if key and value:
                    self.data[self.current_type][key] = value
                    added_count += 1
        
        window.destroy()
        self.display_data()
        messagebox.showinfo("成功", f"已添加 {added_count} 对键值")
    
    def process_batch_direct(self):
        """直接处理批量输入框中的数据"""
        if not self.current_type:
            messagebox.showwarning("警告", "请先选择或创建一个类型")
            return
            
        text = self.batch_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入批量数据")
            return
            
        # 复用原来的批量处理逻辑
        lines = text.split('\n')
        added_count = 0
        
        for line in lines:
            parts = re.split(r'[,;\s]+', line.strip())
            if len(parts) >= 2:
                key = parts[0].strip()
                value = ' '.join(parts[1:]).strip()
                if key and value:
                    self.data[self.current_type][key] = value
                    added_count += 1
        
        self.batch_input.delete("1.0", tk.END)
        self.display_data()
        messagebox.showinfo("成功", f"已添加 {added_count} 对键值")
    
    def save_json(self):
        """保存JSON文件"""
        if not self.data:
            messagebox.showwarning("警告", "没有数据可保存")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("成功", f"文件已保存到 {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时出错: {str(e)}")
    
    def load_json(self):
        """加载JSON文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                
                self.update_type_combobox()
                self.display_data()
                messagebox.showinfo("成功", f"文件已从 {file_path} 加载")
            except Exception as e:
                messagebox.showerror("错误", f"加载文件时出错: {str(e)}")

if __name__ == "__main__":
    # 解决打包后可能出现的路径问题
    import os
    import sys
    
    def resource_path(relative_path):
        """获取打包后资源的绝对路径"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    root = tk.Tk()
    app = JSONEditor(root)
    root.mainloop()