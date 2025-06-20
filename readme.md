# Testes Automatizados com Selenium

Este projeto realiza testes automatizados de navegação e formulário no site [SideMed IA](https://www.sapienslab.tech) utilizando Selenium WebDriver. Para os resultados foi utilizado Pytest para gerar um relatorio em HTML.

## Pré-requisitos

- Python 3.7 ou superior instalado
- Google Chrome instalado

## Instalação

1. **Clone o repositório ou baixe os arquivos do projeto.**

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```sh
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   - No Windows:
     ```sh
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

## Executando os Testes

Execute o script principal para rodar todos os testes automatizados:

```sh
pytest 
```

O script irá:
- Abrir o navegador Chrome em diferentes resoluções (desktop, tablet, mobile)
- Testar a navegação entre as seções do menu
- Testar o envio do formulário de contato