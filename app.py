import streamlit as st
from main import *
import pandas as pd
from algoritmoGenetico import (
    algoritmoGenetico,
    gerarProblema
)

st.set_page_config(page_title="TSP", layout="centered")

st.title("Sistema de Otimização - TSP")

# ── MENU ─────────────────────────────────────
menu = st.sidebar.selectbox(
    "Menu",
    ["Métodos Básicos", "Métodos Genéticos", "Sobre"]
)

# ── SOBRE ────────────────────────────────────
if menu == "Sobre":

    st.header("Sobre o Projeto")

    st.info("""
Trabalho desenvolvido na disciplina de Programação Linear  
Alunos: Allisson Thomas Castilho e Pedro Henrique Bittencourt Fialho  
Curso: 5° ADS
""")

    st.write("""
O sistema implementa soluções para o Problema do Caixeiro Viajante (TSP),
cujo objetivo é encontrar a melhor rota possível entre pontos, minimizando o custo total.
""")

    with st.expander("Representação da Solução"):
        st.write("""
As soluções são representadas como permutações dos pontos.

Exemplo utilizado no sistema:
""")
        st.code("[0, 2, 4, 1, 3]")

    with st.expander("Matriz de Distâncias"):
        st.code("""
[0,5,7,6,8]
[5,0,3,4,6]
[7,3,0,2,5]
[6,4,2,0,3]
[8,6,5,3,0]
""")

    with st.expander("Avaliação da Solução"):
        st.write("""
O custo de uma rota é calculado pela soma das distâncias entre cidades consecutivas,
incluindo o retorno ao início.

Exemplo:
""")
        st.code("C = 5 + 3 + 2 + 3 + 8 = 21")

    with st.expander("Geração de Vizinhos"):
        st.write("""
Novas soluções são geradas trocando a posição de duas cidades na rota.

Também é utilizada uma abordagem que fixa uma posição e busca o melhor vizinho possível
a partir dela.
""")

    with st.expander("Métodos Utilizados"):
        st.write("""
Foram utilizadas três abordagens heurísticas:

- Subida da Encosta: busca local que aceita apenas melhorias.
- Subida da Encosta com Tentativas: continua explorando mesmo sem melhora por um limite.
- Têmpera Simulada: pode aceitar soluções piores para escapar de mínimos locais.
""")

    with st.expander("Análise"):
        st.write("""
O sistema permite executar os métodos individualmente ou compará-los entre si,
avaliando qual apresenta melhor desempenho.
""")

# ── GENÉTICOS ────────────────────────────────
elif menu == "Métodos Genéticos":

    if "ag_matriz" not in st.session_state:
        st.session_state.ag_matriz = None
        st.session_state.ag_melhor_inicial = None
        st.session_state.ag_melhor_final = None
        st.session_state.ag_custo_inicial = None
        st.session_state.ag_custo_final = None

    st.header("Algoritmo Genético")

    col1, col2 = st.columns(2)

    with col1:
        n = st.number_input(
            "Quantidade de cidades (N)",
            min_value=5,
            value=50
        )

        tp = st.number_input(
            "Tamanho da População (TP)",
            min_value=10,
            value=100
        )

        ng = st.number_input(
            "Número de Gerações (NG)",
            min_value=1,
            value=200
        )

    with col2:

        tc = st.number_input(
            "Taxa de Cruzamento (TC)",
            min_value=0.0,
            max_value=1.0,
            value=0.90
        )

        tm = st.number_input(
            "Taxa de Mutação (TM)",
            min_value=0.0,
            max_value=1.0,
            value=0.15
        )

        ig = st.number_input(
            "Elitismo (IG)",
            min_value=0.0,
            max_value=1.0,
            value=0.10
        )

    metodo_selecao = st.selectbox(
        "Método de Seleção",
        ["torneio", "roleta"]
    )

    st.divider()

    if st.button("Executar Algoritmo Genético"):

        matriz = gerarProblema(n)

        (
            melhor_inicial,
            melhor_final,
            custo_inicial,
            custo_final
        ) = algoritmoGenetico(
            matriz,
            tp,
            n,
            ng,
            tc,
            tm,
            ig,
            metodo_selecao
        )

        st.session_state.ag_matriz = matriz
        st.session_state.ag_melhor_inicial = melhor_inicial
        st.session_state.ag_melhor_final = melhor_final
        st.session_state.ag_custo_inicial = custo_inicial
        st.session_state.ag_custo_final = custo_final

        st.success("Execução concluída!")

    if st.session_state.ag_matriz is not None:

        st.subheader("Matriz")

        with st.expander("Visualizar matriz"):
            st.dataframe(
                st.session_state.ag_matriz,
                width="stretch"
            )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Melhor Solução Inicial")
            st.code(
                st.session_state.ag_melhor_inicial.tolist()
            )

            st.metric(
                "Custo Inicial",
                f"{st.session_state.ag_custo_inicial:.0f}"
            )

        with col2:
            st.subheader("Melhor Solução Final")
            st.code(
                st.session_state.ag_melhor_final.tolist()
            )

            st.metric(
                "Custo Final",
                f"{st.session_state.ag_custo_final:.0f}"
            )

        ganho = (
            st.session_state.ag_custo_inicial
            - st.session_state.ag_custo_final
        )

        melhoria = (
            ganho
            / st.session_state.ag_custo_inicial
        ) * 100

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"Ganho: {ganho:.0f}")

        with col2:
            st.success(f"Melhoria: {melhoria:.2f}%")
            
