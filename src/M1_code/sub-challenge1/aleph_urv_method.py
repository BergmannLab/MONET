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
#    along with DREAM DMI Tool. If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################
# Mattia Tomasoni - UNIL, CBG
# 2017 DREAM challenge on Disease Module Identification
# https://www.synapse.org/modulechallenge
###############################################################################

#===========================================================================================#
#  Disease Module Identification by Adjusting Resolution in Community Detection Algorithms  #
#  Sergio Gomez, Manlio De Domenico, Alex Arenas                                            #
#  Universitat Rovira i Virgili, Tarragona (Catalonia)                                      #
#  https://www.synapse.org/#!Synapse:syn7352969/wiki/407384                                 #
#                                                                                           #
#  Disease Module Identification DREAM Challenge                                            #
#  https://www.synapse.org/#!Synapse:syn6156761/wiki/400645                                 #
#                                                                                           #
#  Aleph URV Method                                                                         #
#  Contact: Sergio Gomez                                                                    #
#  sergio.gomez@urv.cat                                                                     #
#  http://deim.urv.cat/~sergio.gomez                                                        #
#===========================================================================================#


#=======================================
#  Global parameters
#=======================================

communities_detection_program = "./Communities_Detection.exe"

desired_average_degree = 25.0
desired_average_degree_tolerance = 0.2

min_community_size = 3
max_community_size = 100

debug_default = False

fn_id = 0


#=======================================
#  Packages
#=======================================

import sys
import re
import os
import os.path
import math
import random
import datetime   as dt
import subprocess as sp
import numpy      as np
import networkx   as nx


#=======================================
#  Elapsed time to string
#=======================================
def elapsed(t_ini, t_end):

  t_diff = t_end - t_ini

  hh = 24 * t_diff.days + int(t_diff.seconds / 3600)
  mm = int((t_diff.seconds % 3600) / 60)
  ss = t_diff.seconds % 60
  cs = int(t_diff.microseconds / 10000)

  elap = ""
  if hh > 0:
    elap += str(hh) + "h "
  if hh > 0 or mm > 0:
    elap += str(mm) + "m "
  elap += str(ss) + "." + str("%02d" % cs) + "s"

  return elap


#=======================================
#  Normalize weights
#=======================================
def normalize_weights(g):

  wh = [d for (i, j, d) in g.edges(data='weight')]
  mx = max(wh)
  if mx > 1.0:
    for (i, j, d) in g.edges(data=True):
      d['weight'] /= mx


#=======================================
#  Preprocessing
#=======================================
def preprocessing(fn_data, fn_net, is_undir, des_avg_deg, des_avg_deg_tol):

  print("    reading network")
  if is_undir:
    G = nx.read_edgelist(fn_data, data=(('weight', float),), create_using=nx.Graph())
  else:
    G = nx.read_edgelist(fn_data, data=(('weight', float),), create_using=nx.DiGraph())

  N = G.number_of_nodes()
  L = G.number_of_edges()
  avg_deg = L / N
  print("    number of nodes: %d" % N)
  print("    number of edges: %d" % L)
  print("    average degree : %.4f" % avg_deg)

  if avg_deg > des_avg_deg:
    print("    pruning")
    max_edges = int(N * des_avg_deg)
    if max_edges < L:
      wh = [d for (i, j, d) in G.edges(data='weight')]
      wh.sort()
      wh_min = wh[L - max_edges]
      # prune edges with lowest weights
      prune_list = []
      for (i, j, d) in G.edges(data='weight'):
        if d < wh_min:
          prune_list.append((i, j))
      G.remove_edges_from(prune_list)
      Lg = G.number_of_edges()
      avgk_g = Lg / N
      if abs(avgk_g - des_avg_deg) / des_avg_deg > des_avg_deg_tol:
        H = G.copy()
        prune_list = []
        for (i, j, d) in H.edges(data='weight'):
          if d <= wh_min:
            prune_list.append((i, j))
        H.remove_edges_from(prune_list)
        Lh = H.number_of_edges()
        avgk_h = Lh / N
        if abs(avgk_h - des_avg_deg) / des_avg_deg < des_avg_deg_tol:
          G = H

    new_L = G.number_of_edges()
    new_avg_deg = new_L / N
    print("    weights cutoff     : %.4f" % wh_min)
    print("    new number of edges: %d" % new_L)
    print("    new average degree : %.4f" % new_avg_deg)

  print("    normalizing network")
  normalize_weights(G)

  print("    writting network")
  nx.write_pajek(G, fn_net)


#=======================================
#  Get converters for id <--> name
#=======================================
def get_converters(g):

  names = {}
  ids = {}
  for (p, d) in g.nodes(data=True):
    if 'id' in d:
      names[d['id']] = p
      ids[p] = d['id']
    else:
      names[str(p)] = p
      ids[p] = str(p)

  return (names, ids)


