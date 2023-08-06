####
# bomail.guistuff.gui_util
#
# various UI actions, like Send, that get called from several places.
####

import os
import subprocess
import curses

from bomail.config.config import pathcfg,guicfg,sendcfg

import bomail.cli.compose as compose
import bomail.cli.send as send
import bomail.cli.mailfile as mailfile

import bomail.guistuff.display as display
import bomail.guistuff.display_fmt as display_fmt
import bomail.guistuff.get_txt as get_txt

import bomail.util.addr as addr
import bomail.util.attach as attach
import bomail.util.datestuff as datestuff
import bomail.util.util as util


# return mode, note
def go_send(gui, filelist):
  if len(sendcfg.smtp_servernames) == 0:
    return "note", "Must configure ~/.bomailrc to send email"
  for filename in filelist:
    attach_list = gui.mail_mgr.get_attachlist(filename)
    if len(attach_list) > 0:
      for f in attach_list:
        if not (os.path.exists(f) and os.path.isfile(f)):
          return "all", "Error (did not send): could not find an attachment: " + str(f)
  lines = ["y  yes, send the email",
           "n  no, cancel"]
  if len(filelist) > 1:
    lines[0] = "y  yes, send " + str(len(filelist)) + " emails"
  display.draw_bottom_text(gui, lines)
  display.redraw_note(gui, "")
  key = gui.screen.getkey()
  if key == "y":
    display.redraw_note(gui, "Sending...")
    results, err_str = send.main(filelist, gui.mail_mgr)
    # trash all that were sent
    done = [fname for res,fname in zip(results,filelist) if res]
    if len(done) > 0:
      gui.acts.exec_act(("trash", done, [gui.mail_mgr.get_all(filename) for filename in done]))
    if len(done) == len(filelist):
      return "all", "Sent mail!"
    else:
      util.err_log("Sending mail: could not send: " + ", ".join([fname for res,fname in zip(results,filelist) if not res]) + "\n")
      util.err_log(err_str)
      return "all", "Some errors, sent " + str(len(done)) + " of " + str(len(filelist)) + " : " + err_str
  else:
    return "all", "Cancelled, did not send"


# return mode, note
def go_compose_draft(gui, key, filename, quote=True):
  if key == "n" or filename is None:
    recip_pairs = get_txt.get_recips(gui.tab_area, gui.addr_book)

    gui.tab_area.clear()
    gui.tab_area.refresh()
    subj = get_txt.get_subj_line(gui, "")
    if subj is None:
      return "all", "Cancelled"
    new_filename = compose.new_compose(subj, addr.pairlist_to_str(recip_pairs), "", "", "", "", gui.mail_mgr)
  elif key == "a":
    new_filename = compose.reply_all(filename, gui.mail_mgr, quote)
  elif key == "o":
    new_filename = compose.reply_one(filename, gui.mail_mgr, quote)
  elif key == "r":
    new_filename = compose.reply_all(filename, gui.mail_mgr, quote, include_sender=False)
  elif key == "f":
    recip_pairs = get_txt.get_recips(gui.tab_area, gui.addr_book)
    new_filename = compose.forward(filename, addr.pairlist_to_str(recip_pairs), gui.mail_mgr, quote)
  elif key == "e":
    new_filename = filename
  else:
    return "all", "Cancelled"
  subprocess.call(guicfg.edit_prog + " \"" + new_filename + "\"", shell=True)
  gui.reset_after_prog()
  gui.mail_mgr.updated_flist([new_filename])
  gui.update_for_change([new_filename])
  return "all", "Edited " + display_fmt.get_shortened(new_filename, gui.mail_mgr)


# if the WRITE key was pressed, get the kind of draft to create
# given current filename
# return mode, note, new_filename
def go_write_key(gui, filename):
  if filename[-5:] == "draft":
    return go_write_key_draft(gui, filename)
  else:
    return go_write_key_email(gui, filename)


def go_write_key_email(gui, filename):
  lines = [
    "a  reply-all        f  forward",
    "o  reply-one        n  new draft",
    "r  reply-recipient  z  CANCEL"]
  display.draw_bottom_text(gui, lines)
  display.redraw_note(gui, "")
  key = gui.screen.getkey()
  if key in ["a", "o", "r", "f", "n"]:
    return go_compose_draft(gui, key, filename)
  else:
    return "all", "Cancelled"


