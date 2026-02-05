from phi.agent import Agent
from phi.model.openai import OpenAIChat
from knowledge import knowledge_base

# 1. Agente de Proteção de Dados (LGPD)
agente_lgpd = Agent(
    name="DPO_Agente",
    role="Garantir conformidade com a LGPD",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Identifique e remova dados pessoais (Nome, CPF, Matrícula) do texto fornecido.",
        "Mantenha intactos os nomes das disciplinas e ementas acadêmicas.",
        "Retorne apenas o texto limpo para o próximo agente."
    ]
)

# 2. Agente Analista com RAG (Usa o LanceDB)
analista_similaridade = Agent(
    name="Analista_Academico",
    role="Especialista em Equivalência de Disciplinas",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Ao receber uma ementa, busque no banco de dados a disciplina interna correspondente.",
        "Compare carga horária (mínimo 80% de compatibilidade).",
        "Compare conteúdo programático (mínimo 75% de similaridade).",
        "Gere uma tabela comparativa entre os tópicos."
    ]
)

# 3. Agente Diretor (Orquestrador)
diretor_coordenacao = Agent(
    team=[agente_lgpd, analista_similaridade],
    name="Diretor_ESAN",
    role="Coordenador de Curso Final",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Coordene a análise: primeiro peça a anonimização ao DPO.",
        "Depois, peça a análise de similaridade técnica.",
        "Emita o parecer final: DEFERIDO ou INDEFERIDO.",
        "Apresente uma justificativa clara baseada nos dados encontrados."
    ],
    show_tool_calls=True,
    markdown=True
)
