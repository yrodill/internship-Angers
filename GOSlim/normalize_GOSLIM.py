"""
Benoît BOTHOREL
GO annotation normalization
19/03/2019

Ref::
Liesecke, Franziska, et al. 
"Ranking genome-wide correlation measurements improves microarray and
 RNA-seq based global and targeted co-expression networks."
 Sci. Rep., vol. 8, no. 1, 18 July 2018, p. 10885, 
 doi:10.1038/s41598-018-29077-3.

 Berardini, TZ, Mundodi, S, Reiser, R, Huala, E, Garcia-Hernandez, M,
Zhang, P, Mueller, LM, Yoon, J, Doyle, A, Lander, G, Moseyko, N, Yoo,
D, Xu, I, Zoeckler, B, Montoya, M, Miller, N, Weems, D, and Rhee, SY
(2004) Functional annotation of the Arabidopsis genome using
controlled vocabularies. Plant Physiol. 135(2):1-11.

Column headers :explanation

1. locus name: standard AGI convention name

2. TAIR accession:the unique identifier for an object in the TAIR database- 
the object type is the prefix, followed by a unique accession number(e.g. gene:12345).  

3. object name : the name of the object (gene, protein, locus) being annotated.

4. relationship type: the relationship between the annotated object and the GO term

5. GO term: the actual string of letters corresponding to the GO ID

6. GO ID: the unique identifier for a GO term.  

7. TAIR Keyword ID: the unique identifier for a keyword in the TAIR database.

8.  Aspect: F=molecular function, C=cellular component, P=biological 13process. 

9. GOslim term: high level GO term helps in functional categorization.

10. Evidence code: three letter code for evidence types (see: http://www.geneontology.org/GO.evidence.html).

11. Evidence description: the analysis that was done to support the annotation

12. Evidence with: supporting evidence for IGI, IPI, IC, IEA and ISS annotations

13. Reference: Either a TAIR accession for a reference (reference table: reference_id) or reference from PubMed (e.g. PMID:1234).  

14. Annotator: TAIR, TIGR, GOC (GO Consortium), UniProt, IntAct or a TAIR community member

15. Date annotated: date the annotation was made.
"""

pairs = []

with open("ATH_GO_GOSLIM.txt") as annots:
    lines = annots.readlines()

print("Filtering...")
with open("ATH_GO_normalized.csv","w")as output:
	for l in lines:
		values = l.strip().split("\t")
		if(values[7] == "P"):
			#avoid same pairs
			if([values[0],values[5]] not in pairs):
				pairs.append([values[0],values[5]])
				output.write("{}\t{}\t{}\n".format(values[13],values[0],values[5]))
print("Done...")
