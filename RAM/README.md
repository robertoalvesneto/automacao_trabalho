# AUTOMAÇÃO DO REGISTRO DE ATIVIDADES
Preciso fazer o registro das atividades que estou fazendo no mês e a porcentagem
de conclusão delas, para, no final do mês, inserir tudo em uma planilha para ser
documentado.

## Como usar:
### Pré configurações:
1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
``` .env
WINDOWSPATH={path_windows}
LINUXPATH={path_linux}
PRIMARYDIR={none_pasta}
SECONDARYDIR={nome_pasta}
OWNER={nome_responsavel_tasks}
```
obs: Por enquanto todas essas vars e estruturas são necessárias

### Rodando script:
ao rodar `python3 main.py` será criado um banco de dados SQLite3 na pasta
`database` e uma interface de texto irá aparecer no seu terminar.

Você pode adicionar uma task, remover, editar, ou exportar todas no formato de
CSV.

As colunas da tabela são:
- description: breve descrição da task
- progress: valor de 0 a 100 em porcentagem
- fortnight: se é para a primeira ou segunda metade do mês
- owner: (preenchimento automático) responsável pela task
- month: (preenchimento automático)
- last_modify: (preenchimento automático)


![registros](/assets/ram.png)