def go_write_key_draft(gui, filename):
  lines = [
    "n  new draft          t/y  add/remove recip  a/x  add/remove attachment",
    "e  edit this draft    c/v  add/remove CC       z  CANCEL",
    "s  edit subject line  b/m  add/remove BCC"]
  display.draw_bottom_text(gui, lines)
  display.redraw_note(gui, "")
  key = gui.screen.getkey()
  mode, text = "all", "Cancelled"
  if key in ["n", "e"]:
    mode, text = go_compose_draft(gui, key, filename)
  
  elif key == "s":
    s = get_txt.get_subj_line(gui, gui.mail_mgr.get(filename, mailfile.SUBJ_L))
    if s is None:
      return "all", "Cancelled"
    gui.mail_mgr.set(filename, mailfile.SUBJ_L, s)
    mode, text = "all", "Edited subject line of " + display_fmt.get_shortened(filename, gui.mail_mgr)

  elif key == "a":
    s = get_txt.get_path(gui.tab_area, gui.mail_mgr)
    if s is None:
      return "all", "Cancelled"
    old_attachlist = gui.mail_mgr.get_attachlist(filename)
    mode, text = gui.acts.do(("add attach", [filename], old_attachlist, [f.strip() for f in s]))

  elif key == "x":
    old_attachlist = gui.mail_mgr.get_attachlist(filename)
    if len(old_attachlist) == 0:
      return "all", "No attachments to remove"
    s = get_txt.get_sublist_from_list(gui.tab_area, old_attachlist, [], allow_new=False)
    if s is None:
      return "all", "Cancelled"
    mode, text = gui.acts.do(("remove attach", [filename], old_attachlist, s))

  else:  # recipient stuff
    if key in ["t", "y"]:
      mail_line = mailfile.TO_L
    elif key in ["c", "v"]:
      mail_line = mailfile.CC_L
    elif key in ["b", "m"]:
      mail_line = mailfile.BCC_L
    else:
      return "all", "Cancelled"
  
    # get the recipients and, if nonempty, do it
    old_recip_line = gui.mail_mgr.get(filename, mail_line)
    old_recip_pairs = addr.str_to_pairlist(old_recip_line)
    if key in ["t", "c", "b"]:
      # get new recips, add to mail_line
      new_recip_pairs = get_txt.get_recips(gui.tab_area, gui.addr_book, already_recip_pairs=old_recip_pairs)
      if len(new_recip_pairs) == 0:
        return "all", "Cancelled"
      new_recip_line = addr.pairlist_to_str(old_recip_pairs + new_recip_pairs)
    else:
      # get from old recips, remove from mail_line
      remove_recip_pairs = get_txt.get_recips(gui.tab_area, gui.addr_book, recip_pairs=old_recip_pairs, allow_new=False)
      if len(remove_recip_pairs) == 0:
        return "all", "Cancelled"
      new_recip_line = addr.pairlist_to_str([r for r in old_recip_pairs if r not in remove_recip_pairs])
    mode, text = gui.acts.do(("edit file", filename, mail_line, new_recip_line, old_recip_line))
  gui.mail_mgr.updated_flist([filename])
  gui.update_for_change([filename])
  return mode, text


# return mode, note
def go_schedule(gui, filelist):
  sched_txt = get_txt.get_sched_txt(gui)
  if sched_txt is None:
    return "view", "Cancelled"
  schedobj = datestuff.parse_schedstr_to_utcobj(sched_txt)
  if schedobj is None:
    return "view", "Cancelled: could not parse input"
  return gui.acts.do(("scheduled", filelist, [gui.mail_mgr.get(f, mailfile.STATE_L) for f in filelist], schedobj))


def go_add_tags(gui, filelist):
  prevtags = [gui.mail_mgr.get_tags(f) for f in filelist]
  oldtaglist = sorted(list(set.intersection(*[gui.mail_mgr.get_tagset(f) for f in filelist])))
  newtags = get_txt.get_tags(gui.tab_area, [t for t in gui.tag_mgr.tags if t not in oldtaglist])
  if newtags is None or len(newtags) == 0:
    return "view", "Cancelled"
  else:
    alltags = set(gui.tag_mgr.tags)
    unknown = [t for t in newtags if t not in alltags]
    return gui.acts.do(("add tags", filelist, newtags, prevtags, unknown))


def go_remove_tags(gui, filelist):
  prevtags = [gui.mail_mgr.get_tags(f) for f in filelist]
  oldtaglist = sorted(list(set.union(*[gui.mail_mgr.get_tagset(f) for f in filelist])))
  removeme = get_txt.get_tags(gui.tab_area, oldtaglist, allow_new=False)
  if removeme is None or len(removeme) == 0:
    return "view", "Cancelled"
  else:
    return gui.acts.do(("remove tags", filelist, removeme, prevtags))


