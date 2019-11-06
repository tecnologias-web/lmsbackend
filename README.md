# Atividades Contínuas 8 e 9

Para as ativdades contínuas 8 e 9 faremos um pequeno projeto em Flask com o conteúdo visto em aula. Esse projeto conterá a navegação completa do sistema e alguns formulários de inclusão, utilizando um banco de dados simples (SQLLite).

## Instruções e Nota

A seguir apresentaremos todas as instruções do projeto. As notas serão dados pelo número de testes passados, conforme fizemos ao longo do semestre. Para fazer os testes, vocês devem estar dentro do ambiente virtual (usem o *requirements.txt* presente nesse repositório) rodando o comando:

``` shell
pytest
```

Isso fará com que os testes presentes rodem e indiquem seus acertos.

## Critétios para AC 8

A AC8 terá como critérios de avaliação a utilização correta dos _templates_ e da navegação do sistema. Siga atentamente as seguintes instruções (nomes de arquivos e urls são importantes!!) para que os testes passem.

O total de testes nessa AC é 32 testes.

### Navegação

Crie as seguintes páginas com as URL's definidas. Todos os _templates_ devem extender um modelo básico, chamado de _base.html_ conforme visto em sala.

* Index ('/'): A página principal da aplicação (Template _index.html_).
* Contato ('/contato/'): Formulário de contato (Template _contato.html_).
* Entrar ('/entrar/'): Formulário de Login (Template _entrar.html_).
* Esqueci ('/esqueci-a-senha/'): Formulário de esquecimento de senha (Template _esqueci.html_).
* Inscrição ('/inscrever/'): Formulário de inscrição na faculdade (Template _inscrever.html_).
* Redefinir a senha ('/redefinicao-de-senha/'): Formulário para redefinir a senha (Template _redefinir.html_).
* Sobre a Faculdade ('/sobre-a-impacta/'): Página de informações da faculdade (Template _sobre.html_).
* Agradecimento ('/agradecimento/'): Página de agradecimento para contatos bem sucedidos (Template _agradecimeno.html_).

Além disso, não esqueça de verificar os links internos das páginas (tanto do _base.html_ quanto das outras) devem estar apontando para as páginas corretas.

## Critétios para AC 9

A AC9 terá como critérios a utilização correta dos formulários. Siga atentamente as seguintes instruções (nomes de arquivos e urls são importantes!!) para que os testes passem.

O total de testes nessa AC é 18 testes.

### Regras de Páginas

Além de responder a URL com um template adequado, os formulários devem responder a um POST da seguinte maneira:

#### Contato

Deve validar os campos obrigatórios (veja o formulário), imprimir uma mensagem no console (use o print do python), redirecionando se der certo para a página de agradecimentos.

A mensagem deve ter o seguinte formato:

``` shell
Envio de e-mail de Contato:
===========================
Nome: {nome digitado}
E-mail: {email digitado}
Assunto: {assunto escolhido}
Como Conheceu: {lista de como conheceu}
Mensagem:
{mensagem}
+++++++++++++++++++++++++++
```

Onde:

* _nome_digitado_: O nome digitado no campo (obrigatório).
* _email_digitado_: O e-mail digitado no campo (obrigatório).
* _assunto_escolhido_: O assunto escolhido, mas no formato completo (se escolheu R, deve colocar Reclamação).
* _mensagem_: A mensagem digitada (obrigatório).
* _lista_de_como_conheceu_: Deve pegar a lista de opções e mostrar separados por Pipes (ex: | Google | Internet |).

Valide as seguintes entradas:

* _nome_: Se não preenchido, volta a mensagem 'Nome completo é obrigatório!'
* _email_: Se não preenchido, volta a mensagem 'E-mail é obrigatório!'
* _assunto_: Se não escolhido, volta a mensagem 'Assunto é obrigatório!'
* _mensagem_: Se não preenchida, volta a mensagem 'Mensagem é obrigatória!'

### Entrar

O formulário de login deve verificar o usuário e senhas digitados. Caso a senha seja `teste123*`, deve redirecionar à página principal.

Efetue as seguintes validações:

* _usuario_ não preenchido volta mensagem 'Usuário é obrigatório!'
* _senha_ não preenchida volta mensagem 'Senha é obrigatória!'
* _senha_ diferente de `teste123*` volta a mensagem 'Usuário e/ou senha incorretos!'

### Esqueci

O formulário de esquecimento de senha deve validar se o e-mail foi digitado e deve redirecionar para a página de redefinição de senha.

Se o e-mail não estiver preenchido, deve retornar a mensagem de erro 'E-mail é obrigatório!'

### Redefinição de senha

Esse formulário deve validar se as duas senhas digitadas estão iguais e se obedecem a seguinte regra:

* Deve ter ao menos um número.
* Deve ter ao menor um caracter alfanumérico (`[!,@,#,$,%,&,*]`)
* Deve ter ao menos 5 caracteres.

Caso esteja correto, volta ao index. Caso contrário volta uma mensagem de erro na página de redefinição de senhas segundo os critérios:

* _senha_ não preenchida volta mensagem 'Senha é obrigatória!'
* _senha2_ não preenchida volta mensagem 'Confirmação de senha é obrigatória!'
* _senha_ diferente de _senha2_ volta mensagem 'Senha e confirmação não estão iguais!'
* _senha_ sem números volta mensagem 'Senha deve ter ao menos um número!'
* _senha_ sem caracteres alfanuméricos volta mensagem 'Senha deve ter ao menos um caracter alfanumérico!'
* _senha_ com tamanho menor que 5 caracteres volta mensagem 'Senha deve ter ao menos 5 caracteres!'
