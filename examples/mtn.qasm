OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
h q[1];
cx q[0], q[1];
h q[1];