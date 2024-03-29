#!/usr/bin/env Rscript
# Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch>
#
# This file is part of DREAM DMI Tool.
#
#    DREAM DMI Tool is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DREAM DMI Tool is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DREAM DMI Tool. If not, see <https://www.gnu.org/licoenses/>.
#
###############################################################################
# Mattia Tomasoni - UNIL, CBG
# 2017 DREAM challenge on Disease Module Identification
# https://www.synapse.org/modulechallenge
###############################################################################

rescale<-function(x,graph,maximum,minimum){
  numV<-vcount(graph)
  return((numV-1)/(maximum-minimum)*(x-maximum)+numV)
}

main <- function(file,b=2,c=5000,i=2,filter,threshold=2,inteWeight="yes",weighted=T,dir,post,smallest,largest,b2,c2,i2){
  input<-read.table(file,sep='\t')
  isString = FALSE
  if (is.integer(input$V1) & is.integer(input$V2) ){
    #add 1 to node number since DREAM dataset starts at 0.
    input[,1:2] <- input[,1:2]+1
  }
  else{
    # for using string as gene name, we transfom the strings to integer and map back at the end.
    isString = TRUE
    dict=unique(c(as.character(input$V1), as.character(input$V2)))
    input$V1 = as.numeric(factor(input$V1,levels = dict))
    input$V2 = as.numeric(factor(input$V2, levels = dict))
  }
  
  # if max(node_id)-min(node_id) > 2 * #nodes
  # get a dictionary that maps the original nodes IDs to start from ONE
  if (max(input[,1])-min(input[,1]) > 2* length(unique(input[,1]))){
    print("Performing Node ID remapping")
    input_new = input
    nodes = sort(union(input_new$V1, input_new$V2))
    nodes_ordered = 1:length(nodes)
    
    assign_hash <- Vectorize(assign, vectorize.args = c("x", "value"))
    get_hash <- Vectorize(get, vectorize.args = "x")
    # exists_hash <- Vectorize(exists, vectorize.args = "x")
    hash <- new.env(hash = TRUE, parent = emptyenv(), size = 10000L)
    assign_hash(as.character(nodes), nodes_ordered, hash)
    
    # map original input to input_new that starts from ONE
    for (iterator in 1:nrow(input_new)){
      input_new[iterator,1] = get_hash(as.character(input[iterator,1]), hash)
      input_new[iterator,2] = get_hash(as.character(input[iterator,2]), hash)
    }
    input = input_new
  }

  print("Read input finished!")
  graph<-preProcessing(input,filter,threshold,integerWeight=inteWeight)
  generateFile(graph,weighted)
  print("Clustering start!")
  system(paste("./mlrmcl -b ",b," -c ",c," -i ",i," -o output.txt test.txt",sep=""))
  output<-postProcessing(post,smallest,largest,graph,b2,c2,i2)
  
  # map input_new starting from ONE back, to the original inputs using dictionary
  if (max(input[,1])-min(input[,1]) >  2 * length(unique(input[,1]))){
    hash2 <- new.env(hash = TRUE, parent = emptyenv(), size = 10000L)
    assign_hash(as.character(nodes_ordered), nodes, hash2)
    for (iterator in 1:length(output)){
      if (length(output)>0){
        for (iterator2 in 1:length(output[[iterator]])){
          output[[iterator]][iterator2] = get_hash(as.character(output[[iterator]][iterator2]+1), hash2)
        }
      }
    }
  }
  
  # If the input is STRING nodes, translate integer back to strings
  if(isString == TRUE){
    # add 1 since postProcessing is not changed, still for DREAM data with 0 as gene id. 
    for (i in 1:length(output)){
      temp = output[[i]] + 1
      for (j in 1:length(temp)){
        temp[j] = dict[as.numeric(temp[j])]
      }
      output[[i]] <- temp
    }
  }
  writeFile(output,basename(file),dir)
  return(output)
  file.remove("output.txt")
  file.remove("test.txt")
}
preProcessing <- function(input,method=c("quantile","pageRank","double"),i,integerWeight = c("yes","no","1")){
  if (method=="quantile"){
    filter<-input[,3] >= quantile(input[,3])[i]
#     # filter<-input[,3] >= 0.25
    input<-input[filter,]
  }
  if (method=="pageRank"){
    graph <- make_graph(c(t(input[,1:2])),directed=FALSE)
    pageRank=page_rank(graph,directed = FALSE,weights = input[,3])$vector
    index=which(pageRank>quantile(pageRank)[i])
    filter<-input[,3] >= quantile(input[,3])[i]
    input<-input[filter,]
  }
  if (method=="double"){
    filter<-input[,3] >= quantile(input[,3])[i]
    # filter<-input[,3] >= 0.25
    input<-input[filter,]
    graph <- make_graph(c(t(input[,1:2])),directed=FALSE)
    pageRank=page_rank(graph,directed = FALSE,weights = input[,3])$vector
    index=which(pageRank>quantile(pageRank)[i])
    filter<-input[,3] >= quantile(input[,3])[i]
    input<-input[filter,]
  }

  graph <- make_graph(c(t(input[,1:2])),directed=FALSE)
  if (integerWeight=="yes"){
    maximum<-max(input[,3])
    minimum<-min(input[,3])
    if (maximum==minimum){
      E(graph)$weight=as.numeric(input[,3])
    } else{
      rescale <- function(x,max,min) (x-minimum)/(maximum - minimum) * 100
      w<-as.integer(rescale(input[,3]))
      E(graph)$weight=as.numeric(w)
    }
  }
  else if (integerWeight=="no")
    E(graph)$weight<-as.numeric(input[,3])
  else 
    E(graph)$weight<-1
  return(graph)
}

