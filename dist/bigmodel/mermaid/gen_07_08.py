#!/usr/bin/env python3
import base64
import subprocess

def mmd_to_png(mmd_file, png_file):
    with open(mmd_file, 'r') as f:
        mmd_content = f.read()

    encoded = base64.b64encode(mmd_content.encode()).decode().replace('\n', '')
    url = f"https://mermaid.ink/img/{encoded}"

    subprocess.run(['curl', '-s', '-o', png_file, url], check=True)
    print(f"Generated: {png_file}")

    # Check file size
    import os
    size = os.path.getsize(png_file)
    print(f"  Size: {size} bytes")
    if size < 1000:
        print(f"  WARNING: File too small, likely error!")

base_path = '/Users/admin/project/lovely/platform/doc/prototype/myagent/mermaid'

# Generate images
mmd_files = [
    ('07-state-machine.mmd', '07-state-machine.png'),
    ('08-execution-flow.mmd', '08-execution-flow.png'),
]

for mmd_file, png_file in mmd_files:
    mmd_to_png(
        f'{base_path}/{mmd_file}',
        f'{base_path}/{png_file}'
    )

print("\nDone!")
