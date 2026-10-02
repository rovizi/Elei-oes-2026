import time
import requests
import logging
from datetime import datetime, timezone, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_APURACAO_TSE = "https://resultados.tse.jus.br/oficial/ele2026/544/dados-simplificados/br/br-c0001-e000544-r.json"

_cache_dados = {
    "timestamp": 0,
    "resposta_completa": {}
}
TEMPO_CACHE = 30

# Fuso horário do Brasil (Brasília - UTC-3)
FUSO_BR = timezone(timedelta(hours=-3))

INFO_ELEICAO = {
    "data_eleicao": "04/10/2026",
    "dia_semana": "Domingo",
    "inicio_votacao": "08:00",
    "fim_votacao": "17:00 (Sujeito a tolerância de filas)",
    "inicio_apuracao": "Imediatamente após o encerramento geral"
}

DADOS_OFICIAIS_PADRAO = [
    {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "numero": 13,
        "posicao": 1,
        "percentual": 0.0,
        "votos": "0",
        "status_texto": "VOTAÇÃO EM ANDAMENTO (AGUARDANDO FECHAMENTO DAS URNAS)",
        "cor_vela": "#CC0000",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Foto_oficial_de_Luiz_In%C3%A1cio_Luiz_da_Silva_%28ombros%29_denoise.jpg",
    },
    {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "numero": 22,
        "posicao": 2,
        "percentual": 0.0,
        "votos": "0",
        "status_texto": "VOTAÇÃO EM ANDAMENTO (AGUARDANDO FECHAMENTO DAS URNAS)",
        "cor_vela": "#002D62",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2025/12/O-senador-Flavio-Bolsonaro-e1765906268178.jpg?w=1200&h=1200&crop=1",
    }
]

def montar_resposta_espera(mensagem_status):
    candidatos = []
    for c in DADOS_OFICIAIS_PADRAO:
        item = c.copy()
        item["status_texto"] = mensagem_status
        candidatos.append(item)
        
    return {
        "eleicao": INFO_ELEICAO,
        "status_conexao": "VOTACAO_EM_ANDAMENTO",
        "totalizacao": {"status_geral": "Votação em curso ou aguardando liberação dos boletins pelo TSE."},
        "candidatos": candidatos
    }

def buscar_dados_completos(uf: str = "br"):
    global _cache_dados
    tempo_atual = time.time()
    
    if _cache_dados["resposta_completa"] and (tempo_atual - _cache_dados["timestamp"] < TEMPO_CACHE):
        return _cache_dados["resposta_completa"]

    agora = datetime.now(FUSO_BR)
    
    # Se nem for domingo, nem tenta o TSE, retorna espera padrão
    eh_domingo = (agora.weekday() == 6) or (agora.year == 2026 and agora.month == 10 and agora.day == 4)
    if not eh_domingo:
        resposta = montar_resposta_espera("AGUARDANDO O DIA DA ELEIÇÃO (DOMINGO 04/10)")
        _cache_dados["resposta_completa"] = resposta
        _cache_dados["timestamp"] = tempo_atual
        return resposta

    # Se for domingo mas ainda estiver antes das 17h, garante votação
    if agora.hour < 17:
        resposta = montar_resposta_espera("VOTAÇÃO EM ANDAMENTO — URNAS ABERTAS")
        _cache_dados["resposta_completa"] = resposta
        _cache_dados["timestamp"] = tempo_atual
        return resposta

    # A partir das 17:00, consultamos o TSE para ver se os dados de apuração já foram liberados
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_APURACAO_TSE, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return montar_resposta_espera("AGUARDANDO ENCERRAMENTO DE FILAS / LIBERAÇÃO DO TSE...")

        data = response.json()
        cand_raw = data.get("cand", [])
        pst = data.get("pst", "0") 
        
        # SEGURANÇA CONTRA ATRASOS: Se o TSE ainda não retornou candidatos com votos (indicando que a apuração não começou por atraso nas seções)
        tem_votos_computados = False
        if cand_raw:
            for item in cand_raw:
                if int(item.get("vap", 0)) > 0:
                    tem_votos_computados = True
                    break

        # Se passou das 17h mas o TSE ainda não computou votos (por causa de filas/atraso), a API continua informando que aguarda o encerramento
        if not tem_votos_computados:
            resposta = montar_resposta_espera("VOTAÇÃO ESTENDIDA / AGUARDANDO PRIMEIROS VOTOS DO TSE")
            _cache_dados["resposta_completa"] = resposta
            _cache_dados["timestamp"] = tempo_atual
            return resposta

        # Se chegou aqui, a apuração de fato começou! Processa os dados reais
        qtd_urnas_aptas = data.get("qu", "N/D")
        qtd_urnas_apuradas = data.get("qupt", "N/D")
        
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
                "votos": f"{int(votos):,}".replace(",", ".") if votos else "0",
                "status_texto": status_final,
                "cor_vela": original["cor_vela"],
                "foto_url": original["foto_url"],
            })

        lista_candidatos.sort(key=lambda x: x["posicao"])
        
        resposta = {
            "eleicao": INFO_ELEICAO,
            "status_conexao": "AO_VIVO_TSE",
            "totalizacao": info_totalizacao,
            "candidatos": lista_candidatos
        }
        
        _cache_dados["resposta_completa"] = resposta
        _cache_dados["timestamp"] = tempo_atual
        return resposta

    except Exception as e:
        logger.error(f"Erro ao buscar TSE: {e}")
        return montar_resposta_espera("AGUARDANDO LIBERAÇÃO OFICIAL DO TSE...")

def obter_candidatos(uf: str = "br"):
    res = buscar_dados_completos(uf)
    if isinstance(res, dict) and "candidatos" in res:
        return res["candidatos"]
    return DADOS_OFICIAIS_PADRAO
