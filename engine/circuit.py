########################### Parameter class ##########################
class Parameter:
    def __init__(self, symbolic, value) -> None:
        """
        Attributs:
            symbolic: bool -> type of the parameter (False for value, True for symbol)
            value: str -> mathematical description
        """
        self.symbolic = symbolic
        self.value = value


############################# Gate class #############################
class Gate:
    def __init__(self, id, type, dom=1, pos=(None,None)) -> None:
        """
        Attributs:
            id: int -> id of the node in dag
            type: str -> type of the gate (H, P, CX, D, G, etc.)
            dom: int -> domain
            preset: [int] -> list of predecessors ids
            postset: [int] -> list of successors ids
        """
        self.id = id
        self.type = type
        self.dom = dom
        self.preset = []
        self.postset = []
        self.pos = pos
        self.depth = None
        self.gate_item = None

        if type == "CNOT": self.dom = 2

    def __str__(self) -> str:
        return str(self.preset)+" <<< "+str(self.type)+"("+str(self.id)+") >>> " + str(self.postset)
    
    def addPredecessor(self, id, wiring) -> None:
        self.preset.append((id,wiring))

    def addSuccessor(self, id, wiring) -> None:
        self.postset.append((id,wiring))
    
    def getPredecessorId(self, wire=0) -> int:
        for (idpre,wiring) in self.preset:
            if wiring[1] == wire: return idpre
            
    def getSuccessorId(self, wire=0) -> int:
        for (idpost,wiring) in self.postset:
            if wiring[0] == wire: return idpost

    def isSparseGate(self) -> bool:
        """Return True iff the ys of the gate are none consecutive"""
        x,y = self.pos
        if not (type(y) == int or len(y)<=1):
            for i in range(self.dom-1):
                if y[i+1]-y[i] != 1: return True
        return False
        



########################### Circuit class ############################
class Circuit:
    """Class of quantum circuits"""

    def __init__(self, name) -> None:
        """
        Attributs:
            name: str -> name of the circuit
            gates: [Gate] -> list of gates indexed by gate id
            org: [int] -> list of origin nodes ids
            dst: [int] -> list of destination nodes ids
        """
        self.name = name
        self.gates = []
        self.org = []
        self.dst = []
        self.dom = 0
        self.cod = 0

        self.updateDepth()

    def __str__(self) -> str:
        return "This circuit is called: " + self.name
    
    def gate(self, type, dom=1, pos=(None,None), org=False, dst=False) -> Gate:
        id = len(self.gates)
        g = Gate(id, type, dom, pos)
        self.gates.append(g)
        if org:
            self.org.append(id)
            self.dom += 1
        if dst:
            self.dst.append(id)
            self.cod += 1
        return g

    def connect(self, org, dst, wiring) -> None:
        org.addSuccessor(dst.id,wiring)
        dst.addPredecessor(org.id,wiring)
    
    def checkConnectivity(self) -> bool:
        return True
    
    def updateDepth(self) -> None:
        """USe dynamic programming to compute the depth of every gates"""
        depths = [None for i in range(len(self.gates))]
        for idorg in self.org: depths[idorg] = 0

        def computeDepth(id) -> int:
            maxPredDepth = 0
            for (idpred,wiring) in self.gates[id].preset:
                if depths[idpred] == None:
                    depths[idpred] = computeDepth(idpred)
                maxPredDepth = max(maxPredDepth,depths[idpred])
            depths[id] = maxPredDepth+1
            return  depths[id]

        for iddst in self.dst: computeDepth(iddst)
        for gate in self.gates: gate.depth = depths[gate.id]
    
    # Only works for connected axiom that contains at least one gate for now
    # but should not be problem because for disconnected axiom, just apply the function to each connected components
    # and if no gate, then the axiom is applicable evrywhere
    def matchAxiom(self, axiom) -> None:
        entryGate = axiom.gates[axiom.gates[axiom.org[0]].postset[0][0]]
        print("entry gate", entryGate.id)
        for matchgate in self.gates:
            if matchgate.type == entryGate.type:
                print("match entry gate candidate", matchgate.id)
                # Initialize new matching and new queue
                matching = [None for i in range(len(axiom.gates))]
                for idorg in axiom.org: matching[idorg] = -1
                for iddst in axiom.dst: matching[iddst] = -1
                matching[entryGate.id] = matchgate.id
                queue = [entryGate]
                visited = [False for i in range(len(axiom.gates))]
                visited[entryGate.id] = True

                matchingFailed = False

                while len(queue)>0:
                    print("matching", matching)
                    currentGate = queue.pop(0)
                    visited[currentGate.id] = True
                    currentMatchedGateId = matching[currentGate.id] # id of the gate of circuit that is matched to currentGate
                    currentMatchedGate = self.gates[currentMatchedGateId]
                    print(currentMatchedGateId)

                    nbpred = len(currentGate.preset)
                    nbsucc = len(currentGate.postset)

                    for i in range(nbpred):
                        currentGatePredId = currentGate.getPredecessorId(wire=i)
                        currentGatePred = axiom.gates[currentGatePredId]
                        
                        if not visited[currentGatePredId]:
                            matchPredCandidateId = currentMatchedGate.getPredecessorId(wire=i)
                            matchPredCandidate = self.gates[matchPredCandidateId]

                            if currentGatePred.type != "in" and currentGatePred.type != "out":
                                if matchPredCandidate.type == currentGatePred.type:
                                    matching[currentGatePredId] = matchPredCandidate.id
                                    queue.append(currentGatePred)
                                else:
                                    matchingFailed = True
                                    break
                    if matchingFailed: break

                    for i in range(nbsucc):
                        currentGateSuccId = currentGate.getSuccessorId(wire=i)
                        currentGateSucc = axiom.gates[currentGateSuccId]

                        if not visited[currentGateSuccId]:
                            matchSuccCandidateId = currentMatchedGate.getSuccessorId(wire=i)
                            matchSuccCandidate = self.gates[matchSuccCandidateId]

                            if currentGateSucc.type != "in" and currentGateSucc.type != "out":
                                if matchSuccCandidate.type == currentGateSucc.type:
                                    matching[currentGateSuccId] = matchSuccCandidate.id
                                    queue.append(currentGateSucc)
                                else:
                                    matchingFailed = True
                                    break
                    if matchingFailed: break