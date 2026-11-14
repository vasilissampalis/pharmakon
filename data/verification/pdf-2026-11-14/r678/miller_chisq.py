import math
def stats(rows):
    # rows: list of (engaged, n)
    N=sum(n for e,n in rows); E=sum(e for e,n in rows)
    pear=g=0
    for e,n in rows:
        for o,col in ((e,E),(n-e,N-E)):
            ex=n*col/N
            pear+=(o-ex)**2/ex
            if o>0: g+=2*o*math.log(o/ex)
    return round(pear,2), round(g,2)
A6,J6,C6=(6,45),(12,40),(29,45)
AS,JS,CS=(6,45),(9,40),(29,45)
for lab,a12 in (("Table 1 (Al-Anon 9/45)",(9,45)),("text (Al-Anon 8/45)",(8,45))):
    J12,C12=(14,40),(30,45)
    print(lab)
    print("  3-group Study2", stats([AS,JS,CS]), "reported 29.84")
    print("  3-group 6 mo  ", stats([A6,J6,C6]), "reported 27.33")
    print("  3-group 12 mo ", stats([a12,J12,C12]), "reported 23.78")
    print("  J vs C Study2 ", stats([JS,CS]), "reported 15.66")
    print("  J vs C 6 mo   ", stats([J6,C6]), "reported 10.29")
    print("  J vs C 12 mo  ", stats([J12,C12]), "reported 8.65")
    print("  A vs J Study2 ", stats([AS,JS]), "reported 1.23")
    print("  A vs J 6 mo   ", stats([A6,J6]), "reported 3.56")
    print("  A vs J 12 mo  ", stats([a12,J12]), "reported 3.29")
print("CRAFT therapists 7/14 vs 10/11", stats([(7,14),(10,11)]), "reported 5.23")
# risk differences (Wald 95% CI)
def rd(a,b):
    p1=a[0]/a[1]; p2=b[0]/b[1]; d=p1-p2; se=math.sqrt(p1*(1-p1)/a[1]+p2*(1-p2)/b[1])
    return round(d*100,1), round((d-1.96*se)*100,1), round((d+1.96*se)*100,1)
print("RD CRAFT-Johnson 6mo", rd(C6,J6), " CRAFT-AlAnon 6mo", rd(C6,A6))
print("RD CRAFT-Johnson 12mo", rd((30,45),(14,40)), " CRAFT-AlAnon 12mo (9/45)", rd((30,45),(9,45)))
print("90% by 6 months: 47/53 =", round(47/53*100,1), " 47/52 =", round(47/52*100,1))
