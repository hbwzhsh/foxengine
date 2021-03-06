# -*- coding: utf-8 -*-

#算法测试

from numpy import select

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1 import lesser,bnot,gmax,gmin,greater,greater_equals,lesser_equals
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum,scover,xfollow,decover1
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1idiom import *
from wolfox.fengine.core.d1indicator import cmacd,score2,adx
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.sfuncs')    

def bma30(stock):
    ''' 
        稳定收盘于30日线上3天后买入
    '''
    linelog('%s:%s' % (bma30.__name__,stock.code))    
    t = stock.transaction
    
    cu3 = msum2(t[CLOSE]>stock.ma3,3) == 3

    fcu3 = gand(cu3,bnot(rollx(cu3)))   #第一次cu3

    signal = gand(fcu3,stock.ref.t3)

    return signal


def xgg(stock):
    '''
        mg20 = ma(stock.g20,13)
        mg60 = ma(stock.g60,13)
        signal = gand(across,stock.ref.t1,stock.ref.t3,stock.ref.t5,xatr<mxatr,xatr>45,xatr<60)#,t[CLOSE]>stock.ma3,t[CLOSE]>stock.ma1)
        评估:总盈亏值=43079,交易次数=515        期望值=1202
                总盈亏率(1/1000)=43079,平均盈亏率(1/1000)=83,盈利交易率(1/1000)=563
                平均持仓时间=28,持仓效率(1/1000000)=2964
                赢利次数=290,赢利总值=58593
                亏损次数=222,亏损总值=15514
                平盘次数=3
        mg20 = ma(stock.g20,7)
        mg60 = ma(stock.g60,13)
        评估:总盈亏值=68168,交易次数=758        期望值=1186
                总盈亏率(1/1000)=68168,平均盈亏率(1/1000)=89,盈利交易率(1/1000)=600
                平均持仓时间=29,持仓效率(1/1000000)=3068
                赢利次数=455,赢利总值=91007
                亏损次数=302,亏损总值=22839
                平盘次数=1
                
    
    '''
    linelog('%s:%s' % (xgg.__name__,stock.code))

    t = stock.transaction

    mg20 = ma(stock.g20,7)
    mg60 = ma(stock.g60,13)

    across = gand(cross(mg60,mg20)>0,strend(mg20)>0)

    #nc = bnot(gand(stock.t3<1,stock.t4<1,stock.t5<1))

    ll = tmin(t[LOW],13)  
    llc = t[CLOSE] < ll* 125/100

    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    bma = gand(stock.ma1>stock.ma4,stock.ma2>stock.ma4,stock.ma3>stock.ma4)

    signal = gand(across,stock.ref.t1,stock.ref.t3,stock.ref.t5,xatr<mxatr,xatr>45,xatr<60,bma)

    return signal


def bxatr(stock):
    ''' #比bxatr2稳定
        数量很多
        但很难提升到50%以上
    '''
    t = stock.transaction
    
    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    x40 = cached_ints(len(xatr),40)
    xcross = gand(cross(x40,xatr)>0,strend(xatr)>0)

    catr = gand(xatr<mxatr,xcross)

    linelog('%s:%s' % (bxatr.__name__,stock.code))

    signals = gand(catr,stock.t5,stock.g60<3000,stock.g20>stock.g60)

    return signals


def bxatr1(stock):
    ''' 
    '''
    t = stock.transaction
    
    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    x40 = cached_ints(len(xatr),40)
    xcross = gand(cross(x40,xatr)<0,strend(xatr)<0)

    catr = gand(xatr<mxatr,xcross)

    linelog('%s:%s' % (bxatr.__name__,stock.code))

    signals = gand(catr,stock.ref.t3)

    return signals


def bxatr2(stock):
    '''
        xatr = stock.atr * BASE / t[CLOSE]
        mxatr = ma(xatr,13)
        across = gand(cross(mxatr,xatr)<0,strend(xatr)<0)
        catr = gand(xatr>40,xatr<60,across)
        signals = gand(catr,stock.g60<3000,stock.diff<stock.dea)
        评估:总盈亏值=106650,交易次数=2309      期望值=541
                总盈亏率(1/1000)=106650,平均盈亏率(1/1000)=46,盈利交易率(1/1000)=528
                平均持仓时间=22,持仓效率(1/1000000)=2090
                赢利次数=1220,赢利总值=199166
                亏损次数=1076,亏损总值=92516
                平盘次数=13
                闭合交易明细:
    
    '''
    t = stock.transaction
    
    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    across = gand(cross(mxatr,xatr)<0,strend(xatr)<0)
    #across = gand(cross(mxatr,xatr)>0,strend(xatr)>0)

    #catr = gand(xatr>40,xatr<60,across)
    #catr = gand(across,xatr>40,xatr<66)
    catr = gand(across,xatr<66)

    linelog('%s:%s' % (bxatr2.__name__,stock.code))

    nc = bnot(gand(stock.t3<1,stock.t4<1,stock.t5<1))


    lmax = tmax(t[HIGH],30)
    lmin = tmin(t[HIGH],5)  
    ll = tmin(t[LOW],5)  


    lmx = t[CLOSE]<lmax*85/100
    lmi = t[CLOSE]>lmin*103/100 #突破最低的最高价
    #llx = t[CLOSE]<ll*115/100   #不超过15%
    
    madx = adx(t[CLOSE],t[HIGH],t[LOW]) #判断是否出于趋势末端

    #signals = gand(catr,stock.g60<3000,nc,stock.diff<stock.dea,cnc,stock.ref.t3,xabove,xatr>50,lmx,lmi)
    signals = gand(catr,stock.g60>5000,nc,stock.ref.t3,lmx,lmi,strend(madx)<0)

    return signals


def bxatr2b(stock):
    '''
    '''
    t = stock.transaction
    
    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    across = gand(cross(mxatr,xatr)<0,strend(xatr)<0)

    madx = adx(t[CLOSE],t[HIGH],t[LOW]) #判断是否出于趋势末端
    
    s_ahead = gand(across,xatr<66,strend(madx)<0)

    linelog('%s:%s' % (bxatr2b.__name__,stock.code))

    nc = bnot(gand(stock.t3<1,stock.t4<1,stock.t5<1))

    lmax = tmax(t[HIGH],30)
    lmin = tmin(t[HIGH],5)  

    lmx = t[CLOSE]<lmax*85/100
    lmi = t[CLOSE]>lmin*103/100 #突破最低的最高价
    
    s_follow = gand(stock.g60>5000,nc,stock.ref.t3,lmx,lmi,xatr<mxatr)

    #signals = gand(catr,stock.g60<3000,nc,stock.diff<stock.dea,cnc,stock.ref.t3,xabove,xatr>50,lmx,lmi)
    signals = sfollow(s_ahead,s_follow,7)#gand(catr,)#,llx)#,strend(dravi)>0)#ravi<0)#,strend(ravi)>0)

    return signals

def bxatr3(stock):
    '''
    '''
    t = stock.transaction
    
    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    across = gand(cross(mxatr,xatr)>0,strend(xatr)>0)

    catr = gand(across)

    linelog('%s:%s' % (bxatr2.__name__,stock.code))

    nc = bnot(gand(stock.t3<1,stock.t4<1,stock.t5<1))

    lmax = tmax(t[HIGH],30)
    lmin = tmin(t[HIGH],5)  


    lmx = t[CLOSE]<lmax*85/100
    lmi = t[CLOSE]>lmin*103/100 #突破最低的最高价
    #llx = t[CLOSE]<ll*115/100   #不超过15%
    
    madx = adx(t[CLOSE],t[HIGH],t[LOW]) #判断是否出于趋势末端

    ravi = (stock.ma1 - stock.ma4)*100/stock.ma4

    #signals = gand(catr,stock.g60<3000,nc,stock.diff<stock.dea,cnc,stock.ref.t3,xabove,xatr>50,lmx,lmi)
    signals = gand(catr,ravi>1)#stock.g60>5000,nc,lmx,lmi)#,llx)#,strend(dravi)>0)#ravi<0)#,strend(ravi)>0)

    return signals

def xatr_seller(stock,buy_signal):
    '''
        seller = sellers_wrapper(t.xatr_seller,seller2000)
    '''
    t = stock.transaction
    
    xatr = stock.atr * BASE / t[CLOSE]

    mxatr = ma(xatr,13)

    across = gand(cross(mxatr,xatr)>0,strend(xatr)>0)

    return across

def ma30_seller(stock,buy_signal):
    ''' 
        稳定收盘于30日线下3天后出掉
        seller = sellers_wrapper(t.ma30_seller,seller2000)
    '''
    t = stock.transaction
    
    cd3 = msum2(t[CLOSE]<stock.ma3,3) == 3

    fcd3 = gand(cd3,bnot(rollx(cd3)))   #第一次cd3

    return fcd3

def ma37_seller(stock,buy_signal):
    '''
        seller = sellers_wrapper(t.ma37_seller,seller2000)
    '''
    t = stock.transaction
    
    across = gand(cross(stock.ma1,stock.ma0)<0,strend(stock.ma0)<0)

    return across


def tsvama2_old(stock,fast,slow):
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above)

