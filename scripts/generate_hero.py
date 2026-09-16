#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

W, H, N, MS = 1200, 360, 20, 90
OUT = 'dist/hero.gif'

def f(size, bold=False, mono=False):
    roots=[]
    if mono:
        roots.append('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
    roots.append('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    for p in roots:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

F_LABEL=f(18,True,True); F_NAME=f(112,True); F_TAG=f(27,True); F_SUB=f(20); F_TERM=f(15,False,True); F_PANEL=f(13,True,True)
runners=[Image.open('assets/runner0.png').convert('RGBA').resize((72,122),Image.Resampling.NEAREST), Image.open('assets/runner1.png').convert('RGBA').resize((74,119),Image.Resampling.NEAREST)]
rng=random.Random(42)
city=[]; x=675
while x<1200:
    bw=rng.randint(55,95); bh=rng.randint(100,245); city.append((x,H-bh,bw,bh)); x+=bw+rng.randint(8,18)
cols=[]
for x in range(690,1190,22):
    cols.append((x,rng.choice([6,8,10,12]),rng.randrange(0,430), ''.join(rng.choice('01<>/{}[]') for _ in range(19))))
platforms=[(680,290,230),(918,238,160),(1075,306,145)]
coins=[(846,206),(901,190),(955,203)]

def bg():
    im=Image.new('RGBA',(W,H),(4,9,17,255)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/(H-1); d.line((0,y,W,y), fill=(int(4+4*t),int(9+6*t),int(17+15*t),255))
    return im

def glow(im,x,y,r,c,a=60,blur=24):
    l=Image.new('RGBA',im.size,(0,0,0,0)); q=ImageDraw.Draw(l); q.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); im.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur)))

def left(im):
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,660,H),fill=(3,8,15,224))
    for x in range(0,665,30): d.line((x,0,x,H),fill=(27,120,104,30))
    for y in range(0,H,30): d.line((0,y,665,y),fill=(27,120,104,28))
    d.rounded_rectangle((38,38,44,322),3,fill=(31,222,172,235))
    d.text((67,43),'ENGINEERING × PRODUCT × AUTOMATION',font=F_LABEL,fill=(112,232,204,255))
    d.text((61,83),'NIAK_',font=F_NAME,fill=(244,250,249,255))
    d.text((67,215),'Engineer-minded builder for useful digital systems.',font=F_TAG,fill=(231,239,241,255))
    d.text((67,259),'Software  ·  AI  ·  Automation  ·  E-commerce  ·  Open Source',font=F_SUB,fill=(170,187,197,255))
    d.rounded_rectangle((66,302,618,338),8,fill=(5,19,22,230),outline=(24,152,119,180))
    d.text((84,312),'> build()  observe()  repair()  repeat()',font=F_TERM,fill=(65,255,191,255))

def world(im,k):
    d=ImageDraw.Draw(im)
    glow(im,1028,87,90,(32,225,182),55,28); glow(im,820,235,130,(64,100,255),25,40)
    d.ellipse((980,38,1078,136),fill=(12,68,76,120),outline=(58,239,202,135),width=2)
    for i,(x,y,w,h) in enumerate(city):
        d.rounded_rectangle((x,y,x+w,H),7,fill=(7+i%3*3,17+i%4*3,26+i%5*2,235),outline=(18,74,78,145))
        for wx in range(x+10,x+w-5,19):
            for wy in range(y+15,H-9,23):
                if (wx+wy+i)%3: d.rectangle((wx,wy,wx+4,wy+8),fill=((20,190,150,72) if (wx//19+i)%2 else (119,69,255,65)))
    for x,speed,phase,seq in cols:
        yy=((k*speed+phase)%480)-120
        for j,ch in enumerate(seq):
            y=yy+j*18
            if 0<y<H: d.text((x,y),ch,font=f(12,False,True),fill=(27,244,153,max(20,175-j*7)))
    for x1,y1,x2,y2,lines in [(710,66,830,147,['HUMAN','×','AI']),(1025,70,1170,157,['IDEAS','→ CODE','→ SHIP'])]:
        d.rounded_rectangle((x1,y1,x2,y2),8,fill=(3,18,22,220),outline=(35,240,181,150),width=2); yy=y1+14
        for s in lines: d.text((x1+12,yy),s,font=F_PANEL,fill=(89,255,203,245)); yy+=23
    for x,y,w in platforms:
        d.rounded_rectangle((x,y,x+w,y+27),7,fill=(8,25,30,255),outline=(22,250,178,210),width=2); d.rectangle((x+12,y+10,x+w-12,y+14),fill=(24,228,163,145))
    for j,(cx,cy) in enumerate(coins):
        yy=cy+int(math.sin((k+j*2)*.55)*5); d.ellipse((cx-13,yy-13,cx+13,yy+13),fill=(91,58,5,245),outline=(255,203,72,255),width=2); d.text((cx-7,yy-8),'<>',font=f(10,True,True),fill=(255,228,130,255))
    rx,ry=1115,210+int(math.sin(k*.45)*9); d.rounded_rectangle((rx-24,ry-18,rx+24,ry+18),10,fill=(8,27,35,255),outline=(76,230,255,230),width=2); d.ellipse((rx-13,ry-3,rx-8,ry+2),fill=(77,255,228)); d.ellipse((rx+8,ry-3,rx+13,ry+2),fill=(77,255,228)); d.line((rx,ry-18,rx,ry-27),fill=(76,230,255),width=2)

def frame(k):
    im=bg(); world(im,k); left(im); d=ImageDraw.Draw(im)
    # Motion stays on the right. The NIAK wordmark never moves.
    sy=30+(k*17)%300; d.line((665,sy,1195,sy),fill=(69,255,206,38),width=2)
    t=(k%(N-1))/(N-2)
    if t<.43: u=t/.43; x=int(690+u*175); base=290
    elif t<.72: u=(t-.43)/.29; x=int(870+u*135); base=int(290+(238-290)*u-42*math.sin(u*math.pi))
    else: u=(t-.72)/.28; x=int(1005+u*130); base=int(238+(306-238)*u-36*math.sin(u*math.pi))
    r=runners[k%2]; d.ellipse((x+11,base+1,x+r.width-8,base+9),fill=(0,0,0,105)); im.alpha_composite(r,(x,base-r.height+6))
    d.rounded_rectangle((1037,320,1174,343),7,fill=(4,19,20,225),outline=(31,177,138,150)); d.text((1048,325),'BUILD · LEARN',font=f(11,True,True),fill=(95,255,205,255))
    return im.convert('P',palette=Image.Palette.ADAPTIVE,colors=96)

os.makedirs('dist',exist_ok=True)
frames=[frame(i) for i in range(N)]
frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=MS,loop=0,optimize=True,disposal=2)
print(f'generated {OUT} ({os.path.getsize(OUT)} bytes)')
