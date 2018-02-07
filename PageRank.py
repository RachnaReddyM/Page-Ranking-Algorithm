import math
import operator


M={}                # set of pages with its incoming links
outlinks={}         # set of pages with its outgoing links
L={}                # set of pages with no. of outgoing links
S=[]                # list of pages with no outgoing links(sink pages)
PR={}               # set of pages with Page Rank
newPR={}            # set of pages with updated Page Rank
d=0.85              # damping/teleportation factor

# function to get inlinks of each page from a file
def inlinks_from_file(fname):

	with open(fname, "r+") as f:
		each_line_list = f.readlines()
	for s in each_line_list[0:len(each_line_list)]:
		line= str(s).strip()
		line_list= line.split()
		M[line_list[0]] = line_list[1:]
	
	f.close()
	
	#for x,y in inlinks.iteritems():
	#	print x,y

	#print(M)
		

# function to get outgoing links of each page
# also gets the no. of outgoing links of each page and no. of sink pages
def outlinks_from_inlinks():

	for x,y in M.iteritems():
		if x not in outlinks.keys():
			outlinks[x] = []
			L[x] = 0
		for node in y:
			if node not in outlinks:
				outlinks[node] = []
				L[node] =0
			outlinks[node].append(x)  
			L[node]+=1

	for sink in L.keys():
		if L[sink]==0:
			S.append(sink)


# function to calculate the page rank of each page till the page ranks converge
def calculate_pagerank(Pages):

	convergence=0
	perplexity=0
	PagesLen=len(Pages)
	for p in Pages:
		PR[p]=(1.0/PagesLen)              # initial value
	while(convergence < 4):
		sinkPR=0
		for p in S:
			sinkPR+=PR[p]
		for p in Pages:                   # calculate total sink page rank
			newPR[p]=(1-d)/PagesLen
			newPR[p]+= d*sinkPR/PagesLen
			for q in M[p]:
				newPR[p]+=d*PR[q]/(L[q])
		for p in Pages:
			PR[p]=newPR[p]

		print perplexity
		oldper=perplexity


# to calculate the convergence factor


		h_of_pr=0

		for i in Pages:
			h_of_pr+=PR[i]*math.log(float(PR[i]),2)
		
		perplexity=pow(2, (-h_of_pr))
		if abs(oldper-perplexity)<1 :
			convergence+=1
		else:
			convergence=0

	return PR
def main():

	inlinks_from_file("G2.txt")
	outlinks_from_inlinks()
	Pages=(M.keys())
	no_of_pages=len(Pages)
	print (no_of_pages)
	#print ("Outlinks of all pages")
	#print outlinks
	#print ("No of Outlinks for each page: ")
	#print L
	print ("No. of Sink nodes: ")
	print (len(S))
	Page_Rank=calculate_pagerank(Pages)
	SortedPageRank=sorted(Page_Rank.iteritems(), key=operator.itemgetter(1), reverse=True)
	

	f=open("PageRankG2.txt",'w+')
	for key,value in SortedPageRank[0:50]:
		f.write(str(key)+' '+str(value)+'\n')
	f.close()

main()