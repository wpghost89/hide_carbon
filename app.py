# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text
# import streamlit as st
# import pandas as pd
# from groq import Groq
# from comandos import instrucao

# load_dotenv()

# def criar_engine():
#     database_url = os.getenv("DATABASE_URL")
#     if not database_url:
#         raise ValueError('Variável de ambiente DATABASE_URL não configurada.')
#     return create_engine(database_url)

# engine = criar_engine()

# if 'df' not in st.session_state:
#     with engine.connect() as conn:
#         st.session_state.df = pd.read_sql(text('select * from vendas_produtos'), conn)


# # LAYOUT STREAMLIT
# st.set_page_config(layout='wide', page_title='Consultor SQL Carbon')
# col1, col2 = st.columns([0.6,0.4])
# with col1:
#     with st.form('form-pergunta'):
#         pergunta = st.text_area('O que você quer saber sobre seus dados?',
#                     placeholder='Total de vendas de agosto de 2026', height=200)
#         enviar_pergunta = st.form_submit_button('Enviar Pergunta')

#         if enviar_pergunta:
#             if pergunta:
#                 instrucao += pergunta
#                 with st.spinner('Gerando resposta'):
#                     client = Groq(api_key=os.getenv('GROQ_API_KEY'))
#                     completion = client.chat.completions.create(
#                         model="openai/gpt-oss-120b",
#                         messages=[{"role": "user","content": instrucao}],
#                         temperature=0.2,
#                     )
#                     st.session_state.sql_gerado = completion.choices[0].message.content
#             else:
#                 st.error('Escreva a sua pergunta')

# with col2:
#     if 'sql_gerado' not in st.session_state:
#         st.session_state.sql_gerado = ''
    
#     with st.form('form-sql'):
#         sql_editavel = st.text_area('SQL Gerado',value=st.session_state.sql_gerado, height=200)
#         executar_sql = st.form_submit_button('Executar consulta')

#         if executar_sql:
#             with engine.connect() as conn:
#                 st.session_state.df = pd.read_sql(text(sql_editavel), conn)
#                 st.success('Consulta realizada')

# st.dataframe(st.session_state.df)
##############################################

from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
from groq import Groq
from comandos import instrucao


def criar_engine():

    database_url = st.secrets.get('DATABASE_URL')
    if not database_url:
        raise ValueError('Variável de ambiente DATABASE_URL não configurada.')
    return create_engine(database_url)

engine = criar_engine()

if 'df' not in st.session_state:
    with engine.connect() as conn:
        st.session_state.df = pd.read_sql(text('select * from vendas_produtos'), conn)


# LAYOUT STREAMLIT
st.set_page_config(layout='wide', page_title='Consultor SQL Carbon')
col1, col2 = st.columns([0.6,0.4])
with col1:
    with st.form('form-pergunta'):
        pergunta = st.text_area('O que você quer saber sobre seus dados?',
                    placeholder='Total de vendas de agosto de 2026', height=200)
        enviar_pergunta = st.form_submit_button('Enviar Pergunta')

        if enviar_pergunta:
            if pergunta:
                instrucao += pergunta
                with st.spinner('Gerando resposta'):
                    client = Groq(api_key=st.secrets.get(('GROQ_API_KEY')))
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[{"role": "user","content": instrucao}],
                        temperature=0.2,
                    )
                    st.session_state.sql_gerado = completion.choices[0].message.content
            else:
                st.error('Escreva a sua pergunta')

with col2:
    if 'sql_gerado' not in st.session_state:
        st.session_state.sql_gerado = ''
    
    with st.form('form-sql'):
        sql_editavel = st.text_area('SQL Gerado',value=st.session_state.sql_gerado, height=200)
        executar_sql = st.form_submit_button('Executar consulta')

        if executar_sql:
            with engine.connect() as conn:
                st.session_state.df = pd.read_sql(text(sql_editavel), conn)
                st.success('Consulta realizada')

st.dataframe(st.session_state.df)

###############################################
# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text
# import streamlit as st
# import pandas as pd
# from groq import Groq
# from comandos import instrucao

# load_dotenv()

# def criar_engine():
#     database_url = os.getenv("DATABASE_URL")
#     if not database_url:
#         raise ValueError('Variavel de ambiente DATABASE_URL não configurada.')
#     return create_engine(database_url)

# engine = criar_engine()

# # Inicializa o DataFrame padrão no session_state caso não exista
# if 'df_resultado' not in st.session_state:
#     with engine.connect() as conn:
#         st.session_state.df_resultado = pd.read_sql(text('select * from vendas_produtos'), conn)

# if 'sql_gerado' not in st.session_state:
#     st.session_state.sql_gerado = ''

# # LAYOUT STREAMLIT
# st.set_page_config(layout='wide', page_title='Consultor SQL Carbon')
# col1, col2 = st.columns([0.6, 0.4])

# with col1:
#     with st.form('form-pergunta'):
#         pergunta = st.text_area('O que você quer saber sobre seus dados?', placeholder='Total de vendas de agosto de 2026', height=200)
#         enviar_pergunta = st.form_submit_button('Enviar pergunta')

#         if enviar_pergunta:
#             if pergunta:
#                 # Cuidado: se 'instrucao' for uma string que acumula a cada clique, 
#                 # o ideal é usar uma variável local para a mensagem da IA.
#                 prompt_completo = instrucao + "\n" + pergunta
#                 with st.spinner('Gerando resposta'):
#                     client = Groq(api_key=os.getenv('GROQ_API_KEY'))
#                     completion = client.chat.completions.create(
#                        model="openai/gpt-oss-120b",
#                        messages=[{"role": "user", "content": prompt_completo}],
#                        temperature=0.2
#                     )
#                     st.session_state.sql_gerado = completion.choices[0].message.content
#                     st.rerun() # Força a atualização da tela para o SQL aparecer no input da coluna 2
#             else:
#                 st.error('Escreva sua pergunta')

# with col2:
#     with st.form('form-sql'):
#         # Usamos o session_state diretamente para refletir o SQL gerado
#         sql_editavel = st.text_area('SQL Gerado', value=st.session_state.sql_gerado, height=200)
#         executar_sql = st.form_submit_button('Executar consulta')

#         if executar_sql:
#             if sql_editavel:
#                 try:
#                     with engine.connect() as conn:
#                         st.session_state.df_resultado = pd.read_sql(text(sql_editavel), conn)
#                     st.success('Consulta realizada')
#                 except Exception as e:
#                     st.error(f'Erro ao executar a consulta: {e}')
#             else:
#                 st.warning('Nenhum código SQL para executar.')

# # Exibe o DataFrame atualizado na tela
# st.dataframe(st.session_state.df_resultado)