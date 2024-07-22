from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from app import app, db
from models import User, Printer, NormalUserData, DSUUserData, RMScannerUserData, user_printer
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from datetime import datetime
import sqlalchemy.exc

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Admin routes
@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def manage_users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        new_user = User(username=username, password=password, role=role)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully', 'success')
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('User already exists or there was an integrity error', 'danger')
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/admin/users/<int:id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_users'))

@app.route('/admin/users/<int:id>/reset_password', methods=['POST'])
@login_required
@role_required('Admin')
def reset_password(id):
    user = User.query.get_or_404(id)
    new_password = request.form['password']
    user.password = new_password
    db.session.commit()
    flash('Password reset successfully', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/printers', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def manage_printers():
    if request.method == 'POST':
        name = request.form['name']
        new_printer = Printer(name=name)
        try:
            db.session.add(new_printer)
            db.session.commit()
            flash('Printer added successfully', 'success')
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Printer already exists or there was an integrity error', 'danger')
    printers = Printer.query.all()
    users = User.query.all()
    return render_template('manage_printers.html', printers=printers, users=users)

@app.route('/admin/printers/assign', methods=['POST'])
@login_required
@role_required('Admin')
def assign_printer():
    printer_id = request.form['printer_id']
    user_id = request.form['user_id']
    printer = Printer.query.get(printer_id)
    user = User.query.get(user_id)
    if printer and user:
        user.printers.append(printer)
        db.session.commit()
        flash(f'Printer {printer.name} assigned to {user.username}', 'success')
    else:
        flash('Failed to assign printer', 'danger')
    return redirect(url_for('manage_printers'))

@app.route('/admin/printers/<int:id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_printer(id):
    printer = Printer.query.get_or_404(id)
    db.session.delete(printer)
    db.session.commit()
    return redirect(url_for('manage_printers'))

@app.route('/admin/backup', methods=['POST'])
@login_required
@role_required('Admin')
def backup():
    subprocess.call(['./backup_script.sh'])
    return jsonify({'message': 'Backup initiated successfully'}), 200

@app.route('/admin/reset', methods=['POST'])
@login_required
@role_required('Admin')
def reset():
    preserve_all = request.json.get('preserve_all', False)
    reset_database(preserve_all)
    return jsonify({'message': 'Database reset successfully'}), 200

# Normal user routes
@app.route('/scan_barcode', methods=['GET', 'POST'])
@login_required
@role_required('Normal')
def scan_barcode():
    if request.method == 'POST':
        user_id = current_user.id
        barcode = request.form['barcode']
        existing_entry = NormalUserData.query.filter_by(barcode=barcode).first()
        if existing_entry:
            return jsonify({
                'status': 'error',
                'message': f"Barcode {barcode} has already been scanned by {existing_entry.user.username} in pallet {existing_entry.pallet_number} on {existing_entry.timestamp}"
            })
        else:
            pallet_number = f"{current_user.username}/{request.form['pallet_number']}"
            new_entry = NormalUserData(user_id=user_id, barcode=barcode, pallet_number=pallet_number, timestamp=datetime.utcnow())
            db.session.add(new_entry)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': f"Barcode {barcode} successfully scanned in pallet {pallet_number}",
                'entry': {
                    'id': new_entry.id,
                    'barcode': barcode,
                    'timestamp': new_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
    return render_template('scan_barcode.html')

@app.route('/next_pallet', methods=['POST'])
@login_required
@role_required('Normal')
def next_pallet():
    # Logic to handle next pallet
    return jsonify({
        'status': 'success',
        'message': 'Pallet finalized and new pallet started'
    })

@app.route('/delete_scan/<int:id>', methods=['POST'])
@login_required
@role_required('Normal')
def delete_scan(id):
    entry = NormalUserData.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Entry deleted successfully'})

# DSU user routes
@app.route('/handle_duplicates', methods=['GET', 'POST'])
@login_required
@role_required('DSU')
def handle_duplicates():
    if request.method == 'POST':
        user_id = current_user.id
        barcode = request.form['barcode']
        pallet_number = f"{current_user.username}/{request.form['pallet_number']}"
        new_entry = DSUUserData(user_id=user_id, barcode=barcode, pallet_number=pallet_number, timestamp=datetime.utcnow())
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f"Barcode {barcode} successfully scanned in pallet {pallet_number}",
            'entry': {
                'id': new_entry.id,
                'barcode': barcode,
                'timestamp': new_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    return render_template('handle_duplicates.html')

@app.route('/edit_delete_data', methods=['GET'])
@login_required
@role_required('DSU')
def edit_delete_data():
    return render_template('edit_delete_data.html')

@app.route('/dsu_print_label', methods=['GET', 'POST'])
@login_required
@role_required('DSU')
def dsu_print_label():
    return render_template('dsu_print_label.html')

@app.route('/dsu_user_data', methods=['POST'])
@login_required
@role_required('DSU')
def add_dsu_user_data():
    user_id = current_user.id
    barcode = request.form['barcode']
    pallet_number = f"{current_user.username}/{datetime.utcnow().strftime('%Y%m%d%H%M%S')}/{request.form['pallet_number']}"
    new_entry = DSUUserData(user_id=user_id, barcode=barcode, pallet_number=pallet_number)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Data added successfully'}), 200

@app.route('/dsu_user_print_label', methods=['POST'])
@login_required
@role_required('DSU')
def dsu_user_print_label():
    part_number = request.form['part_number']
    printer_name = request.form.get('printer_name', 'YOUR_PRINTER_NAME')
    print_label(part_number, printer_name)
    return jsonify({'message': 'Label printed successfully'}), 200

# RM+WIP user routes
@app.route('/form_data_entry', methods=['GET', 'POST'])
@login_required
@role_required('RM+WIP')
def form_data_entry():
    if request.method == 'POST':
        user_id = current_user.id
        bobbin_number = request.form['bobbin_number']
        bobbin_type = request.form['bobbin_type']
        bobbin_size = request.form['bobbin_size']
        cu_size = request.form['cu_size']
        drawn_bunched = request.form['drawn_bunched']
        weight_kg = request.form['weight_kg']
        new_entry = RMScannerUserData(
            user_id=user_id,
            bobbin_number=bobbin_number,
            bobbin_type=bobbin_type,
            bobbin_size=bobbin_size,
            cu_size=cu_size,
            drawn_bunched=drawn_bunched,
            weight_kg=weight_kg,
            timestamp=datetime.utcnow()
        )
        duplicate_entry = RMScannerUserData.query.filter_by(bobbin_number=bobbin_number).first()
        if duplicate_entry:
            response_message = f"Data for bobbin number {bobbin_number} exists. As per previous recorded info by {duplicate_entry.user.username} on {duplicate_entry.timestamp}, it contains {duplicate_entry.cu_size}, {duplicate_entry.drawn_bunched}, {duplicate_entry.weight_kg} kg."
            return jsonify({'message': response_message, 'status': 'duplicate'}), 400

        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Data added successfully'}), 200
    return render_template('form_data_entry.html')

@app.route('/rm_print_label', methods=['POST'])
@login_required
@role_required('RM+WIP')
def rm_print_label():
    part_number = request.form['part_number']
    printer_name = request.form.get('printer_name', 'YOUR_PRINTER_NAME')
    print_label(part_number, printer_name)
    return jsonify({'message': 'Label printed successfully'}), 200

# Modify data route
@app.route('/modify_data', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def modify_data():
    # Add logic to modify data
    if request.method == 'POST':
        # Process modification
        pass
    return render_template('modify_data.html')
