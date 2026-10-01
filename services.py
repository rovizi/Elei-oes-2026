"""
Módulo de serviços para a API de Eleições 2026.
Contém a base de dados mapeada com os candidatos e seus respectivos links de imagens oficiais.
"""

from typing import Dict, List, Optional

# Dicionário central contendo os 13 candidatos presidenciais de 2026 e seus dados (incluindo URL da foto oficial)
CANDIDATOS_DATABASE: Dict[str, dict] = {
    "lula": {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "foto_url": "https://p2.trrsf.com/image/fget/cf/1200/1200/middle/images.terra.com/2018/10/07/romeuzema-dynelle-coelho-qu4rto-studio.png",
    },
    "flavio_bolsonaro": {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "foto_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7zUdpWUY9mchtfyxn_lDhAmfnD2GSLfRN46PZ2yYm4A&s",
    },
    "romeu_zema": {
        "nome": "Romeu Zema",
        "partido": "NOVO",
        "foto_url": "https://p2.trrsf.com/image/fget/cf/1200/1200/middle/images.terra.com/2018/10/07/romeuzema-dynelle-coelho-qu4rto-studio.png",
    },
    "ronaldo_caiado": {
        "nome": "Ronaldo Caiado",
        "partido": "PSD",
        "foto_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7zUdpWUY9mchtfyxn_lDhAmfnD2GSLfRN46PZ2yYm4A&s",
    },
    "renan_santos": {
        "nome": "Renan Santos",
        "partido": "MISSÃO",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/280002540694.jpg?w=161&h=225&crop=0&quality=100",
    },
    "augusto_cury": {
        "nome": "Augusto Cury",
        "partido": "Avante",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/280002551547.jpg?w=161&h=225&crop=0&quality=100",
    },
    "hertz_dias": {
        "nome": "Hertz Dias",
        "partido": "PSTU",
        "foto_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQu9V3OUCaOZoaauf6MgTsGZZHPVnKPlJRvBK0P-_em759agSVfVzBFUZQ&s=10",
    },
    "pablo_marcal": {
        "nome": "Pablo Marçal",
        "partido": "PRTB",
        "foto_url": "https://img.estadao.com.br/fotos/politica/eleicoes-2026/BR/FBR280002553884_div.jpg",
    },
    "eduardo_leite": {
        "nome": "Eduardo Leite",
        "partido": "PSDB",
        "foto_url": "https://psd.org.br/wp-content/uploads/2026/03/Eduardo-Leite-Foto-Governo-do-Rio-Grande-do-Sul.jpg",
    },
    "ciro_gomes": {
        "nome": "Ciro Gomes",
        "partido": "PDT",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/2026_CIRO_GOMES_CANDIDATO_GOVERNADOR_CE_TSE_%2860002531351%29.JPG",
    },
    "eymael": {
        "nome": "José Maria Eymael",
        "partido": "DC",
        "foto_url": "https://www.rbsdirect.com.br/filestore/4/9/1/8/1/0/4_8dd86c1fc60570e/4018194_50cd02134c8559d.jpg",
    },
    "vera_lucia": {
        "nome": "Vera Lúcia",
        "partido": "PSTU",
        "foto_url": "https://nexo-uploads-beta.s3.amazonaws.com/wp-content/uploads/2023/11/29115221/WhatsApp-Image-2020-09-02-at-00.09.03-1_binary_298753.jpeg",
    },
    "padre_kelmon": {
        "nome": "Padre Kelmon",
        "partido": "PRD",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/candidates/2026/250002535998.jpg?w=161&h=225&crop=0&quality=100",
    }
}

def listar_candidatos() -> List[dict]:
    """Retorna a lista completa com todos os candidatos cadastrados."""
    return [{"id": key, **value} for key, value in CANDIDATOS_DATABASE.items()]

def obter_candidato_por_id(candidato_id: str) -> Optional[dict]:
    """Busca um candidato específico pelo seu identificador único."""
    candidato = CANDIDATOS_DATABASE.get(candidato_id)
    if candidato:
        return {"id": candidato_id, **candidato}
    return None
```eof

Prontinho! Agora o código está no bloco padrão com o fundo escuro e o botão de copiar ativado. É só usar para atualizar o repositório!