#=======================================
#  Clear nodes attributes except 'id'
#=======================================
# provisional for NetworkX 2.1: leave only 'id' node attribute, remove others
def clear_attributes(g):
  for (p, d) in g.nodes(data=True):
    if 'id' in d:
      v = d['id']
      d.clear()
      d['id'] = str(v)


#=======================================
#  Convert NetworkX partition to standard form
#=======================================
def partition_nx_to_std(part_nx):

  dict = {}
  vals = set(part_nx.values())

  for v in vals:
    dict[v] = []
  for (k, v) in part_nx.items():
    dict[v].append(k)

  return list(dict.values())


#=======================================
#  Convert LoL partition to standard form
#=======================================
def partition_lol_to_std(part_lol, names):

  part_std = []
  for comm in part_lol:
    comm_names = [names[nod_id] for nod_id in comm]
    part_std.append(comm_names)

  return part_std


#=======================================
#  Convert standard partition to membership
#=======================================
def partition_std_to_memb(part_std, ids):

  part_memb = {}

  comm_id = 0
  for comm in part_std:
    comm_id += 1
    for name in comm:
      part_memb[ids[name]] = comm_id

  return part_memb


#=======================================
#  Read LoL partition
#=======================================
def read_lol(fn_lol, names):

  with open(fn_lol, 'r') as f:
    content = f.read().splitlines()

  mod_str = content[2].split('Q = ')[1]
  try:
    modularity = float(mod_str)
  except:
    modularity = 0.0
  num_nodes  = int(content[4].split(': ')[1])
  num_comms  = int(content[5].split(': ')[1])

  content = content[7:]
  partition = []
  for line in content:
    if len(line.split(':')) == 2:
      partition.append(line.split()[1:])

  partition = partition_lol_to_std(partition, names)

  return (partition, modularity)


#=======================================
#  Write pajek partition
#=======================================
def write_pajek_clu(fn_clu, part_memb):

  num_nodes = len(part_memb)
  with open(fn_clu, 'w') as f:
    f.write("*Vertices " + str(num_nodes) + "\n")
    for i in range(num_nodes):
      f.write(str(part_memb[str(i+1)]) + "\n")


#=======================================
#  Get partition info
#=======================================
def get_partition_info(partition, min_comm_size, max_comm_size, resolution, modularity):

  num_comms = len(partition)

  sizes = [len(comm) for comm in partition]
  sizes.sort()
  sizes = sizes[::-1]

  num_below  = 0
  num_above  = 0
  num_inside = 0
  nodes_below  = 0
  nodes_above  = 0
  nodes_inside = 0
  for size in sizes:
    if size < min_comm_size:
      num_below += 1
      nodes_below += size
    elif size > max_comm_size:
      num_above += 1
      nodes_above += size
    else:
      num_inside += 1
      nodes_inside += size

  num_nodes = nodes_inside + nodes_below + nodes_above

  partition_info = {}
  partition_info['resolution']   = resolution
  partition_info['num_nodes']    = num_nodes
  partition_info['num_comms']    = num_comms
  partition_info['num_inside']   = num_inside
  partition_info['num_below']    = num_below
  partition_info['num_above']    = num_above
  partition_info['nodes_inside'] = nodes_inside
  partition_info['nodes_below']  = nodes_below
  partition_info['nodes_above']  = nodes_above
  partition_info['modularity']   = modularity
  partition_info['max_size']     = sizes[0]
  partition_info['sizes_above']  = sizes[:num_above]

  return partition_info


#=======================================
#  Get partition info at minimum resolution
#=======================================
def get_partition_info_res_min(res_min, num_nodes, min_comm_size, max_comm_size):

  partition_info = {}
  partition_info['resolution'] = res_min
  partition_info['num_nodes']  = num_nodes
  partition_info['num_comms']  = 1
  partition_info['modularity'] = 0.0
  partition_info['max_size']   = num_nodes

  if num_nodes > max_comm_size:
    partition_info['num_inside']   = 0
    partition_info['num_below']    = 0
    partition_info['num_above']    = 1
    partition_info['nodes_inside'] = 0
    partition_info['nodes_below']  = 0
    partition_info['nodes_above']  = num_nodes
    partition_info['sizes_above']  = [num_nodes]
  elif num_nodes < min_comm_size:
    partition_info['num_inside']   = 0
    partition_info['num_below']    = 1
    partition_info['num_above']    = 0
    partition_info['nodes_inside'] = 0
    partition_info['nodes_below']  = num_nodes
    partition_info['nodes_above']  = 0
    partition_info['sizes_above']  = []
  else:
    partition_info['num_inside']   = 1
    partition_info['num_below']    = 0
    partition_info['num_above']    = 0
    partition_info['nodes_inside'] = num_nodes
    partition_info['nodes_below']  = 0
    partition_info['nodes_above']  = 0
    partition_info['sizes_above']  = []

  return partition_info


