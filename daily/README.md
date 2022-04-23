# DAILY
Preciso fazer registro das reuniões que participo pois podem ser úteis posteriormente em relatórios.

## Como usar:
### Pré configurações:
1. Edite o arquivo `credential.json` com as suas credenciais fornecidas na API do driver
2. Crie um arquivo `.env` na raiz do projeto com as seguintes váriaveis:
``` .env
WINDOWSPATH={path_windows}
LINUXPATH={path_linux}
PRIMARYDIR={none_pasta}
SECONDARYDIR={nome_pasta}
```
obs: Por enquanto todas essas vars e estruturas são necessárias

### Rodando script:
1. tire um print da reunião
2. salve com uma das seguintes iniciais de arquivo dentro da pasta criada `WINDOWSPATH/PRIMARYDIR/SECONDARYDIR`:

|sigla|correspondencia|
|-----|---------------|
|  d  |     daily     |
| rev |     review    |
| ret | retrospective |
|  p  |    planning   |
|{str}|    generic    |

O arquivo pode conter qualquer nome após as iniciais definidas, apenas as primeiras letras são analisadas. Se as primeiras letras não tiverem
na tabela, o arquivo é salvo como 'generic'

3. executo `python3 main.py`

## O que o programa faz:

1. pega o ulitmo arquivo de cada tipo na pasta e apaga os demais (digamos que você tirou três prints de daily, d1, d2, d3. ele pega o ultimo).
3. renomeia para `nome + data atual + hora atual`
4. cria, se não existir, a pasta no seu driver do nome da var `PRIMARYDIR` do arquivo .env
5. cria, se não existir, a pasta no seu driver do nome da var `SECONDARYDIR` do arquivo .env
6. cria, se não existir, uma pasta com o mês do arquivo que você vai subir
7. envia o arquivo para o driver
8. limpa sua pasta local
