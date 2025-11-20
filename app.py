from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from iching import IChing
from llm_service import LLMService
from models import db, User, Consultation
from forms import LoginForm, RegistrationForm, ConsultationForm, NoteForm
import os
from dotenv import load_dotenv
import markdown

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_for_session")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iching.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

iching = IChing()
# Initialize LLM service lazily or handle error if key is missing
try:
    llm_service = LLMService()
except ValueError:
    llm_service = None
    print("Warning: GEMINI_API_KEY not set. LLM features will not work.")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ConsultationForm()
    if form.validate_on_submit():
        session['question'] = form.question.data
        session['subject'] = form.subject.data
        session['language'] = form.language.data
        return redirect(url_for('cast'))
    return render_template('index.html', form=form)

@app.route('/cast')
@login_required
def cast():
    question = session.get('question')
    # subject and language are also in session
    if not question:
        return redirect(url_for('index'))
    
    result = iching.cast_hexagram()
    session['cast_result'] = result
    
    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    question = session.get('question')
    subject = session.get('subject')
    language = session.get('language', 'English')
    cast_result = session.get('cast_result')
    
    if not question or not cast_result:
        return redirect(url_for('index'))
    
    interpretation = None
    if llm_service:
        try:
            # Check if we already have an interpretation in session to avoid re-generating on refresh
            # Ideally, we should save to DB immediately.
            # Let's generate if not present.
            raw_interpretation = llm_service.interpret_hexagram(question, cast_result, language)
            interpretation = markdown.markdown(raw_interpretation)
            
            # Save to DB
            consultation = Consultation(
                author=current_user,
                question=question,
                subject=subject,
                interpretation=interpretation
            )
            consultation.set_hexagram_data(cast_result)
            db.session.add(consultation)
            db.session.commit()
            
            # Clear session data to prevent re-submission
            session.pop('question', None)
            session.pop('subject', None)
            session.pop('cast_result', None)
            
            # Redirect to the consultation detail view to show the result
            return redirect(url_for('consultation', id=consultation.id))

        except Exception as e:
            interpretation = f"<p>Error generating interpretation: {str(e)}</p>"
    else:
        interpretation = "<p>LLM Service not configured. Please set GEMINI_API_KEY.</p>"

    # Fallback if error
    return render_template('result.html', 
                           question=question, 
                           cast_result=cast_result, 
                           interpretation=interpretation)

@app.route('/consultation/<int:id>', methods=['GET', 'POST'])
@login_required
def consultation(id):
    consultation = Consultation.query.get_or_404(id)
    if consultation.author != current_user:
        return redirect(url_for('index'))
    
    form = NoteForm()
    if form.validate_on_submit():
        consultation.notes = form.notes.data
        db.session.commit()
        flash('Notes saved.')
        return redirect(url_for('consultation', id=consultation.id))
    elif request.method == 'GET':
        form.notes.data = consultation.notes

    return render_template('result.html', 
                           consultation=consultation,
                           form=form)

@app.route('/history')
@login_required
def history():
    # Group by subject
    consultations = current_user.consultations.order_by(Consultation.timestamp.desc()).all()
    history_data = {}
    for c in consultations:
        subj = c.subject or "General"
        if subj not in history_data:
            history_data[subj] = []
        history_data[subj].append(c)
    
    return render_template('history.html', history_data=history_data)

if __name__ == '__main__':
    app.run(debug=True)
