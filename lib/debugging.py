from datetime import datetime

class Logger:
    debug_file = None

    def start_logging(self):
        if self.debug_file is None:
            try:
                self.debug_file = open("debug.log", "a+")
            except:
                print("Cannot open file for debugging.")

    def end_logging(self):
        if not self.debug_file is None:
            self.debug_file.close()
            self.debug_file = None        

    def log(self, msg):
        if not self.debug_file is None:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.debug_file.write(''.join(['(', now, '): ', str(msg), '\n']))
            self.debug_file.flush()
