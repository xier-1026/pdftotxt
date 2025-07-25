# pdftotxt工具

一个简单易用的PDF转文本工具，通过OCR技术提取PDF中的文字内容，支持中英文混合识别。

## 功能特点

- 图形化界面操作，简单直观
- 支持PDF文件的批量页面转换
- 中英文混合识别（基于Tesseract OCR）
- 实时显示转换进度
- 自动生成结构化文本输出（按页码分割）
- 自动清理临时文件，不占用额外空间

## 安装说明

### 前提条件

- Python 3.6 或更高版本
- Tesseract OCR 引擎（系统级安装）
  - Windows: 从 [UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装
  - macOS: `brew install tesseract tesseract-lang`
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng`

### 安装步骤

安装依赖包
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行程序
```bash
python pdttotxt.py
```

2. 操作流程
   - 点击"选择PDF文件"按钮，选择需要转换的PDF文件
   - 点击"开始转换"按钮，程序将自动处理
   - 转换完成后，文本文件将保存在原PDF文件同级目录的`ocr_output`文件夹中
   - 输出文件以原PDF文件名命名，按页码分割内容

## 项目结构

```
pdf-to-txt-converter/
├── pdttotxt.py       # 主程序文件
├── requirements.txt  # 依赖列表
└── README.md         # 说明文档
```

## 依赖库

- `pymupdf` - 用于PDF文件处理和页面渲染
- `pytesseract` - OCR识别核心库
- `Pillow` - 图像处理支持
- `tkinter` - 图形用户界面（通常随Python默认安装）

## 常见问题

1. **识别速度慢**：OCR处理需要一定时间，尤其是大文件或高分辨率页面，请耐心等待

2. **识别准确率低**：
   - 确保已安装中文语言包（`chi-sim`）
   - 尝试提高PDF的清晰度
   - 确保文字不是艺术字体或过度模糊

3. **程序无法启动**：
   - 检查Python版本是否符合要求
   - 确认所有依赖库已正确安装
   - 确保Tesseract OCR已正确安装并配置环境变量

## 许可证

[MIT](LICENSE)
