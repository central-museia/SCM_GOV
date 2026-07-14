"""
Endpoints oficiais da API do Portal Nacional de Contratações Públicas (PNCP)
"""

BASE_URL = "https://pncp.gov.br/api/consulta"

# ===========================
# CONTRATAÇÕES
# ===========================

CONTRATACOES_PUBLICACAO = "/v1/contratacoes/publicacao"

CONTRATACOES_PROPOSTA = "/v1/contratacoes/proposta"

CONTRATACOES_ATUALIZACAO = "/v1/contratacoes/atualizacao"

CONTRATACAO = "/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}"

# ===========================
# ATAS
# ===========================

ATAS = "/v1/atas"

ATAS_ATUALIZACAO = "/v1/atas/atualizacao"

# ===========================
# CONTRATOS
# ===========================

CONTRATOS = "/v1/contratos"

CONTRATOS_ATUALIZACAO = "/v1/contratos/atualizacao"

# ===========================
# PCA
# ===========================

PCA = "/v1/pca"

PCA_USUARIO = "/v1/pca/usuario"

PCA_ATUALIZACAO = "/v1/pca/atualizacao"

# ===========================
# INSTRUMENTOS DE COBRANÇA
# ===========================

INSTRUMENTOS_COBRANCA = "/v1/instrumentoscobranca/inclusao"