def tsvama2(stock,fast=3,slow=33,bxatr=50):
    ''' svama两线交叉
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8
 
    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    
    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)
    xatr = stock.atr * BASE / t[CLOSE]

    return gand(msvap,stock.above,stock.t5,vfilter,stock.magic,xatr>bxatr)

def tsvama2a(stock,fast=20,slow=100):
    ''' svama两线交叉
        加vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    #vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8
    xatr = stock.atr * BASE / t[CLOSE]

    linelog('%s:%s' % (tsvama2a.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter,xatr<=30)

def tsvama2b(stock,fast=20,slow=170,astart=40):
    ''' svama两线交叉
        另加smacd,vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    sdiff,sdea = cmacd(svap)
    ss = gand(cross_fast_slow,strend(sdiff-sdea)>0)
    #ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    #vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s < vma_l * 7/8)  #t[CLOSE]>stock.ma1无好处
    
    xatr = stock.atr * BASE / t[CLOSE]     
 
    linelog('%s:%s' % (tsvama2b.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter,xatr>=astart)

def pmacd(stock):
    t = stock.transaction
    pdiff,pdea = cmacd(t[CLOSE])
    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,strend(pdea>0)) > 0
    linelog(stock.code)
    #return gand(dcross,stock.golden,stock.above,cs,pdea>0,pdea<12000)
    return gand(dcross,stock.thumb,stock.above,stock.silver,pdea>0,pdea<12000)

def nhigh(stock):#60高点
    t = stock.transaction
    mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    dcross = cross(mline,t[HIGH])>0    
    g = gand(stock.g5>=stock.g20,stock.thumb)
    #linelog(stock.code)
    return gand(g,stock.silver,dcross,strend(stock.ma4)>0,stock.above)

def xma60(stock,astart=45):
    ''' 碰到ma4后回升
        cs,g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)    ##最佳
        评估:总盈亏值=13321,交易次数=45 期望值=6040
                总盈亏率(1/1000)=13321,平均盈亏率(1/1000)=296,盈利交易率(1/1000)=622
                赢利次数=28,赢利总值=14170
                亏损次数=17,亏损总值=849
                平盘次数=0
        
        #金手指
        评估:总盈亏值=33283,交易次数=173        期望值=2493
                总盈亏率(1/1000)=33283,平均盈亏率(1/1000)=192,盈利交易率(1/1000)=526
                赢利次数=91,赢利总值=39607
                亏损次数=82,亏损总值=6324
                平盘次数=0

        #金手指+cs<6600
        评估:总盈亏值=5530,交易次数=17  期望值=8333
                总盈亏率(1/1000)=5530,平均盈亏率(1/1000)=325,盈利交易率(1/1000)=705
                赢利次数=12,赢利总值=5727
                亏损次数=5,亏损总值=197
                平盘次数=0
        
        #银手指
        评估:总盈亏值=23766,交易次数=87 期望值=4706
                总盈亏率(1/1000)=23766,平均盈亏率(1/1000)=273,盈利交易率(1/1000)=574
                赢利次数=50,赢利总值=25929
                亏损次数=37,亏损总值=2163
                平盘次数=0

        sync,stock.above,stock.t5,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g5>=3000,s.g5<=8000,stock.silver
        评估:总盈亏值=11019,交易次数=36 期望值=4781
                总盈亏率(1/1000)=11019,平均盈亏率(1/1000)=306,盈利交易率(1/1000)=777
                赢利次数=28,赢利总值=11535
                亏损次数=8,亏损总值=516
                平盘次数=0
                
    '''
    t = stock.transaction
    water_line = stock.ma4*115/100   #上方15处
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    linelog(stock.code)
    #return gand(sync,stock.above,stock.t5,stock.golden,cs)    
    xatr = stock.atr * BASE / t[CLOSE]     
    
    return gand(sync,stock.above,stock.t5,stock.thumb,stock.silver,xatr>=astart)

def wvad(stock):
    t = stock.transaction
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)
    #ecross = gand(stock.golden,cs,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t5,stock.above)
    ecross = gand(stock.thumb,stock.silver,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t5,stock.above)
    linelog(stock.code)
    return ecross

def temv(stock):
    '''
    name:Mediator:<temv:atr_seller:up_sector=2,trace_times=3000,stop_times=1200,covered=10:make_trade_signal_advanced:B1S1>
    pre_ev:	评估:总盈亏值=2244,交易次数=14	期望值=4210	
		总盈亏率(1/1000)=2244,平均盈亏率(1/1000)=160,盈利交易率(1/1000)=428
		赢利次数=6,赢利总值=2555
		亏损次数=8,亏损总值=311
		平盘次数=0
		闭合交易明细:
    
    '''
    t = stock.transaction
    ts = cached_zeros(len(t[CLOSE]))
    ekey = 'emv'
    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv = msum2(em,14)
    semv = ma(mv,9)
    ecross = gand(stock.thumb,stock.silver,cross(ts,mv)>0,strend(semv)>0,stock.t5,stock.above)
    linelog(stock.code)
    return ecross
    
def vmacd_ma4(stock):
    t = stock.transaction
    
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff)>0,strend(vdiff)>0,strend(vdea)>0)

    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)

    c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=8500)
    cs = catalog_signal_cs(stock.c60,c_ex)    
    return gand(g,cs,dcross,stock.above,strend(stock.ma4)>0,vdea>=0,vdea<=12000)

def ma4(stock): #3X10
    t = stock.transaction
    fma = ma(t[CLOSE],3)
    dcross = gand(cross(stock.ma2,fma),strend(fma)>0,strend(stock.ma2)>0,strend(stock.ma3)>0,strend(stock.ma4)>0,stock.t5>0)
    linelog(stock.code)
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #return gand(stock.golden,cs,dcross,stock.above,stock.t5)
    return gand(g,stock.silver,dcross,stock.above)    

def vmacd(stock):
    t = stock.transaction
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))
    linelog(stock.code)
    return gand(dcross,stock.golden,stock.t5,stock.silver,vdea>0,vdea<12000)

def gx60(stock,fast=5,slow=20):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    ma_fast = ma(g60,fast)
    ma_slow = ma(g60,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    #c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

    linelog(stock.code)

    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    return gand(cross_fast_slow,g,stock.silver,stock.above,stock.t5,trend_ma_120,trend_ma_250)

def gx250(stock,fast=10,slow=67):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    gx = stock.g250
    ma_fast = ma(gx,fast)
    ma_slow = ma(gx,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    #c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

    linelog(stock.code)

    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    return gand(cross_fast_slow,stock.golden,stock.silver,stock.above,stock.t5,trend_ma_120,trend_ma_250)


def gcs(stock):
    '''
        20000101-20090101
        评估:总盈亏值=29163,交易次数=206        期望值=1880
                总盈亏率(1/1000)=29163,平均盈亏率(1/1000)=141,盈利交易率(1/1000)=422
                赢利次数=87,赢利总值=38080
                亏损次数=118,亏损总值=8917
                平盘次数=1
    '''
    t = stock.transaction
    #ma5 = ma(t[CLOSE],5)
    linelog(stock.code)
    sbuy = gand(stock.golden,stock.silver,stock.above,stock.ma1>stock.ma2,stock.ref.t5)
    return sbuy

def xgcs(stock):
    t = stock.transaction
    #ma5 = ma(t[CLOSE],5)
    linelog(stock.code)
    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)
    sbuy = gand(stock.golden,stock.silver,stock.above,stock.ma1>stock.ma2,stock.ref.t5,mxi)
    return sbuy

def xgcs0(stock,astart=50,aend=1000):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    #ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0

    xatr = stock.atr * BASE / t[CLOSE]     

    sbuy = gand(stock.golden,stock.silver,stock.above,stock.ma1>stock.ma2,stock.ref.t5,mxi,t[CLOSE]<stock.ma1,xatr>=astart,xatr<=aend)
    return sbuy


def mgcs(stock):
    t = stock.transaction
    linelog(stock.code)
    s = stock
    g = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g20>=3000,s.g20<=8000,s.g20<=s.g120+1000)     ######
    pdiff,pdea = cmacd(t[CLOSE])
    sbuy = gand(g,pdiff>=225,pdiff<=350,stock.above,stock.ref.t5,strend(stock.ma3)>0,strend(stock.ma4)>0,stock.t5,stock.ref.above)
    return sbuy

def spring(stock,threshold=-30):
    ''' 对于结果
        下影越短越好，close-low/close 也是越短越好
    '''
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t5)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    ref = stock.ref
    sbuy = signals #gand(signals,greater(ref.ma2,ref.ma3),greater(ref.ma3,ref.ma4))

    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,19,39)
    ssignal = gand(strend(sdiff)>0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))


    return gand(sbuy,msvap)


def cma2(stock,fast,slow,gfrom=0,gto=8500):  
    ''' 传统的ma2
        5 X 20
        评估:总盈亏值=11488,交易次数=54 期望值=3164
                总盈亏率(1/1000)=11488,平均盈亏率(1/1000)=212,盈利交易率(1/1000)=685
                赢利次数=37,赢利总值=12628
                亏损次数=17,亏损总值=1140
                平盘次数=0
            g5: 4000-8000
            评估:总盈亏值=10980,交易次数=38 期望值=4571
                总盈亏率(1/1000)=10980,平均盈亏率(1/1000)=288,盈利交易率(1/1000)=763
                赢利次数=29,赢利总值=11547
                亏损次数=9,亏损总值=567
                平盘次数=0
        5 X 13
        评估:总盈亏值=39727,交易次数=213        期望值=2952
                总盈亏率(1/1000)=39727,平均盈亏率(1/1000)=186,盈利交易率(1/1000)=553
                赢利次数=118,赢利总值=45746
                亏损次数=95,亏损总值=6019
                平盘次数=0
            #g5:7000-8500
            评估:总盈亏值=33922,交易次数=149        期望值=3603
                总盈亏率(1/1000)=33922,平均盈亏率(1/1000)=227,盈利交易率(1/1000)=617
                赢利次数=92,赢利总值=37550
                亏损次数=57,亏损总值=3628
                平盘次数=0
 
    '''
    t = stock.transaction
    water_line = ma(t[CLOSE],slow)
    dcross = cross(water_line,ma(t[CLOSE],fast))

    up_cross = dcross > 0

    linelog(stock.code)
    return gand(up_cross,stock.above,stock.t5,stock.g5>=stock.g20+500,stock.g20>=stock.g60+500,stock.g60>=stock.g120,stock.g5>=gfrom,stock.g5<=gto)


def cma1(stock,length=30,covered=7):  #
    t = stock.transaction
    
    water_line = ma(t[CLOSE],length)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,covered=7)
    return gand(sync,stock.above,stock.t5,stock.thumb,stock.silver)


def x30(t):
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return sync

def tsvama2x(stock,fast=20,slow=100):
    ''' svama两线交叉
    '''
    t = stock.transaction
    g = stock.golden
    svap,v2i = stock.svap_ma_67
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    signal = msvap
    s2 = x30(t)
    sbuy = sfollow(signal,s2,10)
    linelog('%s:%s' % (tsvama2x.__name__,stock.code))
    return gand(sbuy,stock.above,stock.thumb,stock.silver)


def gmacd_old(stock): #
    ''' 
        20010701-20090101效果不好，但能持平
        20080701开始效果非常好
        ll5 = rollx(t[LOW],5),   hinc = t[HIGH] * 1000 / ll5
        ll10 = rollx(t[LOW],10),    hh10 = tmax(t[HIGH],10), rhl10 = hh10 * 1000/ll10
        lfilter = hinc<1200 and rhl10<1500
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30),t[LOW]),5),之后+lfilter,2115/704/846
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),5),之后+lfilter,2213/759/595
            g60:4500-8500:  2946/821/286
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),之后+lfilter,2392/746/844    
            g60:0-3000:1457/670/273
            g60:3000-6000: 2709/788/402
            g60:6000-!: 2696/758/273
            g60:6000-8500: 2781/775/232
            g60:>8500:  2193/632/49
            g60:4500-8500:  3078/793/411
            g60:4500-7500:  2888/797/345
            g60:5000-8000:  2925/796/324
            数量太多,需要进一步筛选
        ss1=sfollow(cross(mdea,mdiff) > 0,gand(vdiff>vdea,pdiff>pdea)), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),2392/746/844    
            mdiff>=mdea
            g60:4500-8500:3036/800/451
            g20:4500-8500:3886/817/465  #不需要hinc<1200，只需要rhl10<1500,而且效果也有限
            但这个滤掉了600121,600756,000961,600997等
            g20:5000-9000:3877/845/297   
            ####g20:5000-9500:3937/840/300    #去掉mdiff>=mdea,3571/841/416
                添加 strend(stock.ref.ma4)>0   4063/847/295
                above改为13>30>60>120
                #above = gand(stock.ma2 > stock.ma3,stock.ma3>stock.ma4,stock.ma4>stock.ma5)
                signal = gand(ss,stock.above,stock.t5,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0)
                4217/860/294
            g20:5000-10000:3425/833/306
            g20:6000-9500:3500/847/203
            g20:5000-6000:4097/840/113
            g20:4500-9500:3933/803/346
        仍然无法继续甄别超级强势股,如600756,000961的启动阶段,能够通过cmacd(mdea,mdiff)>0找到初始信号,但无法从噪声中甄别出来
        因为他们不触碰30线,需要进一步考虑
        ss1不变.
        x3 = gand(strend(ma(t[CLOSE],5))>0,strend(stock.ma2)>0,strend(stock.ma3)>0,strend(stock.ma4)>0)
        ss = sfollow(ss1,x3,10)
        
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)
    ldiff,ldea = cmacd(stock.g120)
    lldiff,lldea = cmacd(stock.g250)

    vdiff,vdea = cmacd(t[VOLUME])
    pdiff,pdea = cmacd(t[CLOSE])


    #sfilter = vdiff<vdea
    #sfilter = vdiff<vdea
    sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0  
    #xcross = cross(mdiff,mdea) > 0  

    linelog(stock.code)


    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss1 = sfollow(xcross,sfilter,5)
    
    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0
    
    ss = sfollow(ss1,x2,10)

    gf1 = gand(stock.g20>5000,stock.g20<9500)

    #signal = gand(xcross,stock.above,stock.t5,t[VOLUME]>0,hinc<1200,rhl10<1500,gfilter)
    signal = gand(ss,stock.above,stock.t5,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0)
    
    return signal

def gmacd(stock,ldown=30,astart=60): #
    ''' g60 macd的同时试探ldown均线
        mxi: (-100,0], vfilter:>1.5
                2001.7-2008.12
                评估:总盈亏值=3070,交易次数=57  期望值=670
                总盈亏率(1/1000)=3070,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=298
                赢利次数=17,赢利总值=6164
                亏损次数=39,亏损总值=3094
                平盘次数=1
                2008-2009.5
                评估:总盈亏值=1415,交易次数=8   期望值=1000
                总盈亏率(1/1000)=1415,平均盈亏率(1/1000)=176,盈利交易率(1/1000)=1000
                赢利次数=8,赢利总值=1415
                亏损次数=0,亏损总值=0

        mxi: (-100,0], vfilter:>1.33
                2001.7-2008.12
                评估:总盈亏值=6520,交易次数=26  期望值=41666
                总盈亏率(1/1000)=6520,平均盈亏率(1/1000)=250,盈利交易率(1/1000)=961
                赢利次数=25,赢利总值=6526
                亏损次数=1,亏损总值=6
                平盘次数=0
                2008-2009.5
                评估:总盈亏值=3926,交易次数=111 期望值=492
                总盈亏率(1/1000)=3926,平均盈亏率(1/1000)=35,盈利交易率(1/1000)=279
                赢利次数=31,赢利总值=9542
                亏损次数=79,亏损总值=5616
                平盘次数=1
            macd: 35,77
            评估:总盈亏值=5074,交易次数=91  期望值=763
                总盈亏率(1/1000)=5074,平均盈亏率(1/1000)=55,盈利交易率(1/1000)=296
                赢利次数=27,赢利总值=9624
                亏损次数=63,亏损总值=4550
                平盘次数=1
            36:78
            评估:总盈亏值=4841,交易次数=84  期望值=780
                总盈亏率(1/1000)=4841,平均盈亏率(1/1000)=57,盈利交易率(1/1000)=297
                赢利次数=25,赢利总值=9103
                亏损次数=58,亏损总值=4262
                平盘次数=1
        
            g60 ma3之后：
            评估:总盈亏值=5823,交易次数=97  期望值=845
                总盈亏率(1/1000)=5823,平均盈亏率(1/1000)=60,盈利交易率(1/1000)=329
                赢利次数=32,赢利总值=10401
                亏损次数=64,亏损总值=4578
                平盘次数=1

            评估:总盈亏值=6929,交易次数=31  期望值=5068 #20080601-20090602
                总盈亏率(1/1000)=6929,平均盈亏率(1/1000)=223,盈利交易率(1/1000)=903
                赢利次数=28,赢利总值=7063
                亏损次数=3,亏损总值=134
                平盘次数=0
                
                #之前是
                评估:总盈亏值=5997,交易次数=25  期望值=4596
                总盈亏率(1/1000)=5997,平均盈亏率(1/1000)=239,盈利交易率(1/1000)920
                赢利次数=23,赢利总值=6102
                亏损次数=2,亏损总值=105
            ma5:
                评估:总盈亏值=6850,交易次数=115 期望值=842
                总盈亏率(1/1000)=6850,平均盈亏率(1/1000)=59,盈利交易率(1/1000)=330
                赢利次数=38,赢利总值=12295
                亏损次数=77,亏损总值=5445
                平盘次数=0
            
                评估:总盈亏值=7564,交易次数=34  期望值=5045
                总盈亏率(1/1000)=7564,平均盈亏率(1/1000)=222,盈利交易率(1/1000)=911
                赢利次数=31,赢利总值=7698
                亏损次数=3,亏损总值=134
                平盘次数=0

        目前取1.33
        改成cmacd(svap,19,39)无改进                
    '''

    t = stock.transaction
    
    #mdiff,mdea = cmacd(stock.g5)   
    mdiff,mdea = cmacd(ma(stock.g60,5)) #平滑以去掉首尾效应


    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    #svap,v2i = stock.svap_ma_67
    #sdiff,sdea = cmacd(svap,36,78)
    #ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    #msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],ldown),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    
    gf1 = gand(stock.g20>5000,stock.g20<9500)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    xatr = stock.atr * BASE / t[CLOSE]     
   
    signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0,vfilter,mxi,xatr>=astart)
    
    return signal

