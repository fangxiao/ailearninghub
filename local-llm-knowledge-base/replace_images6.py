import base64
import re

def replace_images_in_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    images = ['use_cases', 'best_practices', 'enterprise_deployment', 
              'knowledge_curation', 'future_trends', 'series_summary']
    
    for img_name in images:
        try:
            with open(f'mermaid-img/{img_name}.png', 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            content = re.sub(
                rf'<img src="{img_name}\.png"',
                f'<img src="data:image/png;base64,{img_b64}"',
                content
            )
        except:
            print(f"Failed to replace {img_name}")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Images replaced in {html_file}")

if __name__ == "__main__":
    replace_images_in_html("本地大模型知识库系列-06-公众号版.html")
