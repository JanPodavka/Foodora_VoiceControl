
def web_help(items,title = "Vybrané restaurace"):
    overlay_content = """
        <div id="customOverlay" style="
            position: fixed;
            top: 10px;
            right: 10px;
            width: 300px;
            height: 400px; /* Set a fixed height */
            overflow-y: auto; /* Enable vertical scrolling */
            background: white;
            border: 1px solid black;
            padding: 10px;
            z-index: 10000;">
            <h3>""" + title + """"</h3>
            <ul>
        """
    for index, name in enumerate(items):
        overlay_content += f"<li>{index}.{name}</li>"
    overlay_content += "</ul><button id='closeOverlay'>Close</button></div>"
    return overlay_content



def web_inject(overlay, driver):
    driver.execute_script(f"""
        var existingOverlay = document.getElementById('customOverlay');
        if (existingOverlay) {{
            existingOverlay.remove();
        }}
        var div = document.createElement('div');
        div.innerHTML = `{overlay}`;
        document.body.appendChild(div);
        document.getElementById('closeOverlay').onclick = function() {{
            document.getElementById('customOverlay').remove();
        }};
    """)