def gmacd5(stock,ldown=30,astart=60): #
    ''' g60 macd的同时试探ldown均线
                gf1 = gand(stock.g20>5000,stock.g20<9500)
                #使用g5,ma3
                评估:总盈亏值=5437,交易次数=19  期望值=71500
                    总盈亏率(1/1000)=5437,平均盈亏率(1/1000)=286,盈利交易率(1/1000)=947
                赢利次数=18,赢利总值=5441
                亏损次数=1,亏损总值=4

                评估:总盈亏值=6564,交易次数=68  期望值=1333 #20010701-20081231
                总盈亏率(1/1000)=6564,平均盈亏率(1/1000)=96,盈利交易率(1/1000)=397
                赢利次数=27,赢利总值=9476
                亏损次数=40,亏损总值=2912
                平盘次数=1

            ma5:
                评估:总盈亏值=5764,交易次数=23  期望值=10000
                总盈亏率(1/1000)=5764,平均盈亏率(1/1000)=250,盈利交易率(1/1000)=869
                赢利次数=20,赢利总值=5841
                亏损次数=3,亏损总值=77
                平盘次数=0
    
                评估:总盈亏值=6049,交易次数=84  期望值=888
                总盈亏率(1/1000)=6049,平均盈亏率(1/1000)=72,盈利交易率(1/1000)=357
                赢利次数=30,赢利总值=10372
                亏损次数=53,亏损总值=4323
                平盘次数=1
            直接计算:       #近期表现绝对彪悍
                评估:总盈亏值=3970,交易次数=14  期望值=1000
                总盈亏率(1/1000)=3970,平均盈亏率(1/1000)=283,盈利交易率(1/1000)=1000
                赢利次数=14,赢利总值=3970
                亏损次数=0,亏损总值=0
                平盘次数=0
                
            评估:总盈亏值=3132,交易次数=33  期望值=1146     #20010701-20081231
                总盈亏率(1/1000)=3132,平均盈亏率(1/1000)=94,盈利交易率(1/1000)=424
                赢利次数=14,赢利总值=4701
                亏损次数=19,亏损总值=1569
                平盘次数=0
            去掉msvap: 无此必要
                评估:总盈亏值=6936,交易次数=24  期望值=13136
                    总盈亏率(1/1000)=6936,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=958
                    赢利次数=23,赢利总值=6958
                    亏损次数=1,亏损总值=22
                    平盘次数=0
                评估:总盈亏值=6766,交易次数=83  期望值=1125
                总盈亏率(1/1000)=6766,平均盈亏率(1/1000)=81,盈利交易率(1/1000)=373
                赢利次数=31,赢利总值=10560
                亏损次数=52,亏损总值=3794
                平盘次数=0
                
        目前取1.33
        改成cmacd(svap,19,39)无改进
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g5)   

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    #above = gand(stock.ma2 > stock.ma3,stock.ma3>stock.ma4,stock.ma4>stock.ma5)


    #svap,v2i = stock.svap_ma_67
    #sdiff,sdea = cmacd(svap,36,78)
    #ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    #msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],ldown),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    
    gf1 = gand(stock.g20>5000,stock.g20<9500)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    

    xatr = stock.atr * BASE / t[CLOSE]     
    
    signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0,vfilter,mxi,xatr>=astart)
    #signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0,vfilter,mxi)
    
    return signal


def smacd(stock):
    '''
        36,78
        评估:总盈亏值=45847,交易次数=379        期望值=1643
                总盈亏率(1/1000)=45847,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=448
                赢利次数=170,赢利总值=61166
                亏损次数=209,亏损总值=15319
                平盘次数=0
    
        36,78,     vfilter = vma_s < vma_l 
        评估:总盈亏值=22086,交易次数=126        期望值=2302
                总盈亏率(1/1000)=22086,平均盈亏率(1/1000)=175,盈利交易率(1/1000)=539
                赢利次数=68,赢利总值=26550
                亏损次数=58,亏损总值=4464
                平盘次数=0
            #20080701-20090531:
            评估:总盈亏值=811,交易次数=63   期望值=214
                总盈亏率(1/1000)=811,平均盈亏率(1/1000)=12,盈利交易率(1/1000)=396
                赢利次数=25,赢利总值=2976
                亏损次数=38,亏损总值=2165
                平盘次数=0
            
        ####36,78,     vfilter = vma_s < vma_l * 7/8
        评估:总盈亏值=8997,交易次数=45  期望值=2618
                总盈亏率(1/1000)=8997,平均盈亏率(1/1000)=199,盈利交易率(1/1000)=511
                赢利次数=23,赢利总值=10690
                亏损次数=22,亏损总值=1693
                平盘次数=0
                闭合交易明细:
            #20080701-20090531:
                评估:总盈亏值=1067,交易次数=20  期望值=1060
                总盈亏率(1/1000)=1067,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=600
                赢利次数=12,赢利总值=1470
                亏损次数=8,亏损总值=403
                平盘次数=0
    '''
    t = stock.transaction
    #g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    #g = np.ones_like(stock.g5)
 
    svap,v2i = stock.svap_ma_67 

    diff,dea = cmacd(svap,36,78)
    dcross = gand(cross(dea,diff)>0,strend(diff)>0,strend(dea)>0)

    msvap = transform(dcross,v2i,len(t[VOLUME]))

    linelog(stock.code)
    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8

    return gand(stock.golden,stock.above,msvap,vfilter)


def xru(stock):
    ''' 成交量分配后的移动上叉
    '''
    t = stock.transaction
    mxc = xc_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma>vma*1/2,svma<vma*2/3,t[CLOSE]>stock.ma1)
    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5)
    linelog(stock.code)
    return signal

def xru0(stock,xfunc=xc_ru0,astart=45):
    ''' 成交量分配后的上叉0线
    '''
    t = stock.transaction
    #mxc = xc_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    mxc1 = xfunc(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    #mxc2 = xc_ru02(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    mxc = mxc1
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    #cf = (t[CLOSE]-t[LOW] + t[HIGH]-t[OPEN])*1000 / (t[HIGH]-t[LOW])   #向上的动力，如果取反，完全等效
    mcf = ma(cf,5)
    vfilter = gand(svma>vma*1/2,svma<vma*2/3,t[CLOSE]>stock.ma1,strend(mcf)<0)
    xatr = stock.atr * BASE / t[CLOSE]     
    #signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5)
    signal = gand(mxc,vfilter,stock.thumb,stock.above,stock.t5,xatr>=astart)
    linelog(stock.code)
    return signal

def mxru(stock,astart=40):
    ''' 成交量分配后的macd
    '''
    t = stock.transaction
    mdiff,mdea = macd_ruv(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    mxc = cross(mdea,mdiff) > 0
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    #vfilter = gand(svma>vma*1/3,svma<vma*7/8)
    vfilter = gand(svma<vma*7/8,svma>vma/2,t[VOLUME]<=vma,t[VOLUME]>vma*2/3,t[CLOSE]>stock.ma1) #cf无效果
    xatr = stock.atr * BASE / t[CLOSE]     

    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0,strend(stock.ref.ma2)>0)


    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5,xatr>=astart,xfilter)
    linelog(stock.code)
    return signal

def mxru3(stock,astart=50):
    ''' 成交量分配后的macd,采用supdown3
    '''
    t = stock.transaction
    mdiff,mdea = macd_ruv3(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    mxc = cross(mdea,mdiff) > 0
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    #cf = (t[CLOSE]-t[LOW])*1000 / (t[HIGH]-t[LOW]) < 900    #物极必反
    cf = (t[CLOSE]-t[LOW])*1000 / (t[HIGH]-t[LOW]) < 900    #物极必反, 如果是大阳线，不能收高
    vfilter = gand(svma<vma*7/8,svma>vma/2,t[VOLUME]<=vma,t[CLOSE]>stock.ma1,cf)
    xatr = stock.atr * BASE / t[CLOSE]     
    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0,strend(stock.ref.ma2)>0)
    
    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5,xatr>=astart,xfilter)
    linelog(stock.code)
    return signal


def ldx(stock,mlen=60,glimit=3000,astart=60,aend=1000): #low down xcross 
    ''' 破60日线
                20010701--
                评估:总盈亏值=4858,交易次数=23  期望值=4137
                总盈亏率(1/1000)=4858,平均盈亏率(1/1000)=211,盈利交易率(1/1000)=652
                赢利次数=15,赢利总值=5269
                亏损次数=8,亏损总值=411
                平盘次数=0
                20080701-- 
                评估:总盈亏值=7552,交易次数=84  期望值=1618
                总盈亏率(1/1000)=7552,平均盈亏率(1/1000)=89,盈利交易率(1/1000)=833
                赢利次数=70,赢利总值=8276
                亏损次数=13,亏损总值=724

                将pdiff<pdea改成strend(pdiff-pdea)<0
                    评估:总盈亏值=4969,交易次数=21  期望值=4720
                    总盈亏率(1/1000)=4969,平均盈亏率(1/1000)=236,盈利交易率(1/1000)=714
                    赢利次数=15,赢利总值=5273
                    亏损次数=6,亏损总值=304
                    平盘次数=0
                
                    评估:总盈亏值=7169,交易次数=83  期望值=1653     #####
                    总盈亏率(1/1000)=7169,平均盈亏率(1/1000)=86,盈利交易率(1/1000)=819
                    赢利次数=68,赢利总值=7952
                    亏损次数=15,亏损总值=783
                    平盘次数=0
        

    #破30日线   
        gf1: <3333
            20080701--
            评估:总盈亏值=9474,交易次数=75  期望值=2739
                总盈亏率(1/1000)=9474,平均盈亏率(1/1000)=126,盈利交易率(1/1000)=826
                赢利次数=62,赢利总值=10026
                亏损次数=12,亏损总值=552
                平盘次数=1
                
            20010701--
            评估:总盈亏值=10510,交易次数=55 期望值=3410
                总盈亏率(1/1000)=10510,平均盈亏率(1/1000)=191,盈利交易率(1/1000)=672
                赢利次数=37,赢利总值=11529
                亏损次数=18,亏损总值=1019
                平盘次数=0
            
            将pdiff<pdea改成strend(pdiff-pdea)<0        ##说明对30日线破的情况不适用
            20080701-
            评估:总盈亏值=6452,交易次数=87  期望值=1720
                总盈亏率(1/1000)=6452,平均盈亏率(1/1000)=74,盈利交易率(1/1000)=643
                赢利次数=56,赢利总值=7750
                亏损次数=30,亏损总值=1298
                平盘次数=1
            
            评估:总盈亏值=11927,交易次数=57 期望值=3732
                总盈亏率(1/1000)=11927,平均盈亏率(1/1000)=209,盈利交易率(1/1000)=684
                赢利次数=39,赢利总值=12936
                亏损次数=18,亏损总值=1009
                平盘次数=0


        #120: glimit=3333   
        20010701-20081231
        评估:总盈亏值=811,交易次数=12   期望值=1456
                总盈亏率(1/1000)=811,平均盈亏率(1/1000)=67,盈利交易率(1/1000)=666
                赢利次数=8,赢利总值=995
                亏损次数=4,亏损总值=184
                平盘次数=0
        20080701-20090605
        评估:总盈亏值=1025,交易次数=5   期望值=1198
                总盈亏率(1/1000)=1025,平均盈亏率(1/1000)=205,盈利交易率(1/1000)=800
                赢利次数=4,赢利总值=1196
                亏损次数=1,亏损总值=171
                平盘次数=0
        

    '''

    t = stock.transaction
    
    vma_l = ma(t[VOLUME],30)
    vma_5 = ma(t[VOLUME],5)

    vfilter = gand(vma_5>vma_l*3/5,t[VOLUME] < vma_l*2/3)   

    linelog(stock.code)

    #c = t[LOW]
    #ma30 = ma(c,30)
    #above = gand(ma(c,13) > ma30,ma30>stock.ma4,stock.ma4>stock.ma5)
    
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s)

    gf1 = gand(stock.g60<glimit)

    pdiff,pdea = stock.ref.diff,stock.ref.dea

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    xatr = stock.atr * BASE / t[CLOSE]     

    signal = gand(x2,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,strend(pdiff-pdea)<0,vfilter,mxi,xatr>=astart,xatr<=aend)

    return signal


def ldx2(stock,mlen=30,glimit=3333,astart=60,aend=1000): #low down xcross
    ''' 30日线，使用pdiff<pdea条件
    '''

    t = stock.transaction
    
    vma_l = ma(t[VOLUME],30)
    vma_5 = ma(t[VOLUME],5)

    vfilter = gand(vma_5>vma_l*3/5,t[VOLUME] < vma_l*2/3)   

    linelog(stock.code)

    #c = t[LOW]
    #ma30 = ma(c,30)
    #above = gand(ma(c,13) > ma30,ma30>stock.ma4,stock.ma4>stock.ma5)
    
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s)

    gf1 = gand(stock.g60<glimit)

    pdiff,pdea = stock.ref.diff,stock.ref.dea

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)

    xatr = stock.atr * BASE / t[CLOSE]     

    signal = gand(x2,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,pdiff<pdea,vfilter,mxi,xatr>=astart,xatr<=aend)

    return signal


def xud(stock,xfunc=xc0s,astart=45):
    ''' 
    '''
    t = stock.transaction
    mxc = xfunc(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=10) > 0

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<vma*2/3)

    stdea = strend(stock.dea)
    stdiff = strend(stock.diff)
    st = gand(stdea<=-3,stdea>=-4,stdiff<=-5,stdiff>=-6)
    #st = gand(stdea<=-3,stdiff>=-6,stdea>stdiff)

    s=stock
    thumb = gand(s.g20>=3000,s.g20<=8000)

    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0)

    signal = gand(mxc,vfilter,thumb,stock.above,stock.t5,stock.ma1<stock.ma2,stock.ma1>stock.ma3,st,xfilter)#,mcf>1000)
    linelog(stock.code)
    return signal

def xudj(stock):
    ''' xud针对基金的特别处理
        #20080701--
        评估:总盈亏值=925,交易次数=9    期望值=6375
                总盈亏率(1/1000)=925,平均盈亏率(1/1000)=102,盈利交易率(1/1000)=888
                赢利次数=8,赢利总值=941
                亏损次数=1,亏损总值=16
                平盘次数=0
    
        #20010701--
        评估:总盈亏值=4455,交易次数=27  期望值=2894
                总盈亏率(1/1000)=4455,平均盈亏率(1/1000)=165,盈利交易率(1/1000)=925
                赢利次数=25,赢利总值=4570
                亏损次数=2,亏损总值=115
                平盘次数=0
    
    '''
    linelog(stock.code)
    t = stock.transaction
    if stock.code[:3] != 'SH5' and stock.code[:4]!='SZ18':    
        return cached_zeros(len(t[CLOSE]))
        #raise Exception(u'skipping ' + stock.code)
    
    mxc = xc0s(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=13) > 0

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma>vma*2/3)
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    xatr = stock.atr * BASE / t[CLOSE]

    #signal = gand(mxc,stock.above,stock.t5,mcf>1000,stock.ma1<stock.ma2,stock.ma1>stock.ma3,stock.g20 >= stock.g60,stock.g60 >= stock.g120)
    signal = gand(mxc,stock.above,stock.t5,stock.ma1<stock.ma2,stock.g20 >= stock.g60,stock.g60 >= stock.g120)
    return signal

def xud0(stock):
    ''' xud对大盘股的优化
        zgb<300000,ag<200000,xatr<=45,xc0s
        #20080701--
        评估:总盈亏值=2977,交易次数=24  期望值=3444
                总盈亏率(1/1000)=2977,平均盈亏率(1/1000)=124,盈利交易率(1/1000)=958
                赢利次数=23,赢利总值=3013
                亏损次数=1,亏损总值=36
                平盘次数=0
        #20010701--
        评估:总盈亏值=2158,交易次数=10  期望值=5810
                总盈亏率(1/1000)=2158,平均盈亏率(1/1000)=215,盈利交易率(1/1000)=600
                赢利次数=6,赢利总值=2307
                亏损次数=4,亏损总值=149
                平盘次数=0
    '''
    linelog(stock.code)
    t = stock.transaction
    if stock.zgb <= 300000 and stock.ag <=200000:
        raise Exception(u'skipping ' + stock.code)
    
    mxc = xc0s(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=13) > 0
    mxc=scover(mxc,3)

    stdea = strend(stock.dea)
    stdiff = strend(stock.diff)
    st = gand(stdea<=-3,stdea>=-4,stdiff<=-4,stdiff>=-7)

    xatr = stock.atr * BASE / t[CLOSE]

    signal = gand(mxc,st,xatr<45,stock.above,stock.t5,stock.ma1<stock.ma2,stock.g20 >= stock.g60,stock.g60 >= stock.g120)    
    return signal

def emv1(stock,fast=15):
    t = stock.transaction

    ##fast = 75       #1565-44-500-108-4695, 3018-53-698-163-8150
    ##fast = 15       #1684-68-470-123-6150,2237-93-741-132-6000
    #fast = 98       #886-34-411-78-4333,3063-30-733-144-6000  
    #fast = 120      #1246-30-533-101-5050,2639-27-814-161-5750   

    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv1 = msum2(em,fast)
    
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)

    baseline = cached_zeros(len(t[CLOSE]))

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20>=3000,stock.g20<8000)
    thumb = gand(stock.magic,stock.g20>3000)
    #thumb = stock.magic

    ecross = gand(thumb,cross(baseline,mv1)>0,strend(mv1)>0,stock.t5,stock.above,vfilter)
    linelog(stock.code)
    return ecross

def emv1b(stock,fast=15,base=120):
    t = stock.transaction

    ##fast = 75       #1565-44-500-108-4695, 3018-53-698-163-8150
    ##fast = 15       #1684-68-470-123-6150,2237-93-741-132-6000
    #fast = 98       #886-34-411-78-4333,3063-30-733-144-6000  
    #fast = 120      #1246-30-533-101-5050,2639-27-814-161-5750   

    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv1 = msum2(em,fast)
    mvbase = msum2(em,base)

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)

    baseline = cached_zeros(len(t[CLOSE]))

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20>=3000,stock.g20<8000)
    thumb = gand(stock.magic,stock.g20>3000)
    #thumb = stock.magic    

    ecross = gand(thumb,cross(baseline,mv1)>0,strend(mv1)>0,stock.t5,stock.above,strend(mvbase)>0,vfilter)
    linelog(stock.code)
    return ecross

def emv2(stock,fast,slow):
    t = stock.transaction
    #2872-34-676-247-9880,1000-1-1000-75-3750

    em = emv(t[HIGH],t[LOW],t[VOLUME])
   
    mv1 = ma(em,fast)
    mv2 = ma(em,slow)

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)
 
    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)#,stock.g20>=3000)
    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120>=stock.g250,stock.g20>=3000,stock.g20<8000)    
    thumb = gand(stock.magic,stock.g20>3000)
    #thumb = stock.magic

    ecross = gand(thumb,cross(mv2,mv1)>0,strend(mv2)>0,mv2<0,stock.t5,stock.above,vfilter)
    linelog(stock.code)
    return ecross

def emv2s(stock,fast=7,slow=30):    #去掉g5
    t = stock.transaction

    #1880-33-424-141-5875,4225-25-760-169-5827

    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv1 = msum2(em,fast)
    mv2 = msum2(em,slow)
    
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)
 
    thumb = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    ecross = gand(thumb,cross(mv2,mv1)>0,strend(mv2)>0,mv2<=0,stock.t5,stock.above,vfilter)
    linelog(stock.code)
    return ecross


def tsvama4(stock,afast,aslow,bfast,bslow,follow=7):
    ''' svama两线交叉
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2
    ma_svapfast_a = ma(svap,afast)
    ma_svapslow_a = ma(svap,aslow)
    trend_ma_svapfast_a = strend(ma_svapfast_a) > 0
    trend_ma_svapslow_a = strend(ma_svapslow_a) > 0
    cross_fast_slow_a = gand(cross(ma_svapslow_a,ma_svapfast_a)>0,trend_ma_svapfast_a,trend_ma_svapslow_a)


    ma_svapfast_b = ma(svap,bfast)
    ma_svapslow_b = ma(svap,bslow)
    trend_ma_svapfast_b = strend(ma_svapfast_b) > 0
    trend_ma_svapslow_b = strend(ma_svapslow_b) > 0
    cross_fast_slow_b = gand(cross(ma_svapslow_b,ma_svapfast_b)>0,trend_ma_svapfast_b,trend_ma_svapslow_b)

    ss = sfollow(cross_fast_slow_a,cross_fast_slow_b,follow)
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama4.__name__,stock.code))

    #vma_s = ma(t[VOLUME],13)
    #vma_l = ma(t[VOLUME],30)

    #vfilter = vma_s < vma_l * 7/8
 
    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(msvap,stock.above,stock.t5,stock.magic)#,vfilter)

