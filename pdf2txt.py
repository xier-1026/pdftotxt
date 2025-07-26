import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import fitz
import pytesseract
from PIL import Image

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.pdf_path = None
        self.output_dir = None
        self._setup_ui()
        
    def _setup_ui(self):
        """初始化现代化界面"""
        self.root.title("PDF转TXT工具")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # 主容器
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 使用grid布局
        self.btn_select = ttk.Button(
            main_frame, 
            text="选择PDF文件", 
            command=self.select_file,
            width=25
        )
        self.btn_select.grid(row=0, column=0, pady=5, sticky=tk.EW)

        self.entry_path = ttk.Entry(main_frame, width=35, state="readonly")
        self.entry_path.grid(row=1, column=0, pady=5, sticky=tk.EW)

        self.btn_ocr = ttk.Button(
            main_frame, 
            text="开始转换", 
            command=self.start_ocr,
            state=tk.DISABLED
        )
        self.btn_ocr.grid(row=2, column=0, pady=10, sticky=tk.EW)

        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.grid(row=3, column=0, pady=10, sticky=tk.EW)

        self.status_label = ttk.Label(main_frame, text="就绪")
        self.status_label.grid(row=4, column=0, pady=5, sticky=tk.W)

        main_frame.columnconfigure(0, weight=1)



    def select_file(self):
        """选择文件"""
        path = filedialog.askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if path:
            self.pdf_path = Path(path)
            self.output_dir = self.pdf_path.parent / "ocr_output"
            self._update_entry(path)
            self.btn_ocr.config(state=tk.NORMAL)
            self.status_label.config(text="文件已选择")

    def _update_entry(self, path):
        """更新路径显示"""
        self.entry_path.config(state=tk.NORMAL)
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, path)
        self.entry_path.config(state="readonly")

    def start_ocr(self):
        """启动处理线程"""
        if not self.pdf_path:
            messagebox.showerror("错误", "请先选择PDF文件")
            return

        self._toggle_buttons(False)
        threading.Thread(target=self.process_pdf, daemon=True).start()

    def process_pdf(self):
        """PDF处理核心逻辑"""
        try:
            with fitz.open(self.pdf_path) as pdf:
                total_pages = pdf.page_count
                self.output_dir.mkdir(exist_ok=True)

                txt_path = self.output_dir / f"{self.pdf_path.stem}.txt"
                
                with open(txt_path, "w", encoding="utf-8") as f:
                    for page_num, page in enumerate(pdf, 1):
                        self._update_progress(page_num, total_pages)
                        
                        # 生成临时图像
                        img_path = self._save_page_image(page, page_num)
                        
                        # OCR识别
                        text = self._ocr_image(img_path)
                        f.write(f"=== 第 {page_num} 页 ===\n{text}\n\n")
                        
                        img_path.unlink()  # 清理临时文件

                self._show_completion()

        except Exception as e:
            self._show_error(str(e))
        finally:
            self._reset_ui()

    def _save_page_image(self, page, page_num):
        """保存页面为临时图像"""
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_path = self.output_dir / f"temp_{page_num}.png"
        pix.save(img_path)
        return img_path

    def _ocr_image(self, img_path):
        """执行OCR识别"""
        try:
            return pytesseract.image_to_string(
                Image.open(img_path),
                lang='chi_sim+eng'  # 支持中英文混合
            )
        except Exception as e:
            messagebox.showwarning("识别警告", f"页面识别失败: {str(e)}")
            return ""

    def _update_progress(self, current, total):
        """更新进度"""
        progress = (current / total) * 100
        self.root.after(0, lambda: [
            self.progress.config(value=progress),
            self.status_label.config(text=f"正在处理 {current}/{total} 页...")
        ])

    def _show_completion(self):
        """显示完成提示"""
        self.root.after(0, lambda: messagebox.showinfo(
            "完成",
            f"转换完成！\n保存路径：{self.output_dir}"
        ))

    def _show_error(self, error_msg):
        """显示错误信息"""
        self.root.after(0, lambda: messagebox.showerror(
            "错误",
            f"处理失败：{error_msg}"
        ))

    def _toggle_buttons(self, enable):
        """按钮状态管理"""
        state = tk.NORMAL if enable else tk.DISABLED
        self.btn_select.config(state=state)
        self.btn_ocr.config(state=state)

    def _reset_ui(self):
        """重置界面状态"""
        self.root.after(0, lambda: [
            self.progress.config(value=0),
            self._toggle_buttons(True),
            self.status_label.config(text="就绪")
        ])

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
