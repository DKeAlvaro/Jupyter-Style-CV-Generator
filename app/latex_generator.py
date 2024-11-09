import os
import subprocess
from datetime import datetime

class JupyterCVGenerator:
    def __init__(self):
        self.template_header = r'''\documentclass{article}
\usepackage{graphicx} 
\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{mdframed}
\usepackage{hyperref}
\definecolor{urlcolor}{rgb}{0,.145,.698}
\definecolor{linkcolor}{rgb}{.71,0.21,0.01}
\definecolor{citecolor}{rgb}{.12,.54,.11}
\hypersetup{
  breaklinks=true,
  colorlinks=true,
  urlcolor=urlcolor,
  linkcolor=linkcolor,
  citecolor=citecolor,
  }
\definecolor{cellBackground}{RGB}{248,248,252}
\definecolor{pythonGreen}{RGB}{0,128,0}
\definecolor{pythonRed}{RGB}{184,49,47}
\definecolor{pythonBlue}{RGB}{0,0,255}
\definecolor{borderGray}{RGB}{230,230,230}
\lstset{
    language=Python,
    frame=none,
    backgroundcolor=\color{cellBackground},
    basicstyle=\ttfamily\normalsize,
    keywordstyle=\color{pythonBlue},
    commentstyle=\color{pythonGreen},
    stringstyle=\color{pythonRed},
    showstringspaces=false,
    moredelim=[s][\color{purple}]{@}{class},  
    classoffset=1,
    keywords={str,float},
    keywordstyle=\color{pythonGreen},
    classoffset=0,
    breaklines=true,
    breakatwhitespace=false,
    columns=flexible,
    keepspaces=true
}
\geometry{verbose,tmargin=0.5in,bmargin=0.5in,lmargin=0.5in,rmargin=0.5in}
\pagenumbering{gobble}'''

    def generate_latex(self, name, email, phone, linkedin, code_cells):
        # Start with the document and contact information
        content = [
            self.template_header,
            r'\begin{document}',
            r'\texttt{',
            r'\textbf{' + name + r'}',
            r'\textbar{}',
            r'\href{mailto:' + email + r'}{' + email + r'} \textbar{} ',
            r'\href{tel:' + phone + r'}{' + phone + r'} \textbar{}',
            r'\href{' + linkedin + r'}{' + linkedin.replace('https://', '') + r'}}\\',
        ]

        # Process each cell
        for cell in code_cells:
            # Split into lines but preserve empty lines
            lines = cell.splitlines()
            
            # Remove only leading and trailing empty lines
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
                
            # Keep all lines including empty ones in the middle
            cell_content = '\n'.join(line.rstrip() for line in lines)
            
            # Add the cell to the document
            content.extend([
                r'\begin{mdframed}[',
                r'    linewidth=1.6pt,',
                r'    linecolor=borderGray,',
                r'    leftmargin=0pt,',
                r'    rightmargin=0pt,',
                r'    innerleftmargin=0pt,',
                r'    innerrightmargin=0pt,',
                r'    innertopmargin=-6pt,',
                r'    innerbottommargin=-6pt,',
                r']',
                r'\begin{lstlisting}',
                cell_content,
                r'\end{lstlisting}',
                r'\end{mdframed}',
                r'\vspace{-0.75cm}'
            ])

        content.append(r'\end{document}')
        
        return '\n'.join(content)
        
    def save_and_compile(self, content, output_dir, filename="jupyter_cv"):
        os.makedirs(output_dir, exist_ok=True)
        tex_path = os.path.join(output_dir, f"{filename}.tex")
        pdf_path = os.path.join(output_dir, f"{filename}.pdf")
        
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        try:
            for _ in range(2):
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_path],
                    check=True,
                    capture_output=True
                )
            return pdf_path
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"LaTeX compilation failed: {e.output.decode()}")
        except FileNotFoundError:
            raise Exception("pdflatex not found. Please install TeX Live or MiKTeX.")