def tsvama3(stock,fast,mid,slow,follow=7):
    ''' svama三线交叉
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2

    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,follow)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,follow)
    
    msvap = transform(sync3,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama3.__name__,stock.code))

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(msvap,stock.above,stock.t5,stock.magic)

def tsvama2sb(stock,fast,slow,follow=7):
    ''' svama慢线下叉快线，follow日后再上叉回来
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2

    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast)
    trend_ma_svapslow = strend(ma_svapslow)

    cross_down = band(cross(ma_svapslow,ma_svapfast)<0,trend_ma_svapfast<0)    
    cross_up = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast>0)        
    
    sdown = transform(cross_down,v2i,len(t[VOLUME]))
    sup = transform(cross_up,v2i,len(t[VOLUME]))    
    
    sync_down_up = sfollow(sdown,sup,follow)
    
    linelog('%s:%s' % (tsvama2sb.__name__,stock.code))

    #vma_s = ma(t[VOLUME],13)
    #vma_l = ma(t[VOLUME],30)

    #vfilter = vma_s > vma_l 

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(sync_down_up,stock.above,stock.t5,stock.magic)#,vfilter)


def tsvama2sbv(stock,fast,slow,follow=7):
    ''' svama慢线下叉快线，follow日后再上叉回来
        添加vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2

    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast)
    trend_ma_svapslow = strend(ma_svapslow)

    cross_down = band(cross(ma_svapslow,ma_svapfast)<0,trend_ma_svapfast<0)    
    cross_up = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast>0)        
    
    sdown = transform(cross_down,v2i,len(t[VOLUME]))
    sup = transform(cross_up,v2i,len(t[VOLUME]))    
    
    sync_down_up = sfollow(sdown,sup,follow)
    
    linelog('%s:%s' % (tsvama2sbv.__name__,stock.code))

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(sync_down_up,stock.above,stock.t5,stock.magic,vfilter)

def ma2s(stock,fast,slow,follow=7):
    ''' svama慢线下叉快线，follow日后再上叉回来
        buyer=fcustom(x.ma2s,slow=30,fast=7,follow=5)
    '''
    t = stock.transaction

    ma_fast = ma(t[CLOSE],fast)
    ma_slow = ma(t[CLOSE],slow)
    trend_ma_fast = strend(ma_fast)
    trend_ma_slow = strend(ma_slow)

    cross_down = gand(cross(ma_slow,ma_fast)<0,trend_ma_fast<0)    
    cross_up = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast>0,trend_ma_slow>0)        
    sync_down_up = sfollow(cross_down,cross_up,follow)
    
    linelog('%s:%s' % (ma2s.__name__,stock.code))

    #vma_s = ma(t[VOLUME],13)
    #vma_l = ma(t[VOLUME],30)

    #vfilter = vma_s > vma_l 

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(sync_down_up,stock.above,stock.t5,stock.magic,stock.ma1>stock.ma3)#,vfilter)


def ma2sv(stock,fast,slow,follow=7):
    ''' svama慢线下叉快线，follow日后再上叉回来
        buyer=fcustom(x.ma2s,slow=30,fast=7,follow=5), 2001-2008不行
    '''
    t = stock.transaction

    ma_fast = ma(t[CLOSE],fast)
    ma_slow = ma(t[CLOSE],slow)
    trend_ma_fast = strend(ma_fast)
    trend_ma_slow = strend(ma_slow)

    cross_down = gand(cross(ma_slow,ma_fast)<0,trend_ma_fast<0)    
    cross_up = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast>0,trend_ma_slow>0)        
    sync_down_up = sfollow(cross_down,cross_up,follow)
    
    linelog('%s:%s' % (ma2sv.__name__,stock.code))

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s < vma_l,vma_s>vma_l*2/3)

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(sync_down_up,stock.above,stock.t5,stock.magic,stock.ma1>stock.ma3,vfilter,stock.t3)

def tsvama3b(stock,fast,mid,slow,follow=7):
    ''' svama三线交叉
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2

    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    
    s1 = transform(cross_fast_mid,v2i,len(t[VOLUME]))
    s2 = transform(cross_fast_slow,v2i,len(t[VOLUME]))    
    s3 = transform(cross_mid_slow,v2i,len(t[VOLUME]))    

    sync12 = sfollow(s1,s2,follow)
    sync3 = sfollow(sync12,s3,follow)
    
    linelog('%s:%s' % (tsvama3b.__name__,stock.code))

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    return gand(sync3,stock.above,stock.t5,stock.magic)


