

## remove all the domains to ignore from the toxin and RND pump HMM files

to_ignore = []
with open("domains_to_ignore.txt") as f:
	for line in f:
		to_ignore.append(line.strip())


def rewrite_hmms(hmm_file_in, hmm_file_out):
	
	out = open(hmm_file_out, "w")
	hmm_file_full = open(hmm_file_in).read()
	hmms = hmm_file_full.split("//")
	for hmm in hmms:
		for line in hmm.split("\n"):
			if line.startswith("NAME"):
				toks = line.split()
				if toks[1] not in to_ignore:
					out.write(hmm + "//\n")
				break
	out.close()

rewrite_hmms("toxins","toxins_new")
rewrite_hmms("RND_pump","RND_new")
## rerun hmmpress