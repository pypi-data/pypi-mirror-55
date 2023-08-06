####
# bomail.util.util
#
# Various utility functions.
####

import os, sys
import shutil

from bomail.config.config import pathcfg
import bomail.util.datestuff as datestuff

def err_log(s):
  try:
    with open(pathcfg.error_log_file, "a") as f:
      f.write("\n================\n")
      f.write("---- " + datestuff.get_local_nowstr() + ":\n")
      f.write(s)
      f.write("\n\n")
  except:
    pass

def mv_file(src, dest):
  try:
    shutil.move(src, dest)
  except:
    error_log("util: could not move file\n" + traceback.format_exc() + "\n")
    with open(src) as f_src, open(dest, "w") as f_dest:
      f_dest.write(f_src.read())
    os.remove(src)

def mv_dir(src, dest):
  shutil.move(src, dest)


# merge lists, assuming they are in sorted order by key()
# using a key actually makes this significantly more complex
# partly because we don't want to call it unnecessarily
def merge_lists(a, b, key, reverse=False):
  if len(a) == 0:
    return b
  if len(b) == 0:
    return a
  new_list = []
  a_ind, b_ind = 0, 0
  a_key, b_key = key(a[0]), key(b[0])

  while True:
    choose_a = a_key >= b_key if reverse else a_key <= b_key
    if choose_a:
      new_list.append(a[a_ind])
      a_ind += 1
      if a_ind >= len(a):
        break
      a_key = key(a[a_ind])
    else:
      new_list.append(b[b_ind])
      b_ind += 1
      if b_ind >= len(b):
        break
      b_key = key(b[b_ind])

  # only one of the following loops will execute
  while b_ind < len(b):
    new_list.append(b[b_ind])
    b_ind += 1
  while a_ind < len(a):
    new_list.append(a[a_ind])
    a_ind += 1
  return new_list


# Input a is a list of values, sorted according to key().
# x_key is an output of key().
# Binary search, giving the position in a to insert x_key
# in order to maintain sorted order, breaking ties to the left.
# Based on the python 3 library's bisect function.
ident = lambda x: x
def bisect_left_key(a, x_key, key=ident, reverse=False, lo=0, hi=None):
  if hi is None:
    hi = len(a)
  while lo < hi:
    mid = int((lo+hi) / 2)
    mid_key = key(a[mid])
    # if it were bisect_right, we'd use <=
    is_above = (x_key < mid_key) if reverse else (mid_key < x_key)
    if is_above:
      lo = mid+1
    else:
      hi = mid
  return lo