#板块计算函数
def tsvama2c(stock,fast=7,slow=250,bxatr=50):
    ''' svama两线交叉
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    #sdiff,sdea = cmacd(svap)
    #ss = gand(cross_fast_slow,strend(sdiff-sdea)>0)
    #ss = cross_fast_slow
    ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    xatr = stock.atr * BASE / t[CLOSE]
    thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)
    return gand(msvap,stock.above,stock.t5,xatr>bxatr,thumb)

def ma2c(stock,fast,slow,follow=7):
    ''' 
    '''
    t = stock.transaction

    ma_fast = ma(t[CLOSE],fast)
    ma_slow = ma(t[CLOSE],slow)
    trend_ma_fast = strend(ma_fast)
    trend_ma_slow = strend(ma_slow)

    cross_up = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast>0,trend_ma_slow>0)        
    
    linelog('%s:%s' % (ma2c.__name__,stock.code))

    return gand(cross_up,stock.above,stock.t5,stock.magic)

def ldxc(stock,mlen=60,astart=60,aend=1000): #low down xcross 
    t = stock.transaction
    
    linelog(stock.code)
  
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s)

    pdiff,pdea = stock.ref.diff,stock.ref.dea

    xatr = stock.atr * BASE / t[CLOSE]     

    signal = gand(x2,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,xatr>=astart,xatr<=aend,stock.magic)

    return signal

def emv1c(stock,fast):
    t = stock.transaction

    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv1 = msum2(em,fast)
    
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)

    baseline = cached_zeros(len(t[CLOSE]))

    thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120>=stock.g250,stock.g20>=3000,stock.g20<8000)

    ecross = gand(thumb,cross(baseline,mv1)>0,strend(mv1)>0,stock.t5,stock.above)
    
    linelog(stock.code)
    return ecross

def emv2c(stock,fast,slow):
    t = stock.transaction

    em = emv(t[HIGH],t[LOW],t[VOLUME])
    #mv1 = msum2(em,fast)
    #mv2 = msum2(em,slow)
    
    mv1 = ma(em,fast)
    mv2 = ma(em,slow)

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)
    #vfilter = gand(svma<=vma*7/8)
 
    thumb = gand(stock.g5>stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)#,stock.g20>=3000)
    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120>=stock.g250,stock.g20>=3000,stock.g20<8000)    

    ecross = gand(thumb,cross(mv2,mv1)>0,strend(mv2)>0,mv2<0,stock.t5,stock.above)
    linelog(stock.code)
    return ecross


def eff(stock):
    ''' 效果不平衡,seller2000
        200501-200909
        评估:总盈亏值=25823,交易次数=104        期望值=3815
                总盈亏率(1/1000)=25823,平均盈亏率(1/1000)=248,盈利交易率(1/1000)=673
                平均持仓时间=36,持仓效率(1/1000000)=6888
                赢利次数=70,赢利总值=28051
                亏损次数=34,亏损总值=2228
                平盘次数=0

        200711-200909
        评估:总盈亏值=15146,交易次数=45 期望值=5694
                总盈亏率(1/1000)=15146,平均盈亏率(1/1000)=336,盈利交易率(1/1000)=800
                平均持仓时间=46,持仓效率(1/1000000)=7304
                赢利次数=36,赢利总值=15684
                亏损次数=9,亏损总值=538
                平盘次数=0
        多选时选择线路走的最顺的那个，比如ma0-->ma5都符合above的
    '''
    linelog(stock.code)
    t = stock.transaction    
    ef = efficient_rate(t[CLOSE])
    zx = cached_zeros(len(t[CLOSE]))
    efz = gand(cross(zx,ef)>0,strend(ef)>0)
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*3/4,t[VOLUME]<vma)
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7) 

    refn = gand(stock.ref.ma0<stock.ref.ma1,stock.ref.ma1<stock.ref.ma2,bnot(stock.ref.t0),bnot(stock.ref.t1),bnot(stock.ref.t2))
    sup = gand(stock.ma0>stock.ma1,stock.ma1>stock.ma2,stock.t1,stock.t2)

    sa1 = gand(efz,bor(bnot(refn),sup))
    sa2 = sfollow(efz,bnot(refn),10)
    ssa = bor(sa1,sa2)
    
    s=stock
    magic = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g5>s.g20,s.g20<=8000)

    xatr = stock.atr * BASE / t[CLOSE]     

    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0,strend(stock.ref.ma2)>0)


    #signal = gand(ssa,stock.above,stock.t5,stock.t4,magic,vfilter,mcf<1000)
    signal = gand(ssa,stock.above,stock.t5,stock.t4,magic,vfilter,mcf<1000,xatr>40,stock.diff<stock.dea,strend(stock.diff-stock.dea)>0,xfilter)
    return signal

###以下为小时线应用
def mag(stock):
    '''
        只在大牛市中有意义,未继续检验
        0501-0909
        评估:总盈亏值=37642,交易次数=119        期望值=4051
                总盈亏率(1/1000)=37642,平均盈亏率(1/1000)=316,盈利交易率(1/1000)=781
                平均持仓时间=37,持仓效率(1/1000000)=8540
                赢利次数=93,赢利总值=39684
                亏损次数=26,亏损总值=2042
                平盘次数=0
                
        0807--0909
        评估:总盈亏值=4108,交易次数=26  期望值=1950
                总盈亏率(1/1000)=4108,平均盈亏率(1/1000)=158,盈利交易率(1/1000)=692
                平均持仓时间=38,持仓效率(1/1000000)=4157
                赢利次数=18,赢利总值=4760
                亏损次数=8,亏损总值=652
                平盘次数=0

    '''    
    s = stock
    t = stock.transaction    
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*3/2,svma>vma*2/3)
    xatr = stock.atr * BASE / t[CLOSE]     
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)
    magnify = gand(stock.ma4_up,stock.mup_100)
    linelog(stock.code)
    magic = gand(s.g20 >= s.g120,s.g60 >= s.g120,s.g120 >= s.g250,s.g5<s.g20,s.g20<=8000)
    hma7 = ma(stock.hour,7)
    hma13 = ma(stock.hour,13)
    hma30 = ma(stock.hour,30)
    hs = hour2day(gand(stock.hour > hma7,gswing(hma7,hma13,hma30,5)<60))
    signal = gand(magnify,s.above,stock.t5,stock.t4,xatr>45,xatr<60,magic,vfilter,mcf<800,stock.ma1>stock.ma3,hs,stock.diff>stock.dea)
    return signal

def heff(stock):
    ''' 效果不平衡
        0501-0909
        评估:总盈亏值=35014,交易次数=178        期望值=2684
                总盈亏率(1/1000)=35014,平均盈亏率(1/1000)=196,盈利交易率(1/1000)=612
                平均持仓时间=32,持仓效率(1/1000000)=6125
                赢利次数=109,赢利总值=40100
                亏损次数=69,亏损总值=5086
                平盘次数=0
        0711-0909
        评估:总盈亏值=17918,交易次数=63 期望值=4437
                总盈亏率(1/1000)=17918,平均盈亏率(1/1000)=284,盈利交易率(1/1000)=809
                平均持仓时间=43,持仓效率(1/1000000)=6604
                赢利次数=51,赢利总值=18686
                亏损次数=12,亏损总值=768
                平盘次数=0

    '''
    linelog(stock.code)
    t = stock.transaction    
    ef = efficient_rate(stock.hour)
    zx = cached_zeros(len(stock.hour))
    efz = hour2day(gand(cross(zx,ef)>0,strend(ef)>0))
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*3/4,t[VOLUME]<vma)
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7) 

    refn = gand(stock.ref.ma0<stock.ref.ma1,stock.ref.ma1<stock.ref.ma2,bnot(stock.ref.t0),bnot(stock.ref.t1),bnot(stock.ref.t2))
    sup = gand(stock.ma0>stock.ma1,stock.ma1>stock.ma2,stock.t1,stock.t2)

    s1 = gand(efz,bor(bnot(refn),sup))
    s2 = sfollow(efz,bnot(refn),10)
    ss = bor(s1,s2)
    s = stock
    magic = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g5>s.g20,s.g20<=8000)
    xatr = stock.atr * BASE / t[CLOSE]     

    #signal = gand(ss,stock.above,stock.t5,stock.t4,magic,vfilter,mcf<1000)
    signal = gand(ss,stock.above,stock.t5,stock.t4,magic,vfilter,mcf<1000,xatr>40,stock.ma1>stock.ma3,stock.diff<stock.dea)
    return signal

def uplain(stock):
    '''
        长期稳定性不够
    '''
    t = stock.transaction

    m1,m2,m3,m4 = stock.ma0,stock.ma1,stock.ma2,ma(t[CLOSE],20)
    mmax = gmax(m1,m2,m3,m4)
    mmin = gmin(m1,m2,m3,m4)

    smm = strend(ma(mmax-mmin,5))<-5

    #print (mmax-mmin)[-60:]

    ndev = (mmax-mmin) * 1000 / mmin< 15

    sdev = msum(ndev,2) > 1 #连续2天

    #print sdev[-60:]
    #print ((mmax-mmin) * 1000 / mmin)[-60:]

    nup = t[CLOSE] > mmax

    smacd = gand(cross(stock.dea,stock.diff)>0,strend(stock.diff)>0)
    
    nsignal = sfollow(sdev,smacd,100)

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<vma)

    #signal = gand(nup,ndev,stock.t3,stock.t4,stock.ma3>stock.ma4,stock.ma4>stock.ma5,vfilter,nwidth,stock.g5<stock.g20,stock.g20<stock.g60)

    signal = gand(nsignal,smm,stock.t4,stock.t5,vfilter,stock.thumb)
    linelog(stock.code)
    return signal

def uinfunc3a(wline,base,len1,len2,len3):
    m1,m2,m3 = ma(wline,len1),ma(wline,len2),ma(wline,len3)
    mmax = gmax(m1,m2,m3)
    mmin = gmin(m1,m2,m3)

    mm2 = gmax(m1,m2)

    ndev = (mmax-mmin) * 1000 / base < 1500

    xcross = gand(cross(mmax,wline),strend(wline)>0)

    return gand(xcross,ndev,strend(m1)>0,mm2>m3)

def uinfunc3b(wline,base,len1,len2,len3):
    m1,m2,m3 = ma(wline,len1),ma(wline,len2),ma(wline,len3)
    mmax = gmax(m1,m2,m3)
    mmin = gmin(m1,m2,m3)

    ndev = (mmax-mmin) * 1000 / base < 1200

    xcross = gand(cross(mmax,wline),strend(wline)>0)

    return gand(xcross,ndev,strend(m1)>0)

def uinfunc3c(wline,base,len1,len2,len3):
    m1,m2,m3 = ma(wline,len1),ma(wline,len2),ma(wline,len3)
    mmax = gmax(m1,m2,m3)
    mmin = gmin(m1,m2,m3)

    ndev = (mmax-mmin) * 1000 / base < 1200

    xcross = gand(cross(mmax,wline),strend(wline)>0)

    return gand(xcross,ndev,strend(m1)>0)


def uplain3(stock,lens,infunc=uinfunc3a):
    ''' 20070101,20080101,20191201
        buyer=fcustom(t.uplain3,lens=(7,13,30))     #
        评估:总盈亏值=2382,交易次数=19  期望值=3676
                总盈亏率(1/1000)=2382,平均盈亏率(1/1000)=125,盈利交易率(1/1000)=894
                平均持仓时间=34,持仓效率(1/1000000)=3676
                赢利次数=17,赢利总值=2416
                亏损次数=1,亏损总值=34
                平盘次数=1
        buyer=fcustom(t.uplain3,lens=(3,7,13))      
        评估:总盈亏值=2065,交易次数=15  期望值=2537
                总盈亏率(1/1000)=2065,平均盈亏率(1/1000)=137,盈利交易率(1/1000)=733
                平均持仓时间=23,持仓效率(1/1000000)=5956
                赢利次数=11,赢利总值=2282
                亏损次数=4,亏损总值=217
                平盘次数=0

        buyer=fcustom(t.uplain3,lens=(5,13,26))     #
        评估:总盈亏值=1812,交易次数=14  期望值=1000
                总盈亏率(1/1000)=1812,平均盈亏率(1/1000)=129,盈利交易率(1/1000)=928
                平均持仓时间=34,持仓效率(1/1000000)=3794
                赢利次数=13,赢利总值=1812
                亏损次数=0,亏损总值=0
                平盘次数=1

        buyer=fcustom(t.uplain3,lens=(4,13,27)) #月/季/半年
        评估:总盈亏值=1901,交易次数=17  期望值=3264
                总盈亏率(1/1000)=1901,平均盈亏率(1/1000)=111,盈利交易率(1/1000)=882
                平均持仓时间=32,持仓效率(1/1000000)=3468
                赢利次数=15,赢利总值=1935
                亏损次数=1,亏损总值=34
                平盘次数=1

        buyer=fcustom(t.uplain3,lens=(2,5,13))      #
        评估:总盈亏值=2442,交易次数=25  期望值=1763
                总盈亏率(1/1000)=2442,平均盈亏率(1/1000)=97,盈利交易率(1/1000)=760
                平均持仓时间=25,持仓效率(1/1000000)=3880
                赢利次数=19,赢利总值=2772
                亏损次数=6,亏损总值=330
                平盘次数=0


        20040101,20050101,20071031
        name:Mediator:<uplain3:lens=(7, 13, 30):seller:make_trade_signal_advanced:B1S1>     ############
        评估:总盈亏值=567,交易次数=6	期望值=723
		总盈亏率(1/1000)=567,平均盈亏率(1/1000)=94,盈利交易率(1/1000)=666
		平均持仓时间=22,持仓效率(1/1000000)=4272
		赢利次数=4,赢利总值=828
		亏损次数=2,亏损总值=261
		平盘次数=0

        name:Mediator:<uplain3:lens=(5, 13, 26):seller:make_trade_signal_advanced:B1S1>
        评估:总盈亏值=-188,交易次数=5	期望值=-295
		总盈亏率(1/1000)=-188,平均盈亏率(1/1000)=-38,盈利交易率(1/1000)=400
		平均持仓时间=17,持仓效率(1/1000000)=-2236
		赢利次数=2,赢利总值=200
		亏损次数=3,亏损总值=388
		平盘次数=0
		闭合交易明细:        

        name:Mediator:<uplain3:lens=(2, 5, 13):seller:make_trade_signal_advanced:B1S1>
        评估:总盈亏值=-667,交易次数=8	期望值=-757
		总盈亏率(1/1000)=-667,平均盈亏率(1/1000)=-84,盈利交易率(1/1000)=125
		平均持仓时间=13,持仓效率(1/1000000)=-6462
		赢利次数=1,赢利总值=113
		亏损次数=7,亏损总值=780
		平盘次数=0
		闭合交易明细:        

    '''
    t = stock.transaction
    i_cofw = stock.i_cofw

    signal = np.zeros(len(t[CLOSE]),int)
    
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    
    dgd = msum(greater(stock.diff,stock.dea),11)

    
    #signal[i_cofw] = infunc(t[CLOSE][i_cofw],5,10,20,stock.atr[i_cofw])    #infunc=uinfunc3b
    #signal[i_cofw] = infunc(t[CLOSE][i_cofw],7,13,30,stock.atr[i_cofw])
    signal[i_cofw] = infunc(t[CLOSE][i_cofw],stock.atr[i_cofw],*lens)
    #signal[i_cofw] = uinfunc4(t[CLOSE][i_cofw],7,13,30,60,stock.atr[i_cofw])

    f60 = gor(strend(stock.ma4)<0,stock.ma4<stock.ma5)

    ma6 = ma(t[CLOSE],250)
    bndown = bnot(gand(stock.ma5>stock.ma4,ma6>stock.ma5))
    linelog(stock.code)
    return gand(signal,stock.t5,stock.golden,xatr<mxatr,stock.diff>stock.dea,dgd<11,f60,bndown,stock.ref.mfilter)

def uplain32(stock,lens,infunc=uinfunc3a):
    '''
        buyer=fcustom(t.uplain32,lens=(5,10,20),infunc=t.uinfunc3b) #
        评估:总盈亏值=1902,交易次数=17  期望值=1480
                总盈亏率(1/1000)=1902,平均盈亏率(1/1000)=111,盈利交易率(1/1000)=941
                平均持仓时间=31,持仓效率(1/1000000)=3580
                赢利次数=16,赢利总值=1977
                亏损次数=1,亏损总值=75
                平盘次数=0

        buyer=fcustom(t.uplain32,lens=(3,7,13),infunc=t.uinfunc3b)  #
        评估:总盈亏值=2408,交易次数=21  期望值=2425
                总盈亏率(1/1000)=2408,平均盈亏率(1/1000)=114,盈利交易率(1/1000)=761
                平均持仓时间=23,持仓效率(1/1000000)=4956
                赢利次数=16,赢利总值=2644
                亏损次数=5,亏损总值=236
                平盘次数=0
        buyer=fcustom(t.uplain32,lens=(5,13,26))
        评估:总盈亏值=630,交易次数=3    期望值=1000
                总盈亏率(1/1000)=630,平均盈亏率(1/1000)=210,盈利交易率(1/1000)=1000
                平均持仓时间=38,持仓效率(1/1000000)=5526
                赢利次数=3,赢利总值=630
                亏损次数=0,亏损总值=0
                平盘次数=0

        buyer=fcustom(t.uplain32,lens=(5,13,26),infunc=t.uinfunc3b) 
        评估:总盈亏值=2208,交易次数=20  期望值=2037
                总盈亏率(1/1000)=2208,平均盈亏率(1/1000)=110,盈利交易率(1/1000)=800
                平均持仓时间=26,持仓效率(1/1000000)=4230
                赢利次数=16,赢利总值=2426
                亏损次数=4,亏损总值=218
                平盘次数=0

        buyer=fcustom(t.uplain32,lens=(4,13,27),infunc=t.uinfunc3b) #月/季/半年
        评估:总盈亏值=2153,交易次数=18  期望值=2704
                总盈亏率(1/1000)=2153,平均盈亏率(1/1000)=119,盈利交易率(1/1000)=833
                平均持仓时间=27,持仓效率(1/1000000)=4407
                赢利次数=15,赢利总值=2287
                亏损次数=3,亏损总值=134
                平盘次数=0
        buyer=fcustom(t.uplain32,lens=(4,13,27))
        评估:总盈亏值=722,交易次数=4    期望值=1000
                总盈亏率(1/1000)=722,平均盈亏率(1/1000)=180,盈利交易率(1/1000)=1000
                平均持仓时间=35,持仓效率(1/1000000)=5142
                赢利次数=4,赢利总值=722
                亏损次数=0,亏损总值=0
                平盘次数=0
        buyer=fcustom(t.uplain32,lens=(2,5,13))
        评估:总盈亏值=1779,交易次数=19  期望值=1978
                总盈亏率(1/1000)=1779,平均盈亏率(1/1000)=93,盈利交易率(1/1000)=736
                平均持仓时间=24,持仓效率(1/1000000)=3875
                赢利次数=14,赢利总值=2015
                亏损次数=5,亏损总值=236
        
        buyer=fcustom(t.uplain32,lens=(2,5,13),infunc=t.uinfunc3b)  #
        评估:总盈亏值=2567,交易次数=24  期望值=2255
                总盈亏率(1/1000)=2567,平均盈亏率(1/1000)=106,盈利交易率(1/1000)=791
                平均持仓时间=25,持仓效率(1/1000000)=4240
                赢利次数=19,赢利总值=2803
                亏损次数=5,亏损总值=236
                平盘次数=0

        buyer=fcustom(t.uplain32,lens=(3,9,27),infunc=t.uinfunc3b)  #
        评估:总盈亏值=1245,交易次数=12  期望值=1839
                总盈亏率(1/1000)=1245,平均盈亏率(1/1000)=103,盈利交易率(1/1000)=833
                平均持仓时间=25,持仓效率(1/1000000)=4120
                赢利次数=10,赢利总值=1358
                亏损次数=2,亏损总值=113
                平盘次数=0

        20040101,20050101,20071031
        name:Mediator:<uplain32:lens=(5, 10, 20),infunc=<function uinfunc3b at 0x01772430>:seller:make_trade_signal_advanced:B1S1>      ################
        评估:总盈亏值=0,交易次数=0	期望值=1000
		总盈亏率(1/1000)=0,平均盈亏率(1/1000)=0,盈利交易率(1/1000)=0
		平均持仓时间=1,持仓效率(1/1000000)=0
		赢利次数=0,赢利总值=0
		亏损次数=0,亏损总值=0
		平盘次数=0
		闭合交易明细:        
        
        name:Mediator:<uplain32:lens=(3, 7, 13),infunc=<function uinfunc3b at 0x01772430>:seller:make_trade_signal_advanced:B1S1>
        评估:总盈亏值=-131,交易次数=1	期望值=-1000
		总盈亏率(1/1000)=-131,平均盈亏率(1/1000)=-131,盈利交易率(1/1000)=0
		平均持仓时间=17,持仓效率(1/1000000)=-7706
		赢利次数=0,赢利总值=0
		亏损次数=1,亏损总值=131        

        name:Mediator:<uplain32:lens=(4, 13, 27),infunc=<function uinfunc3b at 0x01772430>:seller:make_trade_signal_advanced:B1S1>
        评估:总盈亏值=-131,交易次数=1	期望值=-1000
		总盈亏率(1/1000)=-131,平均盈亏率(1/1000)=-131,盈利交易率(1/1000)=0
		平均持仓时间=17,持仓效率(1/1000000)=-7706
		赢利次数=0,赢利总值=0
		亏损次数=1,亏损总值=131
		平盘次数=0
		闭合交易明细:        

        name:Mediator:<uplain32:lens=(2, 5, 13),infunc=<function uinfunc3b at 0x01772430>:seller:make_trade_signal_advanced:B1S1>
        评估:总盈亏值=-211,交易次数=2	期望值=-1010
		总盈亏率(1/1000)=-211,平均盈亏率(1/1000)=-106,盈利交易率(1/1000)=0
		平均持仓时间=17,持仓效率(1/1000000)=-6236
		赢利次数=0,赢利总值=0
		亏损次数=2,亏损总值=211
		平盘次数=0
		闭合交易明细:
        
        name:Mediator:<uplain32:lens=(3, 9, 27),infunc=<function uinfunc3b at 0x01772430>:seller:make_trade_signal_advanced:B1S1>
        评估:总盈亏值=-131,交易次数=1	期望值=-1000
		总盈亏率(1/1000)=-131,平均盈亏率(1/1000)=-131,盈利交易率(1/1000)=0
		平均持仓时间=17,持仓效率(1/1000000)=-7706
		赢利次数=0,赢利总值=0
		亏损次数=1,亏损总值=131
		平盘次数=0
		闭合交易明细:

    '''
    t = stock.transaction
    i_cofw = stock.i_cofw

    signal = np.zeros(len(t[CLOSE]),int)
    
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    
    dgd = msum(greater(stock.diff,stock.dea),11)

    
    #signal[i_cofw] = infunc(t[CLOSE][i_cofw],5,10,20,stock.atr[i_cofw])    #infunc=uinfunc3b
    #signal[i_cofw] = infunc(t[CLOSE][i_cofw],7,13,30,stock.atr[i_cofw])
    signal[i_cofw] = infunc(t[CLOSE][i_cofw],stock.atr[i_cofw],*lens)
    #signal[i_cofw] = uinfunc4(t[CLOSE][i_cofw],7,13,30,60,stock.atr[i_cofw])

    f60 = gand(strend(stock.ma4)<0,stock.ma4<stock.ma5) #与1不同

    ma6 = ma(t[CLOSE],250)
    bndown = bnot(gand(stock.ma5>stock.ma4,ma6>stock.ma5))

    linelog(stock.code)
    return gand(signal,stock.t5,stock.golden,xatr<mxatr,stock.diff>stock.dea,dgd<11,f60,bndown,stock.ref.mfilter)


def uplain33(stock,lens,infunc=uinfunc3a):
    '''
       buyer=fcustom(t.uplain3,lens=(5,10,20),infunc=t.uinfunc3b)
        评估:总盈亏值=1731,交易次数=17  期望值=1629
                总盈亏率(1/1000)=1731,平均盈亏率(1/1000)=101,盈利交易率(1/1000)=823
                平均持仓时间=25,持仓效率(1/1000000)=4040
                赢利次数=14,赢利总值=1919
                亏损次数=3,亏损总值=188
                平盘次数=0
       
    '''
    t = stock.transaction
    i_cofw = stock.i_cofw

    signal = np.zeros(len(t[CLOSE]),int)
    
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    sx = strend(xatr-mxatr)

    dgd = msum(greater(stock.diff,stock.dea),11)

    
    #signal[i_cofw] = infunc(t[CLOSE][i_cofw],5,10,20,stock.atr[i_cofw])    #infunc=uinfunc3b
    #signal[i_cofw] = infunc(t[CLOSE][i_cofw],7,13,30,stock.atr[i_cofw])
    signal[i_cofw] = infunc(t[CLOSE][i_cofw],stock.atr[i_cofw],*lens)
    #signal[i_cofw] = uinfunc4(t[CLOSE][i_cofw],7,13,30,60,stock.atr[i_cofw])

    f60 = gand(strend(stock.ma4)<0)

    gg = gand(stock.g5>stock.g20,stock.g20>stock.g60,stock.g60<stock.g120,stock.g20<8000)

    linelog(stock.code)
    return gand(signal,stock.t5,gg,stock.diff>stock.dea,dgd<11,f60,sx>0)

def uinfunc4(wline,base,len1,len2,len3,len4): #效果奇差
    m1,m2,m3,m4 = ma(wline,len1),ma(wline,len2),ma(wline,len3),ma(wline,len4)
    mmax = gmax(m1,m2,m3,m4)
    mmin = gmin(m1,m2,m3,m4)

    mm2 = gmax(m1,m2)

    ndev = (mmax-mmin) * 1000 / base < 1200

    xcross = gand(cross(mmax,wline),strend(wline)>0)

    return gand(xcross,ndev,strend(m1)>0,mm2>m3)

def uplaind(stock):
    '''
        #2005-200710
        评估:总盈亏值=18679,交易次数=97 期望值=3310
                总盈亏率(1/1000)=18679,平均盈亏率(1/1000)=192,盈利交易率(1/1000)=494
                平均持仓时间=27,持仓效率(1/1000000)=7111
                赢利次数=48,赢利总值=21526
                亏损次数=49,亏损总值=2847
                平盘次数=0
        #2008-201004
        评估:总盈亏值=20815,交易次数=355        期望值=1183
                总盈亏率(1/1000)=20815,平均盈亏率(1/1000)=58,盈利交易率(1/1000)=667
                平均持仓时间=23,持仓效率(1/1000000)=2521
                赢利次数=237,赢利总值=26625
                亏损次数=118,亏损总值=5810
                平盘次数=0
        分布很不均匀。20091026占了2/3
        实际上只有15+的机会
    '''
    t = stock.transaction
    i_cofw = stock.i_cofw

    signal = np.zeros(len(t[CLOSE]),int)
    
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    
    dgd = msum(greater(stock.diff,stock.dea),11)

    

    wline = t[CLOSE][i_cofw]

    base = stock.atr2[i_cofw]

    len1,len2,len3 = 7,13,30

    m1,m2,m3 = ma(wline,len1),ma(wline,len2),ma(wline,len3)
    mmax = gmax(m1,m2,m3)
    mmin = gmin(m1,m2,m3)
    mm12 = gmax(m1,m2)

    w60 = ma(wline,60)

    wdev = gand((wline-w60) * 100 > w60 * 15,(wline-w60) * 100 < w60 * 50)

    ndev = (mmax-mmin)  < base * 2

    xcross = gand(cross(mmax,wline),strend(wline)>0)

    wdiff,wdea = cmacd(wline)

    wdelta = (wline - rollx(wline)) * 10 < rollx(wline)

    signal[i_cofw] = gand(xcross,ndev,strend(m1)>0,strend(wdiff-wdea)>0,wdiff<wdea,wdelta,mm12>=m3,wdev)

    f60 = gor(strend(stock.ma4)<0,stock.ma4<stock.ma5) #与1不同

    ma6 = ma(t[CLOSE],250)
    bndown = bnot(gand(stock.ma5>stock.ma4,ma6>stock.ma5))

    dev10 = gand(t[CLOSE]>stock.ma1,t[CLOSE]>stock.ma2,t[CLOSE]>stock.ma3)

    #gg = gand(stock.g5>stock.g20,stock.g20>stock.g60,stock.g60<stock.g120,stock.g20<8000)

    #gg = gand(stock.g5>stock.g60)

    linelog(stock.code)
    #return gand(signal,stock.t5)#,xatr<mxatr,stock.diff>stock.dea,dgd<11,f60,bndown)
    return gand(signal,stock.t5,bndown,stock.diff>stock.dea,dgd<11,xatr<mxatr,f60,dev10,stock.ref.t5)


def uplaind2(stock,lens=(7,13,30)):
    '''
        ####2008-201004
        评估:总盈亏值=15791,交易次数=212        期望值=1396
                总盈亏率(1/1000)=15791,平均盈亏率(1/1000)=74,盈利交易率(1/1000)=707
                平均持仓时间=27,持仓效率(1/1000000)=2740
                赢利次数=150,赢利总值=19061
                亏损次数=61,亏损总值=3270
                平盘次数=1
        #2005-200710
        评估:总盈亏值=11358,交易次数=33 期望值=6142
                总盈亏率(1/1000)=11358,平均盈亏率(1/1000)=344,盈利交易率(1/1000)=636
                平均持仓时间=34,持仓效率(1/1000000)=10117
                赢利次数=21,赢利总值=12041
                亏损次数=12,亏损总值=683
                平盘次数=0        


        另，去掉strend(diff)>strend(dea)
        评估:总盈亏值=16976,交易次数=231        期望值=1403
                总盈亏率(1/1000)=16976,平均盈亏率(1/1000)=73,盈利交易率(1/1000)=718
                平均持仓时间=27,持仓效率(1/1000000)=2703
                赢利次数=166,赢利总值=20361
                亏损次数=64,亏损总值=3385
                平盘次数=1
        
        评估:总盈亏值=14720,交易次数=42 期望值=5737
                总盈亏率(1/1000)=14720,平均盈亏率(1/1000)=350,盈利交易率(1/1000)=547
                平均持仓时间=33,持仓效率(1/1000000)=10606
                赢利次数=23,赢利总值=15897
                亏损次数=19,亏损总值=1177
                平盘次数=0


    '''
    t = stock.transaction
    i_cofw = stock.i_cofw

    signal = np.zeros(len(t[CLOSE]),int)
    
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    
    wline = t[CLOSE][i_cofw]

    base = stock.atr2[i_cofw]

    #len1,len2,len3 = 7,13,30
    #len1,len2,len3 = 5,10,20
    len1,len2,len3 = lens

    m1,m2,m3 = ma(wline,len1),ma(wline,len2),ma(wline,len3)
    mmax = gmax(m1,m2,m3)
    mmin = gmin(m1,m2,m3)
    mm12 = gmax(m1,m2)

    w60 = ma(wline,60)

    wdev = gand((wline-w60) * 100 > w60 * 15,(wline-w60) * 100 < w60 * 50)

    ndev = (mmax-mmin)  < base * 2

    xcross = gand(cross(mmax,wline),strend(wline)>0)

    wdiff,wdea = cmacd(wline)

    wdelta = (wline - rollx(wline)) * 10 < rollx(wline)

    signal[i_cofw] = gand(xcross,ndev,strend(m1)>0,strend(wdiff-wdea)>0,wdiff<wdea,wdelta,mm12>=m3,wdev)

    #f60 = gor(strend(stock.ma4)<0,stock.ma4<stock.ma5) #与1不同

    ma6 = ma(t[CLOSE],250)
    bndown = bnot(gand(stock.ma5>stock.ma4,ma6>stock.ma5))

    #gg = gand(stock.g5>stock.g20,stock.g20>stock.g60,stock.g60<stock.g120,stock.g20<8000)

    #gg = gand(stock.g5>3000)

    gt = gand(stock.ref.t5)
    st = gand(stock.t1,strend(stock.ma3)>1,strend(stock.ma5)>0,t[CLOSE]>stock.ma1,t[CLOSE]>stock.ma3,stock.ma1>stock.ma2,stock.ma4>stock.ma5,stock.ma5>ma6)

    dgd = msum(greater(stock.diff,stock.dea),11)

    md = gand(stock.diff>stock.dea,dgd<11)#,strend(stock.diff)>strend(stock.dea))

    xr = gand(xatr<mxatr)

    linelog(stock.code)

    #return gand(signal,stock.t5)#,xatr<mxatr,stock.diff>stock.dea,dgd<11,f60,bndown)
    return gand(signal,gt,st,md,xr)


def useller(seller):
    def myseller(stock,sbuy):
        trans= stock.transaction
        return band(seller(stock,sbuy),sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW]))
    return myseller

def xudv(stock):
    t = stock.transaction
    vdea,vdiff = macd_rv(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    vcross = gand(cross(vdea*1.05,vdiff)>0,strend(vdiff)>0)

    xatr = stock.atr * BASE / t[CLOSE]

    signal = gand(vcross,stock.t5,xatr<40,stock.g20>3000,stock.g20<8000,stock.g20>stock.g60)
    linelog(stock.code)
    return signal

def vsum(stock):
    t = stock.transaction
    
    vs1 = msum2(t[AMOUNT],7)/msum2(t[VOLUME],7)
    vs2 = msum2(t[AMOUNT],13)/msum2(t[VOLUME],13)
    vs3 = msum2(t[AMOUNT],30)/msum2(t[VOLUME],30)    
    vs4 = msum2(t[AMOUNT],60)/msum2(t[VOLUME],60)

    svs = gand(cross(vs4,vs1)>0,strend(vs1)>0)

    signal = gand(svs)
    linelog(stock.code)
    return signal

def sagd(stock):
    t = stock.transaction
    
    sx = derepeatc(gand(stock.above,stock.ma1>stock.ma2))
    
    f60 = greater(stock.ma4 * 101/100,t[LOW])

    sxx = sfollow(f60,sx,10)

    s13_30 = gand(t[LOW]>stock.ma3,t[LOW]<stock.ma2)

    ss = sfollow(sxx,s13_30,5)

    tss = gand(ss,stock.ma2>stock.ma3,stock.t4,stock.t3,stock.t2)  #7-13顺序未改
    
    

    linelog(stock.code)

    xatr = stock.atr * BASE / t[CLOSE]

    signal = gand(tss,stock.g20>8500)

    return signal


def nhighxt(stock,m=60,n=10):#m日新高后回踩n日线,踩上后次日买入
    '''     60,10
            2008-201004
            t3&t5 + g20>5000,g5<g20,ma1>ma2,stock.above,lesser(t[VOLUME],rollx(t[VOLUME]))
                +vma_s < vma_l
                评估:总盈亏值=11257,交易次数=96 期望值=1625
                总盈亏率(1/1000)=11257,平均盈亏率(1/1000)=117,盈利交易率(1/1000)=614
                平均持仓时间=32,持仓效率(1/1000000)=3656
                赢利次数=59,赢利总值=13941
                亏损次数=37,亏损总值=2684
                平盘次数=0

            需要避开前期危险性板块，还能进一步提高收益率. 如1002以后的地产等

            2005-200710
            评估:总盈亏值=5953,交易次数=116 期望值=401
                总盈亏率(1/1000)=5953,平均盈亏率(1/1000)=51,盈利交易率(1/1000)=405
                平均持仓时间=22,持仓效率(1/1000000)=2318
                赢利次数=47,赢利总值=14645
                亏损次数=68,亏损总值=8692
                平盘次数=1

            2001-200506 不稳定
            评估:总盈亏值=-725,交易次数=9   期望值=-699
                总盈亏率(1/1000)=-725,平均盈亏率(1/1000)=-81,盈利交易率(1/1000)=111
                平均持仓时间=21,持仓效率(1/1000000)=-3858
                赢利次数=1,赢利总值=203
                亏损次数=8,亏损总值=928
                平盘次数=0
            

            60,13
            评估:总盈亏值=6928,交易次数=85  期望值=1125
                总盈亏率(1/1000)=6928,平均盈亏率(1/1000)=81,盈利交易率(1/1000)=517
                平均持仓时间=29,持仓效率(1/1000000)=2793
                赢利次数=44,赢利总值=9887
                亏损次数=41,亏损总值=2959
                平盘次数=0
            

            120,10
            评估:总盈亏值=20617,交易次数=214        期望值=1246
                总盈亏率(1/1000)=20617,平均盈亏率(1/1000)=96,盈利交易率(1/1000)=570
                平均持仓时间=32,持仓效率(1/1000000)=3000
                赢利次数=122,赢利总值=27701
                亏损次数=92,亏损总值=7084
                平盘次数=0
    
            250,10
            评估:总盈亏值=3345,交易次数=88  期望值=475
                总盈亏率(1/1000)=3345,平均盈亏率(1/1000)=38,盈利交易率(1/1000)=465
                平均持仓时间=24,持仓效率(1/1000000)=1583
                赢利次数=41,赢利总值=7151
                亏损次数=47,亏损总值=3806
                平盘次数=0
            
    '''
    t = stock.transaction
    mline = rollx(tmax(t[HIGH],m))
    dcross = cross(mline,t[HIGH])>0    
    linelog(stock.code)
    
    mam = ma(t[CLOSE],n)
    xcross = cross(mam,t[LOW])<0
 
    xcross = decover1(xcross,3)

    nxt = sfollow(dcross,xcross,5)

    ma1 = ma(t[CLOSE],5)
    ma2 = ma(t[CLOSE],10)

    st = gand(ma1>ma2,stock.above,lesser(t[VOLUME],rollx(t[VOLUME])))

    gt = gand(stock.ref.t5,stock.ref.t3)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr<mxatr,strend(xatr-mxatr)>0,xatr>40)

    md = gand(stock.diff>stock.dea)

    gg = gand(stock.g20>5000,stock.g5<stock.g20)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vt = vma_s < vma_l

    #如何判断首次?

    return gand(nxt,xr,gt,gg,st,vt)


def nhighxt2(stock,m=60,n=10):#m日新高后回踩n日线
    '''
        2008-201004
        评估:总盈亏值=5156,交易次数=45  期望值=1781
                总盈亏率(1/1000)=5156,平均盈亏率(1/1000)=114,盈利交易率(1/1000)=733
                平均持仓时间=35,持仓效率(1/1000000)=3257
                赢利次数=33,赢利总值=5927
                亏损次数=12,亏损总值=771
                平盘次数=0
        2005-200710
        评估:总盈亏值=14416,交易次数=62 期望值=2109
                总盈亏率(1/1000)=14416,平均盈亏率(1/1000)=232,盈利交易率(1/1000)=387
                平均持仓时间=33,持仓效率(1/1000000)=7030
                赢利次数=24,赢利总值=18614
                亏损次数=38,亏损总值=4198
                平盘次数=0
        
        n=13
        2008-201004
        评估:总盈亏值=5653,交易次数=25  期望值=3645
                总盈亏率(1/1000)=5653,平均盈亏率(1/1000)=226,盈利交易率(1/1000)=800
                平均持仓时间=43,持仓效率(1/1000000)=5255
                赢利次数=20,赢利总值=5964
                亏损次数=5,亏损总值=311
                平盘次数=0
        2005-200710
        评估:总盈亏值=1712,交易次数=20  期望值=702
                总盈亏率(1/1000)=1712,平均盈亏率(1/1000)=85,盈利交易率(1/1000)=400
                平均持仓时间=29,持仓效率(1/1000000)=2931
                赢利次数=8,赢利总值=3172
                亏损次数=12,亏损总值=1460
                平盘次数=0
        
        n=20
        2008-201004
        评估:总盈亏值=813,交易次数=5    期望值=1396
                总盈亏率(1/1000)=813,平均盈亏率(1/1000)=162,盈利交易率(1/1000)=600
                平均持仓时间=47,持仓效率(1/1000000)=3446
                赢利次数=3,赢利总值=1045
                亏损次数=2,亏损总值=232
                平盘次数=0
        
        2005-200710
        评估:总盈亏值=158,交易次数=7    期望值=170
                总盈亏率(1/1000)=158,平均盈亏率(1/1000)=22,盈利交易率(1/1000)=428
                平均持仓时间=31,持仓效率(1/1000000)=709
                赢利次数=3,赢利总值=676
                亏损次数=4,亏损总值=518
                平盘次数=0
        

        n=30
        2008-201004
        评估:总盈亏值=-93,交易次数=1    期望值=-1000
                总盈亏率(1/1000)=-93,平均盈亏率(1/1000)=-93,盈利交易率(1/1000)=0

                平均持仓时间=16,持仓效率(1/1000000)=-5813
                赢利次数=0,赢利总值=0
                亏损次数=1,亏损总值=93
                平盘次数=0
        
        2005-200710
        评估:总盈亏值=136,交易次数=3    期望值=401
                总盈亏率(1/1000)=136,平均盈亏率(1/1000)=45,盈利交易率(1/1000)=333
                平均持仓时间=26,持仓效率(1/1000000)=1730
                赢利次数=1,赢利总值=361
                亏损次数=2,亏损总值=225
                平盘次数=0


    '''
    t = stock.transaction

    mline = rollx(tmax(t[HIGH],m))
    dcross = cross(mline,t[HIGH])>0    
    linelog(stock.code)
    
    mam = ma(t[CLOSE],n)
    xcross = cross(mam,t[LOW])<0
 
    xcross = decover1(xcross,3)

    nxt = sfollow(dcross,xcross,5)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr>mxatr,xatr>40)

    #ref_cross = cross(stock.ref.

    #rmd = bnot(gand(stock.ref.diff<stock.ref.dea,strend(stock.ref.diff-stock.ref.dea)<0))

    md = gand(stock.diff>stock.dea,strend(stock.dea)>0)

    gg = gand(stock.g20>8500,stock.g5>8500)

    vma_s = ma(t[VOLUME],7)
    vma_l = ma(t[VOLUME],13)
    vmx = gmax(vma_s,vma_l)
    vmn = gmin(vma_s,vma_l)

    rt = gor(stock.ref.t1,stock.ref.t2,stock.ref.t3)

    st = gand(stock.t3,stock.t5,stock.ma2>stock.ma3,stock.ma3>stock.ma4,bnot(gand(greater(t[VOLUME],rollx(t[VOLUME])),t[CLOSE]<t[OPEN])),t[VOLUME]<vmx,t[VOLUME]>0)

    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    #如何判断首次?

    return gand(nxt,xr,gg,rt,st,md,mcf<750)


def oneup(stock,lens=(7,13)):
    '''
        评估:总盈亏值=1576,交易次数=20  期望值=7090
                总盈亏率(1/1000)=1576,平均盈亏率(1/1000)=78,盈利交易率(1/1000)=700
                平均持仓时间=21,持仓效率(1/1000000)=3714
                赢利次数=14,赢利总值=1646
                亏损次数=6,亏损总值=70
                平盘次数=0
    '''
    linelog(stock.code)

    t = stock.transaction

    if stock.zgb >= 300000 or stock.ag >=200000:
        return cached_zeros(len(t[CLOSE]))

    short,long = lens
    if short == 7:
        ma1 = stock.ma1
    else:
        ma1 = ma(t[CLOSE],short)
    if long == 13:
        ma2 = stock.ma2
    else:
        ma2 = ma(t[CLOSE],long)
    
    mmax = gmax(ma1,ma2)
    mmin = gmin(ma1,ma2)

    up = gand(greater(t[CLOSE],mmax),lesser(t[OPEN],mmin))

    xabove = greater(msum(stock.above,7),6) #理顺已经一段时间

    xdev = greater(stock.ma4,t[CLOSE]*24/25)

    #上下影线都不大于实体，同时实体大于1%
    st = gand(stock.ma2,xabove,xdev,t[HIGH]-t[CLOSE]<t[CLOSE]-t[OPEN],t[OPEN]-t[LOW]<t[CLOSE]-t[OPEN],t[CLOSE]-t[OPEN]>t[OPEN]/100)

    gt = gand(stock.ref.t3,stock.ref.t5)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr<mxatr,mxatr<40,xatr<40)

    gg = gand(stock.g20>3000,stock.g60>3000,stock.g5>5000)

    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    signal = gand(up,st,gt,xr,gg,mcf<750)

    return signal

def xud2(stock,xfunc=xc0s,astart=45):
    ''' 
    '''
    t = stock.transaction
    mxc = xfunc(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=13) > 0

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<vma*2/3)
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    stdea = strend(stock.dea)
    stdiff = strend(stock.diff)
    st = gand(stdea<=-3,stdea>=-4,stdiff<=-5,stdiff>=-6)

    xatr = stock.atr * BASE / t[CLOSE]     

    signal = gand(mxc,vfilter,stock.thumb,stock.above,stock.t5,mcf>1000,stock.ma1<stock.ma2,stock.ma1>stock.ma3,st,xatr>=astart)
    linelog(stock.code)
    return signal

def xud3(stock,xfunc=xc0s,astart=45):
    '''
        #2008-201004
        评估:总盈亏值=38089,交易次数=128        期望值=4125
                总盈亏率(1/1000)=38089,平均盈亏率(1/1000)=297,盈利交易率(1/1000)=937
                平均持仓时间=52,持仓效率(1/1000000)=5711
                赢利次数=120,赢利总值=38669
                亏损次数=8,亏损总值=580
    
        #2005-200712
        评估:总盈亏值=39468,交易次数=101        期望值=4756
                总盈亏率(1/1000)=39468,平均盈亏率(1/1000)=390,盈利交易率(1/1000)=643
                平均持仓时间=44,持仓效率(1/1000000)=8863
                赢利次数=65,赢利总值=42447
                亏损次数=36,亏损总值=2979
                平盘次数=0
    
    '''
    t = stock.transaction
    mxc = xfunc(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=10) > 0

    s=stock
    thumb = gand(s.g20>=3000,s.g20<=8000,s.g20>s.g60,s.g5>s.g60)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr>=mxatr,mxatr>=astart)

    mst = gand(stock.above,stock.t5,stock.ma1<stock.ma2,stock.ma1>stock.ma3)

    gt = gand(stock.ref.t3)

    st2 = gand(strend(stock.dea)>=strend(stock.diff))

    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0,strend(stock.ref.ma2)>0)

    signal = gand(mxc,thumb,mst,xr,gt,st2,xfilter)
    linelog(stock.code)
    return signal


def emv2x(stock,fast,slow):
    t = stock.transaction
    #2872-34-676-247-9880,1000-1-1000-75-3750

    em = emv(t[HIGH],t[LOW],t[VOLUME])
   
    mv1 = ma(em,fast)
    mv2 = ma(em,slow)

    vma = ma(t[VOLUME],10)

    vfilter = bnot(gand(t[CLOSE]<t[OPEN],t[VOLUME]>vma*2))
 
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr>=mxatr,mxatr>=60)

    gt = gand(stock.ref.t3)

    s=stock
    thumb = gand(s.g20>=3000,s.g20<=8000,s.g20>s.g60,s.g5>s.g60)

    mst = gand(stock.above,stock.t5)

    ecross = gand(cross(mv2,mv1)>0,strend(mv1)>0,mst,gt,xr,vfilter)
    linelog(stock.code)
    return ecross


def tsvama2sbv(stock,fast,slow,follow=7):
    ''' svama慢线下叉快线，follow日后再上叉回来
        添加vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2

    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast)
    trend_ma_svapslow = strend(ma_svapslow)

    cross_down = band(cross(ma_svapslow,ma_svapfast)<0,trend_ma_svapfast<0)    
    cross_up = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast>0)        
    
    sdown = transform(cross_down,v2i,len(t[VOLUME]))
    sup = transform(cross_up,v2i,len(t[VOLUME]))    
    
    sync_down_up = sfollow(sdown,sup,follow)
    
    linelog('%s:%s' % (tsvama2sbv.__name__,stock.code))

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr<mxatr,xatr<40)

    md = gand(stock.diff>stock.dea,strend(stock.dea)>0)

    gg = gand(stock.g20>8500,stock.g5>8500,stock.g60>8500)

    vma_s = ma(t[VOLUME],7)
    vma_l = ma(t[VOLUME],13)
    vmx = gmax(vma_s,vma_l)
    vmn = gmin(vma_s,vma_l)

    rt = gor(stock.ref.t1,stock.ref.t2,stock.ref.t3)

    st = gand(stock.t3,stock.t5,stock.ma2>stock.ma3,stock.ma3>stock.ma4,bnot(gand(greater(t[VOLUME],rollx(t[VOLUME])),t[CLOSE]<t[OPEN])),t[VOLUME]<vmx,t[VOLUME]>0)

    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    lmax = tmax(t[HIGH],30)
    lmin = tmin(t[HIGH],30)
    ext = lmax < lmin*3/2

    return gand(sync_down_up,md,ext)

