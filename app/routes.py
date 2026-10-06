import io
import csv
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, Response
from .models import db, User, Ticket
from .services.analytics import clean_dataframe, kpis, grouped_counts
from .services.ml import predict_sentiment

bp = Blueprint('main', __name__)


def logged_in():
    return session.get('user_id') is not None

@bp.route('/')
def index():
    if not logged_in():
        return redirect(url_for('main.login'))
    return redirect(url_for('main.dashboard'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
def dashboard():
    if not logged_in(): return redirect(url_for('main.login'))
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('dashboard.html', kpis=kpis(tickets), tickets=tickets[:8], categories=grouped_counts(tickets, 'category'), sentiments=grouped_counts(tickets, 'sentiment'), statuses=grouped_counts(tickets, 'status'))

@bp.route('/tickets')
def tickets():
    if not logged_in(): return redirect(url_for('main.login'))
    q = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()
    query = Ticket.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(Ticket.subject.ilike(like), Ticket.customer_name.ilike(like), Ticket.description.ilike(like)))
    if status:
        query = query.filter_by(status=status)
    return render_template('tickets.html', tickets=query.order_by(Ticket.created_at.desc()).all(), q=q, status=status)

@bp.route('/ticket/new', methods=['GET','POST'])
def new_ticket():
    if not logged_in(): return redirect(url_for('main.login'))
    if request.method == 'POST':
        description = request.form['description'].strip()
        sentiment = predict_sentiment(description)
        priority = 'High' if sentiment == 'Negative' else ('Low' if sentiment == 'Positive' else 'Medium')
        ticket = Ticket(customer_name=request.form['customer_name'], customer_email=request.form['customer_email'], subject=request.form['subject'], description=description, category=request.form.get('category','Other'), sentiment=sentiment, priority=priority, status='Open', csat=0, response_time_hours=0, resolution_time_hours=0)
        db.session.add(ticket); db.session.commit()
        flash(f'Ticket created. AI sentiment: {sentiment}; suggested priority: {priority}.', 'success')
        return redirect(url_for('main.tickets'))
    return render_template('ticket_form.html')

@bp.route('/ticket/<int:ticket_id>/status', methods=['POST'])
def update_status(ticket_id):
    if not logged_in(): return redirect(url_for('main.login'))
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = request.form['status']
    db.session.commit()
    flash('Ticket status updated.', 'success')
    return redirect(request.referrer or url_for('main.tickets'))

@bp.route('/upload', methods=['GET','POST'])
def upload():
    if not logged_in(): return redirect(url_for('main.login'))
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename:
            flash('Please select a CSV or Excel file.', 'danger'); return redirect(url_for('main.upload'))
        try:
            import pandas as pd
            df = pd.read_csv(file) if file.filename.lower().endswith('.csv') else pd.read_excel(file)
            df = clean_dataframe(df)
            count = 0
            for _, r in df.iterrows():
                db.session.add(Ticket(customer_name=r.customer_name, customer_email=r.customer_email, subject=r.subject, description=r.description, category=r.category or 'Other', sentiment=r.sentiment or predict_sentiment(r.description), priority=r.priority or 'Medium', status=r.status or 'Open', csat=float(r.csat), response_time_hours=float(r.response_time_hours), resolution_time_hours=float(r.resolution_time_hours)))
                count += 1
            db.session.commit()
            flash(f'Successfully imported {count} tickets.', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as exc:
            db.session.rollback(); flash(str(exc), 'danger')
    return render_template('upload.html')

@bp.route('/api/kpis')
def api_kpis():
    tickets = Ticket.query.all()
    return jsonify(kpis(tickets))

@bp.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json(silent=True) or {}
    text = str(data.get('text', '')).strip()
    if not text: return jsonify({'error':'text is required'}), 400
    sentiment = predict_sentiment(text)
    priority = 'High' if sentiment == 'Negative' else ('Low' if sentiment == 'Positive' else 'Medium')
    return jsonify({'sentiment': sentiment, 'suggested_priority': priority})

@bp.route('/export')
def export():
    if not logged_in(): return redirect(url_for('main.login'))
    output = io.StringIO(); writer = csv.writer(output)
    writer.writerow(['id','customer_name','customer_email','subject','description','category','sentiment','priority','status','csat','response_time_hours','resolution_time_hours'])
    for t in Ticket.query.order_by(Ticket.id).all():
        writer.writerow([t.id,t.customer_name,t.customer_email,t.subject,t.description,t.category,t.sentiment,t.priority,t.status,t.csat,t.response_time_hours,t.resolution_time_hours])
    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition':'attachment; filename=support_tickets.csv'})