# THIS VERSION OF generateFile
# 
# SOLVES ISSUE 15 https://github.com/BergmannLab/MONET/issues/15
# - MONET/.test/system_test/retinal_toxicity_test.sh PASSES
# BUT CAUSES ERROR IN SYSTEM TESTS
# - MONET/.test/system_test/reproduce_challenge

# generateFile <- function(graph,weighted=T){
#  test3<-get.adjacency(graph,attr = "weight")
#  m.index<-get.adjlist(graph)
#  graph_directed <- as.directed(graph)
#  m.weight <- get.edge.attribute(graph_directed,name = "weight")
#  # m<-as.matrix(test3)
#  if (weighted){
#    # test<-sapply(1:nrow(m), function(i) m[i,m.index[[i]]])
#    temp2<-list()
#    # temp2_t <- list()
#    count <- 1
#    for (i in 1:length(m.index)){
#      num_edge_i = length(m.index[[i]])
#      if (num_edge_i == 0){
#        temp2[[i]]<-c(rbind(as.character(m.index[[i]]),numeric(0)))
#      } else{
#        edge_weight_i <- m.weight[count:(count+num_edge_i-1)]
#        # temp2_t[[i]]<-c(rbind(as.character(m.index[[i]]),test[[i]]))
#        temp2[[i]]<-c(rbind(as.character(m.index[[i]]),edge_weight_i))
#        count <- count + num_edge_i
#      }
#    }
#    fn <- "test.txt"
#    if (file.exists(fn)) file.remove(fn)
#    write(c(vcount(graph),ecount(graph),1),file="test.txt",sep="\t")
#    dummy<-lapply(temp2, write, "test.txt", ncolumns = length(temp2), append=TRUE,sep="\t")
#  }
#  else{
#    fn <- "test.txt"
#    if (file.exists(fn)) file.remove(fn)
#    write(c(vcount(graph),ecount(graph)),file="test.txt",sep="\t")
#    dummy<-lapply(m.index, write, "test.txt", ncolumns = length(m.index), append=TRUE,sep="\t")
#  }
# }

