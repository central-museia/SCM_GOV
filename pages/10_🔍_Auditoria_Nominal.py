import streamlit as st
import ast
from pathlib import Path


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Auditoria Nominal SCM_GOV",
    layout="wide"
)


st.title("🔍 Auditoria Nominal SCM_GOV")

st.write(
    """
    Mapeamento automático da arquitetura.
    
    Extrai:
    - Serviços
    - Classes
    - Funções
    - Métodos
    - Parâmetros
    - Dependências
    """
)


# ==========================================================
# PASTAS AUDITADAS
# ==========================================================

pastas_para_auditar = [
    "services",
    "api",
    "models",
    "database"
]


# ==========================================================
# ANALISADOR AST
# ==========================================================

def analisar_arquivo(caminho):

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        codigo = arquivo.read()


    arvore = ast.parse(codigo)


    resultado = {

        "arquivo": caminho.name,

        "classes": [],

        "funcoes": [],

        "imports": []

    }


    for node in ast.walk(arvore):


        # -------------------------
        # IMPORTS
        # -------------------------

        if isinstance(node, ast.Import):

            for item in node.names:
                resultado["imports"].append(
                    item.name
                )


        elif isinstance(node, ast.ImportFrom):

            modulo = node.module or ""

            resultado["imports"].append(
                modulo
            )



        # -------------------------
        # CLASSES
        # -------------------------

        elif isinstance(node, ast.ClassDef):

            classe = {

                "nome": node.name,

                "linha": node.lineno,

                "metodos": []

            }


            for metodo in node.body:

                if isinstance(
                    metodo,
                    ast.FunctionDef
                ):

                    classe["metodos"].append({

                        "nome": metodo.name,

                        "linha": metodo.lineno,

                        "parametros": [

                            arg.arg

                            for arg in metodo.args.args

                        ]

                    })


            resultado["classes"].append(
                classe
            )



        # -------------------------
        # FUNÇÕES
        # -------------------------

        elif isinstance(
            node,
            ast.FunctionDef
        ):


            resultado["funcoes"].append({

                "nome": node.name,

                "linha": node.lineno,

                "parametros": [

                    arg.arg

                    for arg in node.args.args

                ]

            })


    return resultado



# ==========================================================
# EXECUÇÃO
# ==========================================================


for pasta in pastas_para_auditar:


    st.divider()

    st.header(
        f"📁 {pasta.upper()}"
    )


    diretorio = Path(pasta)


    if not diretorio.exists():

        st.warning(
            f"Pasta {pasta} não encontrada"
        )

        continue



    arquivos = list(
        diretorio.rglob("*.py")
    )



    for arquivo in arquivos:


        if arquivo.name == "__init__.py":
            continue


        dados = analisar_arquivo(
            arquivo
        )


        with st.expander(
            f"📄 {arquivo}"
        ):



            # --------------------------------
            # FUNÇÕES
            # --------------------------------

            st.subheader(
                "⚙️ Funções"
            )


            if dados["funcoes"]:

                for funcao in dados["funcoes"]:

                    st.code(

                        f"""
{funcao['nome']}(
    {', '.join(funcao['parametros'])}
)

Linha: {funcao['linha']}
                        """

                    )

            else:

                st.info(
                    "Nenhuma função encontrada"
                )



            # --------------------------------
            # CLASSES
            # --------------------------------

            st.subheader(
                "🏗 Classes"
            )


            for classe in dados["classes"]:


                st.success(
                    f"{classe['nome']} "
                    f"(linha {classe['linha']})"
                )


                for metodo in classe["metodos"]:

                    st.code(

                        f"""
{classe['nome']}.{metodo['nome']}(
    {', '.join(metodo['parametros'])}
)

Linha: {metodo['linha']}
                        """

                    )



            # --------------------------------
            # IMPORTS
            # --------------------------------

            st.subheader(
                "🔗 Dependências"
            )


            if dados["imports"]:

                for imp in dados["imports"]:

                    st.write(
                        f"• {imp}"
                    )

            else:

                st.info(
                    "Sem imports"
                )


st.divider()


st.success(
    """
Auditoria concluída.

O relatório acima representa o mapa nominal atual do código SCM_GOV.
"""
)
