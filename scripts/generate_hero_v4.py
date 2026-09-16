#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

W, H, N, MS = 1200, 360, 24, 85
OUT = "dist/hero.gif"
LEFT_W = 635


def font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    for p in candidates:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fit(draw, text, max_width, start, minimum, bold=False, mono=False):
    for size in range(start, minimum - 1, -1):
        f = font(size, bold, mono)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width: return f
    return font(minimum, bold, mono)

F_NAME = font(108, True)
F_LABEL = font(18, True, True)
F_TAG = font(28, True)
F_PANEL = font(13, True, True)
F_SMALL = font(13, False, True)

runners = [
    Image.open("assets/runner0.png").convert("RGBA").resize((78,132), Image.Resampling.NEAREST),
    Image.open("assets/runner1.png").convert("RGBA").resize((80,128), Image.Resampling.NEAREST),
]

rng = random.Random(42)
city=[]; x=660
while x < W:
    bw=rng.randint(42,82); bh=rng.randint(85,220)
    city.append((x,H-bh,bw,bh)); x += bw+rng.randint(8,17)
rain=[]
for x in range(670,1188,24):
    rain.append((x,rng.choice([5,7,9,11]),rng.randrange(0,440),''.join(rng.choice('01<>/{}[]AI') for _ in range(18))))

platforms=[(665,292,170),(840,244,150),(990,290,150)]
coins=[(795,218),(885,176),(980,205)]


def glow(im,x,y,r,color,alpha=55,blur=22):
    layer=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,alpha))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def base():
    im=Image.new("RGBA",(W,H),(4,9,17,255)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/(H-1); d.line((0,y,W,y),fill=(4+int(5*t),9+int(8*t),17+int(16*t),255))
    return im


def draw_left(im):
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,LEFT_W,H),fill=(2,8,15,236))
    for x in range(0,LEFT_W,32): d.line((x,0,x,H),fill=(23,115,105,25))
    for y in range(0,H,32): d.line((0,y,LEFT_W,y),fill=(23,115,105,23))
    d.rounded_rectangle((35,30,41,328),3,fill=(31,222,172,235))
    d.text((62,35),"ENGINEERING × PRODUCT × AUTOMATION",font=F_LABEL,fill=(112,232,204,255))
    d.text((58,69),"NIAK",font=F_NAME,fill=(245,250,250,255))
    d.rectangle((350,165,407,174),fill=(45,247,210,255))
    d.text((62,190),"Engineer-minded builder",font=F_TAG,fill=(236,243,244,255))
    d.text((62,226),"for useful digital systems.",font=F_TAG,fill=(236,243,244,255))
    sub="Software · AI · Automation · E-commerce · Open Source"
    d.text((62,272),sub,font=fit(d,sub,520,17,14),fill=(171,191,200,255))
    d.rounded_rectangle((61,307,570,340),8,fill=(4,18,22,235),outline=(24,152,119,190),width=2)
    pill="> build()   observe()   repair()   repeat()"
    d.text((78,316),pill,font=fit(d,pill,475,14,11,mono=True),fill=(65,255,191,255))
    d.line((LEFT_W,0,LEFT_W,H),fill=(44,224,190,100),width=2)


def player_state(k):
    t=k/(N-1)
    if t < .34:
        u=t/.34; x=666+u*150; foot=292
    elif t < .67:
        u=(t-.34)/.33; x=816+u*176; foot=292-50*math.sin(math.pi*u)-48*u
    else:
        u=(t-.67)/.33; x=992+u*120; foot=244+46*u-34*math.sin(math.pi*u)
    return int(x),int(foot)


def draw_coin(im,cx,cy,phase):
    d=ImageDraw.Draw(im); yy=cy+int(math.sin(phase)*3)
    glow(im,cx,yy,20,(255,190,45),48,8)
    d.ellipse((cx-13,yy-13,cx+13,yy+13),fill=(94,58,4,255),outline=(255,211,91,255),width=2)
    d.text((cx-7,yy-7),"<>",font=font(9,True,True),fill=(255,233,150,255))


def sparkle(im,x,y,strength):
    if strength <= 0: return
    d=ImageDraw.Draw(im)
    for a in range(0,360,45):
        r=9+11*strength; dx=math.cos(math.radians(a))*r; dy=math.sin(math.radians(a))*r
        d.line((x,y,x+dx,y+dy),fill=(255,225,115,int(255*strength)),width=2)


