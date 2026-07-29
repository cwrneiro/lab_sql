#!/usr/bin/env python3
"""
Gerador de dataset sintético de operadora de saúde para o treinamento
Databricks Básico — Curadores de Dados (Unimed Campinas).

Substitui o dataset original de varejo/farmácia/finanças por dados de uma
operadora de plano de saúde, preservando a ESTRUTURA que os labs usam para
ensinar (ex.: chave de join "errada" vs. "certa" em dim_prestador, jargão de
categoria para a lição de instruções da Genie).

- SEM PII: nomes de beneficiários e prestadores são sintéticos ("BENEFICIARIO 00001").
- Reprodutível: seed fixa.
- Saída: 5 CSVs em dados/ (mesma pasta deste script).

Uso:  python3 dados/gerar_dados_saude.py
"""

import csv
import os
import random
from datetime import date, timedelta

SEED = 42
random.seed(SEED)

OUT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ #
# Parâmetros de volume (dimensionados para um workshop: carga rápida) #
# ------------------------------------------------------------------ #
N_BENEFICIARIOS = 2_000
N_PRESTADORES = 300
N_PROCEDIMENTOS = 400
N_SINISTROS = 40_000
N_GUIAS = 10_000

DT_INI = date(2025, 1, 1)
DT_FIM = date(2025, 12, 31)
DIAS = (DT_FIM - DT_INI).days


def data_aleatoria():
    return DT_INI + timedelta(days=random.randint(0, DIAS))


# ------------------------------------------------------------------ #
# Catálogos de apoio                                                 #
# ------------------------------------------------------------------ #
# categoria_procedimento: usada na lição de "instruções" da Genie.
#   Jargão ensinado: "alta complexidade" = INTERNACAO ou CIRURGIA.
CATEGORIAS = ["CONSULTA", "EXAME", "TERAPIA", "INTERNACAO", "CIRURGIA"]

# faixa de valor (R$) por categoria — consulta barata, internação/cirurgia caras
VALOR_POR_CATEGORIA = {
    "CONSULTA": (80, 350),
    "EXAME": (40, 1_200),
    "TERAPIA": (120, 900),
    "INTERNACAO": (2_500, 45_000),
    "CIRURGIA": (3_000, 80_000),
}

ESPECIALIDADES = [
    "CLINICA MEDICA", "CARDIOLOGIA", "ORTOPEDIA", "PEDIATRIA", "GINECOLOGIA",
    "ONCOLOGIA", "NEUROLOGIA", "OFTALMOLOGIA", "DERMATOLOGIA", "PSIQUIATRIA",
]

# nomes de procedimento por categoria (genéricos, plausíveis, sem marca)
NOMES_PROC = {
    "CONSULTA": [
        "CONSULTA ELETIVA", "CONSULTA DE RETORNO", "CONSULTA DE URGENCIA",
        "CONSULTA PRE-OPERATORIA", "AVALIACAO MULTIDISCIPLINAR",
    ],
    "EXAME": [
        "HEMOGRAMA COMPLETO", "RAIO-X DE TORAX", "RESSONANCIA MAGNETICA",
        "TOMOGRAFIA COMPUTADORIZADA", "ULTRASSONOGRAFIA", "ELETROCARDIOGRAMA",
        "GLICEMIA DE JEJUM", "COLONOSCOPIA", "MAMOGRAFIA", "ECOCARDIOGRAMA",
    ],
    "TERAPIA": [
        "SESSAO DE FISIOTERAPIA", "SESSAO DE QUIMIOTERAPIA",
        "SESSAO DE HEMODIALISE", "SESSAO DE PSICOTERAPIA", "SESSAO DE FONOAUDIOLOGIA",
    ],
    "INTERNACAO": [
        "INTERNACAO CLINICA", "INTERNACAO EM UTI", "INTERNACAO PEDIATRICA",
        "INTERNACAO OBSTETRICA", "INTERNACAO PSIQUIATRICA",
    ],
    "CIRURGIA": [
        "CIRURGIA CARDIACA", "ARTROPLASTIA DE QUADRIL", "APENDICECTOMIA",
        "COLECISTECTOMIA", "CIRURGIA DE CATARATA", "CESARIANA",
    ],
}

PLANOS = ["AMBULATORIAL", "HOSPITALAR", "REFERENCIA", "COMPLETO"]
SEXOS = ["F", "M"]
FAIXAS = ["0-17", "18-29", "30-44", "45-59", "60+"]
MUNICIPIOS = [
    "CAMPINAS", "VALINHOS", "VINHEDO", "PAULINIA", "SUMARE",
    "HORTOLANDIA", "INDAIATUBA", "JAGUARIUNA",
]
TIPOS_PRESTADOR = ["HOSPITAL", "CLINICA", "LABORATORIO", "CONSULTORIO", "PRONTO-SOCORRO"]
REDES = [f"REDE {i}" for i in range(1, 6)]
STATUS_GUIA = ["AUTORIZADA", "NEGADA", "EM_ANALISE"]


def cep():
    return f"{random.randint(13000, 13990):05d}"


def lat_long():
    # bounding box aproximado da região de Campinas
    return f"{random.uniform(-23.1, -22.6):.2f},{random.uniform(-47.3, -46.7):.2f}"


