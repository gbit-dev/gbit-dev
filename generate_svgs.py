import os

def create_terminal_svg(filename, title, lines, width=800, height=400):
    svg_header = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <rect width="{width}" height="{height}" rx="10" ry="10" fill="#1e1e1e"/>
    <circle cx="20" cy="20" r="6" fill="#ff5f56"/>
    <circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
    <circle cx="60" cy="20" r="6" fill="#27c93f"/>
    <text x="400" y="24" fill="#a0a0a0" font-family="monospace" font-size="14" text-anchor="middle">{title}</text>
    <g font-family="Consolas, Monaco, monospace" font-size="14" fill="#e0e0e0">
"""
    
    y = 60
    svg_content = ""
    for line in lines:
        if line.startswith("!"):
            color = "#a0a0a0"
            line = line[1:]
        elif line.startswith("+"):
            color = "#27c93f"
            line = line[1:]
        elif line.startswith("-"):
            color = "#ff5f56"
            line = line[1:]
        elif line.startswith("*"):
            color = "#ffbd2e"
            line = line[1:]
        elif line.startswith("$"):
            color = "#56b6c2"
            line = line[1:]
        else:
            color = "#e0e0e0"
        
        # Escape XML chars
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        svg_content += f'        <text x="20" y="{y}" fill="{color}">{line}</text>\n'
        y += 20
        
    svg_footer = """    </g>\n</svg>"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_header + svg_content + svg_footer)

automacao_lines = [
    "$ python smart_briefing.py",
    "🚀 Iniciando geração do Smart Briefing...",
    "🌤️ Buscando dados do clima...",
    "📰 Buscando notícias de tecnologia...",
    "+ ✅ Briefing gerado com sucesso: briefing_2023-10-25.md",
    "!",
    "$ cat briefing_2023-10-25.md",
    "# 🌅 Smart Briefing Matinal - 25/10/2023",
    "",
    "## 🌤️ Previsão do Tempo",
    "- **Máxima:** 28°C",
    "- **Mínima:** 18°C",
    "",
    "## 💻 Top Tech News (HackerNews)",
    "1. Show HN: I built a new open-source AI agent framework",
    "2. PostgreSQL 16 Released",
    "3. Why we moved away from microservices"
]

ia_lines = [
    "$ python ai_code_reviewer.py meu_script.py",
    "🤖 Analisando o seu código... Aguarde.",
    "!",
    "==================================================",
    "* ✨ RESULTADO DO CODE REVIEW ✨",
    "==================================================",
    "",
    "**1. Visão Geral**",
    "Este script Python é um servidor web simples utilizando FastAPI.",
    "",
    "**2. Pontos Positivos**",
    "+ O código está limpo, bem indentado e utiliza type hints adequadamente.",
    "+ As rotas estão bem definidas com verbos HTTP corretos.",
    "",
    "**3. Melhorias de Refatoração / Clean Code**",
    "- Considere extrair a lógica de banco de dados para um módulo separado.",
    "- Evite variáveis globais (ex: `db_connection`).",
    "",
    "**4. Segurança e Bugs**",
    "- ⚠️ **ATENÇÃO:** Encontrei uma vulnerabilidade de SQL Injection na linha 42.",
    "Nunca concatene strings diretamente em queries. Use parâmetros preparados."
]

create_terminal_svg("automacao/demo.svg", "bash - smart_briefing.py", automacao_lines, width=700, height=450)
create_terminal_svg("ia/demo.svg", "bash - ai_code_reviewer.py", ia_lines, width=700, height=500)

print("SVGs gerados com sucesso!")
