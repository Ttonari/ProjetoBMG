from flask  import Flask, render_template, request, redirect, session,flash,url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'bmggym123'

app.config['SQLALCHEMY_DATABASE_URI']= \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario= 'root',
        senha= 'root123',
        servidor= 'localhost',
        database= 'bmgbanco'
    )

db = SQLAlchemy(app)

class Clientes(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome= db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    telefone = db.Column(db.String(14), nullable=False)
    nascimento = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    plano = db.Column(db.String(50), nullable=False)
    pagamento = db.Column(db.String(50), nullable=False)
    datadeinicio = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r' % self.name

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    nome = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=False, primary_key=True)
    senha = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nickname}>'


class Planos(db.Model):
    id= db.Column(db.Integer, nullable=False, primary_key=True)
    nome_plano = db.Column(db.String(50), nullable=False)
    tempo_plano = db.Column(db.String(50), nullable=False)
    valor_plano = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Name %r' % self.name

class Despesas(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    nome_despesa = db.Column(db.String(50), nullable=False)
    valor_despesa = db.Column(db.Integer, nullable=False)
    vencimento_despesa = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r' % self.name



@app.route('/')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')

    return render_template('home.html', usuario=session['usuario_logado'])

@app.route('/cadastrar')
def cadastrar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_planos = Planos.query.order_by(Planos.nome_plano)
    return render_template('cadastrar.html', planos=lista_planos)

@app.route('/cadastrando', methods=['POST',])
def cadastrando():

    nome = request.form['nome']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    email = request.form['email']
    nascimento = request.form['nascimento']
    pagamento = request.form['pagamento']
    plano = request.form['plano']
    datadeinicio = request.form['datadeinicio']

    cliente= Clientes.query.filter_by(nome=nome, cpf=cpf).first()

    if cliente:
        flash('cliente já existe!')
        return redirect(url_for('cadastrar'))

    novo_cliente= Clientes(nome=nome, cpf=cpf, telefone=telefone, email=email, nascimento=nascimento, pagamento=pagamento, plano=plano, datadeinicio=datadeinicio)
    db.session.add(novo_cliente)
    db.session.commit()
    flash('Cliente cadastrado com sucesso')
    return redirect ('/cadastrar')

@app.route('/deletar_aluno/<int:id>')
def deletar_aluno(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    cliente=Clientes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Aluno deletado!')
    return redirect(url_for('alunos'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_planos = Planos.query.order_by(Planos.nome_plano)
    cliente= Clientes.query.filter_by(id=id).first()
    return render_template('editar.html', planos=lista_planos, cliente=cliente)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    cliente= Clientes.query.filter_by(id=request.form['id']).first()
    cliente.nome = request.form['nome']
    cliente.cpf = request.form['cpf']
    cliente.telefone = request.form['telefone']
    cliente.email = request.form['email']
    cliente.nascimento = request.form['nascimento']
    cliente.pagamento = request.form['pagamento']
    cliente.plano = request.form['plano']
    cliente.datadeinicio = request.form['datadeinicio']

    db.session.add(cliente)
    db.session.commit()

    flash("Cliente atualizado!")
    return redirect ('/alunos')


@app.route('/alunos')
def alunos():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_clientes= Clientes.query.order_by(Clientes.id)
    return render_template('alunos.html', clientes=lista_clientes)

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario= Usuario.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            return redirect('/')
        else:
            flash('Senha incorreta.')
    else:
        flash('Usuário incorreto.')

    return redirect('/login')


@app.route('/logout')
def logout():
    session['usuario_logado']= None
    flash('Deslogado com sucesso!')
    return redirect('/login')

@app.route('/planos')
def planos():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_planos= Planos.query.order_by(Planos.nome_plano)
    return render_template('planos.html', planos=lista_planos)


@app.route('/editar_plano/<int:id>')
def editar_plano(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    lista_planos = Planos.query.order_by(Planos.nome_plano)
    plano = Planos.query.filter_by(id=id).first()

    return render_template('editar_plano.html', planos=lista_planos, plano=plano)

@app.route('/deletar_plano/<int:id>')
def deletar_plano(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    plano=Planos.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('planos'))

@app.route('/atualizar_plano', methods=['POST',])
def atualizar_plano():
    plano = Planos.query.filter_by(id=request.form['id']).first()
    plano.nome_plano = request.form['nome_plano']
    plano.tempo_plano = request.form['tempo_plano']
    plano.valor_plano = request.form['valor_plano']

    db.session.add(plano)
    db.session.commit()
    return redirect ('/planos')

@app.route('/relatorios')
def relatorios():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_despesas = Despesas.query.order_by(Despesas.nome_despesa)
    lista_clientes = Clientes.query.order_by(Clientes.id)
    lista_planos = Planos.query.order_by(Planos.nome_plano)

    total_despesas= sum(despesa.valor_despesa for despesa in lista_despesas)
    total_planos_clientes = sum(plano.valor_plano for cliente in lista_clientes for plano in lista_planos if cliente.plano == plano.nome_plano)

    saldo_total = total_planos_clientes - total_despesas

    return render_template('relatorios.html', total_despesas=total_despesas, total_planos_clientes=total_planos_clientes, saldo_total=saldo_total)

@app.route('/despesas')
def despesas():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_despesas = Despesas.query.order_by(Despesas.nome_despesa)
    return render_template('despesas.html', despesas=lista_despesas)

@app.route('/cadastrando_despesas', methods=['POST',])
def cadastrando_despesas():


    nome_despesa = request.form['nome_despesa']
    valor_despesa = float(request.form['valor_despesa'])
    vencimento_despesa = request.form['vencimento_despesa']

    nova_despesa = Despesas(nome_despesa=nome_despesa, valor_despesa=valor_despesa, vencimento_despesa=vencimento_despesa)
    db.session.add(nova_despesa)
    db.session.commit()

    return redirect(url_for('despesas',))

@app.route('/deletar_despesa/<int:id>')
def deletar_despesa(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    despesa=Despesas.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('despesas'))

@app.route('/suporte')
def suporte():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    return render_template('suporte.html')

@app.route('/cadastrar_plano')
def cadastrar_plano():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')

    return render_template('/cadastrar_plano.html')

@app.route('/cadastrando_plano', methods=['POST',])
def cadastrando_plano():

    nome_plano = request.form['nome_plano']
    tempo_plano = request.form['tempo_plano']
    valor_plano = float(request.form['valor_plano'])

    plano = Planos.query.filter_by(nome_plano=nome_plano).first()

    if plano:
        flash('plano já existe!')
        return redirect(url_for('cadastrando_plano'))

    novo_plano = Planos(nome_plano=nome_plano, tempo_plano=tempo_plano, valor_plano=valor_plano)
    db.session.add(novo_plano)
    db.session.commit()

    flash('Plano cadastrado com sucesso')
    return redirect(url_for('cadastrar_plano',))




app.run(debug=True,  port=8000)
