$max_repeat = 5;

# $pdf_mode = 0; # no PDF

# $pdf_mode = 1; # use pdflatex
# $pdflatex = 'pdflatex %O -synctex=1 -interaction=nonstopmode -file-line-error %S';
# $bibtex = 'bibtex';

# $pdf_mode = 2; # use ps2pdf

$pdf_mode = 3; # use dvipdfmx
$latex = 'uplatex %O -synctex=1 -interaction=nonstopmode -file-line-error %S';
$dvipdf = 'dvipdfmx %O -o %D %S';
$bibtex = 'upbibtex';
$makeindex = 'upmendex %O -o %D %S';

# $pdf_mode = 4; # use lualatex
# $lualatex = 'lualatex %O -synctex=1 -interaction=nonstopmode %S';

# $biber = 'biber --bblencoding=utf8 -u -U --output_safechars';


