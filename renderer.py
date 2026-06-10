import io
import html
from playwright.async_api import async_playwright

async def generate_code_image(code_text: str, theme: str = "monokai"):
    try:
        theme_map = {
            "monokai": "monokai-sublime",
            "dracula": "dracula",
            "nord": "nord",
            "github": "github"
        }
        css_theme = theme_map.get(theme, "monokai-sublime")
        
        bg_color = "#ffffff" if theme == "github" else "#1F1F24"
        text_color = "#000000" if theme == "github" else "#ffffff"

        html_content = f"""
        <html>
          <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/{css_theme}.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
            <style>
              body {{ background: transparent; padding: 40px; display: flex; justify-content: center; align-items: center; margin: 0; font-family: sans-serif; }}
              .mac-window {{ background: {bg_color}; color: {text_color}; border-radius: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); padding: 20px 30px; min-width: 400px; max-width: 900px; border: 1px solid rgba(255,255,255,0.1); }}
              .mac-dots {{ display: flex; gap: 8px; margin-bottom: 20px; }}
              .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
              .dot.red {{ background: #ff5f56; }}
              .dot.yellow {{ background: #ffbd2e; }}
              .dot.green {{ background: #27c93f; }}
              pre {{ margin: 0; }}
              code {{ border-radius: 8px; font-size: 18px; line-height: 1.5; font-family: 'Courier New', Courier, monospace; }}
            </style>
          </head>
          <body>
            <div class="mac-window" id="canvas">
              <div class="mac-dots">
                <div class="dot red"></div>
                <div class="dot yellow"></div>
                <div class="dot green"></div>
              </div>
              <pre><code class="language-auto">{html.escape(code_text)}</code></pre>
            </div>
            <script>hljs.highlightAll();</script>
          </body>
        </html>
        """
        
        print(f"🎨 [LOCAL RENDERER] Booting headless engine... (Theme: {theme})")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html_content)
            
            await page.wait_for_selector('code.hljs')
            
            element = await page.query_selector('#canvas')
            screenshot_bytes = await element.screenshot(omit_background=True)
            
            await browser.close()
            
            print("✅ [SUCCESS] Canvas painted locally!")
            
            img_buffer = io.BytesIO(screenshot_bytes)
            img_buffer.name = "snippet.png"
            return img_buffer

    except Exception as e:
        print(f"⚠️ [CRITICAL PLAYWRIGHT ERROR]: {e}")
        return None