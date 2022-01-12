from base64 import b64encode

from flask import Flask, render_template, send_file, request
from flask_mail import Mail, Message
from ColorTransfer import ColorTranseferer
import io


app = Flask(__name__)
app.config.from_pyfile('Config.py')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('input.html', image='empty', alert='')

@app.route('/transferDownload', methods=['POST'])
def transfer_download():
    initial_photo, photo_to_color_transfer, metric = get_data_for_transfer()
    if not initial_photo:
        return render_template('input.html', image='empty', alert='Вставьте фото, на которое нужно перенести цвет')
    if not photo_to_color_transfer:
        return render_template('input.html', image='empty', alert='Вставьте фото, с которого нужно перенести цвет')
    transferer = ColorTranseferer(initial_photo, photo_to_color_transfer)
    img_str = transferer.transfer_color(method=metric)

    out_bytes = io.BytesIO()
    out_bytes.write(img_str)
    out_bytes.seek(0)
    return send_file(
        out_bytes,
        as_attachment=True,
        attachment_filename='image.jpeg',
        mimetype='image/jpeg'
    )

@app.route('/transfer', methods=['POST'])
def transfer():
    initial_photo, photo_to_color_transfer, metric = get_data_for_transfer()
    if not initial_photo:
        return render_template('input.html', image='empty', alert='Вставьте фото, на которое нужно перенести цвет')
    if not photo_to_color_transfer:
        return render_template('input.html', image='empty', alert='Вставьте фото, с которого нужно перенести цвет')
    transferer = ColorTranseferer(initial_photo, photo_to_color_transfer)
    img_str = transferer.transfer_color(method=metric)
    img = b64encode(img_str).decode("utf-8")
    return render_template('input.html', image=img, alert='')

@app.route('/transferSendEmail', methods=['POST'])
def transfer_send_email():
    initial_photo, photo_to_color_transfer, metric = get_data_for_transfer()
    if not initial_photo:
        return render_template('input.html', image='empty', alert='Вставьте фото, на которое нужно перенести цвет')
    if not photo_to_color_transfer:
        return render_template('input.html', image='empty', alert='Вставьте фото, с которого нужно перенести цвет')
    username = request.form['Username']
    server = request.form['Server']
    if not username or not server:
        return render_template('input.html', image='empty', alert='Введите корректную почту')
    target_email = f'{username}@{server}'
    transferer = ColorTranseferer(initial_photo, photo_to_color_transfer)
    img_str = transferer.transfer_color(method=metric)

    message = Message('Send Mail tutorial!',
        sender='victorgrefff@gmail.com',
        recipients=[target_email],
        body='Your picture with transefed color!\n\nBest wishes, Androsov Dmitri')
    message.attach('result_image.jpeg', 'result_image/jpeg', img_str)
    mail.send(message)
    return render_template('input.html', image='empty', alert=f'Обработанное фото отправлено на почту {target_email}')


def get_data_for_transfer():
    initial_photo = request.files['initial_photo'].read()
    photo_to_color_transfer = request.files['photo_to_color_transfer'].read()
    method = request.form['metric']

    # Выбираем метрику, по которой смотрим расстояния между изображениями
    if method == 'linear':
        metric = 'C_1'
    else:
        metric = 'C_2'
    return initial_photo, photo_to_color_transfer, metric


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