def draw_world(im,k,px,pfoot):
    d=ImageDraw.Draw(im)
    glow(im,1035,88,98,(35,235,185),52,26); glow(im,810,235,150,(80,75,255),25,42)
    d.ellipse((965,24,1095,154),fill=(10,65,72,110),outline=(58,239,202,145),width=2)
    d.ellipse((986,45,1074,133),outline=(58,239,202,70),width=1)
    for i,(bx,by,bw,bh) in enumerate(city):
        d.rounded_rectangle((bx,by,bx+bw,H),5,fill=(8+i%3*2,16+i%4*3,27+i%5*2,235),outline=(17,71,79,125))
        for wx in range(bx+7,bx+bw-5,15):
            for wy in range(by+11,H-10,19):
                if (wx+wy+i)%3:
                    c=(20,190,150,78) if (wx//15+i)%2 else (122,68,255,66)
                    d.rectangle((wx,wy,wx+3,wy+6),fill=c)
    for x,speed,phase,seq in rain:
        yy=((k*speed+phase)%455)-120
        for j,ch in enumerate(seq):
            y=yy+j*18
            if 0<y<H: d.text((x,y),ch,font=F_SMALL,fill=(28,244,154,max(18,165-j*7)))
    d.rounded_rectangle((675,58,785,137),8,fill=(3,18,22,220),outline=(35,240,181,150),width=2)
    d.text((694,77),"HUMAN",font=F_PANEL,fill=(89,255,203,245)); d.text((716,100),"×",font=F_PANEL,fill=(89,255,203,245)); d.text((711,117),"AI",font=font(20,True,True),fill=(89,255,203,245))
    d.rounded_rectangle((1024,57,1170,140),8,fill=(3,18,22,220),outline=(35,240,181,150),width=2)
    for i,line in enumerate(("IDEAS","→ CODE","→ SHIP")): d.text((1042,73+i*22),line,font=F_PANEL,fill=(89,255,203,245))
    for x,y,w in platforms:
        d.rounded_rectangle((x,y,x+w,y+25),6,fill=(8,26,31,255),outline=(22,250,178,210),width=2)
        d.rectangle((x+10,y+9,x+w-10,y+13),fill=(24,228,163,145)); d.line((x+w//2,y+25,x+w//2,min(H,y+56)),fill=(28,56,66,255),width=4)
    for j,(cx,cy) in enumerate(coins):
        collected=px+38>=cx
        if not collected: draw_coin(im,cx,cy,k*.55+j)
        delta=abs((px+38)-cx)
        if delta<28: sparkle(im,cx,cy,1-delta/28)
    rx,ry=1128,214+int(math.sin(k*.45)*6)
    d.rounded_rectangle((rx-25,ry-19,rx+25,ry+19),10,fill=(8,27,35,255),outline=(76,230,255,230),width=2)
    d.ellipse((rx-13,ry-3,rx-8,ry+2),fill=(77,255,228)); d.ellipse((rx+8,ry-3,rx+13,ry+2),fill=(77,255,228)); d.line((rx,ry-19,rx,ry-28),fill=(76,230,255),width=2); d.ellipse((rx-3,ry-32,rx+3,ry-26),fill=(76,230,255))
    d.rounded_rectangle((1080,158,1180,198),8,fill=(5,20,27,225),outline=(59,218,246,170),width=2); d.text((1095,167),"LET'S BUILD",font=F_PANEL,fill=(95,245,250,255))


def frame(k):
    im=base(); px,pfoot=player_state(k); draw_world(im,k,px,pfoot); draw_left(im)
    d=ImageDraw.Draw(im); scan_y=22+(k*13)%315
    d.line((LEFT_W+8,scan_y,W-8,scan_y),fill=(69,255,206,35),width=2)
    runner=runners[k%2]; top=pfoot-runner.height+6
    d.ellipse((px+12,pfoot+1,px+runner.width-10,pfoot+9),fill=(0,0,0,110)); im.alpha_composite(runner,(px,top))
    return im.convert("P",palette=Image.Palette.ADAPTIVE,colors=112)

os.makedirs("dist",exist_ok=True)
frames=[frame(i) for i in range(N)]
frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=MS,loop=0,optimize=True,disposal=2)
print(f"generated {OUT} ({os.path.getsize(OUT)} bytes)")
