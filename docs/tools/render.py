import sys, csv, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moderngl

import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
WORK=args.work
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
W,H=960,720
ctx=moderngl.create_standalone_context()
prog=ctx.program(vertex_shader='''#version 330
in vec3 pos; in vec3 norm; uniform mat4 vp; uniform vec3 delta;
out vec3 n;
void main(){gl_Position=vp*vec4(pos+delta,1.0); n=norm;}
''',fragment_shader='''#version 330
in vec3 n; uniform vec3 color; out vec4 outcolor;
void main(){vec3 v=normalize(n);float l=.38+.46*abs(dot(v,normalize(vec3(.4,-.5,1))))+.16*abs(dot(v,normalize(vec3(-.8,.2,.5))));outcolor=vec4(color*l,1);}
''')
fbo=ctx.simple_framebuffer((W*2,H*2))
fbo.use();ctx.enable(moderngl.DEPTH_TEST)
FONT='C:/Windows/Fonts/msyh.ttc'
font=lambda s: ImageFont.truetype(FONT,s)

def style(path, center):
    p=path.lower(); off=np.zeros(3)
    if 'lipo-battery' in p: return (.22,.30,.43), np.array([0,0,-.17])
    if 'batteryholder' in p: return (.05,.52,.73), np.array([0,0,-.10])
    if 'orin' in p or 'lubancat' in p: return (.63,.72,.73),np.array([0,0,.19])
    if 'nxholder_part1' in p: return (.05,.52,.73),np.array([0,0,.10])
    if 'nxholder_part2' in p: return (.05,.52,.73),np.array([0,0,.145])
    if 'propeller' in p: return (.23,.27,.32),np.array([0,0,.065])
    if 'emax' in p: return (.44,.47,.53),np.array([0,0,.022])
    if 'plates/' in p:
        z=.045 if 'top plate' in p else (-.028 if 'bottom' in p else (-.05 if 'armplate' in p else 0))
        return (.26,.29,.34),np.array([0,0,z])
    if '3dp4drone' in p: return (.05,.52,.73),np.array([.04,0,-.045])
    if 'fasteners/' in p: return (.64,.68,.72),np.array([0,0,.02 if center[2]>.05 else -.02])
    if 'c-rtk' in p: return (.83,.75,.55),np.array([-.05,0,.09])
    if 'speedybee' in p: return (.18,.49,.36),np.array([0,0,-.015])
    if 'camera' in p or 'gxivision' in p: return (.36,.40,.44),np.array([.07,0,0])
    if 'telemetry' in p: return (.29,.34,.39),np.array([-.06,0,.04])
    return (.45,.5,.55),off

rows=list(csv.DictReader(open(WORK/'assembly-manifest.tsv',encoding='utf-8-sig'),delimiter='\t'))
for key,title in [('holydrone_nx_v1','ORIN NX'),('holydrone_lbc4_v1','鲁班猫 4')]:
    items=[]; bounds=[]
    for r in rows:
        if not r['assembly'].startswith(key) or not r['mesh']:continue
        v=np.fromfile(WORK/'meshes'/r['mesh'],dtype='<f4').reshape(-1,3).astype('f8')
        m=np.array([float(x) for x in r['transform'].split(',')]);v=(v@m[:9].reshape(3,3))*m[12]+m[9:12]
        col,off=style(r['path'],v.mean(0))
        n=np.cross(v.reshape(-1,3,3)[:,1]-v.reshape(-1,3,3)[:,0],v.reshape(-1,3,3)[:,2]-v.reshape(-1,3,3)[:,0])
        n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
        buf=ctx.buffer(np.column_stack((v,np.repeat(n,3,axis=0))).astype('f4').tobytes())
        vao=ctx.vertex_array(prog,[(buf,'3f 3f','pos','norm')]);items.append((vao,col,off))
        bounds.extend([v.min(0),v.max(0),v.min(0)+off,v.max(0)+off])
    b=np.array(bounds);target=(b.max(0)+b.min(0))/2
    eye=np.array([.85,-1.3,.80]);forward=eye/np.linalg.norm(eye);right=np.cross([0,0,1],forward);right/=np.linalg.norm(right);up=np.cross(forward,right)
    rot=np.array([right,up,forward]); xy=(b-target)@rot.T
    scale=max(np.ptp(xy[:,0])/.98,np.ptp(xy[:,1])/.99)*1.65
    view=np.eye(4);view[:3,:3]=rot;view[:3,3]=-rot@target
    proj=np.diag([2/(scale*W/H),2/scale,-1,1]);proj[0,3]=-.12;proj[1,3]=-.02
    vp=proj@view;prog['vp'].write(vp.T.astype('f4').tobytes())
    frames=[]
    values=[0]*8+[(1-math.cos(math.pi*t/23))/2 for t in range(24)]+[1]*12+[(1+math.cos(math.pi*t/23))/2 for t in range(24)]+[0]*4
    for idx,a in enumerate(values):
        fbo.clear(.9725,.9804,.9882,1,depth=1)
        for vao,col,off in items:
            prog['delta'].value=tuple(off*a);prog['color'].value=col;vao.render(moderngl.TRIANGLES)
        im=Image.frombytes('RGB',fbo.size,fbo.read(components=3)).transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((W,H),Image.Resampling.LANCZOS)
        d=ImageDraw.Draw(im)
        d.text((40,24),'HOLYDRONE / '+title,font=font(28),fill='#162c43')
        d.text((40,65),'装配结构 · CAD 爆炸视图',font=font(16),fill='#597085')
        d.rounded_rectangle((745,30,918,68),12,fill='#e3eef5')
        d.text((762,38),'展开' if a>.5 else '装配',font=font(18),fill='#28506c')
        for j,(c,label) in enumerate([('#1085ba','打印支架'),('#49525e','机架 / 动力'),('#9facb5','上位机 / 紧固件')]):
            y=560+j*27;d.ellipse((748,y+5,758,y+15),fill=c);d.text((768,y),label,font=font(14),fill='#536b7e')
        d.line((40,661,920,661),fill='#dce5ec',width=1)
        d.text((40,675),'来自当前装配体几何 · 参照 demo 分层展开 · 类别配色 / 位移仅供展示',font=font(14),fill='#667d8e')
        d.line((42,643,42+int(660*a),643),fill='#1688b5',width=3)
        frames.append(im)
        if idx==37:im.save(OUT/(key+'-exploded.png'))
        if idx==0:im.save(OUT/(key+'-assembled.png'))
    # Shared palette prevents color flicker and keeps the GIF compact.
    palette=frames[37].quantize(colors=128,method=Image.Quantize.MEDIANCUT)
    palframes=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    palframes[0].save(OUT/(key+'-explode.gif'),save_all=True,append_images=palframes[1:],duration=80,loop=0,optimize=True,disposal=1)
    print(key,len(items),'components',len(frames),'frames',flush=True)
    for vao,_,_ in items:vao.release()
