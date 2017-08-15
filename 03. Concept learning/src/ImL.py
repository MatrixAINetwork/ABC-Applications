class stack:
    def __init__(self):
        self.stack = []
    def put(self,item):
        self.stack.append(item)
        return self
    def get(self):
        res = self.stack[-1]
        self.stack=self.stack[:-1]
        return res
    def empty(self):
        return len(self.stack)==0

class queue(stack):
    def get(self):
        res = self.stack[0]
        self.stack=self.stack[1:]
        return res

class graph:
    def __init__(self):
        self.vertices = []
        self.edges = {}
        self.edge_labelling = {}
        self.vertice_labelling = {}

    def add_edge(self,st,end,label=" "):
        try:
            self.edges[st].append(end)
        except KeyError:
            if st not in self.vertices:
                raise "Wrong starting vertice"
            self.edges[st] =[end]
            
        self.edge_labelling[st,end]=label
        
    def add_vert(self,vert,label=" "):
        self.vertices.append(vert)
        self.vertice_labelling[vert]=label
        self.edges[vert]=[]
        
    def __repr__(self):
        rep = "Graph: \n"
        for v in self.vertices:
            rep += "\t%s"%v
            try:
                rep += "(%s) => "%str(self.vertice_labelling[v])
            except KeyError:
                rep += " => "
            for v2 in self.edges[v]:
                rep+= "%s"%v2
                try:
                     rep+="(%s), "%str(self.edge_labelling[(v,v2)])
                except KeyError:
                    rep+=", "
            rep +="\n"
return rep
            
    def ford_bellman(self,s):
        D = {}
        inf = len(self.vertices)
        for x in self.vertices:
            if x in self.edges[s]:
                D[x]=1
            else:
                D[x]=inf
        D[s]=0
        for i in range(len(self.vertices)-2):
            for v in self.vertices:
                if v != s:
                    for u in self.vertices:
                        if v in self.edges[u]:
                            D[v]=min(D[v],D[u]+1)
        return D

    def avg_dist(self):
        s = 0
        for v in self.vertices:
            s+=sum(self.ford_bellman(v).values())
        return s*1.0/(len(self.vertices)**2-len(self.vertices))

    def make_undirected(self):
        for v in self.vertices:
            for w in self.vertices:
                if (w in self.edges[v]) and (not v in self.edges[w]):
                    self.edges[w].append(v)
                    
    def clust_sig(self,meths=["FFA","FFB","FFC","FB"]):
        lst=[]
        avg={}
        for m in meths:
            avg[m]=0.0
        for v in self.vertices:
            vec=map(lambda m: self.c_v(v,m),meths)
            s=sum(vec)
            if s==0.0:
                norm_vec=vec
            else:
                norm_vec=map(lambda x: x/s,vec)
            lst.append(norm_vec)
            for m,v in zip(meths,norm_vec):
                avg[m]+=v
        s_all=sum(avg.values())
        for m in meths:
            avg[m]/=s_all
        return lst,avg
    
    def random_regular(self,n,k):
        import random
        self.__init__()
        self.vertices=range(n)
        for v in self.vertices:
            self.edges[v]=random.sample(self.vertices,k)

    def random_of_size(self,n,m,e_labels=["+","-"],v_labels=["AND","OR"]):
        import random
        self.__init__()
        self.vertices=range(n)
        for v in self.vertices:
            self.vertice_labelling[v]=random.choice(v_labels)
            self.edges[v]=[]
        edge_pool = []
        for u in self.vertices:
            for v in self.vertices:
                edge_pool.append((u,v))

        sample = random.sample(edge_pool,m)

        for u,v in sample:
            self.edges[u].append(v)
            self.edge_labelling[u,v]=random.choice(e_labels)
        
        
        
    def search(self, start, fun, struct=stack,avoid=None,forward=True,backward=False):
        if not type(start)==type([]): 
            start = [start]
            
        if avoid==None:
            avoid=[] 
            
        st = struct()
        for v in start:
            st.put(v)
            avoid.append(v)
            
        while not st.empty():
            vert = st.get()
            fun(vert)
            if forward:
                for v in self.edges[vert]:
                    if v not in avoid:
                        st.put(v)
                        avoid.append(v)
            if backward: 
                for v in self.parents(vert):
                    if v not in avoid:
                        st.put(v)
                        avoid.append(v)
                    

                

