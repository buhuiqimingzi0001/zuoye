import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'zuoye.settings'

if __name__ == '__main__':
    # send_mail(
    #     'mafuyu',
    #     'shiina_mafuyu',
    #     'songfu01@sina.com',
    #     ['songfu01@126.com'],
    # )
    subject,from_email,to = '有什么问题，请用下面的网站来解决','songfu01@sina.com','songfu01@126.com'
    text_content = '你不会百度吗 '
    html_content = '<p>请去百度 <a  href="https://www.baidu.com/">点击</a></p> '
    msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    msg.attach_alternative(html_content,'text/html')
    msg.send()