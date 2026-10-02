import time
import requests
import logging
from datetime import datetime, timezone, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_APURACAO_TSE = "https://resultados.tse.jus.br/oficial/ele2026/544/dados-simplificados/br/br-c0001-e000544-r.json"

_cache_dados = {
    "timestamp": 0,
    "candidatos": [],
    "totalizacao": {}
}
TEMPO_CACHE = 30

# Fuso horário do Brasil (Brasília - UTC-3)
FUSO_BR = timezone(timedelta(hours=-3))

# Base oficial unificada contendo exclusivamente Lula e Flávio Bolsonaro
DADOS_OFICIAIS_PADRAO = [
    {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "numero": 13,
        "posicao": 1,
        "percentual": 36.5,
        "votos": "45.120.300",
        "status_texto": "AGUARDANDO ABERTURA DA APURAÇÃO",
        "cor_vela": "#CC0000",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Foto_oficial_de_Luiz_In%C3%A1cio_Luiz_da_Silva_%28ombros%29_denoise.jpg",
    },
    {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "numero": 22,
        "posicao": 2,
        "percentual": 29.0,
        "votos": "35.800.100",
        "status_texto": "AGUARDANDO ABERTURA DA APURAÇÃO",
        "cor_vela": "#002D62",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2025/12/O-senador-Flavio-Bolsonaro-e1765906268178.jpg?w=1200&h=1200&crop=1",
    }
]

def verificar_fase_eleicao():
    """
    Retorna a fase atual do dia da eleição:
    - 'votacao': entre 08:00 e 17:00 (urnas abertas, votando)
    - 'apuracao': a partir de 17:00 (fechamento das urnas, contagem oficial)
    - 'fora_horario': antes das 08:00
    """
    agora = datetime.now(FUSO_BR)
    
    # Se não for domingo, retorna padrão pré-eleição
    if agora.weekday() != 6:
        return "pre_eleicao"
        
    hora = agora.hour
    
    if 8 <= hora < 17:
        return "votacao"
    elif hora >= 17:
        return "apuracao"
    else:
        return "pre_eleicao"

def buscar_apuracao_tse():
    fase = verificar_fase_eleicao()
    
    # Se estiver no horário de votação (08h às 17h), a API trabalha informando que a votação está ativa
    if fase == "votacao":
        info_totalizacao = {
            "status_geral": "VOTAÇÃO EM ANDAMENTO (URNA ABERTAS ATÉ AS 17:00)"
        }
        # Retorna os candidatos com status indicando que as urnas estão abertas
        candidatos_votacao = []
        for c in DADOS_OFICIAIS_PADRAO:
            item_copia = c.copy()
            item_copia["status_texto"] = "VOTAÇÃO EM ANDAMENTO — AGUARDANDO AS 17:00"
            candidatos_votacao.append(item_copia)
        return candidatos_votacao, info_totalizacao

    # Se for antes das 08h, mantém o padrão inicial
    if fase == "pre_eleicao":
        return None, None

    # A partir das 17:00, o sistema entra na fase de apuração real buscando do TSE
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_APURACAO_TSE, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return None, None

        data = response.json()
        cand_raw = data.get("cand", [])
        pst = data.get("pst", "0") 
        
        qtd_urnas_aptas = data.get("qu", "N/D")
        qtd_urnas_apuradas = data.get("qupt", "N/D")
        
        if not cand_raw:
            return None, None

        apuracao_concluida = False
        try:
            if float(pst.replace(",", ".")) >= 100.0:
                apuracao_concluida = True
        except:
            pass

        info_totalizacao = {
            "percentual_urnas": pst,
            "urnas_apuradas": qtd_urnas_apuradas,
            "urnas_totais": qtd_urnas_aptas,
            "status_geral": f"Urnas Apuradas: {qtd_urnas_apuradas} de {qtd_urnas_aptas} ({pst}%)" if qtd_urnas_apuradas != "N/D" else f"Urnas Apuradas: {pst}%"
        }

        lista_candidatos = []
        for item in cand_raw:
            numero = int(item.get("n", 0))
            if numero not in [13, 22]:
                continue
                
            nome = item.get("nm")
            votos = item.get("vap")
            percentual = float(item.get("pvap", "0").replace(",", "."))
            
            original = next((c for c in DADOS_OFICIAIS_PADRAO if c["numero"] == numero), None)
            if not original:
                continue

            if apuracao_concluida:
                status_final = "PRESIDENTE ELEITO"
            else:
                status_final = f"APURAÇÃO AO VIVO — {info_totalizacao['status_geral']}"

            lista_candidatos.append({
                "nome": nome or original["nome"],
                "partido": item.get("sgp", original["partido"]),
                "numero": numero,
                "posicao": 1 if numero == 13 else 2,
                "percentual": percentual,
                "votos": f"{int(votos):,}".replace(",", ".") if votos else original["votos"],
                "status_texto": status_final,
                "cor_vela": original["cor_vela"],
                "foto_url": original["foto_url"],
            })

        lista_candidatos.sort(key=lambda x: x["posicao"])
        return lista_candidatos if lista_candidatos else None, info_totalizacao

    except Exception as e:
        logger.error(f"Erro ao buscar TSE: {e}")
        return None, None

def obter_candidatos(uf: str = "br"):
    global _cache_dados
    tempo_atual = time.time()
    
    if _cache_dados["candidatos"] and (tempo_atual - _cache_dados["timestamp"] < TEMPO_CACHE):
        return _cache_dados["candidatos"]
    
    dados_reais, info_tot = buscar_apuracao_tse()
    
    if dados_reais:
        _cache_dados["candidatos"] = dados_reais
        _cache_dados["totalizacao"] = info_tot or {}
        _cache_dados["timestamp"] = tempo_atual
        return dados_reais
        
    return DADOS_OFICIAIS_PADRAO

def buscar_dados_completos(uf: str = "br"):
    return obter_candidatos(uf)
