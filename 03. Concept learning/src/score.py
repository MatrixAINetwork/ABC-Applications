class score:
    
    def learn(self,selected_data,verbose=None,n_min=1,limit=None,score_max=fpconst.PosInf,score_delta=fpconst.PosInf, cores=False, picloud=False):
        
        if verbose:
            print 'Learning parents of', selected_data.vertex.name, '...',
        v = selected_data.vertex
        nd = len(selected_data)
        parents=selected_data.parents
        p_weights=selected_data.weights
        n = len(parents)
        try:
            lim=int(limit)
        except TypeError:
            lim=n
        
        selected_data_empty=selected_data.subset([])
        mindata = self.lower_bound_for_data_score(selected_data_empty)

        min_set = minset(n_min,score_max,score_delta,self.data_score(selected_data_empty)+\
                self.graph_score(n,v,[],nd)) 
        if n: 
            w_min=p_weights[parents[0]]
            w_max=p_weights[parents[-1]]
            if w_min==w_max:  
                if verbose:
                    print "Using algorithm 2"

                weight=w_min
                size = 1
                
                mg = self.graph_score(n,v,[weight],nd)
                while min_set.accepts(mg+mindata) and (size<=lim): 
                    if cores:
                        import multiprocessing
                        import multiprocessing.pool

                        pool=multiprocessing.Pool(cores)
                        sub_obj = list(self.subsets(parents,size))

                        import itertools
                        results=pool.map(looper, [(selected_data, y, self) for y in sub_obj])
                        pool.close()
                        pool.join()

                        for result,sub in itertools.izip(results, sub_obj):
                                min_set.add(mg+result, sub)


                    else:
                        for sub in self.subsets(parents,size):
                            selected_data_sub=selected_data.subset(sub)
                            min_set.add(mg+self.data_score(selected_data_sub), sub)

                    size+=1
                    mg = self.graph_score(n,v,[weight]*size,nd)

            else: 
                if verbose:
                    print "Using algorithm 1"
                if cores:
                    import multiprocessing
                    import multiprocessing.pool
                    pool=multiprocessing.Pool(cores)                
                    size = 1
                    results = [1]
                    while (True in results) and (size<=lim):
                        subs = list(self.subsets(parents,size))
                        scores = pool.map(looper, [(selected_data, y, self) for y in subs])

                        mgs = []
                        for sub in subs:
                            weight = 0
                            for parent in sub:
                                weight = weight + p_weights[parent]
                            mgs.append(self.graph_score(n,v,[weight],nd))

                        import itertools
                        for score, sub, mg in itertools.izip(scores, subs, mgs):
                           min_set.add(mg+score, sub)
                        
                        results = pool.map(unwrap_min_set_accepts, [(min_set, mg+mindata) for mg in mgs])
                        del mgs, subs, scores
                        size+=1

                    pool.close()
                    pool.join()

                else:
                    subsets=[] 
                    for parent in parents: 
                        heappush(subsets, (self.graph_score(n,v,[p_weights[parent]],nd), [p_weights[parent]], [parent]) )
                    while subsets:
                        mg,weights,sub=heappop(subsets)
                        if not min_set.accepts(mg+mindata):
                            break
                        selected_data_sub=selected_data.subset(sub)
                        min_set.add(mg+self.data_score(selected_data_sub), sub)
                        if len(sub)<lim:
                            last_parent=parents.index(sub[-1])
                            for parent in parents[last_parent+1:]:
                                sub_succ=sub+[parent]
                                weights_succ=weights+[p_weights[parent]]
                                mg_succ=self.graph_score(n,v,weights_succ,nd)
                                heappush(subsets,(mg_succ,weights_succ,sub_succ))                        

        if verbose:
            print 'done', min_set
        return min_set.optimal, min_set.tolist() 

    
    def score_graph(self,g,data):
        s = 0.0
        n_vert = len(g.vertices)
        for i,v in enumerate(g.vertices):
            p = g.parents(v)
            selected_data = data.select_1(i,p)
            sg = self.graph_score(n_vert,v,map(lambda par:par.n_disc,p),len(selected_data))
            sd = self.data_score(selected_data)
            s+=sg+sd
        return s
