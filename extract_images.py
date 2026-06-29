from PyPDF2 import PdfReader
import os

output_dir = r'C:\Users\Admin\Documents\StartCarePPEC\extracted_images'
os.makedirs(output_dir, exist_ok=True)

for pdf_name in ['BROCHURE 1.pdf', 'STARTCARE MATERIAL.pdf']:
    filepath = os.path.join(r'C:\Users\Admin\Documents\StartCarePPEC', pdf_name)
    r = PdfReader(filepath)
    print(f'=== {pdf_name} ===')
    print(f'Pages: {len(r.pages)}')
    
    for i, page in enumerate(r.pages):
        if '/Resources' in page and '/XObject' in page['/Resources']:
            xobjects = page['/Resources']['/XObject']
            for name in xobjects:
                obj = xobjects[name].get_object()
                subtype = obj.get('/Subtype')
                if str(subtype) == '/Image':
                    w = obj.get('/Width')
                    h = obj.get('/Height')
                    filt = obj.get('/Filter')
                    print(f'  Page {i+1}, Image {name}: {w}x{h}, filter={filt}')
                    
                    data = obj.get_data()
                    safe_name = pdf_name.replace(' ', '_').replace('.pdf', '')
                    
                    if str(filt) == '/DCTDecode':
                        ext = '.jpg'
                    elif str(filt) == '/FlateDecode':
                        ext = '.png'
                    elif str(filt) == '/JPXDecode':
                        ext = '.jp2'
                    else:
                        ext = '.bin'
                    
                    outfile = os.path.join(output_dir, f'{safe_name}_p{i+1}_{name.strip("/")}{ext}')
                    with open(outfile, 'wb') as f:
                        f.write(data)
                    print(f'    Saved: {outfile}')

print('\nDone!')
