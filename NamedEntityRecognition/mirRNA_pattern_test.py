import re

MIRSTART = r"(([mM][iI])|(micro)|(let)|(has)|(mmu))[-]?"
mirnaPattern = MIRSTART+r"[rR]?[Nn]?[Aa]?[-]?[0-9a-z\-]*"

mirnaShort = MIRSTART + r"[rR]?[Nn]?[Aa]?[-]?[0-9,/&a-zA-Z]*"

test_text = ["miR-123","miR-200a","miR-16-1","let-7a"]
test_short = ["miR-123,-46,-23","miR-200a,b,c","miR-21/37",\
              "miR-99a/100","miR-15a/16-1","miR-221/-222",\
              "miR-23b/-27b","miR-221&222"]


for word in test_text:
    if not (re.search(mirnaPattern,word)):
        print "Error in ",word
    #else : 
    #    print word," is compiled."
   
for word in test_short:
    if not (re.search(mirnaShort,word)):
        print "Error in ",word
    #else : 
    #    print word," is compiled."