#=======================================
#  Get partition info at maximum resolution
#=======================================
def get_partition_info_res_max(res_max, num_nodes, min_comm_size, max_comm_size):

  partition_info = {}
  partition_info['resolution'] = res_max
  partition_info['num_nodes']  = num_nodes
  partition_info['num_comms']  = num_nodes
  partition_info['modularity'] = 1.0
  partition_info['max_size']   = 1

  if min_comm_size > 1:
    partition_info['num_inside']   = 0
    partition_info['num_below']    = num_nodes
    partition_info['num_above']    = 0
    partition_info['nodes_inside'] = 0
    partition_info['nodes_below']  = num_nodes
    partition_info['nodes_above']  = 0
    partition_info['sizes_above']  = []
  else:
    partition_info['num_inside']   = num_nodes
    partition_info['num_below']    = 0
    partition_info['num_above']    = 0
    partition_info['nodes_inside'] = num_nodes
    partition_info['nodes_below']  = 0
    partition_info['nodes_above']  = 0
    partition_info['sizes_above']  = []

  return partition_info


#=======================================
#  Find Radatools communities
#=======================================
def find_communities_radatools(fn_net, is_dir, num_nodes, resolution, names, fast, debug):

  # choose heuristics and repetitions
  if fast:
    radt_algs = "-llrfr"
    radt_reps = 1
  elif num_nodes <= 500:
    radt_algs = "-r-s-e-ll!rfr-trfr"
    radt_reps = 5
  elif num_nodes <= 1000:
    radt_algs = "-r-s-e-ll!rfr-trfr"
    radt_reps = 3
  elif num_nodes <= 1500:
    radt_algs = "-r-s-e-ll!rfr-trfr"
    radt_reps = 1
  elif num_nodes <= 5000:
    radt_algs = "-r-s-e-ll!rfr"
    radt_reps = 2
  elif num_nodes <= 10000:
    radt_algs = "-r-s-ll!rfr"
    radt_reps = 1
  else:
    radt_algs = "-rfr-llrfr"
    radt_reps = 1

  # perform communities detection calling Radatools
  if debug:
    fn_log = fn_net.replace(".net", "-stdout.log")
    stdo = open(fn_log, "w")
  else:
    stdo = sp.DEVNULL

  fn_lol = fn_net.replace(".net", "-lol.txt")
  if os.path.exists(fn_lol):
    os.remove(fn_lol)

  sp.run([communities_detection_program, "v", "WN", radt_algs, str(radt_reps), str(resolution), fn_net, fn_lol], stdout=stdo)

  if debug:
    stdo.close()

  partition, modularity = read_lol(fn_lol, names)

  return (partition, modularity)


#=======================================
#  Get subgraph
#=======================================
def get_subgraph(g, community, names):

  g_aux = g.subgraph(community).copy()
  gs = g.subgraph([]).copy()

  mapping = dict(zip(g_aux.nodes(), range(1, g_aux.number_of_nodes() + 1)))
  gs.add_nodes_from([(k, dict(id=v)) for (k, v) in mapping.items()])

  for (i, j, wh) in g_aux.edges(data='weight', default=1):
    if i != j:
      gs.add_edge(i, j, weight=wh)

  return gs


#=======================================
#  Remove selected files
#=======================================
def remove_selected_files(fn_net, selection):

  fn = fn_net.replace(".net", "")
  r = re.compile(fn + selection)

  with os.scandir(".") as sd:
    for entry in sd:
      if entry.is_file():
        if r.match(entry.name) != None:
          os.remove(entry.name)


#=======================================
#  Remove partition files
#=======================================
def remove_partition_files(fn_net):
  remove_selected_files(fn_net, "(-lol.txt|-lol.txt.log|-stdout.log)$")


#=======================================
#  Remove intermediate files
#=======================================
def remove_intermediate_files(fn_net):
  remove_selected_files(fn_net, "(.net|-lol.txt|-lol.txt.log|-stdout.log)$")


#=======================================
#  Remove all intermediate files
#=======================================
def remove_all_intermediate_files(fn_net):
  remove_selected_files(fn_net, "(-[0-9][0-9].*|-lol|-stdout).(net|net.clu|txt|txt.log|log)$")