# ── MÉTODOS BÁSICOS ──────────────────────────
elif menu == "Métodos Básicos":

    st.header("Configuração")

    if "matriz" not in st.session_state:
        st.session_state.matriz = None
        st.session_state.si = None
        st.session_state.n = None
        st.session_state.vi = None
        st.session_state.resultado = None

    col1, col2 = st.columns(2)

    with col1:
        tipo = st.selectbox("Tipo de Execução", ["FIXO", "ALEATORIO"])

    with col2:
        n = None
        if tipo == "ALEATORIO":
            n = st.number_input("Tamanho", min_value=3, step=1)

    st.divider()

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("Gerar Problema"):
            matriz, si, n = preparar_problema(tipo, n)

            st.session_state.matriz = matriz
            st.session_state.si = si
            st.session_state.n = n
            st.session_state.vi = None
            st.session_state.resultado = None

            st.success("Problema gerado!")

    with col_btn2:
        if st.button("Solução Inicial"):
            if st.session_state.matriz is None:
                st.error("Gere o problema primeiro!")
            else:
                matriz = st.session_state.matriz
                si = st.session_state.si
                n = st.session_state.n

                vi = avaliar(n, si, matriz)
                st.session_state.vi = vi
                st.success("Solução inicial calculada!")

    st.divider()

    metodo_nome = st.selectbox(
        "Método",
        [
            "Subida de Encosta",
            "Subida de Encosta com Tentativas",
            "Têmpera Simulada",
            "Análise Comparativa"
        ]
    )

    mapa_metodos = {
        "Subida de Encosta": "SE",
        "Subida de Encosta com Tentativas": "SET",
        "Têmpera Simulada": "TE"
    }

    metodo = mapa_metodos.get(metodo_nome)

    tmax = None
    ti = tf = fr = None

    if metodo_nome == "Subida de Encosta com Tentativas":
        tmax = st.number_input("TMAX", min_value=1, step=1)

    if metodo_nome == "Têmpera Simulada":
        col1, col2, col3 = st.columns(3)
        with col1:
            ti = st.number_input("TI", value=500.0)
        with col2:
            tf = st.number_input("TF", value=1.0)
        with col3:
            fr = st.number_input("FR", value=0.95)

    st.divider()

    if st.button("Executar"):

        if st.session_state.matriz is None:
            st.error("Gere o problema primeiro!")
        else:
            matriz = st.session_state.matriz
            si = st.session_state.si
            n = st.session_state.n

            if metodo_nome == "Análise Comparativa":

                resultados = analise_tabela(matriz, si, n)

                df = pd.DataFrame(resultados, columns=["Método", "Observação", "Ganho"])

                st.success("Análise concluída!")
                st.dataframe(df, width="stretch") 

            else:
                sol, val = executar_metodo(
                    metodo,
                    matriz,
                    si,
                    n,
                    tmax=tmax,
                    ti=ti,
                    tf=tf,
                    fr=fr
                )

                st.session_state.resultado = (sol, val)
                st.success("Resultado encontrado!")

    st.divider()

    # ── RESULTADOS ──
    if st.session_state.matriz is not None:
        st.subheader("Matriz")
        st.dataframe(st.session_state.matriz, width="stretch")  # ✅ corrigido

    if st.session_state.si is not None and st.session_state.vi is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Solução Inicial")
            st.code(st.session_state.si.tolist())

        with col2:
            st.subheader("Custo Inicial")
            st.write(st.session_state.vi)

    if st.session_state.resultado is not None:
        sol, val = st.session_state.resultado

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Solução Final")
            st.code(sol.tolist())

        with col2:
            st.subheader("Custo Final")
            st.write(val)

        if st.session_state.vi is not None:
            ganho = st.session_state.vi - val
            porcentagem = (ganho / st.session_state.vi) * 100

            st.success(f"Ganho: {ganho}")
            st.success(f"Melhoria: {porcentagem:.2f}%")