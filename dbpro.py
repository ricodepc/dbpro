import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(page_title="Catálogo de Produtos Nuvem", layout="centered")
st.title("📦 Meu Catálogo de Produtos (Neon + Streamlit)")

# Função para conectar usando a URL secreta do Streamlit
def criar_conexao():
    # Ele vai buscar a URL configurada no painel do Streamlit ou localmente
db_url = st.secrets["DATABASE_URL"]

    return psycopg2.connect(db_url)

st.subheader("📊 Produtos Cadastrados em Tempo Real (PostgreSQL na Nuvem)")

try:
    conn = criar_conexao()
    
    query = """
        SELECT 
            p.id AS "ID", 
            p.nome_produto AS "Produto", 
            p.preco AS "Preço (R$)", 
            c.nome_categoria AS "Categoria"
        FROM produtos p
        INNER JOIN categorias c ON p.categoria_id = c.id;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()

    st.dataframe(df, use_container_width=True)
    
    # Métricas
    col1, col2 = st.columns(2)
    col1.metric("Total de Produtos", len(df))
    col2.metric("Preço Médio", f"R$ {df['Preço (R$)'].mean():.2f}")

except Exception as e:
    st.error("Erro ao conectar ao Neon.tech:")
    st.code(e)
