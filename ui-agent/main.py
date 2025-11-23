# main.py
import os
import logfire
from dotenv import load_dotenv

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import uvicorn

load_dotenv()
logfire.configure()

# Default prices for items
def get_item_price(item):
    prices = {
        'apple': 1.5,
        'banana': 1.0,
        'laptop': 1200.0,
        'phone': 800.0,
        'book': 20.0,
        'headphones': 50.0,
        'shoes': 60.0,
        't-shirt': 15.0,
        'watch': 200.0,
        'bag': 40.0,
        'camera': 500.0,
        'mouse': 25.0,
        'keyboard': 45.0,
    }
    for key, price in prices.items():
        if key in item.lower():
            return price
    return 10.0  # default price

# Emoji helper for cart items
def get_item_emoji(item):
    mapping = {
        'apple': '🍎',
        'banana': '🍌',
        'laptop': '💻',
        'phone': '📱',
        'book': '📚',
        'headphones': '🎧',
        'shoes': '👟',
        't-shirt': '👕',
        'watch': '⌚',
        'bag': '👜',
        'camera': '📷',
        'mouse': '🖱️',
        'keyboard': '⌨️',
        'cart': '🛒',
    }
    for key, emoji in mapping.items():
        if key in item.lower():
            return emoji
    return '🛒'

# Simple in-memory chat state and cart
chat_history = []
cart = {}  # item_name -> quantity

# Local screenshot/logo paths (from your uploaded images)
LOGO_1 = "/mnt/data/Screenshot 2025-11-23 at 3.06.27 PM.png"
LOGO_2 = "/mnt/data/Screenshot 2025-11-23 at 3.06.32 PM.png"

