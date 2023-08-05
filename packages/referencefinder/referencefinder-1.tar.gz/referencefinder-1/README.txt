* this is basic tools for finding reference in papers         

Usage        
=====         
  >>> from ReferenceFinder import ReferenceUtils   
  >>> docx_file_path = 'paper.docx'   
  >>> result_file_path = 'final_reference_result.txt'    
  >>> ref_finder = ReferenceUtils()   
  >>> ref_finder.find_references(docx_file_path, result_file_path)   
  >>> print('find references complete  !!!!!!')    