# ------------------------------------------------------------------ #
# 1. dim_procedimento  (espelha dim_medicamento)                     #
# ------------------------------------------------------------------ #
procedimentos = []
pid = 0
for _ in range(N_PROCEDIMENTOS):
    pid += 1
    cat = random.choice(CATEGORIAS)
    nome = random.choice(NOMES_PROC[cat])
    procedimentos.append({
        "id_procedimento": pid,
        "nome_procedimento": nome,
        "categoria_procedimento": cat,
        "codigo_tuss": f"{random.randint(10_000_000, 49_999_999)}",
        "rol_ans": random.choice(["S", "S", "S", "N"]),  # maioria no Rol da ANS
        "porte": random.choice(["1", "2", "3", "4", "ESPECIAL"]),
        "especialidade": random.choice(ESPECIALIDADES),
    })

with open(os.path.join(OUT, "dim_procedimento.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(procedimentos[0].keys()))
    w.writeheader()
    w.writerows(procedimentos)

# ------------------------------------------------------------------ #
# 2. dim_prestador  (espelha dim_loja — LIÇÃO de constraint da Genie) #
#    id_prestador = chave "tentadora, porém ERRADA" para o join       #
#    cod          = chave CORRETA de join com sinistros               #
#    xpto         = nome do prestador (coluna mal nomeada de propósito)#
# ------------------------------------------------------------------ #
prestadores = []
cods_prestador = []
for i in range(1, N_PRESTADORES + 1):
    cod = random.randint(10_000_000_000, 999_999_999_999)
    cods_prestador.append(cod)
    prestadores.append({
        "id_prestador": i,
        "cod": cod,
        "rede": random.choice(REDES),
        "xpto": f"PRESTADOR {i:04d}",
        "tipo": random.choice(TIPOS_PRESTADOR),
        "cep": cep(),
        "lat_long": lat_long(),
    })

with open(os.path.join(OUT, "dim_prestador.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(prestadores[0].keys()))
    w.writeheader()
    w.writerows(prestadores)

# ------------------------------------------------------------------ #
# 3. dim_beneficiario                                                #
# ------------------------------------------------------------------ #
beneficiarios = []
for i in range(1, N_BENEFICIARIOS + 1):
    beneficiarios.append({
        "id_beneficiario": i,
        "nome_beneficiario": f"BENEFICIARIO {i:05d}",  # sintético, sem PII
        "plano": random.choice(PLANOS),
        "sexo": random.choice(SEXOS),
        "faixa_etaria": random.choice(FAIXAS),
        "municipio": random.choice(MUNICIPIOS),
        "dt_adesao": (date(2018, 1, 1) + timedelta(days=random.randint(0, 2900))).isoformat(),
    })

with open(os.path.join(OUT, "dim_beneficiario.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(beneficiarios[0].keys()))
    w.writeheader()
    w.writerows(beneficiarios)

# ------------------------------------------------------------------ #
# 4. sinistros  (fato — espelha vendas)                              #
#    id_prestador referencia dim_prestador.COD (não id_prestador!)    #
# ------------------------------------------------------------------ #
cat_por_proc = {p["id_procedimento"]: p["categoria_procedimento"] for p in procedimentos}

with open(os.path.join(OUT, "sinistros.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_sinistro", "id_beneficiario", "id_prestador", "id_procedimento",
                "dt_atendimento", "qt_procedimento", "vl_sinistro"])
    for _ in range(N_SINISTROS):
        proc = random.randint(1, N_PROCEDIMENTOS)
        cat = cat_por_proc[proc]
        lo, hi = VALOR_POR_CATEGORIA[cat]
        qt = random.randint(1, 3)
        vl = round(random.uniform(lo, hi) * qt, 2)
        w.writerow([
            random.randint(10**17, 10**18),               # id_sinistro
            random.randint(1, N_BENEFICIARIOS),            # id_beneficiario
            random.choice(cods_prestador),                 # id_prestador -> dim_prestador.cod
            proc,                                          # id_procedimento
            data_aleatoria().isoformat(),                  # dt_atendimento
            qt,                                            # qt_procedimento
            vl,                                            # vl_sinistro
        ])

# ------------------------------------------------------------------ #
# 5. guias  (espelha estoque — LIÇÃO de proporção/taxa)              #
#    permite "taxa de autorização" = qt_autorizada / qt_solicitada   #
# ------------------------------------------------------------------ #
with open(os.path.join(OUT, "guias.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_guia", "dt_solicitacao", "id_beneficiario", "id_procedimento",
                "status", "qt_solicitada", "qt_autorizada"])
    for _ in range(N_GUIAS):
        status = random.choices(STATUS_GUIA, weights=[70, 15, 15])[0]
        qt_sol = random.randint(1, 5)
        if status == "AUTORIZADA":
            qt_aut = qt_sol
        elif status == "NEGADA":
            qt_aut = 0
        else:  # EM_ANALISE
            qt_aut = random.randint(0, qt_sol)
        w.writerow([
            random.randint(10**17, 10**18),               # id_guia
            data_aleatoria().isoformat(),                  # dt_solicitacao
            random.randint(1, N_BENEFICIARIOS),            # id_beneficiario
            random.randint(1, N_PROCEDIMENTOS),            # id_procedimento
            status,
            qt_sol,
            qt_aut,
        ])

print("Gerado em", OUT)
for nome in ["dim_procedimento", "dim_prestador", "dim_beneficiario", "sinistros", "guias"]:
    caminho = os.path.join(OUT, nome + ".csv")
    with open(caminho, encoding="utf-8") as f:
        linhas = sum(1 for _ in f) - 1
    print(f"  {nome}.csv: {linhas:,} linhas")
