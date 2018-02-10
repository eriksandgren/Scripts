#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import operator

def recursion(z):
  return [2 * z - z * z, z * z]

def generatePolarCode(n, K, design_SNR):
  z = np.exp(-design_SNR)
  N = 2 ** n
  assert(K <= N)

  level = 0
  prev_leaves = [z]
  while level < n:
    leaves = []
    for leef in prev_leaves:
      leaves += recursion(leef)

    prev_leaves = leaves
    level += 1
  J = []
  max_value = max(leaves)
  for k in xrange(K):
    min_index, min_value = min(enumerate(leaves), key=operator.itemgetter(1))
    J.append(min_index)
    leaves[min_index] = max_value

  return sorted(J)