#=======================================
#  Get strengths
#=======================================
def get_strengths(g, ids, is_dir):

  num_nodes = g.number_of_nodes()

  strength_out = [0.0 for i in range(num_nodes + 1)]
  strength_in  = [0.0 for i in range(num_nodes + 1)]
  total_strength = 0.0
  for (ii, jj, wh) in g.edges(data='weight', default=1):
    i = int(ids[ii])
    j = int(ids[jj])
    strength_out[i] += wh
    strength_in[j]  += wh
    if not is_dir and i != j:
      total_strength  += 2 * wh
    else:
      total_strength  += wh

  strength = [strength_out[i] + strength_in[i] for i in range(num_nodes + 1)]

  return (strength_out, strength_in, strength, total_strength)


#=======================================
#  Calculate modularity
#=======================================
def calculate_modularity(g, ids, is_dir, num_nodes, strengths, part_std, part_memb, resolution):

  num_nodes = g.number_of_nodes()

  strength_out, strength_in, strength, total_strength = strengths
  norm = total_strength + num_nodes * resolution

  # reward of links inside communities
  modularity = num_nodes * resolution
  if is_dir:
    # directed networks
    for (ii, jj, wh) in g.edges(data='weight', default=1):
      si, sj = ids[ii], ids[jj]
      if part_memb[si] == part_memb[sj]:
        modularity += wh
  else:
    # undirected network
    for (ii, jj, wh) in g.edges(data='weight', default=1):
      si, sj = ids[ii], ids[jj]
      if part_memb[si] == part_memb[sj]:
        if si == sj:
          modularity += wh
        else:
          modularity += 2 * wh

  # nullcase
  if is_dir:
    # directed networks
    for comm in part_std:
      sc_out = len(comm) * resolution
      sc_in  = len(comm) * resolution
      for ii in comm:
        si = ids[ii]
        i = int(si)
        sc_out += strength_out[i]
        sc_in  += strength_in[i]
      modularity -= sc_out * sc_in / norm
  else:
    # undirected networks
    for comm in part_std:
      sc = len(comm) * resolution
      for ii in comm:
        si = ids[ii]
        i = int(si)
        sc += strength[i]
      modularity -= sc * sc / norm

  # global normalization
  modularity /= norm

  return modularity


#=======================================
#  Get resolution range
#=======================================
def get_resolution_range(g, ids, num_nodes, strengths):

  eps = 1.e-4

  strength_out, strength_in, strength, total_strength = strengths

  r_min = - total_strength / num_nodes

  r_max = r_min

  if not g.is_directed():
    # undirected network
    for (ii, jj, wh) in g.edges(data='weight', default=1):
      i = int(ids[ii])
      j = int(ids[jj])
      b = strength[i] + strength[j] - num_nodes * wh;
      c = strength[i] * strength[j] - total_strength * wh
      disc = b * b - 4 * c
      if disc >= 0:
        x = (-b + math.sqrt(disc)) / 2
        if x > r_max:
          r_max = x
  else:
    # directed networks
    for (ii, jj, whij) in g.edges(data='weight', default=1):
      i = int(ids[ii])
      j = int(ids[jj])
      if g.has_edge(jj, ii):
        whji = g.edges[jj, ii]['weight']
      else:
        whji = 0.0
      a = 2
      b = strength_out[i] + strength_in[j] + strength_out[j] + strength_in[i] - num_nodes * (whij + whji)
      c = strength_out[i] * strength_in[j] + strength_out[j] * strength_in[i] - total_strength * (whij + whji)
      disc = b * b - 4 * a * c
      if disc >= 0:
        x = (-b + math.sqrt(disc)) / (2 * a)
        if x > r_max:
          r_max = x

  r_min *= 1. - eps
  r_max *= 1. + eps

  return (r_min, r_max)


#=======================================
#  Print if in debug mode
#=======================================
def print_debug(s, debug):
  if debug:
    print(s)


#=======================================
#  Print partitions info if in debug mode
#=======================================
def print_info_debug(pinfo1, pinfo, pinfo2, res1, res, res2, debug):
  if debug:
    num_nodes = pinfo['num_nodes']
    nc = pinfo1['num_comms'], pinfo['num_comms'], pinfo2['num_comms']
    ms = pinfo1['max_size'], pinfo['max_size'], pinfo2['max_size']
    na = pinfo1['nodes_above'] / num_nodes * 100, pinfo['nodes_above'] / num_nodes * 100, pinfo2['nodes_above'] / num_nodes * 100
    qs = pinfo1['modularity'], pinfo['modularity'], pinfo2['modularity']
    rs = res1, res, res2
    print("        %d  %d  %d  |  %d  %d  %d  |  %.2f%%  %.2f%%  %.2f%%  |  %.4f  %.4f  %.4f  |  %.4f  %.4f  %.4f" % (*nc, *ms, *na, *qs, *rs))


#=======================================
#  Weighted mean
#=======================================
def weighted_mean(val1, val2, wh1, wh2):
  return (wh1 * val1 + wh2 * val2) / (wh1 + wh2)


