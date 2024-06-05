OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
p(pi/2) q[0];
p(pi/2) q[1];
cx q[0], q[1];
p(-pi/2) q[1];
cx q[0], q[1];