# services.py

ESTADO_SISTEMA = {
    "eleicao_encerrada": False,
    "percentual_apurado": 0.0
}

def obter_dados_velas(uf: str = None):
    # Lista oficial de candidatos à presidência para 2026
    candidatos = [
        {"posicao": 1, "nome": "Luiz Inácio Lula da Silva", "partido": "PT", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 2, "nome": "Flávio Nantes Bolsonaro", "partido": "PL", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 3, "nome": "Romeu Zema Neto", "partido": "NOVO", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 4, "nome": "Ronaldo Ramos Caiado", "partido": "PSD", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 5, "nome": "Renan Antônio Ferreira dos Santos", "partido": "MISSÃO", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 6, "nome": "Augusto Jorge Cury", "partido": "Avante", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 7, "nome": "Clariana Zacarkim Barão", "partido": "DC", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 8, "nome": "Edmilson Silva Costa", "partido": "PCB", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 9, "nome": "Hertz Da Conceição Dias", "partido": "PSTU", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 10, "nome": "Leonardo Alves De Araujo", "partido": "PRTB", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 11, "nome": "Rui Costa Pimenta", "partido": "PCO", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 12, "nome": "Samara Martins Da Silva Feitosa", "partido": "UP", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"},
        {"posicao": 13, "nome": "Wilson Grassi Júnior", "partido": "DEMOCRATA", "votos_ou_media": "0.0%", "eleito": False, "foto_url": "https://via.placeholder.com/150"}
    ]

    return {
        "status_servico": "Oficializadas",
        "eleicao_encerrada": ESTADO_SISTEMA["eleicao_encerrada"],
        "percentual_apurado": ESTADO_SISTEMA["percentual_apurado"],
        "candidatos": candidatos
    }