#=======================================
#  Adjust minimum resolution
#=======================================
def adjust_minimum_resolution(g, names, ids, res_min, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, fast, debug):

  num_res = 100
  if num_nodes <= 1000:
    num_steps = 10
  elif num_nodes <= 5000:
    num_steps = 8
  elif num_nodes <= 10000:
    num_steps = 6
  else:
    num_steps = 4

  print_debug("      r_min", debug)

  # initialize
  res_list = np.linspace(res_min, 0.0, num=num_res+1, endpoint=True)[1:]
  pinfo_list = [get_partition_info_res_min(r, num_nodes, min_comm_size, max_comm_size) for r in res_list]
  qs_max = np.zeros(num_res)
  i_used = set()
  i_rem = set(range(num_res))

  # iterate to improve minimum resolution
  for step in range(num_steps):
    qmin = min(qs_max)
    pos_min = [i for i in range(num_res) if qs_max[i] == qmin]
    pos_min_left = min(pos_min)
    pos_min_right = max(pos_min)
    if not is_dir:
      if step == 0:
        ic = num_res - 1
      elif pos_min_right in i_rem:
        ic = pos_min_right
      else:
        break
    else:
      pos_inc = max([i for i in range(1, num_res) if qs_max[i-1] >= qs_max[i]])
      if step == 0:
        ic = num_res - 1
      elif step == 1:
        ic = 0
      elif qmin == 0.0 and pos_min_left in i_rem:
        ic = pos_min_left
      elif pos_min_right in i_rem:
        ic = pos_min_right
      elif pos_inc in i_rem:
        ic = pos_inc
      else:
        break

    res = res_list[ic]
    partition, q = find_communities_radatools(fn_net, is_dir, num_nodes, res, names, fast, debug)
    pinfo = get_partition_info(partition, min_comm_size, max_comm_size, res, q)
    remove_partition_files(fn_net)
    part_memb = partition_std_to_memb(partition, ids)
    print_debug("        r = %.4f    q = %.4f    nc = %d" % (res, q, pinfo['num_comms']), debug)
    i_used |= {ic}
    i_rem -= {ic}

    if pinfo['num_comms'] > 1:
      for j in range(num_res):
        r = res_list[j]
        q = calculate_modularity(g, ids, is_dir, num_nodes, strengths, partition, part_memb, r)
        if q > qs_max[j]:
          qs_max[j] = q
          pinfo_list[j] = get_partition_info(partition, min_comm_size, max_comm_size, r, q)

  # choose final minimum resolution
  if not is_dir:
    qmin = min(qs_max)
    pos_min_right = max([i for i in range(num_res) if qs_max[i] == qmin])
    ic = pos_min_right
  else:
    pos_inc = max([i for i in range(1, num_res) if qs_max[i-1] >= qs_max[i]])
    ic = pos_inc

  # save modularity profile
  if debug:
    with open(fn_net.replace(".net", "-rmin.txt"), 'w') as f:
      f.write("resolution\tq_max\tnum_comms\n")
      for i in range(num_res):
        f.write("%.6f\t%.6f\t%d\n" % (res_list[i], qs_max[i], pinfo_list[i]['num_comms']))

  return (res_list[ic], pinfo_list[ic])


