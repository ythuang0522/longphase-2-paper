all: main.pdf Supplementary.pdf

Supplementary.pdf: Supplementary.tex references.bib figures/supp/*.pdf
	latexmk -pdf -interaction=nonstopmode -halt-on-error Supplementary.tex

figures/supp/%.pdf: figures/supp/%.svg
	rsvg-convert -f pdf -o $@ $<

figures/fig1_overview.svg: figures-source/make_fig1.py
	python3 figures-source/make_fig1.py

figures/fig1_overview.pdf: figures/fig1_overview.svg
	rsvg-convert -f pdf -o $@ $<

main.pdf: main.tex sections/*.tex references.bib figures/fig1_overview.pdf figures/*.png
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

wordcount:
	@texcount -1 -sum sections/introduction.tex

clean:
	latexmk -C
	rm -f *.bbl *.blg *.run.xml

.PHONY: all wordcount clean
