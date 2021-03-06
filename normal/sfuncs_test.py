# -*- coding: utf-8 -*-

import unittest

from random import randint
import numpy as np

from wolfox.fengine.core.base import BaseObject
from wolfox.fengine.normal.sfuncs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.funcs_test')

class ModuleTest(unittest.TestCase):    #通路测试
    def setUp(self):
        #prepare data
        sopen = sclose = svolume = shigh = slow = savg = samount = np.array([randint(10000,15000) for i in range(2000)])
        shour = np.array([randint(10000,15000) for i in range(8000)])
        trans = [sopen,sclose,svolume,shigh,savg,samount,svolume]
        vi = np.array([i for i in range(2000)])
        g = np.array([randint(0,10000) for i in range(2000)])
        s = BaseObject(code='SH50TEST',zgb=10000000,ag=4000,transaction=trans,
                atr=g,atr2=g,silver=g,g5=g,g20=g,g60=g,g120=g,g250=g,diff=g,dea=g,
                mfilter = g,
                ma0=g,ma1=g,ma2=g,ma3=g,ma4=g,ma5=g,t5=g,t4=g,t3=g,t2=g,t1=g,t0=g,above=g,golden=g,thumb=g,magic=g,
                hour=shour,hmxc=g,xru3=g,xru=g,ma4_up=g,hup=g,hdown=g,hdev=g,mup_100=g,
                svap_ma_67=(g,vi),svap_ma_67_2=(g,vi),
                i_cofw = np.arange(0,2000,5)
                )
        s.ref = s   #指向自己
        s.catalog = {s:g}
        s.c60 = {s:g}
        self.stock = s

    def test_x30(self):
        ss = x30(self.stock.transaction)
        self.assertTrue(True)

    def test_tsvama2(self):
        sbuy = tsvama2(self.stock,5,20)
        self.assertTrue(True)
    
    def test_tsvama2_old(self):
        sbuy = tsvama2_old(self.stock,5,20)
        self.assertTrue(True)

    def test_tsvama2a(self):
        sbuy = tsvama2a(self.stock,5,20)
        self.assertTrue(True)

    def test_tsvama2b(self):
        sbuy = tsvama2b(self.stock,5,20)
        self.assertTrue(True)

    def test_tsvama2x(self):
        sbuy = tsvama2x(self.stock,5,20)
        self.assertTrue(True)

    def test_pmacd(self):
        sbuy = pmacd(self.stock)
        self.assertTrue(True)

    def test_nhigh(self):
        sbuy = nhigh(self.stock)
        self.assertTrue(True)
    
    def test_xma60(self):
        sbuy = xma60(self.stock)
        self.assertTrue(True)

    def test_wvad(self):
        sbuy = wvad(self.stock)
        self.assertTrue(True)

    def test_temv(self):
        sbuy = temv(self.stock)
        self.assertTrue(True)

    def test_vmacd_ma4(self):
        sbuy = vmacd_ma4(self.stock)
        self.assertTrue(True)

    def test_ma4(self):
        sbuy = ma4(self.stock)
        self.assertTrue(True)

    def test_vmacd(self):
        sbuy = vmacd(self.stock)
        self.assertTrue(True)

    def test_gx60(self):
        sbuy = gx60(self.stock)
        self.assertTrue(True)
    
    def test_gx250(self):
        sbuy = gx250(self.stock)
        self.assertTrue(True)

    def test_xgcs(self):
        sbuy = xgcs(self.stock)
        self.assertTrue(True)

    def test_xgcs0(self):
        sbuy = xgcs0(self.stock)
        self.assertTrue(True)

    def test_gcs(self):
        sbuy = gcs(self.stock)
        self.assertTrue(True)

    def test_mgcs(self):
        sbuy = mgcs(self.stock)
        self.assertTrue(True)

    def test_cma1(self):
        sbuy = cma1(self.stock)
        self.assertTrue(True)

    def test_gmacd(self):
        sbuy = gmacd(self.stock)
        self.assertTrue(True)

    def test_gmacd5(self):
        sbuy = gmacd5(self.stock)
        self.assertTrue(True)

    def test_gmacd_old(self):
        sbuy = gmacd_old(self.stock)
        self.assertTrue(True)

    def test_smacd(self):
        sbuy = smacd(self.stock)
        self.assertTrue(True)

    def test_xru(self):
        sbuy = xru(self.stock)
        self.assertTrue(True)
    
    def test_xru0(self):
        sbuy = xru0(self.stock)
        self.assertTrue(True)

    def test_mxru(self):
        sbuy = mxru(self.stock)
        self.assertTrue(True)

    def test_ldx(self):
        sbuy = ldx(self.stock)
        sbuy = ldx(self.stock,30,3333)
        self.assertTrue(True)

    def test_ldx2(self):
        sbuy = ldx(self.stock)
        sbuy = ldx(self.stock,30,3333)
        self.assertTrue(True)

    def test_xud(self):
        sbuy = xud(self.stock)
        self.assertTrue(True)

    def test_xud0(self):
        sbuy = xud0(self.stock)
        self.assertTrue(True)

    def test_xudj(self):
        sbuy = xudj(self.stock)
        self.assertTrue(True)

    def test_emv1(self):
        sbuy = emv1(self.stock)
        self.assertTrue(True)

    def test_emv1b(self):
        sbuy = emv1b(self.stock)
        self.assertTrue(True)

    def test_emv2(self):
        sbuy = emv2(self.stock,fast=10,slow=100)
        self.assertTrue(True)

    def test_emv2s(self):
        sbuy = emv2s(self.stock)
        self.assertTrue(True)

    def test_tsvama4(self):
        sbuy = tsvama4(self.stock,10,20,30,40)
        self.assertTrue(True)

    def test_tsvama3(self):
        sbuy = tsvama3(self.stock,10,20,30)
        self.assertTrue(True)

    def test_tsvama2sb(self):
        sbuy = tsvama2sb(self.stock,10,20)
        self.assertTrue(True)

    def test_tsvama2sbv(self):
        sbuy = tsvama2sbv(self.stock,10,20)
        self.assertTrue(True)

    def test_tsvama3b(self):
        sbuy = tsvama3b(self.stock,10,20,30)
        self.assertTrue(True)

    def test_ma2s(self):
        sbuy = ma2s(self.stock,10,20)
        self.assertTrue(True)

    def test_ma2sv(self):
        sbuy = ma2sv(self.stock,10,20)
        self.assertTrue(True)

    def test_ma2c(self):
        sbuy = ma2c(self.stock,10,20)
        self.assertTrue(True)

    def test_ldxc(self):
        sbuy = ldxc(self.stock)
        sbuy = ldxc(self.stock,30,3333)
        self.assertTrue(True)

    def test_tsvama2c(self):
        sbuy = tsvama2c(self.stock,5,20)
        self.assertTrue(True)

    def test_emv1c(self):
        sbuy = emv1c(self.stock,100)
        self.assertTrue(True)

    def test_emv2c(self):
        sbuy = emv2c(self.stock,fast=10,slow=100)
        self.assertTrue(True)

    def test_eff(self):
        sbuy = eff(self.stock)
        self.assertTrue(True)

    ##小时测试
    def test_heff(self):
        sbuy = heff(self.stock)
        self.assertTrue(True)

    def test_mag(self):
        sbuy = mag(self.stock)
        self.assertTrue(True)

    def test_uplain3(self):
        sbuy = uplain3(self.stock,lens=(1,2,3))
        self.assertTrue(True)

    def test_uplaind2(self):
        sbuy = uplaind2(self.stock,lens=(1,2,3))
        self.assertTrue(True)

    def test_xud3(self):
        sbuy = xud3(self.stock)
        self.assertTrue(True)

    def test_nhighxt(self):
        sbuy = nhighxt(self.stock)
        self.assertTrue(True)

    def test_nhighxt2(self):
        sbuy = nhighxt2(self.stock)
        self.assertTrue(True)

    def test_ldxx(self):
        sbuy = ldxx(self.stock)
        self.assertTrue(True)

    def test_tsvama2n(self):
        sbuy = tsvama2n(self.stock)
        self.assertTrue(True)

    def test_pmacd2(self):
        sbuy = pmacd2(self.stock)
        self.assertTrue(True)

    def test_b102(self):
        sbuy = b102(self.stock)
        self.assertTrue(True)

    def test_b2(self):
        sbuy = b2(self.stock)
        self.assertTrue(True)

    def test_b102b(self):
        sbuy = b102b(self.stock)
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