async def homepage(request):
    logfire.info("Homepage accessed", path=str(request.url.path))
    # Ensure the first message is from the assistant
    if not chat_history:
        chat_history.append({
            "role": "Assistant",
            "text": "Hii, good afternoon, I'm E-commerce chat assistant. How can I help you?"
        })
    messages_html = "".join(render_message_html(m) for m in chat_history)
    cart_html = cart_list_html()
    total = sum(get_item_price(item) * qty for item, qty in cart.items())

    # Main beautiful UI: modern card, sidebar, composer
    html = f'''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>E-Commerce Chat Assistant</title>
      <style>
        :root{{
          --bg1: linear-gradient(180deg,#f4f8ff 0%, #eef4ff 100%);
          --card: #ffffff;
          --accent: #2563eb;
          --muted: #6b7280;
          --glass: rgba(255,255,255,0.7);
          --radius: 16px;
          --shadow-1: 0 8px 30px rgba(12, 20, 40, 0.08);
        }}
        html,body{{height:100%;margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial; background: var(--bg1); color:#0b1220;}}
        .container{{max-width:1200px;margin:32px auto;padding:16px;display:flex;gap:24px;box-sizing:border-box;align-items:flex-start}}
        .chat-card{{flex:1;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow-1);padding:28px;min-height:560px;position:relative;overflow:hidden}}
        .header{{display:flex;align-items:center;gap:14px;margin-bottom:18px}}
        .logo{{width:56px;height:56px;border-radius:12px;overflow:hidden;flex:0 0 56px;box-shadow:0 6px 18px rgba(37,99,235,0.14)}}
        .logo img{{width:100%;height:100%;object-fit:cover;display:block}}
        .title{{font-size:20px;color:var(--accent);font-weight:700}}
        .subtitle{{font-size:13px;color:var(--muted)}}
        #messages{{display:flex;flex-direction:column;gap:14px;max-height:420px;overflow:auto;padding-right:8px;padding-left:2px}}
        /* message bubbles */
        .msg{{max-width:72%;padding:12px 14px;border-radius:12px;box-shadow:0 6px 18px rgba(15,23,42,0.06);animation:pop 0.36s ease;line-height:1.3}}
    .assistant{{background:linear-gradient(180deg,#fafbff,#f3f6ff);align-self:flex-start;border-top-left-radius:4px}}
    .user{{background:linear-gradient(180deg,#eaf2ff,#dfeeff);align-self:flex-end;border-top-right-radius:4px;text-align:right}}
    .msg .role{{display:block;font-weight:700;margin-bottom:6px;font-size:13px}}
    .composer{{position:absolute;left:28px;right:28px;bottom:18px;padding:12px;border-radius:12px;background:linear-gradient(180deg,#ffffff,#fbfdff);display:flex;gap:8px;align-items:center;box-shadow:0 8px 30px rgba(37,99,235,0.06)}}
    .composer input{{flex:1;padding:12px 14px;border-radius:10px;border:1px solid #e6eefc;background:#f8fbff;font-size:15px;outline:none}}
    .send-btn{{padding:10px 18px;border-radius:10px;background:linear-gradient(90deg,#4f8cff,#2563eb);border:none;color:white;font-weight:700;cursor:pointer;box-shadow:0 8px 26px rgba(37,99,235,0.18)}}
    .cart-panel{{width:320px;min-width:280px;background:linear-gradient(180deg,#fff,#fbfdff);border-radius:var(--radius);padding:18px;box-shadow:var(--shadow-1);position:sticky;top:32px;height:fit-content}}
    .cart-panel h3{{margin:0 0 8px 0;color:var(--accent);display:flex;align-items:center;gap:8px}}
    .cart-list{{list-style:none;padding:0;margin:6px 0 8px 0;display:flex;flex-direction:column;gap:8px}}
    .cart-item{{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:10px;border-radius:10px;border:1px solid #eef4ff;background:rgba(250,251,255,0.7)}}
    .cart-item .left{{display:flex;gap:10px;align-items:center;flex:1}}
    .emoji{{font-size:20px;display:inline-block;width:36px;height:36px;border-radius:8px;background:white;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(2,6,23,0.04)}}
    .cart-item .meta{{font-size:14px;}}
    .cart-item .qty-controls{{display:flex;align-items:center;gap:8px}}
    .qty-controls button{{background:transparent;border:1px solid #e6eefc;padding:6px 8px;border-radius:8px;cursor:pointer}}
    .total-row{{margin-top:12px;font-weight:800;color:var(--accent);font-size:17px;text-align:right}}
    .empty{{color:var(--muted);font-style:italic;padding:12px;text-align:center}}
    /* small responsive */
@media (max-width:980px) {{
  .container {{
    flex-direction: column;
    padding: 12px;
  }}
  .cart-panel {{
    width: 100%;
    position: relative;
    top: 0;
  }}
  .composer {{
    left: 12px;
    right: 12px;
  }}
}}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="chat-card" role="main">
          <div class="header">
            <div class="logo">
              <img src="https://static.vecteezy.com/system/resources/previews/023/753/025/non_2x/ai-e-commerce-icon-in-illustration-vector.jpg" alt="logo" onerror="this.style.display='none'"/>
            </div>
            <div>
              <div class="title">E-Commerce Chat Assistant</div>
            </div>
          </div>

          <div id="messages" aria-live="polite">
            {messages_html}
          </div>

          <form id="composer" class="composer" autocomplete="off">
            <input name="message" id="message-input" type="text" placeholder="Try: add apple / remove laptop / show cart" />
            <button class="send-btn" type="submit">Send</button>
          </form>
        </div>

        <aside class="cart-panel" aria-label="shopping cart">
          <h3>🛒 Cart</h3>
          <ul id="cart-items" class="cart-list">
            {cart_html or '<li class="empty">Cart is empty — add something from chat!</li>'}
          </ul>
          <div id="cart-total" class="total-row">Total: ${{0.0}}</div>
        </aside>
      </div>

      <script>
        // helper to re-render messages and cart from server responses
        async function postMessage(text){{
          const fd = new FormData();
          fd.append('message', text);
          const res = await fetch('/chat', {{ method: 'POST', body: fd }});
          const j = await res.json();
          document.getElementById('messages').innerHTML = j.html;
          scrollMessages();
        }}

        async function refreshCart(){{
          const res = await fetch('/cart');
          const j = await res.json();
          document.getElementById('cart-items').innerHTML = j.html;
          document.getElementById('cart-total').innerHTML = j.total_html;
        }}

        function scrollMessages(){{
          const m = document.getElementById('messages');
          m.scrollTop = m.scrollHeight;
        }}

        // composer submit
        document.getElementById('composer').onsubmit = async function(e){{
          e.preventDefault();
          const input = document.getElementById('message-input');
          const txt = input.value.trim();
          if(!txt) return;
          await postMessage(txt);
          input.value = '';
          await refreshCart();
        }};

        // delegate cart actions (increase / decrease / remove)
        document.getElementById('cart-items').addEventListener('click', async function(e){{
          const target = e.target;
          const item = target.closest('[data-item]');
          if(!item) return;
          const name = item.dataset.item;
          if(target.matches('.remove-btn')){{
            await fetch('/remove', {{ method:'POST', body: new URLSearchParams({{item:name}}) }});
            await refreshCart();
            const r = await fetch('/chat', {{ method:'POST', body: new URLSearchParams({{message: `removed ${{name}}`}}) }});
            const j = await r.json();
            document.getElementById('messages').innerHTML = j.html;
            scrollMessages();
          }} else if (target.matches('.inc-btn')){{
            await fetch('/adjust', {{ method:'POST', body: new URLSearchParams({{item:name, delta: '1'}}) }});
            await refreshCart();
          }} else if (target.matches('.dec-btn')){{
            await fetch('/adjust', {{ method:'POST', body: new URLSearchParams({{item:name, delta: '-1'}}) }});
            await refreshCart();
          }}
        }});

        // initial scroll
        scrollMessages();
      </script>
    </body>
    </html>
    '''
    return HTMLResponse(html)

