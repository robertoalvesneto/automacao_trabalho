# AUTORUN
O processo de trocar de branchs e tasks é repetitivo:
- atualizar branchs;
- apagar minhas alterações locais;
- selecionar qual branch eu quero [talvez uma task também]

O processo de rodar o projeto também é repetitivo:
- verificar pacotes do npm;
- abrir o navegador no link certo [se for frontend]
- rodar o projeto

O objetivo desse script é simplificar essas etapas, que, como sou tester e mudo muito de branchs
e rodo muitas tasks, se torna repetitivo e cansativo.

## Observações:
O script foi feito visando um **workflow específico de github** (o que acredito ser o mais comum) e é voltado para projetos de **nodejs**, usando os comandos  **npm run dev** para rodar o front e **npm start** para o back.

Ele também abre o navegador **firefox** na porta **3000** do **localhost**.

Acredito que essas mudanças sejam simples de serem feitas com um pouco de conhecimento de bash, uma vez que está tudo dividido em funções pequenas e claras, e que os comandos rodados dentro do script que devem ser alterados são os mesmos que rodamos diretamente no terminal, ficando fácil de achar.

## Como usar:
### Pré configurações:
Exporte o script para ser acessivel de qualquer lugar `source work`.

Desse modo, sempre que reiniciar o sistema terá que exportar novamente, se quiser **adicionar
permanentemente** ao path, adicione ao seu **.bashrc** `source [Dir-path]/work`.

### Rodando:
Digitando `work -h` você tem acesso as mesmas instruções que a seguir:

**Uso:** work [OPTION]... [TASK]...

**Sem passar argumentos:**

Tenta checar automaticamente se é frontend ou backend (funciona apenas para nextjs e nestjs)

**Argumentos:**
|ARGUMENTO| O QUE FAZ |
|---|---|
|`-rf` | rodar o frontend (deve ser o primeiro comando)|
|`-rb` | rodar o backend (deve ser o primeiro comando)|
|`--auto` | Tenta checar automaticamente se é frontend ou backend (funciona apenas para nextjs e nestjs)|
|`-cop [OPTION]` | atualiza a lista de branchs; apaga as mudanças locais; checkout e pull|
|&emsp;`-m` ou `--main` | main branch|
|&emsp;`-d` ou `--develop` | develop branch|
|&emsp;`-f` ou `--feature` | feature branch|
|&emsp;`-b` ou `--bugfix` | bugfix branch|
|&emsp;`-h` ou `--hotfix` | hotfix branch|

### Exemplos:
``` bash
# Rodar o front
work -rf

# Dar checkout na main
work -cop --main

# Dar checkout em uma branch especifica de desenvolvimento e depois rodar o frontend
work -rf -cop -d [SUB-BRANCH]
```

![rodando front](/assets/rodando_frontend.png)

![work cop](/assets/work-cop.png)
