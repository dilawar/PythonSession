all : ./Intro2Prog.pdf

%.pdf : %.md
	# pandoc --pdf-engine=lualatex -t beamer $< -o $@
	pandoc --pdf-engine=pdflatex -t beamer $< -o $@
