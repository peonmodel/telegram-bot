from docx import Document

#Sample Input needed
#project information
project_ref = "A1234-00001-2021"
project_title = "MMT Kranji Loop"
date_inspection = "07/08/2022"
time_inspection = "10:35"
inspector = "Ms Lee"
designation = "Site supervisor"
reviewer = "Mr Ong"
approver = "Ms Chen"
filename = "inspection report"

#Inspection information
qty = [1,2,3]
photo = ["photo 1","photo 2","photo 3"]
description = ["desc 1","desc 2","desc 3"]
remarks =["remark 1","remark 2","remark 3"]

document = Document()

document.add_heading('Inspection Checklist', 0)

document.add_paragraph('Project reference:\t {}'.format(project_ref))
document.add_paragraph('Project title:\t\t {}'.format(project_title))
document.add_paragraph('Date:\t\t\t {}'.format(date_inspection))
document.add_paragraph('Time:\t\t\t {}'.format(time_inspection))
document.add_paragraph('Inspector name:\t {}'.format(inspector))
document.add_paragraph('Designation:\t\t {}'.format(designation))
document.add_paragraph('\n')

table = document.add_table(rows=1, cols=4)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'S/N'
hdr_cells[1].text = 'Photos'
hdr_cells[2].text = 'Description'
hdr_cells[3].text = 'Remarks'

for qty, photo, desc, remark in zip(qty, photo, description, remarks):
    row_cells = table.add_row().cells
    row_cells[0].text = str(qty)
    row_cells[1].text = photo
    row_cells[2].text = desc
    row_cells[3].text = remark

document.add_paragraph('\n')

document.add_paragraph('Submitted by:\t {}'.format(inspector))
document.add_paragraph('Reviewed by:\t {}'.format(reviewer))
document.add_paragraph('Approved by:\t {}'.format(approver))

document.save('{}.docx'.format(filename))

save_pdf = input("Do you want to save the report as PDF? (Y/N)")
save_pdf = save_pdf.upper()

if save_pdf == "Y":
    import docx2pdf 
    word_file ='{}.docx'.format(filename)
    pdf_file = '{}.pdf'.format(filename)
    with open(pdf_file, "wb") as f:
        pass
    docx2pdf.convert(word_file, pdf_file)
    print("Inspection report saved as {}.pdf.".format(filename))
else:
    print ("Please review the drafted inspection report.")
