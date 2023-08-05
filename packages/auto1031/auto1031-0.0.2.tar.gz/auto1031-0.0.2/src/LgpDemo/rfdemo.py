class RfDemo(object):

#     ROBOT_LIBRARY_VERSION = 1.0

    def __init__(self):
        pass

    def Base_64(self,PATH,IMGNAME):
        file_path = os.path.join(PATH,IMGNAME) #获取base_dir+'/image'文件夹内的文件
        f=open(file_path,'rb') #二进制方式打开图文件
        lsReadImage_f=base64.b64encode(f.read())#读取文件内容，转换为base64编码
        f.close()#关闭文件
        return    lsReadImage_f
