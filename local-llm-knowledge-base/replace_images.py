import base64
import re

def replace_images_in_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open('mermaid-img/local_vs_cloud.png', 'rb') as f:
        local_vs_cloud_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    with open('mermaid-img/rag_flow.png', 'rb') as f:
        rag_flow_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    content = re.sub(
        r'<img src="https://trae-api-cn\.mchost\.guru/api/ide/v1/text_to_image\?prompt=A%20warm%20friendly%20comic-style%20illustration%20showing%20a%20person%20protecting%20documents%20from%20a%20big%20cloud%20monster[^"]*"',
        f'<img src="data:image/png;base64,{local_vs_cloud_b64}"',
        content
    )
    
    content = re.sub(
        r'<img src="https://trae-api-cn\.mchost\.guru/api/ide/v1/text_to_image\?prompt=A%20warm%20friendly%20comic-style%20illustration%20showing%20how%20RAG%20works[^"]*"',
        f'<img src="data:image/png;base64,{rag_flow_b64}"',
        content
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Images replaced in {html_file}")

if __name__ == "__main__":
    replace_images_in_html("本地大模型知识库系列-01-公众号版.html")