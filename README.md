# Global Solution

Este projeto tem como objetivo fornecer uma solução para o **gerenciamento e otimização do consumo energético** em residências, utilizando **Streamlit** para visualização, **MQTT** para comunicação, **SQLite** como banco de dados para armazenar os dados gerados e **R** para análise estatística. A aplicação monitora, em tempo real, o consumo de energia, as tarifas de energia, e gera relatórios de eficiência energética. O sistema também analisa padrões e propõe soluções sustentáveis com base em dados exploratórios.

## Demonstração no YouTube - CTWP, CDS, SCR

[![Assista no YouTube](https://img.youtube.com/vi/EPctkxhwnlY/0.jpg)](https://youtu.be/EPctkxhwnlY)

## Demonstração no YouTube - AICSS

[![Assista no YouTube](https://img.youtube.com/vi/S_Mf1gLilYA/0.jpg)](https://youtu.be/S_Mf1gLilYA)

---

## Funcionalidades

- **Métricas em tempo real**: Exibe o consumo atual de energia, a tarifa de energia e o custo total em tempo real.
- **Relatórios de Eficiência**: Exibe o custo total por zona e dispositivo, além de gráficos interativos de consumo por zona e dispositivo.
- **Filtros interativos**: Permite selecionar zonas, dispositivos e períodos específicos para visualizar os dados.
- **Simulação de eventos**: O arquivo `mqtt.py` simula uma conexão entre um microcontrolador e a aplicação Python, enviando eventos dos dispositivos registrados, como leituras de sensores e consumo de energia.
- **Análise histórica do consumo de energia elétrica no Brasil**: A aplicação inclui gráficos e relatórios baseados em dados históricos de consumo, utilizando fontes confiáveis, como a **Base dos Dados**.
- **Análise Estatística com R**: Exploração de dados de projetos de eficiência energética disponibilizados pela **ANEEL**, utilizando estatísticas descritivas, gráficos e clusterização para identificar padrões e propor soluções sustentáveis.
- **Otimização de Iluminação com AICSS**: Integração com um circuito simulado no Wokwi usando **ESP32**, sensores LDR e ultrassônico para controlar iluminação interna e externa.

---

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```bash
aicss/
├── diagram.json                                    # Diagrama do circuito no Wokwi
├── libraries.txt                                   # Bibliotecas utilizadas no projeto
└── sketch.ino                                      # Código-fonte do ESP32

cds/
├── data-source/
│   └── br_mme_consumo_energia_eletrica.csv         # Dados históricos do consumo de energia no Brasil
├── database/
│   ├── init.sql                                    # Script SQL para inicializar o banco de dados
│   └── data.db                                     # Banco de dados SQLite (gerado automaticamente)
├── database.py                                     # Funções para interação com o banco de dados
└── main.py                                         # Análise histórica e relatórios do consumo de energia no Brasil

ctwp/
├── database/
│   ├── init.sql                                    # Script SQL para inicializar o banco de dados
│   └── data.db                                     # Banco de dados SQLite (gerado automaticamente)
│   ├── data-model.png                              # Imagem da modelagem do banco de dados
│   └── data-model.xml                              # XML do SQL Designer (pode ser importado em https://sql.toad.cz/)
├── database.py                                     # Funções para interação com o banco de dados
├── main.py                                         # Aplicação principal do Streamlit para eficiência energética
└── mqtt.py                                         # Simulação de comunicação via MQTT

scr/
├── outputs/                                        # Gráficos gerados pelo script R
├── projetos-eficiencia-energetica-empresa.csv      # Dados de empresas
├── projetos-eficiencia-energetica-equipamento.csv  # Dados de equipamentos
├── projetos-eficiencia-energetica-uso-final.csv    # Dados de uso final
├── analysis.html                                   # Análise em HTML gerada pelo Jupyter Notebook
├── analysis.ipynb                                  # Jupyter Notebook com a análise exploratória
├── analysis.r                                      # Script R para análise exploratória
└── main.py                                         # Aplicação principal do Streamlit para exibir gráficos e executar o script R

renv/                                               # Diretório do ambiente isolado R (gerenciado pelo renv)
.Rprofile                                           # Configurações para inicialização do ambiente R
renv.lock                                           # Arquivo de bloqueio do renv para reproduzir o ambiente R
dashboard.py                                        # Dashboard unificado para CTWP, CDS e SCR
requirements.txt                                    # Dependências do projeto
```

---

## Tecnologias Utilizadas

- **Streamlit**: Para criar a interface de usuário interativa.
- **Paho MQTT**: Para simulação de comunicação entre a aplicação e dispositivos.
- **SQLite**: Para armazenamento dos dados do consumo energético e eventos dos dispositivos.
- **Plotly**: Para criação de gráficos interativos.
- **R**: Para análise estatística dos dados de eficiência energética.
- **Python 3.x**: Linguagem de programação utilizada para implementar toda a lógica do sistema.
- **Wokwi**: Simulador para desenvolvimento do circuito **AICSS**.

---

## Requisitos

Certifique-se de ter as ferramentas necessárias instaladas:

- **Python 3.x**
- **R** (com o mirror <https://cran-r.c3sl.ufpr.br/> configurado)
- Dependências do projeto Python:
  ```bash
  pip install -r requirements.txt
  ```

---

## Instruções para Execução

### Configuração do Banco de Dados

Os bancos de dados SQLite para **CDS** e **CTWP** são inicializados automaticamente ao executar os respectivos módulos (`cds/main.py` ou `ctwp/main.py`). O arquivo `init.sql` contém os comandos necessários para criar as tabelas e dados iniciais.

---

### Executando o MQTT

O arquivo **`mqtt.py`** simula a comunicação entre a aplicação Python (CTWP) e o microcontrolador (AICSS). Ele publica eventos no **MQTT Broker** (usando o broker público `test.mosquitto.org`).

**Para executar:**

```bash
python ctwp/mqtt.py
```

Os eventos simulados incluem:

```json
{
  "device_id": 1,
  "type": "sensor-reading",
  "timestamp": "2024-11-20T10:30:00Z",
  "value": "345.78",
  "numeric_value": 345.78
}
```

---

### Executando o Dashboard

Para iniciar o dashboard unificado, execute:

```bash
streamlit run dashboard.py
```

O dashboard oferece:

- **CTWP**: Interface para gerenciamento e otimização de consumo energético em residências.
- **CDS**: Análise histórica do consumo de energia elétrica no Brasil.
- **SCR**: Análise estatística e exploração de dados de eficiência energética fornecidos pela ANEEL.

---

### Executando a Simulação no Wokwi (AICSS)

O circuito foi desenvolvido no simulador Wokwi e pode ser acessado diretamente no link:

[Simulação no Wokwi](https://wokwi.com/projects/414702202497227777)

**Para rodar a simulação:**

1. Acesse o link do Wokwi.
2. Clique em "Start Simulation" para iniciar.
3. O ESP32 enviará eventos simulados para o broker MQTT, que serão consumidos pelo script Python `ctwp/mqtt.py`.

Os arquivos do circuito estão no diretório `aicss/`.

---

### Executando a Análise Estatística com R

Após iniciar o dashboard principal, navegue até a aba **SCR** e clique no botão **"Executar Script R"**.

Os gráficos gerados serão exibidos diretamente na aba, utilizando dados de eficiência energética fornecidos pela ANEEL para identificar padrões e propor soluções sustentáveis.

---

### Fluxo de Dados

1. **AICSS**: O ESP32 simula a detecção de presença e luminosidade, ajustando as luzes e printando eventos.
2. **MQTT**: O script `mqtt.py` simula a comunicação entre o AICSS e o CTWP, recebe os eventos e os armazena no banco de dados.
3. **Banco de Dados**: Os eventos são salvos no SQLite para análise.
4. **Interface**: O Streamlit exibe as métricas, gráficos e relatórios com base nos dados coletados.
5. **R**: Executa análises estatísticas detalhadas para identificar padrões de consumo energético.

---

## Conclusão

Este sistema foi projetado para integrar tecnologias modernas (MQTT, Streamlit, Wokwi e R) em uma solução completa para monitoramento, análise e otimização do consumo energético. Além disso, incorpora simulações de hardware (AICSS) e análises estatísticas detalhadas para identificar padrões e propor ações sustentáveis no setor energético. Ideal para residências, pequenas empresas e estudos acadêmicos.
