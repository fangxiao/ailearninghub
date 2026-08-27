#!/usr/bin/env python3
"""简化版衔接 - 自然融入，不刻意"""

import re
import os

BASE_DIR = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent-harness-skill'


def clean_old_connector(content):
    """清除之前添加的生硬衔接内容"""
    # 移除生硬的衔接块
    content = re.sub(
        r'<blockquote class="highlight">\s*<p><strong>📎 与原系列的衔接</strong>.*?</blockquote>',
        '', content, flags=re.DOTALL
    )
    # 移除"前面我们讲了"和"本篇目标"
    content = re.sub(
        r'<p><strong>前面我们讲了：</strong>.*?</p>\s*<p><strong>本篇目标：</strong>.*?</p>',
        '', content, flags=re.DOTALL
    )
    # 移除中间的hr
    content = re.sub(
        r'<hr style="border: none; height: 1px; background: linear-gradient\(to right, transparent, #e0e0e0, transparent\); margin: 24px 0;">\s*(?=<h3>)',
        '', content
    )
    # 移除结尾的系列导航
    content = re.sub(
        r'<hr style="border: none; height: 1px; background: linear-gradient\(to right, transparent, #e0e0e0, transparent\); margin: 36px 0;">\s*<p style="text-align: center; color: #888; font-size: 14px; padding-top: 20px;">.*?</p>\s*(?=</div>)',
        '', content, flags=re.DOTALL
    )
    return content


def add_natural_opening(content, article_no):
    """自然的开头衔接"""
    # 在第一个h3之前加一句自然的话
    # 第1篇特殊处理，因为是开篇
    if article_no == 1:
        natural_text = '''<p style="color: #888; font-size: 14px; font-style: italic; margin: 16px 0 24px;">
💡 如果你看过之前的《客服Agent实战系列》，应该熟悉V1插件架构。本篇是加强版开篇，我们来聊聊怎么把那个原型升级成真正的生产级架构。
</p>
'''
    else:
        natural_text = '''<p style="color: #888; font-size: 14px; font-style: italic; margin: 16px 0 24px;">
💡 延续《客服Agent实战系列》的实战风格，本篇继续深入 Harness+Skill 架构的核心设计。
</p>
'''
    
    h3_match = re.search(r'<h3>', content)
    if h3_match:
        return content[:h3_match.start()] + natural_text + content[h3_match.start()]
    return content


def add_simple_ending(content):
    """简单的结尾导航"""
    ending = '''<hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #e0e0e0, transparent); margin: 36px 0;">

<p style="text-align: center; color: #888; font-size: 14px; padding: 16px 0;">
<strong>客服Agent加强版</strong> · Harness+Skill 实战系列<br>
共 14 篇，从架构革命到生产落地<br>
<span style="font-size: 12px; color: #aaa;">（前置系列：客服Agent实战系列 · V1插件架构）</span>
</p>
'''
    
    closing_div = content.rfind('</div>')
    if closing_div > 0:
        return content[:closing_div] + ending + '\n' + content[closing_div:]
    return content


def clean_extra_blank_lines(content):
    """清理多余的空行"""
    # 把连续3个以上的空行替换为1个空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    # 把blockquote结束后的多余空行清理
    content = re.sub(r'</blockquote>\n{3,}', '</blockquote>\n\n', content)
    return content


def process_file(filepath, article_no):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 先清除旧的生硬衔接
    content = clean_old_connector(content)
    
    # 2. 清理多余空行
    content = clean_extra_blank_lines(content)
    
    # 3. 添加自然的开头
    content = add_natural_opening(content, article_no)
    
    # 4. 添加简单的结尾
    content = add_simple_ending(content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False


def main():
    html_files = sorted([f for f in os.listdir(BASE_DIR) 
                        if f.endswith('.html') and '公众号版' not in f 
                        and 'batch_convert' not in f 
                        and 'add_code' not in f 
                        and 'add_connector' not in f])
    
    print(f"找到 {len(html_files)} 篇文章\n")
    
    processed = 0
    for filename in html_files:
        match = re.search(r'-(\d+)\.html', filename)
        if not match:
            continue
        
        article_no = int(match.group(1))
        filepath = os.path.join(BASE_DIR, filename)
        
        print(f"处理: {filename}")
        
        if process_file(filepath, article_no):
            print(f"  ✓ 已更新")
            processed += 1
        else:
            print(f"  - 未修改")
    
    print(f"\n完成！共处理 {processed} 篇文章")


if __name__ == '__main__':
    main()
