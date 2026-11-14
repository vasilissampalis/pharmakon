import math
def rd(a,b):
    p1=a[0]/a[1]; p2=b[0]/b[1]; d=p1-p2; se=math.sqrt(p1*(1-p1)/a[1]+p2*(1-p2)/b[1])
    return round(d*100,1), round((d-1.96*se)*100,1), round((d+1.96*se)*100,1)
print("Miller RD CRAFT-Johnson 6mo", rd((29,45),(12,40)))
print("Miller RD CRAFT-AlAnon 6mo", rd((29,45),(6,45)))
print("Roozen pooled props", round(84/125*100,1), round(18/99*100,1))
# Smith chi-square on percentages (Fig 9B)
over={'S':15.0,'H':60.6,'I':24.4}
cl={'I':{'S':11.1,'H':64.1,'I':24.8},'II':{'S':15.6,'H':57.1,'I':27.4},'III':{'S':30.9,'H':55.8,'I':13.3}}
for k,v in cl.items():
    print("chi2 on % cluster",k, round(sum((v[c]-over[c])**2/over[c] for c in over),2))
print("Fig9A sum with category", 7306+2944+1813, "all", 7306+2944+1813+1338)
print("shares", round(7306/12063*100,1), round(2944/12063*100,1), round(1813/12063*100,1))
print("Fig6A sum", 17616+12322+6681+4582, "None share", round(12322/41201*100,1))
print("clusters", round(21811/41201*100,1), round(14188/41201*100,1), round(5202/41201*100,1), round((21811+14188)/41201*100,1))
# Hughes odds
hv=70.6; cp=76.6
print("Hughes OR not offending HVP vs CP", round(((100-hv)/hv)/((100-cp)/cp),3), "OR offending", round((hv/(100-hv))/(cp/(100-cp)),3))
# Hazekamp
print("Hazekamp purchases", 18+17, "of 40")