#=======================================
#  Resolution bisection
#=======================================
def resolution_bisection(g, names, ids, lt_left, gt_right, res_min, res_max, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, debug):

  num_steps = 6
  wh_left   = 0.8
  wh_right  = 0.2
  fast = True

  print_debug("      res_min = %.4f    res_max = %.4f" % (res_min, res_max), debug)

  # min, max partition info
  pinfo_min = get_partition_info_res_min(res_min, num_nodes, min_comm_size, max_comm_size)
  pinfo_max = get_partition_info_res_max(res_max, num_nodes, min_comm_size, max_comm_size)

  # adjust res_min
  res_min, pinfo_min = adjust_minimum_resolution(g, names, ids, res_min, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, fast, debug)

  res_ice, pinfo_ice = res_max, pinfo_max

  # find initial bounds of resolution
  print_debug("      init", debug)
  res1, res2 = res_min, res_max
  pinfo1, pinfo2 = pinfo_min, pinfo_max
  while True:
    res = weighted_mean(res1, res2, wh_left, wh_right)
    partition, q = find_communities_radatools(fn_net, is_dir, num_nodes, res, names, fast, debug)
    pinfo = get_partition_info(partition, min_comm_size, max_comm_size, res, q)
    remove_partition_files(fn_net)
    print_info_debug(pinfo1, pinfo, pinfo2, res1, res, res2, debug)
    if 2 <= pinfo['num_comms'] < pinfo_ice['num_comms']:
      res_ice, pinfo_ice = res, pinfo
    if gt_right(pinfo):
      res2, pinfo2 = res, pinfo
    elif lt_left(pinfo):
      res1, pinfo1 = res, pinfo
    else:
      res_mid, pinfo_mid = res, pinfo
      break

  # fine tuning of left resolution
  print_debug("      left", debug)
  r1, r2 = res1, res_mid
  p1, p2 = pinfo1, pinfo_mid
  for step in range(num_steps):
    r = weighted_mean(r1, r2, wh_left, wh_right)
    partition, q = find_communities_radatools(fn_net, is_dir, num_nodes, r, names, fast, debug)
    pinfo = get_partition_info(partition, min_comm_size, max_comm_size, r, q)
    remove_partition_files(fn_net)
    print_info_debug(p1, pinfo, p2, r1, r, r2, debug)
    if 2 <= pinfo['num_comms'] < pinfo_ice['num_comms']:
      res_ice, pinfo_ice = r, pinfo
    if lt_left(pinfo):
      r1, p1 = r, pinfo
    else:
      r2, p2 = r, pinfo
  if p2['num_comms'] == 1:
    res_left = None
  elif p1['num_comms'] == 1:
    res_left = r2
  else:
    res_left = weighted_mean(r1, r2, wh_left, wh_right)

  # fine tuning of right resolution
  print_debug("      right", debug)
  r1, r2 = res_mid, res2
  p1, p2 = pinfo_mid, pinfo2
  for step in range(num_steps):
    r = weighted_mean(r1, r2, wh_left, wh_right)
    partition, q = find_communities_radatools(fn_net, is_dir, num_nodes, r, names, fast, debug)
    pinfo = get_partition_info(partition, min_comm_size, max_comm_size, r, q)
    remove_partition_files(fn_net)
    print_info_debug(p1, pinfo, p2, r1, r, r2, debug)
    if 2 <= pinfo['num_comms'] < pinfo_ice['num_comms']:
      res_ice, pinfo_ice = r, pinfo
    if gt_right(pinfo):
      r2, p2 = r, pinfo
    else:
      r1, p1 = r, pinfo
  if p2['num_comms'] == 1:
    res_right = None
  elif p1['num_comms'] == 1:
    res_right = r2
  else:
    res_right = weighted_mean(r1, r2, wh_left, wh_right)

  # choose final resolution
  if res_left == None or res_right == None:
    res = res_ice
  else:
    res = weighted_mean(res_left, res_right, wh_left, wh_right)

  if is_dir and res != res_ice:
    partition, q = find_communities_radatools(fn_net, is_dir, num_nodes, res, names, fast, debug)
    pinfo = get_partition_info(partition, min_comm_size, max_comm_size, res, q)
    remove_partition_files(fn_net)
    if pinfo['num_comms'] == 1:
      res = res_ice

  return res


#=======================================
#  Find resolution
#=======================================
def find_resolution(g, names, ids, fn_net, is_dir, num_nodes, min_comm_size, max_comm_size, debug):

  strengths = get_strengths(g, ids, is_dir)
  res_min, res_max = get_resolution_range(g, ids, num_nodes, strengths)
  resolution = 0

  if num_nodes > 50 * max_comm_size:
    # find a resolution such that 45% < nodes_above / num_nodes < 55%
    # lt_left  = lambda pinfo: pinfo['nodes_above'] / num_nodes > 0.55
    # gt_right = lambda pinfo: pinfo['nodes_above'] / num_nodes < 0.45
    # resolution = resolution_bisection(g, names, ids, lt_left, gt_right, res_min, res_max, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, debug)

    # simple rule to avoid search of resolution for large networks
    resolution = (num_nodes - 50 * max_comm_size) / 100

  elif num_nodes > 10 * max_comm_size:
    # find a resolution such that max_comm_size / 2 < max_size < 4 * max_comm_size
    lt_left  = lambda pinfo: pinfo['max_size'] > 4 * max_comm_size
    gt_right = lambda pinfo: pinfo['max_size'] < max_comm_size / 2
    resolution = resolution_bisection(g, names, ids, lt_left, gt_right, res_min, res_max, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, debug)

  elif num_nodes > 5 * max_comm_size:
    # find a resolution such that max_comm_size / 3 < max_size < 2 * max_comm_size
    lt_left  = lambda pinfo: pinfo['max_size'] > 2 * max_comm_size
    gt_right = lambda pinfo: pinfo['max_size'] < max_comm_size / 3
    resolution = resolution_bisection(g, names, ids, lt_left, gt_right, res_min, res_max, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, debug)

  elif num_nodes > max_comm_size:
    # find a resolution such that max_comm_size / 4 <= max_size <= max_comm_size
    lt_left  = lambda pinfo: pinfo['max_size'] > max_comm_size
    gt_right = lambda pinfo: pinfo['max_size'] < max_comm_size / 4
    resolution = resolution_bisection(g, names, ids, lt_left, gt_right, res_min, res_max, fn_net, is_dir, num_nodes, strengths, min_comm_size, max_comm_size, debug)

  else:
    resolution = 0

  return resolution


