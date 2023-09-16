import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.notification import NotificationCreateSchema
from server.oldsrc.core.models.user import User
from server.oldsrc.core.settings import Tags, NOTIFICATIONS_ROUTER_PREFIX, email_config, RoleType
from server.oldsrc.core.utils.auth import GetCurrentUser
from server.oldsrc.core.utils.db import get_db

router = APIRouter(prefix=NOTIFICATIONS_ROUTER_PREFIX, tags=[Tags.NOTIFICATIONS])


@router.post('/')
async def create(notification_data: NotificationCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,)))):
    user = await User.by_id(db, notification_data.user_id)

    host = 'smtp.mail.ru'
    port = 587
    username = email_config['ADDRESS']
    password = email_config['PASSWORD']
    subject = 'Foggie уведомление'
    from_addr = email_config['ADDRESS']

    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = user.email
    message['Subject'] = Header(subject, 'utf-8')

    body = MIMEText(notification_data.content, 'plain', 'utf-8')
    message.attach(body)

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr, user.email, message.as_string())
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Email sending failed. Error message: {str(e)}')
