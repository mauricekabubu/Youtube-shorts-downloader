from flask import Flask,render_template,redirect,url_for,flash,request,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import current_user, login_required, login_user, login_manager,UserMixin,LoginManager,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
import os
from extract import download_youtube_video
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail,Message
from datetime import timedelta
import threading



load_dotenv()


app = Flask(__name__)

#Setting up security key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#Securing my cookies in the browser
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)



# Mail configurations for SendGrid
app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "apikey"  
app.config["MAIL_PASSWORD"] = os.getenv("SENDGRID_API_KEY")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("SENDGRID_SENDER")

#mail initialisation
mail = Mail(app)   




#Database initialisation
#old sqlite database
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
#New Mysql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mauricekabubu2006%40@localhost/flask_app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app,db)



#Setting up LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(Users, int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    history = db.relationship("History", backref="user", lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id}, salt="password-reset")

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(
                token,
                salt="password-reset",
                max_age=expires_sec
            )
        except Exception:
            return None
        return Users.query.get(data["user_id"])
    
    
    def __repr__(self):        
        return f"<User id={self.id} username={self.username} history_count={len(self.history)}>"
        
        
    
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default="downloading")


#sending the reset link via email for reset password



@app.route("/",methods=["POST","GET"])
def index():
    
    return render_template("welcome.html")

@app.route("/welcome",methods=["GET","POST"])
def welcome():
    
    return render_template("welcome.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            
            
            flash("You are logged in",category="success")
            
            return redirect(url_for("dashboard"))
        
        else:
            flash("Invalid inputs please try again!",category="danger")
            
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email","").strip()
        password = request.form.get("password")
        password1 = request.form.get("password1")
        
        user = Users.query.filter_by(username=username).first()
        if user:
            flash("Account exists!",category="danger")
            
            return redirect(url_for("register"))
        
        elif len(username)<4:
            flash("Username must exceed 4 characters!",category="danger")
            
            return redirect(url_for("register"))
        
        if not email:
            flash("Email is required", "danger")
            return redirect(url_for("register"))

        if "@" not in email:
            flash("Invalid email address", "danger")
            return redirect(url_for("register"))

        
        elif not email or "@" not in email:
            flash("Please enter a valid email address", "danger")
            return redirect(url_for("register"))

        
        elif len(password)<8:
            flash("password must exceed 8 characters!",category="danger")
            
            return redirect(url_for("register"))
        
        elif password!=password1:
            flash("both passwords should be same",category="danger")
            
            return redirect(url_for("register"))
        
        
        else:
            new_user = Users(username=username,
                             email=email,
                             password=generate_password_hash(password))
            
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            
            
            flash("Account created successfully",category="success")           
            
            return redirect(url_for("dashboard"))
    
    return render_template("register.html")

@app.route("/logout",methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out!",category="success")
    
    return redirect(url_for("welcome"))
      

@app.route("/delete/<int:id>",methods=["GET","POST"])
@login_required
def delete(id):
    url = History.query.get_or_404(id)    
    print("VIDEO ID:", url.id, "VIDEO USER_ID:", url.user_id, "CURRENT USER ID:", current_user.id)
    if url.user_id != current_user.id:
        flash("You cannot delete this video!",category="danger")
        
        return redirect(url_for("history"))    
    
    db.session.delete(url)
    db.session.commit()
    
    flash("You have successfully deleted the video",category="success")    
    
    return redirect(url_for("history"))
    

@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = Users.query.filter_by(email=email).first()
        print("FORM EMAIL:", repr(email))
        print("USER FOUND:", user)
        if user:
            print("USER.EMAIL:", repr(user.email))

        
        if user and user.email:
            token = user.get_reset_token()
            reset_link = url_for(
               "reset_password",
               token=token,
               _external=True 
            )
            
            print("USER EMAIL:", repr(user.email))
            print("DEFAULT SENDER:", repr(app.config["MAIL_DEFAULT_SENDER"]))
            
            msg = Message(
                subject="password_reset",
                recipients= [user.email],
                body=f"Hi {user.username}\n\n To reset this password, click this link {reset_link}\n\nIf you didn't request it ignore this message."
            )
            mail.send(msg)
            
            # TODO: send reset_link via email here
            
            flash("if an account with that email exists, a reset link has been sent.\nClick the link sent via email.",category="success")
            
            return redirect(url_for('login'))
    
    return render_template("forgot.html")


@app.route("/reset_password/<token>",methods=["GET","POST"])
def reset_password(token):
    user = Users.verify_reset_token(token)
    
    if not user:
        flash("invalid or expired token!",category="danger")
        
        return redirect(url_for("forgot_password"))
    
    if request.method == "POST":
        password = request.form.get("password")
        password1 = request.form.get("password1")
        
        
        if password != password1:
            flash("both passwords must be same",category="danger")
            
            return redirect(request.url)
        
        user.password = generate_password_hash(password)
        db.session.commit()
        
        flash("password reset successful, you can now login",category="success")
        
        return redirect(url_for("login"))
    
    return render_template("reset_password.html",token=token)



@app.route("/dashboard",methods=["POST","GET"])
@login_required
def dashboard():
    items = Users.query.all()
    
    return render_template("dashboard.html",items=items)


@app.route("/download", methods=["POST"])
@login_required
def download():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    def download_video_in_background(app, url, user_id):
        with app.app_context():
            try:
                # Mark as downloading
                video = History(
                    url=url,
                    title="Downloading...",
                    filename="",
                    user_id=user_id,
                    status="downloading"
                )
                db.session.add(video)
                db.session.commit()

                video_data = download_youtube_video(url=url)
                # Update with actual info
                video.title = video_data["title"]
                video.filename = video_data["filename"]
                video.status = "completed"
                db.session.commit()
            except Exception as e:
                video.status = "failed"
                db.session.commit()
                print("Download failed:", e)
                

    thread = threading.Thread(target=download_video_in_background, args=(app, url, current_user.id))
    thread.start()


    return jsonify({"message": "Download started"})

    #flash("Download started in the background, you can continue using the app.",category="success")
    
    #return redirect(url_for("dashboard"))
        


@app.route("/history",methods=["GET","POST"])
@login_required
def history():
    urls = History.query.filter_by(user_id=current_user.id).all()
    
    return render_template("history.html",urls=urls)
    
@app.route("/download_status")
@login_required
def download_status():
    downloading = History.query.filter_by(user_id=current_user.id, status="downloading").count()
    return jsonify({"downloading": downloading})

    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
