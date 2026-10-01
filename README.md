# 🇧🇷 Eleições Brasil - API de Monitoramento em Tempo Real

API desenvolvida em **FastAPI** para o acompanhamento das eleições, estruturada com um sistema visual de **"velas" dinâmicas** e transição inteligente entre dados de pesquisas pré-eleição e a apuração oficial do TSE.

---

## 🚀 Principais Funcionalidades

* **Lógica Híbrida de Dados:** 
  * *Pré-eleição / Hoje:* Puxa dados consolidados de intenção de voto (pesquisas).
  * *Domingo (a partir das 17h):* Transiciona automaticamente para os dados oficiais de votação em tempo real direto das urnas do TSE.
* **Sistema Visual de "Velas" por Cores:**
  * 🟢 **Verde Esmeralda:** 1º Lugar (Líder da apuração/pesquisa).
  * 🟡 **Amarelo Ouro:** 2º Lugar (Principal oponente).
  * ⚪ **Cinza Tecnológico:** Demais posições.
  * 🟢 **Verde Neon Brilhante:** Candidato vencedor com o selo oficial de **ELEITO** (incluindo foto, partido, nome e contagem de votos).
* **Congelamento Automático:** Assim que a apuração atinge 100% e o vencedor é declarado pelo TSE, a API trava e cessa as buscas de novos dados, congelando o resultado final.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI** (Framework web de alta performance)
* **Uvicorn** (Servidor ASGI)
* **Requests** (Integração de requisições HTTP)

---

## 📦 Estrutura do Projeto

O projeto é composto por 4 arquivos principais:
1. `main.py` — Configuração central do FastAPI, rotas e controle de estado do sistema.
2. `services.py` — Inteligência de busca, manipulação das fontes de dados (TSE / Pesquisas) e regras das velas.
3. `config.py` — Constantes globais, endpoints oficiais e paleta de cores.
4. `requirements.txt` — Lista de dependências do Python.

---

## ⚙️ Como Executar o Projeto Localmente

1. Clone o repositório ou baixe os arquivos para sua máquina:
   ```bash
   git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
   cd SEU-REPOSITORIO
