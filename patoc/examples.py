from .circuit import Circuit

# LHS of axiom CZ
czLHS = Circuit("cz-one-cnot")
CZorg1 = czLHS.gate("in", pos=(0,0), org=True)
CZorg2 = czLHS.gate("in", pos=(0,1), org=True)
CZh1 = czLHS.gate("H", pos=(1,1))
CZcx1 = czLHS.gate("CNOT", pos=(2,[1,1]))
CZh2 = czLHS.gate("H", pos=(3,1))
CZdst1 = czLHS.gate("out", pos=(4,0), dst=True)
CZdst2 = czLHS.gate("out", pos=(4,1), dst=True)
czLHS.connect(CZorg1, CZcx1, wiring=(0,0))
czLHS.connect(CZorg2, CZh1, wiring=(0,0))
czLHS.connect(CZcx1, CZdst1, wiring=(0,0))
czLHS.connect(CZh1, CZcx1, wiring=(0,1))
czLHS.connect(CZcx1, CZh2, wiring=(1,0))
czLHS.connect(CZh2, CZdst2, wiring=(0,0))

# Big circuit containing LHS of axiom CZ
circuit1 = Circuit("My circuit")
org1 = circuit1.gate("in", pos=(0,0), org=True)
org2 = circuit1.gate("in", pos=(0,1), org=True)
org3 = circuit1.gate("in", pos=(0,2), org=True)
org4 = circuit1.gate("in", pos=(0,3), org=True)
h1 = circuit1.gate("H", pos=(1,1))
a = circuit1.gate("A", dom=2, pos=(1,[2,3]))
h2 = circuit1.gate("H", pos=(2,2))
cx1 = circuit1.gate("CNOT", pos=(3,[1,2]))
h3 = circuit1.gate("H", pos=(4,2))
b = circuit1.gate("B", dom=2, pos=(4,[0,1]))
cx2 = circuit1.gate("CNOT", pos=(5,[1,2]))
dst1 = circuit1.gate("out", pos=(7,0), dst=True)
dst2 = circuit1.gate("out", pos=(7,1), dst=True)
dst3 = circuit1.gate("out", pos=(7,2), dst=True)
dst4 = circuit1.gate("out", pos=(7,3), dst=True)
h4 = circuit1.gate("H", pos=(6,2))
circuit1.connect(org1, b, wiring=(0,0))
circuit1.connect(org2, h1, wiring=(0,0))
circuit1.connect(org3, a, wiring=(0,0))
circuit1.connect(org4, a, wiring=(0,1))
circuit1.connect(a, h2, wiring=(0,0))
circuit1.connect(a, dst4, wiring=(1,0))
circuit1.connect(h1, cx1, wiring=(0,0))
circuit1.connect(h2, cx1, wiring=(0,1))
circuit1.connect(cx1, b, wiring=(0,1))
circuit1.connect(cx1, h3, wiring=(1,0))
circuit1.connect(b, dst1, wiring=(0,0))
circuit1.connect(b, cx2, wiring=(1,0))
circuit1.connect(h3, cx2, wiring=(0,1))
circuit1.connect(cx2, dst2, wiring=(0,0))
circuit1.connect(cx2, h4, wiring=(1,0))
circuit1.connect(h4, dst3, wiring=(0,0))

# Sub-circuit of circuit1
subcircuit1 = Circuit("My sub-circuit")
org1 = subcircuit1.gate("in", pos=(0,0), org=True)
org2 = subcircuit1.gate("in", pos=(0,1), org=True)
org3 = subcircuit1.gate("in", pos=(0,2), org=True)
h3 = subcircuit1.gate("H", pos=(1,2))
b = subcircuit1.gate("B", dom=2, pos=(1,[0,1]))
cx2 = subcircuit1.gate("CNOT", pos=(2,[1,2]))
dst1 = subcircuit1.gate("out", pos=(3,0), dst=True)
dst2 = subcircuit1.gate("out", pos=(3,1), dst=True)
dst3 = subcircuit1.gate("out", pos=(3,2), dst=True)
subcircuit1.connect(org1, b, wiring=(0,0))
subcircuit1.connect(org2, b, wiring=(0,1))
subcircuit1.connect(org3, h3, wiring=(0,0))
subcircuit1.connect(b, dst1, wiring=(0,0))
subcircuit1.connect(b, cx2, wiring=(1,0))
subcircuit1.connect(h3, cx2, wiring=(0,1))
subcircuit1.connect(cx2, dst2, wiring=(0,0))
subcircuit1.connect(cx2, dst3, wiring=(1,0))