def tsvama2n(stock,fast=3,slow=33):
    ''' svama两线交叉
        3,33
        评估:总盈亏值=7730,交易次数=60  期望值=1882
                总盈亏率(1/1000)=7730,平均盈亏率(1/1000)=128,盈利交易率(1/1000)=683
                平均持仓时间=38,持仓效率(1/1000000)=3368
                赢利次数=41,赢利总值=9038
                亏损次数=19,亏损总值=1308
                平盘次数=0
        2005-200710    
        评估:总盈亏值=5277,交易次数=63  期望值=932
                总盈亏率(1/1000)=5277,平均盈亏率(1/1000)=83,盈利交易率(1/1000)=539
                平均持仓时间=24,持仓效率(1/1000000)=3458
                赢利次数=34,赢利总值=7882
                亏损次数=29,亏损总值=2605
        15,75
        评估:总盈亏值=5460,交易次数=35  期望值=2260
                总盈亏率(1/1000)=5460,平均盈亏率(1/1000)=156,盈利交易率(1/1000)=800
                平均持仓时间=39,持仓效率(1/1000000)=4000
                赢利次数=28,赢利总值=5949
                亏损次数=7,亏损总值=489
                平盘次数=0
        

        2005-200710
        评估:总盈亏值=17073,交易次数=73 期望值=2505
                总盈亏率(1/1000)=17073,平均盈亏率(1/1000)=233,盈利交易率(1/1000)=575
                平均持仓时间=35,持仓效率(1/1000000)=6657
                赢利次数=42,赢利总值=19968
                亏损次数=31,亏损总值=2895
                平盘次数=0

    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    
    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)
    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr<mxatr)

    vma_s = ma(t[VOLUME],7)
    vma_l = ma(t[VOLUME],30)

    rt = gor(stock.ref.t1,stock.ref.t2,stock.ref.t3,stock.ref.t4,strend(stock.ref.diff-stock.ref.dea)>2)

    hsl = t[VOLUME]*1000/stock.ag

    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    md = gand(strend(stock.diff-stock.dea)>1)

    #signal = gand(gor(sfollow(msvap,stock.hup,5),sfollow(stock.hup,msvap,5)),stock.xup)

    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0,strend(stock.ref.ma2)>0)


    return gand(msvap,stock.magic,stock.above,xr,rt,hsl<10000,vma_s<vma_l,mcf<900,xfilter)


def tsvama3(stock,fast,mid,slow,follow=7):
    ''' svama三线交叉
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67_2

    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,follow)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,follow)
    
    msvap = transform(sync3,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama3.__name__,stock.code))

    #thumb = gand(stock.g5>stock.g60,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250,stock.g20<8000)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr<mxatr,xatr<50)

    rt = gor(stock.ref.t1,stock.ref.t2,stock.ref.t3,stock.ref.t4,strend(stock.ref.diff-stock.ref.dea)>2)

    hsl = t[VOLUME]*1000/stock.ag

    md = gand(strend(stock.diff-stock.dea)>1)

    st = gand(stock.t3,stock.t5)

    return gand(msvap,xr,rt,md,hsl<8000,st,gg)


