import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import webbrowser
import pyperclip
import re
import os

class DouyinParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("抖音视频解析工具")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        self.api_list = [
            "https://apis.jxcxin.cn/api/douyin",
            "https://api.lvxiaodong.com/api/dypro"
        ]
        self.current_api_index = 0

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="抖音视频解析工具",
                                font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=(0, 20))

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(input_frame, text="抖音链接:", font=("微软雅黑", 11)).pack(side=tk.LEFT, padx=(0, 10))

        self.url_entry = ttk.Entry(input_frame, width=50, font=("微软雅黑", 10))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.parse_btn = ttk.Button(input_frame, text="解析", command=self.parse_video, width=10)
        self.parse_btn.pack(side=tk.LEFT)

        self.paste_btn = ttk.Button(input_frame, text="粘贴并解析", command=self.paste_and_parse, width=12)
        self.paste_btn.pack(side=tk.LEFT, padx=(5, 0))

        self.clear_btn = ttk.Button(input_frame, text="清空", command=self.clear_all, width=10)
        self.clear_btn.pack(side=tk.LEFT, padx=(5, 0))

        result_frame = ttk.LabelFrame(main_frame, text="解析结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=12,
                                   font=("微软雅黑", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        self.copy_btn = ttk.Button(btn_frame, text="复制视频链接",
                                   command=self.copy_video_url, state=tk.DISABLED)
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.download_btn = ttk.Button(btn_frame, text="下载视频",
                                       command=self.download_video, state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.open_btn = ttk.Button(btn_frame, text="在浏览器打开",
                                  command=self.open_in_browser, state=tk.DISABLED)
        self.open_btn.pack(side=tk.LEFT)

        self.status_label = ttk.Label(main_frame, text="就绪",
                                      foreground="green", font=("微软雅黑", 9))
        self.status_label.pack(pady=(10, 0))

        self.video_url = None

    def extract_douyin_url(self, text):
        pattern = r'https?://v\.douyin\.com/[a-zA-Z0-9_-]+'
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        pattern2 = r'https?://www\.douyin\.com/[a-zA-Z0-9_-]+'
        match2 = re.search(pattern2, text)
        if match2:
            return match2.group(0)
        return None

    def parse_video(self):
        input_text = self.url_entry.get().strip()

        if not input_text:
            messagebox.showwarning("警告", "请输入内容！")
            return

        url = self.extract_douyin_url(input_text)

        if not url:
            messagebox.showwarning("警告", "未在文本中找到抖音链接！\n请输入包含抖音链接的文本。")
            return

        self.parse_btn.config(state=tk.DISABLED)
        self.status_label.config(text=f"已识别链接: {url}", foreground="blue")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"已识别抖音链接: {url}\n正在解析，请稍候...\n")
        self.root.update()

        success = False

        for api_index in range(len(self.api_list)):
            api_url = self.api_list[api_index]

            try:
                response = requests.get(api_url, params={"url": url}, timeout=15)
                data = response.json()

                self.result_text.delete(1.0, tk.END)

                if api_index == 0:
                    if data.get("code") == 200:
                        item = data["data"]
                        self.video_url = item.get("url", "")

                        result_info = f"✓ 解析成功！\n\n"
                        result_info += f"标题: {item.get('title', '无')}\n\n"
                        result_info += f"作者: {item.get('author', '无')}\n\n"
                        result_info += f"点赞: {item.get('like', '无')}\n\n"
                        result_info += f"发布时间: {item.get('time', '无')}\n\n"
                        result_info += f"视频URL:\n{self.video_url}\n\n"

                        if item.get("cover"):
                            result_info += f"封面URL:\n{item.get('cover')}\n\n"

                        music = item.get("music")
                        if music and music.get("url"):
                            result_info += f"音乐URL:\n{music.get('url')}\n"

                        self.result_text.insert(tk.END, result_info)
                        self.status_label.config(text="解析成功！", foreground="green")

                        self.copy_btn.config(state=tk.NORMAL)
                        self.download_btn.config(state=tk.NORMAL)
                        self.open_btn.config(state=tk.NORMAL)
                        success = True
                        break

                elif api_index == 1:
                    if data.get("code") == 0:
                        item = data["data"]["item"]
                        self.video_url = item.get("url", "")

                        result_info = f"✓ 解析成功！\n\n"
                        result_info += f"标题: {item.get('title', '无')}\n\n"
                        result_info += f"作者: {item.get('author', '无')}\n\n"
                        result_info += f"视频URL:\n{self.video_url}\n\n"

                        if item.get("cover"):
                            result_info += f"封面URL:\n{item.get('cover')}\n\n"

                        if item.get("music"):
                            result_info += f"音乐URL:\n{item.get('music')}\n"

                        self.result_text.insert(tk.END, result_info)
                        self.status_label.config(text="解析成功！", foreground="green")

                        self.copy_btn.config(state=tk.NORMAL)
                        self.download_btn.config(state=tk.NORMAL)
                        self.open_btn.config(state=tk.NORMAL)
                        success = True
                        break

            except:
                continue

        if not success:
            error_msg = data.get("msg", "解析失败，请检查链接是否有效") if 'data' in locals() else "所有API均无法解析此链接"
            self.result_text.insert(tk.END, f"✗ 解析失败: {error_msg}\n")
            self.status_label.config(text="解析失败", foreground="red")
            messagebox.showerror("错误", f"解析失败: {error_msg}\n\n可能的原因：\n1. 链接已过期\n2. 视频被删除或私密\n3. API临时不可用")

        self.parse_btn.config(state=tk.NORMAL)

    def copy_video_url(self):
        if self.video_url:
            try:
                pyperclip.copy(self.video_url)
                self.status_label.config(text="已复制到剪贴板！", foreground="blue")
                messagebox.showinfo("成功", "视频链接已复制到剪贴板！")
            except Exception as e:
                messagebox.showerror("错误", f"复制失败: {str(e)}")

    def open_in_browser(self):
        if self.video_url:
            webbrowser.open(self.video_url)

    def paste_and_parse(self):
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, clipboard_text)
                self.parse_video()
            else:
                messagebox.showwarning("警告", "剪贴板为空！")
        except Exception as e:
            messagebox.showerror("错误", f"粘贴失败: {str(e)}")

    def clear_all(self):
        self.url_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="就绪", foreground="green")
        self.copy_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        self.open_btn.config(state=tk.DISABLED)
        self.video_url = None

    def download_video(self):
        if not self.video_url:
            messagebox.showwarning("警告", "没有可下载的视频！")
            return

        save_path = filedialog.asksaveasfilename(
            title="保存视频",
            defaultextension=".mp4",
            filetypes=[("MP4视频", "*.mp4"), ("所有文件", "*.*")],
            initialfile="douyin_video.mp4"
        )

        if not save_path:
            return

        self.download_btn.config(state=tk.DISABLED)
        self.status_label.config(text="正在下载...", foreground="orange")
        self.root.update()

        try:
            response = requests.get(self.video_url, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            self.status_label.config(text=f"下载中: {percent:.1f}%", foreground="blue")
                            self.root.update()

            self.status_label.config(text="下载完成！", foreground="green")
            messagebox.showinfo("成功", f"视频已保存到:\n{save_path}")

            if messagebox.askyesno("询问", "是否打开下载文件夹？"):
                folder = os.path.dirname(save_path)
                if folder:
                    webbrowser.open(f"file:///{folder}")

        except requests.Timeout:
            messagebox.showerror("错误", "下载超时，请重试！")
            self.status_label.config(text="下载超时", foreground="red")
        except requests.RequestException as e:
            messagebox.showerror("错误", f"下载失败: {str(e)}")
            self.status_label.config(text="下载失败", foreground="red")
        finally:
            self.download_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = DouyinParserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
