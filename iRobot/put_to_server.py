import paramiko  # 用于调用scp命令
from scp import SCPClient
class Server():
    def __init__(self):
        host = "111.230.59.85"  # 服务器ip地址
        port = 22  # 端口号
        username = "root"  # ssh 用户名
        password = "irobot@kexie#215"  # 密码
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh_client.connect(host, port, username, password)
        self.chan = self.ssh_client.invoke_shell()
        self.scpclient = SCPClient(self.chan.get_transport(), socket_timeout=15.0)
    def upload_img(self, img_path="./data/1.jpg", remote_path="/var/www/html"):
        try:
            self.scpclient.put(img_path, remote_path)
        except FileNotFoundError as e:
            print(e)
            print("系统找不到指定文件" + img_path)
       
        self.chan.close()
if __name__ == '__main__':
    server = Server()
    for i in range(10):
        server.upload_img()
