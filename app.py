import streamlit as st
from main import *
import pandas as pd

st.set_page_config(page_title="TSP", layout="centered")

st.title("Sistema de Otimização - TSP")

# ── MENU ─────────────────────────────────────
menu = st.sidebar.selectbox(
    "Menu",
    ["Métodos Básicos", "Métodos Genéticos", "Sobre"]
)

# ── SOBRE ────────────────────────────────────
if menu == "Sobre":
    st.write("Trabalho de Otimização com heurísticas:")
    st.write("- Subida da Encosta")
    st.write("- SET")
    st.write("- Têmpera Simulada")

# ── GENÉTICOS ────────────────────────────────
elif menu == "Métodos Genéticos":
    st.warning("Módulo em desenvolvimento")

# ── MÉTODOS BÁSICOS ──────────────────────────
elif menu == "Métodos Básicos":

    st.header("Configuração")

    # ── Estado persistente ──
    if "matriz" not in st.session_state:
        st.session_state.matriz = None
        st.session_state.si = None
        st.session_state.n = None
        st.session_state.vi = None
        st.session_state.resultado = None

    # ── Tipo ──
    tipo = st.selectbox("Tipo de Execução", ["FIXO", "ALEATORIO"])

    n = None
    if tipo == "ALEATORIO":
        n = st.number_input("Tamanho do Problema", min_value=3, step=1)

    # ── GERAR PROBLEMA ──
    if st.button("Gerar Problema", key="btn_gerar"):
        matriz, si, n = preparar_problema(tipo, n)

        st.session_state.matriz = matriz
        st.session_state.si = si
        st.session_state.n = n
        st.session_state.vi = None
        st.session_state.resultado = None

        st.success("Problema gerado!")

    # ── SOLUÇÃO INICIAL ──
    if st.button("Solução Inicial", key="btn_si"):
        if st.session_state.matriz is None:
            st.error("Gere o problema primeiro!")
        else:
            matriz = st.session_state.matriz
            si = st.session_state.si
            n = st.session_state.n

            vi = avaliar(n, si, matriz)
            st.session_state.vi = vi

    # ── Método ──
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

    # ── Parâmetros ──
    tmax = None
    ti = tf = fr = None

    if metodo_nome == "Subida de Encosta com Tentativas":
        tmax = st.number_input("TMAX", min_value=1, step=1)

    if metodo_nome == "Têmpera Simulada":
        ti = st.number_input("TI", value=500.0)
        tf = st.number_input("TF", value=1.0)
        fr = st.number_input("FR", value=0.95)

    # ── EXECUTAR ──
    if st.button("Executar", key="btn_exec"):

        if st.session_state.matriz is None:
            st.error("Gere o problema primeiro!")
        else:
            matriz = st.session_state.matriz
            si = st.session_state.si
            n = st.session_state.n

            # 🔥 ANÁLISE COMPARATIVA
            if metodo_nome == "Análise Comparativa":

                vi = avaliar(n, si, matriz)
                resultados = []

                # ───── SE ─────
                sol, val = subida_da_encosta(matriz, n, si)
                resultados.append(("SE", "-", vi - val))

                # ───── SET ─────
                configs_set = [
                    ("TMAX=N", n),
                    ("TMAX=2N", 2*n),
                    ("TMAX=N/2", int(n/2))
                ]

                for nome, tmax_cfg in configs_set:
                    sol, val = subida_da_encosta_tentativas(matriz, n, tmax_cfg)
                    resultados.append(("SET", nome, vi - val))

                # ───── TÊMPERA ─────
                configs_te = [
                    ("TI=100 TF=0.1 FR=0.8", 100, 0.1, 0.8),
                    ("TI=200 TF=0.1 FR=0.8", 200, 0.1, 0.8),
                    ("TI=500 TF=0.1 FR=0.8", 500, 0.1, 0.8),
                    ("TI=200 TF=0.1 FR=0.9", 200, 0.1, 0.9),
                    ("TI=500 TF=0.1 FR=0.9", 500, 0.1, 0.9),
                    ("TI=200 TF=0.01 FR=0.9", 200, 0.01, 0.9),
                    ("TI=500 TF=0.01 FR=0.9", 500, 0.01, 0.9),
                ]

                for nome, ti_cfg, tf_cfg, fr_cfg in configs_te:
                    sol, val = tempera(si, vi, matriz, ti_cfg, tf_cfg, fr_cfg)
                    resultados.append(("TE", nome, vi - val))

                df = pd.DataFrame(resultados, columns=["Método", "Observação", "Ganho"])

                st.success("Análise comparativa concluída!")
                st.write("## Tabela Comparativa")
                st.dataframe(df)

            # ───── MÉTODOS NORMAIS ─────
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

    # ── EXIBIÇÃO PERSISTENTE ──

    if st.session_state.matriz is not None:
        st.write("### Matriz")
        st.write(st.session_state.matriz)

    if st.session_state.si is not None and st.session_state.vi is not None:
        st.write("### Solução Inicial")
        st.write(st.session_state.si)

        st.write("### Custo Inicial")
        st.write(st.session_state.vi)

    if st.session_state.resultado is not None:
        sol, val = st.session_state.resultado

        st.write("### Solução Final")
        st.write(sol)

        st.write("### Custo Final")
        st.write(val)

        if st.session_state.vi is not None:
            ganho = st.session_state.vi - val
            st.write(f"### Ganho: {ganho}")