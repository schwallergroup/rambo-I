# Generation of ChromaDB 

**Source of the dataset**: King-Smith, E., Berritt, S., Bernier, L. *et al.* Probing the chemical 'reactome’ with high-throughput experimentation data.  *Nat. Chem.*  (2024). https://doi.org/10.1038/s41557-023-01393-w

https://github.com/emmaking-smith/HiTEA/tree/master/data 

SMILES structures were canonicalized. Each row of the dataset  was wrapped in text and then embedded using the OpenAI embedding 'text-embedding-3-small'. Each vector in the VB represents one reaction with conditions, reagents, etc. 