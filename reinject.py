import json

with open('api/data.json', 'r') as f:
    api_data = f.read()

script_to_inject = f"""
<script>
  const mockedApiData = {api_data};
  const origFetch_new = window.fetch;
  window.fetch = async function() {{
    const url = arguments[0];
    if (url && typeof url === "string" && url.includes("/api/invites/get/byURL")) {{
        return new Response(JSON.stringify(mockedApiData), {{
            status: 200,
            headers: {{ 'Content-Type': 'application/json' }}
        }});
    }}
    return origFetch_new.apply(this, arguments);
  }};
</script>
"""

with open('index.html', 'r') as f:
    html = f.read()

# Insert right after <head>, ONLY ONCE
html = html.replace("<head>", "<head>\n" + script_to_inject, 1)

with open('index.html', 'w') as f:
    f.write(html)
