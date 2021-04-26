from flask import Flask, redirect, render_template
from data import users, rentarea, Items, db_session
import datetime
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from Forms import LoginForm, RegisterForm, ItemsForm, ChangeForm, ItemsDelForm
from sqlalchemy import delete

User = users.User
UserData = rentarea.RentArea
Items = Items.Items
ItemsDel = ItemsDelForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/users.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def mains():
    summweight = 0
    summsqmeters = 0
    cliennumber = 0
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.id > 0)
    clients = db_sess.query(UserData).filter(UserData.id > 0)
    for j in items:
        summweight += j.weight
    for j in clients:
        summsqmeters += j.sqmeters
        cliennumber += 1
    if 1 < cliennumber < 5:
        sklonenie = "человека"
    else:
        sklonenie = "человек"
    return render_template('index.html', weight=summweight, sqmeters=summsqmeters, clients=cliennumber,
                           okonch=sklonenie)


@app.route('/index')
def ind():
    summweight = 0
    summsqmeters = 0
    cliennumber = 0
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.id > 0)
    clients = db_sess.query(UserData).filter(UserData.id > 0)
    for j in items:
        summweight += j.weight
    for j in clients:
        summsqmeters += j.sqmeters
        cliennumber += 1
    if 1 < cliennumber < 5:
        sklonenie = "человека"
    else:
        sklonenie = "человек"
    return render_template('index.html', weight=summweight, sqmeters=summsqmeters, clients=cliennumber,
                           okonch=sklonenie)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(3)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/cabinet")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            print(form.email.data)
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        user2 = UserData(
            user_id=user.id
        )
        db_sess.add(user2)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/index")


@app.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    form = ChangeForm()
    form2 = ItemsForm()
    form3 = ItemsDelForm()
    meters = 0
    payment = 0
    db_sess = db_session.create_session()
    CurrentUserData = db_sess.query(UserData).filter(UserData.user_id == current_user.id).first()
    CurrentItems = db_sess.query(Items).filter(Items.user_id == current_user.id)
    if form.submit1.data and form.validate():
        if form.value.data.isdigit() and int(form.value.data) >= 0:
            CurrentUserData.sqmeters = int(form.value.data)
            CurrentUserData.update_date = datetime.datetime.now()
            db_sess.commit()
    if form2.submit2.data and form2.validate():
        if form2.weight.data.isdigit() and int(form2.weight.data) > 0:
            NewItem = Items(
                user_id=current_user.id,
                name=form2.name.data,
                weight=form2.weight.data,
                about=form2.about.data,
                add_date=datetime.datetime.now()
            )

            db_sess.add(NewItem)
            db_sess.commit()
    if form3.submit3.data and form3.validate():
        DeletedItem = db_sess.query(Items).filter(Items.id == form3.id.data).first()
        db_sess.delete(DeletedItem)
        db_sess.commit()
    if CurrentUserData:
        meters = CurrentUserData.sqmeters
        payment = meters * 3
    return render_template('cabinet.html', meters=meters, form=form, payment=payment, items=CurrentItems, form2=form2,
                           form3=form3)


if __name__ == '__main__':
    main()
    app.run(port=5000, host='127.0.0.1')