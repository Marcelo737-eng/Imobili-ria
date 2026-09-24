# Como executar o sistema

## Primeiro, o mais importante

O sistema é um **programa que roda no seu computador**. Ele não fica na internet.
Quando você o inicia, seu próprio computador passa a funcionar como servidor, e você usa o
sistema pelo navegador (Chrome, Edge, Firefox ou Safari).

Por isso:

- **No computador:** funciona em Windows, Mac e Linux.
- **No celular:** o celular **não executa** o sistema. Ele **acessa** o sistema que está
  rodando no computador, pela rede Wi-Fi. Veja a seção
  [Usar no celular](#usar-no-celular).

---

## O que você precisa

Apenas o **Python 3.9 ou mais novo**. Nada além disso — nenhuma biblioteca, nenhum banco
de dados para instalar.

### Como saber se já tenho Python

Abra o terminal e digite:

| Sistema | Como abrir o terminal | Comando |
|---|---|---|
| **Windows** | Tecla ⊞ Windows → digite `cmd` → Enter | `py --version` |
| **Mac** | ⌘ + Espaço → digite `terminal` → Enter | `python3 --version` |
| **Linux** | Ctrl + Alt + T | `python3 --version` |

Se aparecer algo como `Python 3.11.5`, está pronto. Se aparecer
*"comando não encontrado"* ou uma versão menor que 3.9, instale primeiro:

- **Windows e Mac:** https://www.python.org/downloads/
  → No Windows, durante a instalação, **marque a caixa "Add Python to PATH"**.
  Essa opção é o motivo mais comum de erro depois.
- **Ubuntu/Debian:** `sudo apt install python3`
- **Fedora:** `sudo dnf install python3`

---

## Instalar do zero num computador novo

Se você recebeu os arquivos `instalar-parte-1.py` até `instalar-parte-11.py`, o caminho é
este (não precisa de instalação anterior, nem de nada que estivesse na máquina antes):

1. Crie uma pasta vazia, por exemplo `C:\Sistema` (Windows) ou `~/Sistema` (Mac/Linux).
2. Coloque **as 11 partes na mesma pasta**. Se faltar alguma, o instalador diz qual.
3. Execute **apenas a parte 1** — ela encontra as outras sozinha:

   | Sistema | Comando |
   |---|---|
   | **Windows** | `py instalar-parte-1.py` |
   | **Mac / Linux** | `python3 instalar-parte-1.py` |

4. O instalador cria a pasta `sistema-imobiliaria`, grava os 102 arquivos, pede um Enter
   e já inicia o sistema com os dados de exemplo.

Se preferir o arquivo único, use `sistema-imobiliaria.zip`: extraia tudo e siga para o
passo a passo do seu sistema, abaixo.

### Conferir se a instalação ficou completa

Depois do primeiro início, entre como administrador e confirme estes seis pontos. Se
todos aparecerem, a instalação está íntegra — não é preciso conferir arquivo por arquivo.

| Onde olhar | O que deve aparecer |
|---|---|
| **Imóveis** | 10 imóveis cadastrados, com fotos (70 no total) |
| **Clientes** | 10 clientes, com os papéis de proprietário, locatário, comprador e fiador |
| **Contratos** | 2 contratos assinados: `2026/0001` (compra e venda) e `2026/0002` (locação) |
| **Documentos e modelos** | 7 modelos de texto, entre eles *Compromisso de compra e venda* e *Contrato de locação residencial* |
| **Vistorias e laudos** | 4 vistorias (`VS0001` a `VS0004`); abra uma concluída e baixe o laudo em PDF |
| **Análise de locação** | 2 análises: `AL0001` (aprovada) e `AL0002` (aprovada com ressalvas); abra uma e baixe o relatório em PDF |

Os dois PDFs — laudo de vistoria e relatório de análise — são gerados na hora pelo
sistema. Se os dois abrirem, significa que o gerador de PDF, o banco e os arquivos
anexados estão todos funcionando.

---

## Windows — passo a passo

1. Coloque a pasta do sistema em um lugar simples, por exemplo `C:\Sistema`.
2. Abra a pasta e **dê dois cliques em `INICIAR-WINDOWS.bat`**.
3. Uma janela preta vai abrir e o navegador abrirá sozinho no sistema.
4. Entre com:
   - E-mail: `admin@imobiliaria.com.br`
   - Senha: `admin123`

**Mantenha a janela preta aberta** enquanto usar o sistema. Para encerrar, feche a janela
ou pressione `Ctrl + C` nela.

> **Na primeira vez demora cerca de meio minuto.** O sistema está montando os dados de
> exemplo: 10 imóveis com 70 fotos, 56 documentos em PDF, captações, uma venda com contrato
> assinado, uma locação com cobranças, 4 vistorias com laudo e 2 análises de crédito de
> locação. Nas próximas vezes a abertura é imediata.

### Acessos de exemplo (para ver as permissões de cada perfil)

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | `admin@imobiliaria.com.br` | `admin123` |
| Gerente | `gerente@imobiliaria.com.br` | `gerente123` |
| Corretor | `corretor@imobiliaria.com.br` | `corretor123` |
| Captador | `captador@imobiliaria.com.br` | `captador123` |
| Assistente | `assistente@imobiliaria.com.br` | `assistente123` |
| Vistoriador | `vistoriador@imobiliaria.com.br` | `vistoria123` |

Se o duplo clique não funcionar, faça pelo Prompt de Comando:

```
cd C:\Sistema\sistema-imobiliaria
py run.py --demo
```

---

## Mac e Linux — passo a passo

Abra o terminal e digite (ajustando o caminho para onde você colocou a pasta):

```bash
cd ~/sistema-imobiliaria
python3 run.py --demo
```

O navegador abrirá sozinho. Entre com `admin@imobiliaria.com.br` / `admin123`.

Alternativa: `./iniciar-mac-linux.sh`
(se der erro de permissão, rode antes `chmod +x iniciar-mac-linux.sh`)

---

## Usar no celular

O celular acessa o sistema que está rodando no computador. Os dois precisam estar
**na mesma rede Wi-Fi**.

1. Inicie o sistema no computador normalmente.
2. Olhe a janela do terminal. Ela mostra duas linhas, mais ou menos assim:

   ```
   ABRA NO NAVEGADOR DESTE COMPUTADOR:
       http://localhost:8000

   ABRA NO CELULAR OU TABLET (na mesma rede Wi-Fi):
       http://192.168.0.15:8000        <-- este endereço
   ```

3. No celular, abra o navegador e digite **o segundo endereço** (o que começa com
   `192.168.` ou `10.`). Não use `localhost` no celular — no celular, `localhost`
   significa o próprio celular.

A interface se adapta à tela do celular: o menu vira um botão de três linhas no canto
superior esquerdo.

### Deixar o sistema com ícone próprio, como um aplicativo

Dá para colocar o sistema na tela inicial do celular. Ele passa a abrir com um toque,
em tela cheia, sem a barra de endereço do navegador.

**No Android (Chrome):** toque no menu **⋮** e escolha **Adicionar à tela inicial**.

**No iPhone (Safari):** toque no botão **Compartilhar** (o quadrado com a flecha para
cima) e escolha **Adicionar à Tela de Início**.

O ícone é o mesmo do sistema (a casa branca sobre o azul) e o nome que aparece embaixo
dele é o nome da sua imobiliária, como está em Configurações.

**Uma explicação honesta sobre o botão "Instalar".** Quando você acessa por
`http://localhost` no próprio computador, o navegador mostra um convite para instalar e
o sistema aparece na lista de aplicativos. Pelo endereço de rede (`http://192.168...`)
esse convite **não** aparece: os navegadores só oferecem a instalação completa em
endereços `https://`, e montar HTTPS numa rede doméstica exigiria certificado. O
"Adicionar à tela inicial" acima funciona igual nos dois casos e resolve o que
importa — abrir rápido, com ícone e em tela cheia.

**O sistema não funciona sem internet.** Todos os dados ficam no computador que está
rodando o servidor, não no celular. Sem rede, o aplicativo abre e avisa que está sem
conexão, mas não mostra imóveis nem clientes. Isso é de propósito: guardar ficha
cadastral, comprovante de renda e consulta de crédito na memória do celular
transformaria um aparelho perdido em um vazamento de dados.

### Fazer vistoria pelo celular

A tela de vistoria foi feita para isso. Dentro do imóvel, no celular:

1. Entre em **Vistorias e laudos** e abra a vistoria (ou crie uma nova).
2. A lista de ambientes aparece em cima; toque no ambiente que vai conferir.
3. Toque em **Preencher** no item, escolha o estado de conservação, descreva e anote a
   ressalva se houver.
4. Toque em **Salvar e tirar foto** — o celular abre a câmera direto.
5. Terminado o ambiente, toque em **Marcar como vistoriado**; o sistema já abre o próximo.
6. No fim, **Concluir vistoria** gera o laudo em PDF.

Para o vistoriador de campo existe um perfil próprio, que vê apenas o que ele precisa
(imóveis, locações, vistorias, agenda e tarefas) e não vê financeiro, contratos nem
comissões. Nos dados de exemplo ele é o `vistoriador@imobiliaria.com.br` / `vistoria123`.

### Se o celular não abrir a página

| Verifique | Como resolver |
|---|---|
| Mesma rede Wi-Fi? | Celular e computador devem estar no mesmo Wi-Fi. Dados móveis (4G/5G) não funcionam. |
| Firewall do Windows | Na primeira execução aparece um aviso do Windows Defender. Clique em **Permitir acesso**. Se você clicou em cancelar, veja abaixo. |
| Rede "pública" no Windows | Configurações → Rede → mude o perfil da rede de *Pública* para *Privada*. |
| Rede de empresa/escola | Muitas bloqueiam a comunicação entre aparelhos. Use uma rede doméstica ou o roteador do celular. |

**Liberar no firewall do Windows** (se você cancelou o aviso): Painel de Controle →
Firewall do Windows Defender → Permitir um aplicativo → Alterar configurações →
Permitir outro aplicativo → procure o `python.exe` → marque **Redes privadas**.

### Rodar direto no celular (Android)

É possível, mas trabalhoso. Se realmente precisar, instale o
[Termux](https://f-droid.org/packages/com.termux/) e execute:

```bash
pkg install python
cd /storage/emulated/0/Download/sistema-imobiliaria
python run.py --demo
```

Depois acesse `http://localhost:8000` no navegador do próprio celular.
**Para uso no dia a dia, o caminho recomendado é o computador servindo o celular pela
rede Wi-Fi.**

---

## Problemas comuns

### "python não é reconhecido como comando" (Windows)

O Python foi instalado sem a opção *Add Python to PATH*. Duas saídas:

1. Reinstale o Python marcando a caixa **"Add Python to PATH"** na primeira tela; ou
2. Use `py` em vez de `python`: `py run.py --demo`

### "ModuleNotFoundError: No module named 'app'"

Você está executando de fora da pasta do sistema, ou extraiu o `.zip` pela metade.

- Confirme que `run.py` e a pasta `app` estão **lado a lado** na mesma pasta.
- Se baixou um `.zip`, **extraia todo o conteúdo** antes de executar — não dê duplo
  clique dentro do zip.
- Entre na pasta antes de rodar: `cd caminho/da/pasta` e depois `python3 run.py`.

### A janela abre e fecha na hora (Windows)

Houve um erro que você não conseguiu ler. Para ver a mensagem, abra o Prompt de Comando,
entre na pasta e execute `py run.py` — assim o erro fica visível na tela.

### "Address already in use" / porta ocupada

O sistema já troca de porta sozinho e avisa. Se quiser escolher:

```
python3 run.py --porta 8500
```

Depois acesse `http://localhost:8500`.

### O navegador não abriu sozinho

Abra manualmente e digite `http://localhost:8000`.

### Esqueci a senha do administrador

Com o servidor parado, execute:

```bash
python3 -c "import sys; sys.path.insert(0,'.'); from app import db, seguranca; db.inicializar(); db.execute('UPDATE usuarios SET senha_hash=? WHERE papel=?', (seguranca.gerar_hash('novasenha123'), 'administrador')); print('Senha redefinida para: novasenha123')"
```

### Atualizei o sistema — vou perder o que já cadastrei?

Não. A pasta `dados/` (onde ficam o banco `imobiliaria.db`, as fotos e os documentos)
**não é tocada** na atualização: o instalador nem inclui essa pasta no pacote. Ao subir
uma versão nova, o sistema acrescenta as tabelas e as colunas que faltam e mantém tudo
o que já existia.

Isso foi testado partindo de um banco da primeira versão, com 26 tabelas: depois da
atualização ficaram 61 tabelas, e os 10 imóveis, 10 clientes, 70 fotos, os documentos,
as propostas, os corretores e os usuários continuaram lá. Rodar a atualização várias
vezes seguidas não duplica nem altera nada.

Quando o sistema encontra um banco de versão anterior **com cadastros**, ele guarda uma
cópia de segurança em `dados/imobiliaria-antes-v2.db` antes de mexer em qualquer coisa.
Numa instalação nova esse arquivo não é criado — não havia nada para proteger.

Mesmo assim, antes de atualizar, **copie a pasta `dados/`** para outro lugar. É um
backup completo e leva um segundo — vale o hábito.

### Quero começar do zero, sem os dados de exemplo

```bash
python3 run.py --reset
```

Ele pede confirmação (digite `apagar`) e apaga tudo. Na próxima inicialização o sistema
recria o administrador padrão e começa com a base vazia.

---

## Perguntas frequentes

**Preciso de internet?**
Não. O sistema funciona totalmente offline. Internet só é necessária para instalar o
Python, uma única vez.

**Os dados ficam salvos?**
Sim, na pasta `dados/`, dentro da pasta do sistema. Fechar o servidor não apaga nada.

**Como faço backup?**
Copie a pasta `dados/` para um pendrive ou serviço de nuvem. Ela contém o banco de dados,
as fotos e todos os documentos anexados.

**Vários computadores podem usar ao mesmo tempo?**
Sim. Deixe o sistema rodando em um computador e os outros acessam pelo endereço da rede
(`http://192.168.x.x:8000`), do mesmo jeito que o celular.

**Posso colocar na internet para acessar de qualquer lugar?**
Tecnicamente sim, mas exige cuidados de segurança (HTTPS, domínio, servidor). Como o
sistema guarda documentos e dados pessoais de clientes, isso deve ser feito com apoio
técnico. Para uso no escritório, a rede local é mais simples e mais segura.