#=======================================
#  Find new name for a file
#=======================================
def new_name(fn, i):
  global fn_id
  length_cutoff = 80

  pos_dot  = fn.rfind('.')
  fn_name  = fn[:pos_dot]
  fn_ext   = fn[pos_dot:]
  has_plus = fn_name[-4] == '+'

  if len(fn) < length_cutoff:
    si = "-%02d" % i
    name = fn[:-4] + si + fn_ext
  elif not has_plus:
    fn_id += 1
    si = "+%03d" % fn_id
    name = fn_name + si + fn_ext
  else:
    fn_id += 1
    si = "+%03d" % fn_id
    name = fn_name[:-4] + si + fn_ext

  return name


#=======================================
#  Find communities by recursion
#=======================================
def find_communities_by_recursion(fn_net, min_comm_size, max_comm_size, debug):

  # read network, calculate connected components, and several initializations
  print("    " + fn_net, flush=True)
  g = nx.read_pajek(fn_net)
  is_dir = g.is_directed()
  if is_dir:
    g = nx.DiGraph(g)
    comps = [list(c) for c in sorted(nx.weakly_connected_components(g), key=len, reverse=True)]
  else:
    g = nx.Graph(g)
    comps = [list(c) for c in sorted(nx.connected_components(g), key=len, reverse=True)]
  num_nodes = g.number_of_nodes()
  num_comps = len(comps)
  print("      " + str(num_nodes) + " nodes", flush=True)

  names, ids = get_converters(g)

  # analize separately each connected component
  if num_comps > 1:
    print("      connectivity: " + str(num_comps) + " connected components", flush=True)
    gcc_pc = 100 * len(comps[0]) / num_nodes
    print("      GCC  size   : %5.2f%%    (%d nodes)" % (gcc_pc, len(comps[0])), flush=True)
    slcc_pc = 100 * len(comps[1]) / num_nodes
    print("      SLCC size   : %5.2f%%    (%d nodes)" % (slcc_pc, len(comps[1])), flush=True)
    if num_comps > 2:
      not_gcc_pc = 100 - gcc_pc
      print("      not in GCC  : %5.2f%%    (%d nodes)" % (not_gcc_pc, num_nodes - len(comps[0])), flush=True)
    # recursive community detection of too large components
    part_end = []
    i = 0
    pending_nets = []
    for comm in comps:
      size = len(comm)
      if size <= max_comm_size:
        part_end.append(comm)
      else:
        # write pending components
        gs = get_subgraph(g, comm, names)
        i += 1
        fn_sub_net = new_name(fn_net, i)
        clear_attributes(gs)
        nx.write_pajek(gs, fn_sub_net)
        pending_nets.append(fn_sub_net)
    # process pending components
    for fn_sub_net in pending_nets:
      part_sub = find_communities_by_recursion(fn_sub_net, min_comm_size, max_comm_size, debug)
      part_end += part_sub
    return part_end

  t_ini = dt.datetime.now()

  # select appropriate resolution
  print("      finding resolution")
  resolution = find_resolution(g, names, ids, fn_net, is_dir, num_nodes, min_comm_size, max_comm_size, debug)

  # community detection with Radatools
  print("      finding modules")
  part_ini, q = find_communities_radatools(fn_net, is_dir, num_nodes, resolution, names, False, debug)

  print("      Q = %.6f    %d modules    r = %.6f" % (q, len(part_ini), resolution), end="", flush=True)

  # print elapsed time if long enough
  t_end = dt.datetime.now()
  if (t_end - t_ini).seconds >= 60:
    print("    " + elapsed(t_ini, t_end), flush=True)
  else:
    print()

  # check size of partition to avoid recursion
  if len(part_ini) == 1:
    print("      Error: the partition has just one community!")
    quit()

  # clean up
  if not debug:
    remove_intermediate_files(fn_net)

  # recursive community detection of too large modules
  part_end = []
  i = 0
  pending_nets = []
  for comm in part_ini:
    size = len(comm)
    if size <= max_comm_size:
      part_end.append(comm)
    else:
      # write pending subnetworks
      gs = get_subgraph(g, comm, names)
      i += 1
      fn_sub_net = new_name(fn_net, i)
      clear_attributes(gs)
      nx.write_pajek(gs, fn_sub_net)
      pending_nets.append(fn_sub_net)
  # process pending subnetworks
  for fn_sub_net in pending_nets:
    part_sub = find_communities_by_recursion(fn_sub_net, min_comm_size, max_comm_size, debug)
    part_end += part_sub

  # clean up
  if not debug:
    remove_all_intermediate_files(fn_net)

  return part_end