generateFile <- function(graph,weighted=T){
  test3<-get.adjacency(graph,attr = "weight")
  m<-as.matrix(test3)
  m.index<-apply(m!=0,1,which,arr.ind=T)
  # weight<-m[m.index]
  if (weighted){
    test<-sapply(1:nrow(m), function(i) m[i,m.index[[i]]])
    temp2<-list()
    for (i in 1:length(m.index)){
      temp2[[i]]<-c(rbind(as.character(m.index[[i]]),test[[i]]))
    }
    fn <- "test.txt"
    if (file.exists(fn)) file.remove(fn)
    write(c(vcount(graph),ecount(graph),1),file="test.txt",sep="\t")
    dummy<-lapply(temp2, write, "test.txt", ncolumns = length(temp2), append=TRUE,sep="\t")
  }
  else{
    fn <- "test.txt"
    if (file.exists(fn)) file.remove(fn)
    write(c(vcount(graph),ecount(graph)),file="test.txt",sep="\t")
    dummy<-lapply(m.index, write, "test.txt", ncolumns = length(m.index), append=TRUE,sep="\t")
  }
}

postProcessing <- function(method=c("random","discard","recluster"),smallest = 3,largest=100,
                           g=graph,b2,c2,i2){
  result<-read.table("output.txt")
  output<-list()
  # for (i in 1:nrow(unique(result))){
  for (i in 0:nrow(unique(result))){
    # output[[i]]<-which(result==i)-1 # minus 1 for node numbering
    output[[i+1]]<-which(result==i)-1 # minus 1 for node numbering
  }
  #remove clusters size < 3
  output<-output[lapply(output,length)>=smallest]
  if (method=="random"){

    #need some strategy for cluster size > 100, current randomly split
    output1<-output[lapply(output,length)<=100]
    
    temp<-output[lapply(output,length)>100]
    for (i in 1:length(temp)){
      output1<-append(output1,split(temp[[i]],1:ceiling(length(temp[[i]])/100)))
    }
    output<-output1
  }
  if (method=="discard"){

    #remove cluster size >100
    print(sum(lapply(output,length)>100))
    output<-output[lapply(output,length)<=100]
  }
  if (method=="recluster"){
      rerun<-function(graph,large,smallest){
        index<-unlist(large)+1
        graph.new<-induced_subgraph(g,index,"copy_and_delete")
        V(graph.new)$name<-as.character(index)
        #reclustered with MLRMCL
        generateFile(graph.new,weighted=T)
        system(paste("./mlrmcl -b ",b2," -c ",c2," -i ",i2," -o output2.txt test.txt",sep=""))
        result<-read.table("output2.txt")
        output2<-list()
        for (i in 1:nrow(unique(result))){
          output2[[i]]<-as.integer(V(graph.new)$name[which(result==i)])-1 # minus 1 for node numbering
        }
        output2<-output2[lapply(output2,length)>smallest]
        return(output2)
      }
      good<-output[lapply(output,length)<=100]
      
      large<-output[lapply(output,length)>100]
      temp<-list()
      i=1
      while(length(large)>0 && i<4){
        print(i)
        i=i+1
        splitted<-rerun(graph,large,smallest)
        small<-splitted[lapply(splitted,length)<=100]
        large<-splitted[lapply(splitted,length)>100]
        temp<-append(temp,small)
      }
      output<-append(good,temp)
  }
  output<-output[lapply(output,length)<=largest]
  return(output)
}

writeFile <- function(output,file,dir){
  dir.create(dir, showWarnings = FALSE)
  fn <- paste(dir,"/",file,sep="")
  if (file.exists(fn)) file.remove(fn)
  file.remove("output.txt")
  if (file.exists("output2.txt")) file.remove("output2.txt")
  file.remove("test.txt")
  for (i in 1:length(output)){
    if (length(output)>0)
      {temp<-c(i,1,output[[i]])
      write(temp,file=fn, ncolumns = length(output[[i]])+2, append=T, sep="\t")}
    else{
      write("No satisfactory clusters found",file=fn)
    }
  }
}



