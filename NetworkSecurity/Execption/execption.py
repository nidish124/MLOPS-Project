import sys
class Custom_execption(Exception):
    def __init__(self, error_message, error:sys):
        super().__init__(error_message)
        self.error_message = error_message
        _,_,err_tb = error.exc_info()

        self.line_no = err_tb.tb_lineno
        self.file_name = err_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"*****'{self.error_message}' at line '{self.line_no}' in '{self.file_name}'******"



    