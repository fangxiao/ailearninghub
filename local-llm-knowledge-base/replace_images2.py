import base64
import re

def replace_images_in_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open('mermaid-img/installation_flow.png', 'rb') as f:
        installation_flow_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    with open('mermaid-img/model_comparison.png', 'rb') as f:
        model_comparison_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    content = re.sub(
        r'<img src="installation_flow.png"',
        f'<img src="data:image/png;base64,{installation_flow_b64}"',
        content
    )
    
    content = re.sub(
        r'<img src="model_comparison.png"',
        f'<img src="data:image/png;base64,{model_comparison_b64}"',
        content
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Images replaced in {html_file}")

if __name__ == "__main__":
    replace_images_in_html("本地大模型知识库系列-02-公众号版.html")
