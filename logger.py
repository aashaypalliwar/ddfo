
class Logger:
    
    log_folder = "/home/aashay/cupboard/ddfo/data/ddfo_exps/logs/"
    
    def __init__(self, filename):
        self.file = open(self.log_folder + filename, 'a', newline='', encoding='utf8')
        
        
    def close(self):
        self.file.close()
        
    def log(self, line):
        self.file.write(line + "\n")
        print(line)
        
    def flush(self):
        self.file.flush()