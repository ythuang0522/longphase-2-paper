PYTHON ?= python3

all: main.pdf Supplementary.pdf

# Figs. 2-6, Supp. Figs. 10-12/14 and Supp. Tables 7-12 from supplementary.xlsx;
# needs matplotlib + openpyxl (here: make results-figs PYTHON=~/miniforge3/envs/gemini/bin/python3)
results-figs:
	cd figures-source && $(PYTHON) make_results_figs.py

Supplementary.pdf: Supplementary.tex references.bib figures/supp/*.pdf figures-source/supp_tables.tex
	latexmk -pdf -interaction=nonstopmode -halt-on-error Supplementary.tex

figures/supp/%.pdf: figures/supp/%.svg
	rsvg-convert -f pdf -o $@ $<

figures/fig1_overview.svg: figures-source/make_fig1.py
	python3 figures-source/make_fig1.py

figures/fig1_overview.pdf: figures/fig1_overview.svg
	rsvg-convert -f pdf -o $@ $<

main.pdf: main.tex sections/*.tex references.bib figures/fig1_overview.pdf figures/fig[2-6]_*.pdf
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

wordcount:
	@texcount -1 -sum sections/introduction.tex

clean:
	latexmk -C
	rm -f *.bbl *.blg *.run.xml

.PHONY: all wordcount clean results-figs
