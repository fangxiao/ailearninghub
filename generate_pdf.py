#!/usr/bin/env python3
import os
import glob
import re
import base64
from io import BytesIO
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from PIL import Image

class PDFWithChinese(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('PingFang', '', '/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc')
        self.add_font('PingFang', 'B', '/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc')
        self.add_font('Menlo', '', '/System/Library/Fonts/Menlo.ttc')
        self.add_font('Menlo', 'B', '/System/Library/Fonts/Menlo.ttc')

    def chapter_title(self, title):
        self.set_font('PingFang', 'B', 16)
        self.cell(0, 15, title, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

    def chapter_subtitle(self, subtitle):
        self.set_font('PingFang', 'B', 14)
        self.cell(0, 12, subtitle, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def chapter_text(self, text):
        self.set_font('PingFang', '', 11)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def code_block(self, code, language='python'):
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            try:
                lexer = guess_lexer(code)
            except:
                lexer = get_lexer_by_name('text', stripall=True)
        
        formatter = HtmlFormatter(style='monokai', full=False)
        highlighted_html = highlight(code, lexer, formatter)
        
        soup = BeautifulSoup(highlighted_html, 'html.parser')
        lines = soup.find_all('span')
        
        self.set_fill_color(45, 55, 72)
        self.set_draw_color(45, 55, 72)
        self.rect(self.get_x(), self.get_y(), self.w - 20, 100)
        
        self.set_xy(self.get_x() + 10, self.get_y() + 5)
        self.set_font('Menlo', '', 10)
        
        current_line = []
        for span in lines:
            text = span.get_text()
            if '\n' in text:
                parts = text.split('\n')
                current_line.append(parts[0])
                self.output_line(''.join(current_line))
                for part in parts[1:-1]:
                    self.output_line(part)
                current_line = [parts[-1]]
            else:
                current_line.append(text)
        
        if current_line:
            self.output_line(''.join(current_line))
        
        self.ln(10)

    def output_line(self, line):
        if len(line) > 60:
            chunks = [line[i:i+60] for i in range(0, len(line), 60)]
            for chunk in chunks:
                self.cell(0, 6, chunk, new_x=XPos.LMARGIN + 10, new_y=YPos.NEXT)
        else:
            self.cell(0, 6, line, new_x=XPos.LMARGIN + 10, new_y=YPos.NEXT)

    def image_from_base64(self, base64_str):
        try:
            if base64_str.startswith('data:image'):
                parts = base64_str.split(',', 1)
                if len(parts) > 1:
                    base64_str = parts[1]
            
            base64_str = base64_str.strip()
            base64_str = re.sub(r'\s+', '', base64_str)
            
            if len(base64_str) < 100:
                print("图片数据过短，跳过")
                return False
            
            padding = len(base64_str) % 4
            if padding != 0:
                base64_str += '=' * (4 - padding)
            
            try:
                image_data = base64.b64decode(base64_str)
            except Exception as decode_err:
                print(f"Base64解码失败: {str(decode_err)}")
                return False
            
            if len(image_data) < 100:
                print("解码后数据过短，跳过")
                return False
            
            try:
                image = Image.open(BytesIO(image_data))
            except Exception as img_err:
                print(f"图片打开失败: {str(img_err)}")
                return False
            
            max_width = self.w - 40
            max_height = 300
            
            width, height = image.size
            original_height = height
            
            if width > max_width:
                ratio = max_width / width
                width = max_width
                height = height * ratio
            if height > max_height:
                ratio = max_height / height
                height = max_height
                width = width * ratio
            
            temp_file = '/tmp/temp_image.png'
            image.save(temp_file, format='PNG')
            
            self.image(temp_file, x=self.l_margin, w=width)
            os.remove(temp_file)
            
            self.ln(height + 15)
            print(f"图片处理成功: {original_height}x{width}")
            return True
        except Exception as e:
            print(f"图片处理失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

SERIES_CONFIG = {
    "大模型原理系列": {
        "folder": "bigmodel",
        "pattern": "大模型原理系列-*.html",
        "output": "大模型原理系列-电子书.pdf",
        "title": "大模型原理系列",
        "subtitle": "深入理解Transformer架构"
    }
}

def sort_files(file_list):
    def extract_number(filename):
        match = re.search(r'-(\d+)-', filename)
        if match:
            return int(match.group(1))
        match = re.search(r'-(\d+)', filename)
        if match:
            return int(match.group(1))
        return 999
    return sorted(file_list, key=extract_number)

def extract_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(strip=True)
    h2 = soup.find('h2')
    if h2:
        return h2.get_text(strip=True)
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text(strip=True)
    return "未命名文章"

def parse_html_to_pdf_elements(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    elements = []
    
    for script in soup(['script', 'style']):
        script.decompose()
    
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'pre', 'img', 'ul', 'ol', 'li', 'blockquote', 'table', 'tr', 'td', 'th']):
        if element.name == 'h1' or element.name == 'h2':
            text = element.get_text(strip=True)
            if text and len(text) < 100:
                elements.append(('title', text))
        elif element.name == 'h3':
            text = element.get_text(strip=True)
            if text and len(text) < 100:
                elements.append(('subtitle', text))
        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text and len(text) > 0:
                elements.append(('paragraph', text))
        elif element.name == 'pre':
            code = element.get_text(strip=True)
            if code and len(code) > 0:
                elements.append(('code', code))
        elif element.name == 'img':
            src = element.get('src', '')
            if src and 'base64' in src:
                elements.append(('image', src))
        elif element.name == 'ul' or element.name == 'ol':
            items = []
            for li in element.find_all('li'):
                li_text = li.get_text(strip=True)
                if li_text:
                    items.append(li_text)
            if items:
                elements.append(('list', items))
        elif element.name == 'blockquote':
            text = element.get_text(strip=True)
            if text and len(text) > 0:
                elements.append(('blockquote', text))
    
    return elements

def generate_pdf_for_series(series_name, config):
    base_path = "/Users/admin/project/lovely/platform/doc/prototype"
    folder_path = os.path.join(base_path, config["folder"])
    pattern = os.path.join(folder_path, config["pattern"])
    
    html_files = glob.glob(pattern)
    
    if not html_files:
        print(f"未找到{series_name}的HTML文件")
        return False
    
    html_files = sort_files(html_files)
    print(f"找到{series_name}的{len(html_files)}个文件")
    
    try:
        pdf = PDFWithChinese()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.set_font('PingFang', '', 12)
        
        pdf.add_page()
        pdf.set_font('PingFang', 'B', 28)
        pdf.cell(0, 50, config["title"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(15)
        pdf.set_font('PingFang', '', 18)
        pdf.cell(0, 25, config["subtitle"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(50)
        pdf.set_font('PingFang', '', 12)
        pdf.cell(0, 15, "AI技术专栏", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)
        pdf.cell(0, 15, "2026年", align='C')
        
        pdf.add_page()
        pdf.set_font('PingFang', 'B', 20)
        pdf.cell(0, 25, "目录", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(20)
        
        pdf.set_font('PingFang', '', 12)
        toc_entries = []
        for i, html_file in enumerate(html_files, 1):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            title = extract_title(content)
            toc_entries.append((i, title))
            pdf.cell(0, 10, f"{i}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        for i, html_file in enumerate(html_files, 1):
            pdf.add_page()
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title = extract_title(content)
            
            pdf.set_font('PingFang', 'B', 18)
            pdf.cell(0, 20, f"{i}. {title}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(15)
            
            elements = parse_html_to_pdf_elements(content)
            
            for elem_type, elem_content in elements:
                if elem_type == 'title':
                    pdf.set_font('PingFang', 'B', 16)
                    pdf.cell(0, 12, elem_content, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.ln(8)
                elif elem_type == 'subtitle':
                    pdf.set_font('PingFang', 'B', 14)
                    pdf.cell(0, 10, elem_content, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.ln(5)
                elif elem_type == 'paragraph':
                    pdf.set_font('PingFang', '', 11)
                    pdf.multi_cell(0, 8, elem_content)
                    pdf.ln(3)
                elif elem_type == 'code':
                    pdf.set_font('Menlo', '', 9)
                    pdf.set_fill_color(245, 245, 245)
                    pdf.set_draw_color(200, 200, 200)
                    pdf.set_line_width(0.5)
                    
                    lines = elem_content.split('\n')
                    max_chars = max(len(line) for line in lines) if lines else 0
                    line_height = 5
                    total_height = len(lines) * line_height + 20
                    code_width = min(max_chars * 4 + 20, pdf.w - 40)
                    
                    pdf.rect(pdf.l_margin, pdf.get_y(), code_width, total_height, 'DF')
                    
                    pdf.set_xy(pdf.l_margin + 10, pdf.get_y() + 10)
                    
                    for line in lines:
                        if len(line) > 70:
                            chunks = [line[i:i+70] for i in range(0, len(line), 70)]
                            for chunk in chunks:
                                pdf.cell(0, line_height, chunk, new_x=XPos.LMARGIN + 10, new_y=YPos.NEXT)
                        else:
                            pdf.cell(0, line_height, line, new_x=XPos.LMARGIN + 10, new_y=YPos.NEXT)
                    
                    pdf.set_xy(pdf.l_margin, pdf.get_y() + 10)
                    pdf.ln(10)
                elif elem_type == 'image':
                    pdf.image_from_base64(elem_content)
                elif elem_type == 'list':
                    pdf.set_font('PingFang', '', 11)
                    for idx, item in enumerate(elem_content, 1):
                        pdf.cell(0, 8, f"• {item}")
                        pdf.ln(3)
                    pdf.ln(5)
                elif elem_type == 'blockquote':
                    pdf.set_font('PingFang', '', 11)
                    pdf.set_fill_color(250, 250, 255)
                    pdf.set_draw_color(100, 149, 237)
                    pdf.set_line_width(1)
                    
                    pdf.rect(pdf.l_margin, pdf.get_y(), pdf.w - 20, 50, 'D')
                    pdf.set_xy(pdf.l_margin + 10, pdf.get_y() + 10)
                    pdf.multi_cell(0, 8, elem_content)
                    pdf.ln(15)
        
        output_path = os.path.join(base_path, config["output"])
        pdf.output(output_path)
        print(f"成功生成: {output_path}")
        return True
        
    except Exception as e:
        print(f"生成{series_name}失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("开始生成PDF电子书...")
    print("=" * 60)
    
    success_count = 0
    total_count = len(SERIES_CONFIG)
    
    for series_name, config in SERIES_CONFIG.items():
        print(f"\n正在处理: {series_name}")
        if generate_pdf_for_series(series_name, config):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"生成完成: {success_count}/{total_count} 个系列成功")

if __name__ == "__main__":
    main()
