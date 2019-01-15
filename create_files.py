import string
import random
import json
import os


class create_file(object):

    def __init__(self,config):
        self.upload_path = 'upload_files'
        self.create_file = config['list']

    def create_all(self):
        self.check_dir()
        x = 0

        for self.file_size in self.create_file.keys():
            for i in range(self.create_file[self.file_size]):
                x += 1
                file_name = '{0}-{1}.txt'.format(self.file_size,x)
                print '{0} is created.'.format(file_name)
                self.create_one(file_name)

    def check_dir(self):
        listdir = os.listdir('.')

        if not (self.upload_path in listdir) and not os.path.isdir(self.upload_path):
            os.mkdir(self.upload_path)
            print 'Creating directory {0}'.format(self.upload_path)
        else:
            print 'Directory {0} already exists.'.format(self.upload_path)

    def create_one(self,file_name):
        size = self.file_size[0:-1]
        f_path = os.path.join(self.upload_path + '/', file_name)
        f = open(f_path,'wb')

        if 'K' in self.file_size:
            for i in range(int(size)):
                line = self._id_generator(gn_size = 1023)
                line = line + '\n'
                f.write(line)
        elif 'M' in self.file_size:
            for i in range(int(size)*1024):
                line = self._id_generator(gn_size = 1023)
                line = line + '\n'
                f.write(line)
        f.close()

    def create_file_server(self,times,file_type,file_name):
        for i in range(times):
            create_file_server_one(file_type,file_name)

    def create_file_server_one(self,file_type,file_name):
        size = file_type[0:-1]
        file_name = self.upload_path + '/' + file_name + '.txt'
        f = open(file_name,'wb')

        if 'K' in file_type:
            for i in range(int(size)):
                line = self._id_generator(gn_size = 1023)
                line = line + '\n'
                f.write(line)
        elif 'M' in file_type:
            for i in range(int(size) * 1024):
                line = self._id_generator(gn_size = 1023)
                line = line + '\n'
                f.write(line)
        else:
            raise Exception('No method..')
        f.close()

    def _id_generator(self, gn_size, chars = string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for z in range(gn_size))

if __name__ == "__main__":
    config = {}
    execfile("create_files.conf",config)
    test = create_file(config)
    test.create_all()
