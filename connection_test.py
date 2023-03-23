# 测试连接状态
import poplib

# 账户信息
email = 'your email address'
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
