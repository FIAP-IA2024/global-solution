# Ativar o ambiente renv, se disponível
if (file.exists("renv/activate.R")) {
  source("renv/activate.R")
}

# Configurar mirror rápido e confiável
options(repos = c(CRAN = "https://cran-r.c3sl.ufpr.br/"))

# Configurar instalação paralela (usa múltiplos núcleos do processador)
options(Ncpus = parallel::detectCores() - 1)

# Criar pasta "outputs" se não existir
if (!dir.exists("scr/outputs")) {
  dir.create("scr/outputs")
}

# Carregar pacotes necessários
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("dplyr")) install.packages("dplyr")
if (!require("tidyr")) install.packages("tidyr")
if (!require("readr")) install.packages("readr")
if (!require("corrplot")) install.packages("corrplot")
if (!require("plotly")) install.packages("plotly")

# Carregar pacotes
library(ggplot2)
library(dplyr)
library(tidyr)
library(readr)
library(corrplot)
library(plotly)

# Importação e Limpeza dos Dados
# Importar arquivos CSV
empresa_data <- read.csv("scr/projetos-eficiencia-energetica-empresa.csv", sep = ";", encoding = "latin1", stringsAsFactors = FALSE)
equipamento_data <- read.csv("scr/projetos-eficiencia-energetica-equipamento.csv", sep = ";", encoding = "latin1", stringsAsFactors = FALSE)
uso_final_data <- read.csv("scr/projetos-eficiencia-energetica-uso-final.csv", sep = ";", encoding = "latin1", stringsAsFactors = FALSE)

# Converter valores financeiros de string para numérico
empresa_data$VlrCustoTotal <- as.numeric(gsub(",", ".", empresa_data$VlrCustoTotal))
empresa_data$VlrEnergiaEconomizadaTotal <- as.numeric(gsub(",", ".", empresa_data$VlrEnergiaEconomizadaTotal))
empresa_data$VlrRetiradaDemandaPontaTotal <- as.numeric(gsub(",", ".", empresa_data$VlrRetiradaDemandaPontaTotal))

# Remover valores ausentes nas colunas principais
empresa_data <- na.omit(empresa_data)

# Resumo dos dados para garantir que foram limpos corretamente
str(empresa_data)

# Análise Exploratória dos Dados
# Calcular medidas de tendência central e dispersão
media_custo <- mean(empresa_data$VlrCustoTotal, na.rm = TRUE)
mediana_custo <- median(empresa_data$VlrCustoTotal, na.rm = TRUE)
variancia_custo <- var(empresa_data$VlrCustoTotal, na.rm = TRUE)
desvio_padrao_custo <- sd(empresa_data$VlrCustoTotal, na.rm = TRUE)

# Exibir os resultados
cat("Média do Custo Total dos Projetos: R$", round(media_custo, 2), "\n")
cat("Mediana do Custo Total dos Projetos: R$", round(mediana_custo, 2), "\n")
cat("Variância do Custo Total dos Projetos: R$", round(variancia_custo, 2), "\n")
cat("Desvio Padrão do Custo Total dos Projetos: R$", round(desvio_padrao_custo, 2), "\n")

# Análise descritiva dos dados adicionais
summary(empresa_data)

# Agrupar por empresa e somar valores
projetos_por_empresa <- empresa_data %>%
  group_by(NomAgente) %>%
  summarise(
    TotalCusto = sum(VlrCustoTotal, na.rm = TRUE),
    EnergiaEconomizada = sum(VlrEnergiaEconomizadaTotal, na.rm = TRUE),
    TotalProjetos = n()
  ) %>%
  arrange(desc(TotalCusto))

# Visualizar os primeiros resultados
df_head <- head(projetos_por_empresa, 10)
print(df_head)

# Visualização dos Dados
# Alterar NomAgente para conter apenas as iniciais
projetos_por_empresa$NomAgente <- sapply(
  strsplit(projetos_por_empresa$NomAgente, " "),
  function(x) paste(toupper(substring(x, 1, 1)), collapse = "")
)

# Gráfico de barras: Investimento Total por Empresa (com iniciais no eixo x)
grafico_investimento <- ggplot(data = projetos_por_empresa, aes(x = reorder(NomAgente, -TotalCusto), y = TotalCusto, fill = NomAgente)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Investimento Total por Empresa (Top 10)",
    x = "Empresa (Iniciais)", y = "Investimento Total (R$)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Exibir e salvar gráfico
print(grafico_investimento)
ggsave("scr/outputs/investimento_total_por_empresa.png", plot = grafico_investimento, width = 10, height = 6)

# Análise de Correlação entre Investimento e Economia de Energia
correlacao <- cor(empresa_data[, c("VlrCustoTotal", "VlrEnergiaEconomizadaTotal", "VlrRetiradaDemandaPontaTotal")], use = "complete.obs")
cat("Correlação entre Investimento e Economia de Energia: \n")
print(round(correlacao, 2))

# Visualizar matriz de correlação
png("scr/outputs/matriz_de_correlacao.png", width = 800, height = 800)
corrplot(correlacao, method = "circle")
dev.off()

# Gráfico de dispersão: Investimento vs. Economia de Energia
grafico_dispersao <- ggplot(empresa_data, aes(x = VlrCustoTotal, y = VlrEnergiaEconomizadaTotal)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", col = "red") +
  theme_minimal() +
  labs(
    title = "Investimento vs Economia de Energia por Empresa",
    x = "Investimento Total (R$)", y = "Energia Economizada (kWh)"
  )

# Exibir e salvar gráfico
print(grafico_dispersao)
ggsave("outputs/investimento_vs_economia_energia.png", plot = grafico_dispersao, width = 10, height = 6)

# Análise de Frequência de Uso por Tipo de Equipamento
equipamento_frequencia <- equipamento_data %>%
  count(DscTipoEquipamento) %>%
  arrange(desc(n))

# Gráfico de barras para frequência de uso de tipos de equipamento
grafico_frequencia <- ggplot(equipamento_frequencia, aes(x = reorder(DscTipoEquipamento, -n), y = n, fill = DscTipoEquipamento)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Frequência de Uso por Tipo de Equipamento",
    x = "Tipo de Equipamento", y = "Frequência de Uso"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Exibir e salvar gráfico
print(grafico_frequencia)
ggsave("scr/outputs/frequencia_tipo_equipamento.png", plot = grafico_frequencia, width = 10, height = 6)
