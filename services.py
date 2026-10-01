"""
Módulo de serviços para a API de Eleições 2026.
Contém a base completa consolidada: candidatos, fotos, números de urna, percentuais e posições.
"""

from typing import Dict, List

# Dicionário central contendo os 13 candidatos presidenciais de 2026, com dados completos
CANDIDATOS_DATABASE: Dict[str, dict] = {
    "lula": {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "numero": 13,
        "posicao": 1,
        "percentual": 36.5,
        "votos": "45.120.300",
        "status_texto": "LIDERANDO PESQUISAS",
        "cor_vela": "#CC0000",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/280002513904.jpg?w=161&h=225&crop=0&quality=100",
    },
    "flavio_bolsonaro": {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "numero": 22,
        "posicao": 2,
        "percentual": 29.0,
        "votos": "35.800.100",
        "status_texto": "NA DISPUTA",
        "cor_vela": "#002D62",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Fl%C3%A1vio_Bolsonaro_em_2023_%28cropped%29.jpg",
    },
    "pablo_marcal": {
        "nome": "Pablo Marçal",
        "partido": "PRTB",
        "numero": 28,
        "posicao": 3,
        "percentual": 12.4,
        "votos": "15.300.400",
        "status_texto": "EM CRESCIMENTO",
        "cor_vela": "#008000",
        "foto_url": "https://img.estadao.com.br/fotos/politica/eleicoes-2026/BR/FBR280002553884_div.jpg",
    },
    "romeu_zema": {
        "nome": "Romeu Zema",
        "partido": "NOVO",
        "numero": 30,
        "posicao": 5,
        "percentual": 5.2,
        "votos": "6.420.100",
        "status_texto": "ESTÁVEL",
        "cor_vela": "#FF6600",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/300002534571.jpg?w=161&h=225&crop=0&quality=100",
    },
    "ronaldo_caiado": {
        "nome": "Ronaldo Caiado",
        "partido": "PSD",
        "numero": 44,
        "posicao": 6,
        "percentual": 3.9,
        "votos": "4.810.000",
        "status_texto": "ESTÁVEL",
        "cor_vela": "#0055A5",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/280002540694.jpg?w=161&h=225&crop=0&quality=100",
    },
    "eduardo_leite": {
        "nome": "Eduardo Leite",
        "partido": "PSDB",
        "numero": 45,
        "posicao": 7,
        "percentual": 2.5,
        "votos": "3.080.000",
        "status_texto": "NA DISPUTA",
        "cor_vela": "#0066CC",
        "foto_url": "https://psd.org.br/wp-content/uploads/2026/03/Eduardo-Leite-Foto-Governo-do-Rio-Grande-do-Sul.jpg",
    },
    "renan_santos": {
        "nome": "Renan Santos",
        "partido": "MISSÃO",
        "numero": 35,
        "posicao": 4,
        "percentual": 6.1,
        "votos": "7.530.000",
        "status_texto": "EM ASCENSÃO",
        "cor_vela": "#333333",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/280002540694.jpg?w=161&h=225&crop=0&quality=100",
    },
    "augusto_cury": {
        "nome": "Augusto Cury",
        "partido": "Avante",
        "numero": 70,
        "posicao": 8,
        "percentual": 1.5,
        "votos": "1.850.000",
        "status_texto": "NA DISPUTA",
        "cor_vela": "#FFCC00",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/280002551547.jpg?w=161&h=225&crop=0&quality=100",
    },
    "ciro_gomes": {
        "nome": "Ciro Gomes",
        "partido": "PDT",
        "numero": 12,
        "posicao": 9,
        "percentual": 1.2,
        "votos": "1.480.000",
        "status_texto": "NA DISPUTA",
        "cor_vela": "#FF0000",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/2026_CIRO_GOMES_CANDIDATO_GOVERNADOR_CE_TSE_%2860002531351%29.JPG",
    },
    "hertz_dias": {
        "nome": "Hertz Dias",
        "partido": "PSTU",
        "numero": 16,
        "posicao": 10,
        "percentual": 0.4,
        "votos": "490.000",
        "status_texto": "REGISTRADO",
        "cor_vela": "#990000",
        "foto_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQu9V3OUCaOZoaauf6MgTsGZZHPVnKPlJRvBK0P-_em759agSVfVzBFUZQ&s=10",
    },
    "eymael": {
        "nome": "José Maria Eymael",
        "partido": "DC",
        "numero": 27,
        "posicao": 11,
        "percentual": 0.3,
        "votos": "370.000",
        "status_texto": "REGISTRADO",
        "cor_vela": "#003366",
        "foto_url": "https://www.rbsdirect.com.br/filestore/4/9/1/8/1/0/4_8dd86c1fc60570e/4018194_50cd02134c8559d.jpg",
    },
    "vera_lucia": {
        "nome": "Vera Lúcia",
        "partido": "PSTU",
        "numero": 16,
        "posicao": 12,
        "percentual": 0.2,
        "votos": "240.000",
        "status_texto": "REGISTRADO",
        "cor_vela": "#8B0000",
        "foto_url": "https://nexo-uploads-beta.s3.amazonaws.com/wp-content/uploads/2023/11/29115221/WhatsApp-Image-2020-09-02-at-00.09.03-1_binary_298753.jpeg",
    },
    "padre_kelmon": {
        "nome": "Padre Kelmon",
        "partido": "PRD",
        "numero": 14,
        "posicao": 13,
        "percentual": 0.1,
        "votos": "120.000",
        "status_texto": "REGISTRADO",
        "cor_vela": "#4B0082",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/250002535998.jpg?w=161&h=225&crop=0&quality=100",
    }
}

def listar_candidatos() -> List[dict]:
    """Retorna a lista completa com todos os candidatos e seus dados detalhados."""
    return [{"id": key, **value} for key, value in CANDIDATOS_DATABASE.items()]

def buscar_dados_completos(uf: str = "br") -> dict:
    """
    Função principal chamada pelo main.py para retornar os dados consolidados da eleição.
    """
    return {
        "uf": uf.upper(),
        "eleicao_encerrada": False,
        "candidatos": listar_candidatos()
    }