def render_message_html(m):
    role = m.get("role", "Assistant")
    text = m.get("text", "")
    css_class = "assistant" if role.lower().startswith("assistant") else "user"
    role_label = "Assistant" if css_class == "assistant" else "User"
    # simple HTML escaping
    safe_text = (text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>"))
    return f'<div class="msg {css_class}"><span class="role">{role_label}:</span><div class="text">{safe_text}</div></div>'

def cart_list_html():
    if not cart:
        return ''
    parts = []
    for item, qty in cart.items():
        emoji = get_item_emoji(item)
        price = get_item_price(item)
        parts.append(
            f'''<li class="cart-item" data-item="{item}">
                  <div class="left">
                    <div class="emoji">{emoji}</div>
                    <div class="meta"><div style="font-weight:700">{item}</div><div style="font-size:13px;color:#6b7280">${price:.2f} each</div></div>
                  </div>
                  <div style="display:flex;align-items:center;gap:8px">
                    <div class="qty-controls">
                      <button class="dec-btn" title="Decrease">−</button>
                      <span style="padding:0 6px;font-weight:700">{qty}</span>
                      <button class="inc-btn" title="Increase">+</button>
                    </div>
                    <button class="remove-btn" style="margin-left:8px;border-radius:8px;padding:6px 8px;border:1px solid #fde68a;background:#fff8e0;cursor:pointer">Remove</button>
                  </div>
               </li>'''
        )
    return "\n".join(parts)

# Chat endpoint - accepts natural language commands, mutates cart and chat_history
async def chat(request: Request):
    logfire.info("Chat endpoint called", method=request.method)
    import re
    form = await request.form()
    message = form.get('message', '').strip()
    response = ""
    if message:
        chat_history.append({"role": "User", "text": message})
        lower = message.lower()
        # Try to extract item name for natural language
        item = None
        # add patterns
        if match := re.search(r"add (?:one more |another |an |a )?(.*?)(?: to cart)?$", lower):
            item = match.group(1).strip()
            if item:
                cart[item] = cart.get(item, 0) + 1
                response = f"Added 1 {item} to cart."
        elif match := re.search(r"increase (.*?) count|increase (.*?) quantity|increase (.*)", lower):
            item = (match.group(1) or match.group(2) or match.group(3) or '').strip()
            if item in cart:
                cart[item] += 1
                response = f"Increased {item} quantity to {cart[item]}."
            else:
                response = f"{item} not in cart."
        elif match := re.search(r"decrease (.*?) count|decrease (.*?) quantity|decrease (.*)", lower):
            item = (match.group(1) or match.group(2) or match.group(3) or '').strip()
            if item in cart:
                cart[item] -= 1
                if cart[item] <= 0:
                    del cart[item]
                    response = f"Removed {item} from cart."
                else:
                    response = f"Decreased {item} quantity to {cart[item]}."
            else:
                response = f"{item} not in cart."
        elif match := re.search(r"remove (.*?)$", lower):
            item = match.group(1).strip()
            if item in cart:
                del cart[item]
                response = f"Removed {item} from cart."
            else:
                response = f"{item} not in cart."
        elif lower == "show cart" or lower == "cart":
            if cart:
                response = "Cart contents:<br>" + "<br>".join(f"{item}: {qty}" for item, qty in cart.items())
            else:
                response = "Cart is empty."
        else:
            response = "Hii!! How can I help you?"
        chat_history.append({"role": "Assistant", "text": response})
    messages_html = "".join(render_message_html(m) for m in chat_history)
    return JSONResponse({"html": messages_html})

# Cart API returns HTML for sidebar and a separate text for total (so client can set both)
async def cart_api(request: Request):
    logfire.info("Cart API accessed", method=request.method)
    cart_html = cart_list_html()
    total = sum(get_item_price(item) * qty for item, qty in cart.items())
    total_html = f"Total: ${total:.2f}"
    html = (cart_html or '<li class="empty">Cart is empty — add something from chat!</li>')
    return JSONResponse({"html": html, "total_html": total_html})

# Remove a single item entirely
async def remove_item(request: Request):
    form = await request.form()
    item = form.get('item', '').strip()
    if item in cart:
        del cart[item]
        logfire.info("Removed item from cart", item=item)
        return JSONResponse({"ok": True})
    return JSONResponse({"ok": False, "error": "item not in cart"}, status_code=400)

# Adjust quantity by delta (+1 or -1 expected)
async def adjust_item(request: Request):
    form = await request.form()
    item = form.get('item', '').strip()
    try:
        delta = int(form.get('delta', '0'))
    except:
        delta = 0
    if not item:
        return JSONResponse({"ok": False, "error": "missing item"}, status_code=400)
    if item not in cart and delta > 0:
        cart[item] = delta
    elif item in cart:
        cart[item] = cart[item] + delta
        if cart[item] <= 0:
            del cart[item]
    return JSONResponse({"ok": True})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/chat', chat, methods=["POST"]),
    Route('/cart', cart_api),
    Route('/remove', remove_item, methods=["POST"]),
    Route('/adjust', adjust_item, methods=["POST"]),
])

if __name__ == "__main__":
    # keep printing the logfire project url if available for debugging
    project_url = os.getenv("LOGFIRE_PROJECT_URL", "https://logfire-eu.pydantic.dev/basha/starter-project-ai")
    print("Logfire project URL:", project_url)
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8020)))
