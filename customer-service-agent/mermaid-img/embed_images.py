#!/usr/bin/env python3
import base64
import os

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

for i in range(1, 5):
    png_file = f'{base_dir}/diagram{i}.png'
    with open(png_file, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    
    print(f'<img src="data:image/png;base64,{data}" alt="diagram{i}" style="max-width:100%;height:auto;">')
    print()
