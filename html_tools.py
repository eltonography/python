# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This library is a set of helper functions that return properly tagged content
# with select HTML entities.
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# anchor tag
# ----------------------------------------------------------------------------
def A(content, href="", dclass="", alt="", target="") :
  myclass = ""
  if (dclass): myclass = ' class="'+dclass+'"'
  myhref = ""
  if href: myhref = ' href="' + href + '"'
  myalt = ""
  if alt: myalt = ' alt="' + alt + '"'
  mytarget = ""
  if target: mytarget = ' target="' + target + '"'
  return '<a' + myhref + myclass + myalt + mytarget + '>' + content + '</a>'

# ----------------------------------------------------------------------------
# bold tag
# ----------------------------------------------------------------------------
def B(content) :
  return '<b>' + content + '</b>'

# ----------------------------------------------------------------------------
# body tag
# ----------------------------------------------------------------------------
def BODY(content, dclass="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  return '<body' + myclass + '>' + content + '</body>'

# ----------------------------------------------------------------------------
# break tag
# ----------------------------------------------------------------------------
def BR() :
  return '<br/>\n'

# ----------------------------------------------------------------------------
# divider tag
# ----------------------------------------------------------------------------
def DIV(content, id="", dclass="", onclick="", style="") :
  myid = ""
  if id: myid = ' id="' + id + '"'
  myclass = "";
  if dclass: myclass = ' class="' + dclass + '"'
  myclick = ""
  if onclick: myclick = ' onclick="' + onclick + '"'
  mystyle = ""
  if style: mystyle = ' style="' + style + '"'
  return '<div'+ myclass + myid + myclick + mystyle + '>' + content + '</div>'

# ----------------------------------------------------------------------------
# form tag
# ----------------------------------------------------------------------------
def FORM(content, action="", method="POST") :
  myaction = ""
  if action: myaction = ' action="' + action + '"'
  mymethod = ' method="' + method + '"'
  return '<form' + myaction + mymethod + '>' + content + '</form>'

# ----------------------------------------------------------------------------
# head tag
# ----------------------------------------------------------------------------
def HEAD(content) :
  return '<head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n' + content + '</head>'

# ----------------------------------------------------------------------------
# html tag
# ----------------------------------------------------------------------------
def HTML(content) :
  return '<!DOCTYPE html><html>'+content+'</html>'

# ----------------------------------------------------------------------------
# input tag
# ----------------------------------------------------------------------------
def INPUT(dclass="", type="", size="", name="", value="", checked="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  mytype = ""
  if type: mytype = ' type="' + type + '"'
  mysize = ""
  if size: mysize = ' size="' + size + '"'
  myname = ""
  if name: myname = ' name="' + name + '"'
  myvalue = ""
  if value: myvalue = ' value="' + value + '"'
  mychecked = ""
  if checked: mychecked = ' checked="' + checked + '"'
  return '<input' + myclass + mytype + mysize + myname + myvalue + mychecked + '/>'

# ----------------------------------------------------------------------------
# list item
# ----------------------------------------------------------------------------
def LI(content, dclass="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  return '<li' + myclass + '>' + content + '</li>'

# ----------------------------------------------------------------------------
# image tag
# ----------------------------------------------------------------------------
def IMG(dclass="", id="", src="", width="", height="", alt="", title="", border="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  myid = ""
  if id: myid = ' id="' + id + '"'
  mysrc = ""
  if src: mysrc = ' src="' + src + '"'
  mywidth = ""
  if width: mywidth = ' width="' + str(width) + '"'
  myheight = ""
  if height: myheight = ' height="' + str(height) + '"'
  myalt = ""
  if alt: myalt = ' alt="' + alt + '"'
  myborder = ""
  if border or border == 0: myborder = ' border="' + str(border) + '"'
  mytitle = ""
  if title : mytitle = ' title="' + title + '"'
  return '<img' + myclass + myid + mysrc + mywidth + myheight + myalt + myborder + mytitle + '/>'

# ----------------------------------------------------------------------------
# meta tag
# ----------------------------------------------------------------------------
def META(name="", content="") :
  return '<meta name="%s" content="%s"/>' % (name, content)

# ----------------------------------------------------------------------------
# ordered list
# ----------------------------------------------------------------------------
def OL(content, dclass="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  return '<ol' + myclass + '>' + content + '</ol>'

# ----------------------------------------------------------------------------
# selector option
# ----------------------------------------------------------------------------
def OPTION(content, value=""):
  myvalue = ""
  if value: myvalue = ' value="' + value + '"'
  return '<option' + myvalue + '>' + content + '</option>'

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def SELECT(content, dclass="", size="", onChange=""):
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  mysize = ""
  if size: mysize = ' size="' + str(size) + '"'
  mychange = ""
  if onChange: mychange = ' onChange="' + onChange + '"'
  return '<select' + mysize + myclass + mychange + '>' + content + '</select>'

# ----------------------------------------------------------------------------
# span tag
# ----------------------------------------------------------------------------
def SPAN(content, dclass="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  return '<span' + myclass + '>' + content + '</span>'

# ----------------------------------------------------------------------------
# style tag
# ----------------------------------------------------------------------------
def STYLE(content) :
  return '<style>' + content + '</style>'

# ----------------------------------------------------------------------------
# table tag
# ----------------------------------------------------------------------------
def TABLE(content, dclass="", width="", border="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  mywidth = ""
  if width: mywidth = ' width="' + width + '"'
  myborder = ""
  if border: myborder = ' border="' + border + '"'
  return '<table' + myclass + mywidth + myborder + '>' + content + '</table>'

# ----------------------------------------------------------------------------
# table data tag
# ----------------------------------------------------------------------------
def TD(content, dclass="", align="", valign="", colspan="", width="", onClick="", style="", id="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  myalign = ""
  if align: myalign = ' align="' + align + '"'
  myvalign = ""
  if valign: myvalign = ' valign="' + valign + '"'
  mycolspan = ""
  if colspan: mycolspan = ' colspan="' + str(colspan) + '"'
  mywidth = ""
  if width: mywidth = ' width="' + str(width) + '"'
  myonclick = ""
  if onClick: myonclick = ' onClick="' + onClick + '"'
  mystyle = ""
  if style: mystyle = ' style="' + style + '"'
  myid = ""
  if id: myid = ' id="' + id + '"'
  return '<td' + myclass + myalign + myvalign + mycolspan + mywidth + myonclick + mystyle + myid + '>' + content + '</td>'

# ----------------------------------------------------------------------------
# textarea tag
# ----------------------------------------------------------------------------
def TEXTAREA(content, name="", rows="1", cols="20") :
  myname = ""
  if name: myname = ' name="' + name + '"'
  myrows = ' rows="' + rows + '"'
  mycols = ' cols="' + cols + '"'
  return '<textarea' + myrows + mycols + myname + '>' + content + '</textarea>'

# ----------------------------------------------------------------------------
# title tag
# ----------------------------------------------------------------------------
def TITLE(content) :
  return '<title>' + content + '</title>'

# ----------------------------------------------------------------------------
# table row tag
# ----------------------------------------------------------------------------
def TR(content, dclass="", style="", id="") :
  myclass = ""
  if dclass: myclass = ' class="' + dclass + '"'
  mystyle = ""
  if style: mystyle = ' style="' + style + '"'
  myid = ""
  if id: myid = ' id="' + id + '"'
  return '<tr' + myclass + mystyle + myid + '>' + content + '</tr>\n'

# ----------------------------------------------------------------------------
# underline tag
# ----------------------------------------------------------------------------
def U(content) :
  return '<u>' + content + '</u>'