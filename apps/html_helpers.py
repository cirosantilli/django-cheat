class Row():

    def __init__(self,content,attrs={}):
        self.cols = cols

class Column():

    def __init__(self,rows,attrs={}):
        self.cols = cols

class Table():

    def __init__(self,cols,attrs={}):
        self.cols = cols

    def render():

        output = []

        output.append('<table>')

        if self.cols[0].header:
            output.append('<thead><tr>')
            for col in self.cols:
                output.append(col.render_header())
            output.append('</thead>')

        output.append('<tbody>')
        for i in xrange(len(self.cols[0].rows)):
            for col in self.cols:
                output.append('<tr>')
                output.append(col.rows[i].render())
                output.append('</tr>')
        output.append('<tbody>')

        output.append('<tfoot>')
        for i in xrange(len(self.cols[0].footer_rows)):
            for col in self.cols:
                output.append('<tr>')
                output.append(col.footer_rows[i].render())
                output.append('</tr>')
        output.append('<tfoot>')

        output.append('</tr></table>')

        return '\n'.join(output)


