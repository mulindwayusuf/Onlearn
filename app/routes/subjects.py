from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import SubjectForm
from app.models import Subject, db

subjects = Blueprint('subjects', __name__)

@subjects.route('/create_subject', methods=['GET', 'POST'])
@login_required
def create_subject():
    if current_user.role != 'Instructor':
        flash('You are not authorized to create subjects.', 'danger')
        return redirect(url_for('main.index'))
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(title=form.title.data, description=form.description.data, instructor_id=current_user.id)
        db.session.add(subject)
        db.session.commit()
        flash('Subject created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_subject.html', form=form)

@subjects.route('/course/<int:course_id>')
def subject_detail(course_id):
    subject = Subject.query.get_or_404(course_id)
    return render_template('course_detail.html', subject=subject)
