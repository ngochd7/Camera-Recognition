from datetime import datetime
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendEmailNotify(photoDir):
    fromaddr = "nguyendinhhdpv3@gmail.com"
    toaddr = "nguyenngochdpv3@gmail.com"

    msg = MIMEMultipart()    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Thông báo phát hiện người lạ" 

    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    
    body = "Camera đã phát hiện người lạ vào lúc: "+ dtString + " và đây là ảnh của người đó:"
    html = """\
    <html>
        <body>
            <img src="cid:Mailtrapimage">
        </body>
    </html>
    """
    try:
        msg.attach(MIMEText(body, 'plain'))
        part = MIMEText(html, 'html')
        msg.attach(part)
        fp = open(str(photoDir), 'rb')
        image = MIMEImage(fp.read())
        fp.close()

        image.add_header('Content-ID', '<Mailtrapimage>')
        msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "Ngochd24gma@")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    sendEmailNotify("/Users/ngoc/Downloads/photo/co_gai.jpeg")