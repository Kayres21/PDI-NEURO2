from fpdf import FPDF 


def make_pdf(tiempo, aciertos, nombre_archivo):
    
    pdf = FPDF()
    pdf.add_page()
    
    acierto = aciertos[0]
    total = aciertos[1]
    porcentaje_error = round((acierto/total)*100)
    
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(200,10 , 'Resultados', ln=1,align='C')
    
    pdf.set_font('Arial', size= 12)
    pdf.cell(200,10 , 'Tiempo de procesamiento: ' + str(round(tiempo)) + '[s]', ln=2,align='C')
    pdf.ln(10)
    pdf.cell(200,10 , 'Pisadas acertadas: ' + str(acierto),ln=3,  align='C')
    pdf.ln(10)
    pdf.cell(200,10 , 'Pisadas totales: ' + str(total) ,ln=4, align='C')
    pdf.ln(10)
    pdf.cell(200,10, 'Porcentaje acierto: ' + str(porcentaje_error) +'%', ln=5, align='C')
    
    
    
    
    pdf.output('resultados_' + nombre_archivo +'.pdf', 'F')
    