def ldxx(stock,mlen=60): #low down xcross 
    ''' 
        2008-201004
        评估:总盈亏值=27462,交易次数=224        期望值=1876
                总盈亏率(1/1000)=27462,平均盈亏率(1/1000)=122,盈利交易率(1/1000)=732
                平均持仓时间=36,持仓效率(1/1000000)=3388
                赢利次数=164,赢利总值=31385
                亏损次数=60,亏损总值=3923
                平盘次数=0
        
        2005-200710
        评估:总盈亏值=33155,交易次数=362        期望值=957
                总盈亏率(1/1000)=33155,平均盈亏率(1/1000)=91,盈利交易率(1/1000)=397
                平均持仓时间=24,持仓效率(1/1000000)=3791
                赢利次数=144,赢利总值=53906
                亏损次数=218,亏损总值=20751
                平盘次数=0
    
    '''
    linelog('%s:%s' % (tsvama3.__name__,stock.code))
    t = stock.transaction
    
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s,t[VOLUME]>0,t[VOLUME]<rollx(t[VOLUME]))

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    #xr = gand(xatr>mxatr,mxatr>60)
    xr = gand(xatr>30,strend(xatr-mxatr)<0)

    ma6 = ma(t[CLOSE],250)

    rt = gand(stock.ref.t1,stock.ref.t3,gor(stock.ref.t4,stock.ref.t5,strend(ma6)>0))

    hsl = t[VOLUME]*1000/stock.ag

    gg = gand(stock.g5<5000,stock.g20<5000)

    xfilter = gor(stock.ref.mfilter,stock.ref.ma1>stock.ref.ma2,stock.ref.ma2>stock.ref.ma3,strend(stock.ref.ma1)>0,strend(stock.ref.ma3)>0,strend(stock.ref.ma2)>0)

    signal = gand(x2,hsl<2500,gg,rt,xr,xfilter)

    return signal