# test circuit containing LHS of axiom CZ
circuit2 = Circuit("My circuit")
org1 = circuit2.gate("in", org=True)
org2 = circuit2.gate("in", org=True)
org3 = circuit2.gate("in", org=True)
org4 = circuit2.gate("in", org=True)
h1 = circuit2.gate("H")
a = circuit2.gate("A", dom=2)
h2 = circuit2.gate("H")
p = circuit2.gate("P", dom=3)
b = circuit2.gate("B", dom=2)
h3 = circuit2.gate("H")
u = circuit2.gate("U", dom=2)
h4 = circuit2.gate("H")
dst1 = circuit2.gate("out", dst=True)
dst2 = circuit2.gate("out", dst=True)
dst3 = circuit2.gate("out", dst=True)
dst4 = circuit2.gate("out", dst=True)
circuit2.connect(org1, b, wiring=(0,0))
circuit2.connect(org2, h1, wiring=(0,0))
circuit2.connect(org3, a, wiring=(0,0))
circuit2.connect(org4, a, wiring=(0,1))
circuit2.connect(a, h2, wiring=(0,0))
circuit2.connect(a, p, wiring=(1,2))
circuit2.connect(h1, p, wiring=(0,1))
circuit2.connect(h2, p, wiring=(0,0))
circuit2.connect(p, b, wiring=(0,1))
circuit2.connect(p, h3, wiring=(1,0))
circuit2.connect(b, dst1, wiring=(0,0))
circuit2.connect(b, u, wiring=(1,0))
circuit2.connect(h3, u, wiring=(0,1))
circuit2.connect(u, dst2, wiring=(0,0))
circuit2.connect(u, h4, wiring=(1,0))
circuit2.connect(h4, dst3, wiring=(0,0))
circuit2.connect(p, dst4, wiring=(2,0))

# test
connectivity = Circuit("Connectivity")
org1 = connectivity.gate("in", dom=0, cod=1, org=True)
org2 = connectivity.gate("in", dom=0, cod=1, org=True)
org3 = connectivity.gate("in", dom=0, cod=1, org=True)
a = connectivity.gate("A", dom=2, cod=1)
b = connectivity.gate("B", dom=2, cod=3)
c = connectivity.gate("C", dom=1, cod=1)
dst1 = connectivity.gate("out", dom=1, cod=0, dst=True)
dst2 = connectivity.gate("out", dom=1, cod=0, dst=True)
dst3 = connectivity.gate("out", dom=1, cod=0, dst=True)
connectivity.connect(org1, a, wiring=(0,0))
connectivity.connect(org2, a, wiring=(0,1))
connectivity.connect(org3, b, wiring=(0,1))
connectivity.connect(a, b, wiring=(0,0))
connectivity.connect(b, c, wiring=(0,0))
connectivity.connect(c, dst1, wiring=(0,0))
connectivity.connect(b, dst2, wiring=(1,0))
connectivity.connect(b, dst3, wiring=(2,0))

fullexample = Circuit("A circuit that contains all gate types.")
org1 = fullexample.gate("in", org=True)
org2 = fullexample.gate("in", org=True)
org3 = fullexample.gate("in", org=True)
a = fullexample.gate("A")
b = fullexample.gate("B", dom=2)
c = fullexample.gate("[2]C", dom=3)
d = fullexample.gate("D")
e = fullexample.gate("E", dom=2, cod=1)
f = fullexample.gate("F", dom=2, cod=3)
g = fullexample.gate("div", dom=1, cod=2)
h = fullexample.gate("[2]H", dom=4, cod=3)
dst1 = fullexample.gate("out", dst=True)
dst2 = fullexample.gate("out", dst=True)
dst3 = fullexample.gate("out", dst=True)
fullexample.connect(org1, a, wiring=(0,0))
fullexample.connect(org2, b, wiring=(0,0))
fullexample.connect(org3, b, wiring=(0,1))
fullexample.connect(a, c, wiring=(0,0))
fullexample.connect(b, c, wiring=(0,1))
fullexample.connect(b, c, wiring=(1,2))
fullexample.connect(c, d, wiring=(1,0))
fullexample.connect(c, e, wiring=(0,0))
fullexample.connect(c, e, wiring=(2,1))
fullexample.connect(d, f, wiring=(0,0))
fullexample.connect(e, f, wiring=(0,1))
fullexample.connect(f, h, wiring=(0,0))
fullexample.connect(f, g, wiring=(1,0))
fullexample.connect(f, h, wiring=(2,1))
fullexample.connect(g, h, wiring=(0,2))
fullexample.connect(g, h, wiring=(1,3))
fullexample.connect(h, dst1, wiring=(0,0))
fullexample.connect(h, dst2, wiring=(2,0))
fullexample.connect(h, dst3, wiring=(1,0))