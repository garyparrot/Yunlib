text0   = { "size": "xs" }
text1   = { "size": "sm" }
text2   = { "size": "md" }
text3   = { "size": "lg" }
text4   = { "size": "xl" }
text5   = { "size": "xxl" }

space0   = { "spacing": "xs" }
space1   = { "spacing": "sm" }
space2   = { "spacing": "md" }
space3   = { "spacing": "lg" }
space4   = { "spacing": "xl" }
space5   = { "spacing": "xxl" }

bold = { "weight": "bold" }

horizontal = { "layout": "horizontal" }
vertical   = { "layout": "vertical"   }

margin0  = { "margin": "xs" }
margin1  = { "margin": "sm" }
margin2  = { "margin": "md" }
margin3  = { "margin": "lg" }
margin4  = { "margin": "xl" }
margin5  = { "margin": "xxl" }

align_start  = { "align" : "start" }
align_center = { "align" : "center" }
align_end    = { "align" : "end" }

flex0 = { "flex": 0 }
flex1 = { "flex": 1 }
flex2 = { "flex": 2 }
flex3 = { "flex": 3 }
flex4 = { "flex": 4 }
flex5 = { "flex": 5 }
flex6 = { "flex": 6 }
flex7 = { "flex": 7 }
flex8 = { "flex": 8 }
flex9 = { "flex": 9 }
flex10= { "flex": 10 }

cwhite = { "color": "#ffffff" }
cgrey0 = { "color": "#eeeeee" }
cgrey1 = { "color": "#aaaaaa" }
cgrey2 = { "color": "#555555" }
cgrey3 = { "color": "#333333" }
cblack = { "color": "#181818" }

cgreen = { "color": "#1db446" }
cred   = { "color": "#ee3333" }

wrap = { "wrap": True }

gbottom = { "gravity": "bottom" }

def compose(*args):
    sty = {}
    for item in args:
        sty = { **sty, **item }

    return sty

