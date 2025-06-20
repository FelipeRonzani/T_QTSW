import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

URL_BASE = "https://www.sapienslab.tech"

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

# @pytest.mark.skip(reason="Desativado temporariamente")
@pytest.mark.parametrize("driver", DISPOSITIVOS.items(), ids=DISPOSITIVOS.keys(), indirect=True)
def test_navegacao(driver):
    """
    Testa a navegação pelo menu principal, garantindo que ao clicar nas seções
    (O aplicativo, Funcionalidades, Sobre nós, Contato, Avaliações*) a rolagem ocorre corretamente.
    A seção 'Avaliações' só é testada na versão Android.
    Relata todas as falhas ao final.
    """
    wait = WebDriverWait(driver, 10)
    driver.get(URL_BASE)
    time.sleep(5)
    
    secoes = [
        "O aplicativo",
        "Funcionalidades",
        "Sobre nós",
        "Contato",
    ]
    # Adiciona "Avaliações" apenas para Android
    if getattr(driver, "_emulacao_nome", None) == "android":
        secoes.append("Avaliações")

    original_scroll = driver.execute_script("return window.scrollY;")
    erros = []

    for secao_texto in secoes:
        try:
            if getattr(driver, "_emulacao_nome", None) == "android":
                try:
                    menu_container = driver.find_element(By.ID, "MENU_AS_CONTAINER")
                    if menu_container.is_displayed():
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                        time.sleep(5)
                except Exception:
                    pass

                menu_btn = wait.until(
                    EC.element_to_be_clickable((By.ID, "MENU_AS_CONTAINER_TOGGLE"))
                )
                menu_btn.click()
                wait.until(
                    EC.visibility_of_element_located((By.ID, "MENU_AS_CONTAINER"))
                )
                time.sleep(5)
                elemento = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//nav[@id='MENU_AS_CONTAINER_EXPANDABLE_MENU']//a[normalize-space(text())='{secao_texto}']")
                    )
                )
                scroll_before = driver.execute_script("return window.scrollY;")
                elemento.click()
                time.sleep(5)
                scroll_after = driver.execute_script("return window.scrollY;")
                assert scroll_after != scroll_before, f"Não houve rolagem ao clicar em '{secao_texto}' no Android. Antes: {scroll_before}, Depois: {scroll_after}"
            else:
                time.sleep(5)
                elemento = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//wix-dropdown-menu//a[@data-testid='linkElement'][.//p[normalize-space(text())='{secao_texto}']]")
                    )
                )
                scroll_before = driver.execute_script("return window.scrollY;")
                elemento.click()
                time.sleep(5)
                scroll_after = driver.execute_script("return window.scrollY;")
                assert scroll_after != scroll_before, f"Não houve rolagem ao clicar em '{secao_texto}' no desktop/tablet. Antes: {scroll_before}, Depois: {scroll_after}"
            driver.execute_script("window.scrollTo(0, arguments[0]);", original_scroll)
        except Exception as e:
            erros.append(str(e))
    if erros:
        pytest.fail("Falhas na navegação:\n" + "\n".join(erros))

# @pytest.mark.skip(reason="Desativado temporariamente")
def test_formulario(driver):
    """
    Testa o formulário de contato e verifica se houve rolagem ao clicar no menu.
    Relata todas as falhas ao final.
    """
    wait = WebDriverWait(driver, 10)
    driver.get(URL_BASE)
    time.sleep(5)
    erros = []

    try:
        if getattr(driver, "_emulacao_nome", None) == "android":
            menu_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "MENU_AS_CONTAINER_TOGGLE"))
            )
            menu_btn.click()
            wait.until(
                EC.visibility_of_element_located((By.ID, "MENU_AS_CONTAINER"))
            )
            time.sleep(5)
            contato_menu = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//nav[@id='MENU_AS_CONTAINER_EXPANDABLE_MENU']//a[normalize-space(text())='Contato']")
                )
            )
        else:
            time.sleep(5)
            contato_menu = wait.until(
                EC.element_to_be_clickable(
                (By.XPATH, "//wix-dropdown-menu//a[@data-testid='linkElement'][.//p[normalize-space(text())='Contato']]")
                )
            )
        scroll_before = driver.execute_script("return window.scrollY;")
        contato_menu.click()
        time.sleep(5)
        scroll_after = driver.execute_script("return window.scrollY;")
        assert scroll_after != scroll_before, f"Não houve rolagem ao clicar em 'Contato'. Antes: {scroll_before}, Depois: {scroll_after}"
    except Exception as e:
        erros.append(str(e))

    try:
        campo_nome = wait.until(EC.visibility_of_element_located((By.ID, "input_comp-kd49plgt1")))
        campo_nome.clear()
        campo_nome.send_keys("Teste")

        campo_sobrenome = wait.until(EC.visibility_of_element_located((By.ID, "input_comp-kd49plh0")))
        campo_sobrenome.clear()
        campo_sobrenome.send_keys("Automação")

        campo_email = wait.until(EC.visibility_of_element_located((By.ID, "input_comp-kd49plh2")))
        campo_email.clear()
        campo_email.send_keys("teste@example.com")

        campo_mensagem = wait.until(EC.visibility_of_element_located((By.ID, "textarea_comp-kd49plh62")))
        campo_mensagem.clear()
        campo_mensagem.send_keys("Mensagem detalhada de teste automatizado.")

        botao_enviar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='buttonElement']")))
        botao_enviar.click()
        mensagem_sucesso = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Mensagem enviada!')]")))
        assert mensagem_sucesso.is_displayed(), "Mensagem de sucesso não exibida após envio do formulário"  
    except Exception as e:
        erros.append(str(e))

    if erros:
        pytest.fail("Falhas no formulário:\n" + "\n".join(erros))