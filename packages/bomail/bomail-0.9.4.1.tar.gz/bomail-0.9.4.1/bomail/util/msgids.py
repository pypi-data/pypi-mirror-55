####
# bomail.util.msgids
#
# Given a message-id, look up if we have an email file for it.
# Basically a wrapper for reading and writing to plain text file
#
# line format: msgid filename
####

import os, sys

from bomail.config.config import pathcfg
import bomail.util.merge_lines as merge_lines
import bomail.util.remove_lines as remove_lines
import bomail.util.util as util


def msgid_file_line(msgid, filename):
  return msgid.strip() + " " + filename


def get_idfile_lines(msg_id_list, filename_list):
  return sorted([msgid_file_line(m, f) for m,f in zip(msg_id_list,filename_list)])


# given a dictionary mapping all message-ids to their filenames, rewrite the file
def rewrite_from_dict(ids_to_fnames):
  slist = [msgid + " " + fname for msgid,fname in ids_to_fnames.items()]
  slist.sort()
  with open(pathcfg.msg_ids_file, "w") as f:
    f.write("\n".join(slist))


class Ids:
  def __init__(self):
    # map msgid to filename
    self.ids_to_fnames = {}
    if os.path.exists(pathcfg.msg_ids_file):
      with open(pathcfg.msg_ids_file) as f:
        for line in f:
          if " " not in line:
            continue
          ind = line.index(" ")
          if ind+1 >= len(line):
            continue
          msgid = line[:ind].strip()
          fname = line[ind+1:].strip()
          self.ids_to_fnames[msgid] = fname

  def has(self, msg_id):
    return msg_id in self.ids_to_fnames

  def get(self, msg_id):
    return self.ids_to_fnames[msg_id]

  def add(self, msg_id_list, fname_list):
    for m,f in zip(msg_id_list, fname_list):
      self.ids_to_fnames[m] = f
    merge_lines.do(pathcfg.msg_ids_file, get_idfile_lines(msg_id_list, fname_list))

  def remove(self, msg_id_list, fname_list):
    for m,fname in zip(msg_id_list, fname_list):
      if m in self.ids_to_fnames:
        del self.ids_to_fnames[m]
      elif not fname.endswith("draft"):
        # if it's not a draft, then it should have been in our database
        util.err_log("trying to remove a message id that's not in our database:\n" + m)
    remove_lines.do_sorted(pathcfg.msg_ids_file, get_idfile_lines(msg_id_list, fname_list))


