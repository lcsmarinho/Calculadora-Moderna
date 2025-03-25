# Calculadora Moderna

Este é um projeto de uma calculadora moderna construída com a biblioteca Tkinter do Python. A calculadora oferece funcionalidades básicas e científicas, além de um histórico de cálculos.

## Funcionalidades

-   **Calculadora Básica:**
    -   Operações aritméticas básicas: adição, subtração, multiplicação, divisão.
    -   Cálculo de porcentagem.
    -   Limpeza da tela.
    -   Suporte para entrada de números e operações via teclado.
-   **Calculadora Científica:**
    -   Funções trigonométricas: seno, cosseno, tangente.
    -   Funções logarítmicas: logaritmo natural, logaritmo base 10.
    -   Potenciação e radiciação.
    -   Constantes matemáticas: π (pi) e e (número de Euler).
    -   Funções de memória: MC, MR, M+, M-.
    -   Suporte para parênteses e outras funções científicas.
-   **Histórico de Cálculos:**
    -   Armazena um histórico de todos os cálculos realizados.
    -   Permite visualizar e usar cálculos anteriores.
    -   Opção para limpar o histórico.
-   **Interface Gráfica:**
    -   Interface amigável e intuitiva.
    -   Design moderno com temas estilizados.
    -   Barra de status para feedback ao usuário.
    -   Abas para alternar entre os modos básico, científico e histórico.
-   **Persistência de dados:**
    -   o histórico é salvo em um arquivo json.

## Como Executar

1.  **Pré-requisitos:**
    -   Python 3.x instalado.
    -   Biblioteca Tkinter (geralmente incluída na instalação do Python).
2.  **Execução:**
    -   Salve o código em um arquivo Python (por exemplo, `calculadora.py`).
    -   Abra o terminal ou prompt de comando.
    -   Navegue até o diretório onde você salvou o arquivo.
    -   Execute o comando `python calculadora.py`.

## Estrutura do Código

-   **`CalculadoraModerna` (classe):**
    -   Classe principal que define a interface da calculadora.
    -   Métodos para criar widgets, configurar botões, processar entradas, gerenciar histórico, etc.
-   **`carregar_historico()` e `salvar_historico()`:**
    -   Funções para carregar e salvar o histórico de cálculos em um arquivo JSON.
-   **`criar_widgets()`:**
    -   Função para criar todos os widgets da interface gráfica.
-   **`configurar_calc_basica()` e `configurar_calc_cientifica()`:**
    -   Funções para configurar os botões das calculadoras básica e científica.
-   **`configurar_historico()`:**
    -   Função para configurar a aba de histórico.
-   **`processar_botao()` e `processar_botao_cientifico()`:**
    -   Funções para processar os cliques nos botões.
-   **`atualizar_historico_listbox()`, `limpar_historico()` e `usar_historico_selecionado()`:**
    -   Funções para gerenciar o histórico.
-   **`bind_atalhos()`:**
    -   Função para configurar os atalhos de teclado.
-   **`apagar_ultimo_caractere()`:**
    -   Função para apagar o último caractere da expressão.

## Dependências

-   Tkinter
-   json
-   os
-   math
-   datetime
-   re

## Notas

-   O código utiliza a função `eval()` para avaliar expressões matemáticas, o que pode ser perigoso se a entrada do usuário não for confiável.
-   O histórico de cálculos é salvo em um arquivo JSON local (`historico.json`).
-   A interface gráfica é estilizada com o tema "clam" do Tkinter.

## Contribuição

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.
