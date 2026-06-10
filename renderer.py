import os
import requests

async def generate_code_image(code_text: str, output_path: str = "output.png", theme: str = "monokai"):
    try:
        api_url = "https://carbonara.solopov.dev/api/cook"
        
        payload = {
            "code": code_text,
            "backgroundColor": "#1F1F24",
            "theme": theme,
            "exportSize": "2x",
            "paddingVertical": "30px",
            "paddingHorizontal": "30px"
        }
        
        response = requests.post(api_url, json=payload, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return output_path
        else:
            print(f"Renderer API returned status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error rendering code image: {e}")
        return None