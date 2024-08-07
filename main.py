from flask import Flask, render_template, request, send_file, session
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)
app.secret_key = 'huehuehuehuehue'  
@app.route('/')
def home():
  
    session.pop('qrcode_image', None)
    return render_template('index.html', data=None)

@app.route('/', methods=['POST'])
def generateQR():
    memory = BytesIO()
    data = request.form.get('link')
    img = qrcode.make(data)
    img.save(memory, 'PNG')  
    memory.seek(0)  

    base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')

    session['qrcode_image'] = memory.getvalue()

    return render_template('index.html', data=base64_img)

@app.route('/download')
def download():
    image_data = session.get('qrcode_image')
    if image_data:
        memory = BytesIO(image_data)
        memory.seek(0)
        return send_file(memory, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    return "No image to download", 404

if __name__ == '__main__':
    app.run(debug=True)