#=======================================
#  Save partition
#=======================================
def save_partition(fn_out, partition):

  partition.sort(key=lambda comm: len(comm), reverse=True)
  comm_id = 0
  with open(fn_out, "w") as f:
    for comm in partition:
      comm_id += 1
      f.write("%d\t1.0\t" % comm_id)
      f.write("\t".join(comm) + "\n")


#=======================================
#  Check partition consistency
#=======================================
def check_partition(fn_net, partition):

  g = nx.read_pajek(fn_net)
  nodes_g = set(g.nodes())
  nodes_p = set([nod for comm in partition for nod in comm])
  if nodes_p != nodes_g:
    print("  Error: nodes in network and final partition do not match")
    g_minus_p = nodes_g - nodes_p
    p_minus_g = nodes_p - nodes_g
    if len(g_minus_p) > 0:
      print()
      print("  Missing nodes:")
      print(g_minus_p)
    if len(p_minus_g) > 0:
      print()
      print("  Unknown nodes:")
      print(p_minus_g)
    quit()

  names, ids = get_converters(g)
  part_memb = partition_std_to_memb(partition, ids)
  write_pajek_clu(fn_net + ".clu", part_memb)


#=======================================
#  prepare command line arguments
#=======================================
def prepare_sys_argv(sys_argv):

  is_undir = True
  linksdir = sys_argv[1].lower()
  if linksdir not in ["undirected", "directed"]:
    print("Warning: '" + linksdir + "' is unknown value of 'linksdir' parameter, must be [undirected | directed]")
    print("         Choosing the default value: 'undirected'")
  if linksdir == "directed":
    is_undir = False

  des_avg_deg = desired_average_degree
  avgk = float(sys_argv[2])
  if avgk > 0.0:
    des_avg_deg = avgk

  min_comm_size = min_community_size
  smallest = int(sys_argv[3])
  if smallest > 0:
    min_comm_size = smallest

  max_comm_size = max_community_size
  largest = int(sys_argv[4])
  if largest >= min_comm_size:
    max_comm_size = largest

  return {'is_undir'      : is_undir,
          'des_avg_deg'   : des_avg_deg,
          'min_comm_size' : min_comm_size,
          'max_comm_size' : max_comm_size}


#=======================================
#  Find communities
#=======================================
def find_communities(fn_data, fn_out, is_undir, des_avg_deg=desired_average_degree, des_avg_deg_tol=desired_average_degree_tolerance, min_comm_size=min_community_size, max_comm_size=max_community_size, debug=debug_default):

  params = locals()
  t_ini = dt.datetime.now()

  print("------")
  if not os.path.exists(fn_data):
    print("Error: file '" + fn_data + "' not found")
    quit()

  print("Community detection")
  print(fn_data + " -> " + fn_out)

  print("  Parameters")
  for k, v in params.items():
    print("    " + k + " : " + str(v))

  fn_net = "urv-" + fn_data.replace(".txt", ".net")
  remove_all_intermediate_files(fn_net)

  print("  Preprocessing")
  print("  " + fn_data + " -> " + fn_net)
  preprocessing(fn_data, fn_net, is_undir, des_avg_deg, des_avg_deg_tol)

  print("  Finding community structure")
  print("  " + fn_net + " -> " + fn_out)
  partition = find_communities_by_recursion(fn_net, min_comm_size, max_comm_size, debug)

  print("  Saving partition")
  print("  " + fn_out)
  save_partition(fn_out, partition)

  print("  Finalizing")
  if debug:
    check_partition(fn_net, partition)
  else:
    remove_all_intermediate_files(fn_net)

  t_end = dt.datetime.now()
  print("  Elapsed time:  " + elapsed(t_ini, t_end))


#=======================================
#  Main
#=======================================

#find_communities("1_ppi_anonym_v2.txt"            , "1_ppi_anonym_v2-comms.txt"            , is_undir=True , debug=False)
#find_communities("2_ppi_anonym_v2.txt"            , "2_ppi_anonym_v2-comms.txt"            , is_undir=True , debug=False)
#find_communities("3_signal_anonym_directed_v3.txt", "3_signal_anonym_directed_v3-comms.txt", is_undir=False, debug=False)
#find_communities("4_coexpr_anonym_v2.txt"         , "4_coexpr_anonym_v2-comms.txt"         , is_undir=True , debug=False)
#find_communities("5_cancer_anonym_v2.txt"         , "5_cancer_anonym_v2-comms.txt"         , is_undir=True , debug=False)
#find_communities("6_homology_anonym_v2.txt"       , "6_homology_anonym_v2-comms.txt"       , is_undir=True , debug=False)

cmd_args = prepare_sys_argv(sys.argv)

find_communities("input.txt", "output.txt", debug=True, **cmd_args)
