from agno.agent import Agent
from agno.models.openai import OpenAIChat
from knowledge import knowledge_base
from utils import extrair_texto_pdf, anonimizar_texto

# 1. Agente de Leitura (Ementário da Casa)
leitor_interno = Agent(
    name="Leitor de Ementários Internos",
    role="Especialista em documentos acadêmicos da UFMS",
    model=OpenAIChat(id="gpt-5-nano"),
    instructions=["Você é um Analista de Documentos Acadêmicos da UFMS. Sua tarefa é transformar PDFs brutos em dados estruturados. Foque em extrair: 1. Nome da Disciplina, 2. Carga Horária Total, 3. Ementa (conteúdo programático) e 4. Bibliografia. Se o texto estiver truncado, use lógica para reconstruir termos acadêmicos conhecidos."],
)

# 2. Agente de Leitura (Ementário Externo)
leitor_externo = Agent(
    name="Leitor de Ementários Externos",
    role="Analista de documentos de outras IES",
    model=OpenAIChat(id="gpt-5-nano"),
    instructions=["Você é um Analista de Documentos Acadêmicos de outras IES. Sua tarefa é transformar PDFs brutos em dados estruturados. Foque em extrair: 1. Nome da Disciplina, 2. Carga Horária Total, 3. Ementa (conteúdo programático) e 4. Bibliografia. Se o texto estiver truncado, use lógica para reconstruir termos acadêmicos conhecidos."],
)

# 3. Agente LGPD (Anonimizador)
agente_lgpd = Agent(
    name="Protetor de Dados",
    role="Auditor de Privacidade",
    model=OpenAIChat(id="gpt-5-nano"),
    instructions=["Você é um Oficial de Proteção de Dados (DPO). Sua missão é agir antes que os dados cheguem à análise de similaridade. Identifique e remova: Nomes de alunos, números de matrícula, CPFs, e-mails, endereços e assinaturas. Substitua-os por '[DADO ANONIMIZADO]'. Mantenha a integridade total do conteúdo das disciplinas."],
)

# 4. Analista RAG
analista_similaridade = Agent(
    name="Analista_Academico_RAG",
    role="Especialista em Equivalência de Disciplinas",
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Ao receber uma ementa de um aluno, busque no banco de dados a disciplina correspondente.",
        "Compare a carga horária e o conteúdo programático.",
        "Se não encontrar uma disciplina com mais de 75% de similaridade, informe que não há equivalente.",
        "Sempre cite o nome da disciplina interna encontrada para comparação.",
        "Fazer um ranking de top 5 disciplinas mais similares."
    ],
)

# 5. Agente Diretor
diretor_coordenacao = Agent(
    team=[leitor_interno, leitor_externo, agente_lgpd, analista_similaridade],
    name="Diretor de Aproveitamento",
    role="Coordenador de Curso Final",
    model=OpenAIChat(id="gpt-4o"),
    instructions=["Você é o Coordenador de Curso. Você recebe os relatórios dos agentes de leitura, privacidade e similaridade. Sua função é dar a palavra final. Se o match for > 75% e a carga horária for compatível, declare 'DEFERIDO'. Caso contrário, 'INDEFERIDO'. Sempre apresente uma justificativa técnica curta e clara para o aluno. Faça também um Top 5 das disciplinas mais semelhantes."],
    show_tool_calls=True,
    markdown=True

)
