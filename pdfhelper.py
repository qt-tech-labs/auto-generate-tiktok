from operator import contains
from PDFMark import PDFMark as FPDF
class PDF(FPDF):
    pdf_w=210
    pdf_h=297

    def build_body(self, contents):
        indx = 0
        for ques, answer in contents:
            indx += 1
            self.question(str(indx) + ". " + ques, answer)

    def question(self, question, answer):
        # "string", ["", "", "", ""]
        print("doing " + question)
        if len(answer) < 4 :
            return
        # self.set_font('Times', '', 15)
        self.multi_cell(0, 5, question)
        self.ln()
        # caculate the width of the answers
        # self.set_font('Times', '', 12)
        # w1 = self.get_string_width(answer[0])
        # w2 = self.get_string_width(answer[1])
        # w3 = self.get_string_width(answer[2])
        # w4 = self.get_string_width(answer[3])

        # space = (self.pdf_w - (w1 + w2 + w3 + w4))/3
        
        for indx, anws in enumerate(answer):
            self.cell(self.get_string_width(anws), 0, anws)
            if indx != 3:
                self.cell(20)
        self.ln(5)
        
