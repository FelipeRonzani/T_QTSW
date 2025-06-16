import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

URL_BASE = "https://www.sapienslab.tech"

MENU_SECOES = {
    "Produto": [f"{URL_BASE}/produto"],
    "Soluções": [
        f"{URL_BASE}/soluções",
        f"{URL_BASE}/solucoes",  
        f"{URL_BASE}/solu%C3%A7%C3%B5es"  
    ],
    "Preços": [
        f"{URL_BASE}/preços",
        f"{URL_BASE}/precos",  
        f"{URL_BASE}/pre%C3%A7os"  
    ],
    "Recursos": [f"{URL_BASE}/recursos"],
    "Login": [None],  # Botão Login
    "Testar grátis": [
        f"{URL_BASE}/preços",
        f"{URL_BASE}/precos",
        f"{URL_BASE}/pre%C3%A7os"
    ]
}

# Emulação de dispositivos
DISPOSITIVOS = {
    "desktop": None,  # Sem emulação, apenas janela normal
    "android": {"deviceName": "Pixel 7"},
    "tablet": {"deviceName": "iPad Mini"}
}

@pytest.fixture(params=DISPOSITIVOS.items(), ids=DISPOSITIVOS.keys())
def driver(request):
    nome_disp, emulacao = request.param  # Desempacote a tupla
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    if emulacao:
        options.add_experimental_option("mobileEmulation", emulacao)
    driver = webdriver.Chrome(service=Service(), options=options)
    if not emulacao:
        driver.set_window_size(1366, 768)  # Desktop padrão (NoteBook)
    # Adicione o nome_disp ao driver para uso nos testes, se necessário
    driver._emulacao_nome = nome_disp
    driver._emulacao_dict = emulacao
    yield driver
    driver.quit()

# Teste de navegação pelo menu
@pytest.mark.parametrize("driver", DISPOSITIVOS.items(), ids=DISPOSITIVOS.keys(), indirect=True)
def test_navegacao(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(URL_BASE)

    is_mobile = driver._emulacao_dict is not None

    for nome, url_esperada in MENU_SECOES.items():
        if nome == "Login":
            botao_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#comp-kp5f4njg span.LcZX5c")))
            botao_login.click()
        elif nome == "Testar grátis":
            botao_testar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#comp-knd86aci span.l7_2fn")))
            botao_testar.click()
            wait.until(lambda d: any(u in d.current_url for u in url_esperada))
            assert any(u in driver.current_url for u in url_esperada), f"Falha ao navegar para {nome}"
        else:
            links = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="linkElement"]')
            link_correto = None
            for link in links:
                try:
                    texto = link.find_element(By.TAG_NAME, "p").text.strip()
                    if texto == nome:
                        link_correto = link
                        break
                except Exception:
                    continue
            assert link_correto is not None, f"Link '{nome}' não encontrado no menu"
            link_correto.click()
            wait.until(lambda d: any(u in d.current_url for u in url_esperada))
            assert any(u in driver.current_url for u in url_esperada), f"Falha ao navegar para {nome}"

# Teste do formulário de contato
def test_formulario(driver): 
    wait = WebDriverWait(driver, 10)
    driver.get(URL_BASE)
    # Clique no link de contato para abrir o popup
    try:
        contato_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="chjhg"]')))
    except Exception:
        contato_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Contato")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contato_link)
    contato_link.click()

    # Aguarde o campo nome aparecer no popup
    campo_nome = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knodt8ll")))
    campo_nome.click()
    campo_nome.clear()
    campo_nome.send_keys("Teste")

    # Tente avançar para o próximo campo usando TAB, caso clicar não funcione
    try:
        campo_nome.send_keys(Keys.TAB)
        campo_sobrenome = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knodt8lm")))
        campo_sobrenome.clear()
        campo_sobrenome.send_keys("Automação")
    except Exception:
        # Se não avançar, tente clicar diretamente
        campo_sobrenome = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knodt8lm")))
        campo_sobrenome.click()
        campo_sobrenome.clear()
        campo_sobrenome.send_keys("Automação")

    try:
        campo_sobrenome.send_keys(Keys.TAB)
        campo_email = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knodt8lo1")))
        campo_email.clear()
        campo_email.send_keys("teste@example.com")
    except Exception:
        campo_email = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knodt8lo1")))
        campo_email.click()
        campo_email.clear()
        campo_email.send_keys("teste@example.com")

    try:
        campo_email.send_keys(Keys.TAB)
        campo_mensagem_titulo = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knoean29")))
        campo_mensagem_titulo.clear()
        campo_mensagem_titulo.send_keys("Assunto do contato")
    except Exception:
        campo_mensagem_titulo = wait.until(EC.presence_of_element_located((By.ID, "input_comp-knoean29")))
        campo_mensagem_titulo.click()
        campo_mensagem_titulo.clear()
        campo_mensagem_titulo.send_keys("Assunto do contato")

    try:
        campo_mensagem_titulo.send_keys(Keys.TAB)
        campo_mensagem_texto = wait.until(EC.presence_of_element_located((By.ID, "textarea_comp-knodt8lq1")))
        campo_mensagem_texto.clear()
        campo_mensagem_texto.send_keys("Mensagem detalhada de teste automatizado.")
    except Exception:
        campo_mensagem_texto = wait.until(EC.presence_of_element_located((By.ID, "textarea_comp-knodt8lq1")))
        campo_mensagem_texto.click()
        campo_mensagem_texto.clear()
        campo_mensagem_texto.send_keys("Mensagem detalhada de teste automatizado.")

    # Botão enviar
    botao_enviar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#comp-knodt8lw button[data-testid='buttonElement']")))
    botao_enviar.click()

    # Aguarda mensagem de sucesso
    mensagem_sucesso = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Mensagem enviada com sucesso!')]"))
    )
    assert mensagem_sucesso.is_displayed(), "Mensagem de sucesso não exibida após envio do formulário"
