# Ativar o ambiente renv, se disponível
if (file.exists("renv/activate.R")) {
  source("renv/activate.R")
}

# Configurar mirror rápido e confiável
options(repos = c(CRAN = "https://cran-r.c3sl.ufpr.br/"))

# Configurar instalação paralela (usa múltiplos núcleos do processador)
options(Ncpus = parallel::detectCores() - 1)

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
empresa_data <- read.csv("projetos-eficiencia-energetica-empresa.csv", sep = ";", encoding = "latin1", stringsAsFactors = FALSE)
equipamento_data <- read.csv("projetos-eficiencia-energetica-equipamento.csv", sep = ";", encoding = "latin1", stringsAsFactors = FALSE)
uso_final_data <- read.csv("projetos-eficiencia-energetica-uso-final.csv", sep = ";", encoding = "latin1", stringsAsFactors = FALSE)

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
# Gráfico de barras: Investimento Total por Empresa
ggplot(data = projetos_por_empresa, aes(x = reorder(NomAgente, -TotalCusto), y = TotalCusto, fill = NomAgente)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Investimento Total por Empresa (Top 10)",
    x = "Empresa", y = "Investimento Total (R$)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Análise de Correlação entre Investimento e Economia de Energia
correlacao <- cor(empresa_data[, c("VlrCustoTotal", "VlrEnergiaEconomizadaTotal", "VlrRetiradaDemandaPontaTotal")], use = "complete.obs")
cat("Correlação entre Investimento e Economia de Energia: \n")
print(round(correlacao, 2))

# Visualizar matriz de correlação
corrplot(correlacao, method = "circle")

# Gráfico de dispersão: Investimento vs. Economia de Energia
ggplot(empresa_data, aes(x = VlrCustoTotal, y = VlrEnergiaEconomizadaTotal)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", col = "red") +
  theme_minimal() +
  labs(
    title = "Investimento vs Economia de Energia por Empresa",
    x = "Investimento Total (R$)", y = "Energia Economizada (kWh)"
  )

# Análise de Frequência de Uso por Tipo de Equipamento
equipamento_frequencia <- equipamento_data %>%
  count(DscTipoEquipamento) %>%
  arrange(desc(n))

# Gráfico de barras para frequência de uso de tipos de equipamento
ggplot(equipamento_frequencia, aes(x = reorder(DscTipoEquipamento, -n), y = n, fill = DscTipoEquipamento)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Frequência de Uso por Tipo de Equipamento",
    x = "Tipo de Equipamento", y = "Frequência de Uso"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Análise do Uso Final da Energia
uso_final_energia <- uso_final_data %>%
  group_by(DscUsoFinal) %>%
  summarise(
    EnergiaEconomizadaTotal = sum(VlrBeneficioEnergiaEconomizada, na.rm = TRUE),
    DemandaReduzidaPonta = sum(VlrDemandaReduzidaPonta, na.rm = TRUE),
    TotalProjetos = n()
  ) %>%
  arrange(desc(EnergiaEconomizadaTotal))

# Visualizar os primeiros resultados de uso final de energia
print(head(uso_final_energia, 10))

# Gráfico de barras: Uso Final da Energia
ggplot(uso_final_energia, aes(x = reorder(DscUsoFinal, -EnergiaEconomizadaTotal), y = EnergiaEconomizadaTotal, fill = DscUsoFinal)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Energia Economizada por Uso Final",
    x = "Uso Final", y = "Energia Economizada Total (kWh)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Análise de Retirada de Demanda de Ponta por Uso Final
ggplot(uso_final_energia, aes(x = reorder(DscUsoFinal, -DemandaReduzidaPonta), y = DemandaReduzidaPonta, fill = DscUsoFinal)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Demanda Reduzida na Ponta por Uso Final",
    x = "Uso Final", y = "Demanda Reduzida na Ponta (kW)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Análise de Projetos por Equipamento
equipamentos_utilizados <- equipamento_data %>%
  group_by(DscTipoEquipamento) %>%
  summarise(
    QuantidadeTotal = sum(QtdTipoEquipamento, na.rm = TRUE),
    TotalProjetos = n()
  ) %>%
  arrange(desc(QuantidadeTotal))

# Visualizar os primeiros resultados dos tipos de equipamento utilizados
print(head(equipamentos_utilizados, 10))

# Gráfico de barras: Quantidade de Equipamentos Utilizados
ggplot(equipamentos_utilizados, aes(x = reorder(DscTipoEquipamento, -QuantidadeTotal), y = QuantidadeTotal, fill = DscTipoEquipamento)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Quantidade de Equipamentos Utilizados nos Projetos",
    x = "Tipo de Equipamento", y = "Quantidade Total"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = FALSE)

# Análise de Clusters para Identificar Grupos Similares
# Normalizar os dados para clustering
empresa_data_norm <- empresa_data %>%
  select(VlrCustoTotal, VlrEnergiaEconomizadaTotal, VlrRetiradaDemandaPontaTotal) %>%
  scale()

# Aplicar k-means clustering
set.seed(123)
kmeans_result <- kmeans(empresa_data_norm, centers = 3, nstart = 20)

# Adicionar os clusters ao dataset original
empresa_data$Cluster <- as.factor(kmeans_result$cluster)

# Visualizar distribuição dos clusters
ggplot(empresa_data, aes(x = VlrCustoTotal, y = VlrEnergiaEconomizadaTotal, color = Cluster)) +
  geom_point(alpha = 0.6) +
  theme_minimal() +
  labs(
    title = "Clusters de Empresas com Base no Investimento e Economia de Energia",
    x = "Investimento Total (R$)", y = "Energia Economizada (kWh)"
  )

# Visualização Interativa com Plotly
plotly_bar <- plot_ly(data = projetos_por_empresa, x = ~NomAgente, y = ~TotalCusto, type = "bar", name = "Investimento Total")
plotly_bar <- plotly_bar %>% layout(
  title = "Investimento Total por Empresa (Interativo)",
  xaxis = list(title = "Empresa"),
  yaxis = list(title = "Investimento Total (R$)")
)
plotly_bar

# Insights e Próximos Passos
cat("\nInsights Práticos:\n")
cat("- Empresas com maiores investimentos em eficiência energética indicam potenciais parceiros para desenvolvimento tecnológico.\n")
cat("- Projetos que atendem a comunidades de baixa renda devem ser ampliados para garantir benefícios econômicos e acesso equitativo.\n")
cat("- A energia economizada contribui diretamente para a redução de emissões de carbono, promovendo uma matriz energética mais limpa.\n")

# Futuros desenvolvimentos: Modelagem preditiva, análise de clusters e relatórios detalhados.
cat("\nPróximos Passos:\n")
cat("- Realizar análises de correlação adicionais para identificar fatores críticos de sucesso.\n")
cat("- Desenvolver modelos preditivos para prever impactos futuros dos projetos.\n")
cat("- Agrupar projetos similares para definir estratégias mais direcionadas.\n")
