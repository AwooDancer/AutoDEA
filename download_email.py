# _*_ coding: utf-8 _*_


import poplib
import email
import os
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


# 防止汉字乱码
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        if charset == 'gb2312':
            charset = 'gb18030'
        value = value.decode(charset)
    return value


def get_email_headers(msg):
    headers = {}
    for header in ['From', 'To', 'Cc', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            # 发件人
            if header == 'From':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                from_addr = u'%s <%s>' % (name, addr)
                headers['From'] = from_addr
            # 收件人
            if header == 'To':
                all_cc = value.split(',')
                to = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    to_addr = u'%s <%s>' % (name, addr)
                    to.append(to_addr)
                headers['To'] = ','.join(to)
            # 抄送
            if header == 'Cc':
                all_cc = value.split(',')
                cc = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    cc_addr = u'%s <%s>' % (name, addr)
                    cc.append(to_addr)
                headers['Cc'] = ','.join(cc)
            # 主题
            if header == 'Subject':
                subject = decode_str(value)
                headers['Subject'] = subject
            # 时间
            if header == 'Date':
                headers['Date'] = value
    return headers


# 下载附件
def get_email_content(message, save_path):
    attachments = []
    # 遍历
    for part in message.walk():
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            abs_filename = os.path.join(save_path, filename)
            attach = open(abs_filename, 'wb')
            attachments.append(filename)
            attach.write(data)
            attach.close()
    return attachments


if __name__ == '__main__':
    # 邮箱
    email = 'your email address'
    # 授权码
    password = 'authorization code'
    pop3_server = 'pop.xx.com'
    # 连接到POP3服务器，带SSL的:
    server = poplib.POP3_SSL(pop3_server)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(0)
    # POP3服务器的欢迎文字:
    print(server.getwelcome())
    # 身份认证:
    server.user(email)
    server.pass_(password)
    # stat()返回邮件数量和占用空间:
    msg_count, msg_size = server.stat()
    print('message count:', msg_count)
    print('message size:', msg_size, 'bytes')
    print('-----------------------------')
    # b'+OK 237 174238271' list()响应的状态/邮件数量/邮件占用的空间大小
    resp, mails, octets = server.list()

    for i in range(1, msg_count):
        resp, byte_lines, octets = server.retr(i)
        # 转码
        str_lines = []
        for x in byte_lines:
            str_lines.append(x.decode())
        # 拼接邮件内容
        msg_content = '\n'.join(str_lines)
        # 把邮件内容解析为Message对象
        msg = Parser().parsestr(msg_content)
        headers = get_email_headers(msg)
        # 附件保存位置
        attachments = get_email_content(msg, r'store location')

        print('subject:', headers['Subject'])
        print('from:', headers['From'])
        print('to:', headers['To'])
        if 'cc' in headers:
            print('cc:', headers['Cc'])
        print('date:', headers['Date'])
        print('attachments: ', attachments)
        print('-----------------------------')

    server.quit()
