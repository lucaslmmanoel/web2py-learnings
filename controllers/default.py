# -*- coding: utf-8 -*-


# Retornando a index da aplição
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome To the rent Moovies!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin')
def grid():
    response.view = 'generic.html'
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


""" Relizando o CRUD de Locação """

# Controller para uma nova locação
def new_location():
    form = SQLFORM(Locacao)
    if form.process().accepted:
        session.flash = "Locação Realizada filme: %s" % form.vars.filmes
        redirect(URL('new_location'))
    elif form.errors:
        response.flash = 'Algum erro no formulário foi encontrado'
    else:
        response.flash = 'Preencha o formulário'
    return dict(form=form)
# Visualizando as locações
def see_locations():
    grid = SQLFORM.grid(Locacao)
    return dict (grid=grid)
# Editando os dados de locações
def edit_location():
    form = SQLFORM(Locacao, request.args(0 , cast = int), showid=False)
    if form.process().accepted:
        session.flash ="Locação editada"
    elif form.errors:
        response.flash = "Algo de errado ocorreu"
    else:
        response.flash = "Selecione algo para editar"
    return dict(form = form)
def delete_location():
    db = (Locacao.id==request.args(0, cast = int).delete())
    session.flash = "A locação foi apagada"
    redirect(URL('see_location'))



"""realizando o crud de estoque """

# Controller para estoque
def new_estoque():
    form = SQLFORM(ItemsEstoque)
    if form.process().accepted:
        session.flash = "Estoque Atualizado"
        redirect(URL('estoque'))
    elif form.errors:
        response.flash = 'Algum Erro no formulário foi encontrado'
    else:
        response.flash = 'Preencha o formulário'
    return dict(form=form)

# Visualizadno os estoques
def see_estoque():
    grid = SQLFORM.grid(ItemsEstoque)
    return dict(grid=grid)

# Alteração de estoque
def edit_estoque():
    form = SQLFORM(ItemsEstoque, request.args(0, cast=int), showid=False)
    if form.process().accepted:
        session.flash = "Estoque Atualizado"
    elif form.errors:
        response.flash = "Algum erro foi encontrado"
    else:
        response.flash = "Selecione Ago para editar"
    return dict(form=form)
# Excluindo o estoque
def delete_estoque():
    db = (ItemsEstoque.id==request.args(0, cast = int).delete())
    session.flash = "O filme foi apagado"
    redirect(URL('see_estoque'))


"""Controllers para Realizar o CRUD de filme """
# Controller que cria um filme
def new_moovie():
    form = SQLFORM(Filmes)
    if form.process().accepted:
        session.flash = 'Novo Filme inserido: %s' % form.vars.titulo
        redirect(URL('see_moovies'))
    elif form.errors:
        response.flash = 'Algum erro encontrado no formulário'
    else:
        response.flash = 'Preencha o formulário'
    return dict(form=form)

# Controller que retorna os filmes
def see_moovies():    
    grid = SQLFORM.grid(Filmes)
    return dict(grid=grid)
# Controller para realizar a edição dos dados do filme
def edit_moovie():
    form = SQLFORM(Filmes, request.args(0, cast=int), showid=False)
    if form.process().accepted:
        session.flash = 'Filme atualizado: %s' % form.vars.titulo
        redirect(URL('see_moovies'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = "Selecione algo para editar!"
    return dict(form=form)


# Controller que realiza a exclusão de um filme
def delete_moovie():
    db = (Filmes.id==request.args(0, cast=int).delete())
    session.flash = "O filme foi apagado"
    redirect(URL("see_moovies"))