def rebeat(stock):
    ''' 
        超跌
    '''
    linelog('%s:%s' % (rebeat.__name__,stock.code))    
    t = stock.transaction
    
    gaps = msum2(t[HIGH]<rollx(t[LOW]),30)  #x天内的下行缺口数

    ldown = t[CLOSE] * 1000 / tmax(t[HIGH],60) #y天内的价格幅度
    sdown = t[CLOSE] * 1000 / tmax(t[HIGH],7) #z天内的价格幅度

    signal = gand(gaps>3,ldown<600,sdown<800,stock.ref.t1>0)   #715=1000/(1+0.4),870=1000(1+.15)

    dc = gand(cross(stock.dea,stock.diff)>0,strend(stock.diff)>0)

    signal = sfollow(signal,dc,7)
    return signal

def rebeat2(stock):
    ''' 
        超跌反弹
    '''
    linelog('%s:%s' % (rebeat2.__name__,stock.code))    
    t = stock.transaction
    
    gaps = msum2(t[HIGH]<rollx(t[LOW]),30)  #x天内的下行缺口数

    ldown = tmin(t[CLOSE],30) * 1000 / tmax(t[CLOSE],30) #y天内的价格幅度
    sdown = tmin(t[CLOSE],7) * 1000 / tmax(t[CLOSE],7) #z天内的价格幅度
    sup = t[CLOSE] * 1000 / tmin(t[CLOSE],7)
    
    signal = gand(gaps>3,ldown<600,sup>1080)   #715=1000/(1+0.4),870=1000(1+.15)

    return signal

def rebeat3(stock):
    ''' 
        超跌>大盘跌幅
    '''
    linelog('%s:%s' % (rebeat.__name__,stock.code))    
    t = stock.transaction
    
    if 'ldown' not in stock.ref.__dict__:
        stock.ref.ldown = stock.ref.transaction[CLOSE] * 1000 / tmax(stock.ref.transaction[HIGH],30)
        stock.ref.sdown = stock.ref.transaction[CLOSE] * 1000 / tmax(stock.ref.transaction[HIGH],17)

    ldown = t[CLOSE] * 1000 / tmax(t[HIGH],30) #y天内的价格幅度
    sdown = t[CLOSE] * 1000 / tmax(t[HIGH],7) #z天内的价格幅度

    rl = ldown - stock.ref.ldown
    rs = sdown - stock.ref.sdown

    signal = gand(ldown<715,sdown<850,rl<-150,rs<-100)   #715=1000/(1+0.4),870=1000(1+.15)

    return signal


def xrebeat(stock,drop_range=300,covered=120):
    ''' 
        超跌drop_range以上的小时线反弹
        1. covered日内跌幅超过drop_range
        2. covered*2 日内跌幅不超过 drop_range * 1.2. 就是说不是二次超跌
    '''

    linelog('%s:%s' % (xrebeat.__name__,stock.code))    
    t = stock.transaction

    lmax = tmax(t[HIGH],covered)
    lmax2 = tmax(t[HIGH],covered * 2)

    line = lmax * (1000-drop_range) / 1000
    line2 = lmax2 * (1000-drop_range*1.2) /1000

    dcross = gand(cross(line,t[CLOSE])<0,t[CLOSE]>line2)

    ssignal = sfollow(dcross,stock.hup_t,7)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    #xr = gand(xatr>mxatr,mxatr>60)
    #xr = gand(xatr<mxatr,xatr<30)

    signal = gand(ssignal,stock.g20<2000)

    return signal

def pmacdh(stock):
    linelog('%s:%s' % (pmacdh.__name__,stock.code))
    t = stock.transaction

    #ssignal = gand(stock.hup_t,stock.diff>stock.dea,strend(stock.diff-stock.dea)>0)

    ssignal = sfollow(cross(stock.dea,stock.diff)>0,stock.hup_t,7)

    bdown = gand(stock.ma1<stock.ma2,stock.ma2<stock.ma3,stock.ma3<stock.ma4,stock.t3<1,stock.t4<1)

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xr = gand(xatr<mxatr,xatr<30)

    signal = gand(ssignal,bnot(bdown),stock.golden,xr)

    return signal

def pmacd2(stock):
    '''
        评估:总盈亏值=32018,交易次数=227        期望值=1855
                总盈亏率(1/1000)=32018,平均盈亏率(1/1000)=141,盈利交易率(1/1000)=700
                平均持仓时间=32,持仓效率(1/1000000)=4406
                赢利次数=159,赢利总值=37191
                亏损次数=68,亏损总值=5173
                平盘次数=0

        2005-200710
        评估:总盈亏值=2146,交易次数=72  期望值=292
                总盈亏率(1/1000)=2146,平均盈亏率(1/1000)=29,盈利交易率(1/1000)=347
                平均持仓时间=22,持仓效率(1/1000000)=1318
                赢利次数=25,赢利总值=6805
                亏损次数=47,亏损总值=4659
                平盘次数=0
        

    '''
    t = stock.transaction
    pdiff,pdea = stock.diff,stock.dea

    adiff = ma(np.abs(pdiff),30)

    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,pdiff<adiff*1/2,pdiff>-adiff*1/2)
    linelog(stock.code)
    #return gand(dcross,stock.golden,stock.above,cs,pdea>0,pdea<12000)
    ssignal = dcross

    up2 = gand(greater(t[CLOSE],rollx(t[CLOSE])*1015/1000),lesser(t[CLOSE],rollx(t[CLOSE])*1033/1000))

    gfilter = gand(stock.ref.mfilter)

    sfilter = gand(gor(stock.t1,stock.t2,stock.t3))

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xfilter = gand(xatr<mxatr,xatr>40,xatr<60)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 1/2,vma_s < vma_l)

    zfilter = gand(stock.ma1 > stock.ma2,t[CLOSE]>stock.ma1,t[CLOSE]>stock.ma3,t[CLOSE]>stock.ma4,stock.g20<5000,stock.g20>1000)


    signal = gand(ssignal,up2,gfilter,sfilter,xfilter,vfilter,zfilter)

    return gand(signal)


def b102(stock,covered=60):
    '''
        10元以下股票，创新高后，第一次退回到2个整数关
        快速出击品种，上涨超过8%之后必须出掉1半，超过12%再出2/3
            macd小时线破掉必须全出, 上碰到30均线也必须全出
        结合15分钟走势买入更佳，最好情况是选出时15分钟正在下行，然后上叉时(必须>0.00，而不是0.00,防止夭折情况)买入。
                如果正在上行，等待下一次上叉(时间不能超过3个交易日),或者放过
                同时，延后2个周期，且买入点小于理论买入点的也可以买入(15分钟仍在向上发展)
            出局点在15分钟下叉(-0.00也算),此时如果日线macd走坏，则全出;否则出半-2/3,小时线走坏时出2/3

        可以合理的去掉ST股，因为ST股的快速下跌可能有内在原因,以及在群跌时存在当日或几日跌不透(因5%限制)，而拉长下跌期的情况。

        多选1时，选择XATR大的，打于8.0最好。g20小的。

        08-1004
        评估:总盈亏值=107432,交易次数=578       期望值=1989
                总盈亏率(1/1000)=107432,平均盈亏率(1/1000)=185,盈利交易率(1/1000)=740
                平均持仓时间=39,持仓效率(1/1000000)=4743
                赢利次数=428,赢利总值=121215
                亏损次数=147,亏损总值=13783
                平盘次数=3

        g20<3000
        评估:总盈亏值=54575,交易次数=261        期望值=2271
                总盈亏率(1/1000)=54575,平均盈亏率(1/1000)=209,盈利交易率(1/1000)=754
                平均持仓时间=40,持仓效率(1/1000000)=5225
                赢利次数=197,赢利总值=60206
                亏损次数=61,亏损总值=5631
                平盘次数=3



        05-0710
        评估:总盈亏值=26807,交易次数=401        期望值=605
                总盈亏率(1/1000)=26807,平均盈亏率(1/1000)=66,盈利交易率(1/1000)=473
                平均持仓时间=27,持仓效率(1/1000000)=2444
                赢利次数=190,赢利总值=49861
                亏损次数=210,亏损总值=23054
                平盘次数=1

        g20<30
        评估:总盈亏值=11222,交易次数=265        期望值=388
                总盈亏率(1/1000)=11222,平均盈亏率(1/1000)=42,盈利交易率(1/1000)=452
                平均持仓时间=28,持仓效率(1/1000000)=1500
                赢利次数=120,赢利总值=26900
                亏损次数=144,亏损总值=15678
                平盘次数=1


    '''
    linelog('%s:%s' % (b102.__name__,stock.code))
    t = stock.transaction

    nh = tmax(t[HIGH],covered)

    #nhl = (nh*97/100 / 1000 - 1) * 1000    #此为第二个整数关，第一个整数关是抹平位. 小于3%的出头也算前一关
    nhl = (nh/ 1000 - 1) * 1000    #此为第二个整数关，第一个整数关是抹平位.

    #nsignal = gand(t[LOW] < nhl,t[HIGH]>nhl)    #跌入

    nsignal = gand(cross(nhl,t[CLOSE])<0)

    inh = equals(nh,t[HIGH])

    times = rsum(rsum(nsignal,inh),inh) #第一次rsum,结果是第一次触碰和第二次触碰之间都是1,第二次rsum，只有第一次触碰是1

    ssignal = gand(equals(times,1),t[CLOSE]<8000)    #第一次碰到这个整数关,且新高时价位小于10

    #前面没有超过8%的小反弹
    bouce = gand(t[HIGH] > rollx(tmin(t[LOW],3)) * 108/100)
    nfilter = msum(bouce,3) < 1

    sfilter = gand(gor(stock.t1,stock.t2,stock.t3))

    xatr = stock.atr * BASE / t[CLOSE]
    mxatr = ma(xatr,13)
    xfilter = gand(xatr>mxatr,xatr>60)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s < vma_l * 3/2,vma_s > vma_l / 2)


    #所谓背离，是指价格新高头部形成时，macd没有创相应周期的新高

    xdev = devi(t[HIGH],stock.diff)
    dfilter = bnot(repeat(xdev,30))

    gfilter = gand(stock.g20<6000)

    #signal = gand(ssignal,sfilter,xfilter,vfilter)#,nfilter)#,gfilter)#,dfilter)
    signal = gand(ssignal,xfilter,vfilter,gfilter)  #这个搭配的区分度不会群蔽，在时间分布上比较均匀

    return signal


def b2(stock,covered=60):
    '''
      退回高点20%舍入后的整数位  

      快速出击品种，b102的扩展版本，效果上不如b102

        快速出击品种，上涨超过8%之后必须出掉1半，超过12%再出2/3
            macd小时线破掉必须全出, 上碰到30均线也必须全出
        结合15分钟走势买入更佳，最好情况是选出时15分钟正在下行，然后上叉时(必须>0.00，而不是0.00,防止夭折情况)买入。
                如果正在上行，等待下一次上叉(时间不能超过3个交易日),或者放过
                同时，延后不超过4个周期，且买入点小于理论买入点的也可以买入(15分钟仍在向上发展)
            出局点在15分钟下叉(-0.00也算),此时如果日线macd走坏，则全出;否则出半-2/3,小时线走坏时出2/3

        可以合理的去掉ST股，因为ST股的快速下跌可能有内在原因
        
        多选1时，选择XATR大的，打于8.0最好。g20小的。

        08-1004
        评估:总盈亏值=80255,交易次数=664        期望值=937
                总盈亏率(1/1000)=80255,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=608
                平均持仓时间=34,持仓效率(1/1000000)=3529
                赢利次数=404,赢利总值=113201
                亏损次数=257,亏损总值=32946
                平盘次数=3
 
        gfilter = gand(stock.g20<6000)
        评估:总盈亏值=44446,交易次数=223        期望值=1745
                总盈亏率(1/1000)=44446,平均盈亏率(1/1000)=199,盈利交易率(1/1000)=753
                平均持仓时间=41,持仓效率(1/1000000)=4853
                赢利次数=168,赢利总值=50717
                亏损次数=55,亏损总值=6271
                平盘次数=0
        

        05-0710 #因为除权因素的存在，所以在价位上的判断失准
        评估:总盈亏值=5902,交易次数=575 期望值=81
                总盈亏率(1/1000)=5902,平均盈亏率(1/1000)=10,盈利交易率(1/1000)=377
                平均持仓时间=22,持仓效率(1/1000000)=454
                赢利次数=217,赢利总值=49615
                亏损次数=356,亏损总值=43713
                平盘次数=2


        gfilter = gand(stock.g20<6000)
        评估:总盈亏值=-699,交易次数=263 期望值=-23
                总盈亏率(1/1000)=-699,平均盈亏率(1/1000)=-3,盈利交易率(1/1000)=349
                平均持仓时间=20,持仓效率(1/1000000)=-150
                赢利次数=92,赢利总值=21932
                亏损次数=170,亏损总值=22631
                平盘次数=1


        05-0710 (xatr>60)
        评估:总盈亏值=13958,交易次数=694        期望值=166
                总盈亏率(1/1000)=13958,平均盈亏率(1/1000)=20,盈利交易率(1/1000)=380
                平均持仓时间=22,持仓效率(1/1000000)=909
                赢利次数=264,赢利总值=65548
                亏损次数=427,亏损总值=51590
                平盘次数=3

        gfilter = gand(stock.g20<6000)
        评估:总盈亏值=603,交易次数=318  期望值=7
                总盈亏率(1/1000)=603,平均盈亏率(1/1000)=1,盈利交易率(1/1000)=358
                平均持仓时间=20,持仓效率(1/1000000)=50
                赢利次数=114,赢利总值=26820
                亏损次数=202,亏损总值=26217
                平盘次数=2


    '''
    linelog('%s:%s' % (b2.__name__,stock.code))
    t = stock.transaction

    nh = tmax(t[HIGH],covered)

    nhl = (nh* 80/100)/1000 * 1000    #下20%之后的整数关,先抹掉尾数，八成后再抹平

    #nsignal = gand(t[LOW] < nhl,t[HIGH]>nhl)    #跌入

    nsignal = gand(cross(nhl,t[LOW])<0)

    inh = equals(nh,t[HIGH])

    times = rsum(rsum(nsignal,inh),inh) #第一次rsum,结果是第一次触碰和第二次触碰之间都是1,第二次rsum，只有第一次触碰是1

    ssignal = gand(equals(times,1))    #第一次碰到这个整数关,且新高时价位小于10

    sfilter = gand(gor(stock.t1,stock.t2,stock.t3))

    xatr = stock.atr * BASE / t[LOW]
    mxatr = ma(xatr,13)
    xfilter = gand(xatr>mxatr,xatr>75)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l,vma_s<vma_l*2)


    #所谓背离，是指价格新高头部形成时，macd没有创相应周期的新高

    xdev = devi(t[HIGH],stock.diff)
    dfilter = bnot(repeat(xdev,30))

    gfilter = gand(stock.g20<6000)

    signal = gand(ssignal,sfilter,xfilter,vfilter)#,gfilter)

    return signal


