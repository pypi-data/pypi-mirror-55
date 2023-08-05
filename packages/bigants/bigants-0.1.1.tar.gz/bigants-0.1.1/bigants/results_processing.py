#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mygene
import networkx as nx
import numpy as np
import seaborn as sns; sns.set(color_codes=True)
import gseapy


class results_analysis():
    '''
        Performs analysis over the output of BiGAnts algorithm
        
        Attributes:
        -----------
        solution - the output file of BiGAnts.run_search() function
        labels - data preprocessing labels from data_preprocessing() function
    '''
    def __init__(self, solution, labels):
        self.solution = solution
        self.labels = labels
        self.patients1 = [str(self.labels[x]) for x in self.solution[1][0]]
        self.patients2 = [str(self.labels[x]) for x in self.solution[1][1]]
        self.genes1 = [str(self.labels[x]) for x in self.solution[0][0]]    
        self.genes2 = [str(self.labels[x]) for x in self.solution[0][1]]   
    
    def save(self, output, gene_names = False):
        '''
        Saves the results in a csv file
        
        Attributes:
        -----------
        output - the output file name
        gene_names - flag that indicates wheather the initial Entrez (!) ids should be converted to gene names before saving (default - False)
        
        '''
        patients1_str = "|".join(self.patients1)
        patients2_str = "|".join(self.patients2)
        
        if gene_names:
            all_genes  = self.genes1 + self.genes2
            mg = mygene.MyGeneInfo()
            out = mg.querymany(all_genes, scopes='entrezgene', fields='symbol', species='human', verbose = False)
            mapping =dict()
            rev_mapping = dict()
            for line in out:
                rev_mapping[line["symbol"]] = line["query"]
                mapping[line["query"]] = line["symbol"]
            genes1_name = [mapping[x] for x in self.genes1]
            genes2_name = [mapping[x] for x in self.genes2]
        genes1_str = "|".join(genes1_name)
    
        genes2_str = "|".join(genes2_name)
        
        #Saving the solution
        pd.DataFrame([[genes1_str,genes2_str,patients1_str,patients2_str]],columns = ["genes1","genes2","patients1","patients2"]).to_csv(output)
    
    def show_networks(self, GE, G, output = None):
        '''
        Shows the resulting subnetworks coloured wrt to their difference in expression patterns in patients subgroups
        
        Attributes:
        -----------
        GE - processed gene expression data from data_preprocessing() function
        G - processed PPI network from data_preprocessing() function
        output - str or PathLike or file-like object (png, eps, pdf, etc)    
        '''
        # relabel solution IDs to the actual IDs

        all_genes_entr  =  self.genes1 + self.genes2
        all_genes = self.solution[0][0] + self.solution[0][1]
        mg = mygene.MyGeneInfo()
        out = mg.querymany(all_genes_entr, scopes='entrezgene', fields='symbol', species='human', verbose = False)
        mapping =dict()
        rev_mapping = dict()
        for line in out:
            rev_mapping[line["symbol"]] = line["query"]
            mapping[line["query"]] = line["symbol"]
    
        genes1_name = [mapping[x] for x in self.genes1]
        genes2_name = [mapping[x] for x in self.genes2]
        all_genes_names = genes1_name+genes2_name
        
        #relabel expression matrix and the graph to the actual patients ids and gene names
        G_small = nx.subgraph(G, all_genes)
        G_small=nx.relabel_nodes(G_small,self.labels)
        G_small=nx.relabel_nodes(G_small,mapping)
        GE_small = GE[self.solution[1][0]+self.solution[1][1]].loc[all_genes]
        GE_small.index = all_genes_names
        GE_small.columns = self.patients1 +self.patients2
        #compute difference in expression for each gene in different patients groups
        means = list(np.mean(GE_small[self.patients1].loc[all_genes_names],axis = 1)-np.mean(GE_small[self.patients2].loc[all_genes_names],axis = 1).values)
        # set plotting settings
        plt.rc('font', size=20)          # controls default text sizes
        plt.rc('axes', titlesize=20)     # fontsize of the axes title
        plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=25)    # fontsize of the tick labels
        plt.rc('legend', fontsize=30)
        fig = plt.figure(figsize=(15,15))
        vmin = -2
        vmax = 2
        cmap = plt.cm.coolwarm(np.linspace(-0.45,0.8,20))
        cmap = mpl.colors.ListedColormap(cmap[10:,:-1])
        pos = nx.spring_layout(G_small)
        nx.draw_networkx_edges(G_small,pos)
        nc1 = nx.draw_networkx_nodes(G_small, pos = pos,node_color=means, node_size=1700,alpha=.7,
                                     vmin=vmin, vmax=vmax,cmap =cmap, node_shape = "s")
        nx.draw_networkx_labels(G_small,pos,font_size = 22,font_weight = "heavy")
        plt.colorbar(nc1)
        plt.axis('off')
        fig.tight_layout()
        #save if required
        if output != None:
            plt.savefig(output,dpi = 300)
        plt.show()
    
    def show_clustermap(self, GE, G, output = None, true_labels = None):
        '''
        Shows a clustermap of the achieved solution alone or also along with the known patients groups
        
        Attributes:
        -----------
        GE - processed gene expression data from data_preprocessing() function
        G - processed PPI network from data_preprocessing() function
        output - str or PathLike or file-like object (png, eps, pdf, etc)
        true_labels    
        '''
        
        if true_labels !=None:
            patients = self.patients1 + self.patients2
            true_patients = true_labels[0] + true_labels[1]
            if len(set(patients).difference(set(true_patients))) != 0: 
                print("WARNING: Patients ids in true_labels do not match, comparisson wil not be performed")
                true_labels = None
                
        
        

        all_genes_entr  = self.genes1 + self.genes2
        all_genes = self.solution[0][0] + self.solution[0][1]
        mg = mygene.MyGeneInfo()
        out = mg.querymany(all_genes_entr, scopes='entrezgene', fields='symbol', species='human', verbose = False)
        mapping =dict()
        rev_mapping = dict()
        for line in out:
            rev_mapping[line["symbol"]] = line["query"]
            mapping[line["query"]] = line["symbol"]
    
        genes1_name = [mapping[x] for x in self.genes1]
        genes2_name = [mapping[x] for x in self.genes2]
        all_genes_names = genes1_name + genes2_name
        
        #relabel expression matrix and the graph to the actual patients ids and gene names
        G_small = nx.subgraph(G, all_genes)
        G_small=nx.relabel_nodes(G_small,self.labels)
        G_small=nx.relabel_nodes(G_small,mapping)
        GE_small = GE[self.solution[1][0]+self.solution[1][1]].loc[all_genes]
        GE_small.index = all_genes_names
        GE_small.columns = self.patients1 +self.patients2
        # prepare the clustermap
        
        grouping_p = []
        p_num = self.patients1 + self.patients2
        for p in p_num:
            if p in self.patients1:
                grouping_p.append(1)
            else:
                grouping_p.append(2)
        grouping_p = pd.DataFrame(grouping_p,index = p_num)
        grouping_p.columns = ["clusters"]
        species = grouping_p["clusters"]
        lut = {1: '#4FB6D3',2: '#22863E'}
        row_colors1 = species.map(lut)
        
        if true_labels != None:
            grouping_p_true = []
            patients1_true = true_labels[0]
            patients2_true = true_labels[1]
            
            for p in p_num:
                if p in patients1_true:
                    grouping_p_true.append(5)
                elif p in patients2_true:
                    grouping_p_true.append(6)
            grouping_p_true = pd.DataFrame(grouping_p_true,index = p_num)
            grouping_p_true.columns = ["true"]
            species = grouping_p_true["true"]
            lut = {5: '#F3FF33',6: 'm'}
            row_colors2 = species.map(lut)
        grouping_g =[]
        g_num = GE_small.index
        for g in g_num:
            if g in genes1_name :
                grouping_g.append(1)
            elif  g in genes2_name :
                grouping_g.append(2)
            else:
                grouping_g.append(3)
        
                
        grouping_g = pd.DataFrame(grouping_g,index = g_num)
        grouping_g.columns = [" "]
        species = grouping_g[" "]
        lut = {1: '#4FB6D3',2: '#22863E'}
        col_colors = species.map(lut)
        
        
        
        plt.rc('font', size=10)          # controls default text sizes
        plt.rc('axes', titlesize=20)     # fontsize of the axes title
        plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
        plt.rc('legend', fontsize=20)
        
        if true_labels != None:
            g = sns.clustermap(GE_small.T, row_colors=[row_colors1,row_colors2],row_cluster = False,col_cluster = False, col_colors = col_colors,figsize=(15, 10),cbar_kws=dict(ticks=[4, 0, -4]),
                           cmap = "Spectral",yticklabels=False)
        
            values = ["true class1","true class2", "cluster1", "cluster2"]
            colors = ['#F3FF33','m','#4FB6D3', '#22863E']
            for i in range(len(values)):
                l = values[i]
                c = colors[i]
                g.ax_col_dendrogram.bar(0, 0, color=c,
                                        label=l, linewidth=0)
            g.ax_col_dendrogram.legend(loc="upper center", ncol=2,bbox_to_anchor=(0.72, 0.87),
                                        borderaxespad=0.)
        else:
            g = sns.clustermap(GE_small.T, row_colors=row_colors1,row_cluster = False,col_cluster = False, col_colors = col_colors,figsize=(15, 10),cbar_kws=dict(ticks=[4, 0, -4]),
                           cmap = "Spectral",yticklabels=False)
        
            values = ["cluster1", "cluster2"]
            colors = ['#4FB6D3', '#22863E']
            for i in range(len(values)):
                l = values[i]
                c = colors[i]
                g.ax_col_dendrogram.bar(0, 0, color=c,
                                        label=l, linewidth=0)
            g.ax_col_dendrogram.legend(loc="upper center", ncol=2,bbox_to_anchor=(0.72, 0.87),
                                        borderaxespad=0.)
            
        ax = g.ax_heatmap
        ax.set_xlabel("Genes")
        ax.set_ylabel("Patients")
        if output != None:
            plt.savefig(output,dpi = 300)
        plt.show()
    
    def jaccard_index(self, true_labels): 
        def jac(x,y):
            if len(x)>0 and len(y)>0:
                return len(set(x).intersection(set(y)))/len((set(x).union(set(y))))
            else:
                return(0)
            
        def jac_matrix(true,pred):
            res = np.zeros((len(true),len(true)))
            for i in range(len(true)):
                for j in range(len(true)):
                    res[i,j] = jac(true[i],pred[j])
            cand1 = (res[0][0],res[1][1])
            cand2 = (res[0][1],res[1][0])
            if sum(cand1)>sum(cand2):
                return(cand1)
            else:
                return(cand2)
        ids = jac_matrix([self.patients1, self.patients2],true_labels)
    
        print("Jaccard indices for two groups are {0} and {1}".format(round(ids[0],2),round(ids[1],2)))   
    
    def enrichment_analysis(self, library, output):
        '''
        Saves the results of enrichment analysis
        
        Attributes:
        -----------
        library - Enrichr library to be used. Recommendations: 
            - 'GO_Molecular_Function_2018'
            - 'GO_Biological_Process_2018'
            - 'GO_Cellular_Component_2018'
            for more options check available libraries by typing gseapy.get_library_name()
            
        output - directory name where results should be saved    
        '''
        libs = gseapy.get_library_name()
        assert library in libs, "the library is not available, check gseapy.get_library_name() for available options"
        all_genes_entr  = self.genes1 + self.genes2
        mg = mygene.MyGeneInfo()
        out = mg.querymany(all_genes_entr, scopes='entrezgene', fields='symbol', species='human', verbose = False)
        mapping =dict()
        rev_mapping = dict()
        for line in out:
            rev_mapping[line["symbol"]] = line["query"]
            mapping[line["query"]] = line["symbol"]
    
        genes1_name = [mapping[x] for x in self.genes1]
        genes2_name = [mapping[x] for x in self.genes2]
        all_genes_names = genes1_name+genes2_name
        gseapy.enrichr(gene_list=all_genes_names, description='pathway', gene_sets=library, cutoff = 0.05, outdir = output)