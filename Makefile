all: main.pdf Supplementary.pdf

Supplementary.pdf: Supplementary.tex references.bib figures/supp/*.pdf
	latexmk -pdf -interaction=nonstopmode -halt-on-error Supplementary.tex

figures/supp/%.pdf: figures/supp/%.svg
	rsvg-convert -f pdf -o $@ $<

main.pdf: main.tex sections/*.tex references.bib figures/*
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

wordcount:
	@texcount -1 -sum sections/introduction.tex

clean:
	latexmk -C
	rm -f *.bbl *.blg *.run.xml

.PHONY: all wordcount clean
