# Global Solution

Este projeto tem como objetivo fornecer uma solução para o **gerenciamento e otimização do consumo energético** em residências, utilizando **Streamlit** para visualização, **MQTT** para comunicação e **SQLite** como banco de dados para armazenar os dados gerados. A aplicação monitora, em tempo real, o consumo de energia, as tarifas de energia, e gera relatórios de eficiência energética. O sistema permite a análise do consumo por zona e dispositivo, além de possibilitar a visualização de gráficos detalhados.

## Funcionalidades

- **Métricas em tempo real**: Exibe o consumo atual de energia, a tarifa de energia e o custo total em tempo real.
- **Relatórios de Eficiência**: Exibe o custo total por zona e dispositivo, além de gráficos interativos de consumo por zona e dispositivo.
- **Filtros interativos**: Permite selecionar zonas, dispositivos e períodos específicos para visualizar os dados.
- **Exportação de dados**: Exportação de tabelas e gráficos para análise externa.
- **Gráficos de Consumo**: Exibe gráficos de consumo total por zona e dispositivo, além de possibilitar a visualização do consumo por períodos específicos (diário, semanal, mensal).
- **Simulação de eventos**: O arquivo `mqtt.py` simula uma conexão entre um microcontrolador e a aplicação Python, enviando eventos dos dispositivos registrados, como leituras de sensores e consumo de energia.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```bash
app/
├── main.py              # Código principal do Streamlit
├── mqtt.py              # Código de publicação e assinatura MQTT
├── database.py          # Funções para interação com o banco de dados
├── requirements.txt     # Dependências do projeto

database/
├── data.db              # Banco de dados SQLite
├── init.sql             # Script SQL para criação do banco de dados
├── data-model.png       # Imagem da modelagem do banco de dados
├── data-model.xml       # XML do SQL Designer
```

## Tecnologias Utilizadas

- **Streamlit**: Para criar a interface de usuário interativa.
- **Paho MQTT**: Para simulação de comunicação entre a aplicação e dispositivos.
- **SQLite**: Para armazenamento dos dados do consumo energético e eventos dos dispositivos.
- **Plotly**: Para criação de gráficos interativos.
- **Python 3.x**: Linguagem de programação utilizada para implementar toda a lógica do sistema.

## Requisitos

Para rodar este projeto, é necessário ter o Python 3.x instalado. Além disso, as dependências podem ser instaladas com o seguinte comando:

```bash
pip install -r app/requirements.txt
```

## Instruções para Execução

### 1. Configuração do Banco de Dados

- O arquivo `init.sql` contém os comandos necessários para criar o banco de dados SQLite e suas tabelas, além de inserir dados fictícios para testes.
- O banco de dados é automaticamente inicializado quando o aplicativo é executado pela primeira vez, garantindo que as tabelas e dados estejam prontos para uso.

### 2. Executando o MQTT

O arquivo **`mqtt.py`** simula a comunicação entre dispositivos (como microcontroladores) e a aplicação Python. Ele publica eventos no **MQTT Broker** (usando o broker `test.mosquitto.org` para este exemplo). O código envia eventos a cada 10 segundos, que incluem **estado de dispositivos**, **leituras de sensores** e **consumo de energia**.

**Passo para executar o MQTT:**

1. Primeiro, execute o arquivo `mqtt.py` para começar a simulação de eventos dos dispositivos:

    ```bash
    python app/mqtt.py
    ```

    Esse script começará a enviar eventos do microcontrolador para o broker MQTT, que serão recebidos pela aplicação.

2. O formato dos eventos gerados segue o modelo:

    ```json
    {
      "device_id": 3,
      "type": "sensor-reading",
      "timestamp": "2024-11-15T00:00:00Z",
      "value": "502.78",
      "numeric_value": 502.78
    }
    ```

    Esses eventos são recebidos pela aplicação e salvos no banco de dados para posterior análise.

### 3. Executando o Streamlit

Para iniciar a aplicação Streamlit, execute o seguinte comando:

```bash
streamlit run app/main.py
```

Isso abrirá uma interface web local onde você poderá visualizar as métricas em tempo real, relatórios de eficiência e gráficos interativos. O Streamlit também permite que você interaja com os filtros e exporte dados.

### 4. Fluxo de Dados

1. O **microcontrolador** (simulado pelo `mqtt.py`) envia eventos de sensores ou dispositivos para o **MQTT broker**.
2. A **aplicação Python** (utilizando o `mqtt.py`) escuta os eventos e os salva no banco de dados SQLite.
3. O **Streamlit** exibe em tempo real os dados coletados, gráficos de consumo, relatórios de eficiência e oferece a opção de exportar os dados.

---

## Conclusão

Este sistema automatizado foi projetado para otimizar o consumo de energia em residências, permitindo monitoramento em tempo real, análise de dados históricos e geração de relatórios de eficiência energética. A integração com **MQTT** simula a comunicação com microcontroladores e sensores, tornando o sistema adaptável para ambientes reais.

Se precisar de mais ajustes ou informações, estou à disposição para ajudar!
