import streamlit as st
import random

st.title("🎮 Jogo da Velha (Tic-Tac-Toe)")
st.subheader("Escolha o modo de jogo e divirta-se!")

# -------------------------------
# MENU DE MODO DE JOGO
# -------------------------------
if "modo" not in st.session_state:
    st.session_state.modo = None

modo = st.radio("Selecione o modo de jogo:", ["👫 2 Jogadores", "🤖 Contra a Máquina"])

if modo == "👫 2 Jogadores":
    st.session_state.modo = "2p"
else:
    st.session_state.modo = "cpu"

# -------------------------------
# ESTADO DO JOGO
# -------------------------------
if "tabuleiro" not in st.session_state:
    st.session_state.tabuleiro = [""] * 9
    st.session_state.jogador = "X"
    st.session_state.vencedor = None

# -------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------
def verificar_vencedor():
    t = st.session_state.tabuleiro
    combinacoes = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for c in combinacoes:
        if t[c[0]] == t[c[1]] == t[c[2]] != "":
            return t[c[0]]
    if "" not in t:
        return "Empate"
    return None


def jogar(pos):
    if st.session_state.tabuleiro[pos] == "" and not st.session_state.vencedor:
        st.session_state.tabuleiro[pos] = st.session_state.jogador
        st.session_state.vencedor = verificar_vencedor()
        if not st.session_state.vencedor:
            if st.session_state.modo == "2p":
                st.session_state.jogador = "O" if st.session_state.jogador == "X" else "X"
            elif st.session_state.modo == "cpu":
                st.session_state.jogador = "O"
                jogar_cpu()


def jogar_cpu():
    posicoes_vazias = [i for i, v in enumerate(st.session_state.tabuleiro) if v == ""]
    if not posicoes_vazias:
        return

    # Estratégia simples: tenta ganhar, bloquear, ou jogar aleatório
    for simbolo in ["O", "X"]:
        for i in posicoes_vazias:
            copia = st.session_state.tabuleiro.copy()
            copia[i] = simbolo
            if vencedor_teste(copia) == simbolo:
                st.session_state.tabuleiro[i] = "O"
                st.session_state.vencedor = verificar_vencedor()
                st.session_state.jogador = "X"
                return

    # Caso contrário, jogada aleatória
    pos = random.choice(posicoes_vazias)
    st.session_state.tabuleiro[pos] = "O"
    st.session_state.vencedor = verificar_vencedor()
    st.session_state.jogador = "X"


def vencedor_teste(tabuleiro):
    combinacoes = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for c in combinacoes:
        if tabuleiro[c[0]] == tabuleiro[c[1]] == tabuleiro[c[2]] != "":
            return tabuleiro[c[0]]
    if "" not in tabuleiro:
        return "Empate"
    return None

# -------------------------------
# TABULEIRO (3x3)
# -------------------------------
cols = st.columns(3)
for i in range(9):
    if cols[i % 3].button(st.session_state.tabuleiro[i] or " ", key=i):
        if not st.session_state.vencedor:
            jogar(i)

# -------------------------------
# STATUS E RESULTADO
# -------------------------------
if st.session_state.vencedor:
    if st.session_state.vencedor == "Empate":
        st.warning("🤝 Empate!")
    elif st.session_state.vencedor == "X":
        st.success("🏆 Jogador X venceu!")
    else:
        st.error("💀 Jogador O venceu!" if st.session_state.modo == "2p" else "💻 A máquina venceu!")
else:
    if st.session_state.modo == "2p":
        st.info(f"👉 Vez de {st.session_state.jogador}")
    else:
        st.info("👉 Sua vez!" if st.session_state.jogador == "X" else "🤖 Pensando...")

# -------------------------------
# BOTÃO DE REINICIAR
# -------------------------------
if st.button("🔄 Reiniciar Jogo"):
    st.session_state.tabuleiro = [""] * 9
    st.session_state.jogador = "X"
    st.session_state.vencedor = None
