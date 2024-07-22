from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import difflib

def filter_and_generate_pdf(file1_path, file2_path, output1_path, output2_path, pdf_output_path):
    i = 0
    # Read the files
    with open(file1_path, 'r') as file:
        file1_lines = file.readlines()

    with open(file2_path, 'r') as file:
        file2_lines = file.readlines()

    # Extract matriculas
    file1_matriculas = {line.split(',')[0].split(':')[1].strip() for line in file1_lines}
    file2_matriculas = {line.split(',')[0].split(':')[1].strip() for line in file2_lines}

    # Find common and unique matriculas
    common_matriculas = file1_matriculas.intersection(file2_matriculas)
    only_in_file1 = file1_matriculas - file2_matriculas
    only_in_file2 = file2_matriculas - file1_matriculas

    # Filter lines
    filtered_file1_lines = [line for line in file1_lines if line.split(',')[0].split(':')[1].strip() in common_matriculas]
    filtered_file2_lines = [line for line in file2_lines if line.split(',')[0].split(':')[1].strip() in common_matriculas]

    # Save filtered lines to new files
    with open(output1_path, 'w') as file:
        file.writelines(filtered_file1_lines)

    with open(output2_path, 'w') as file:
        file.writelines(filtered_file2_lines)

    # Generate PDF report
    c = canvas.Canvas(pdf_output_path, pagesize=letter)
    width, height = letter
    y_position = height - 40
    line_height = 14

    c.drawString(40, y_position, "Matrículas Retiradas:")
    y_position -= line_height

    c.drawString(40, y_position, "Presentes no sigp mas faltando no vitruvio:")
    y_position -= line_height

    for matricula in only_in_file1:
        c.drawString(60, y_position, matricula)
        y_position -= line_height
        i+=1
        if i >= 50:
            c.showPage()
            y_position = height - 40
            line_height = 14
            c.drawString(40, y_position, "Matrículas Retiradas:")
            y_position -= line_height

            c.drawString(40, y_position, "Presentes no sigp mas faltando no vitruvio:")
            y_position -= line_height

            i = 0

    if not only_in_file1:
        c.drawString(60, y_position, "Nenhuma")
        y_position -= line_height
        

    

    c.save()

# Usage
file1_path = 'saida/entrada_sigp.txt'
file2_path = 'saida/entrada_vitruvio.txt'
output1_path = 'saida/filtered_entrada_sigp.txt'
output2_path = 'saida/filtered_entrada_vitruvio.txt'
pdf_output_path = 'resultados/matriculasFaltandonNoVitruvio.pdf'

filter_and_generate_pdf(file1_path, file2_path, output1_path, output2_path, pdf_output_path)
