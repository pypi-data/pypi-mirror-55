import os
import struct
import datetime
from enum import Enum

class Message:

    def __init__(self, file_path = None, buffer = None, parent = None):

        print('independentsoft.msg module - evaluation version. Copyright 2019 Independentsoft.')

        self.u___cz_sn___ = None        
        self.___t_lgsh__n = "IPM.Note"
        self.b_t___b_q_xu = None
        self._______c__ty = None
        self._s_k_n_jb___ = None
        self.w__teeli____ = None
        self.qj_wgu_zzu_s = None
        self.qw_____z__u_ = None
        self.p____t__w_g_ = None
        self.cx_p_u___h_i = None
        self.j__kfc___d_g = None
        self.p__w___rx_bo = None
        self.i_f__lcbcp__ = None
        self.kh_____k_y_g = None
        self.__zr_cn_k__x = None
        self._fz___ad_f__ = None
        self.a_uk__ilatjb = None
        self.____gw__e_a_ = None
        self.__z_j__au_m_ = datetime.datetime(1,1,1)
        self.i_zt_m_sm__i = datetime.datetime(1,1,1)
        self.___ud_______ = datetime.datetime(1,1,1)
        self._w______i_dp = datetime.datetime(1,1,1)
        self._e__gxx__h_u = datetime.datetime(1,1,1)
        self.__g__h_iwita = datetime.datetime(1,1,1)
        self.y_ze__l___u_ = datetime.datetime(1,1,1)
        self.__okvntl__d_ = None
        self.____l__er___ = None
        self.wo___yi_w__x = None
        self._so__s_lu_o_ = None
        self.j_a_______a_ = None
        self._r_h__rjorsu = None
        self._f__a___jm_p = 0
        self.__y__kwxb___ = 0
        self.c_dv__cjvvx_ = 0
        self.b_s_cu_d_ovr = 0
        self.wto_g_dk_qpf = None
        self.____zm_r_ip_ = False
        self.__m__df_ka_l = False
        self.veb_bv_____o = False
        self.i___d_zbbg__ = False
        self.r__gl__wj_yq = False
        self._h_____pvsgq = False
        self._qvy_dii__st = False
        self.________k___ = False
        self.j_ka_nrf____ = None
        self._g_h__sre__k = Sensitivity.NONE
        self.___ot__i_wup = Importance.NONE
        self._ff___oikg_n = Priority.NONE
        self._dhn__eqsl_x = FlagIcon.NONE
        self.j_e_m__r_qgm = FlagStatus.NONE
        self.uubu___mqh__ = ObjectType.NONE
        self._dn_pem__l__ = None
        self.li_leu_wgzg_ = None
        self._vezy_n_ikln = None
        self.q__q_k_r_cw_ = None
        self.i_r___noho_c = None
        self._ze__u_auq__ = None
        self.g__nj___m__u = None
        self.k_l_bco_s_jv = None
        self.__xh_ve_____ = None
        self.____uw__pp__ = None
        self.___onygff_yd = None
        self._p_y__of_ma_ = None
        self.p_k_wh_____c = None
        self.___yu____xb_ = None
        self.___xm__ne_t_ = None
        self.___s_iffiu__ = None
        self.__w_y_scz_u_ = None
        self.______z_____ = None
        self.y______e___l = None
        self.dqgxw_hnt__k = None
        self._o_wcivl____ = None
        self.__dq___iif_g = None
        self.___i___cdtv_ = None
        self.s_jwv_w__ng_ = datetime.datetime(1,1,1)
        self.i__n____fy__ = LastVerbExecuted.NONE
        self.r_w_jc__qzn_ = []
        self.s__f__m_okw_ = []
        self.___r_____tvp = None
        self._hv_i__xj___ = 0
        self.cr_xv___r_qv = datetime.datetime(1,1,1)
        self.egv____dws__ = datetime.datetime(1,1,1)
        self._i_n________ = datetime.datetime(1,1,1)
        self.s__a_____uwe = False
        self._fusob_vbnex = datetime.datetime(1,1,1)
        self._k__nlldizui = 0
        self.k__q__s__kb_ = []
        self._ycq__y_lj__ = []
        self.v__c___fhx_s = []
        self.__c_kkkbm_zh = None
        self._______ii___ = None
        self.z___xyhng_ev = None
        self.__pmh__t___j = False
        self.il__q_yhe___ = False
        self._y__h_t_h___ = False
        self.q___st__n__j = False
        self.__wn_______l = None
        self._l__p__mwm_q = datetime.datetime(1,1,1)
        self.__ma_m___ciq = datetime.datetime(1,1,1)
        self.sw__fy_____w = False
        self._____q__c_v_ = None
        self.__q__v_af___ = BusyStatus.NONE
        self.w_h_gqfnzf_i = MeetingStatus.NONE
        self.neh_l__xlj__ = ResponseStatus.NONE
        self.umc_fo_____x = RecurrenceType.NONE
        self.___d_l___xct = None
        self.____uf_h_uu_ = None
        self.m__zc_il___y = None
        self.r___af_zj_r_ = None
        self.____y___frl_ = None
        self._g___ehew___ = -1
        self.cy__hhh_jv__ = 0
        self.q________c_r = datetime.datetime(1,1,1)
        self.x___asp___iv = datetime.datetime(1,1,1)
        self.__wxx__pych_ = None
        self.rpu_b_xx__u_ = None
        self.____narlie_r = 0
        self._m__f_j__e_i = 0
        self.____v_y_n___ = 0
        self.__hk___s__ux = False
        self._n_ad___dz__ = False
        self._gfko_gic___ = datetime.datetime(1,1,1)
        self.__t___l__g__ = TaskStatus.NONE
        self.___pp__l____ = TaskOwnership.NONE
        self._____xn_oymn = TaskDelegationState.NONE
        self._____f_t_h__ = 0
        self.___e_p_s___a = 0
        self._mxah_ge__t_ = 0
        self.m_rdx____o__ = 0
        self.__zuaq___k_g = NoteColor.NONE
        self.c_p_irtpd___ = datetime.datetime(1,1,1)
        self.fyg_hq__zqla = datetime.datetime(1,1,1)
        self._n___mr_t_pn = None
        self.cbw_______xx = None
        self.w__c_rjwf_j_ = 0
        self.f___v_bof__x = datetime.datetime(1,1,1)
        self.__c__cw_h__a = []
        self.__e__w_t_p_q = None
        self._f_ha_w___mw = None
        self.vj_b__f__u__ = None
        self.hy_wucpf_c_j = None
        self._km___gfyym_ = None
        self.hhk__zyd_d__ = None
        self.bun___q__o__ = None
        self.___zpfq_tz__ = None
        self.__x_r_e_yh__ = None
        self.q_ob_____ij_ = None
        self.__f_fqzb___i = None
        self.y_b_h___p___ = None
        self.n____j____xe = None
        self.___yr__bvg__ = None
        self.__jjr_pc__t_ = None
        self.d_lurjyi___x = None
        self.__jra_lp____ = None
        self.____iiu_h__i = None
        self._y______e___ = None
        self.ol____d_r__y = None
        self.__t_j_op_tt_ = None
        self._m___i______ = None
        self.z__b________ = None
        self.jg____s__g_s = None
        self.gmy_g__pb__d = None
        self._pro__frgm__ = None
        self.___s__yjk_q_ = None
        self.kzdmh__i__y_ = None
        self.p__lj__pay_g = None
        self.vo___j____gl = None
        self.z_w_qqxyx___ = None
        self.___w__pydr__ = None
        self.__ppjf_____v = None
        self.____ixh_____ = None
        self.f__fj___kg__ = None
        self.fcg__x__l_bh = None
        self.hxpxy___q__z = None
        self.___a___sf___ = None
        self.___l__fc_s_d = None
        self.t____l_e_ob_ = None
        self.sfuq__vbny_x = None
        self._ox_pj__nhnr = None
        self.__b_y_d_kqv_ = None
        self.a_akhxq__gp_ = None
        self.k_m_i___o__h = None
        self._e___sik_flm = None
        self.lp_y_____s__ = None
        self.b_xkfy_m__v_ = None
        self.qvx_e_ns____ = None
        self.sba__qjh___k = None
        self.gs_m_____l__ = None
        self.__ju____j__c = None
        self._p__wc_gnx_g = None
        self.sc_gg_f____i = None
        self.lkex____f__e = None
        self.s___b__i___o = None
        self.lkc__aliq_g_ = None
        self._sw_lg____k_ = None
        self.b____ioy____ = None
        self.__j_____m_ge = None
        self.u_u_t_ci___p = datetime.datetime(1,1,1)
        self.bw____sz____ = Gender.NONE
        self._hle_ua_z__g = SelectedMailingAddress.NONE
        self.y__i_no____g = False
        self.__el_ca_i_l_ = None
        self.___w___f___x = None
        self.l_a_g_kx____ = None
        self.g___cd_p_do_ = None
        self.q_j______u_u = None
        self._iwxsuk___iu = None
        self._d_d___jg__u = None
        self.c_x_q___hzc_ = None
        self._c_dcu_np_f_ = None
        self._y_g__fjv_r_ = None
        self.____e____jg_ = None
        self.go___g_____l = None
        self.ypp___r__q__ = None
        self.q_vxh_uz___i = None
        self.qw__y_l__p__ = None
        self._a___u____sj = None
        self.v__kpwt___jh = None
        self.v_rn_m______ = None
        self.kiork_z_o__p = None
        self.n_dl_t_l____ = None
        self.____cve____g = None

        self.__g_y__yifly = []
        self.j____d____c_ = []
        self._r__n__wc_bq = []
        self._m_rz____h__ = []

        self._e_p_wn___m_ = "001E"
        self.sll__adckt__ = 0x001E
        self.q_rcyqzvz___ = "101E"
        self.__e_ylz_t_hl = 0x101E

        self._gm_g__n___a = 'utf_8'
        self.__z_oxrob_zv = 'utf_8'
        self.bn_lyk_isr_a = 'utf-16-le'
        self.ulyx_zb_hrlu = False

        if file_path is not None: 
            f = open(file_path, 'rb')
            buffer = f.read()
            self.jo__bob__g__(buffer)
            f.close()

        elif buffer != None:
            self.jo__bob__g__(buffer)
        elif parent != None:
            self.ulyx_zb_hrlu = True
            self.gv____n_c_u_(parent)
        else:
            self.s__f__m_okw_.append(StoreSupportMask.ATTACHMENTS)
            self.s__f__m_okw_.append(StoreSupportMask.CATEGORIZE)
            self.s__f__m_okw_.append(StoreSupportMask.CREATE)
            self.s__f__m_okw_.append(StoreSupportMask.HTML)
            self.s__f__m_okw_.append(StoreSupportMask.ITEM_PROC)
            self.s__f__m_okw_.append(StoreSupportMask.MODIFY)
            self.s__f__m_okw_.append(StoreSupportMask.MULTI_VALUE_PROPERTIES)
            self.s__f__m_okw_.append(StoreSupportMask.NOTIFY)
            self.s__f__m_okw_.append(StoreSupportMask.OLE)
            self.s__f__m_okw_.append(StoreSupportMask.PUSHER)
            self.s__f__m_okw_.append(StoreSupportMask.READ_ONLY)
            self.s__f__m_okw_.append(StoreSupportMask.RESTRICTIONS)
            self.s__f__m_okw_.append(StoreSupportMask.RTF)
            self.s__f__m_okw_.append(StoreSupportMask.SEARCH)
            self.s__f__m_okw_.append(StoreSupportMask.SORT)
            self.s__f__m_okw_.append(StoreSupportMask.SUBMIT)
            self.s__f__m_okw_.append(StoreSupportMask.UNCOMPRESSED_RTF)
            self.s__f__m_okw_.append(StoreSupportMask.UNICODE)

    def jo__bob__g__(self, __o_yqq_m_og):

            _d_nk_____s_ = CompoundFile(file_path = None, buffer = __o_yqq_m_og)

            fibxcee__jo_ =  _d_nk_____s_.root.get_entry("__nameid_version1.0")

            _____tdu__n_ = fibxcee__jo_.get_entry("__substg1.0_00020102")
            i_c_jk_bz___ = fibxcee__jo_.get_entry("__substg1.0_00030102")
            __ds_yzz_vtp = fibxcee__jo_.get_entry("__substg1.0_00040102")

            _u__j__z_s__ = {}
            self._m_rz____h__ = []

            if i_c_jk_bz___ is not None:

                u_______vi_v = int(i_c_jk_bz___.size / 8)
                xc____j___ge = i_c_jk_bz___.buffer

                for i in range(u_______vi_v):

                    _hi____o____ = int.from_bytes(xc____j___ge[i * 8: i * 8 + 4], "little")
                    _wemyf___m_m = int.from_bytes(xc____j___ge[i * 8 + 4: i * 8 + 8], "little")

                    _tgs__ywd___ = Message.pc____k_j___(_wemyf___m_m >> 16)
                    __u__ny__m_g = Message.pc____k_j___((_wemyf___m_m << 16) >> 16)
                    a__z____b_zn = Message.pc____k_j___(__u__ny__m_g >> 1)
                    dr___hgmpofu = Message.pc____k_j___(__u__ny__m_g << 15)

                    y_qm____k_zb = NamedProperty()

                    if dr___hgmpofu == 0: 
                        _____h_p__x_ = _hi____o____

                        y_qm____k_zb.id = _____h_p__x_
                        y_qm____k_zb.type = NamedPropertyType.NUMERICAL
                   
                    else:

                        __ez________ = _hi____o____
                        ___kuyfw____ = __ds_yzz_vtp.buffer
                        
                        _b___h_y_z__ = int.from_bytes(___kuyfw____[__ez________: __ez________ + 4], "little")

                        _h__v_yn__yl = None

                        if (_b___h_y_z__ > 0):
                            __x_z_b_xu__ = ___kuyfw____[__ez________ + 4: __ez________ + 4 + _b___h_y_z__]
                            _h__v_yn__yl = __x_z_b_xu__.decode('utf-16-le')

                        y_qm____k_zb.name = _h__v_yn__yl
                        y_qm____k_zb.type = NamedPropertyType.STRING

                    if a__z____b_zn == 1:
                        y_qm____k_zb.guid = StandardPropertySet.MAPI
                    elif a__z____b_zn == 2:
                        y_qm____k_zb.guid = StandardPropertySet.PUBLIC_STRINGS
                    elif a__z____b_zn > 2:
                        
                        ex_______o__ = a__z____b_zn - 3

                        u___ke_f__o_ = _____tdu__n_.buffer
                        _____r_u__z_ = u___ke_f__o_[ex_______o__ * 16: ex_______o__ * 16 + 16]

                        y_qm____k_zb.guid = _____r_u__z_
                    
                    if y_qm____k_zb.id > 0:

                        _or_tq__a___ = Message.t_z__y_g_o__(y_qm____k_zb.id, y_qm____k_zb.guid)
                        _lo_____z___ = str.format("{:04X}", 0x8000 + _tgs__ywd___)

                        if _or_tq__a___ not in _u__j__z_s__: 
                            _u__j__z_s__[_or_tq__a___] = _lo_____z___

                    elif (y_qm____k_zb.name is not None):

                        _or_tq__a___ = Message.t_z__y_g_o__(y_qm____k_zb.name, y_qm____k_zb.guid)
                        _lo_____z___ = str.format("{:04X}", 0x8000 + _tgs__ywd___)

                        if _or_tq__a___ not in _u__j__z_s__: 
                            _u__j__z_s__[_or_tq__a___] = _lo_____z___
         
                    self._m_rz____h__.append(y_qm____k_zb)


            for n in range(len(self._m_rz____h__)):

                qdn__kr____m = self._m_rz____h__[n]

                if qdn__kr____m.name is not None:
                    __g____jzf__ = ExtendedPropertyName(qdn__kr____m.name, qdn__kr____m.guid)
                    hdhurb__lfto = ExtendedProperty(__g____jzf__)
                    self._r__n__wc_bq.append(hdhurb__lfto)

                elif qdn__kr____m.id > 0:
                    ar__gs_s___a = ExtendedPropertyId(qdn__kr____m.id, qdn__kr____m.guid)
                    hdhurb__lfto = ExtendedProperty(ar__gs_s___a)
                    self._r__n__wc_bq.append(hdhurb__lfto)           

            self.gv____n_c_u_(_d_nk_____s_.root, _u__j__z_s__)

    def gv____n_c_u_(self, ___g__on___b, _u__j__z_s__ = None):
        self.wozah__z_gk_ = 24
        self.u___cz_sn___ = {}

        ne__vmw_____ = ___g__on___b.get_entry("__properties_version1.0")

        _rz_pt___fj_ = 0
        tb_x_f_rsw__ = 0

        if ne__vmw_____ is not None:
            __jiy_k_sel_ = int.from_bytes(ne__vmw_____.buffer[0:4], "little")
            __x_pz____x_ = int.from_bytes(ne__vmw_____.buffer[4:8], "little")
            _fsypxlk____ = int.from_bytes(ne__vmw_____.buffer[8:12], "little")
            jfjr_____ggm = int.from_bytes(ne__vmw_____.buffer[12:16], "little")
            _rz_pt___fj_ = int.from_bytes(ne__vmw_____.buffer[16:20], "little")
            tb_x_f_rsw__ = int.from_bytes(ne__vmw_____.buffer[20:24], "little")

        if not self.ulyx_zb_hrlu:
            
            if ne__vmw_____ is not None:
                w_____j___y_ = int.from_bytes(ne__vmw_____.buffer[24:28], "little")
                dex____toxfq = int.from_bytes(ne__vmw_____.buffer[28:32], "little")

            self.wozah__z_gk_ = 32

        if ne__vmw_____ is not None and ne__vmw_____.buffer is not None:
            
            for i in range(self.wozah__z_gk_, len(ne__vmw_____.buffer) - 15, 16):

                l___pci__a__ = ne__vmw_____.buffer[i: i+16]

                w___pj_kb__e = Property(l___pci__a__)

                if w___pj_kb__e.size > 0:

                    __f_j__nap_l = "__substg1.0_" + str.format("{:08X}", w___pj_kb__e.tag)

                    _wpy_q______ = ___g__on___b.get_entry(__f_j__nap_l)

                    if _wpy_q______ is not None and _wpy_q______.buffer is not None and len(_wpy_q______.buffer) > 0:
                        w___pj_kb__e.value = _wpy_q______.buffer[0: len(_wpy_q______.buffer)]                         
   
                b_f_g__mz__e = str.format("{:08X}", w___pj_kb__e.tag)

                try:
                    self.u___cz_sn___[b_f_g__mz__e] = w___pj_kb__e
                except:
                    pass


        _____fv____x = self.u___cz_sn___["3FDE0003"] if "3FDE0003" in self.u___cz_sn___ else None

        if _____fv____x is not None and _____fv____x.value is not None:
            self.b_s_cu_d_ovr = int.from_bytes(_____fv____x.value[0:4], "little")

        ___ly__xuf_j =  self.u___cz_sn___["3FFD0003"] if "3FFD0003" in self.u___cz_sn___ else None

        if ___ly__xuf_j is not None and ___ly__xuf_j.value is not None:
            self._f__a___jm_p = int.from_bytes(___ly__xuf_j.value[0:4], "little")
        
        if self._f__a___jm_p > 0:
        
            try:
                self._gm_g__n___a = Message.qb_s_dghkmbh(self._f__a___jm_p)
            except:
                pass 

        elif self.b_s_cu_d_ovr > 0:

            try:
                self._gm_g__n___a = Message.qb_s_dghkmbh(self.b_s_cu_d_ovr)
            except:
                pass

        __h_mw___yc_ = self.u___cz_sn___["340D0003"] if "340D0003" in self.u___cz_sn___ else None

        if __h_mw___yc_ is not None and __h_mw___yc_.value is not None:

            v____dys_oko = int.from_bytes(__h_mw___yc_.value[0: 4], "little")

            self.s__f__m_okw_ = EnumUtil.parse_store_support_mask(v____dys_oko)

            if (v____dys_oko & 0x00040000) == 0x00040000:

                self._gm_g__n___a = "utf-16-le"
                self._e_p_wn___m_ = "001F"
                self.sll__adckt__ = 0x001F
                self.q_rcyqzvz___ = "101F"
                self.__e_ylz_t_hl = 0x101F

       
        mkkh___d_lvf = len("\0".encode(self._gm_g__n___a))

        __okm_jmcx__ = self.u___cz_sn___["30070040"] if "30070040" in self.u___cz_sn___ else None

        if __okm_jmcx__ is not None and __okm_jmcx__.value is not None:

            s__q_pxjmgp_ = int.from_bytes(__okm_jmcx__.value[0: 4], "little")
            ___u___y_fk_ = int.from_bytes(__okm_jmcx__.value[4: 8], "little")

            if ___u___y_fk_ > 0:
                i_x____hz_to = s__q_pxjmgp_ + (___u___y_fk_ << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)  

                try:    
                    self.__z_j__au_m_ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.__z_j__au_m_ = Message._j__y____u__(self.__z_j__au_m_)
                except:
                    pass

        _yofpl_kej_s = self.u___cz_sn___["30080040"] if "30080040" in self.u___cz_sn___ else None

        if _yofpl_kej_s is not None and _yofpl_kej_s.value is not None:

            ____k_i____h = int.from_bytes(_yofpl_kej_s.value[0: 4], "little")
            tscb__mc_k__ = int.from_bytes(_yofpl_kej_s.value[4: 8], "little")

            if tscb__mc_k__ > 0:
                i_x____hz_to = ____k_i____h + (tscb__mc_k__ << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)   

                try:    
                    self.i_zt_m_sm__i = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.i_zt_m_sm__i = Message._j__y____u__(self.i_zt_m_sm__i)
                except:
                    pass

        wr_q_s___m__ = self.u___cz_sn___["0E060040"] if "0E060040" in self.u___cz_sn___ else None

        if wr_q_s___m__ is not None and wr_q_s___m__.value is not None:

            _zx_ajnb_vf_ = int.from_bytes(wr_q_s___m__.value[0: 4], "little")
            n__pv___x__i = int.from_bytes(wr_q_s___m__.value[4: 8], "little")

            if n__pv___x__i > 0:
                i_x____hz_to = _zx_ajnb_vf_ + (n__pv___x__i << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)

                try:    
                    self.___ud_______ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.___ud_______ = Message._j__y____u__(self.___ud_______)
                except:
                    pass

        _ay_z__qhtgj = self.u___cz_sn___["00390040"] if "00390040" in self.u___cz_sn___ else None

        if _ay_z__qhtgj is not None and _ay_z__qhtgj.value is not None:

            ze___zx__fbk = int.from_bytes(_ay_z__qhtgj.value[0: 4], "little")
            csgu________ = int.from_bytes(_ay_z__qhtgj.value[4: 8], "little")

            if csgu________ > 0:
                i_x____hz_to = ze___zx__fbk + (csgu________ << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)

                try:    
                    self._w______i_dp = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self._w______i_dp = Message._j__y____u__(self._w______i_dp)
                except:
                    pass 

        ___qm__iio__ = self.u___cz_sn___["000F0040"] if "000F0040" in self.u___cz_sn___ else None

        if ___qm__iio__ is not None and ___qm__iio__.value is not None:

            od_u_j___a_b = int.from_bytes(___qm__iio__.value[0: 4], "little")
            e___f__q__f_ = int.from_bytes(___qm__iio__.value[4: 8], "little")

            if e___f__q__f_ > 0:
                i_x____hz_to = od_u_j___a_b + (e___f__q__f_ << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)

                try:    
                    self._e__gxx__h_u = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self._e__gxx__h_u = Message._j__y____u__(self._e__gxx__h_u)
                except:
                    pass 

        zl__s_fs_z__ = self.u___cz_sn___["00480040"] if "00480040" in self.u___cz_sn___ else None

        if zl__s_fs_z__ is not None and zl__s_fs_z__.value is not None:

            _____e_fr___ = int.from_bytes(zl__s_fs_z__.value[0: 4], "little")
            _xg____mpl_c = int.from_bytes(zl__s_fs_z__.value[4: 8], "little")

            if _xg____mpl_c > 0:
                i_x____hz_to = _____e_fr___ + (_xg____mpl_c << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)

                try:    
                    self.__g__h_iwita = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.__g__h_iwita = Message._j__y____u__(self.__g__h_iwita)
                except:
                    pass 

        _c_bymosg_oo = self.u___cz_sn___["00320040"] if "00320040" in self.u___cz_sn___ else None

        if _c_bymosg_oo is not None and _c_bymosg_oo.value is not None:

            ugv_dkz_ak__ = int.from_bytes(_c_bymosg_oo.value[0: 4], "little")
            __t___cr___n = int.from_bytes(_c_bymosg_oo.value[4: 8], "little")

            if __t___cr___n > 0:
                i_x____hz_to = ugv_dkz_ak__ + (__t___cr___n << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)   

                try:    
                    self.y_ze__l___u_ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.y_ze__l___u_ = Message._j__y____u__(self.y_ze__l___u_)
                except:
                    pass 


        ___n______qb = self.u___cz_sn___["10820040"] if "10820040" in self.u___cz_sn___ else None

        if ___n______qb is not None and ___n______qb.value is not None:

            ___ppmcef___ = int.from_bytes(___n______qb.value[0: 4], "little")
            p___nn____sj = int.from_bytes(___n______qb.value[4: 8], "little")

            if p___nn____sj > 0:
                i_x____hz_to = ___ppmcef___ + (p___nn____sj << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)      

                try:    
                    self.s_jwv_w__ng_ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.s_jwv_w__ng_ = Message._j__y____u__(self.s_jwv_w__ng_)
                except:
                    pass 

        _y_l_f_ib_r_ = self.u___cz_sn___["10800003"] if "10800003" in self.u___cz_sn___ else None

        if _y_l_f_ib_r_ is not None and _y_l_f_ib_r_.value is not None:
            self.__y__kwxb___ = int.from_bytes(_y_l_f_ib_r_.value[0:4], "little")

        r_d__uad____ = self.u___cz_sn___["0E080003"] if "0E080003" in self.u___cz_sn___ else None

        if r_d__uad____ is not None and r_d__uad____.value is not None:
            self.c_dv__cjvvx_ = int.from_bytes(r_d__uad____.value[0:4], "little")

        _b___p__z_vn = self.u___cz_sn___["0E070003"] if "0E070003" in self.u___cz_sn___ else None

        if _b___p__z_vn is not None and _b___p__z_vn.value is not None:
            l__l_sh_yb__ = int.from_bytes(_b___p__z_vn.value[0:4], "little")
            self.r_w_jc__qzn_ = EnumUtil.parse_message_flag(l__l_sh_yb__)

        isw_jy_tcw_i = self.u___cz_sn___["10F4000B"] if "10F4000B" in self.u___cz_sn___ else None

        if isw_jy_tcw_i is not None and isw_jy_tcw_i.value is not None:
            _o_b______f_ = int.from_bytes(isw_jy_tcw_i.value[0:2], "little")
            
            if _o_b______f_ > 0:
                self.____zm_r_ip_ = True

        __sra_ufo__v = self.u___cz_sn___["10F6000B"] if "10F6000B" in self.u___cz_sn___ else None

        if __sra_ufo__v is not None and __sra_ufo__v.value is not None:
            z_f_w_st_s__ = int.from_bytes(__sra_ufo__v.value[0:2], "little")
            
            if z_f_w_st_s__ > 0:
                self.__m__df_ka_l = True

        zeq__w_ewwvv = self.u___cz_sn___["10F5000B"] if "10F5000B" in self.u___cz_sn___ else None

        if zeq__w_ewwvv is not None and zeq__w_ewwvv.value is not None:
            ___a____hwj_ = int.from_bytes(zeq__w_ewwvv.value[0:2], "little")
            
            if ___a____hwj_ > 0:
                self.veb_bv_____o = True

        u__xm_he___i = self.u___cz_sn___["10F2000B"] if "10F2000B" in self.u___cz_sn___ else None

        if u__xm_he___i is not None and u__xm_he___i.value is not None:
            c__j_yq__fn_ = int.from_bytes(u__xm_he___i.value[0:2], "little")
            
            if c__j_yq__fn_ > 0:
                self.i___d_zbbg__ = True

        jk__i_wc_dbz = self.u___cz_sn___["0E1B000B"] if "0E1B000B" in self.u___cz_sn___ else None

        if jk__i_wc_dbz is not None and jk__i_wc_dbz.value is not None:
            o_y_qsz____i = int.from_bytes(jk__i_wc_dbz.value[0:2], "little")
            
            if o_y_qsz____i > 0:
                self.r__gl__wj_yq = True

        e_m_ymrr_ob_ = self.u___cz_sn___["0E1F000B"] if "0E1F000B" in self.u___cz_sn___ else None

        if e_m_ymrr_ob_ is not None and e_m_ymrr_ob_.value is not None:
            __xp_ombn___ = int.from_bytes(e_m_ymrr_ob_.value[0:2], "little")
            
            if __xp_ombn___ > 0:
                self._h_____pvsgq = True

        i__bkuk__d__ = self.u___cz_sn___["0029000B"] if "0029000B" in self.u___cz_sn___ else None

        if i__bkuk__d__ is not None and i__bkuk__d__.value is not None:
            z______lrieg = int.from_bytes(i__bkuk__d__.value[0:2], "little")
            
            if z______lrieg > 0:
                self._qvy_dii__st = True

        _b___q______ = self.u___cz_sn___["0023000B"] if "0023000B" in self.u___cz_sn___ else None

        if _b___q______ is not None and _b___q______.value is not None:
            __o___sqtore = int.from_bytes(_b___q______.value[0:2], "little")
            
            if __o___sqtore > 0:
                self.________k___ = True

        _a___t___cit = self.u___cz_sn___["00360003"] if "00360003" in self.u___cz_sn___ else None

        if _a___t___cit is not None and _a___t___cit.value is not None:
            __x__e_b_nth = int.from_bytes(_a___t___cit.value[0:4], "little")
            
            self._g_h__sre__k = EnumUtil.parse_sensitivity(__x__e_b_nth)

        __j__f___wp_ = self.u___cz_sn___["10810003"] if "10810003" in self.u___cz_sn___ else None

        if __j__f___wp_ is not None and __j__f___wp_.value is not None:
            __o_w_zo___g = int.from_bytes(__j__f___wp_.value[0:4], "little")
            
            self.i__n____fy__ = EnumUtil.parse_last_verb_executed(__o_w_zo___g)

        r___i_jx__ws = self.u___cz_sn___["00170003"] if "00170003" in self.u___cz_sn___ else None

        if r___i_jx__ws is not None and r___i_jx__ws.value is not None:
            q_ux_l__jhs_ = int.from_bytes(r___i_jx__ws.value[0:4], "little")
            
            self.___ot__i_wup = EnumUtil.parse_importance(q_ux_l__jhs_)

        _i_w_vq_o__s = self.u___cz_sn___["00260003"] if "00260003" in self.u___cz_sn___ else None

        if _i_w_vq_o__s is not None and _i_w_vq_o__s.value is not None:
            h_f_u__y____ = int.from_bytes(_i_w_vq_o__s.value[0:4], "little")
            
            self._ff___oikg_n = EnumUtil.parse_priority(h_f_u__y____)

        _fqf__z__hlb = self.u___cz_sn___["10950003"] if "10950003" in self.u___cz_sn___ else None

        if _fqf__z__hlb is not None and _fqf__z__hlb.value is not None:
            e_rew_yg__x_ = int.from_bytes(_fqf__z__hlb.value[0:4], "little")
            
            self._dhn__eqsl_x = EnumUtil.parse_flag_icon(e_rew_yg__x_)

        d_w_l_n____u = self.u___cz_sn___["10950003"] if "10950003" in self.u___cz_sn___ else None

        if d_w_l_n____u is not None and d_w_l_n____u.value is not None:
            gk____fi__iu = int.from_bytes(d_w_l_n____u.value[0:4], "little")
            
            self.j_e_m__r_qgm = EnumUtil.parse_flag_status(gk____fi__iu)

        _wm___g_s__j = self.u___cz_sn___["0FFE0003"] if "0FFE0003" in self.u___cz_sn___ else None

        if _wm___g_s__j is not None and _wm___g_s__j.value is not None:
            njn_____cu_x = int.from_bytes(_wm___g_s__j.value[0:4], "little")
            
            self.uubu___mqh__ = EnumUtil.parse_object_type(njn_____cu_x)


        j_x_f__c_g__ = 0x8554
        ___pgf_na___ = StandardPropertySet.COMMON

        __v_p_j_c_r_ = Message.t_z__y_g_o__(j_x_f__c_g__, ___pgf_na___)

        if _u__j__z_s__ is not None and __v_p_j_c_r_ in _u__j__z_s__ and _u__j__z_s__[__v_p_j_c_r_] is not None:
            
            d___pr____z_ = _u__j__z_s__[__v_p_j_c_r_]
            d___pr____z_ = d___pr____z_ + self._e_p_wn___m_

            ve________ov = self.u___cz_sn___[d___pr____z_] if d___pr____z_ in self.u___cz_sn___ else None

            if ve________ov is not None and ve________ov.value is not None:
                self.___r_____tvp = ve________ov.value.decode(self._gm_g__n___a)


        xr_mb_s___uj = 0x8552
        ____a_____f_ = StandardPropertySet.COMMON

        ____n___zn__ = Message.t_z__y_g_o__(xr_mb_s___uj, ____a_____f_)

        if _u__j__z_s__ is not None and ____n___zn__ in _u__j__z_s__ and _u__j__z_s__[____n___zn__] is not None:
            
            ______y__u_v = _u__j__z_s__[____n___zn__]
            ______y__u_v = ______y__u_v + "0003"

            __n__b_ca___ = self.u___cz_sn___[______y__u_v] if ______y__u_v in self.u___cz_sn___ else None

            if __n__b_ca___ is not None and __n__b_ca___.value is not None:
                self._hv_i__xj___ = name = int.from_bytes(__n__b_ca___.value[0:4], "little")


        vn__hg_wtq_c = 0x8516
        q_w__m___pgg = StandardPropertySet.COMMON

        __im__o_lm__ = Message.t_z__y_g_o__(vn__hg_wtq_c, q_w__m___pgg)

        if _u__j__z_s__ is not None and __im__o_lm__ in _u__j__z_s__ and _u__j__z_s__[__im__o_lm__] is not None:
            
            y__zo_me_a__ = _u__j__z_s__[__im__o_lm__]
            y__zo_me_a__ = y__zo_me_a__ + "0040"

            ___mwe___zci = self.u___cz_sn___[y__zo_me_a__] if y__zo_me_a__ in self.u___cz_sn___ else None

            if ___mwe___zci is not None and ___mwe___zci.value is not None:

                ___c___i_l__ = int.from_bytes(___mwe___zci.value[0: 4], "little")
                _i_myr__b_za = int.from_bytes(___mwe___zci.value[4: 8], "little")

                if _i_myr__b_za > 0:
                    i_x____hz_to = ___c___i_l__ + (_i_myr__b_za << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)

                    try:    
                        self.cr_xv___r_qv = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.cr_xv___r_qv = Message._j__y____u__(self.cr_xv___r_qv)
                    except:
                        pass 

        __vj__i__ill = 0x8517
        l_z_d_y_m_ur = StandardPropertySet.COMMON

        __qq__xm____ = Message.t_z__y_g_o__(__vj__i__ill, l_z_d_y_m_ur)

        if _u__j__z_s__ is not None and __qq__xm____ in _u__j__z_s__ and _u__j__z_s__[__qq__xm____] is not None:
            
            _m__kh__p_xf = _u__j__z_s__[__qq__xm____]
            _m__kh__p_xf = _m__kh__p_xf + "0040"

            i_tnclu_o___ = self.u___cz_sn___[_m__kh__p_xf] if _m__kh__p_xf in self.u___cz_sn___ else None

            if i_tnclu_o___ is not None and i_tnclu_o___.value is not None:

                gs_____u_yq_ = int.from_bytes(i_tnclu_o___.value[0: 4], "little")
                ___t_____r__ = int.from_bytes(i_tnclu_o___.value[4: 8], "little")

                if ___t_____r__ > 0:
                    i_x____hz_to = gs_____u_yq_ + (___t_____r__ << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)

                    try:    
                        self.egv____dws__ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.egv____dws__ = Message._j__y____u__(self.egv____dws__)
                    except:
                        pass 


        ai_y_pu__w_g = 0x8560
        _tih__qfeq__ = StandardPropertySet.COMMON

        _cvh_yus_y_s = Message.t_z__y_g_o__(ai_y_pu__w_g, _tih__qfeq__)

        if _u__j__z_s__ is not None and _cvh_yus_y_s in _u__j__z_s__ and _u__j__z_s__[_cvh_yus_y_s] is not None:
            
            d___w_t_agf_ = _u__j__z_s__[_cvh_yus_y_s]
            d___w_t_agf_ = d___w_t_agf_ + "0040"

            v__j___wzj__ = self.u___cz_sn___[d___w_t_agf_] if d___w_t_agf_ in self.u___cz_sn___ else None

            if v__j___wzj__ is not None and v__j___wzj__.value is not None:

                n_o_i___x_p_ = int.from_bytes(v__j___wzj__.value[0: 4], "little")
                _ni___gw____ = int.from_bytes(v__j___wzj__.value[4: 8], "little")

                if _ni___gw____ > 0:
                    i_x____hz_to = n_o_i___x_p_ + (_ni___gw____ << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)      
                    
                    try:
                        self._i_n________ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)
                        self._i_n________ = Message._j__y____u__(self._i_n________)
                    except:
                        pass 


        _____h____cb = 0x8539
        wh___hbs_l_n = StandardPropertySet.COMMON

        iw__jh__u_c_ = Message.t_z__y_g_o__(_____h____cb, wh___hbs_l_n)

        if _u__j__z_s__ is not None and iw__jh__u_c_ in _u__j__z_s__ and _u__j__z_s__[iw__jh__u_c_] is not None:
            
            md__qo_pf__r = _u__j__z_s__[iw__jh__u_c_]
            md__qo_pf__r = d___w_t_agf_ + self.q_rcyqzvz___

            ___h_q_f__r_ = self.u___cz_sn___[md__qo_pf__r] if md__qo_pf__r in self.u___cz_sn___ else None

            if ___h_q_f__r_ is not None and ___h_q_f__r_.value is not None:

                _v__x_pqz_l_ = int(___h_q_f__r_.size / 4)

                self.k__q__s__kb_ = []

                for i in range(_v__x_pqz_l_):

                    __ie_wy_lv__ = "__substg1.0_" + md__qo_pf__r + "-" + str.format("{:08X}", i)

                    j___a_x_____ = ___g__on___b.get_entry(__ie_wy_lv__)

                    if j___a_x_____ is not None and j___a_x_____.buffer is not None:

                        gja_g__soa__ = j___a_x_____.buffer[0: len(j___a_x_____.buffer) - mkkh___d_lvf].decode(self._gm_g__n___a)
                        self.k__q__s__kb_.append(gja_g__soa__)


        _____f__p_h_ = 0x853A
        objsr_gt___f = StandardPropertySet.COMMON

        __vyq_____h_ = Message.t_z__y_g_o__(_____f__p_h_, objsr_gt___f)

        if _u__j__z_s__ is not None and __vyq_____h_ in _u__j__z_s__ and _u__j__z_s__[__vyq_____h_] is not None:
            
            s__uhzj_wn_o = _u__j__z_s__[__vyq_____h_]
            s__uhzj_wn_o = d___w_t_agf_ + self.q_rcyqzvz___

            ____uo_ejfb_ = self.u___cz_sn___[s__uhzj_wn_o] if s__uhzj_wn_o in self.u___cz_sn___ else None

            if ____uo_ejfb_ is not None and ____uo_ejfb_.value is not None:

                _v__hj_gpwg_ = int(____uo_ejfb_.size / 4)

                self._ycq__y_lj__ = []

                for i in range(_v__hj_gpwg_):

                    __ie_wy_lv__ = "__substg1.0_" + s__uhzj_wn_o + "-" + str.format("{:08X}", i)

                    j___a_x_____ = ___g__on___b.get_entry(__ie_wy_lv__)

                    if j___a_x_____ is not None and j___a_x_____.buffer is not None:

                        bfz_f____bja = j___a_x_____.buffer[0: len(j___a_x_____.buffer) - mkkh___d_lvf].decode(self._gm_g__n___a)
                        self._ycq__y_lj__.append(bfz_f____bja)


        _wjd_fi____l = "Keywords"
        k__wjg__n___ = StandardPropertySet.PUBLIC_STRINGS

        __fw_r_o__n_ = Message.t_z__y_g_o__(_wjd_fi____l, k__wjg__n___)

        if _u__j__z_s__ is not None and __fw_r_o__n_ in _u__j__z_s__ and _u__j__z_s__[__fw_r_o__n_] is not None:
            
            tuf__xu_nri_ = _u__j__z_s__[__fw_r_o__n_]
            tuf__xu_nri_ = tuf__xu_nri_ + self.q_rcyqzvz___

            i__x_______a = self.u___cz_sn___[tuf__xu_nri_] if tuf__xu_nri_ in self.u___cz_sn___ else None

            if i__x_______a is not None and i__x_______a.value is not None:

                _vernp_t___z = int(i__x_______a.size / 4)

                self.v__c___fhx_s = []

                for i in range(_vernp_t___z):

                    __ie_wy_lv__ = "__substg1.0_" + tuf__xu_nri_ + "-" + str.format("{:08X}", i)

                    j___a_x_____ = ___g__on___b.get_entry(__ie_wy_lv__)

                    if j___a_x_____ is not None and j___a_x_____.buffer is not None:

                        ___jmnvmy___ = j___a_x_____.buffer[0: len(j___a_x_____.buffer) - mkkh___d_lvf].decode(self._gm_g__n___a)
                        self.v__c___fhx_s.append(___jmnvmy___)


        wszve_b____d = 0x8535
        q___m_wjlb__ = StandardPropertySet.COMMON

        ____gimkk__d = Message.t_z__y_g_o__(wszve_b____d, q___m_wjlb__)

        if _u__j__z_s__ is not None and ____gimkk__d in _u__j__z_s__ and _u__j__z_s__[____gimkk__d] is not None:
            
            ____sroi__kx = _u__j__z_s__[____gimkk__d]
            ____sroi__kx = ____sroi__kx + self._e_p_wn___m_

            y_mb_jpg_h_g = self.u___cz_sn___[____sroi__kx] if ____sroi__kx in self.u___cz_sn___ else None

            if y_mb_jpg_h_g is not None and y_mb_jpg_h_g.value is not None:
                self.__c_kkkbm_zh = y_mb_jpg_h_g.value.decode(self._gm_g__n___a)


        _d__jp_fla_t = 0x8534
        __p__x_f_s__ = StandardPropertySet.COMMON

        _____gni_p__ = Message.t_z__y_g_o__(_d__jp_fla_t, __p__x_f_s__)

        if _u__j__z_s__ is not None and _____gni_p__ in _u__j__z_s__ and _u__j__z_s__[_____gni_p__] is not None:
            
            y__l___zmk__ = _u__j__z_s__[_____gni_p__]
            y__l___zmk__ = y__l___zmk__ + self._e_p_wn___m_

            h___bhzdke__ = self.u___cz_sn___[y__l___zmk__] if y__l___zmk__ in self.u___cz_sn___ else None

            if h___bhzdke__ is not None and h___bhzdke__.value is not None:
                self._______ii___ = h___bhzdke__.value.decode(self._gm_g__n___a)

        
        q__ak_w_oe_c = 0x8580
        _vxpp__y____ = StandardPropertySet.COMMON

        _g__w__ddz__ = Message.t_z__y_g_o__(q__ak_w_oe_c, _vxpp__y____)

        if _u__j__z_s__ is not None and _g__w__ddz__ in _u__j__z_s__ and _u__j__z_s__[_g__w__ddz__] is not None:
            
            oobeed_y__i_ = _u__j__z_s__[_g__w__ddz__]
            oobeed_y__i_ = oobeed_y__i_ + self._e_p_wn___m_

            x_husr_n_cz_ = self.u___cz_sn___[oobeed_y__i_] if oobeed_y__i_ in self.u___cz_sn___ else None

            if x_husr_n_cz_ is not None and x_husr_n_cz_.value is not None:
                self.__wn_______l = x_husr_n_cz_.value.decode(self._gm_g__n___a)


        f_ul_mt_n_aw = 0x851F
        d___lh______ = StandardPropertySet.COMMON

        _vx___zgtr__ = Message.t_z__y_g_o__(f_ul_mt_n_aw, d___lh______)

        if _u__j__z_s__ is not None and _vx___zgtr__ in _u__j__z_s__ and _u__j__z_s__[_vx___zgtr__] is not None:
            
            ot_othmd_exl = _u__j__z_s__[_vx___zgtr__]
            ot_othmd_exl = ot_othmd_exl + self._e_p_wn___m_

            __od_eqrqf__ = self.u___cz_sn___[ot_othmd_exl] if ot_othmd_exl in self.u___cz_sn___ else None

            if __od_eqrqf__ is not None and __od_eqrqf__.value is not None:
                self.z___xyhng_ev = __od_eqrqf__.value.decode(self._gm_g__n___a)


        _k_wq__u__f_ = 0x8506
        n__ecaz__pjq = StandardPropertySet.COMMON

        x_x___tl_l_r = Message.t_z__y_g_o__(_k_wq__u__f_, n__ecaz__pjq)

        if _u__j__z_s__ is not None and x_x___tl_l_r in _u__j__z_s__ and _u__j__z_s__[x_x___tl_l_r] is not None:
            
            mog___lnxm__ = _u__j__z_s__[x_x___tl_l_r]
            mog___lnxm__ = mog___lnxm__ + "000B"

            jyj_ccw_m___ = self.u___cz_sn___[mog___lnxm__] if mog___lnxm__ in self.u___cz_sn___ else None

            if jyj_ccw_m___ is not None and jyj_ccw_m___.value is not None:

                ls___wzfnz_i = int.from_bytes(jyj_ccw_m___.value[0:2], "little")
                
                if ls___wzfnz_i > 0:
                    self.__pmh__t___j = True
        

        hrq____y__u_ = 0x851C
        ___h_g__ehjk = StandardPropertySet.COMMON

        _sk_odp_a_fr = Message.t_z__y_g_o__(hrq____y__u_, ___h_g__ehjk)

        if _u__j__z_s__ is not None and _sk_odp_a_fr in _u__j__z_s__ and _u__j__z_s__[_sk_odp_a_fr] is not None:
            
            wx______kg_r = _u__j__z_s__[_sk_odp_a_fr]
            wx______kg_r = wx______kg_r + "000B"

            __fnzpa_fn_c = self.u___cz_sn___[wx______kg_r] if wx______kg_r in self.u___cz_sn___ else None

            if __fnzpa_fn_c is not None and __fnzpa_fn_c.value is not None:

                loaux_g_n___ = int.from_bytes(__fnzpa_fn_c.value[0:2], "little")
                
                if loaux_g_n___ > 0:
                    self._y__h_t_h___ = True


        _l_l_k_mtz__ = 0x851E
        _s__o_i___f_ = StandardPropertySet.COMMON

        ____zbl__s__ = Message.t_z__y_g_o__(_l_l_k_mtz__, _s__o_i___f_)

        if _u__j__z_s__ is not None and ____zbl__s__ in _u__j__z_s__ and _u__j__z_s__[____zbl__s__] is not None:
            
            j_m_a_jl_z_u = _u__j__z_s__[____zbl__s__]
            j_m_a_jl_z_u = j_m_a_jl_z_u + "000B"

            c_ycbvt_b___ = self.u___cz_sn___[j_m_a_jl_z_u] if j_m_a_jl_z_u in self.u___cz_sn___ else None

            if c_ycbvt_b___ is not None and c_ycbvt_b___.value is not None:

                _i_y__h_ocf_ = int.from_bytes(c_ycbvt_b___.value[0:2], "little")
                
                if _i_y__h_ocf_ > 0:
                    self.q___st__n__j = True


        yvq_jxfd_b__ = 0x820D
        ____b_muq_x_ = StandardPropertySet.APPOINTMENT

        __igg_l_____ = Message.t_z__y_g_o__(yvq_jxfd_b__, ____b_muq_x_)

        if _u__j__z_s__ is not None and __igg_l_____ in _u__j__z_s__ and _u__j__z_s__[__igg_l_____] is not None:
            
            _ib_u_i_o___ = _u__j__z_s__[__igg_l_____]
            _ib_u_i_o___ = _ib_u_i_o___ + "0040"

            _o_______ojy = self.u___cz_sn___[_ib_u_i_o___] if _ib_u_i_o___ in self.u___cz_sn___ else None

            if _o_______ojy is not None and _o_______ojy.value is not None:

                gy_ft_pu__r_ = int.from_bytes(_o_______ojy.value[0: 4], "little")
                w____u_p_w__ = int.from_bytes(_o_______ojy.value[4: 8], "little")

                if w____u_p_w__ > 0:
                    i_x____hz_to = gy_ft_pu__r_ + (w____u_p_w__ << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)  

                    try:    
                        self._l__p__mwm_q = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self._l__p__mwm_q = Message._j__y____u__(self._l__p__mwm_q)
                    except:
                        pass 

        do_iav__mtbm = 0x820E
        rj_ld_t__omh = StandardPropertySet.APPOINTMENT

        zjrs__sr_e_h = Message.t_z__y_g_o__(do_iav__mtbm, rj_ld_t__omh)

        if _u__j__z_s__ is not None and zjrs__sr_e_h in _u__j__z_s__ and _u__j__z_s__[zjrs__sr_e_h] is not None:
            
            ia___pmzlgxe = _u__j__z_s__[zjrs__sr_e_h]
            ia___pmzlgxe = ia___pmzlgxe + "0040"

            ___a_c_k_x_x = self.u___cz_sn___[ia___pmzlgxe] if ia___pmzlgxe in self.u___cz_sn___ else None

            if ___a_c_k_x_x is not None and ___a_c_k_x_x.value is not None:

                d__dhr_____s = int.from_bytes(___a_c_k_x_x.value[0: 4], "little")
                __g_b__s__o_ = int.from_bytes(___a_c_k_x_x.value[4: 8], "little")

                if __g_b__s__o_ > 0:
                    i_x____hz_to = d__dhr_____s + (__g_b__s__o_ << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)

                    try:    
                        self.__ma_m___ciq = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.__ma_m___ciq = Message._j__y____u__(self.__ma_m___ciq)
                    except:
                        pass 


        q______y_s_t = 0x8208
        _to_h_____vg = StandardPropertySet.APPOINTMENT

        lnwc_lfd__j_ = Message.t_z__y_g_o__(q______y_s_t, _to_h_____vg)

        if _u__j__z_s__ is not None and lnwc_lfd__j_ in _u__j__z_s__ and _u__j__z_s__[lnwc_lfd__j_] is not None:
            
            i____p_kr_ie = _u__j__z_s__[lnwc_lfd__j_]
            i____p_kr_ie = i____p_kr_ie + self._e_p_wn___m_

            ____ng_v_g_m = self.u___cz_sn___[i____p_kr_ie] if i____p_kr_ie in self.u___cz_sn___ else None

            if ____ng_v_g_m is not None and ____ng_v_g_m.value is not None:
                self._____q__c_v_ = ____ng_v_g_m.value.decode(self._gm_g__n___a)


        _j_jv___fppe =  0x24
        e____ib____a = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5])

        _n__jgj__eup = Message.t_z__y_g_o__(_j_jv___fppe, e____ib____a)

        if _u__j__z_s__ is not None and _n__jgj__eup in _u__j__z_s__ and _u__j__z_s__[_n__jgj__eup] is not None:
            
            qoz_j_j__nt_ = _u__j__z_s__[_n__jgj__eup]
            qoz_j_j__nt_ = qoz_j_j__nt_ + self._e_p_wn___m_

            qs____r_ue__ = self.u___cz_sn___[qoz_j_j__nt_] if qoz_j_j__nt_ in self.u___cz_sn___ else None

            if qs____r_ue__ is not None and qs____r_ue__.value is not None:
                self.___d_l___xct = qs____r_ue__.value.decode(self._gm_g__n___a)


        __v__l____je = 0x8234
        an_w_d_c_g_s = StandardPropertySet.APPOINTMENT

        g__d_o__siyf = Message.t_z__y_g_o__(__v__l____je, an_w_d_c_g_s)

        if _u__j__z_s__ is not None and g__d_o__siyf in _u__j__z_s__ and _u__j__z_s__[g__d_o__siyf] is not None:
            
            _fwrvtg____g = _u__j__z_s__[g__d_o__siyf]
            _fwrvtg____g = _fwrvtg____g + self._e_p_wn___m_

            p_s__x___x_b = self.u___cz_sn___[_fwrvtg____g] if _fwrvtg____g in self.u___cz_sn___ else None

            if p_s__x___x_b is not None and p_s__x___x_b.value is not None:
                self.____uf_h_uu_ = p_s__x___x_b.value.decode(self._gm_g__n___a)


        _yx_dr___k__ = 0x8232
        mj__q_zv_ztt = StandardPropertySet.APPOINTMENT

        l___q_w_____ = Message.t_z__y_g_o__(_yx_dr___k__, mj__q_zv_ztt)

        if _u__j__z_s__ is not None and l___q_w_____ in _u__j__z_s__ and _u__j__z_s__[l___q_w_____] is not None:
            
            v_ud_f_z_kjp = _u__j__z_s__[l___q_w_____]
            v_ud_f_z_kjp = v_ud_f_z_kjp + self._e_p_wn___m_

            mi__ye_o___w = self.u___cz_sn___[v_ud_f_z_kjp] if v_ud_f_z_kjp in self.u___cz_sn___ else None

            if mi__ye_o___w is not None and mi__ye_o___w.value is not None:
                self.m__zc_il___y = mi__ye_o___w.value.decode(self._gm_g__n___a)


        sz_afva__hr_ = 0x8216
        n_fkq_x___ly = StandardPropertySet.APPOINTMENT

        i_qluwdi_hyo = Message.t_z__y_g_o__(sz_afva__hr_, n_fkq_x___ly)

        if _u__j__z_s__ is not None and i_qluwdi_hyo in _u__j__z_s__ and _u__j__z_s__[i_qluwdi_hyo] is not None:
            
            ______n___e_ = _u__j__z_s__[i_qluwdi_hyo]
            ______n___e_ = ______n___e_ + "0102"

            _____a___m_h = self.u___cz_sn___[______n___e_] if ______n___e_ in self.u___cz_sn___ else None

            if _____a___m_h is not None and _____a___m_h.value is not None:
                self.r___af_zj_r_ = RecurrencePattern(_____a___m_h.value)


        z___dg____yr = 0x8116
        _____jrsarf_ = StandardPropertySet.TASK

        _______ir_o_ = Message.t_z__y_g_o__(z___dg____yr, _____jrsarf_)

        if _u__j__z_s__ is not None and _______ir_o_ in _u__j__z_s__ and _u__j__z_s__[_______ir_o_] is not None:
            
            k____ph___d_ = _u__j__z_s__[_______ir_o_]
            k____ph___d_ = k____ph___d_ + "0102"

            __zc_jemtnau = self.u___cz_sn___[k____ph___d_] if k____ph___d_ in self.u___cz_sn___ else None

            if __zc_jemtnau is not None and __zc_jemtnau.value is not None:
                self.n_c_fo_t__s_ = RecurrencePattern(__zc_jemtnau.value)


        _e__td_ktmwq = 0x8205
        _oq_p___idky = StandardPropertySet.APPOINTMENT

        __w__sqgh__r = Message.t_z__y_g_o__(_e__td_ktmwq, _oq_p___idky)

        if _u__j__z_s__ is not None and __w__sqgh__r in _u__j__z_s__ and _u__j__z_s__[__w__sqgh__r] is not None:
            
            jbe_j_gy_nd_ = _u__j__z_s__[__w__sqgh__r]
            jbe_j_gy_nd_ = jbe_j_gy_nd_ + "0003"

            _ps____ww_j_ = self.u___cz_sn___[jbe_j_gy_nd_] if jbe_j_gy_nd_ in self.u___cz_sn___ else None

            if _ps____ww_j_ is not None and _ps____ww_j_.value is not None:

                __tne__aq__g = int.from_bytes(_ps____ww_j_.value[0:4], "little")

                self.__q__v_af___ = EnumUtil.parse_busy_status(__tne__aq__g)


        m__e__rk_zd_ = 0x8217
        _________ogw = StandardPropertySet.APPOINTMENT

        __ov_c_b_ae_ = Message.t_z__y_g_o__(m__e__rk_zd_, _________ogw)

        if _u__j__z_s__ is not None and __ov_c_b_ae_ in _u__j__z_s__ and _u__j__z_s__[__ov_c_b_ae_] is not None:
            
            __qs____u___ = _u__j__z_s__[__ov_c_b_ae_]
            __qs____u___ = __qs____u___ + "0003"

            i___e___b_vq = self.u___cz_sn___[__qs____u___] if __qs____u___ in self.u___cz_sn___ else None

            if i___e___b_vq is not None and i___e___b_vq.value is not None:

                b____jedbm__ = int.from_bytes(i___e___b_vq.value[0:4], "little")

                self.w_h_gqfnzf_i = EnumUtil.parse_meeting_status(b____jedbm__)


        p_z__l_ho_j_ = 0x8218
        __g___y___ey = StandardPropertySet.APPOINTMENT

        el__fi_j_v__ = Message.t_z__y_g_o__(p_z__l_ho_j_, __g___y___ey)

        if _u__j__z_s__ is not None and el__fi_j_v__ in _u__j__z_s__ and _u__j__z_s__[el__fi_j_v__] is not None:
            
            __j_vs__gr_s = _u__j__z_s__[el__fi_j_v__]
            __j_vs__gr_s = __j_vs__gr_s + "0003"

            _gp___ue____ = self.u___cz_sn___[__j_vs__gr_s] if __j_vs__gr_s in self.u___cz_sn___ else None

            if _gp___ue____ is not None and _gp___ue____.value is not None:

                bcdrtv_x____ = int.from_bytes(_gp___ue____.value[0:4], "little")

                self.neh_l__xlj__ = EnumUtil.parse_response_status(bcdrtv_x____)

    
        ___y_____h_j = 0x8231
        i__csgv_z__i = StandardPropertySet.APPOINTMENT

        y_k______s_n = Message.t_z__y_g_o__(___y_____h_j, i__csgv_z__i)

        if _u__j__z_s__ is not None and y_k______s_n in _u__j__z_s__ and _u__j__z_s__[y_k______s_n] is not None:
            
            et_m__fv___e = _u__j__z_s__[y_k______s_n]
            et_m__fv___e = et_m__fv___e + "0003"

            h_u___q__odh = self.u___cz_sn___[et_m__fv___e] if et_m__fv___e in self.u___cz_sn___ else None

            if h_u___q__odh is not None and h_u___q__odh.value is not None:

                ___u__reud__ = int.from_bytes(h_u___q__odh.value[0:4], "little")

                self.umc_fo_____x = EnumUtil.parse_recurrence_type(___u__reud__)


        _e_i__g_____ = 0x3
        _truj_w__gb_ = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5])

        j_____j__a__ = Message.t_z__y_g_o__(_e_i__g_____, _truj_w__gb_)

        if _u__j__z_s__ is not None and j_____j__a__ in _u__j__z_s__ and _u__j__z_s__[j_____j__a__] is not None:
            
            _y__wu_rokj_ = _u__j__z_s__[j_____j__a__]
            _y__wu_rokj_ = _y__wu_rokj_ + "0102"

            y___rwyjp_my = self.u___cz_sn___[_y__wu_rokj_] if _y__wu_rokj_ in self.u___cz_sn___ else None

            if y___rwyjp_my is not None and y___rwyjp_my.value is not None:

                self.____y___frl_ = y___rwyjp_my.value


        ui_r_blwj__e = 0x8214
        pn___yc___t_ = StandardPropertySet.APPOINTMENT

        l__________w = Message.t_z__y_g_o__(ui_r_blwj__e, pn___yc___t_)

        if _u__j__z_s__ is not None and l__________w in _u__j__z_s__ and _u__j__z_s__[l__________w] is not None:
            
            wwh_mvk__tw_ = _u__j__z_s__[l__________w]
            wwh_mvk__tw_ = wwh_mvk__tw_ + "0003"

            __rw_zptmxdr = self.u___cz_sn___[wwh_mvk__tw_] if wwh_mvk__tw_ in self.u___cz_sn___ else None

            if __rw_zptmxdr is not None and __rw_zptmxdr.value is not None:

                self._g___ehew___ = int.from_bytes(__rw_zptmxdr.value[0:4], "little")


        ____l__yjuow = 0x8213
        s_dj_p_____t = StandardPropertySet.APPOINTMENT

        _g_lm__xe_nf = Message.t_z__y_g_o__(____l__yjuow, s_dj_p_____t)

        if _u__j__z_s__ is not None and _g_lm__xe_nf in _u__j__z_s__ and _u__j__z_s__[_g_lm__xe_nf] is not None:
            
            q_j_yo_____m = _u__j__z_s__[_g_lm__xe_nf]
            q_j_yo_____m = q_j_yo_____m + "0003"

            _s_q_hpk_fli = self.u___cz_sn___[q_j_yo_____m] if q_j_yo_____m in self.u___cz_sn___ else None

            if _s_q_hpk_fli is not None and _s_q_hpk_fli.value is not None:

                self.cy__hhh_jv__ = int.from_bytes(_s_q_hpk_fli.value[0:4], "little")


        __q_r_b__p__ = 0x811F
        e__t_vq_hm__ = StandardPropertySet.TASK

        __sh____r__q = Message.t_z__y_g_o__(__q_r_b__p__, e__t_vq_hm__)

        if _u__j__z_s__ is not None and __sh____r__q in _u__j__z_s__ and _u__j__z_s__[__sh____r__q] is not None:
            
            pb_r___dy_jl = _u__j__z_s__[__sh____r__q]
            pb_r___dy_jl = pb_r___dy_jl + self._e_p_wn___m_

            __g______z__ = self.u___cz_sn___[pb_r___dy_jl] if pb_r___dy_jl in self.u___cz_sn___ else None

            if __g______z__ is not None and __g______z__.value is not None:

                self.__wxx__pych_ = __g______z__.value.decode(self._gm_g__n___a)


        _n_____l_wyv = 0x8121
        _tbfje__n__d = StandardPropertySet.TASK

        o___nxz__o__ = Message.t_z__y_g_o__(_n_____l_wyv, _tbfje__n__d)

        if _u__j__z_s__ is not None and o___nxz__o__ in _u__j__z_s__ and _u__j__z_s__[o___nxz__o__] is not None:
            
            fo__h_____h_ = _u__j__z_s__[o___nxz__o__]
            fo__h_____h_ = fo__h_____h_ + self._e_p_wn___m_

            ___af_____e_ = self.u___cz_sn___[fo__h_____h_] if fo__h_____h_ in self.u___cz_sn___ else None

            if ___af_____e_ is not None and ___af_____e_.value is not None:

                self.rpu_b_xx__u_ = ___af_____e_.value.decode(self._gm_g__n___a)


        k_f_tek_gvpp = 0x8102
        w__p_h_n__b_ = StandardPropertySet.TASK

        ___u_z_by__c = Message.t_z__y_g_o__(k_f_tek_gvpp, w__p_h_n__b_)

        if _u__j__z_s__ is not None and ___u_z_by__c in _u__j__z_s__ and _u__j__z_s__[___u_z_by__c] is not None:
            
            ut_k_sn_b_gd = _u__j__z_s__[___u_z_by__c]
            ut_k_sn_b_gd = ut_k_sn_b_gd + "0005"

            ____k_k_i__n = self.u___cz_sn___[ut_k_sn_b_gd] if ut_k_sn_b_gd in self.u___cz_sn___ else None

            if ____k_k_i__n is not None and ____k_k_i__n.value is not None:

                _ekd____pux_ = struct.unpack('<d', ____k_k_i__n.value[0:8])

                if _ekd____pux_ is not None:
                    self.____narlie_r = _ekd____pux_[0]
                  
                
        __b__oj_va__ = 0x8110
        oh___pk___x_ = StandardPropertySet.TASK

        _y___tisv__a = Message.t_z__y_g_o__(__b__oj_va__, oh___pk___x_)

        if _u__j__z_s__ is not None and _y___tisv__a in _u__j__z_s__ and _u__j__z_s__[_y___tisv__a] is not None:
            
            _tp_z_______ = _u__j__z_s__[_y___tisv__a]
            _tp_z_______ = _tp_z_______ + "0003"

            ___oi____p_r = self.u___cz_sn___[_tp_z_______] if _tp_z_______ in self.u___cz_sn___ else None

            if ___oi____p_r is not None and ___oi____p_r.value is not None:

                self._m__f_j__e_i = int.from_bytes(___oi____p_r.value[0:4], "little")


        _i_n__y__q_d = 0x8111
        _fhi___vo___ = StandardPropertySet.TASK

        ____r__to__o = Message.t_z__y_g_o__(_i_n__y__q_d, _fhi___vo___)

        if _u__j__z_s__ is not None and ____r__to__o in _u__j__z_s__ and _u__j__z_s__[____r__to__o] is not None:
            
            xm_sqh_w_tm_ = _u__j__z_s__[____r__to__o]
            xm_sqh_w_tm_ = xm_sqh_w_tm_ + "0003"

            ieemg__lv_kt = self.u___cz_sn___[xm_sqh_w_tm_] if xm_sqh_w_tm_ in self.u___cz_sn___ else None

            if ieemg__lv_kt is not None and ieemg__lv_kt.value is not None:

                self.____v_y_n___ = int.from_bytes(ieemg__lv_kt.value[0:4], "little")


        _qvgga__u__s = 0x8103
        __s__j_j__t_ = StandardPropertySet.TASK

        qk___d_t_fb_ = Message.t_z__y_g_o__(_qvgga__u__s, __s__j_j__t_)

        if _u__j__z_s__ is not None and qk___d_t_fb_ in _u__j__z_s__ and _u__j__z_s__[qk___d_t_fb_] is not None:
            
            rio__ploo___ = _u__j__z_s__[qk___d_t_fb_]
            rio__ploo___ = rio__ploo___ + "000B"

            s_fa_m___l__ = self.u___cz_sn___[rio__ploo___] if rio__ploo___ in self.u___cz_sn___ else None

            if s_fa_m___l__ is not None and s_fa_m___l__.value is not None:

                is_team_value = int.from_bytes(s_fa_m___l__.value[0:2], "little")

                if is_team_value > 0:
                    self.__hk___s__ux = True


        __z_p_v_joil = 0x811C
        _u___c__x___ = StandardPropertySet.TASK

        a__vcx_____b = Message.t_z__y_g_o__(__z_p_v_joil, _u___c__x___)

        if _u__j__z_s__ is not None and a__vcx_____b in _u__j__z_s__ and _u__j__z_s__[a__vcx_____b] is not None:
            
            __p__thl__w_ = _u__j__z_s__[a__vcx_____b]
            __p__thl__w_ = __p__thl__w_ + "000B"

            __a____ho__l = self.u___cz_sn___[__p__thl__w_] if __p__thl__w_ in self.u___cz_sn___ else None

            if __a____ho__l is not None and __a____ho__l.value is not None:

                r_jw___ew__w = int.from_bytes(__a____ho__l.value[0:2], "little")

                if r_jw___ew__w > 0:
                    self._____btju__g = True


        tm_____x_bkj = 0x8223
        k___rujx_h_s = StandardPropertySet.APPOINTMENT

        ______skzj__ = Message.t_z__y_g_o__(tm_____x_bkj, k___rujx_h_s)

        if _u__j__z_s__ is not None and ______skzj__ in _u__j__z_s__ and _u__j__z_s__[______skzj__] is not None:
            
            x_pt_uffo__n = _u__j__z_s__[______skzj__]
            x_pt_uffo__n = x_pt_uffo__n + "000B"

            _a_t_____j_q = self.u___cz_sn___[x_pt_uffo__n] if x_pt_uffo__n in self.u___cz_sn___ else None

            if _a_t_____j_q is not None and _a_t_____j_q.value is not None:

                ____i_____lq = int.from_bytes(_a_t_____j_q.value[0:2], "little")

                if ____i_____lq > 0:
                    self.ejz_p_f___pd = True


        qhwt_____qvq = 0x8215
        _te_kg_qj___ = StandardPropertySet.APPOINTMENT

        v__xpmxa__m_ = Message.t_z__y_g_o__(qhwt_____qvq, _te_kg_qj___)

        if _u__j__z_s__ is not None and v__xpmxa__m_ in _u__j__z_s__ and _u__j__z_s__[v__xpmxa__m_] is not None:
            
            pag_u_p_kgr_ = _u__j__z_s__[v__xpmxa__m_]
            pag_u_p_kgr_ = pag_u_p_kgr_ + "000B"

            c__sytej___f = self.u___cz_sn___[pag_u_p_kgr_] if pag_u_p_kgr_ in self.u___cz_sn___ else None

            if c__sytej___f is not None and c__sytej___f.value is not None:

                _zi_t_dt_n__ = int.from_bytes(c__sytej___f.value[0:2], "little")

                if _zi_t_dt_n__ > 0:
                    self.g__j__he___k = True


        ____eqqs_pwf = 0x8503
        vq__a__sd_xl = StandardPropertySet.COMMON

        _sb_n_tk_k_u = Message.t_z__y_g_o__(____eqqs_pwf, vq__a__sd_xl)

        if _u__j__z_s__ is not None and _sb_n_tk_k_u in _u__j__z_s__ and _u__j__z_s__[_sb_n_tk_k_u] is not None:
            
            rx__kq_rqbi_ = _u__j__z_s__[_sb_n_tk_k_u]
            rx__kq_rqbi_ = rx__kq_rqbi_ + "000B"

            __nndk_gd__k = self.u___cz_sn___[rx__kq_rqbi_] if rx__kq_rqbi_ in self.u___cz_sn___ else None

            if __nndk_gd__k is not None and __nndk_gd__k.value is not None:

                xc____tg_le_ = int.from_bytes(__nndk_gd__k.value[0:2], "little")

                if xc____tg_le_ > 0:
                    self.a_wghb__mj__ = True


        __g_____w_oj = 0x8502
        __fu___g_rn_ = StandardPropertySet.COMMON

        qf__z_o__oet = Message.t_z__y_g_o__(__g_____w_oj, __fu___g_rn_)

        if _u__j__z_s__ is not None and qf__z_o__oet in _u__j__z_s__ and _u__j__z_s__[qf__z_o__oet] is not None:
            
            hze__iof_l_r = _u__j__z_s__[qf__z_o__oet]
            hze__iof_l_r = hze__iof_l_r + "0040"

            _yo_fd__lf__ = self.u___cz_sn___[hze__iof_l_r] if hze__iof_l_r in self.u___cz_sn___ else None

            if _yo_fd__lf__ is not None and _yo_fd__lf__.value is not None:

                _pyhbix___i_ = int.from_bytes(_yo_fd__lf__.value[0: 4], "little")
                rjzy______xp = int.from_bytes(_yo_fd__lf__.value[4: 8], "little")

                if rjzy______xp > 0:
                    i_x____hz_to = _pyhbix___i_ + (rjzy______xp << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)      

                    try:    
                        self._fusob_vbnex = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self._fusob_vbnex = Message._j__y____u__(self._fusob_vbnex)
                    except:
                        pass 


        __p_hk_d__k_ = 0x8501
        ____e___i_ql = StandardPropertySet.COMMON

        xxg___c_w__w = Message.t_z__y_g_o__(__p_hk_d__k_, ____e___i_ql)

        if _u__j__z_s__ is not None and xxg___c_w__w in _u__j__z_s__ and _u__j__z_s__[xxg___c_w__w] is not None:
            
            x____o_ba_ae = _u__j__z_s__[xxg___c_w__w]
            x____o_ba_ae = x____o_ba_ae + "0003"

            _y__l_______ = self.u___cz_sn___[x____o_ba_ae] if x____o_ba_ae in self.u___cz_sn___ else None

            if _y__l_______ is not None and _y__l_______.value is not None:

                self._k__nlldizui = int.from_bytes(_y__l_______.value[0:4], "little")


        e_____f___kj = 0x8104
        u____c_vb__g = StandardPropertySet.TASK

        _h__c_jd__fj = Message.t_z__y_g_o__(e_____f___kj, u____c_vb__g)

        if _u__j__z_s__ is not None and _h__c_jd__fj in _u__j__z_s__ and _u__j__z_s__[_h__c_jd__fj] is not None:
            
            p_a_njwt_lr_ = _u__j__z_s__[_h__c_jd__fj]
            p_a_njwt_lr_ = p_a_njwt_lr_ + "0040"

            __d_y_nc_x__ = self.u___cz_sn___[p_a_njwt_lr_] if p_a_njwt_lr_ in self.u___cz_sn___ else None

            if __d_y_nc_x__ is not None and __d_y_nc_x__.value is not None:

                ___tge__fsy_ = int.from_bytes(__d_y_nc_x__.value[0: 4], "little")
                g_f___t__v__ = int.from_bytes(__d_y_nc_x__.value[4: 8], "little")

                if g_f___t__v__ > 0:
                    i_x____hz_to = ___tge__fsy_ + (g_f___t__v__ << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)   

                    try:    
                        self.q________c_r = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.q________c_r = Message._j__y____u__(self.q________c_r)
                    except:
                        pass 


        __p_u__wgr_h = 0x8105
        dcy____z_g_s = StandardPropertySet.TASK

        k_djn_gs_j_b = Message.t_z__y_g_o__(__p_u__wgr_h, dcy____z_g_s)

        if _u__j__z_s__ is not None and k_djn_gs_j_b in _u__j__z_s__ and _u__j__z_s__[k_djn_gs_j_b] is not None:
            
            _____p_i___r = _u__j__z_s__[k_djn_gs_j_b]
            _____p_i___r = _____p_i___r + "0040"

            _xt_______lr = self.u___cz_sn___[_____p_i___r] if _____p_i___r in self.u___cz_sn___ else None

            if _xt_______lr is not None and _xt_______lr.value is not None:

                ____y__ncrh_ = int.from_bytes(_xt_______lr.value[0: 4], "little")
                _wn__sofyne_ = int.from_bytes(_xt_______lr.value[4: 8], "little")

                if _wn__sofyne_ > 0:
                    i_x____hz_to = ____y__ncrh_ + (_wn__sofyne_ << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)  

                    try:    
                        self.x___asp___iv = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.x___asp___iv = Message._j__y____u__(self.x___asp___iv)
                    except:
                        pass 


        __q____sc___ = 0x810F
        __c_ojp__ai_ = StandardPropertySet.TASK

        _nkry_______ = Message.t_z__y_g_o__(__q____sc___, __c_ojp__ai_)

        if _u__j__z_s__ is not None and _nkry_______ in _u__j__z_s__ and _u__j__z_s__[_nkry_______] is not None:
            
            _az__v_____r = _u__j__z_s__[_nkry_______]
            _az__v_____r = _az__v_____r + "0040"

            _nj__ehbt__z = self.u___cz_sn___[_az__v_____r] if _az__v_____r in self.u___cz_sn___ else None

            if _nj__ehbt__z is not None and _nj__ehbt__z.value is not None:

                riqklb___wn_ = int.from_bytes(_nj__ehbt__z.value[0: 4], "little")
                _bdp___p_duw = int.from_bytes(_nj__ehbt__z.value[4: 8], "little")

                if _bdp___p_duw > 0:
                    i_x____hz_to = riqklb___wn_ + (_bdp___p_duw << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)

                    try:    
                        self._gfko_gic___ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self._gfko_gic___ = Message._j__y____u__(self._gfko_gic___)
                    except:
                        pass


        q___ls___o_s = 0x8101
        _bzvp_ntsm__ = StandardPropertySet.TASK

        ____r_puqpa_ = Message.t_z__y_g_o__(q___ls___o_s, _bzvp_ntsm__)

        if _u__j__z_s__ is not None and ____r_puqpa_ in _u__j__z_s__ and _u__j__z_s__[____r_puqpa_] is not None:
            
            _z_jjp_li___ = _u__j__z_s__[____r_puqpa_]
            _z_jjp_li___ = _z_jjp_li___ + "0003"

            _o_vrx_s___q = self.u___cz_sn___[_z_jjp_li___] if _z_jjp_li___ in self.u___cz_sn___ else None

            if _o_vrx_s___q is not None and _o_vrx_s___q.value is not None:

                _t__c____cwa = int.from_bytes(_o_vrx_s___q.value[0:4], "little")

                self.__t___l__g__ = EnumUtil.parse_task_status(_t__c____cwa)


        ___q__iv___u = 0x8129
        _______ul_h_ = StandardPropertySet.TASK

        __rj__h_r_dh = Message.t_z__y_g_o__(___q__iv___u, _______ul_h_)

        if _u__j__z_s__ is not None and __rj__h_r_dh in _u__j__z_s__ and _u__j__z_s__[__rj__h_r_dh] is not None:
            
            fp_y_vk___ey = _u__j__z_s__[__rj__h_r_dh]
            fp_y_vk___ey = fp_y_vk___ey + "0003"

            iv_etk_hke_i = self.u___cz_sn___[fp_y_vk___ey] if fp_y_vk___ey in self.u___cz_sn___ else None

            if iv_etk_hke_i is not None and iv_etk_hke_i.value is not None:

                __r_wz_xwqps = int.from_bytes(iv_etk_hke_i.value[0:4], "little")

                self.___pp__l____ = EnumUtil.parse_task_ownership(__r_wz_xwqps)


        o___dbv___nv = 0x812A
        uqto__tyfsys = StandardPropertySet.TASK

        __u_d_o__bb_ = Message.t_z__y_g_o__(o___dbv___nv, uqto__tyfsys)

        if _u__j__z_s__ is not None and __u_d_o__bb_ in _u__j__z_s__ and _u__j__z_s__[__u_d_o__bb_] is not None:
            
            pifq_____nb_ = _u__j__z_s__[__u_d_o__bb_]
            pifq_____nb_ = pifq_____nb_ + "0003"

            _s____g_en_y = self.u___cz_sn___[pifq_____nb_] if pifq_____nb_ in self.u___cz_sn___ else None

            if _s____g_en_y is not None and _s____g_en_y.value is not None:

                xp_____ejj_q = int.from_bytes(_s____g_en_y.value[0:4], "little")

                self._____xn_oymn = EnumUtil.parse_task_delegation_state(xp_____ejj_q)


        nwoy____udr_ = 0x8B05
        aiz_cf__bxvq = StandardPropertySet.NOTE

        n_h_jtbheee_ = Message.t_z__y_g_o__(nwoy____udr_, aiz_cf__bxvq)

        if _u__j__z_s__ is not None and n_h_jtbheee_ in _u__j__z_s__ and _u__j__z_s__[n_h_jtbheee_] is not None:
            
            z__p_uzns__i = _u__j__z_s__[n_h_jtbheee_]
            z__p_uzns__i = z__p_uzns__i + "0003"

            bsh_x__cz__r = self.u___cz_sn___[z__p_uzns__i] if z__p_uzns__i in self.u___cz_sn___ else None

            if bsh_x__cz__r is not None and bsh_x__cz__r.value is not None:

                self.m_rdx____o__ = int.from_bytes(bsh_x__cz__r.value[0:4], "little")


        __o_cgg__nh_ = 0x8B04
        _l__d_fefk_d = StandardPropertySet.NOTE

        xt_e_d___o__ = Message.t_z__y_g_o__(__o_cgg__nh_, _l__d_fefk_d)

        if _u__j__z_s__ is not None and xt_e_d___o__ in _u__j__z_s__ and _u__j__z_s__[xt_e_d___o__] is not None:
            
            __g__ww_b_np = _u__j__z_s__[xt_e_d___o__]
            __g__ww_b_np = __g__ww_b_np + "0003"

            qd_o_e_amv__ = self.u___cz_sn___[__g__ww_b_np] if __g__ww_b_np in self.u___cz_sn___ else None

            if qd_o_e_amv__ is not None and qd_o_e_amv__.value is not None:

                self._mxah_ge__t_ = int.from_bytes(qd_o_e_amv__.value[0:4], "little")


        rc__n_b__u__ = 0x8B03
        h____m__zvc_ = StandardPropertySet.NOTE

        qif_c_k_ai__ = Message.t_z__y_g_o__(rc__n_b__u__, h____m__zvc_)

        if _u__j__z_s__ is not None and qif_c_k_ai__ in _u__j__z_s__ and _u__j__z_s__[qif_c_k_ai__] is not None:
            
            md_l_c__a___ = _u__j__z_s__[qif_c_k_ai__]
            md_l_c__a___ = md_l_c__a___ + "0003"

            ____ghjs__q_ = self.u___cz_sn___[md_l_c__a___] if md_l_c__a___ in self.u___cz_sn___ else None

            if ____ghjs__q_ is not None and ____ghjs__q_.value is not None:

                self.___e_p_s___a = int.from_bytes(____ghjs__q_.value[0:4], "little")


        _e___k_u____ = 0x8B02
        _nshvax_h_fo = StandardPropertySet.NOTE

        d____mio__jh = Message.t_z__y_g_o__(_e___k_u____, _nshvax_h_fo)

        if _u__j__z_s__ is not None and d____mio__jh in _u__j__z_s__ and _u__j__z_s__[d____mio__jh] is not None:
            
            __sm_yh_j___ = _u__j__z_s__[d____mio__jh]
            __sm_yh_j___ = __sm_yh_j___ + "0003"

            __________a_ = self.u___cz_sn___[__sm_yh_j___] if __sm_yh_j___ in self.u___cz_sn___ else None

            if __________a_ is not None and __________a_.value is not None:

                self._____f_t_h__ = int.from_bytes(__________a_.value[0:4], "little")


        m____le_bm__ = 0x8B00
        umt__k_vef_e = StandardPropertySet.NOTE

        __k___rhvu__ = Message.t_z__y_g_o__(m____le_bm__, umt__k_vef_e)

        if _u__j__z_s__ is not None and __k___rhvu__ in _u__j__z_s__ and _u__j__z_s__[__k___rhvu__] is not None:
            
            tgm_e_mtx___ = _u__j__z_s__[__k___rhvu__]
            tgm_e_mtx___ = tgm_e_mtx___ + "0003"

            __m___kcq___ = self.u___cz_sn___[tgm_e_mtx___] if tgm_e_mtx___ in self.u___cz_sn___ else None

            if __m___kcq___ is not None and __m___kcq___.value is not None:

                self.__zuaq___k_g = int.from_bytes(__m___kcq___.value[0:4], "little")


        d____j_a_p__ = 0x8706
        n__w_w____q_ = StandardPropertySet.JOURNAL

        ___z_b_f___x = Message.t_z__y_g_o__(d____j_a_p__, n__w_w____q_)

        if _u__j__z_s__ is not None and ___z_b_f___x in _u__j__z_s__ and _u__j__z_s__[___z_b_f___x] is not None:
            
            _ivcy____jl_ = _u__j__z_s__[___z_b_f___x]
            _ivcy____jl_ = _ivcy____jl_ + "0040"

            hh___qy_f__h = self.u___cz_sn___[_ivcy____jl_] if _ivcy____jl_ in self.u___cz_sn___ else None

            if hh___qy_f__h is not None and hh___qy_f__h.value is not None:

                _____uvx_ho_ = int.from_bytes(hh___qy_f__h.value[0: 4], "little")
                eg____l_z__m = int.from_bytes(hh___qy_f__h.value[4: 8], "little")

                if eg____l_z__m > 0:
                    i_x____hz_to = _____uvx_ho_ + (eg____l_z__m << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)

                    try:    
                        self.c_p_irtpd___ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.c_p_irtpd___ = Message._j__y____u__(self.c_p_irtpd___)
                    except:
                        pass 

        l_k____y__ft = 0x8708
        k___hy__i__i = StandardPropertySet.JOURNAL

        r_os____w_e_ = Message.t_z__y_g_o__(l_k____y__ft, k___hy__i__i)

        if _u__j__z_s__ is not None and r_os____w_e_ in _u__j__z_s__ and _u__j__z_s__[r_os____w_e_] is not None:
            
            r___m_sa___n = _u__j__z_s__[r_os____w_e_]
            r___m_sa___n = r___m_sa___n + "0040"

            ku_____wsu__ = self.u___cz_sn___[r___m_sa___n] if r___m_sa___n in self.u___cz_sn___ else None

            if ku_____wsu__ is not None and ku_____wsu__.value is not None:

                ____ze__v_f_ = int.from_bytes(ku_____wsu__.value[0: 4], "little")
                _m_pzv_c__yh = int.from_bytes(ku_____wsu__.value[4: 8], "little")

                if _m_pzv_c__yh > 0:
                    i_x____hz_to = ____ze__v_f_ + (_m_pzv_c__yh << 32)
                    j____h_x_v_h = datetime.datetime(1601,1,1)

                    try:    
                        self.fyg_hq__zqla = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                        self.fyg_hq__zqla = Message._j__y____u__(self.fyg_hq__zqla)
                    except:
                        pass 


        c____g___zr_ = 0x8700
        dme__xr__vl_ = StandardPropertySet.JOURNAL

        m___se_____h = Message.t_z__y_g_o__(c____g___zr_, dme__xr__vl_)

        if _u__j__z_s__ is not None and m___se_____h in _u__j__z_s__ and _u__j__z_s__[m___se_____h] is not None:
            
            ___t__y__i__ = _u__j__z_s__[m___se_____h]
            ___t__y__i__ = ___t__y__i__ + self._e_p_wn___m_

            s__g__fn_in_ = self.u___cz_sn___[___t__y__i__] if ___t__y__i__ in self.u___cz_sn___ else None

            if s__g__fn_in_ is not None and s__g__fn_in_.value is not None:

                self._n___mr_t_pn = s__g__fn_in_.value.decode(self._gm_g__n___a)

        
        zx_wf__k_g_l = 0x8712
        _yrsk_s_mro_ = StandardPropertySet.JOURNAL

        y____vy_u__f = Message.t_z__y_g_o__(zx_wf__k_g_l, _yrsk_s_mro_)

        if _u__j__z_s__ is not None and y____vy_u__f in _u__j__z_s__ and _u__j__z_s__[y____vy_u__f] is not None:
            
            _____p___w_k = _u__j__z_s__[y____vy_u__f]
            _____p___w_k = _____p___w_k + self._e_p_wn___m_

            y___hqk___m_ = self.u___cz_sn___[_____p___w_k] if _____p___w_k in self.u___cz_sn___ else None

            if y___hqk___m_ is not None and y___hqk___m_.value is not None:

                self.cbw_______xx = y___hqk___m_.value.decode(self._gm_g__n___a)


        __q_s____n_y = 0x8707
        f_j_r_z_sox_ = StandardPropertySet.JOURNAL

        _____gy__j_i = Message.t_z__y_g_o__(__q_s____n_y, f_j_r_z_sox_)

        if _u__j__z_s__ is not None and _____gy__j_i in _u__j__z_s__ and _u__j__z_s__[_____gy__j_i] is not None:
            
            k__o___u_kai = _u__j__z_s__[_____gy__j_i]
            k__o___u_kai = k__o___u_kai + "0003"

            k_____qh_h_z = self.u___cz_sn___[k__o___u_kai] if k__o___u_kai in self.u___cz_sn___ else None

            if k_____qh_h_z is not None and k_____qh_h_z.value is not None:

                self.w__c_rjwf_j_ = int.from_bytes(k_____qh_h_z.value[0:4], "little")


        i_z_i__b____ = self.u___cz_sn___["3A420040"] if "3A420040" in self.u___cz_sn___ else None

        if i_z_i__b____ is not None and i_z_i__b____.value is not None:

            _g_q______x_ = int.from_bytes(i_z_i__b____.value[0: 4], "little")
            sw__ff__jl__ = int.from_bytes(i_z_i__b____.value[4: 8], "little")

            if sw__ff__jl__ > 0:
                i_x____hz_to = _g_q______x_ + (sw__ff__jl__ << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)     

                try:    
                    self.f___v_bof__x = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.f___v_bof__x = Message._j__y____u__(self.f___v_bof__x)
                except:
                    pass 


        k_yxw____cl_ = self.u___cz_sn___["3A58" + self.q_rcyqzvz___] if "3A58" + self.q_rcyqzvz___ in self.u___cz_sn___ else None

        if k_yxw____cl_ is not None and k_yxw____cl_.value is not None:

            __a__ia_e__d = int(k_yxw____cl_.size / 4)

            self.__c__cw_h__a = []

            for i in range(__a__ia_e__d):

                __ie_wy_lv__ = "__substg1.0_3A58" + self.q_rcyqzvz___ + "-" + str.format("{:08X}", i)

                j___a_x_____ = ___g__on___b.get_entry(__ie_wy_lv__)

                if j___a_x_____ is not None and j___a_x_____.buffer is not None:

                    __mte_lzor_t = j___a_x_____.buffer[0: len(j___a_x_____.buffer) - mkkh___d_lvf].decode(self._gm_g__n___a)
                    self.__c__cw_h__a.append(__mte_lzor_t)


        _z_auh___r_f = self.u___cz_sn___["3A410040"] if "3A410040" in self.u___cz_sn___ else None

        if _z_auh___r_f is not None and _z_auh___r_f.value is not None:

            _ay__dy___q_ = int.from_bytes(_z_auh___r_f.value[0: 4], "little")
            on_i___h___r = int.from_bytes(_z_auh___r_f.value[4: 8], "little")

            if on_i___h___r > 0:
                i_x____hz_to = _ay__dy___q_ + (on_i___h___r << 32)
                j____h_x_v_h = datetime.datetime(1601,1,1)   

                try:    
                    self.u_u_t_ci___p = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                    self.u_u_t_ci___p = Message._j__y____u__(self.u_u_t_ci___p)
                except:
                    pass 

        v_f___la_el_ = self.u___cz_sn___["3A4D0002"] if "3A4D0002" in self.u___cz_sn___ else None

        if v_f___la_el_ is not None and v_f___la_el_.value is not None:

            d_yw_f_n_km_ = int.from_bytes(v_f___la_el_.value[0:4], "little")

            self.bw____sz____ = EnumUtil.parse_gender(d_yw_f_n_km_)


        _kt_i_f___j_ = 0x8022
        __gw______j_ = StandardPropertySet.ADDRESS

        s__ih_z_s___ = Message.t_z__y_g_o__(_kt_i_f___j_, __gw______j_)

        if _u__j__z_s__ is not None and s__ih_z_s___ in _u__j__z_s__ and _u__j__z_s__[s__ih_z_s___] is not None:
            
            _ga_zj___z__ = _u__j__z_s__[s__ih_z_s___]
            _ga_zj___z__ = _ga_zj___z__ + "0003"

            w_____lw___n = self.u___cz_sn___[_ga_zj___z__] if _ga_zj___z__ in self.u___cz_sn___ else None

            if w_____lw___n is not None and w_____lw___n.value is not None:

                _cj_____bw__ = int.from_bytes(w_____lw___n.value[0:4], "little")

                self._hle_ua_z__g = EnumUtil.parse_selected_mailing_address(_cj_____bw__)


        zo___sese___ = 0x8015
        __rnojp_lr__ = StandardPropertySet.ADDRESS

        y________iw_ = Message.t_z__y_g_o__(zo___sese___, __rnojp_lr__)

        if _u__j__z_s__ is not None and y________iw_ in _u__j__z_s__ and _u__j__z_s__[y________iw_] is not None:
            
            _ui__szqbmx_ = _u__j__z_s__[y________iw_]
            _ui__szqbmx_ = _ui__szqbmx_ + "000B"

            g_q_w_o_fz__ = self.u___cz_sn___[_ui__szqbmx_] if _ui__szqbmx_ in self.u___cz_sn___ else None

            if g_q_w_o_fz__ is not None and g_q_w_o_fz__.value is not None:

                lg_vorfx___o = int.from_bytes(g_q_w_o_fz__.value[0:2], "little")

                if lg_vorfx___o > 0:
                    self.____e_n__hf_ = True

        _mhn_s__xnqp = 0x8005
        __u____z__tb = StandardPropertySet.ADDRESS

        _________l__ = Message.t_z__y_g_o__(_mhn_s__xnqp, __u____z__tb)

        if _u__j__z_s__ is not None and _________l__ in _u__j__z_s__ and _u__j__z_s__[_________l__] is not None:
            
            r___kc___yv_ = _u__j__z_s__[_________l__]
            r___kc___yv_ = r___kc___yv_ + self._e_p_wn___m_

            ______ok_d__ = self.u___cz_sn___[r___kc___yv_] if r___kc___yv_ in self.u___cz_sn___ else None

            if ______ok_d__ is not None and ______ok_d__.value is not None:

                self.__el_ca_i_l_ = ______ok_d__.value.decode(self._gm_g__n___a)


        _ik_m_jhtev_ = 0x8062
        _ox____l__rm = StandardPropertySet.ADDRESS

        z_kgq__ar_l_ = Message.t_z__y_g_o__(_ik_m_jhtev_, _ox____l__rm)

        if _u__j__z_s__ is not None and z_kgq__ar_l_ in _u__j__z_s__ and _u__j__z_s__[z_kgq__ar_l_] is not None:
            
            zz_z_l_q__zf = _u__j__z_s__[z_kgq__ar_l_]
            zz_z_l_q__zf = zz_z_l_q__zf + self._e_p_wn___m_

            q__dv_t_____ = self.u___cz_sn___[zz_z_l_q__zf] if zz_z_l_q__zf in self.u___cz_sn___ else None

            if q__dv_t_____ is not None and q__dv_t_____.value is not None:

                self.___w___f___x = q__dv_t_____.value.decode(self._gm_g__n___a)


        c_ke________ = 0x80D8
        ________y_em = StandardPropertySet.ADDRESS

        _e__kg_x__y_ = Message.t_z__y_g_o__(c_ke________, ________y_em)

        if _u__j__z_s__ is not None and _e__kg_x__y_ in _u__j__z_s__ and _u__j__z_s__[_e__kg_x__y_] is not None:
            
            _lebej_h_v__ = _u__j__z_s__[_e__kg_x__y_]
            _lebej_h_v__ = _lebej_h_v__ + self._e_p_wn___m_

            u__xqhqk__j_ = self.u___cz_sn___[_lebej_h_v__] if _lebej_h_v__ in self.u___cz_sn___ else None

            if u__xqhqk__j_ is not None and u__xqhqk__j_.value is not None:

                self.l_a_g_kx____ = u__xqhqk__j_.value.decode(self._gm_g__n___a)


        _z_vu____mcp = 0x801B
        _ctt__i_x__c = StandardPropertySet.ADDRESS

        __lxahtzw_y_ = Message.t_z__y_g_o__(_z_vu____mcp, _ctt__i_x__c)

        if _u__j__z_s__ is not None and __lxahtzw_y_ in _u__j__z_s__ and _u__j__z_s__[__lxahtzw_y_] is not None:
            
            _jr_y__o_tvg = _u__j__z_s__[__lxahtzw_y_]
            _jr_y__o_tvg = _jr_y__o_tvg + self._e_p_wn___m_

            _y_wz_dnrk__ = self.u___cz_sn___[_jr_y__o_tvg] if _jr_y__o_tvg in self.u___cz_sn___ else None

            if _y_wz_dnrk__ is not None and _y_wz_dnrk__.value is not None:

                self.g___cd_p_do_ = _y_wz_dnrk__.value.decode(self._gm_g__n___a)


        __uzs__hl_fu = 0x8045
        ebz__b__o___ = StandardPropertySet.ADDRESS

        ________pajt = Message.t_z__y_g_o__(__uzs__hl_fu, ebz__b__o___)

        if _u__j__z_s__ is not None and ________pajt in _u__j__z_s__ and _u__j__z_s__[________pajt] is not None:
            
            __aj____g__s = _u__j__z_s__[________pajt]
            __aj____g__s = __aj____g__s + self._e_p_wn___m_

            _xuh_ih__o__ = self.u___cz_sn___[__aj____g__s] if __aj____g__s in self.u___cz_sn___ else None

            if _xuh_ih__o__ is not None and _xuh_ih__o__.value is not None:

                self.gs_m_____l__ = _xuh_ih__o__.value.decode(self._gm_g__n___a)


        n___h__s_iv_ = 0x8046
        aa_jvca___p_ = StandardPropertySet.ADDRESS

        wd_k_uh_____ = Message.t_z__y_g_o__(n___h__s_iv_, aa_jvca___p_)

        if _u__j__z_s__ is not None and wd_k_uh_____ in _u__j__z_s__ and _u__j__z_s__[wd_k_uh_____] is not None:
            
            c______ll__x = _u__j__z_s__[wd_k_uh_____]
            c______ll__x = c______ll__x + self._e_p_wn___m_

            _m_f_fv_zf_s = self.u___cz_sn___[c______ll__x] if c______ll__x in self.u___cz_sn___ else None

            if _m_f_fv_zf_s is not None and _m_f_fv_zf_s.value is not None:

                self.lp_y_____s__ = _m_f_fv_zf_s.value.decode(self._gm_g__n___a)


        ____j_me__ux = 0x8047
        w_peixpbgr_t = StandardPropertySet.ADDRESS

        ___j_qjzoplp = Message.t_z__y_g_o__(____j_me__ux, w_peixpbgr_t)

        if _u__j__z_s__ is not None and ___j_qjzoplp in _u__j__z_s__ and _u__j__z_s__[___j_qjzoplp] is not None:
            
            rij_nji__l_f = _u__j__z_s__[___j_qjzoplp]
            rij_nji__l_f = rij_nji__l_f + self._e_p_wn___m_

            qefwn___cesi = self.u___cz_sn___[rij_nji__l_f] if rij_nji__l_f in self.u___cz_sn___ else None

            if qefwn___cesi is not None and qefwn___cesi.value is not None:

                self.sba__qjh___k = qefwn___cesi.value.decode(self._gm_g__n___a)


        _____zs____e = 0x8048
        ______tkmehb = StandardPropertySet.ADDRESS

        uce____aj_h_ = Message.t_z__y_g_o__(_____zs____e, ______tkmehb)

        if _u__j__z_s__ is not None and uce____aj_h_ in _u__j__z_s__ and _u__j__z_s__[uce____aj_h_] is not None:
            
            u___r__urh__ = _u__j__z_s__[uce____aj_h_]
            u___r__urh__ = u___r__urh__ + self._e_p_wn___m_

            y_syd_j__kbs = self.u___cz_sn___[u___r__urh__] if u___r__urh__ in self.u___cz_sn___ else None

            if y_syd_j__kbs is not None and y_syd_j__kbs.value is not None:

                self.b_xkfy_m__v_ = y_syd_j__kbs.value.decode(self._gm_g__n___a)


        _ljgtyi_jkme = 0x8049
        z___zu___tmp = StandardPropertySet.ADDRESS

        ky__e__x_tm_ = Message.t_z__y_g_o__(_ljgtyi_jkme, z___zu___tmp)

        if _u__j__z_s__ is not None and ky__e__x_tm_ in _u__j__z_s__ and _u__j__z_s__[ky__e__x_tm_] is not None:
            
            f__h_snd_ls_ = _u__j__z_s__[ky__e__x_tm_]
            f__h_snd_ls_ = f__h_snd_ls_ + self._e_p_wn___m_

            __fp_j__ht__ = self.u___cz_sn___[f__h_snd_ls_] if f__h_snd_ls_ in self.u___cz_sn___ else None

            if __fp_j__ht__ is not None and __fp_j__ht__.value is not None:

                self._e___sik_flm = __fp_j__ht__.value.decode(self._gm_g__n___a)


        _e_v__r__f__ = 0x801A
        _d_skcm__f_i = StandardPropertySet.ADDRESS

        ____xeas___c = Message.t_z__y_g_o__(_e_v__r__f__, _d_skcm__f_i)

        if _u__j__z_s__ is not None and ____xeas___c in _u__j__z_s__ and _u__j__z_s__[____xeas___c] is not None:
            
            wy___e__mud_ = _u__j__z_s__[____xeas___c]
            wy___e__mud_ = wy___e__mud_ + self._e_p_wn___m_

            ___xt_dd__m_ = self.u___cz_sn___[wy___e__mud_] if wy___e__mud_ in self.u___cz_sn___ else None

            if ___xt_dd__m_ is not None and ___xt_dd__m_.value is not None:

                self.q_j______u_u = ___xt_dd__m_.value.decode(self._gm_g__n___a)


        d_av_bsv____ = 0x801C
        ___x_______p = StandardPropertySet.ADDRESS

        _q_p__na____ = Message.t_z__y_g_o__(d_av_bsv____, ___x_______p)

        if _u__j__z_s__ is not None and _q_p__na____ in _u__j__z_s__ and _u__j__z_s__[_q_p__na____] is not None:
            
            ____g_x___ql = _u__j__z_s__[_q_p__na____]
            ____g_x___ql = ____g_x___ql + self._e_p_wn___m_

            dva___m____n = self.u___cz_sn___[____g_x___ql] if ____g_x___ql in self.u___cz_sn___ else None

            if dva___m____n is not None and dva___m____n.value is not None:

                self._iwxsuk___iu = dva___m____n.value.decode(self._gm_g__n___a)


        _d_______c__ = 0x8083
        ___bza___h_h = StandardPropertySet.ADDRESS

        __ze_hmv___o = Message.t_z__y_g_o__(_d_______c__, ___bza___h_h)

        if _u__j__z_s__ is not None and __ze_hmv___o in _u__j__z_s__ and _u__j__z_s__[__ze_hmv___o] is not None:
            
            xf_v_dpyk___ = _u__j__z_s__[__ze_hmv___o]
            xf_v_dpyk___ = xf_v_dpyk___ + self._e_p_wn___m_

            h_yp______u_ = self.u___cz_sn___[xf_v_dpyk___] if xf_v_dpyk___ in self.u___cz_sn___ else None

            if h_yp______u_ is not None and h_yp______u_.value is not None:

                self._d_d___jg__u = h_yp______u_.value.decode(self._gm_g__n___a)


        b_g______nrd = 0x8093
        _sg_t__n__aj = StandardPropertySet.ADDRESS

        ____mubt__fr = Message.t_z__y_g_o__(b_g______nrd, _sg_t__n__aj)

        if _u__j__z_s__ is not None and ____mubt__fr in _u__j__z_s__ and _u__j__z_s__[____mubt__fr] is not None:
            
            _fa_juzu__c_ = _u__j__z_s__[____mubt__fr]
            _fa_juzu__c_ = _fa_juzu__c_ + self._e_p_wn___m_

            e__s_q_b_bb_ = self.u___cz_sn___[_fa_juzu__c_] if _fa_juzu__c_ in self.u___cz_sn___ else None

            if e__s_q_b_bb_ is not None and e__s_q_b_bb_.value is not None:

                self.c_x_q___hzc_ = e__s_q_b_bb_.value.decode(self._gm_g__n___a)


        w__a___k____ = 0x80A3
        __wfx_t__vvf = StandardPropertySet.ADDRESS

        d_n_____wro_ = Message.t_z__y_g_o__(w__a___k____, __wfx_t__vvf)

        if _u__j__z_s__ is not None and d_n_____wro_ in _u__j__z_s__ and _u__j__z_s__[d_n_____wro_] is not None:
            
            __a_kbmg_ba_ = _u__j__z_s__[d_n_____wro_]
            __a_kbmg_ba_ = __a_kbmg_ba_ + self._e_p_wn___m_

            h_vh__fg____ = self.u___cz_sn___[__a_kbmg_ba_] if __a_kbmg_ba_ in self.u___cz_sn___ else None

            if h_vh__fg____ is not None and h_vh__fg____.value is not None:

                self._c_dcu_np_f_ = h_vh__fg____.value.decode(self._gm_g__n___a)


        __zg_p_g__o_ = 0x8084
        d_hlenaj____ = StandardPropertySet.ADDRESS

        zn_qo_t_w___ = Message.t_z__y_g_o__(__zg_p_g__o_, d_hlenaj____)

        if _u__j__z_s__ is not None and zn_qo_t_w___ in _u__j__z_s__ and _u__j__z_s__[zn_qo_t_w___] is not None:
            
            zkg_i____b_j = _u__j__z_s__[zn_qo_t_w___]
            zkg_i____b_j = zkg_i____b_j + self._e_p_wn___m_

            o_dp_qdxj__i = self.u___cz_sn___[zkg_i____b_j] if zkg_i____b_j in self.u___cz_sn___ else None

            if o_dp_qdxj__i is not None and o_dp_qdxj__i.value is not None:

                self._y_g__fjv_r_ = o_dp_qdxj__i.value.decode(self._gm_g__n___a)


        _r__________ = 0x8094
        ln_g__u__is_ = StandardPropertySet.ADDRESS

        uh____z_l_u_ = Message.t_z__y_g_o__(_r__________, ln_g__u__is_)

        if _u__j__z_s__ is not None and uh____z_l_u_ in _u__j__z_s__ and _u__j__z_s__[uh____z_l_u_] is not None:
            
            _n___i____w_ = _u__j__z_s__[uh____z_l_u_]
            _n___i____w_ = _n___i____w_ + self._e_p_wn___m_

            n__bvv_____p = self.u___cz_sn___[_n___i____w_] if _n___i____w_ in self.u___cz_sn___ else None

            if n__bvv_____p is not None and n__bvv_____p.value is not None:

                self.____e____jg_ = n__bvv_____p.value.decode(self._gm_g__n___a)


        __c_i_a___wc = 0x80A4
        _t__fe_h_xk_ = StandardPropertySet.ADDRESS

        __s__fsjlm__ = Message.t_z__y_g_o__(__c_i_a___wc, _t__fe_h_xk_)

        if _u__j__z_s__ is not None and __s__fsjlm__ in _u__j__z_s__ and _u__j__z_s__[__s__fsjlm__] is not None:
            
            z__ka___q__y = _u__j__z_s__[__s__fsjlm__]
            z__ka___q__y = z__ka___q__y + self._e_p_wn___m_

            lu_og_bg_yla = self.u___cz_sn___[z__ka___q__y] if z__ka___q__y in self.u___cz_sn___ else None

            if lu_og_bg_yla is not None and lu_og_bg_yla.value is not None:

                self.go___g_____l = lu_og_bg_yla.value.decode(self._gm_g__n___a)


        ___j_e_t_sob = 0x8080
        f__y____q_xz = StandardPropertySet.ADDRESS

        ____ji_f____ = Message.t_z__y_g_o__(___j_e_t_sob, f__y____q_xz)

        if _u__j__z_s__ is not None and ____ji_f____ in _u__j__z_s__ and _u__j__z_s__[____ji_f____] is not None:
            
            _____c___i_d = _u__j__z_s__[____ji_f____]
            _____c___i_d = _____c___i_d + self._e_p_wn___m_

            ____uawac___ = self.u___cz_sn___[_____c___i_d] if _____c___i_d in self.u___cz_sn___ else None

            if ____uawac___ is not None and ____uawac___.value is not None:

                self.ypp___r__q__ = ____uawac___.value.decode(self._gm_g__n___a)


        m___r_liy_za = 0x8090
        vx______c___ = StandardPropertySet.ADDRESS

        _u___o__k__q = Message.t_z__y_g_o__(m___r_liy_za, vx______c___)

        if _u__j__z_s__ is not None and _u___o__k__q in _u__j__z_s__ and _u__j__z_s__[_u___o__k__q] is not None:
            
            _lkszl_z___l = _u__j__z_s__[_u___o__k__q]
            _lkszl_z___l = _lkszl_z___l + self._e_p_wn___m_

            fscf____r___ = self.u___cz_sn___[_lkszl_z___l] if _lkszl_z___l in self.u___cz_sn___ else None

            if fscf____r___ is not None and fscf____r___.value is not None:

                self.q_vxh_uz___i = fscf____r___.value.decode(self._gm_g__n___a)


        x_r_e__bubk_ = 0x80A0
        a__s_____d__ = StandardPropertySet.ADDRESS

        _xd___ip____ = Message.t_z__y_g_o__(x_r_e__bubk_, a__s_____d__)

        if _u__j__z_s__ is not None and _xd___ip____ in _u__j__z_s__ and _u__j__z_s__[_xd___ip____] is not None:
            
            zt_sqc__s___ = _u__j__z_s__[_xd___ip____]
            zt_sqc__s___ = zt_sqc__s___ + self._e_p_wn___m_

            b__el__q_u_a = self.u___cz_sn___[zt_sqc__s___] if zt_sqc__s___ in self.u___cz_sn___ else None

            if b__el__q_u_a is not None and b__el__q_u_a.value is not None:

                self.qw__y_l__p__ = b__el__q_u_a.value.decode(self._gm_g__n___a)


        s_aws_f____x = 0x8082
        _wo_a_k____m = StandardPropertySet.ADDRESS

        ____b___m_mp = Message.t_z__y_g_o__(s_aws_f____x, _wo_a_k____m)

        if _u__j__z_s__ is not None and ____b___m_mp in _u__j__z_s__ and _u__j__z_s__[____b___m_mp] is not None:
            
            ___i_j___ir_ = _u__j__z_s__[____b___m_mp]
            ___i_j___ir_ = ___i_j___ir_ + self._e_p_wn___m_

            __n__tt_r___ = self.u___cz_sn___[___i_j___ir_] if ___i_j___ir_ in self.u___cz_sn___ else None

            if __n__tt_r___ is not None and __n__tt_r___.value is not None:

                self._a___u____sj = __n__tt_r___.value.decode(self._gm_g__n___a)


        _qft____f_vn = 0x8092
        __l____ald__ = StandardPropertySet.ADDRESS

        _h_j_a___o_t = Message.t_z__y_g_o__(_qft____f_vn, __l____ald__)

        if _u__j__z_s__ is not None and _h_j_a___o_t in _u__j__z_s__ and _u__j__z_s__[_h_j_a___o_t] is not None:
            
            __l_a__a__jd = _u__j__z_s__[_h_j_a___o_t]
            __l_a__a__jd = __l_a__a__jd + self._e_p_wn___m_

            _t_w_o__gj_v = self.u___cz_sn___[__l_a__a__jd] if __l_a__a__jd in self.u___cz_sn___ else None

            if _t_w_o__gj_v is not None and _t_w_o__gj_v.value is not None:

                self.v__kpwt___jh = _t_w_o__gj_v.value.decode(self._gm_g__n___a)


        n_etdlxh_a_f = 0x80A2
        k___p_____l_ = StandardPropertySet.ADDRESS

        __do_f_b__sf = Message.t_z__y_g_o__(n_etdlxh_a_f, k___p_____l_)

        if _u__j__z_s__ is not None and __do_f_b__sf in _u__j__z_s__ and _u__j__z_s__[__do_f_b__sf] is not None:
            
            _____oz_jdue = _u__j__z_s__[__do_f_b__sf]
            _____oz_jdue = _____oz_jdue + self._e_p_wn___m_

            dqrw_u_kyk_s = self.u___cz_sn___[_____oz_jdue] if _____oz_jdue in self.u___cz_sn___ else None

            if dqrw_u_kyk_s is not None and dqrw_u_kyk_s.value is not None:

                self.v_rn_m______ = dqrw_u_kyk_s.value.decode(self._gm_g__n___a)   


        xw___h___gth = 0x8085
        b__xctlp_jdq = StandardPropertySet.ADDRESS

        _o_e__zline_ = Message.t_z__y_g_o__(xw___h___gth, b__xctlp_jdq)

        if _u__j__z_s__ is not None and _o_e__zline_ in _u__j__z_s__ and _u__j__z_s__[_o_e__zline_] is not None:
            
            __pr_q___s__ = _u__j__z_s__[_o_e__zline_]
            __pr_q___s__ = __pr_q___s__ + self._e_p_wn___m_

            _x_mfumxoz_o = self.u___cz_sn___[__pr_q___s__] if __pr_q___s__ in self.u___cz_sn___ else None

            if _x_mfumxoz_o is not None and _x_mfumxoz_o.value is not None:

                self.kiork_z_o__p = _x_mfumxoz_o.value.decode(self._gm_g__n___a)


        f_dhzzc___tp = 0x8095
        lbl_gw__k_rr = StandardPropertySet.ADDRESS

        _h__t_o_r__a = Message.t_z__y_g_o__(f_dhzzc___tp, lbl_gw__k_rr)

        if _u__j__z_s__ is not None and _h__t_o_r__a in _u__j__z_s__ and _u__j__z_s__[_h__t_o_r__a] is not None:
            
            ___aa___ll_d = _u__j__z_s__[_h__t_o_r__a]
            ___aa___ll_d = ___aa___ll_d + self._e_p_wn___m_

            p_y_v_____fx = self.u___cz_sn___[___aa___ll_d] if ___aa___ll_d in self.u___cz_sn___ else None

            if p_y_v_____fx is not None and p_y_v_____fx.value is not None:

                self.n_dl_t_l____ = p_y_v_____fx.value.decode(self._gm_g__n___a)


        _________b_e = 0x80A5
        _______jf_ix = StandardPropertySet.ADDRESS

        zepq_w_ij___ = Message.t_z__y_g_o__(_________b_e, _______jf_ix)

        if _u__j__z_s__ is not None and zepq_w_ij___ in _u__j__z_s__ and _u__j__z_s__[zepq_w_ij___] is not None:
            
            _qciodsw__q_ = _u__j__z_s__[zepq_w_ij___]
            _qciodsw__q_ = _qciodsw__q_ + self._e_p_wn___m_

            udo___e_j_cg = self.u___cz_sn___[_qciodsw__q_] if _qciodsw__q_ in self.u___cz_sn___ else None

            if udo___e_j_cg is not None and udo___e_j_cg.value is not None:

                self.____cve____g = udo___e_j_cg.value.decode(self._gm_g__n___a)  


        for e in range(len(self._r__n__wc_bq)):
            
            c_sds_____e_ = None

            if isinstance(self._r__n__wc_bq[e].tag, ExtendedPropertyId):
                l_nvq_ia___o = self._r__n__wc_bq[e].tag
                c_sds_____e_ = Message.t_z__y_g_o__(l_nvq_ia___o.id, l_nvq_ia___o.guid)

            else:
                l_nvq_ia___o = self._r__n__wc_bq[e].tag
                c_sds_____e_ = Message.t_z__y_g_o__(l_nvq_ia___o.name, l_nvq_ia___o.guid)
            
            if _u__j__z_s__ is not None and c_sds_____e_ in _u__j__z_s__ and _u__j__z_s__[c_sds_____e_] is not None:

                ar__gs_s___a = _u__j__z_s__[c_sds_____e_]

                for kj_r_t_ri_x_ in self.u___cz_sn___:

                    if kj_r_t_ri_x_.startswith(ar__gs_s___a):

                        w___pj_kb__e = self.u___cz_sn___[kj_r_t_ri_x_]

                        self._r__n__wc_bq[e].tag.type = w___pj_kb__e.type

                        if self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_BINARY:

                            ar__gs_s___a = ar__gs_s___a + "1102"

                            if w___pj_kb__e is not None and w___pj_kb__e.value is not None:

                                w_m_w__h___n = int(w___pj_kb__e.size / 8)

                                _c_dsqr____d = []

                                for i in range(w_m_w__h___n):

                                    __ie_wy_lv__ = "__substg1.0_" + ar__gs_s___a + "-" + str.format("{:08X}", i)

                                    j___a_x_____ = ___g__on___b.get_entry(__ie_wy_lv__)

                                    if j___a_x_____ is not None and j___a_x_____.buffer is not None:
                                        _c_dsqr____d.append(j___a_x_____.buffer)

                                if len(_c_dsqr____d) > 0:

                                    eynjn_yv_lq_ = bytearray()

                                    x_f__uf_ldn_ = int.to_bytes(len(_c_dsqr____d), 4, "little")
                                    eynjn_yv_lq_ += x_f__uf_ldn_

                                    ____m_fe__fr = 0

                                    for i in range(len(_c_dsqr____d)):

                                        __o_yqq_m_og = _c_dsqr____d[i]
                                        _hm_x___pb_t = int.to_bytes(4 + len(_c_dsqr____d) * 4 + ____m_fe__fr, 4, "little")
                                        eynjn_yv_lq_ += _hm_x___pb_t

                                        ____m_fe__fr += len(__o_yqq_m_og)
                  
                                    for i in range(len(_c_dsqr____d)):

                                        __o_yqq_m_og = _c_dsqr____d[i]
                                        eynjn_yv_lq_ += __o_yqq_m_og
                  
                                    self._r__n__wc_bq[e].value = bytes(eynjn_yv_lq_)

                        else:
                            self._r__n__wc_bq[e].value = w___pj_kb__e.value


        hx_sji__ibte = ___g__on___b.get_entry("__substg1.0_001A" + self._e_p_wn___m_)
        j______vi_ad = ___g__on___b.get_entry("__substg1.0_0037" + self._e_p_wn___m_)
        ___zwn__fwe_ = ___g__on___b.get_entry("__substg1.0_003D" + self._e_p_wn___m_)
        ____c__ufir_ = ___g__on___b.get_entry("__substg1.0_0070" + self._e_p_wn___m_)
        ___oxquhgjr_ = ___g__on___b.get_entry("__substg1.0_0E02" + self._e_p_wn___m_)
        j_lk_h__c__a = ___g__on___b.get_entry("__substg1.0_0E03" + self._e_p_wn___m_)
        _w_v_j_h_lex = ___g__on___b.get_entry("__substg1.0_0E04" + self._e_p_wn___m_)
        __n_x_rpwstp = ___g__on___b.get_entry("__substg1.0_0074" + self._e_p_wn___m_)
        __zp___t____ = ___g__on___b.get_entry("__substg1.0_0050" + self._e_p_wn___m_)
        a_m_i__b__q_ = ___g__on___b.get_entry("__substg1.0_0E1D" + self._e_p_wn___m_)
        __qpng__up__ = ___g__on___b.get_entry("__substg1.0_1000" + self._e_p_wn___m_)
        _z_i__ta__g_ = ___g__on___b.get_entry("__substg1.0_10090102")
        ____cg______ = ___g__on___b.get_entry("__substg1.0_300B0102")
        _plxm___ts_l = ___g__on___b.get_entry("__substg1.0_65E20102")
        _______zt_ct = ___g__on___b.get_entry("__substg1.0_0FFF0102")
        l__r___n___t = ___g__on___b.get_entry("__substg1.0_00460102")
        _____p__r__s = ___g__on___b.get_entry("__substg1.0_00530102")
        ztbcqksg____ = ___g__on___b.get_entry("__substg1.0_1001" + self._e_p_wn___m_)
        _csi_y______ = ___g__on___b.get_entry("__substg1.0_3FF8" + self._e_p_wn___m_)
        _xs__l__x_bl = ___g__on___b.get_entry("__substg1.0_3FFA" + self._e_p_wn___m_)
        _f_bsa_d__j_ = ___g__on___b.get_entry("__substg1.0_1035" + self._e_p_wn___m_)
        e___a_p_____ = ___g__on___b.get_entry("__substg1.0_1042" + self._e_p_wn___m_)
        ___f_k_q_oqd = ___g__on___b.get_entry("__substg1.0_1039" + self._e_p_wn___m_)
        i___jsjb____ = ___g__on___b.get_entry("__substg1.0_00710102")
        ___of__j_m__ = ___g__on___b.get_entry("__substg1.0_10130102")
        _ov_nty_fl__ = ___g__on___b.get_entry("__substg1.0_1013" + self._e_p_wn___m_)
        _b___ud_so_t = ___g__on___b.get_entry("__substg1.0_0077" + self._e_p_wn___m_)
        __t_d_s___j_ = ___g__on___b.get_entry("__substg1.0_0078" + self._e_p_wn___m_)
        ___v_wvp_s_r = ___g__on___b.get_entry("__substg1.0_00430102")
        bd_sy_fq___c = ___g__on___b.get_entry("__substg1.0_0044" + self._e_p_wn___m_)
        gyrot_q__n__ = ___g__on___b.get_entry("__substg1.0_00520102")
        _x__u____f__ = ___g__on___b.get_entry("__substg1.0_0075" + self._e_p_wn___m_)
        c____uy__b_h = ___g__on___b.get_entry("__substg1.0_0076" + self._e_p_wn___m_)
        _____k____a_ = ___g__on___b.get_entry("__substg1.0_003F0102")
        i_j___zaxcvd = ___g__on___b.get_entry("__substg1.0_0040" + self._e_p_wn___m_)
        o__rdj_vwcu_ = ___g__on___b.get_entry("__substg1.0_00510102")
        _y______dkq_ = ___g__on___b.get_entry("__substg1.0_0C1E" + self._e_p_wn___m_)
        qqm___s__o__ = ___g__on___b.get_entry("__substg1.0_0C1F" + self._e_p_wn___m_)
        d__tf_f_u_n_ = ___g__on___b.get_entry("__substg1.0_5D01" + self._e_p_wn___m_)
        _il_u_iv__sx = ___g__on___b.get_entry("__substg1.0_0C190102")
        gnmw__te_j__ = ___g__on___b.get_entry("__substg1.0_0C1A" + self._e_p_wn___m_)
        _mr_ve__r___ = ___g__on___b.get_entry("__substg1.0_0C1D0102")
        _i_g__t_n_e_ = ___g__on___b.get_entry("__substg1.0_0064" + self._e_p_wn___m_)
        __qy_i__izcp = ___g__on___b.get_entry("__substg1.0_0065" + self._e_p_wn___m_)
        qa_g_ac_rprm = ___g__on___b.get_entry("__substg1.0_5D02" + self._e_p_wn___m_)
        g________iji = ___g__on___b.get_entry("__substg1.0_00410102")
        _sz____q____ = ___g__on___b.get_entry("__substg1.0_0042" + self._e_p_wn___m_)
        _z_vnxvx_nys = ___g__on___b.get_entry("__substg1.0_003B0102")
        vhf____ua_g_ = ___g__on___b.get_entry("__substg1.0_007D" + self._e_p_wn___m_)
        fly__qyfl___ = ___g__on___b.get_entry("__substg1.0_3A30" + self._e_p_wn___m_)
        __b___h__p__ = ___g__on___b.get_entry("__substg1.0_3A2E" + self._e_p_wn___m_)
        ___n____v__j = ___g__on___b.get_entry("__substg1.0_3A1B" + self._e_p_wn___m_)
        __hk_d___bu_ = ___g__on___b.get_entry("__substg1.0_3A24" + self._e_p_wn___m_)
        _h_r_______u = ___g__on___b.get_entry("__substg1.0_3A51" + self._e_p_wn___m_)
        ct__nx_o___d = ___g__on___b.get_entry("__substg1.0_3A02" + self._e_p_wn___m_)
        _dlkj_a_s___ = ___g__on___b.get_entry("__substg1.0_3A1E" + self._e_p_wn___m_)
        _g__i__f____ = ___g__on___b.get_entry("__substg1.0_3A1C" + self._e_p_wn___m_)
        aeptc_r___r_ = ___g__on___b.get_entry("__substg1.0_3A57" + self._e_p_wn___m_)
        cc_lrr__z__j = ___g__on___b.get_entry("__substg1.0_3A16" + self._e_p_wn___m_)
        _e_xr____b__ = ___g__on___b.get_entry("__substg1.0_3A49" + self._e_p_wn___m_)
        _______vxjiu = ___g__on___b.get_entry("__substg1.0_3A4A" + self._e_p_wn___m_)
        ____c__l__ua = ___g__on___b.get_entry("__substg1.0_3A18" + self._e_p_wn___m_)
        _c___rn__r__ = ___g__on___b.get_entry("__substg1.0_3001" + self._e_p_wn___m_)
        tx_n__j_l___ = ___g__on___b.get_entry("__substg1.0_3A45" + self._e_p_wn___m_)
        l_i_____gyer = ___g__on___b.get_entry("__substg1.0_3A4C" + self._e_p_wn___m_)
        ____tl_kk_hv = ___g__on___b.get_entry("__substg1.0_3A05" + self._e_p_wn___m_)
        i__g_u_mj__r = ___g__on___b.get_entry("__substg1.0_3A06" + self._e_p_wn___m_)
        ea___b__lpkp = ___g__on___b.get_entry("__substg1.0_3A07" + self._e_p_wn___m_)
        __a__l__haq_ = ___g__on___b.get_entry("__substg1.0_3A43" + self._e_p_wn___m_)
        d__q_f_q__o_ = ___g__on___b.get_entry("__substg1.0_3A2F" + self._e_p_wn___m_)
        e___n_l_____ = ___g__on___b.get_entry("__substg1.0_3A59" + self._e_p_wn___m_)
        ____g_i__a_t = ___g__on___b.get_entry("__substg1.0_3A5A" + self._e_p_wn___m_)
        b_____n_i_kd = ___g__on___b.get_entry("__substg1.0_3A5B" + self._e_p_wn___m_)
        _r__azo_g_hk = ___g__on___b.get_entry("__substg1.0_3A5E" + self._e_p_wn___m_)
        ___e__unp__h = ___g__on___b.get_entry("__substg1.0_3A5C" + self._e_p_wn___m_)
        __qq_q__ov_v = ___g__on___b.get_entry("__substg1.0_3A5D" + self._e_p_wn___m_)
        bll__dx_y__x = ___g__on___b.get_entry("__substg1.0_3A25" + self._e_p_wn___m_)
        _zp____a____ = ___g__on___b.get_entry("__substg1.0_3A09" + self._e_p_wn___m_)
        kkt___a_d_mo = ___g__on___b.get_entry("__substg1.0_3A0A" + self._e_p_wn___m_)
        __u_vk_u_iit = ___g__on___b.get_entry("__substg1.0_3A2D" + self._e_p_wn___m_)
        ____gp___q__ = ___g__on___b.get_entry("__substg1.0_3A4E" + self._e_p_wn___m_)
        ndsvo__hpu__ = ___g__on___b.get_entry("__substg1.0_3A44" + self._e_p_wn___m_)
        x__td_fiu_h_ = ___g__on___b.get_entry("__substg1.0_3A4F" + self._e_p_wn___m_)
        ________n_ur = ___g__on___b.get_entry("__substg1.0_3A19" + self._e_p_wn___m_)
        _zrt_fatw_cw = ___g__on___b.get_entry("__substg1.0_3A08" + self._e_p_wn___m_)
        d_____o___ot = ___g__on___b.get_entry("__substg1.0_3A5F" + self._e_p_wn___m_)
        bt_a___k____ = ___g__on___b.get_entry("__substg1.0_3A60" + self._e_p_wn___m_)
        __q__zyb__x_ = ___g__on___b.get_entry("__substg1.0_3A61" + self._e_p_wn___m_)
        ___qc_s_k__r = ___g__on___b.get_entry("__substg1.0_3A62" + self._e_p_wn___m_)
        m___n___a_dp = ___g__on___b.get_entry("__substg1.0_3A63" + self._e_p_wn___m_)
        _o_a_a_f_cr_ = ___g__on___b.get_entry("__substg1.0_3A1F" + self._e_p_wn___m_)
        t____r_mnuta = ___g__on___b.get_entry("__substg1.0_3A21" + self._e_p_wn___m_)
        _b_rkr_x_wrq = ___g__on___b.get_entry("__substg1.0_3A50" + self._e_p_wn___m_)
        np_mxk_h_e_r = ___g__on___b.get_entry("__substg1.0_3A15" + self._e_p_wn___m_)
        __w_b_sbajoq = ___g__on___b.get_entry("__substg1.0_3A27" + self._e_p_wn___m_)
        ta____blht__ = ___g__on___b.get_entry("__substg1.0_3A26" + self._e_p_wn___m_)
        _oc_rkqwc___ = ___g__on___b.get_entry("__substg1.0_3A2A" + self._e_p_wn___m_)
        _____kd_y__i = ___g__on___b.get_entry("__substg1.0_3A2B" + self._e_p_wn___m_)
        rqh_dxoz_t__ = ___g__on___b.get_entry("__substg1.0_3A28" + self._e_p_wn___m_)
        ___g_i_i_u_j = ___g__on___b.get_entry("__substg1.0_3A29" + self._e_p_wn___m_)
        o_a_____tu__ = ___g__on___b.get_entry("__substg1.0_3A23" + self._e_p_wn___m_)
        m_e_r_j_fdrw = ___g__on___b.get_entry("__substg1.0_3A1A" + self._e_p_wn___m_)
        __y_u__ma_up = ___g__on___b.get_entry("__substg1.0_3A46" + self._e_p_wn___m_)
        _msvt___r_e_ = ___g__on___b.get_entry("__substg1.0_3A1D" + self._e_p_wn___m_)
        _____q__p_kb = ___g__on___b.get_entry("__substg1.0_3A48" + self._e_p_wn___m_)
        uwky_zfyjvmt = ___g__on___b.get_entry("__substg1.0_3A11" + self._e_p_wn___m_)
        z__v_v_r____ = ___g__on___b.get_entry("__substg1.0_3A2C" + self._e_p_wn___m_)
        z_b_____m__v = ___g__on___b.get_entry("__substg1.0_3A17" + self._e_p_wn___m_)
        dl___shau___ = ___g__on___b.get_entry("__substg1.0_3A4B" + self._e_p_wn___m_)


        if hx_sji__ibte is not None and hx_sji__ibte.buffer is not None:
            self.___t_lgsh__n = hx_sji__ibte.buffer.decode(self._gm_g__n___a)  

        if j______vi_ad  is not None and j______vi_ad .buffer is not None:
            self.b_t___b_q_xu = j______vi_ad.buffer.decode(self._gm_g__n___a)  

        if ___zwn__fwe_ is not None and ___zwn__fwe_.buffer is not None:
            self._______c__ty = ___zwn__fwe_.buffer.decode(self._gm_g__n___a)  

        if ____c__ufir_ is not None and ____c__ufir_.buffer is not None:
            self._s_k_n_jb___ = ____c__ufir_.buffer.decode(self._gm_g__n___a)  

        if ___oxquhgjr_ is not None and ___oxquhgjr_.buffer is not None:
            self.w__teeli____ = ___oxquhgjr_.buffer.decode(self._gm_g__n___a)  

        if j_lk_h__c__a is not None and j_lk_h__c__a.buffer is not None:
            self.qj_wgu_zzu_s = j_lk_h__c__a.buffer.decode(self._gm_g__n___a)  

        if _w_v_j_h_lex is not None and _w_v_j_h_lex.buffer is not None:
            self.qw_____z__u_ = _w_v_j_h_lex.buffer.decode(self._gm_g__n___a)  

        if __n_x_rpwstp is not None and __n_x_rpwstp.buffer is not None:
            self.p____t__w_g_ = __n_x_rpwstp.buffer.decode(self._gm_g__n___a)  

        if __zp___t____ is not None and __zp___t____.buffer is not None:
            self.cx_p_u___h_i = __zp___t____.buffer.decode(self._gm_g__n___a)  

        if a_m_i__b__q_ is not None and a_m_i__b__q_.buffer is not None:
            self.j__kfc___d_g = a_m_i__b__q_.buffer.decode(self._gm_g__n___a)  

        if __qpng__up__ is not None and __qpng__up__.buffer is not None:
            self.p__w___rx_bo = __qpng__up__.buffer.decode(self._gm_g__n___a) 

        if _z_i__ta__g_ is not None and _z_i__ta__g_.buffer is not None:
            self.i_f__lcbcp__ = _z_i__ta__g_.buffer

        if ____cg______ is not None and ____cg______.buffer is not None:
            self.kh_____k_y_g = ____cg______.buffer

        if _plxm___ts_l is not None and _plxm___ts_l.buffer is not None:
            self.__zr_cn_k__x = _plxm___ts_l.buffer

        if _______zt_ct is not None and _______zt_ct.buffer is not None:
            self._fz___ad_f__ = _______zt_ct.buffer

        if l__r___n___t is not None and l__r___n___t.buffer is not None:
            self.a_uk__ilatjb = l__r___n___t.buffer

        if _____p__r__s is not None and _____p__r__s.buffer is not None:
            self.____gw__e_a_ = _____p__r__s.buffer

        if ztbcqksg____ is not None and ztbcqksg____.buffer is not None:
            self.__okvntl__d_ = ztbcqksg____.buffer.decode(self._gm_g__n___a)  

        if _csi_y______ is not None and _csi_y______.buffer is not None:
            self.____l__er___ = _csi_y______.buffer.decode(self._gm_g__n___a)  

        if _xs__l__x_bl is not None and _xs__l__x_bl.buffer is not None:
            self.wo___yi_w__x = _xs__l__x_bl.buffer.decode(self._gm_g__n___a)  

        if _f_bsa_d__j_ is not None and _f_bsa_d__j_.buffer is not None:
            self._so__s_lu_o_ = _f_bsa_d__j_.buffer.decode(self._gm_g__n___a)  

        if e___a_p_____ is not None and e___a_p_____.buffer is not None:
            self.j_a_______a_ = e___a_p_____.buffer.decode(self._gm_g__n___a)  

        if ___f_k_q_oqd is not None and ___f_k_q_oqd.buffer is not None:
            self._r_h__rjorsu = ___f_k_q_oqd.buffer.decode(self._gm_g__n___a)  

        if i___jsjb____ is not None and i___jsjb____.buffer is not None:
            self.wto_g_dk_qpf = i___jsjb____.buffer

        if _______zt_ct is not None and _______zt_ct.buffer is not None:
            self._fz___ad_f__ = _______zt_ct.buffer

        if ___of__j_m__ is not None and ___of__j_m__.buffer is not None:
            self.j_ka_nrf____ = ___of__j_m__.buffer
        elif _ov_nty_fl__ is not None and _ov_nty_fl__.buffer is not None:
            
            if self.b_s_cu_d_ovr > 0:

                __ayiv___up_ = qb_s_dghkmbh(self.b_s_cu_d_ovr)

                _g___xd__irl = _ov_nty_fl__.buffer.decode(__ayiv___up_)
                self.j_ka_nrf____ = _g___xd__irl.decode(__ayiv___up_)

            else:
                _g___xd__irl = _ov_nty_fl__.buffer.decode(self.__z_oxrob_zv)
                self.j_ka_nrf____ = _g___xd__irl.decode(self.__z_oxrob_zv)


        if _b___ud_so_t is not None and _b___ud_so_t.buffer is not None:
            self._dn_pem__l__ = _b___ud_so_t.buffer.decode(self._gm_g__n___a) 

        if __t_d_s___j_ is not None and __t_d_s___j_.buffer is not None:
            self.li_leu_wgzg_ = __t_d_s___j_.buffer.decode(self._gm_g__n___a) 

        if ___v_wvp_s_r is not None and ___v_wvp_s_r.buffer is not None:
            self._vezy_n_ikln = ___v_wvp_s_r.buffer

        if bd_sy_fq___c is not None and bd_sy_fq___c.buffer is not None:
            self.q__q_k_r_cw_ = bd_sy_fq___c.buffer.decode(self._gm_g__n___a) 

        if gyrot_q__n__ is not None and gyrot_q__n__.buffer is not None:
            self.i_r___noho_c = gyrot_q__n__.buffer

        if _x__u____f__ is not None and _x__u____f__.buffer is not None:
            self._ze__u_auq__ = _x__u____f__.buffer.decode(self._gm_g__n___a) 

        if c____uy__b_h is not None and c____uy__b_h.buffer is not None:
            self.g__nj___m__u = c____uy__b_h.buffer.decode(self._gm_g__n___a) 

        if _____k____a_ is not None and _____k____a_.buffer is not None:
            self.k_l_bco_s_jv = _____k____a_.buffer

        if i_j___zaxcvd is not None and i_j___zaxcvd.buffer is not None:
            self.__xh_ve_____ = i_j___zaxcvd.buffer.decode(self._gm_g__n___a) 

        if o__rdj_vwcu_ is not None and o__rdj_vwcu_.buffer is not None:
            self.____uw__pp__ = o__rdj_vwcu_.buffer

        if _y______dkq_ is not None and _y______dkq_.buffer is not None:
            self.___onygff_yd = _y______dkq_.buffer.decode(self._gm_g__n___a) 

        if qqm___s__o__ is not None and qqm___s__o__.buffer is not None:
            self._p_y__of_ma_ = qqm___s__o__.buffer.decode(self._gm_g__n___a)

        if d__tf_f_u_n_ is not None and d__tf_f_u_n_.buffer is not None:
            self.p_k_wh_____c = d__tf_f_u_n_.buffer.decode(self._gm_g__n___a) 

        if _il_u_iv__sx is not None and _il_u_iv__sx.buffer is not None:
            self.___yu____xb_ = _il_u_iv__sx.buffer

        if gnmw__te_j__ is not None and gnmw__te_j__.buffer is not None:
            self.___xm__ne_t_ = gnmw__te_j__.buffer.decode(self._gm_g__n___a) 

        if _mr_ve__r___ is not None and _mr_ve__r___.buffer is not None:
            self.___s_iffiu__ = _mr_ve__r___.buffer

        if _i_g__t_n_e_ is not None and _i_g__t_n_e_.buffer is not None:
            self.__w_y_scz_u_ = _i_g__t_n_e_.buffer.decode(self._gm_g__n___a) 

        if __qy_i__izcp is not None and __qy_i__izcp.buffer is not None:
            self.______z_____ = __qy_i__izcp.buffer.decode(self._gm_g__n___a)

        if qa_g_ac_rprm is not None and qa_g_ac_rprm.buffer is not None:
            self.y______e___l = qa_g_ac_rprm.buffer.decode(self._gm_g__n___a) 

        if g________iji is not None and g________iji.buffer is not None:
            self.dqgxw_hnt__k = g________iji.buffer

        if _sz____q____ is not None and _sz____q____.buffer is not None:
            self._o_wcivl____ = _sz____q____.buffer.decode(self._gm_g__n___a) 

        if _z_vnxvx_nys is not None and _z_vnxvx_nys.buffer is not None:
            self.__dq___iif_g = _z_vnxvx_nys.buffer

        if vhf____ua_g_ is not None and vhf____ua_g_.buffer is not None:
            self.___i___cdtv_ = vhf____ua_g_.buffer.decode(self._gm_g__n___a) 

        if fly__qyfl___ is not None and fly__qyfl___.buffer is not None:
            self.__e__w_t_p_q = fly__qyfl___.buffer.decode(self._gm_g__n___a)

        if __b___h__p__ is not None and __b___h__p__.buffer is not None:
            self._f_ha_w___mw = __b___h__p__.buffer.decode(self._gm_g__n___a) 

        if ___n____v__j is not None and ___n____v__j.buffer is not None:
            self.hy_wucpf_c_j = ___n____v__j.buffer.decode(self._gm_g__n___a) 

        if __hk_d___bu_ is not None and __hk_d___bu_.buffer is not None:
            self._km___gfyym_ = __hk_d___bu_.buffer.decode(self._gm_g__n___a) 

        if _h_r_______u is not None and _h_r_______u.buffer is not None:
            self.hhk__zyd_d__ = _h_r_______u.buffer.decode(self._gm_g__n___a) 

        if ct__nx_o___d is not None and ct__nx_o___d.buffer is not None:
            self.bun___q__o__ = ct__nx_o___d.buffer.decode(self._gm_g__n___a) 

        if _dlkj_a_s___ is not None and _dlkj_a_s___.buffer is not None:
            self.___zpfq_tz__ = _dlkj_a_s___.buffer.decode(self._gm_g__n___a)

        if _g__i__f____ is not None and _g__i__f____.buffer is not None:
            self.__x_r_e_yh__ = _g__i__f____.buffer.decode(self._gm_g__n___a) 

        if aeptc_r___r_ is not None and aeptc_r___r_.buffer is not None:
            self.q_ob_____ij_ = aeptc_r___r_.buffer.decode(self._gm_g__n___a) 

        if cc_lrr__z__j is not None and cc_lrr__z__j.buffer is not None:
            self.__f_fqzb___i = cc_lrr__z__j.buffer.decode(self._gm_g__n___a) 

        if _e_xr____b__ is not None and _e_xr____b__.buffer is not None:
            self.y_b_h___p___ = _e_xr____b__.buffer.decode(self._gm_g__n___a) 

        if _______vxjiu is not None and _______vxjiu.buffer is not None:
            self.n____j____xe = _______vxjiu.buffer.decode(self._gm_g__n___a) 

        if ____c__l__ua is not None and ____c__l__ua.buffer is not None:
            self.___yr__bvg__ = ____c__l__ua.buffer.decode(self._gm_g__n___a)

        if _c___rn__r__ is not None and _c___rn__r__.buffer is not None:
            self.__jjr_pc__t_ = _c___rn__r__.buffer.decode(self._gm_g__n___a) 

        if tx_n__j_l___ is not None and tx_n__j_l___.buffer is not None:
            self.d_lurjyi___x = tx_n__j_l___.buffer.decode(self._gm_g__n___a) 

        if l_i_____gyer is not None and l_i_____gyer.buffer is not None:
            self.__jra_lp____ = l_i_____gyer.buffer.decode(self._gm_g__n___a) 

        if ____tl_kk_hv is not None and ____tl_kk_hv.buffer is not None:
            self.____iiu_h__i = ____tl_kk_hv.buffer.decode(self._gm_g__n___a) 

        if i__g_u_mj__r is not None and i__g_u_mj__r.buffer is not None:
            self._y______e___ = i__g_u_mj__r.buffer.decode(self._gm_g__n___a)

        if ea___b__lpkp is not None and ea___b__lpkp.buffer is not None:
            self.ol____d_r__y = ea___b__lpkp.buffer.decode(self._gm_g__n___a)

        if __a__l__haq_ is not None and __a__l__haq_.buffer is not None:
            self.__t_j_op_tt_ = __a__l__haq_.buffer.decode(self._gm_g__n___a) 

        if d__q_f_q__o_ is not None and d__q_f_q__o_.buffer is not None:
            self._m___i______ = d__q_f_q__o_.buffer.decode(self._gm_g__n___a) 

        if e___n_l_____ is not None and e___n_l_____.buffer is not None:
            self.z__b________ = e___n_l_____.buffer.decode(self._gm_g__n___a) 

        if ____g_i__a_t is not None and ____g_i__a_t.buffer is not None:
            self.jg____s__g_s = ____g_i__a_t.buffer.decode(self._gm_g__n___a) 

        if b_____n_i_kd is not None and b_____n_i_kd.buffer is not None:
            self.gmy_g__pb__d = b_____n_i_kd.buffer.decode(self._gm_g__n___a) 

        if _r__azo_g_hk is not None and _r__azo_g_hk.buffer is not None:
            self._pro__frgm__ = _r__azo_g_hk.buffer.decode(self._gm_g__n___a)

        if ___e__unp__h is not None and ___e__unp__h.buffer is not None:
            self.___s__yjk_q_ = ___e__unp__h.buffer.decode(self._gm_g__n___a) 

        if __qq_q__ov_v is not None and __qq_q__ov_v.buffer is not None:
            self.kzdmh__i__y_ = __qq_q__ov_v.buffer.decode(self._gm_g__n___a) 

        if bll__dx_y__x is not None and bll__dx_y__x.buffer is not None:
            self.p__lj__pay_g = bll__dx_y__x.buffer.decode(self._gm_g__n___a) 

        if _zp____a____ is not None and _zp____a____.buffer is not None:
            self.vo___j____gl = _zp____a____.buffer.decode(self._gm_g__n___a) 

        if kkt___a_d_mo is not None and kkt___a_d_mo.buffer is not None:
            self.z_w_qqxyx___ = kkt___a_d_mo.buffer.decode(self._gm_g__n___a) 

        if __u_vk_u_iit is not None and __u_vk_u_iit.buffer is not None:
            self.___w__pydr__ = __u_vk_u_iit.buffer.decode(self._gm_g__n___a)

        if ____gp___q__ is not None and ____gp___q__.buffer is not None:
            self.__ppjf_____v = ____gp___q__.buffer.decode(self._gm_g__n___a) 

        if ndsvo__hpu__ is not None and ndsvo__hpu__.buffer is not None:
            self.____ixh_____ = ndsvo__hpu__.buffer.decode(self._gm_g__n___a) 

        if x__td_fiu_h_ is not None and x__td_fiu_h_.buffer is not None:
            self.f__fj___kg__ = x__td_fiu_h_.buffer.decode(self._gm_g__n___a) 

        if ________n_ur is not None and ________n_ur.buffer is not None:
            self.fcg__x__l_bh = ________n_ur.buffer.decode(self._gm_g__n___a) 

        if _zrt_fatw_cw is not None and _zrt_fatw_cw.buffer is not None:
            self.vj_b__f__u__ = _zrt_fatw_cw.buffer.decode(self._gm_g__n___a) 

        if d_____o___ot is not None and d_____o___ot.buffer is not None:
            self.hxpxy___q__z = d_____o___ot.buffer.decode(self._gm_g__n___a)

        if bt_a___k____ is not None and bt_a___k____.buffer is not None:
            self.___a___sf___ = bt_a___k____.buffer.decode(self._gm_g__n___a) 

        if __q__zyb__x_ is not None and __q__zyb__x_.buffer is not None:
            self.___l__fc_s_d = __q__zyb__x_.buffer.decode(self._gm_g__n___a) 

        if ___qc_s_k__r is not None and ___qc_s_k__r.buffer is not None:
            self.t____l_e_ob_ = ___qc_s_k__r.buffer.decode(self._gm_g__n___a) 

        if m___n___a_dp is not None and m___n___a_dp.buffer is not None:
            self.sfuq__vbny_x = m___n___a_dp.buffer.decode(self._gm_g__n___a) 

        if _o_a_a_f_cr_ is not None and _o_a_a_f_cr_.buffer is not None:
            self._ox_pj__nhnr = _o_a_a_f_cr_.buffer.decode(self._gm_g__n___a) 

        if t____r_mnuta is not None and t____r_mnuta.buffer is not None:
            self.__b_y_d_kqv_ = t____r_mnuta.buffer.decode(self._gm_g__n___a)

        if _b_rkr_x_wrq is not None and _b_rkr_x_wrq.buffer is not None:
            self.a_akhxq__gp_ = _b_rkr_x_wrq.buffer.decode(self._gm_g__n___a) 

        if np_mxk_h_e_r is not None and np_mxk_h_e_r.buffer is not None:
            self.k_m_i___o__h = np_mxk_h_e_r.buffer.decode(self._gm_g__n___a) 

        if __w_b_sbajoq is not None and __w_b_sbajoq.buffer is not None:
            self.lp_y_____s__ = __w_b_sbajoq.buffer.decode(self._gm_g__n___a) 

        if ta____blht__ is not None and ta____blht__.buffer is not None:
            self._e___sik_flm = ta____blht__.buffer.decode(self._gm_g__n___a) 

        if _oc_rkqwc___ is not None and _oc_rkqwc___.buffer is not None:
            self.b_xkfy_m__v_ = _oc_rkqwc___.buffer.decode(self._gm_g__n___a) 

        if _____kd_y__i is not None and _____kd_y__i.buffer is not None:
            self.qvx_e_ns____ = _____kd_y__i.buffer.decode(self._gm_g__n___a)

        if rqh_dxoz_t__ is not None and rqh_dxoz_t__.buffer is not None:
            self.sba__qjh___k = rqh_dxoz_t__.buffer.decode(self._gm_g__n___a) 

        if ___g_i_i_u_j is not None and ___g_i_i_u_j.buffer is not None:
            self.gs_m_____l__ = ___g_i_i_u_j.buffer.decode(self._gm_g__n___a) 

        if o_a_____tu__ is not None and o_a_____tu__.buffer is not None:
            self.__ju____j__c = o_a_____tu__.buffer.decode(self._gm_g__n___a) 

        if m_e_r_j_fdrw is not None and m_e_r_j_fdrw.buffer is not None:
            self._p__wc_gnx_g = m_e_r_j_fdrw.buffer.decode(self._gm_g__n___a) 

        if __y_u__ma_up is not None and __y_u__ma_up.buffer is not None:
            self.sc_gg_f____i = __y_u__ma_up.buffer.decode(self._gm_g__n___a) 

        if _msvt___r_e_ is not None and _msvt___r_e_.buffer is not None:
            self.lkex____f__e = _msvt___r_e_.buffer.decode(self._gm_g__n___a)

        if _____q__p_kb is not None and _____q__p_kb.buffer is not None:
            self.s___b__i___o = _____q__p_kb.buffer.decode(self._gm_g__n___a) 

        if uwky_zfyjvmt is not None and uwky_zfyjvmt.buffer is not None:
            self.lkc__aliq_g_ = uwky_zfyjvmt.buffer.decode(self._gm_g__n___a) 

        if z__v_v_r____ is not None and z__v_v_r____.buffer is not None:
            self._sw_lg____k_ = z__v_v_r____.buffer.decode(self._gm_g__n___a) 

        if z_b_____m__v is not None and z_b_____m__v.buffer is not None:
            self.b____ioy____ = z_b_____m__v.buffer.decode(self._gm_g__n___a) 

        if dl___shau___ is not None and dl___shau___.buffer is not None:
            self.__j_____m_ge = dl___shau___.buffer.decode(self._gm_g__n___a) 


        for i in range(_rz_pt___fj_):

            v_an_t_wn_i_ = {}
            __e_ph__r___ = str.format("__recip_version1.0_#{:08X}", i)

            _z___q_p_i__ = ___g__on___b.get_entry(__e_ph__r___)

            if _z___q_p_i__ is None:
                continue

            _____wm____u = _z___q_p_i__.get_entry("__properties_version1.0")

            if _____wm____u is not None and _____wm____u.buffer is not None:

                for j in range(8, len(_____wm____u.buffer), 16):

                    _g_q_______v = _____wm____u.buffer[j: j + 16]
                    b__v_h_x_uyp = Property(_g_q_______v)

                    if b__v_h_x_uyp.size > 0:                       
                        __phe_zb_v_h = "__substg1.0_" + str.format("{:08X}", b__v_h_x_uyp.tag)
                        f___ym____zl = _z___q_p_i__.get_entry(__phe_zb_v_h)

                        if f___ym____zl is not None and f___ym____zl.buffer is not None and len(f___ym____zl.buffer) > 0:            
                            b__v_h_x_uyp.value = f___ym____zl.buffer

                    k____y_x___d = str.format("{:08X}", b__v_h_x_uyp.tag)
                    v_an_t_wn_i_[k____y_x___d] = b__v_h_x_uyp


            b__lh_eua_bp = Recipient()

            k____rk_rj_k = v_an_t_wn_i_["39000003"] if "39000003" in v_an_t_wn_i_ else None

            if k____rk_rj_k is not None and k____rk_rj_k.value is not None:
                n_e__y___x__ = int.from_bytes(k____rk_rj_k.value[0:4], "little")
                b__lh_eua_bp.display_type = EnumUtil.parse_display_type(n_e__y___x__)

            __v__ca___h_ = v_an_t_wn_i_["0FFE0003"] if "0FFE0003" in v_an_t_wn_i_ else None

            if __v__ca___h_ is not None and __v__ca___h_.value is not None:
                h__zm____cr_ = int.from_bytes(__v__ca___h_.value[0:4], "little")
                b__lh_eua_bp.object_type = EnumUtil.parse_object_type(h__zm____cr_)

            _a__tb_____l = v_an_t_wn_i_["0C150003"] if "0C150003" in v_an_t_wn_i_ else None

            if _a__tb_____l is not None and _a__tb_____l.value is not None:
                ____k__j_ddh = int.from_bytes(_a__tb_____l.value[0:4], "little")
                b__lh_eua_bp.recipient_type = EnumUtil.parse_recipient_type(____k__j_ddh)

            g_bzk__nyjpe = v_an_t_wn_i_["0E0F000B"] if "0E0F000B" in v_an_t_wn_i_ else None

            if g_bzk__nyjpe is not None and g_bzk__nyjpe.value is not None:
                _i_c__y___ma = int.from_bytes(g_bzk__nyjpe.value[0:2], "little")

                if _i_c__y___ma > 0:
                    b__lh_eua_bp.responsibility = True

            es_f____n___ = v_an_t_wn_i_["3A40000B"] if "3A40000B" in v_an_t_wn_i_ else None

            if es_f____n___ is not None and es_f____n___.value is not None:
                rg__c_p_____ = int.from_bytes(es_f____n___.value[0:2], "little")

                if rg__c_p_____ > 0:
                    b__lh_eua_bp.send_rich_info = True

            ____w_x_yog_ = v_an_t_wn_i_["3A710003"] if "3A710003" in v_an_t_wn_i_ else None

            if ____w_x_yog_ is not None and ____w_x_yog_.value is not None:
                b__lh_eua_bp.send_internet_encoding = int.from_bytes(____w_x_yog_.value[0:4], "little")

            _k_ru___u___ = _z___q_p_i__.get_entry("__substg1.0_3001" + self._e_p_wn___m_)
            _w_g_nh____n = _z___q_p_i__.get_entry("__substg1.0_3002" + self._e_p_wn___m_)
            k_kl__r_xfjr = _z___q_p_i__.get_entry("__substg1.0_3003" + self._e_p_wn___m_)
            q_vgq____x__ = _z___q_p_i__.get_entry("__substg1.0_39FE" + self._e_p_wn___m_)
            k____z__nba_ = _z___q_p_i__.get_entry("__substg1.0_39FF" + self._e_p_wn___m_)
            __cl_u_f_d__ = _z___q_p_i__.get_entry("__substg1.0_3A20" + self._e_p_wn___m_)
            _____k__sm_i = _z___q_p_i__.get_entry("__substg1.0_403D" + self._e_p_wn___m_)
            lyz__w_z__vf = _z___q_p_i__.get_entry("__substg1.0_403E" + self._e_p_wn___m_)
            hxgb__rz_bu_ = _z___q_p_i__.get_entry("__substg1.0_0FFF0102")
            _r___ti_g__e = _z___q_p_i__.get_entry("__substg1.0_300B0102")
            l___pxoj_gj_ = _z___q_p_i__.get_entry("__substg1.0_0FF60102")

            if _k_ru___u___ is not None and _k_ru___u___.buffer is not None:
                b__lh_eua_bp.display_name = _k_ru___u___.buffer.decode(self._gm_g__n___a)

            if _w_g_nh____n is not None and _w_g_nh____n.buffer is not None:
                b__lh_eua_bp.address_type = _w_g_nh____n.buffer.decode(self._gm_g__n___a) 

            if k_kl__r_xfjr is not None and k_kl__r_xfjr.buffer is not None:
                b__lh_eua_bp.email_address = k_kl__r_xfjr.buffer.decode(self._gm_g__n___a) 

            if q_vgq____x__ is not None and q_vgq____x__.buffer is not None:
                b__lh_eua_bp.smtp_address = q_vgq____x__.buffer.decode(self._gm_g__n___a) 

            if k____z__nba_ is not None and k____z__nba_.buffer is not None:
                b__lh_eua_bp.display_name_7bit = k____z__nba_.buffer.decode(self._gm_g__n___a) 

            if __cl_u_f_d__ is not None and __cl_u_f_d__.buffer is not None:
                b__lh_eua_bp.transmitable_display_name = __cl_u_f_d__.buffer.decode(self._gm_g__n___a) 

            if _____k__sm_i is not None and _____k__sm_i.buffer is not None:
                b__lh_eua_bp.originating_address_type = _____k__sm_i.buffer.decode(self._gm_g__n___a) 

            if lyz__w_z__vf is not None and lyz__w_z__vf.buffer is not None:
                b__lh_eua_bp.originating_email_address = lyz__w_z__vf.buffer.decode(self._gm_g__n___a) 

            if hxgb__rz_bu_ is not None and hxgb__rz_bu_.buffer is not None:
                b__lh_eua_bp.entry_id = hxgb__rz_bu_.buffer

            if _r___ti_g__e is not None and _r___ti_g__e.buffer is not None:
                b__lh_eua_bp.search_key = _r___ti_g__e.buffer

            if l___pxoj_gj_ is not None and l___pxoj_gj_.buffer is not None:
                b__lh_eua_bp.instance_key = l___pxoj_gj_.buffer

            self.__g_y__yifly.append(b__lh_eua_bp)
        
        _obygm___w__ = 0

        for s in range(len(___g__on___b.directory_entries)):

            if isinstance(___g__on___b.directory_entries[s], Storage):
                _obygm___w__ += 1


        for i in range(tb_x_f_rsw__):

            gix_c_qt____ = {}
            _____f___q__ = str.format("__attach_version1.0_#{:08X}", i)

            hrj_xw_r_l_q = ___g__on___b.get_entry(_____f___q__)

            if hrj_xw_r_l_q is None:
                tb_x_f_rsw__ += 1

                if tb_x_f_rsw__ > _obygm___w__:
                    break

            else:

                a__uop__n___ = hrj_xw_r_l_q.get_entry("__properties_version1.0")

                o_smy__q_j_d = Attachment()

                if a__uop__n___ is not None and a__uop__n___.buffer is not None:

                    for j in range(8, len(a__uop__n___.buffer), 16):

                        e_z__ed___b_ = a__uop__n___.buffer[j: j + 16]
                        ______h_____ = Property(e_z__ed___b_)

                        if ______h_____.size > 0:

                            r__oai_k____ = "__substg1.0_" + str.format("{:08X}", ______h_____.tag)

                            if isinstance(hrj_xw_r_l_q.get_entry(r__oai_k____), Stream):

                                wdx_z_d__rkz = hrj_xw_r_l_q.get_entry(r__oai_k____)

                                if wdx_z_d__rkz is not None and wdx_z_d__rkz.buffer is not None and len(wdx_z_d__rkz.buffer) > 0:
                                    ______h_____.value = wdx_z_d__rkz.buffer

                            elif isinstance(hrj_xw_r_l_q.get_entry(r__oai_k____), Storage):

                                ____ty_oa___ = hrj_xw_r_l_q.get_entry(r__oai_k____)

                                if ____ty_oa___ is not None and ____ty_oa___.get_entry("__properties_version1.0") is not None:
                                    
                                    ______db____ = Message(file_path = None, buffer = None, parent = ____ty_oa___)
                                    o_smy__q_j_d.embedded_message = ______db____

                        __c_eshyg_z_ = str.format("{:08X}", ______h_____.tag)

                        if __c_eshyg_z_ not in gix_c_qt____:
                            gix_c_qt____[__c_eshyg_z_] = ______h_____
                        

                _wmbh_a_loqs = gix_c_qt____["37140003"] if "37140003" in gix_c_qt____ else None

                if _wmbh_a_loqs is not None and _wmbh_a_loqs.value is not None:
                    p__gzw_o___g = int.from_bytes(_wmbh_a_loqs.value[0:4], "little")
                    o_smy__q_j_d.flags = EnumUtil.parse_attachment_flags(p__gzw_o___g)
            
                _yrbs_m_r__i = gix_c_qt____["37050003"] if "37050003" in gix_c_qt____ else None

                if _yrbs_m_r__i is not None and _yrbs_m_r__i.value is not None:
                    __o_sq_bws__ = int.from_bytes(_yrbs_m_r__i.value[0:4], "little")
                    o_smy__q_j_d.method = EnumUtil.parse_attachment_method(__o_sq_bws__)

                z_qnv_n__j_z = gix_c_qt____["37100003"] if "37100003" in gix_c_qt____ else None

                if z_qnv_n__j_z is not None and z_qnv_n__j_z.value is not None:
                    o_smy__q_j_d.mime_sequence = int.from_bytes(z_qnv_n__j_z.value[0:4], "little")

                _____jb___s_ = gix_c_qt____["370B0003"] if "370B0003" in gix_c_qt____ else None

                if _____jb___s_ is not None and _____jb___s_.value is not None:
                    o_smy__q_j_d.rendering_position = int.from_bytes(_____jb___s_.value[0:4], "little")

                z_p_opfcy_d_ = gix_c_qt____["0E200003"] if "0E200003" in gix_c_qt____ else None

                if z_p_opfcy_d_ is not None and z_p_opfcy_d_.value is not None:
                    o_smy__q_j_d.size = int.from_bytes(z_p_opfcy_d_.value[0:4], "little")

                _of_ew_rl__s = gix_c_qt____["0FFE0003"] if "0FFE0003" in gix_c_qt____ else None

                if _of_ew_rl__s is not None and _of_ew_rl__s.value is not None:
                    x_e_jal_v_mn = int.from_bytes(_of_ew_rl__s.value[0:4], "little")
                    o_smy__q_j_d.object_type = EnumUtil.parse_object_type(x_e_jal_v_mn)

                _c_rnqb_zm__ = gix_c_qt____["7FFE000B"] if "7FFE000B" in gix_c_qt____ else None

                if _c_rnqb_zm__ is not None and _c_rnqb_zm__.value is not None:
                    ____l_fy_qgb = int.from_bytes(_c_rnqb_zm__.value[0:2], "little")

                    if ____l_fy_qgb > 0:
                        o_smy__q_j_d.is_hidden = True

                u_e_h___f__q = gix_c_qt____["7FFF000B"] if "7FFF000B" in gix_c_qt____ else None

                if u_e_h___f__q is not None and u_e_h___f__q.value is not None:
                    dc___vf_r__x = int.from_bytes(u_e_h___f__q.value[0:4], "little")

                    if dc___vf_r__x > 0:
                        o_smy__q_j_d.is_contact_photo = True

                v_k_b_x_q_c_ = gix_c_qt____["30070040"] if "30070040" in gix_c_qt____ else None

                if v_k_b_x_q_c_ is not None and v_k_b_x_q_c_.value is not None:
                    i__s______z_ = int.from_bytes(v_k_b_x_q_c_.value[0: 4], "little")
                    _ilkt_q_d___ = int.from_bytes(v_k_b_x_q_c_.value[4: 8], "little")

                    if _ilkt_q_d___ > 0:
                        i_x____hz_to = i__s______z_ + (_ilkt_q_d___ << 32)
                        j____h_x_v_h = datetime.datetime(1601,1,1)   

                        try:    
                            o_smy__q_j_d.creation_time = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                            o_smy__q_j_d.creation_time = Message._j__y____u__(o_smy__q_j_d.creation_time)
                        except:
                            pass 

                k_p____f___b = gix_c_qt____["30080040"] if "30080040" in gix_c_qt____ else None

                if k_p____f___b is not None and k_p____f___b.value is not None:
                    cb_yxujjeenz = int.from_bytes(k_p____f___b.value[0: 4], "little")
                    sc____yeyoyg = int.from_bytes(k_p____f___b.value[4: 8], "little")

                    if sc____yeyoyg > 0:
                        i_x____hz_to = cb_yxujjeenz + (sc____yeyoyg << 32)
                        j____h_x_v_h = datetime.datetime(1601,1,1)   

                        try:    
                            o_smy__q_j_d.last_modification_time = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                            o_smy__q_j_d.last_modification_time = Message._j__y____u__(o_smy__q_j_d.last_modification_time)
                        except:
                            pass 


                __s______s_s = hrj_xw_r_l_q.get_entry("__substg1.0_370F0102")
                __gwj__un__s = hrj_xw_r_l_q.get_entry("__substg1.0_3711" + self._e_p_wn___m_)
                r_zubzhwd___ = hrj_xw_r_l_q.get_entry("__substg1.0_3712" + self._e_p_wn___m_)
                ___e___k__q_ = hrj_xw_r_l_q.get_entry("__substg1.0_3713" + self._e_p_wn___m_)
                p_v_a___bam_ = hrj_xw_r_l_q.get_entry("__substg1.0_3716" + self._e_p_wn___m_)
                ___yknf__gea = hrj_xw_r_l_q.get_entry("__substg1.0_37010102")
                _____i___a__ = hrj_xw_r_l_q.get_entry("__substg1.0_37020102")
                hakpxcyhequk = hrj_xw_r_l_q.get_entry("__substg1.0_3703" + self._e_p_wn___m_)
                c_ludp___f_f = hrj_xw_r_l_q.get_entry("__substg1.0_3704" + self._e_p_wn___m_)
                ___itg__b_e_ = hrj_xw_r_l_q.get_entry("__substg1.0_3707" + self._e_p_wn___m_)
                __r_s_fd____ = hrj_xw_r_l_q.get_entry("__substg1.0_370D" + self._e_p_wn___m_)
                mn_uc_____kk = hrj_xw_r_l_q.get_entry("__substg1.0_370E" + self._e_p_wn___m_)
                q____u_vfb__ = hrj_xw_r_l_q.get_entry("__substg1.0_3708" + self._e_p_wn___m_)
                _ps______y__ = hrj_xw_r_l_q.get_entry("__substg1.0_37090102")
                _c____p___fi = hrj_xw_r_l_q.get_entry("__substg1.0_370A0102")
                ___z_l_uyn__ = hrj_xw_r_l_q.get_entry("__substg1.0_370C" + self._e_p_wn___m_)
                eg_mif__k___ = hrj_xw_r_l_q.get_entry("__substg1.0_3001" + self._e_p_wn___m_)  

                if hrj_xw_r_l_q.get_entry("__substg1.0_3701000D") is not None and isinstance(hrj_xw_r_l_q.get_entry("__substg1.0_3701000D"), Storage):
                    _fgd_szp___k = hrj_xw_r_l_q.get_entry("__substg1.0_3701000D")
                    o_smy__q_j_d.data_object_storage = _fgd_szp___k
                    o_smy__q_j_d.properties_stream = a__uop__n___

                if __s______s_s is not None and __s______s_s.buffer is not None:
                    o_smy__q_j_d.additional_info = __s______s_s.buffer

                if __gwj__un__s is not None and __gwj__un__s.buffer is not None:
                    o_smy__q_j_d.content_base = __gwj__un__s.buffer.decode(self._gm_g__n___a)

                if r_zubzhwd___ is not None and r_zubzhwd___.buffer is not None:
                    o_smy__q_j_d.content_id = r_zubzhwd___.buffer.decode(self._gm_g__n___a) 

                if ___e___k__q_ is not None and ___e___k__q_.buffer is not None:
                    o_smy__q_j_d.content_location = ___e___k__q_.buffer.decode(self._gm_g__n___a) 

                if p_v_a___bam_ is not None and p_v_a___bam_.buffer is not None:
                    o_smy__q_j_d.content_disposition = p_v_a___bam_.buffer.decode(self._gm_g__n___a) 

                if ___yknf__gea is not None and ___yknf__gea.buffer is not None:
                    o_smy__q_j_d.data = ___yknf__gea.buffer 

                if _____i___a__ is not None and _____i___a__.buffer is not None:
                    o_smy__q_j_d.encoding = _____i___a__.buffer

                if hakpxcyhequk is not None and hakpxcyhequk.buffer is not None:
                    o_smy__q_j_d.extension = hakpxcyhequk.buffer.decode(self._gm_g__n___a) 

                if c_ludp___f_f is not None and c_ludp___f_f.buffer is not None:
                    o_smy__q_j_d.file_name = c_ludp___f_f.buffer.decode(self._gm_g__n___a) 

                if ___itg__b_e_ is not None and ___itg__b_e_.buffer is not None:
                    o_smy__q_j_d.long_file_name = ___itg__b_e_.buffer.decode(self._gm_g__n___a) 

                if __r_s_fd____ is not None and __r_s_fd____.buffer is not None:
                    o_smy__q_j_d.long_path_name = __r_s_fd____.buffer.decode(self._gm_g__n___a) 

                if mn_uc_____kk is not None and mn_uc_____kk.buffer is not None:
                    o_smy__q_j_d.mime_tag = mn_uc_____kk.buffer.decode(self._gm_g__n___a) 

                if q____u_vfb__ is not None and q____u_vfb__.buffer is not None:
                    o_smy__q_j_d.path_name = q____u_vfb__.buffer.decode(self._gm_g__n___a) 

                if _ps______y__ is not None and _ps______y__.buffer is not None:
                    o_smy__q_j_d.rendering = _ps______y__.buffer

                if _c____p___fi is not None and _c____p___fi.buffer is not None:
                    o_smy__q_j_d.tag = _c____p___fi.buffer

                if ___z_l_uyn__ is not None and ___z_l_uyn__.buffer is not None:
                    o_smy__q_j_d.transport_name = ___z_l_uyn__.buffer.decode(self._gm_g__n___a) 

                if eg_mif__k___ is not None and eg_mif__k___.buffer is not None:
                    o_smy__q_j_d.display_name = eg_mif__k___.buffer.decode(self._gm_g__n___a)

                if o_smy__q_j_d.data is not None or o_smy__q_j_d.data_object is not None or o_smy__q_j_d.data_object_storage is not None or o_smy__q_j_d.embedded_message is not None:
                    self.j____d____c_.append(o_smy__q_j_d)

    def kon_r_h___t_(self):

        _d_nk_____s_ = CompoundFile()
        _d_nk_____s_.major_version = 4
        _d_nk_____s_.root.class_id = bytes([11, 13, 2, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])

        _____gix___f = bytearray()
        hxf__o_ztdyt = bytearray()
        __e_p_n_x_k_ = bytearray()

        h_u_wgs____i = []

        h_u_wgs____i.append(bytes(16))
        h_u_wgs____i.append(StandardPropertySet.MAPI)
        h_u_wgs____i.append(StandardPropertySet.PUBLIC_STRINGS)

        ______ui____ = []
        __o_t_nc_ic_ = {}

        self._m_rz____h__ = []

        l_bteg____g_ = self.__nfho_____d(self._m_rz____h__)

        __ez________ = 0

        for i in range(len(self._m_rz____h__)):
        
            a__z____b_zn = Message.__g__j__gx__(self._m_rz____h__[i].guid, h_u_wgs____i)

            if a__z____b_zn == -1 and self._m_rz____h__[i].guid is not None:
            
                h_u_wgs____i.append(self._m_rz____h__[i].guid)
                a__z____b_zn = len(h_u_wgs____i) - 1
            
            _hi____o____ = 0
            dr___hgmpofu = 0

            if self._m_rz____h__[i].name is not None:
            
                ______ui____.append(self._m_rz____h__[i].name)
                dr___hgmpofu = 1

                _hi____o____ = __ez________
            
            else:           
                _hi____o____ = self._m_rz____h__[i].id            

            _tgs__ywd___ = i

            _wemyf___m_m = _tgs__ywd___ << 16
            __u__ny__m_g = a__z____b_zn << 1

            if dr___hgmpofu == 1:
                __u__ny__m_g = __u__ny__m_g + 1
            
            _wemyf___m_m = _wemyf___m_m + __u__ny__m_g

            xc____j___ge = bytearray(8)
            _d___dh_qp__ = int.to_bytes(_hi____o____, 4, "little")
            ____j______y = int.to_bytes(_wemyf___m_m, 4, "little")

            xc____j___ge[0: 4] = _d___dh_qp__
            xc____j___ge[4: 8] = ____j______y

            hxf__o_ztdyt += xc____j___ge

            if dr___hgmpofu == 0:
            
                up_g_db_k_mp = (0x1000 + ((self._m_rz____h__[i].id ^ a__z____b_zn << 1) % 0x1F))
                up_g_db_k_mp = (up_g_db_k_mp << 16) | 0x00000102

                _gfd_hthczv_ = str.format("{:08X}", up_g_db_k_mp)
                _gfd_hthczv_ = "__substg1.0_" + _gfd_hthczv_

                if _gfd_hthczv_ in __o_t_nc_ic_:                
                    eynjn_yv_lq_ = __o_t_nc_ic_[_gfd_hthczv_]
                    eynjn_yv_lq_ += xc____j___ge
                
                else:                
                    __o_t_nc_ic_[_gfd_hthczv_] = xc____j___ge                
            
            else:
            
                hputte_____p = Crc()
                
                hputte_____p.update(self._m_rz____h__[i].name.encode(self._gm_g__n___a))
                _x___dg_h_kg = hputte_____p.value

                up_g_db_k_mp = (0x1000 + ((_x___dg_h_kg ^ ((a__z____b_zn << 1) | 1)) % 0x1F))
                up_g_db_k_mp = (up_g_db_k_mp << 16) | 0x00000102

                _gfd_hthczv_ = str.format("{:08X}", up_g_db_k_mp)
                _gfd_hthczv_ = "__substg1.0_" + _gfd_hthczv_

                if _gfd_hthczv_ in __o_t_nc_ic_:                
                    eynjn_yv_lq_ = __o_t_nc_ic_[_gfd_hthczv_]
                    eynjn_yv_lq_ += xc____j___ge
                
                else:                
                    __o_t_nc_ic_[_gfd_hthczv_] = xc____j___ge            

            if self._m_rz____h__[i].name is not None:            
                ___kuyfw____ = self._m_rz____h__[i].name.encode(self.bn_lyk_isr_a)
                ____h__wwaw_ = len(___kuyfw____) % 4
                __ez________ += len(___kuyfw____) + ____h__wwaw_ + 4


        _e_l_____i_c = Storage("__nameid_version1.0")

        i_c_jk_bz___ = Stream("__substg1.0_00030102", bytes(hxf__o_ztdyt))

        for i in range(3, len(h_u_wgs____i), 1):     
            u___ke_f__o_ = h_u_wgs____i[i]
            _____gix___f += u___ke_f__o_
        

        _____tdu__n_ = Stream("__substg1.0_00020102", bytes(_____gix___f))

        for i in range(len(______ui____)):
        
            ___kuyfw____ = ______ui____[i].encode(self.bn_lyk_isr_a)
            __s__juy_ap_ = int.to_bytes(len(___kuyfw____), 4, "little")

            __e_p_n_x_k_ += __s__juy_ap_[0: 4]
            __e_p_n_x_k_ += ___kuyfw____

            ____h__wwaw_ = len(___kuyfw____) % 4

            if ____h__wwaw_ > 0:
            
                __kiv_j__za_ = bytes(____h__wwaw_)
                __e_p_n_x_k_ += __kiv_j__za_
        

        __ds_yzz_vtp = Stream("__substg1.0_00040102", bytes(__e_p_n_x_k_))

        _e_l_____i_c.directory_entries.append(_____tdu__n_)
        _e_l_____i_c.directory_entries.append(i_c_jk_bz___)
        _e_l_____i_c.directory_entries.append(__ds_yzz_vtp)

        for kj_r_t_ri_x_ in __o_t_nc_ic_:
        
            eynjn_yv_lq_ = __o_t_nc_ic_[kj_r_t_ri_x_]
            _____iz_____ = Stream(kj_r_t_ri_x_, eynjn_yv_lq_)
            _e_l_____i_c.directory_entries.append(_____iz_____)
        

        _d_nk_____s_.root.directory_entries.extend(l_bteg____g_)        

        _d_nk_____s_.root.directory_entries.append(_e_l_____i_c)

        return _d_nk_____s_.to_bytes()

    def __nfho_____d(self, __d_v___a_yf):

        n_b__sfzn___ = []
        _d____y___bd = bytearray()
        mkkh___d_lvf = len("\0".encode(self._gm_g__n___a))


        ____h__d____ = 0
        _b____v_k__m = int.to_bytes(____h__d____, 4, "little")
        e_w_e_ju_q__ = int.to_bytes(len(self.__g_y__yifly), 4, "little")
        ___g_xgrexqt = int.to_bytes(len(self.j____d____c_), 4, "little")

        _d____y___bd += _b____v_k__m
        _d____y___bd += _b____v_k__m
        _d____y___bd += e_w_e_ju_q__
        _d____y___bd += ___g_xgrexqt
        _d____y___bd += e_w_e_ju_q__
        _d____y___bd += ___g_xgrexqt

        if not self.ulyx_zb_hrlu:
            _d____y___bd += _b____v_k__m
            _d____y___bd += _b____v_k__m

        if self._gm_g__n___a == self.bn_lyk_isr_a:
            self._e_p_wn___m_ = "001F"
            self.sll__adckt__ = 0x001F
            self.q_rcyqzvz___ = "101F"
            self.__e_ylz_t_hl = 0x101F

            if StoreSupportMask.UNICODE not in self.s__f__m_okw_:
                self.s__f__m_okw_.append(StoreSupportMask.UNICODE)

        elif StoreSupportMask.UNICODE in self.s__f__m_okw_:
            self.s__f__m_okw_.remove(StoreSupportMask.UNICODE)

        if self.s__f__m_okw_ is not None:
        
            __h_mw___yc_ = Property()
            __h_mw___yc_.tag = 0x340D0003
            __h_mw___yc_.type = PropertyType.INTEGER_32
            __h_mw___yc_.value = int.to_bytes(EnumUtil.parse_store_support_mask(self.s__f__m_okw_), 4, "little")
            __h_mw___yc_.is_readable = True
            __h_mw___yc_.is_writeable = True

            _d____y___bd += __h_mw___yc_.to_bytes()
        

        if self.___t_lgsh__n is not None:
        
            _yd_k___ru__ = self.___t_lgsh__n.encode(self._gm_g__n___a)
            hx_sji__ibte = Stream("__substg1.0_001A" + self._e_p_wn___m_, _yd_k___ru__)
            n_b__sfzn___.append(hx_sji__ibte)

            __n_ig__d___ = Property()
            __n_ig__d___.tag = 0x001A << 16 | self.sll__adckt__
            __n_ig__d___.type = PropertyType.STRING_8
            __n_ig__d___.size = len(_yd_k___ru__) + mkkh___d_lvf
            __n_ig__d___.is_readable = True
            __n_ig__d___.is_writeable = True

            _d____y___bd += __n_ig__d___.to_bytes()
        

        if self.b_t___b_q_xu is not None:
        
            _ge_jg__i_z_ = self.b_t___b_q_xu.encode(self._gm_g__n___a)
            j______vi_ad = Stream("__substg1.0_0037" + self._e_p_wn___m_, _ge_jg__i_z_)
            n_b__sfzn___.append(j______vi_ad)

            __b_u_i____r = Property()
            __b_u_i____r.tag = 0x0037 << 16 | self.sll__adckt__
            __b_u_i____r.type = PropertyType.STRING_8
            __b_u_i____r.size = len(_ge_jg__i_z_) + mkkh___d_lvf
            __b_u_i____r.is_readable = True
            __b_u_i____r.is_writeable = True

            _d____y___bd += __b_u_i____r.to_bytes()
        

        if self._______c__ty is not None:
        
            _z__h__i_q__ = self._______c__ty.encode(self._gm_g__n___a)
            ___zwn__fwe_ = Stream("__substg1.0_003D" + self._e_p_wn___m_, _z__h__i_q__)
            n_b__sfzn___.append(___zwn__fwe_)

            _____k__fn_w = Property()
            _____k__fn_w.tag = 0x003D << 16 | self.sll__adckt__
            _____k__fn_w.type = PropertyType.STRING_8
            _____k__fn_w.size = len(_z__h__i_q__) + mkkh___d_lvf
            _____k__fn_w.is_readable = True
            _____k__fn_w.is_writeable = True

            _d____y___bd += _____k__fn_w.to_bytes()
        

        if self._s_k_n_jb___ is not None:
        
            ebl_e_qth___ = self._s_k_n_jb___.encode(self._gm_g__n___a)
            ____c__ufir_ = Stream("__substg1.0_0070" + self._e_p_wn___m_, ebl_e_qth___)
            n_b__sfzn___.append(____c__ufir_)

            _eg_nppzh__x = Property()
            _eg_nppzh__x.tag = 0x0070 << 16 | self.sll__adckt__
            _eg_nppzh__x.type = PropertyType.STRING_8
            _eg_nppzh__x.size = len(ebl_e_qth___) + mkkh___d_lvf
            _eg_nppzh__x.is_readable = True
            _eg_nppzh__x.is_writeable = True

            _d____y___bd += _eg_nppzh__x.to_bytes()
        

        if self.w__teeli____ is not None:
        
            b_oxx_b_k___ = self.w__teeli____.encode(self._gm_g__n___a)
            ___oxquhgjr_ = Stream("__substg1.0_0E02" + self._e_p_wn___m_, b_oxx_b_k___)
            n_b__sfzn___.append(___oxquhgjr_)

            mcw_nxf__w__ = Property()
            mcw_nxf__w__.tag = 0x0E02 << 16 | self.sll__adckt__
            mcw_nxf__w__.type = PropertyType.STRING_8
            mcw_nxf__w__.size = len(b_oxx_b_k___) + mkkh___d_lvf
            mcw_nxf__w__.is_readable = True
            mcw_nxf__w__.is_writeable = True

            _d____y___bd += mcw_nxf__w__.to_bytes()
        

        if self.qj_wgu_zzu_s is not None:
        
            _qr_n_j_p__w = self.qj_wgu_zzu_s.encode(self._gm_g__n___a)
            j_lk_h__c__a = Stream("__substg1.0_0E03" + self._e_p_wn___m_, _qr_n_j_p__w)
            n_b__sfzn___.append(j_lk_h__c__a)

            h_____y___o_ = Property()
            h_____y___o_.tag = 0x0E03 << 16 | self.sll__adckt__
            h_____y___o_.type = PropertyType.STRING_8
            h_____y___o_.size = len(_qr_n_j_p__w) + mkkh___d_lvf
            h_____y___o_.is_readable = True
            h_____y___o_.is_writeable = True

            _d____y___bd += h_____y___o_.to_bytes()
        

        if self.qw_____z__u_ is not None:
        
            __nk_d__q_fn = self.qw_____z__u_.encode(self._gm_g__n___a)
            _w_v_j_h_lex = Stream("__substg1.0_0E04" + self._e_p_wn___m_, __nk_d__q_fn)
            n_b__sfzn___.append(_w_v_j_h_lex)

            _ns__azrm_pm = Property()
            _ns__azrm_pm.tag = 0x0E04 << 16 | self.sll__adckt__
            _ns__azrm_pm.type = PropertyType.STRING_8
            _ns__azrm_pm.size = len(__nk_d__q_fn) + mkkh___d_lvf
            _ns__azrm_pm.is_readable = True
            _ns__azrm_pm.is_writeable = True

            _d____y___bd += _ns__azrm_pm.to_bytes()
        

        if self.p____t__w_g_ is not None:
        
            __q_____vyr_ = self.p____t__w_g_.encode(self._gm_g__n___a)
            __n_x_rpwstp = Stream("__substg1.0_0074" + self._e_p_wn___m_, __q_____vyr_)
            n_b__sfzn___.append(__n_x_rpwstp)

            hc_h_c_c____ = Property()
            hc_h_c_c____.tag = 0x0074 << 16 | self.sll__adckt__
            hc_h_c_c____.type = PropertyType.STRING_8
            hc_h_c_c____.size = len(__q_____vyr_) + mkkh___d_lvf
            hc_h_c_c____.is_readable = True
            hc_h_c_c____.is_writeable = True

            _d____y___bd += hc_h_c_c____.to_bytes()
        

        if self.cx_p_u___h_i is not None:
        
            _m_wps__cn_l = self.cx_p_u___h_i.encode(self._gm_g__n___a)
            __zp___t____ = Stream("__substg1.0_0050" + self._e_p_wn___m_, _m_wps__cn_l)
            n_b__sfzn___.append(__zp___t____)

            n__rf__y____ = Property()
            n__rf__y____.tag = 0x0050 << 16 | self.sll__adckt__
            n__rf__y____.type = PropertyType.STRING_8
            n__rf__y____.size = len(_m_wps__cn_l) + mkkh___d_lvf
            n__rf__y____.is_readable = True
            n__rf__y____.is_writeable = True

            _d____y___bd += n__rf__y____.to_bytes()


            _cz____o__ka = Message.xh_nz___yzlo(self.cx_p_u___h_i)

            bqjtdekl___m = Stream("__substg1.0_004F0102", _cz____o__ka)
            n_b__sfzn___.append(bqjtdekl___m)

            ____fv_f_kgh = Property()
            ____fv_f_kgh.tag = 0x004F0102
            ____fv_f_kgh.type = PropertyType.BINARY
            ____fv_f_kgh.size = len(_cz____o__ka)
            ____fv_f_kgh.is_readable = True
            ____fv_f_kgh.is_writeable = True

            _d____y___bd += ____fv_f_kgh.to_bytes()
        

        if self.j__kfc___d_g is not None:
        
            t_s_zn_hkaj_ = self.j__kfc___d_g.encode(self._gm_g__n___a)
            a_m_i__b__q_ = Stream("__substg1.0_0E1D" + self._e_p_wn___m_, t_s_zn_hkaj_)
            n_b__sfzn___.append(a_m_i__b__q_)

            flb__v__o___ = Property()
            flb__v__o___.tag = 0x0E1D << 16 | self.sll__adckt__
            flb__v__o___.type = PropertyType.STRING_8
            flb__v__o___.size = len(t_s_zn_hkaj_) + mkkh___d_lvf
            flb__v__o___.is_readable = True
            flb__v__o___.is_writeable = True

            _d____y___bd += flb__v__o___.to_bytes()
        

        if self.p__w___rx_bo is not None:
        
            _m_wmkr_g_zp = self.p__w___rx_bo.encode(self._gm_g__n___a)
            __qpng__up__ = Stream("__substg1.0_1000" + self._e_p_wn___m_, _m_wmkr_g_zp)
            n_b__sfzn___.append(__qpng__up__)

            _bc__al_____ = Property()
            _bc__al_____.tag = 0x1000 << 16 | self.sll__adckt__
            _bc__al_____.type = PropertyType.STRING_8
            _bc__al_____.size =len(_m_wmkr_g_zp) + mkkh___d_lvf
            _bc__al_____.is_readable = True
            _bc__al_____.is_writeable = True

            _d____y___bd += _bc__al_____.to_bytes()
        

        if self.i_f__lcbcp__ is not None:
        
            _z_i__ta__g_ = Stream("__substg1.0_10090102", self.i_f__lcbcp__)
            n_b__sfzn___.append(_z_i__ta__g_)

            _j_jg__j__n_ = Property()
            _j_jg__j__n_.tag = 0x10090102
            _j_jg__j__n_.type = PropertyType.BINARY
            _j_jg__j__n_.size = len(self.i_f__lcbcp__)
            _j_jg__j__n_.is_readable = True
            _j_jg__j__n_.is_writeable = True

            _d____y___bd += _j_jg__j__n_.to_bytes()
        

        if self.kh_____k_y_g is not None:
        
            _ip__h_p__ya = Stream("__substg1.0_300B0102", self.kh_____k_y_g)
            n_b__sfzn___.append(_ip__h_p__ya)

            __kwr__a___d = Property()
            __kwr__a___d.tag = 0x300B0102
            __kwr__a___d.type = PropertyType.BINARY
            __kwr__a___d.size = len(self.kh_____k_y_g)
            __kwr__a___d.is_readable = True
            __kwr__a___d.is_writeable = True

            _d____y___bd += __kwr__a___d.to_bytes()
        

        if self.__zr_cn_k__x is not None:
        
            u_pl_____w__ = Stream("__substg1.0_65E20102", self.__zr_cn_k__x)
            n_b__sfzn___.append(u_pl_____w__)

            frvc_t___c_r = Property()
            frvc_t___c_r.tag = 0x65E20102
            frvc_t___c_r.type = PropertyType.BINARY
            frvc_t___c_r.size = len(self.__zr_cn_k__x)
            frvc_t___c_r.is_readable = True
            frvc_t___c_r.is_writeable = True

            _d____y___bd += frvc_t___c_r.to_bytes()
        

        if self._fz___ad_f__ is not None:
        
            _______zt_ct = Stream("__substg1.0_0FFF0102", self._fz___ad_f__)
            n_b__sfzn___.append(_______zt_ct)

            _cr__d__m__l = Property()
            _cr__d__m__l.tag = 0x0FFF0102
            _cr__d__m__l.type = PropertyType.BINARY
            _cr__d__m__l.size = len(self._fz___ad_f__)
            _cr__d__m__l.is_readable = True
            _cr__d__m__l.is_writeable = True

            _d____y___bd += _cr__d__m__l.to_bytes()
        

        if self.a_uk__ilatjb is not None:
        
            ___ue_______ = Stream("__substg1.0_00460102", self.a_uk__ilatjb)
            n_b__sfzn___.append(___ue_______)

            ______l_f___ = Property()
            ______l_f___.tag = 0x00460102
            ______l_f___.type = PropertyType.BINARY
            ______l_f___.size = len(self.a_uk__ilatjb)
            ______l_f___.is_readable = True
            ______l_f___.is_writeable = True

            _d____y___bd += ______l_f___.to_bytes()
        

        if self.____gw__e_a_ is not None:
        
            _____p__r__s = Stream("__substg1.0_00530102", self.____gw__e_a_)
            n_b__sfzn___.append(_____p__r__s)

            fg_______l_j = Property()
            fg_______l_j.tag = 0x00530102
            fg_______l_j.type = PropertyType.BINARY
            fg_______l_j.size = len(self.____gw__e_a_)
            fg_______l_j.is_readable = True
            fg_______l_j.is_writeable = True

            _d____y___bd += fg_______l_j.to_bytes()
        

        if self.__z_j__au_m_ > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.__z_j__au_m_ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            __okm_jmcx__ = Property()
            __okm_jmcx__.tag = 0x30070040
            __okm_jmcx__.type = PropertyType.TIME
            __okm_jmcx__.value = __cwx_qbk___
            __okm_jmcx__.is_readable = True
            __okm_jmcx__.is_writeable = False

            _d____y___bd += __okm_jmcx__.to_bytes()
        

        if self.i_zt_m_sm__i > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.i_zt_m_sm__i - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _yofpl_kej_s = Property()
            _yofpl_kej_s.tag = 0x30080040
            _yofpl_kej_s.type = PropertyType.TIME
            _yofpl_kej_s.value = __cwx_qbk___
            _yofpl_kej_s.is_readable = True
            _yofpl_kej_s.is_writeable = False

            _d____y___bd += _yofpl_kej_s.to_bytes()
        

        if self.___ud_______ > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.___ud_______ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            wr_q_s___m__ = Property()
            wr_q_s___m__.tag = 0x0E060040
            wr_q_s___m__.type = PropertyType.TIME
            wr_q_s___m__.value = __cwx_qbk___
            wr_q_s___m__.is_readable = True
            wr_q_s___m__.is_writeable = True

            _d____y___bd += wr_q_s___m__.to_bytes()
        

        if self._w______i_dp > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self._w______i_dp - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _ay_z__qhtgj = Property()
            _ay_z__qhtgj.tag = 0x00390040
            _ay_z__qhtgj.type = PropertyType.TIME
            _ay_z__qhtgj.value = __cwx_qbk___
            _ay_z__qhtgj.is_readable = True
            _ay_z__qhtgj.is_writeable = True

            _d____y___bd += _ay_z__qhtgj.to_bytes()
        

        if self._e__gxx__h_u > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self._e__gxx__h_u - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            ___qm__iio__ = Property()
            ___qm__iio__.tag = 0x000F0040
            ___qm__iio__.type = PropertyType.TIME
            ___qm__iio__.value = __cwx_qbk___
            ___qm__iio__.is_readable = True
            ___qm__iio__.is_writeable = True

            _d____y___bd += ___qm__iio__.to_bytes()
        

        if self.__g__h_iwita > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.__g__h_iwita - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            zl__s_fs_z__ = Property()
            zl__s_fs_z__.tag = 0x00480040
            zl__s_fs_z__.type = PropertyType.TIME
            zl__s_fs_z__.value = __cwx_qbk___
            zl__s_fs_z__.is_readable = True
            zl__s_fs_z__.is_writeable = True

            _d____y___bd += zl__s_fs_z__.to_bytes()
        

        if self.y_ze__l___u_ > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.y_ze__l___u_ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _c_bymosg_oo = Property()
            _c_bymosg_oo.tag = 0x00320040
            _c_bymosg_oo.type = PropertyType.TIME
            _c_bymosg_oo.value = __cwx_qbk___
            _c_bymosg_oo.is_readable = True
            _c_bymosg_oo.is_writeable = True

            _d____y___bd += _c_bymosg_oo.to_bytes()
        

        if self.s_jwv_w__ng_ > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.s_jwv_w__ng_ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            ___n______qb = Property()
            ___n______qb.tag = 0x10820040
            ___n______qb.type = PropertyType.TIME
            ___n______qb.value = __cwx_qbk___
            ___n______qb.is_readable = True
            ___n______qb.is_writeable = True

            _d____y___bd += ___n______qb.to_bytes()
        

        if self.__okvntl__d_ is not None:
        
            uouq_f___c_u = self.__okvntl__d_.encode(self._gm_g__n___a)
            ztbcqksg____ = Stream("__substg1.0_1001" + self._e_p_wn___m_, uouq_f___c_u)
            n_b__sfzn___.append(ztbcqksg____)

            _u__w_ed_u_m = Property()
            _u__w_ed_u_m.tag = 0x1001 << 16 | self.sll__adckt__
            _u__w_ed_u_m.type = PropertyType.STRING_8
            _u__w_ed_u_m.size = len(uouq_f___c_u) + mkkh___d_lvf
            _u__w_ed_u_m.is_readable = True
            _u__w_ed_u_m.is_writeable = True

            _d____y___bd += _u__w_ed_u_m.to_bytes()
        

        if self.____l__er___ is not None:
        
            h_v__q____qu = self.____l__er___.encode(self._gm_g__n___a)
            _csi_y______ = Stream("__substg1.0_3FF8" + self._e_p_wn___m_, h_v__q____qu)
            n_b__sfzn___.append(_csi_y______)

            _c_fq____u_l = Property()
            _c_fq____u_l.tag = 0x3FF8 << 16 | self.sll__adckt__
            _c_fq____u_l.type = PropertyType.STRING_8
            _c_fq____u_l.size = len(h_v__q____qu) + mkkh___d_lvf
            _c_fq____u_l.is_readable = True
            _c_fq____u_l.is_writeable = True

            _d____y___bd += _c_fq____u_l.to_bytes()
        

        if self.wo___yi_w__x is not None:
        
            _fu__a___tio = self.wo___yi_w__x.encode(self._gm_g__n___a)
            _xs__l__x_bl = Stream("__substg1.0_3FFA" + self._e_p_wn___m_, _fu__a___tio)
            n_b__sfzn___.append(_xs__l__x_bl)

            b_q__m_kpy_i = Property()
            b_q__m_kpy_i.tag = 0x3FFA << 16 | self.sll__adckt__
            b_q__m_kpy_i.type = PropertyType.STRING_8
            b_q__m_kpy_i.size = len(_fu__a___tio) + mkkh___d_lvf
            b_q__m_kpy_i.is_readable = True
            b_q__m_kpy_i.is_writeable = True

            _d____y___bd += b_q__m_kpy_i.to_bytes()
        

        if self._so__s_lu_o_ is not None:
        
            _vd_a_se__df = self._so__s_lu_o_.encode(self._gm_g__n___a)
            _f_bsa_d__j_ = Stream("__substg1.0_1035" + self._e_p_wn___m_, _vd_a_se__df)
            n_b__sfzn___.append(_f_bsa_d__j_)

            sx_xs_k_x_vd = Property()
            sx_xs_k_x_vd.tag = 0x1035 << 16 | self.sll__adckt__
            sx_xs_k_x_vd.type = PropertyType.STRING_8
            sx_xs_k_x_vd.size = len(_vd_a_se__df) + mkkh___d_lvf
            sx_xs_k_x_vd.is_readable = True
            sx_xs_k_x_vd.is_writeable = True

            _d____y___bd += sx_xs_k_x_vd.to_bytes()
        

        if self.j_a_______a_ is not None:
        
            ___jb_dl___u = self.j_a_______a_.encode(self._gm_g__n___a)
            e___a_p_____ = Stream("__substg1.0_1042" + self._e_p_wn___m_, ___jb_dl___u)
            n_b__sfzn___.append(e___a_p_____)

            jytk___nn_wa = Property()
            jytk___nn_wa.tag = 0x1042 << 16 | self.sll__adckt__
            jytk___nn_wa.type = PropertyType.STRING_8
            jytk___nn_wa.size = len(___jb_dl___u) + mkkh___d_lvf
            jytk___nn_wa.is_readable = True
            jytk___nn_wa.is_writeable = True

            _d____y___bd += jytk___nn_wa.to_bytes()
        

        if self._r_h__rjorsu is not None:
        
            _gw_j_nbm_b_ = self._r_h__rjorsu.encode(self._gm_g__n___a)
            ___f_k_q_oqd = Stream("__substg1.0_1039" + self._e_p_wn___m_, _gw_j_nbm_b_)
            n_b__sfzn___.append(___f_k_q_oqd)

            _g__a_h_e__g = Property()
            _g__a_h_e__g.tag = 0x1039 << 16 | self.sll__adckt__
            _g__a_h_e__g.type = PropertyType.STRING_8
            _g__a_h_e__g.size = len(_gw_j_nbm_b_) + mkkh___d_lvf
            _g__a_h_e__g.is_readable = True
            _g__a_h_e__g.is_writeable = True

            _d____y___bd += _g__a_h_e__g.to_bytes()
        

        if self._f__a___jm_p > 0:
        
            ___ly__xuf_j = Property()
            ___ly__xuf_j.tag = 0x3FFD0003
            ___ly__xuf_j.type = PropertyType.INTEGER_32
            ___ly__xuf_j.value = int.to_bytes(self._f__a___jm_p, 4, "little")
            ___ly__xuf_j.is_readable = True
            ___ly__xuf_j.is_writeable = True

            _d____y___bd += ___ly__xuf_j.to_bytes()
        

        if self.__y__kwxb___ > 0:
        
            _y_l_f_ib_r_ = Property()
            _y_l_f_ib_r_.tag = 0x10800003
            _y_l_f_ib_r_.type = PropertyType.INTEGER_32
            _y_l_f_ib_r_.value = int.to_bytes(self.__y__kwxb___, 4, "little")
            _y_l_f_ib_r_.is_readable = True
            _y_l_f_ib_r_.is_writeable = True

            _d____y___bd += _y_l_f_ib_r_.to_bytes()
        

        if self.c_dv__cjvvx_ > 0:
        
            r_d__uad____ = Property()
            r_d__uad____.tag = 0x0E080003
            r_d__uad____.type = PropertyType.INTEGER_32
            r_d__uad____.value = int.to_bytes(self.c_dv__cjvvx_, 4, "little")
            r_d__uad____.is_readable = True
            r_d__uad____.is_writeable = True

            _d____y___bd += r_d__uad____.to_bytes()
        

        if self.r_w_jc__qzn_ is not None and len(self.r_w_jc__qzn_) > 0:
        
            _b___p__z_vn = Property()
            _b___p__z_vn.tag = 0x0E070003
            _b___p__z_vn.type = PropertyType.INTEGER_32
            _b___p__z_vn.value = int.to_bytes(EnumUtil.parse_message_flag(self.r_w_jc__qzn_), 4, "little")
            _b___p__z_vn.is_readable = True
            _b___p__z_vn.is_writeable = True

            _d____y___bd += _b___p__z_vn.to_bytes()
        

        if self.b_s_cu_d_ovr > 0:
        
            _____fv____x = Property()
            _____fv____x.tag = 0x3FDE0003
            _____fv____x.type = PropertyType.INTEGER_32
            _____fv____x.value = int.to_bytes(self.b_s_cu_d_ovr, 4, "little")
            _____fv____x.is_readable = True
            _____fv____x.is_writeable = True

            _d____y___bd += _____fv____x.to_bytes()
        

        if self.wto_g_dk_qpf is not None:
        
            i___jsjb____ = Stream("__substg1.0_00710102", self.wto_g_dk_qpf)
            n_b__sfzn___.append(i___jsjb____)

            _lh_o_v_oi_m = Property()
            _lh_o_v_oi_m.tag = 0x00710102
            _lh_o_v_oi_m.type = PropertyType.BINARY
            _lh_o_v_oi_m.size = len(self.wto_g_dk_qpf)
            _lh_o_v_oi_m.is_readable = True
            _lh_o_v_oi_m.is_writeable = True

            _d____y___bd += _lh_o_v_oi_m.to_bytes()
        

        if self.____zm_r_ip_:
        
            isw_jy_tcw_i = Property()
            isw_jy_tcw_i.tag = 0x10F4000B
            isw_jy_tcw_i.type = PropertyType.BOOLEAN
            isw_jy_tcw_i.value = int.to_bytes(1,1,"little")
            isw_jy_tcw_i.is_readable = True
            isw_jy_tcw_i.is_writeable = True

            _d____y___bd += isw_jy_tcw_i.to_bytes()
        

        if self.__m__df_ka_l:
        
            __sra_ufo__v = Property()
            __sra_ufo__v.tag = 0x10F6000B
            __sra_ufo__v.type = PropertyType.BOOLEAN
            __sra_ufo__v.value = int.to_bytes(1,1,"little")
            __sra_ufo__v.is_readable = True
            __sra_ufo__v.is_writeable = True

            _d____y___bd += __sra_ufo__v.to_bytes()
        

        if self.veb_bv_____o:
        
            zeq__w_ewwvv = Property()
            zeq__w_ewwvv.tag = 0x10F5000B
            zeq__w_ewwvv.type = PropertyType.BOOLEAN
            zeq__w_ewwvv.value = int.to_bytes(1,1,"little")
            zeq__w_ewwvv.is_readable = True
            zeq__w_ewwvv.is_writeable = True

            _d____y___bd += zeq__w_ewwvv.to_bytes()
        

        if self.i___d_zbbg__:
        
            u__xm_he___i = Property()
            u__xm_he___i.tag = 0x10F2000B
            u__xm_he___i.type = PropertyType.BOOLEAN
            u__xm_he___i.value = int.to_bytes(1,1,"little")
            u__xm_he___i.is_readable = True
            u__xm_he___i.is_writeable = True

            _d____y___bd += u__xm_he___i.to_bytes()
        

        if len(self.j____d____c_) > 0:
        
            jk__i_wc_dbz = Property()
            jk__i_wc_dbz.tag = 0x0E1B000B
            jk__i_wc_dbz.type = PropertyType.BOOLEAN
            jk__i_wc_dbz.value = int.to_bytes(1,1,"little")
            jk__i_wc_dbz.is_readable = True
            jk__i_wc_dbz.is_writeable = True

            _d____y___bd += jk__i_wc_dbz.to_bytes()
        

        if self._h_____pvsgq:
        
            e_m_ymrr_ob_ = Property()
            e_m_ymrr_ob_.tag = 0x0E1F000B
            e_m_ymrr_ob_.type = PropertyType.BOOLEAN
            e_m_ymrr_ob_.value = int.to_bytes(1,1,"little")
            e_m_ymrr_ob_.is_readable = True
            e_m_ymrr_ob_.is_writeable = True

            _d____y___bd += e_m_ymrr_ob_.to_bytes()
        

        if self._qvy_dii__st:
        
            i__bkuk__d__ = Property()
            i__bkuk__d__.tag = 0x0029000B
            i__bkuk__d__.type = PropertyType.BOOLEAN
            i__bkuk__d__.value = int.to_bytes(1,1,"little")
            i__bkuk__d__.is_readable = True
            i__bkuk__d__.is_writeable = True

            _d____y___bd += i__bkuk__d__.to_bytes()
        

        if self.________k___:
        
            _b___q______ = Property()
            _b___q______.tag = 0x0023000B
            _b___q______.type = PropertyType.BOOLEAN
            _b___q______.value = int.to_bytes(1,1,"little")
            _b___q______.is_readable = True
            _b___q______.is_writeable = True

            _d____y___bd += _b___q______.to_bytes()
        

        if self.j_ka_nrf____ is not None:
        
            ___of__j_m__ = Stream("__substg1.0_10130102", self.j_ka_nrf____)
            n_b__sfzn___.append(___of__j_m__)

            _oj_jjc_f__s = Property()
            _oj_jjc_f__s.tag = 0x10130102
            _oj_jjc_f__s.type = PropertyType.BINARY
            _oj_jjc_f__s.size = len(self.j_ka_nrf____)
            _oj_jjc_f__s.is_readable = True
            _oj_jjc_f__s.is_writeable = True

            _d____y___bd += _oj_jjc_f__s.to_bytes()
        

        if self._g_h__sre__k is not Sensitivity.NONE:
        
            _a___t___cit = Property()
            _a___t___cit.tag = 0x00360003
            _a___t___cit.type = PropertyType.INTEGER_32
            _a___t___cit.value = int.to_bytes(EnumUtil.parse_sensitivity(self._g_h__sre__k), 4, "little")
            _a___t___cit.is_readable = True
            _a___t___cit.is_writeable = True

            _d____y___bd += _a___t___cit.to_bytes()
        

        if self.i__n____fy__ is not LastVerbExecuted.NONE:
        
            __j__f___wp_ = Property()
            __j__f___wp_.tag = 0x10810003
            __j__f___wp_.type = PropertyType.INTEGER_32
            __j__f___wp_.value = int.to_bytes(EnumUtil.parse_last_verb_executed(self.i__n____fy__), 4, "little")
            __j__f___wp_.is_readable = True
            __j__f___wp_.is_writeable = True

            _d____y___bd += __j__f___wp_.to_bytes()
        

        if self.___ot__i_wup is not Importance.NONE:
        
            r___i_jx__ws = Property()
            r___i_jx__ws.tag = 0x00170003
            r___i_jx__ws.type = PropertyType.INTEGER_32
            r___i_jx__ws.value = int.to_bytes(EnumUtil.parse_importance(self.___ot__i_wup), 4, "little")
            r___i_jx__ws.is_readable = True
            r___i_jx__ws.is_writeable = True

            _d____y___bd += r___i_jx__ws.to_bytes()
        

        if self._ff___oikg_n is not Priority.NONE:
        
            _i_w_vq_o__s = Property()
            _i_w_vq_o__s.tag = 0x00260003
            _i_w_vq_o__s.type = PropertyType.INTEGER_32
            _i_w_vq_o__s.value = int.to_bytes(EnumUtil.parse_priority(self._ff___oikg_n), 4, "little")
            _i_w_vq_o__s.is_readable = True
            _i_w_vq_o__s.is_writeable = True

            _d____y___bd += _i_w_vq_o__s.to_bytes()
        

        if self._dhn__eqsl_x is not FlagIcon.NONE:
        
            _fqf__z__hlb = Property()
            _fqf__z__hlb.tag = 0x10950003
            _fqf__z__hlb.type = PropertyType.INTEGER_32
            _fqf__z__hlb.value = int.to_bytes(EnumUtil.parse_flag_icon(self._dhn__eqsl_x), 4, "little")
            _fqf__z__hlb.is_readable = True
            _fqf__z__hlb.is_writeable = True

            _d____y___bd += _fqf__z__hlb.to_bytes()
        

        if self.j_e_m__r_qgm is not FlagStatus.NONE:
        
            d_w_l_n____u = Property()
            d_w_l_n____u.tag = 0x10900003
            d_w_l_n____u.type = PropertyType.INTEGER_32
            d_w_l_n____u.value = int.to_bytes(EnumUtil.parse_flag_status(self.j_e_m__r_qgm), 4, "little")
            d_w_l_n____u.is_readable = True
            d_w_l_n____u.is_writeable = True

            _d____y___bd += d_w_l_n____u.to_bytes()
        

        if self.uubu___mqh__ is not ObjectType.NONE:
        
            _wm___g_s__j = Property()
            _wm___g_s__j.tag = 0x0FFE0003
            _wm___g_s__j.type = PropertyType.INTEGER_32
            _wm___g_s__j.value = int.to_bytes(EnumUtil.parse_object_type(self.uubu___mqh__), 4, "little")
            _wm___g_s__j.is_readable = True
            _wm___g_s__j.is_writeable = True

            _d____y___bd += _wm___g_s__j.to_bytes()
        

        if self._dn_pem__l__ is not None:
        
            ______o_kz__ = self._dn_pem__l__.encode(self._gm_g__n___a)
            _b___ud_so_t = Stream("__substg1.0_0077" + self._e_p_wn___m_, ______o_kz__)
            n_b__sfzn___.append(_b___ud_so_t)

            __fmim_nh_om = Property()
            __fmim_nh_om.tag = 0x0077 << 16 | self.sll__adckt__
            __fmim_nh_om.type = PropertyType.STRING_8
            __fmim_nh_om.size = len(______o_kz__) + mkkh___d_lvf
            __fmim_nh_om.is_readable = True
            __fmim_nh_om.is_writeable = True

            _d____y___bd += __fmim_nh_om.to_bytes()
        

        if self.li_leu_wgzg_ is not None:
        
            a_lma__i____ = self.li_leu_wgzg_.encode(self._gm_g__n___a)
            __t_d_s___j_ = Stream("__substg1.0_0078" + self._e_p_wn___m_, a_lma__i____)
            n_b__sfzn___.append(__t_d_s___j_)

            _pd___y_r___ = Property()
            _pd___y_r___.tag = 0x0078 << 16 | self.sll__adckt__
            _pd___y_r___.type = PropertyType.STRING_8
            _pd___y_r___.size = len(a_lma__i____) + mkkh___d_lvf
            _pd___y_r___.is_readable = True
            _pd___y_r___.is_writeable = True

            _d____y___bd += _pd___y_r___.to_bytes()
        

        if self._vezy_n_ikln is not None:
        
            ___v_wvp_s_r = Stream("__substg1.0_00430102", self._vezy_n_ikln)
            n_b__sfzn___.append(___v_wvp_s_r)

            c_bckgbz_s_h = Property()
            c_bckgbz_s_h.tag = 0x00430102
            c_bckgbz_s_h.type = PropertyType.BINARY
            c_bckgbz_s_h.size = len(self._vezy_n_ikln)
            c_bckgbz_s_h.is_readable = True
            c_bckgbz_s_h.is_writeable = True

            _d____y___bd += c_bckgbz_s_h.to_bytes()
        

        if self.q__q_k_r_cw_ is not None:
        
            xk_b_t__p___ = self.q__q_k_r_cw_.encode(self._gm_g__n___a)
            bd_sy_fq___c = Stream("__substg1.0_0044" + self._e_p_wn___m_, xk_b_t__p___)
            n_b__sfzn___.append(bd_sy_fq___c)

            _e__g___se__ = Property()
            _e__g___se__.tag = 0x0044 << 16 | self.sll__adckt__
            _e__g___se__.type = PropertyType.STRING_8
            _e__g___se__.size = len(xk_b_t__p___) + mkkh___d_lvf
            _e__g___se__.is_readable = True
            _e__g___se__.is_writeable = True

            _d____y___bd += _e__g___se__.to_bytes()
        

        if self.i_r___noho_c is not None:
        
            gyrot_q__n__ = Stream("__substg1.0_00520102", self.i_r___noho_c)
            n_b__sfzn___.append(gyrot_q__n__)

            d__p__yxa_pq = Property()
            d__p__yxa_pq.tag = 0x00520102
            d__p__yxa_pq.type = PropertyType.BINARY
            d__p__yxa_pq.size = len(self.i_r___noho_c)
            d__p__yxa_pq.is_readable = True
            d__p__yxa_pq.is_writeable = True

            _d____y___bd += d__p__yxa_pq.to_bytes()
        

        if self._ze__u_auq__ is not None:
        
            x_y__wzp_g_n = self._ze__u_auq__.encode(self._gm_g__n___a)
            _f_______k__ = Stream("__substg1.0_0075" + self._e_p_wn___m_, x_y__wzp_g_n)
            n_b__sfzn___.append(_f_______k__)

            mv_h_a___tjt = Property()
            mv_h_a___tjt.tag = 0x0075 << 16 | self.sll__adckt__
            mv_h_a___tjt.type = PropertyType.STRING_8
            mv_h_a___tjt.size = len(x_y__wzp_g_n) + mkkh___d_lvf
            mv_h_a___tjt.is_readable = True
            mv_h_a___tjt.is_writeable = True

            _d____y___bd += mv_h_a___tjt.to_bytes()
        

        if self.g__nj___m__u is not None:
        
            uw____uk_e_p = self.g__nj___m__u.encode(self._gm_g__n___a)
            c____uy__b_h = Stream("__substg1.0_0076" + self._e_p_wn___m_, uw____uk_e_p)
            n_b__sfzn___.append(c____uy__b_h)

            _u___g____ej = Property()
            _u___g____ej.tag = 0x0076 << 16 | self.sll__adckt__
            _u___g____ej.type = PropertyType.STRING_8
            _u___g____ej.size = len(uw____uk_e_p) + mkkh___d_lvf
            _u___g____ej.is_readable = True
            _u___g____ej.is_writeable = True

            _d____y___bd += _u___g____ej.to_bytes()
        

        if self.k_l_bco_s_jv is not None:
        
            _____k____a_ = Stream("__substg1.0_003F0102", self.k_l_bco_s_jv)
            n_b__sfzn___.append(_____k____a_)

            wwa_z_zy__fl = Property()
            wwa_z_zy__fl.tag = 0x003F0102
            wwa_z_zy__fl.type = PropertyType.BINARY
            wwa_z_zy__fl.size = len(self.k_l_bco_s_jv)
            wwa_z_zy__fl.is_readable = True
            wwa_z_zy__fl.is_writeable = True

            _d____y___bd += wwa_z_zy__fl.to_bytes()
        

        if self.__xh_ve_____ is not None:
        
            dj_qc_f__cs_ = self.__xh_ve_____.encode(self._gm_g__n___a)
            i_j___zaxcvd = Stream("__substg1.0_0040" + self._e_p_wn___m_, dj_qc_f__cs_)
            n_b__sfzn___.append(i_j___zaxcvd)

            og_l__v_ubj_ = Property()
            og_l__v_ubj_.tag = 0x0040 << 16 | self.sll__adckt__
            og_l__v_ubj_.type = PropertyType.STRING_8
            og_l__v_ubj_.size = len(dj_qc_f__cs_) + mkkh___d_lvf
            og_l__v_ubj_.is_readable = True
            og_l__v_ubj_.is_writeable = True

            _d____y___bd += og_l__v_ubj_.to_bytes()
        

        if self.____uw__pp__ is not None:
        
            o__rdj_vwcu_ = Stream("__substg1.0_00510102", self.____uw__pp__)
            n_b__sfzn___.append(o__rdj_vwcu_)

            sehx___b_otk = Property()
            sehx___b_otk.tag = 0x00510102
            sehx___b_otk.type = PropertyType.BINARY
            sehx___b_otk.size = len(self.____uw__pp__)
            sehx___b_otk.is_readable = True
            sehx___b_otk.is_writeable = True

            _d____y___bd += sehx___b_otk.to_bytes()
        

        if self.___onygff_yd is not None:
        
            v_u__h__c_gx = self.___onygff_yd.encode(self._gm_g__n___a)
            _y______dkq_ = Stream("__substg1.0_0C1E" + self._e_p_wn___m_, v_u__h__c_gx)
            n_b__sfzn___.append(_y______dkq_)

            k__ha_r____p = Property()
            k__ha_r____p.tag = 0x0C1E << 16 | self.sll__adckt__
            k__ha_r____p.type = PropertyType.STRING_8
            k__ha_r____p.size = len(v_u__h__c_gx) + mkkh___d_lvf
            k__ha_r____p.is_readable = True
            k__ha_r____p.is_writeable = True

            _d____y___bd += k__ha_r____p.to_bytes()
        

        if self._p_y__of_ma_ is not None:
        
            ___p_ysmu_i_ = self._p_y__of_ma_.encode(self._gm_g__n___a)
            qqm___s__o__ = Stream("__substg1.0_0C1F" + self._e_p_wn___m_, ___p_ysmu_i_)
            n_b__sfzn___.append(qqm___s__o__)

            ______v___lp = Property()
            ______v___lp.tag = 0x0C1F << 16 | self.sll__adckt__
            ______v___lp.type = PropertyType.STRING_8
            ______v___lp.size = len(___p_ysmu_i_) + mkkh___d_lvf
            ______v___lp.is_readable = True
            ______v___lp.is_writeable = True

            _d____y___bd += ______v___lp.to_bytes()
        

        if self.p_k_wh_____c is not None:
        
            x__r__kaw_qt = self.p_k_wh_____c.encode(self._gm_g__n___a)
            d__tf_f_u_n_ = Stream("__substg1.0_5D01" + self._e_p_wn___m_, x__r__kaw_qt)
            n_b__sfzn___.append(d__tf_f_u_n_)

            _ytlu__rb_di = Property()
            _ytlu__rb_di.tag = 0x5D01 << 16 | self.sll__adckt__
            _ytlu__rb_di.type = PropertyType.STRING_8
            _ytlu__rb_di.size = len(x__r__kaw_qt) + mkkh___d_lvf
            _ytlu__rb_di.is_readable = True
            _ytlu__rb_di.is_writeable = True

            _d____y___bd += _ytlu__rb_di.to_bytes()
        

        if self.___yu____xb_ is not None:
        
            _il_u_iv__sx = Stream("__substg1.0_0C190102", self.___yu____xb_)
            n_b__sfzn___.append(_il_u_iv__sx)

            d__g____p___ = Property()
            d__g____p___.tag = 0x0C190102
            d__g____p___.type = PropertyType.BINARY
            d__g____p___.size = len(self.___yu____xb_)
            d__g____p___.is_readable = True
            d__g____p___.is_writeable = True

            _d____y___bd += d__g____p___.to_bytes()
        

        if self.___xm__ne_t_ is not None:
        
            rmq_r__bn_ph = self.___xm__ne_t_.encode(self._gm_g__n___a)
            gnmw__te_j__ = Stream("__substg1.0_0C1A" + self._e_p_wn___m_, rmq_r__bn_ph)
            n_b__sfzn___.append(gnmw__te_j__)

            __tvky__n_ld = Property()
            __tvky__n_ld.tag = 0x0C1A << 16 | self.sll__adckt__
            __tvky__n_ld.type = PropertyType.STRING_8
            __tvky__n_ld.size = len(rmq_r__bn_ph) + mkkh___d_lvf
            __tvky__n_ld.is_readable = True
            __tvky__n_ld.is_writeable = True

            _d____y___bd += __tvky__n_ld.to_bytes()
        

        if self.___s_iffiu__ is not None:
        
            _mr_ve__r___ = Stream("__substg1.0_0C1D0102", self.___s_iffiu__)
            n_b__sfzn___.append(_mr_ve__r___)

            __ur__iu_a__ = Property()
            __ur__iu_a__.tag = 0x0C1D0102
            __ur__iu_a__.type = PropertyType.BINARY
            __ur__iu_a__.size = len(self.___s_iffiu__)
            __ur__iu_a__.is_readable = True
            __ur__iu_a__.is_writeable = True

            _d____y___bd += __ur__iu_a__.to_bytes()
        

        if self.__w_y_scz_u_ is not None:
        
            qevm____n__h = self.__w_y_scz_u_.encode(self._gm_g__n___a)
            _i_g__t_n_e_ = Stream("__substg1.0_0064" + self._e_p_wn___m_, qevm____n__h)
            n_b__sfzn___.append(_i_g__t_n_e_)

            m_l_m__sm__b = Property()
            m_l_m__sm__b.tag = 0x0064 << 16 | self.sll__adckt__
            m_l_m__sm__b.type = PropertyType.STRING_8
            m_l_m__sm__b.size = len(qevm____n__h) + mkkh___d_lvf
            m_l_m__sm__b.is_readable = True
            m_l_m__sm__b.is_writeable = True

            _d____y___bd += m_l_m__sm__b.to_bytes()
        

        if self.______z_____ is not None:
        
            vv_b_p__fz__ = self.______z_____.encode(self._gm_g__n___a)
            __qy_i__izcp = Stream("__substg1.0_0065" + self._e_p_wn___m_, vv_b_p__fz__)
            n_b__sfzn___.append(__qy_i__izcp)

            ___gmo_m__kt = Property()
            ___gmo_m__kt.tag = 0x0065 << 16 | self.sll__adckt__
            ___gmo_m__kt.type = PropertyType.STRING_8
            ___gmo_m__kt.size = len(vv_b_p__fz__) + mkkh___d_lvf
            ___gmo_m__kt.is_readable = True
            ___gmo_m__kt.is_writeable = True

            _d____y___bd += ___gmo_m__kt.to_bytes()
        

        if self.y______e___l is not None:
        
            ___p_pm__fm_ = self.y______e___l.encode(self._gm_g__n___a)
            qa_g_ac_rprm = Stream("__substg1.0_5D02" + self._e_p_wn___m_, ___p_pm__fm_)
            n_b__sfzn___.append(qa_g_ac_rprm)

            w_pvaa_s____ = Property()
            w_pvaa_s____.tag = 0x5D02 << 16 | self.sll__adckt__
            w_pvaa_s____.type = PropertyType.STRING_8
            w_pvaa_s____.size = len(___p_pm__fm_) + mkkh___d_lvf
            w_pvaa_s____.is_readable = True
            w_pvaa_s____.is_writeable = True

            _d____y___bd += w_pvaa_s____.to_bytes()
        

        if self.dqgxw_hnt__k is not None:
        
            g________iji = Stream("__substg1.0_00410102", self.dqgxw_hnt__k)
            n_b__sfzn___.append(g________iji)

            l_____ym__o_ = Property()
            l_____ym__o_.tag = 0x00410102
            l_____ym__o_.type = PropertyType.BINARY
            l_____ym__o_.size = len(self.dqgxw_hnt__k)
            l_____ym__o_.is_readable = True
            l_____ym__o_.is_writeable = True

            _d____y___bd += l_____ym__o_.to_bytes()
        

        if self._o_wcivl____ is not None:
        
            __x__p_xr___ = self._o_wcivl____.encode(self._gm_g__n___a)
            _sz____q____ = Stream("__substg1.0_0042" + self._e_p_wn___m_, __x__p_xr___)
            n_b__sfzn___.append(_sz____q____)

            ax__re___nqc = Property()
            ax__re___nqc.tag = 0x0042 << 16 | self.sll__adckt__
            ax__re___nqc.type = PropertyType.STRING_8
            ax__re___nqc.size = len(__x__p_xr___) + mkkh___d_lvf
            ax__re___nqc.is_readable = True
            ax__re___nqc.is_writeable = True

            _d____y___bd += ax__re___nqc.to_bytes()
        

        if self.__dq___iif_g is not None:
        
            _z_vnxvx_nys = Stream("__substg1.0_003B0102", self.__dq___iif_g)
            n_b__sfzn___.append(_z_vnxvx_nys)

            m_k__sus__st = Property()
            m_k__sus__st.tag = 0x003B0102
            m_k__sus__st.type = PropertyType.BINARY
            m_k__sus__st.size = len(self.__dq___iif_g)
            m_k__sus__st.is_readable = True
            m_k__sus__st.is_writeable = True

            _d____y___bd += m_k__sus__st.to_bytes()
        

        if self.___i___cdtv_ is not None:
        
            x____jtl_tep = self.___i___cdtv_.encode(self._gm_g__n___a)
            vhf____ua_g_ = Stream("__substg1.0_007D" + self._e_p_wn___m_, x____jtl_tep)
            n_b__sfzn___.append(vhf____ua_g_)

            o__f___q___e = Property()
            o__f___q___e.tag = 0x007D << 16 | self.sll__adckt__
            o__f___q___e.type = PropertyType.STRING_8
            o__f___q___e.size = len(x____jtl_tep) + mkkh___d_lvf
            o__f___q___e.is_readable = True
            o__f___q___e.is_writeable = True

            _d____y___bd += o__f___q___e.to_bytes()
        

        if self.___r_____tvp is not None:
        
            gd___e_az_nr = NamedProperty()
            gd___e_az_nr.id = 0x8554
            gd___e_az_nr.guid = StandardPropertySet.COMMON
            gd___e_az_nr.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, gd___e_az_nr)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(gd___e_az_nr)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __b___vx_jf_ = self.___r_____tvp.encode(self._gm_g__n___a)
            _yi__pw__s_l = Stream("__substg1.0_" + ____w_ah__g_, __b___vx_jf_)
            n_b__sfzn___.append(_yi__pw__s_l)

            ve________ov = Property()
            ve________ov.tag = ezi__t__sl__
            ve________ov.type = PropertyType.STRING_8
            ve________ov.size = len(__b___vx_jf_) + mkkh___d_lvf
            ve________ov.is_readable = True
            ve________ov.is_writeable = True

            _d____y___bd += ve________ov.to_bytes()
        

        if self._hv_i__xj___ > 0:
        
            __s___d_r_i_ = NamedProperty()
            __s___d_r_i_.id = 0x8552
            __s___d_r_i_.guid = StandardPropertySet.COMMON
            __s___d_r_i_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __s___d_r_i_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__s___d_r_i_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            __n__b_ca___ = Property()
            __n__b_ca___.tag = ezi__t__sl__
            __n__b_ca___.type = PropertyType.INTEGER_32
            __n__b_ca___.value = int.to_bytes(self._hv_i__xj___, 4, "little")
            __n__b_ca___.is_readable = True
            __n__b_ca___.is_writeable = True

            _d____y___bd += __n__b_ca___.to_bytes()
        

        if self.cr_xv___r_qv > datetime.datetime(1901,1,1):
        
            __w_s__s__cn = NamedProperty()
            __w_s__s__cn.id = 0x8516
            __w_s__s__cn.guid = StandardPropertySet.COMMON
            __w_s__s__cn.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __w_s__s__cn)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__w_s__s__cn)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            
            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.cr_xv___r_qv - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            ___mwe___zci = Property()
            ___mwe___zci.tag = ezi__t__sl__
            ___mwe___zci.type = PropertyType.TIME
            ___mwe___zci.value = __cwx_qbk___
            ___mwe___zci.is_readable = True
            ___mwe___zci.is_writeable = True

            _d____y___bd += ___mwe___zci.to_bytes()
        

        if self.egv____dws__ > datetime.datetime(1901,1,1):
        
            qiu_v__uv_m_ = NamedProperty()
            qiu_v__uv_m_.id = 0x8517
            qiu_v__uv_m_.guid = StandardPropertySet.COMMON
            qiu_v__uv_m_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, qiu_v__uv_m_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(qiu_v__uv_m_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.egv____dws__ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            i_tnclu_o___ = Property()
            i_tnclu_o___.tag = ezi__t__sl__
            i_tnclu_o___.type = PropertyType.TIME
            i_tnclu_o___.value = __cwx_qbk___
            i_tnclu_o___.is_readable = True
            i_tnclu_o___.is_writeable = True

            _d____y___bd += i_tnclu_o___.to_bytes()
        

        if self._i_n________ > datetime.datetime(1901,1,1):
        
            __ewm___duk_ = NamedProperty()
            __ewm___duk_.id = 0x8560
            __ewm___duk_.guid = StandardPropertySet.COMMON
            __ewm___duk_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __ewm___duk_)

            if _tgs__ywd___ == -1:

                __d_v___a_yf.append(__ewm___duk_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1          

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self._i_n________ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            v__j___wzj__ = Property()
            v__j___wzj__.tag = ezi__t__sl__
            v__j___wzj__.type = PropertyType.TIME
            v__j___wzj__.value = __cwx_qbk___
            v__j___wzj__.is_readable = True
            v__j___wzj__.is_writeable = True

            _d____y___bd += v__j___wzj__.to_bytes()
        

        if len(self.k__q__s__kb_) > 0:
        
            _____vm_o_fp = NamedProperty()
            _____vm_o_fp.id = 0x8539
            _____vm_o_fp.guid = StandardPropertySet.COMMON
            _____vm_o_fp.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _____vm_o_fp)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_____vm_o_fp)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.__e_ylz_t_hl
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            tgz__qsa_e_d = bytearray()

            for i in range(len(self.k__q__s__kb_)):
            
                r_e__vl__n_m = (self.k__q__s__kb_[i] + "\0").encode(self._gm_g__n___a)
                r_c__f_f_iit = len(r_e__vl__n_m)
                kn__y___efn_ = int.to_bytes(r_c__f_f_iit, 4, "little")

                tgz__qsa_e_d += kn__y___efn_

                _gfd_hthczv_ = "__substg1.0_" + ____w_ah__g_ + "-" + str.format("{:08X}", i)

                u__x_o_as_pq = Stream(_gfd_hthczv_, r_e__vl__n_m)
                n_b__sfzn___.append(u__x_o_as_pq)
            

            _t__ib_f_x__ = bytes(tgz__qsa_e_d)

            _s_l_v_hss_m = Stream("__substg1.0_" + ____w_ah__g_, _t__ib_f_x__)
            n_b__sfzn___.append(_s_l_v_hss_m)

            _____p___aqr = Property()
            _____p___aqr.tag = ezi__t__sl__
            _____p___aqr.type = PropertyType.MULTIPLE_STRING_8
            _____p___aqr.size = len(_t__ib_f_x__)
            _____p___aqr.is_readable = True
            _____p___aqr.is_writeable = True

            _d____y___bd += _____p___aqr.to_bytes()
        

        if len(self._ycq__y_lj__) > 0:
        
            qa_____o_qn_ = NamedProperty()
            qa_____o_qn_.id = 0x853A
            qa_____o_qn_.guid = StandardPropertySet.COMMON
            qa_____o_qn_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, qa_____o_qn_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(qa_____o_qn_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.__e_ylz_t_hl
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            z_____oo_n__ = bytearray()

            for i in range(len(self._ycq__y_lj__)):
            
                _gz__m_g_dw_ = (self._ycq__y_lj__[i] + "\0").encode(self._gm_g__n___a)
                r_c__f_f_iit = len(_gz__m_g_dw_)
                kn__y___efn_ = int.to_bytes(r_c__f_f_iit, 4, "little")

                z_____oo_n__ += kn__y___efn_

                _gfd_hthczv_ = "__substg1.0_" + ____w_ah__g_ + "-" + str.format("{:08X}", i)

                b_x_cet_ume_ = Stream(_gfd_hthczv_, _gz__m_g_dw_)
                n_b__sfzn___.append(b_x_cet_ume_)
            

            hwknwds____o = bytes(z_____oo_n__)

            v__p_u_lqczr = Stream("__substg1.0_" + ____w_ah__g_, hwknwds____o)
            n_b__sfzn___.append(v__p_u_lqczr)

            po_l_ft_qnk_ = Property()
            po_l_ft_qnk_.tag = ezi__t__sl__
            po_l_ft_qnk_.type = PropertyType.MULTIPLE_STRING_8
            po_l_ft_qnk_.size = len(hwknwds____o)
            po_l_ft_qnk_.is_readable = True
            po_l_ft_qnk_.is_writeable = True

            _d____y___bd += po_l_ft_qnk_.to_bytes()
        

        if len(self.v__c___fhx_s) > 0:
        
            _z_d_sehj_t_ = NamedProperty()
            _z_d_sehj_t_.Name = "Keywords"
            _z_d_sehj_t_.guid = StandardPropertySet.PUBLIC_STRINGS
            _z_d_sehj_t_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _z_d_sehj_t_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_z_d_sehj_t_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.__e_ylz_t_hl
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __uc___i_ww_ = bytearray()

            for i in range(len(self.v__c___fhx_s)):
            
                __ocizpn__m_ = (self.v__c___fhx_s[i] + "\0").encode(self._gm_g__n___a)
                r_c__f_f_iit = len(__ocizpn__m_)
                kn__y___efn_ = int.to_bytes(r_c__f_f_iit, 4, "little")

                __uc___i_ww_ += kn__y___efn_

                _gfd_hthczv_ = "__substg1.0_" + ____w_ah__g_ + "-" + str.format("{:08X}", i)

                __vsih_____k = Stream(_gfd_hthczv_, __ocizpn__m_)
                n_b__sfzn___.append(__vsih_____k)
            

            __fjou___c__ = bytes(__uc___i_ww_)

            ____y___r_ms = Stream("__substg1.0_" + ____w_ah__g_, __fjou___c__)
            n_b__sfzn___.append(____y___r_ms)

            w__as__dz_t_ = Property()
            w__as__dz_t_.tag = ezi__t__sl__
            w__as__dz_t_.type = PropertyType.MULTIPLE_STRING_8
            w__as__dz_t_.size = len(__fjou___c__)
            w__as__dz_t_.is_readable = True
            w__as__dz_t_.is_writeable = True

            _d____y___bd += w__as__dz_t_.to_bytes()
        

        if self.__c_kkkbm_zh is not None:
        
            e___p__v_j_p = NamedProperty()
            e___p__v_j_p.id = 0x8535
            e___p__v_j_p.guid = StandardPropertySet.COMMON
            e___p__v_j_p.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, e___p__v_j_p)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(e___p__v_j_p)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __zu_l____z_ = self.__c_kkkbm_zh.encode(self._gm_g__n___a)
            t__vrnkbr_gi = Stream("__substg1.0_" + ____w_ah__g_, __zu_l____z_)
            n_b__sfzn___.append(t__vrnkbr_gi)

            y_mb_jpg_h_g = Property()
            y_mb_jpg_h_g.tag = ezi__t__sl__
            y_mb_jpg_h_g.type = PropertyType.STRING_8
            y_mb_jpg_h_g.size = len(__zu_l____z_) + mkkh___d_lvf
            y_mb_jpg_h_g.is_readable = True
            y_mb_jpg_h_g.is_writeable = True

            _d____y___bd += y_mb_jpg_h_g.to_bytes()
        

        if self._______ii___ is not None:
        
            _v_b__cf__fl = NamedProperty()
            _v_b__cf__fl.id = 0x8534
            _v_b__cf__fl.guid = StandardPropertySet.COMMON
            _v_b__cf__fl.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _v_b__cf__fl)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_v_b__cf__fl)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __fxe___h_z_ = self._______ii___.encode(self._gm_g__n___a)
            ____np____aw = Stream("__substg1.0_" + ____w_ah__g_, __fxe___h_z_)
            n_b__sfzn___.append(____np____aw)

            h___bhzdke__ = Property()
            h___bhzdke__.tag = ezi__t__sl__
            h___bhzdke__.type = PropertyType.STRING_8
            h___bhzdke__.size = len(__fxe___h_z_) + mkkh___d_lvf
            h___bhzdke__.is_readable = True
            h___bhzdke__.is_writeable = True

            _d____y___bd += h___bhzdke__.to_bytes()
        

        if self.__wn_______l is not None:
        
            iz___c_dz___ = NamedProperty()
            iz___c_dz___.id = 0x8580
            iz___c_dz___.guid = StandardPropertySet.COMMON
            iz___c_dz___.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, iz___c_dz___)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(iz___c_dz___)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            q_o_iu_r__p_ = self.__wn_______l.encode(self._gm_g__n___a)
            _____i_____h = Stream("__substg1.0_" + ____w_ah__g_, q_o_iu_r__p_)
            n_b__sfzn___.append(_____i_____h)

            x_husr_n_cz_ = Property()
            x_husr_n_cz_.tag = ezi__t__sl__
            x_husr_n_cz_.type = PropertyType.STRING_8
            x_husr_n_cz_.size = len(q_o_iu_r__p_) + mkkh___d_lvf
            x_husr_n_cz_.is_readable = True
            x_husr_n_cz_.is_writeable = True

            _d____y___bd += x_husr_n_cz_.to_bytes()
        

        if self.z___xyhng_ev is not None:
        
            __rx_r_____g = NamedProperty()
            __rx_r_____g.id = 0x851F
            __rx_r_____g.guid = StandardPropertySet.COMMON
            __rx_r_____g.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __rx_r_____g)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__rx_r_____g)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            jmfbom_f__yw = self.z___xyhng_ev.encode(self._gm_g__n___a)
            ___yji__t_n_ = Stream("__substg1.0_" + ____w_ah__g_, jmfbom_f__yw)
            n_b__sfzn___.append(___yji__t_n_)

            __od_eqrqf__ = Property()
            __od_eqrqf__.tag = ezi__t__sl__
            __od_eqrqf__.type = PropertyType.STRING_8
            __od_eqrqf__.size = len(jmfbom_f__yw) + mkkh___d_lvf
            __od_eqrqf__.is_readable = True
            __od_eqrqf__.is_writeable = True

            _d____y___bd += __od_eqrqf__.to_bytes()
        

        if self.__pmh__t___j:
        
            jwi__c_r_de_ = NamedProperty()
            jwi__c_r_de_.id = 0x8506
            jwi__c_r_de_.guid = StandardPropertySet.COMMON
            jwi__c_r_de_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, jwi__c_r_de_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(jwi__c_r_de_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            jyj_ccw_m___ = Property()
            jyj_ccw_m___.tag = ezi__t__sl__
            jyj_ccw_m___.type = PropertyType.BOOLEAN
            jyj_ccw_m___.value = int.to_bytes(1,1,"little")
            jyj_ccw_m___.is_readable = True
            jyj_ccw_m___.is_writeable = True

            _d____y___bd += jyj_ccw_m___.to_bytes()
        

        if self._y__h_t_h___:
        
            e_p__xs___t_ = NamedProperty()
            e_p__xs___t_.id = 0x851C
            e_p__xs___t_.guid = StandardPropertySet.COMMON
            e_p__xs___t_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, e_p__xs___t_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(e_p__xs___t_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            __fnzpa_fn_c = Property()
            __fnzpa_fn_c.tag = ezi__t__sl__
            __fnzpa_fn_c.type = PropertyType.BOOLEAN
            __fnzpa_fn_c.value = int.to_bytes(1,1,"little")
            __fnzpa_fn_c.is_readable = True
            __fnzpa_fn_c.is_writeable = True

            _d____y___bd += __fnzpa_fn_c.to_bytes()
        

        if self.q___st__n__j:
        
            __bfpr_fpsef = NamedProperty()
            __bfpr_fpsef.id = 0x851E
            __bfpr_fpsef.guid = StandardPropertySet.COMMON
            __bfpr_fpsef.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __bfpr_fpsef)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__bfpr_fpsef) 
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            c_ycbvt_b___ = Property()
            c_ycbvt_b___.tag = ezi__t__sl__
            c_ycbvt_b___.type = PropertyType.BOOLEAN
            c_ycbvt_b___.value = int.to_bytes(1,1,"little")
            c_ycbvt_b___.is_readable = True
            c_ycbvt_b___.is_writeable = True

            _d____y___bd += c_ycbvt_b___.to_bytes()
        

        if self._l__p__mwm_q > datetime.datetime(1901,1,1):
        
            ___nh___op__ = NamedProperty()
            ___nh___op__.id = 0x820D
            ___nh___op__.guid = StandardPropertySet.APPOINTMENT
            ___nh___op__.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___nh___op__)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___nh___op__)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self._l__p__mwm_q - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _o_______ojy = Property()
            _o_______ojy.tag = ezi__t__sl__
            _o_______ojy.type = PropertyType.TIME
            _o_______ojy.value = __cwx_qbk___
            _o_______ojy.is_readable = True
            _o_______ojy.is_writeable = True

            _d____y___bd += _o_______ojy.to_bytes()
        

        if self.__ma_m___ciq > datetime.datetime(1901,1,1):
        
            ____el__va_r = NamedProperty()
            ____el__va_r.id = 0x820E
            ____el__va_r.guid = StandardPropertySet.APPOINTMENT
            ____el__va_r.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ____el__va_r)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(____el__va_r)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.__ma_m___ciq - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            ___a_c_k_x_x = Property()
            ___a_c_k_x_x.tag = ezi__t__sl__
            ___a_c_k_x_x.type = PropertyType.TIME
            ___a_c_k_x_x.value = __cwx_qbk___
            ___a_c_k_x_x.is_readable = True
            ___a_c_k_x_x.is_writeable = True

            _d____y___bd += ___a_c_k_x_x.to_bytes()
        

        if self._____q__c_v_ is not None:
        
            ___o__q___k_ = NamedProperty()
            ___o__q___k_.id = 0x8208
            ___o__q___k_.guid = StandardPropertySet.APPOINTMENT
            ___o__q___k_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___o__q___k_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___o__q___k_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            c__yof____u_ = self._____q__c_v_.encode(self._gm_g__n___a)
            dbgg_f_____r = Stream("__substg1.0_" + ____w_ah__g_, c__yof____u_)
            n_b__sfzn___.append(dbgg_f_____r)

            ____ng_v_g_m = Property()
            ____ng_v_g_m.tag = ezi__t__sl__
            ____ng_v_g_m.type = PropertyType.STRING_8
            ____ng_v_g_m.size = len(c__yof____u_) + mkkh___d_lvf
            ____ng_v_g_m.is_readable = True
            ____ng_v_g_m.is_writeable = True

            _d____y___bd += ____ng_v_g_m.to_bytes()
        

        if self.___d_l___xct is not None:
        
            vuzd____r__q = NamedProperty()
            vuzd____r__q.id = 0x24
            vuzd____r__q.guid = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5])
            vuzd____r__q.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, vuzd____r__q)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(vuzd____r__q)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            e___cvv_i_de = self.___d_l___xct.encode(self._gm_g__n___a)
            n____n_ldih_ = Stream("__substg1.0_" + ____w_ah__g_, e___cvv_i_de)
            n_b__sfzn___.append(n____n_ldih_)

            qs____r_ue__ = Property()
            qs____r_ue__.tag = ezi__t__sl__
            qs____r_ue__.type = PropertyType.STRING_8
            qs____r_ue__.size = len(e___cvv_i_de) + mkkh___d_lvf
            qs____r_ue__.is_readable = True
            qs____r_ue__.is_writeable = True

            _d____y___bd += qs____r_ue__.to_bytes()
        

        if self.____uf_h_uu_ is not None:
        
            _u__ru___ct_ = NamedProperty()
            _u__ru___ct_.id = 0x8234
            _u__ru___ct_.guid = StandardPropertySet.APPOINTMENT
            _u__ru___ct_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _u__ru___ct_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_u__ru___ct_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            ___yfk__n__b = self.____uf_h_uu_.encode(self._gm_g__n___a)
            qnvl_qkscl__ = Stream("__substg1.0_" + ____w_ah__g_, ___yfk__n__b)
            n_b__sfzn___.append(qnvl_qkscl__)

            p_s__x___x_b = Property()
            p_s__x___x_b.tag = ezi__t__sl__
            p_s__x___x_b.type = PropertyType.STRING_8
            p_s__x___x_b.size = len(___yfk__n__b) + mkkh___d_lvf
            p_s__x___x_b.is_readable = True
            p_s__x___x_b.is_writeable = True

            _d____y___bd += p_s__x___x_b.to_bytes()
        

        if self.m__zc_il___y is not None:
        
            mi__ye_o___w = NamedProperty()
            mi__ye_o___w.id = 0x8232
            mi__ye_o___w.guid = StandardPropertySet.APPOINTMENT
            mi__ye_o___w.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, mi__ye_o___w)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(mi__ye_o___w)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _it___j__hb_ = self.m__zc_il___y.encode(self._gm_g__n___a)
            w_zu_____wfp = Stream("__substg1.0_" + ____w_ah__g_, _it___j__hb_)
            n_b__sfzn___.append(w_zu_____wfp)

            mi__ye_o___w = Property()
            mi__ye_o___w.tag = ezi__t__sl__
            mi__ye_o___w.type = PropertyType.STRING_8
            mi__ye_o___w.size = len(_it___j__hb_) + mkkh___d_lvf
            mi__ye_o___w.is_readable = True
            mi__ye_o___w.is_writeable = True

            _d____y___bd += mi__ye_o___w.to_bytes()
        

        if self.__q__v_af___ != BusyStatus.NONE:
        
            ___hl______d = NamedProperty()
            ___hl______d.id = 0x8205
            ___hl______d.guid = StandardPropertySet.APPOINTMENT
            ___hl______d.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___hl______d)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___hl______d)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            _ps____ww_j_ = Property()
            _ps____ww_j_.tag = ezi__t__sl__
            _ps____ww_j_.type = PropertyType.INTEGER_32
            _ps____ww_j_.value = int.to_bytes(EnumUtil.parse_busy_status(self.__q__v_af___), 4, "little")
            _ps____ww_j_.is_readable = True
            _ps____ww_j_.is_writeable = True

            _d____y___bd += _ps____ww_j_.to_bytes()
        

        if self.w_h_gqfnzf_i != MeetingStatus.NONE:
        
            h_f_cs____fr = NamedProperty()
            h_f_cs____fr.id = 0x8217
            h_f_cs____fr.guid = StandardPropertySet.APPOINTMENT
            h_f_cs____fr.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, h_f_cs____fr)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(h_f_cs____fr)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            i___e___b_vq = Property()
            i___e___b_vq.tag = ezi__t__sl__
            i___e___b_vq.type = PropertyType.INTEGER_32
            i___e___b_vq.value = int.to_bytes(EnumUtil.parse_meeting_status(self.w_h_gqfnzf_i), 4, "little")
            i___e___b_vq.is_readable = True
            i___e___b_vq.is_writeable = True

            _d____y___bd += i___e___b_vq.to_bytes()
        

        if self.neh_l__xlj__ != ResponseStatus.NONE:
        
            _t__nst_wa_b = NamedProperty()
            _t__nst_wa_b.id = 0x8218
            _t__nst_wa_b.guid = StandardPropertySet.APPOINTMENT
            _t__nst_wa_b.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _t__nst_wa_b)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_t__nst_wa_b)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            _gp___ue____ = Property()
            _gp___ue____.tag = ezi__t__sl__
            _gp___ue____.type = PropertyType.INTEGER_32
            _gp___ue____.value = int.to_bytes(EnumUtil.parse_response_status(self.neh_l__xlj__), 4, "little")
            _gp___ue____.is_readable = True
            _gp___ue____.is_writeable = True

            _d____y___bd += _gp___ue____.to_bytes()
        

        if self.umc_fo_____x != RecurrenceType.NONE:
        
            _if_hex__c__ = NamedProperty()
            _if_hex__c__.id = 0x8231
            _if_hex__c__.guid = StandardPropertySet.APPOINTMENT
            _if_hex__c__.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _if_hex__c__)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_if_hex__c__)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            h_u___q__odh = Property()
            h_u___q__odh.tag = ezi__t__sl__
            h_u___q__odh.type = PropertyType.INTEGER_32
            h_u___q__odh.value = int.to_bytes(EnumUtil.parse_recurrence_type(self.umc_fo_____x), 4, "little")
            h_u___q__odh.is_readable = True
            h_u___q__odh.is_writeable = True

            _d____y___bd += h_u___q__odh.to_bytes()
        

        if self.____y___frl_ is not None:
        
            u____h__b__x = NamedProperty()
            u____h__b__x.id = 0x3
            u____h__b__x.guid = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5]) 
            u____h__b__x.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, u____h__b__x)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(u____h__b__x)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0102
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _____tdu__n_ = Stream("__substg1.0_" + ____w_ah__g_, self.____y___frl_)
            n_b__sfzn___.append(_____tdu__n_)

            y___rwyjp_my = Property()
            y___rwyjp_my.tag = ezi__t__sl__
            y___rwyjp_my.type = PropertyType.INTEGER_32
            y___rwyjp_my.size = len(self.____y___frl_)
            y___rwyjp_my.is_readable = True
            y___rwyjp_my.is_writeable = True

            _d____y___bd += y___rwyjp_my.to_bytes()
        

        if self._g___ehew___ > -1:
        
            _xe_olfa___z = NamedProperty()
            _xe_olfa___z.id = 0x8214
            _xe_olfa___z.guid = StandardPropertySet.APPOINTMENT
            _xe_olfa___z.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _xe_olfa___z)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_xe_olfa___z)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            __rw_zptmxdr = Property()
            __rw_zptmxdr.tag = ezi__t__sl__
            __rw_zptmxdr.type = PropertyType.INTEGER_32
            __rw_zptmxdr.value = int.to_bytes(self._g___ehew___, 4, "little")
            __rw_zptmxdr.is_readable = True
            __rw_zptmxdr.is_writeable = True

            _d____y___bd += __rw_zptmxdr.to_bytes()
        

        if self.cy__hhh_jv__ > 0:
        
            i___v_____ru = NamedProperty()
            i___v_____ru.id = 0x8213
            i___v_____ru.guid = StandardPropertySet.APPOINTMENT
            i___v_____ru.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, i___v_____ru)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(i___v_____ru)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            _s_q_hpk_fli = Property()
            _s_q_hpk_fli.tag = ezi__t__sl__
            _s_q_hpk_fli.type = PropertyType.INTEGER_32
            _s_q_hpk_fli.value = int.to_bytes(self.cy__hhh_jv__, 4, "little")
            _s_q_hpk_fli.is_readable = True
            _s_q_hpk_fli.is_writeable = True

            _d____y___bd += _s_q_hpk_fli.to_bytes()       


        if self.__wxx__pych_ is not None:
        
            sy____lqt__o = NamedProperty()
            sy____lqt__o.id = 0x811F
            sy____lqt__o.guid = StandardPropertySet.TASK
            sy____lqt__o.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, sy____lqt__o)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(sy____lqt__o)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            vm______o__i = self.__wxx__pych_.encode(self._gm_g__n___a)
            a_n_a_git___ = Stream("__substg1.0_" + ____w_ah__g_, vm______o__i)
            n_b__sfzn___.append(a_n_a_git___)

            __g______z__ = Property()
            __g______z__.tag = ezi__t__sl__
            __g______z__.type = PropertyType.STRING_8
            __g______z__.size = len(vm______o__i) + mkkh___d_lvf
            __g______z__.is_readable = True
            __g______z__.is_writeable = True

            _d____y___bd += __g______z__.to_bytes()
        

        if self.rpu_b_xx__u_ is not None:
        
            u_s_c_d_wgh_ = NamedProperty()
            u_s_c_d_wgh_.id = 0x8121
            u_s_c_d_wgh_.guid = StandardPropertySet.TASK
            u_s_c_d_wgh_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, u_s_c_d_wgh_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(u_s_c_d_wgh_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _p_______vz_ = self.rpu_b_xx__u_.encode(self._gm_g__n___a)
            _r_c_m_ygkgg = Stream("__substg1.0_" + ____w_ah__g_, _p_______vz_)
            n_b__sfzn___.append(_r_c_m_ygkgg)

            ___af_____e_ = Property()
            ___af_____e_.tag = ezi__t__sl__
            ___af_____e_.type = PropertyType.STRING_8
            ___af_____e_.size = len(_p_______vz_) + mkkh___d_lvf
            ___af_____e_.is_readable = True
            ___af_____e_.is_writeable = True

            _d____y___bd += ___af_____e_.to_bytes()
        

        if self.____narlie_r > 0:
        
            _smnlo_hs_q_ = NamedProperty()
            _smnlo_hs_q_.id = 0x8102
            _smnlo_hs_q_.guid = StandardPropertySet.TASK
            _smnlo_hs_q_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _smnlo_hs_q_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_smnlo_hs_q_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0005

            ____k_k_i__n = Property()
            ____k_k_i__n.tag = ezi__t__sl__
            ____k_k_i__n.type = PropertyType.FLOATING_64
            ____k_k_i__n.value = int.to_bytes(0, 8, "little")
            ____k_k_i__n.is_readable = True
            ____k_k_i__n.is_writeable = True

            _d____y___bd += ____k_k_i__n.to_bytes()
        

        if self._m__f_j__e_i > 0:
        
            a_msx__cpy__ = NamedProperty()
            a_msx__cpy__.id = 0x8110
            a_msx__cpy__.guid = StandardPropertySet.TASK
            a_msx__cpy__.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, a_msx__cpy__)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(a_msx__cpy__)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            ___oi____p_r = Property()
            ___oi____p_r.tag = ezi__t__sl__
            ___oi____p_r.type = PropertyType.INTEGER_32
            ___oi____p_r.value = int.to_bytes(self._m__f_j__e_i, 4, "little")
            ___oi____p_r.is_readable = True
            ___oi____p_r.is_writeable = True

            _d____y___bd += ___oi____p_r.to_bytes()
        

        if self.____v_y_n___ > 0:
        
            __od__s__vj_ = NamedProperty()
            __od__s__vj_.id = 0x8111
            __od__s__vj_.guid = StandardPropertySet.TASK
            __od__s__vj_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __od__s__vj_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__od__s__vj_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            ieemg__lv_kt = Property()
            ieemg__lv_kt.tag = ezi__t__sl__
            ieemg__lv_kt.type = PropertyType.INTEGER_32
            ieemg__lv_kt.value = int.to_bytes(self.____v_y_n___, 4, "little")
            ieemg__lv_kt.is_readable = True
            ieemg__lv_kt.is_writeable = True

            _d____y___bd += ieemg__lv_kt.to_bytes()
        

        if self.__hk___s__ux:
        
            kwr__ech____ = NamedProperty()
            kwr__ech____.id = 0x8103
            kwr__ech____.guid = StandardPropertySet.TASK
            kwr__ech____.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, kwr__ech____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(kwr__ech____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            ____u_______ = Property()
            ____u_______.tag = ezi__t__sl__
            ____u_______.type = PropertyType.BOOLEAN
            ____u_______.value = int.to_bytes(1,1,"little")
            ____u_______.is_readable = True
            ____u_______.is_writeable = True

            _d____y___bd += ____u_______.to_bytes()
        

        if self._n_ad___dz__:
        
            _j_qo_q___of = NamedProperty()
            _j_qo_q___of.id = 0x811C
            _j_qo_q___of.guid = StandardPropertySet.TASK
            _j_qo_q___of.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _j_qo_q___of)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_j_qo_q___of)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            __a____ho__l = Property()
            __a____ho__l.tag = ezi__t__sl__
            __a____ho__l.type = PropertyType.BOOLEAN
            __a____ho__l.value = int.to_bytes(1,1,"little")
            __a____ho__l.is_readable = True
            __a____ho__l.is_writeable = True

            _d____y___bd += __a____ho__l.to_bytes()
        

        if self.s__a_____uwe:
        
            ____hgnzq_qn = NamedProperty()
            ____hgnzq_qn.id = 0x8223
            ____hgnzq_qn.guid = StandardPropertySet.APPOINTMENT
            ____hgnzq_qn.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ____hgnzq_qn)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(____hgnzq_qn)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            _a_t_____j_q = Property()
            _a_t_____j_q.tag = ezi__t__sl__
            _a_t_____j_q.type = PropertyType.BOOLEAN
            _a_t_____j_q.value = int.to_bytes(1,1,"little")
            _a_t_____j_q.is_readable = True
            _a_t_____j_q.is_writeable = True

            _d____y___bd += _a_t_____j_q.to_bytes()
        

        if self.sw__fy_____w:
        
            _n_u_c_f_k__ = NamedProperty()
            _n_u_c_f_k__.id = 0x8215
            _n_u_c_f_k__.guid = StandardPropertySet.APPOINTMENT
            _n_u_c_f_k__.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _n_u_c_f_k__)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_n_u_c_f_k__)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            _p___kzwf_mw = Property()
            _p___kzwf_mw.tag = ezi__t__sl__
            _p___kzwf_mw.type = PropertyType.BOOLEAN
            _p___kzwf_mw.value = int.to_bytes(1,1,"little")
            _p___kzwf_mw.is_readable = True
            _p___kzwf_mw.is_writeable = True

            _d____y___bd += _p___kzwf_mw.to_bytes()
        

        if self.il__q_yhe___:
        
            hg_fh_q_s_g_ = NamedProperty()
            hg_fh_q_s_g_.id = 0x8503
            hg_fh_q_s_g_.guid = StandardPropertySet.COMMON
            hg_fh_q_s_g_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, hg_fh_q_s_g_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(hg_fh_q_s_g_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            __nndk_gd__k = Property()
            __nndk_gd__k.tag = ezi__t__sl__
            __nndk_gd__k.type = PropertyType.BOOLEAN
            __nndk_gd__k.value = int.to_bytes(1,1,"little")
            __nndk_gd__k.is_readable = True
            __nndk_gd__k.is_writeable = True

            _d____y___bd += __nndk_gd__k.to_bytes()
        

        if self._fusob_vbnex > datetime.datetime(1901,1,1):
        
            d_wl_r_prv_b = NamedProperty()
            d_wl_r_prv_b.id = 0x8502
            d_wl_r_prv_b.guid = StandardPropertySet.COMMON
            d_wl_r_prv_b.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, d_wl_r_prv_b)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(d_wl_r_prv_b)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self._fusob_vbnex - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _yo_fd__lf__ = Property()
            _yo_fd__lf__.tag = ezi__t__sl__
            _yo_fd__lf__.type = PropertyType.TIME
            _yo_fd__lf__.value = __cwx_qbk___
            _yo_fd__lf__.is_readable = True
            _yo_fd__lf__.is_writeable = True

            _d____y___bd += _yo_fd__lf__.to_bytes()
        

        if self._k__nlldizui > 0:
        
            b_r__v______ = NamedProperty()
            b_r__v______.id = 0x8501
            b_r__v______.guid = StandardPropertySet.COMMON
            b_r__v______.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, b_r__v______)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(b_r__v______)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            _y__l_______ = Property()
            _y__l_______.tag = ezi__t__sl__
            _y__l_______.type = PropertyType.INTEGER_32
            _y__l_______.value = int.to_bytes(self._k__nlldizui, 4, "little")
            _y__l_______.is_readable = True
            _y__l_______.is_writeable = True

            _d____y___bd += _y__l_______.to_bytes()
        

        if self.q________c_r > datetime.datetime(1901,1,1):
        
            __ia_fj___tj = NamedProperty()
            __ia_fj___tj.id = 0x8104
            __ia_fj___tj.guid = StandardPropertySet.TASK
            __ia_fj___tj.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __ia_fj___tj)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__ia_fj___tj)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.q________c_r - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            __d_y_nc_x__ = Property()
            __d_y_nc_x__.tag = ezi__t__sl__
            __d_y_nc_x__.type = PropertyType.TIME
            __d_y_nc_x__.value = __cwx_qbk___
            __d_y_nc_x__.is_readable = True
            __d_y_nc_x__.is_writeable = True

            _d____y___bd += __d_y_nc_x__.to_bytes()
        

        if self.x___asp___iv > datetime.datetime(1901,1,1):
        
            _r___hu_ms_m = NamedProperty()
            _r___hu_ms_m.id = 0x8105
            _r___hu_ms_m.guid = StandardPropertySet.TASK
            _r___hu_ms_m.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _r___hu_ms_m)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_r___hu_ms_m)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.x___asp___iv - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _xt_______lr = Property()
            _xt_______lr.tag = ezi__t__sl__
            _xt_______lr.type = PropertyType.TIME
            _xt_______lr.value = __cwx_qbk___
            _xt_______lr.is_readable = True
            _xt_______lr.is_writeable = True

            _d____y___bd += _xt_______lr.to_bytes()
        

        if self._gfko_gic___ > datetime.datetime(1901,1,1):
        
            y_d_fv_____g = NamedProperty()
            y_d_fv_____g.id = 0x810F
            y_d_fv_____g.guid = StandardPropertySet.TASK
            y_d_fv_____g.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, y_d_fv_____g)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(y_d_fv_____g)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self._gfko_gic___ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _nj__ehbt__z = Property()
            _nj__ehbt__z.tag = ezi__t__sl__
            _nj__ehbt__z.type = PropertyType.TIME
            _nj__ehbt__z.value = __cwx_qbk___
            _nj__ehbt__z.is_readable = True
            _nj__ehbt__z.is_writeable = True

            _d____y___bd += _nj__ehbt__z.to_bytes()
        

        if self.__t___l__g__ != TaskStatus.NONE:

            n__l_m_____x = NamedProperty()
            n__l_m_____x.id = 0x8101
            n__l_m_____x.guid = StandardPropertySet.TASK
            n__l_m_____x.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, n__l_m_____x)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(n__l_m_____x)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            _o_vrx_s___q = Property()
            _o_vrx_s___q.tag = ezi__t__sl__
            _o_vrx_s___q.type = PropertyType.INTEGER_32
            _o_vrx_s___q.value = int.to_bytes(EnumUtil.parse_task_status(self.__t___l__g__), 4, "little")
            _o_vrx_s___q.is_readable = True
            _o_vrx_s___q.is_writeable = True

            _d____y___bd += _o_vrx_s___q.to_bytes()
        

        if self.___pp__l____ != TaskOwnership.NONE:
        
            yo_d___x_pc_ = NamedProperty()
            yo_d___x_pc_.id = 0x8129
            yo_d___x_pc_.guid = StandardPropertySet.TASK
            yo_d___x_pc_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, yo_d___x_pc_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(yo_d___x_pc_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            iv_etk_hke_i = Property()
            iv_etk_hke_i.tag = ezi__t__sl__
            iv_etk_hke_i.type = PropertyType.INTEGER_32
            iv_etk_hke_i.value = int.to_bytes(EnumUtil.parse_task_ownership(self.___pp__l____), 4, "little")
            iv_etk_hke_i.is_readable = True
            iv_etk_hke_i.is_writeable = True

            _d____y___bd += iv_etk_hke_i.to_bytes()
        

        if self._____xn_oymn != TaskDelegationState.NONE:
        
            _mtcxw___y_x = NamedProperty()
            _mtcxw___y_x.id = 0x812A
            _mtcxw___y_x.guid = StandardPropertySet.TASK
            _mtcxw___y_x.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _mtcxw___y_x)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_mtcxw___y_x)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            _s____g_en_y = Property()
            _s____g_en_y.tag = ezi__t__sl__
            _s____g_en_y.type = PropertyType.INTEGER_32
            _s____g_en_y.value = int.to_bytes(EnumUtil.parse_task_delegation_state(self._____xn_oymn), 4, "little")
            _s____g_en_y.is_readable = True
            _s____g_en_y.is_writeable = True

            _d____y___bd += _s____g_en_y.to_bytes()
        

        if self.m_rdx____o__ > 0:
        
            __b_yt_cmbu_ = NamedProperty()
            __b_yt_cmbu_.id = 0x8B05
            __b_yt_cmbu_.guid = StandardPropertySet.NOTE
            __b_yt_cmbu_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __b_yt_cmbu_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__b_yt_cmbu_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            bsh_x__cz__r = Property()
            bsh_x__cz__r.tag = ezi__t__sl__
            bsh_x__cz__r.type = PropertyType.INTEGER_32
            bsh_x__cz__r.value = int.to_bytes(self.m_rdx____o__, 4, "little")
            bsh_x__cz__r.is_readable = True
            bsh_x__cz__r.is_writeable = True

            _d____y___bd += bsh_x__cz__r.to_bytes()
        

        if self._mxah_ge__t_ > 0:
        
            l_____vlkjvy = NamedProperty()
            l_____vlkjvy.id = 0x8B04
            l_____vlkjvy.guid = StandardPropertySet.NOTE
            l_____vlkjvy.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, l_____vlkjvy)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(l_____vlkjvy)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            qd_o_e_amv__ = Property()
            qd_o_e_amv__.tag = ezi__t__sl__
            qd_o_e_amv__.type = PropertyType.INTEGER_32
            qd_o_e_amv__.value = int.to_bytes(self._mxah_ge__t_, 4, "little")
            qd_o_e_amv__.is_readable = True
            qd_o_e_amv__.is_writeable = True

            _d____y___bd += qd_o_e_amv__.to_bytes()
        

        if self.___e_p_s___a > 0:
        
            _z__m_____zv = NamedProperty()
            _z__m_____zv.id = 0x8B03
            _z__m_____zv.guid = StandardPropertySet.NOTE
            _z__m_____zv.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _z__m_____zv)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_z__m_____zv)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            ____ghjs__q_ = Property()
            ____ghjs__q_.tag = ezi__t__sl__
            ____ghjs__q_.type = PropertyType.INTEGER_32
            ____ghjs__q_.value = int.to_bytes(self.___e_p_s___a, 4, "little")
            ____ghjs__q_.is_readable = True
            ____ghjs__q_.is_writeable = True

            _d____y___bd += ____ghjs__q_.to_bytes()
        

        if self._____f_t_h__ > 0:
        
            bo__pu____f_ = NamedProperty()
            bo__pu____f_.id = 0x8B02
            bo__pu____f_.guid = StandardPropertySet.NOTE
            bo__pu____f_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, bo__pu____f_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(bo__pu____f_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            __________a_ = Property()
            __________a_.tag = ezi__t__sl__
            __________a_.type = PropertyType.INTEGER_32
            __________a_.value = int.to_bytes(self._____f_t_h__, 4, "little")
            __________a_.is_readable = True
            __________a_.is_writeable = True

            _d____y___bd += __________a_.to_bytes()
        

        if self.__zuaq___k_g != NoteColor.NONE:
        
            c__wa____n_t = NamedProperty()
            c__wa____n_t.id = 0x8B00
            c__wa____n_t.guid = StandardPropertySet.NOTE
            c__wa____n_t.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, c__wa____n_t)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(c__wa____n_t)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            __m___kcq___ = Property()
            __m___kcq___.tag = ezi__t__sl__
            __m___kcq___.type = PropertyType.INTEGER_32
            __m___kcq___.value = int.to_bytes(EnumUtil.parse_note_color(self.__zuaq___k_g), 4, "little")
            __m___kcq___.is_readable = True
            __m___kcq___.is_writeable = True

            _d____y___bd += __m___kcq___.to_bytes()
        

        if self.c_p_irtpd___ > datetime.datetime(1901,1,1):
        
            _w__n__f_e_b = NamedProperty()
            _w__n__f_e_b.id = 0x8706
            _w__n__f_e_b.guid = StandardPropertySet.JOURNAL
            _w__n__f_e_b.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _w__n__f_e_b)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_w__n__f_e_b)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.c_p_irtpd___ - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            hh___qy_f__h = Property()
            hh___qy_f__h.tag = ezi__t__sl__
            hh___qy_f__h.type = PropertyType.TIME
            hh___qy_f__h.value = __cwx_qbk___
            hh___qy_f__h.is_readable = True
            hh___qy_f__h.is_writeable = True

            _d____y___bd += hh___qy_f__h.to_bytes()
        

        if self.fyg_hq__zqla > datetime.datetime(1901,1,1):
        
            __nb__f_rq_l = NamedProperty()
            __nb__f_rq_l.id = 0x8708
            __nb__f_rq_l.guid = StandardPropertySet.JOURNAL
            __nb__f_rq_l.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __nb__f_rq_l)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__nb__f_rq_l)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0040

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.fyg_hq__zqla - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            ku_____wsu__ = Property()
            ku_____wsu__.tag = ezi__t__sl__
            ku_____wsu__.type = PropertyType.TIME
            ku_____wsu__.value = __cwx_qbk___
            ku_____wsu__.is_readable = True
            ku_____wsu__.is_writeable = True

            _d____y___bd += ku_____wsu__.to_bytes()
        

        if self._n___mr_t_pn is not None:
        
            h_yz_____v__ = NamedProperty()
            h_yz_____v__.id = 0x8700
            h_yz_____v__.guid = StandardPropertySet.JOURNAL
            h_yz_____v__.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, h_yz_____v__)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(h_yz_____v__)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            stg_p___t___ = self._n___mr_t_pn.encode(self._gm_g__n___a)
            _____qdu_s_n = Stream("__substg1.0_" + ____w_ah__g_, stg_p___t___)
            n_b__sfzn___.append(_____qdu_s_n)

            s__g__fn_in_ = Property()
            s__g__fn_in_.tag = ezi__t__sl__
            s__g__fn_in_.type = PropertyType.STRING_8
            s__g__fn_in_.size = len(stg_p___t___) + mkkh___d_lvf
            s__g__fn_in_.is_readable = True
            s__g__fn_in_.is_writeable = True

            _d____y___bd += s__g__fn_in_.to_bytes()
        

        if self.cbw_______xx is not None:
        
            ogqotp_fg_zm = NamedProperty()
            ogqotp_fg_zm.id = 0x8712
            ogqotp_fg_zm.guid = StandardPropertySet.JOURNAL
            ogqotp_fg_zm.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ogqotp_fg_zm)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(ogqotp_fg_zm)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _e__z_gw__fi = self.cbw_______xx.encode(self._gm_g__n___a)
            ___lz__bz_v_ = Stream("__substg1.0_" + ____w_ah__g_, _e__z_gw__fi)
            n_b__sfzn___.append(___lz__bz_v_)

            y___hqk___m_ = Property()
            y___hqk___m_.tag = ezi__t__sl__
            y___hqk___m_.type = PropertyType.STRING_8
            y___hqk___m_.size = len(_e__z_gw__fi) + mkkh___d_lvf
            y___hqk___m_.is_readable = True
            y___hqk___m_.is_writeable = True

            _d____y___bd += y___hqk___m_.to_bytes()
        

        if self.w__c_rjwf_j_ > 0:
        
            _kq_y__xipi_ = NamedProperty()
            _kq_y__xipi_.id = 0x8707
            _kq_y__xipi_.guid = StandardPropertySet.JOURNAL
            _kq_y__xipi_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _kq_y__xipi_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_kq_y__xipi_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            k_____qh_h_z = Property()
            k_____qh_h_z.tag = ezi__t__sl__
            k_____qh_h_z.type = PropertyType.INTEGER_32
            k_____qh_h_z.value = int.to_bytes(self.w__c_rjwf_j_, 4, "little")
            k_____qh_h_z.is_readable = True
            k_____qh_h_z.is_writeable = True

            _d____y___bd += k_____qh_h_z.to_bytes()
        

        if self.f___v_bof__x > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.f___v_bof__x - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            i_z_i__b____ = Property()
            i_z_i__b____.tag = 0x3A420040
            i_z_i__b____.type = PropertyType.TIME
            i_z_i__b____.value = __cwx_qbk___
            i_z_i__b____.is_readable = True
            i_z_i__b____.is_writeable = False

            _d____y___bd += i_z_i__b____.to_bytes()
        

        if len(self.__c__cw_h__a) > 0:
        
            l_ewqv_____z = bytearray()

            for i in range(len(self.__c__cw_h__a)):
            
                _________tl_ = (self.__c__cw_h__a[i] + "\0").encode(self._gm_g__n___a)
                r_c__f_f_iit = len(_________tl_)
                kn__y___efn_ = int.to_bytes(r_c__f_f_iit, 4, "little")

                l_ewqv_____z += kn__y___efn_

                _gfd_hthczv_ = "__substg1.0_3A58" + self.q_rcyqzvz___ + "-" + str.format("{:08X}", i)

                bwv____khhqv = Stream(_gfd_hthczv_, _________tl_)
                n_b__sfzn___.append(bwv____khhqv)
            
            __u_l_____ha = bytes(l_ewqv_____z)

            ____uy__lt__ = Stream("__substg1.0_3A58" + self.q_rcyqzvz___, __u_l_____ha)
            n_b__sfzn___.append(____uy__lt__)

            k_yxw____cl_ = Property()
            k_yxw____cl_.tag = 0x3A58 << 16 | self.__e_ylz_t_hl
            k_yxw____cl_.type = PropertyType.MULTIPLE_STRING_8
            k_yxw____cl_.size = len(__u_l_____ha)
            k_yxw____cl_.is_readable = True
            k_yxw____cl_.is_writeable = True

            _d____y___bd += k_yxw____cl_.to_bytes()
        

        if self.__e__w_t_p_q is not None:
        
            _k_x_ga_b_be = self.__e__w_t_p_q.encode(self._gm_g__n___a)
            fly__qyfl___ = Stream("__substg1.0_3A30" + self._e_p_wn___m_, _k_x_ga_b_be)
            n_b__sfzn___.append(fly__qyfl___)

            _f____g__zv_ = Property()
            _f____g__zv_.tag = 0x3A30 << 16 | self.sll__adckt__
            _f____g__zv_.type = PropertyType.STRING_8
            _f____g__zv_.size = len(_k_x_ga_b_be) + mkkh___d_lvf
            _f____g__zv_.is_readable = True
            _f____g__zv_.is_writeable = True

            _d____y___bd += _f____g__zv_.to_bytes()
        

        if self._f_ha_w___mw is not None:
        
            __y___pxy_bm = self._f_ha_w___mw.encode(self._gm_g__n___a)
            __b___h__p__ = Stream("__substg1.0_3A2E" + self._e_p_wn___m_, __y___pxy_bm)
            n_b__sfzn___.append(__b___h__p__)

            _o_e_sun_l__ = Property()
            _o_e_sun_l__.tag = 0x3A2E << 16 | self.sll__adckt__
            _o_e_sun_l__.type = PropertyType.STRING_8
            _o_e_sun_l__.size = len(__y___pxy_bm) + mkkh___d_lvf
            _o_e_sun_l__.is_readable = True
            _o_e_sun_l__.is_writeable = True

            _d____y___bd += _o_e_sun_l__.to_bytes()
        

        if self.hy_wucpf_c_j is not None:
        
            xf_ol____x__ = self.hy_wucpf_c_j.encode(self._gm_g__n___a)
            ___n____v__j = Stream("__substg1.0_3A1B" + self._e_p_wn___m_, xf_ol____x__)
            n_b__sfzn___.append(___n____v__j)

            _bqi______n_ = Property()
            _bqi______n_.tag = 0x3A1B << 16 | self.sll__adckt__
            _bqi______n_.type = PropertyType.STRING_8
            _bqi______n_.size = len(xf_ol____x__) + mkkh___d_lvf
            _bqi______n_.is_readable = True
            _bqi______n_.is_writeable = True

            _d____y___bd += _bqi______n_.to_bytes()
        

        if self._km___gfyym_ is not None:
        
            ____kxh_____ = self._km___gfyym_.encode(self._gm_g__n___a)
            __hk_d___bu_ = Stream("__substg1.0_3A24" + self._e_p_wn___m_, ____kxh_____)
            n_b__sfzn___.append(__hk_d___bu_)

            c_eb_q_s____ = Property()
            c_eb_q_s____.tag = 0x3A24 << 16 | self.sll__adckt__
            c_eb_q_s____.type = PropertyType.STRING_8
            c_eb_q_s____.size = len(____kxh_____) + mkkh___d_lvf
            c_eb_q_s____.is_readable = True
            c_eb_q_s____.is_writeable = True

            _d____y___bd += c_eb_q_s____.to_bytes()
        

        if self.hhk__zyd_d__ is not None:
        
            c_h_m__q___l = self.hhk__zyd_d__.encode(self._gm_g__n___a)
            _h_r_______u = Stream("__substg1.0_3A51" + self._e_p_wn___m_, c_h_m__q___l)
            n_b__sfzn___.append(_h_r_______u)

            _____x__wnbp = Property()
            _____x__wnbp.tag = 0x3A51 << 16 | self.sll__adckt__
            _____x__wnbp.type = PropertyType.STRING_8
            _____x__wnbp.size = len(c_h_m__q___l) + mkkh___d_lvf
            _____x__wnbp.is_readable = True
            _____x__wnbp.is_writeable = True

            _d____y___bd += _____x__wnbp.to_bytes()
        

        if self.bun___q__o__ is not None:
        
            _nlf_p____i_ = self.bun___q__o__.encode(self._gm_g__n___a)
            ct__nx_o___d = Stream("__substg1.0_3A02" + self._e_p_wn___m_, _nlf_p____i_)
            n_b__sfzn___.append(ct__nx_o___d)

            yubn__ilz_hq = Property()
            yubn__ilz_hq.tag = 0x3A02 << 16 | self.sll__adckt__
            yubn__ilz_hq.type = PropertyType.STRING_8
            yubn__ilz_hq.size = len(_nlf_p____i_) + mkkh___d_lvf
            yubn__ilz_hq.is_readable = True
            yubn__ilz_hq.is_writeable = True

            _d____y___bd += yubn__ilz_hq.to_bytes()
        

        if self.___zpfq_tz__ is not None:
        
            qh____ojfy__ = self.___zpfq_tz__.encode(self._gm_g__n___a)
            _dlkj_a_s___ = Stream("__substg1.0_3A1E" + self._e_p_wn___m_, qh____ojfy__)
            n_b__sfzn___.append(_dlkj_a_s___)

            __uc_uo_dvz_ = Property()
            __uc_uo_dvz_.tag = 0x3A1E << 16 | self.sll__adckt__
            __uc_uo_dvz_.type = PropertyType.STRING_8
            __uc_uo_dvz_.size = len(qh____ojfy__) + mkkh___d_lvf
            __uc_uo_dvz_.is_readable = True
            __uc_uo_dvz_.is_writeable = True

            _d____y___bd += __uc_uo_dvz_.to_bytes()
        

        if self.__x_r_e_yh__ is not None:
        
            _rri__q___ut = self.__x_r_e_yh__.encode(self._gm_g__n___a)
            _g__i__f____ = Stream("__substg1.0_3A1C" + self._e_p_wn___m_, _rri__q___ut)
            n_b__sfzn___.append(_g__i__f____)

            cik____k_s_e = Property()
            cik____k_s_e.tag = 0x3A1C << 16 | self.sll__adckt__
            cik____k_s_e.type = PropertyType.STRING_8
            cik____k_s_e.size = len(_rri__q___ut) + mkkh___d_lvf
            cik____k_s_e.is_readable = True
            cik____k_s_e.is_writeable = True

            _d____y___bd += cik____k_s_e.to_bytes()
        

        if self.q_ob_____ij_ is not None:
        
            yiu_ips____o = self.q_ob_____ij_.encode(self._gm_g__n___a)
            aeptc_r___r_ = Stream("__substg1.0_3A57" + self._e_p_wn___m_, yiu_ips____o)
            n_b__sfzn___.append(aeptc_r___r_)

            n____s____zn = Property()
            n____s____zn.tag = 0x3A57 << 16 | self.sll__adckt__
            n____s____zn.type = PropertyType.STRING_8
            n____s____zn.size = len(yiu_ips____o) + mkkh___d_lvf
            n____s____zn.is_readable = True
            n____s____zn.is_writeable = True

            _d____y___bd += n____s____zn.to_bytes()
        

        if self.__f_fqzb___i is not None:
        
            bwho____x___ = self.__f_fqzb___i.encode(self._gm_g__n___a)
            cc_lrr__z__j = Stream("__substg1.0_3A16" + self._e_p_wn___m_, bwho____x___)
            n_b__sfzn___.append(cc_lrr__z__j)

            d_g__e__y___ = Property()
            d_g__e__y___.tag = 0x3A16 << 16 | self.sll__adckt__
            d_g__e__y___.type = PropertyType.STRING_8
            d_g__e__y___.size = len(bwho____x___) + mkkh___d_lvf
            d_g__e__y___.is_readable = True
            d_g__e__y___.is_writeable = True

            _d____y___bd += d_g__e__y___.to_bytes()
        

        if self.y_b_h___p___ is not None:
        
            iokl_e__t___ = self.y_b_h___p___.encode(self._gm_g__n___a)
            _e_xr____b__ = Stream("__substg1.0_3A49" + self._e_p_wn___m_, iokl_e__t___)
            n_b__sfzn___.append(_e_xr____b__)

            _y_li__j_nx_ = Property()
            _y_li__j_nx_.tag = 0x3A49 << 16 | self.sll__adckt__
            _y_li__j_nx_.type = PropertyType.STRING_8
            _y_li__j_nx_.size = len(iokl_e__t___) + mkkh___d_lvf
            _y_li__j_nx_.is_readable = True
            _y_li__j_nx_.is_writeable = True

            _d____y___bd += _y_li__j_nx_.to_bytes()
        

        if self._e___sik_flm is not None:
        
            _r______d_oa = NamedProperty()
            _r______d_oa.id = 0x8049
            _r______d_oa.guid = StandardPropertySet.ADDRESS
            _r______d_oa.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _r______d_oa)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_r______d_oa)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _z_______cn_ = self._e___sik_flm.encode(self._gm_g__n___a)

            o_af________ = Stream("__substg1.0_" + ____w_ah__g_, _z_______cn_)
            n_b__sfzn___.append(o_af________)

            __tusxf___uq = Property()
            __tusxf___uq.tag = ezi__t__sl__
            __tusxf___uq.type = PropertyType.STRING_8
            __tusxf___uq.size = len(_z_______cn_) + mkkh___d_lvf
            __tusxf___uq.is_readable = True
            __tusxf___uq.is_writeable = True

            _d____y___bd += __tusxf___uq.to_bytes()

            __be_l____q_ = Stream("__substg1.0_3A26" + self._e_p_wn___m_, _z_______cn_)
            n_b__sfzn___.append(__be_l____q_)

            kp___p_ea_k_ = Property()
            kp___p_ea_k_.tag = 0x3A26 << 16 | self.sll__adckt__
            kp___p_ea_k_.type = PropertyType.STRING_8
            kp___p_ea_k_.size = len(_z_______cn_) + mkkh___d_lvf
            kp___p_ea_k_.is_readable = True
            kp___p_ea_k_.is_writeable = True

            _d____y___bd += kp___p_ea_k_.to_bytes()
        

        if self.n____j____xe is not None:
        
            _p__pfd___vf = self.n____j____xe.encode(self._gm_g__n___a)
            _______vxjiu = Stream("__substg1.0_3A4A" + self._e_p_wn___m_, _p__pfd___vf)
            n_b__sfzn___.append(_______vxjiu)

            z__k_ql__j_e = Property()
            z__k_ql__j_e.tag = 0x3A4A << 16 | self.sll__adckt__
            z__k_ql__j_e.type = PropertyType.STRING_8
            z__k_ql__j_e.size = len(_p__pfd___vf) + mkkh___d_lvf
            z__k_ql__j_e.is_readable = True
            z__k_ql__j_e.is_writeable = True

            _d____y___bd += z__k_ql__j_e.to_bytes()
        

        if self.___yr__bvg__ is not None:
        
            _i_tozk__v__ = self.___yr__bvg__.encode(self._gm_g__n___a)
            ____c__l__ua = Stream("__substg1.0_3A18" + self._e_p_wn___m_, _i_tozk__v__)
            n_b__sfzn___.append(____c__l__ua)

            _ii_____ea_j = Property()
            _ii_____ea_j.tag = 0x3A18 << 16 | self.sll__adckt__
            _ii_____ea_j.type = PropertyType.STRING_8
            _ii_____ea_j.size = len(_i_tozk__v__) + mkkh___d_lvf
            _ii_____ea_j.is_readable = True
            _ii_____ea_j.is_writeable = True

            _d____y___bd += _ii_____ea_j.to_bytes()
        

        if self.__jjr_pc__t_ is not None:
        
            _u__f_______ = self.__jjr_pc__t_.encode(self._gm_g__n___a)
            _c___rn__r__ = Stream("__substg1.0_3001" + self._e_p_wn___m_, _u__f_______)
            n_b__sfzn___.append(_c___rn__r__)

            ____e__v_yr_ = Property()
            ____e__v_yr_.tag = 0x3001 << 16 | self.sll__adckt__
            ____e__v_yr_.type = PropertyType.STRING_8
            ____e__v_yr_.size = len(_u__f_______) + mkkh___d_lvf
            ____e__v_yr_.is_readable = True
            ____e__v_yr_.is_writeable = True

            _d____y___bd += ____e__v_yr_.to_bytes()
        

        if self.d_lurjyi___x is not None:
        
            z__z_g_lsrj_ = self.d_lurjyi___x.encode(self._gm_g__n___a)
            tx_n__j_l___ = Stream("__substg1.0_3A45" + self._e_p_wn___m_, z__z_g_lsrj_)
            n_b__sfzn___.append(tx_n__j_l___)

            __t__hatb_er = Property()
            __t__hatb_er.tag = 0x3A45 << 16 | self.sll__adckt__
            __t__hatb_er.type = PropertyType.STRING_8
            __t__hatb_er.size = len(z__z_g_lsrj_) + mkkh___d_lvf
            __t__hatb_er.is_readable = True
            __t__hatb_er.is_writeable = True

            _d____y___bd += __t__hatb_er.to_bytes()
        

        if self.__jra_lp____ is not None:
        
            krc_woi_u_j_ = self.__jra_lp____.encode(self._gm_g__n___a)
            l_i_____gyer = Stream("__substg1.0_3A4C" + self._e_p_wn___m_, krc_woi_u_j_)
            n_b__sfzn___.append(l_i_____gyer)

            g____rj__k__ = Property()
            g____rj__k__.tag = 0x3A4C << 16 | self.sll__adckt__
            g____rj__k__.type = PropertyType.STRING_8
            g____rj__k__.size = len(krc_woi_u_j_) + mkkh___d_lvf
            g____rj__k__.is_readable = True
            g____rj__k__.is_writeable = True

            _d____y___bd += g____rj__k__.to_bytes()
        

        if self.____iiu_h__i is not None:
        
            ________d__s = self.____iiu_h__i.encode(self._gm_g__n___a)
            ____tl_kk_hv = Stream("__substg1.0_3A05" + self._e_p_wn___m_, ________d__s)
            n_b__sfzn___.append(____tl_kk_hv)

            _pz_cn__l___ = Property()
            _pz_cn__l___.tag = 0x3A05 << 16 | self.sll__adckt__
            _pz_cn__l___.type = PropertyType.STRING_8
            _pz_cn__l___.size = len(________d__s) + mkkh___d_lvf
            _pz_cn__l___.is_readable = True
            _pz_cn__l___.is_writeable = True

            _d____y___bd += _pz_cn__l___.to_bytes()
        

        if self._y______e___ is not None:
        
            __pe__t__d_x = self._y______e___.encode(self._gm_g__n___a)
            i__g_u_mj__r = Stream("__substg1.0_3A06" + self._e_p_wn___m_, __pe__t__d_x)
            n_b__sfzn___.append(i__g_u_mj__r)

            ___z___c__ep = Property()
            ___z___c__ep.tag = 0x3A06 << 16 | self.sll__adckt__
            ___z___c__ep.type = PropertyType.STRING_8
            ___z___c__ep.size = len(__pe__t__d_x) + mkkh___d_lvf
            ___z___c__ep.is_readable = True
            ___z___c__ep.is_writeable = True

            _d____y___bd += ___z___c__ep.to_bytes()
        

        if self.ol____d_r__y is not None:
        
            _____r_iroj_ = self.ol____d_r__y.encode(self._gm_g__n___a)
            ea___b__lpkp = Stream("__substg1.0_3A07" + self._e_p_wn___m_, _____r_iroj_)
            n_b__sfzn___.append(ea___b__lpkp)

            t_m_m___r_k_ = Property()
            t_m_m___r_k_.tag = 0x3A07 << 16 | self.sll__adckt__
            t_m_m___r_k_.type = PropertyType.STRING_8
            t_m_m___r_k_.size = len(_____r_iroj_) + mkkh___d_lvf
            t_m_m___r_k_.is_readable = True
            t_m_m___r_k_.is_writeable = True

            _d____y___bd += t_m_m___r_k_.to_bytes()
        

        if self.__t_j_op_tt_ is not None:
        
            _ye____xgi_s = self.__t_j_op_tt_.encode(self._gm_g__n___a)
            __a__l__haq_ = Stream("__substg1.0_3A43" + self._e_p_wn___m_, _ye____xgi_s)
            n_b__sfzn___.append(__a__l__haq_)

            nfn___p_d_uq = Property()
            nfn___p_d_uq.tag = 0x3A43 << 16 | self.sll__adckt__
            nfn___p_d_uq.type = PropertyType.STRING_8
            nfn___p_d_uq.size = len(_ye____xgi_s) + mkkh___d_lvf
            nfn___p_d_uq.is_readable = True
            nfn___p_d_uq.is_writeable = True

            _d____y___bd += nfn___p_d_uq.to_bytes()
        

        if self._m___i______ is not None:
        
            x_ii__v_u_f_ = self._m___i______.encode(self._gm_g__n___a)
            d__q_f_q__o_ = Stream("__substg1.0_3A2F" + self._e_p_wn___m_, x_ii__v_u_f_)
            n_b__sfzn___.append(d__q_f_q__o_)

            vdw__f__a___ = Property()
            vdw__f__a___.tag = 0x3A2F << 16 | self.sll__adckt__
            vdw__f__a___.type = PropertyType.STRING_8
            vdw__f__a___.size = len(x_ii__v_u_f_) + mkkh___d_lvf
            vdw__f__a___.is_readable = True
            vdw__f__a___.is_writeable = True

            _d____y___bd += vdw__f__a___.to_bytes()
        

        if self.z__b________ is not None:
        
            hdn_zgsm_x__ = self.z__b________.encode(self._gm_g__n___a)
            e___n_l_____ = Stream("__substg1.0_3A59" + self._e_p_wn___m_, hdn_zgsm_x__)
            n_b__sfzn___.append(e___n_l_____)

            ____lc__ci_h = Property()
            ____lc__ci_h.tag = 0x3A59 << 16 | self.sll__adckt__
            ____lc__ci_h.type = PropertyType.STRING_8
            ____lc__ci_h.size = len(hdn_zgsm_x__) + mkkh___d_lvf
            ____lc__ci_h.is_readable = True
            ____lc__ci_h.is_writeable = True

            _d____y___bd += ____lc__ci_h.to_bytes()
        

        if self.jg____s__g_s is not None:
        
            _tj__tt_i_st = self.jg____s__g_s.encode(self._gm_g__n___a)
            ____g_i__a_t = Stream("__substg1.0_3A5A" + self._e_p_wn___m_, _tj__tt_i_st)
            n_b__sfzn___.append(____g_i__a_t)

            ____lia_c___ = Property()
            ____lia_c___.tag = 0x3A5A << 16 | self.sll__adckt__
            ____lia_c___.type = PropertyType.STRING_8
            ____lia_c___.size = len(_tj__tt_i_st) + mkkh___d_lvf
            ____lia_c___.is_readable = True
            ____lia_c___.is_writeable = True

            _d____y___bd += ____lia_c___.to_bytes()
        

        if self.gmy_g__pb__d is not None:
        
            u___o__h_hdg = self.gmy_g__pb__d.encode(self._gm_g__n___a)
            b_____n_i_kd = Stream("__substg1.0_3A5B" + self._e_p_wn___m_, u___o__h_hdg)
            n_b__sfzn___.append(b_____n_i_kd)

            ___b_gf_g__b = Property()
            ___b_gf_g__b.tag = 0x3A5B << 16 | self.sll__adckt__
            ___b_gf_g__b.type = PropertyType.STRING_8
            ___b_gf_g__b.size = len(u___o__h_hdg) + mkkh___d_lvf
            ___b_gf_g__b.is_readable = True
            ___b_gf_g__b.is_writeable = True

            _d____y___bd += ___b_gf_g__b.to_bytes()
        

        if self._pro__frgm__ is not None:
        
            _hkdpy_b_r__ = self._pro__frgm__.encode(self._gm_g__n___a)
            _r__azo_g_hk = Stream("__substg1.0_3A5E" + self._e_p_wn___m_, _hkdpy_b_r__)
            n_b__sfzn___.append(_r__azo_g_hk)

            _____tw_nvs_ = Property()
            _____tw_nvs_.tag = 0x3A5E << 16 | self.sll__adckt__
            _____tw_nvs_.type = PropertyType.STRING_8
            _____tw_nvs_.size = len(_hkdpy_b_r__) + mkkh___d_lvf
            _____tw_nvs_.is_readable = True
            _____tw_nvs_.is_writeable = True

            _d____y___bd += _____tw_nvs_.to_bytes()
        

        if self.___s__yjk_q_ is not None:
        
            _p_peq_s___f = self.___s__yjk_q_.encode(self._gm_g__n___a)
            _z__r_q_q_ee = Stream("__substg1.0_3A5C" + self._e_p_wn___m_, _p_peq_s___f)
            n_b__sfzn___.append(_z__r_q_q_ee)

            ______q___hc = Property()
            ______q___hc.tag = 0x3A5C << 16 | self.sll__adckt__
            ______q___hc.type = PropertyType.STRING_8
            ______q___hc.size = len(_p_peq_s___f) + mkkh___d_lvf
            ______q___hc.is_readable = True
            ______q___hc.is_writeable = True

            _d____y___bd += ______q___hc.to_bytes()
        

        if self.kzdmh__i__y_ is not None:
        
            j____ei_kegt = self.kzdmh__i__y_.encode(self._gm_g__n___a)
            __qq_q__ov_v = Stream("__substg1.0_3A5D" + self._e_p_wn___m_, j____ei_kegt)
            n_b__sfzn___.append(__qq_q__ov_v)

            cz__w_kb_g_w = Property()
            cz__w_kb_g_w.tag = 0x3A5D << 16 | self.sll__adckt__
            cz__w_kb_g_w.type = PropertyType.STRING_8
            cz__w_kb_g_w.size = len(j____ei_kegt) + mkkh___d_lvf
            cz__w_kb_g_w.is_readable = True
            cz__w_kb_g_w.is_writeable = True

            _d____y___bd += cz__w_kb_g_w.to_bytes()
        

        if self.p__lj__pay_g is not None:
        
            ___tr____i__ = self.p__lj__pay_g.encode(self._gm_g__n___a)
            bll__dx_y__x = Stream("__substg1.0_3A25" + self._e_p_wn___m_, ___tr____i__)
            n_b__sfzn___.append(bll__dx_y__x)

            vss_ghq____c = Property()
            vss_ghq____c.tag = 0x3A25 << 16 | self.sll__adckt__
            vss_ghq____c.type = PropertyType.STRING_8
            vss_ghq____c.size = len(___tr____i__) + mkkh___d_lvf
            vss_ghq____c.is_readable = True
            vss_ghq____c.is_writeable = True

            _d____y___bd += vss_ghq____c.to_bytes()
        

        if self.vo___j____gl is not None:
        
            _b_sxqp_____ = self.vo___j____gl.encode(self._gm_g__n___a)
            _zp____a____ = Stream("__substg1.0_3A09" + self._e_p_wn___m_, _b_sxqp_____)
            n_b__sfzn___.append(_zp____a____)

            bkg____x__k_ = Property()
            bkg____x__k_.tag = 0x3A09 << 16 | self.sll__adckt__
            bkg____x__k_.type = PropertyType.STRING_8
            bkg____x__k_.size = len(_b_sxqp_____) + mkkh___d_lvf
            bkg____x__k_.is_readable = True
            bkg____x__k_.is_writeable = True

            _d____y___bd += bkg____x__k_.to_bytes()
        

        if self.z_w_qqxyx___ is not None:
        
            ___cp_w_k_z_ = self.z_w_qqxyx___.encode(self._gm_g__n___a)
            kkt___a_d_mo = Stream("__substg1.0_3A0A" + self._e_p_wn___m_, ___cp_w_k_z_)
            n_b__sfzn___.append(kkt___a_d_mo)

            _m_c____dl__ = Property()
            _m_c____dl__.tag = 0x3A0A << 16 | self.sll__adckt__
            _m_c____dl__.type = PropertyType.STRING_8
            _m_c____dl__.size = len(___cp_w_k_z_) + mkkh___d_lvf
            _m_c____dl__.is_readable = True
            _m_c____dl__.is_writeable = True

            _d____y___bd += _m_c____dl__.to_bytes()
        

        if self.___w__pydr__ is not None:
        
            l_obr__u__g_ = self.___w__pydr__.encode(self._gm_g__n___a)
            __u_vk_u_iit = Stream("__substg1.0_3A2D" + self._e_p_wn___m_, l_obr__u__g_)
            n_b__sfzn___.append(__u_vk_u_iit)

            ___u_wczwh__ = Property()
            ___u_wczwh__.tag = 0x3A2D << 16 | self.sll__adckt__
            ___u_wczwh__.type = PropertyType.STRING_8
            ___u_wczwh__.size = len(l_obr__u__g_) + mkkh___d_lvf
            ___u_wczwh__.is_readable = True
            ___u_wczwh__.is_writeable = True

            _d____y___bd += ___u_wczwh__.to_bytes()
        

        if self.lp_y_____s__ is not None:
        
            r___kcl__x_n = NamedProperty()
            r___kcl__x_n.id = 0x8046
            r___kcl__x_n.guid = StandardPropertySet.ADDRESS
            r___kcl__x_n.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, r___kcl__x_n)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(r___kcl__x_n)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _jn_l____sy_ = self.lp_y_____s__.encode(self._gm_g__n___a)

            _xtv__qhl___ = Stream("__substg1.0_" + ____w_ah__g_, _jn_l____sy_)
            n_b__sfzn___.append(_xtv__qhl___)

            d_z_nfy_____ = Property()
            d_z_nfy_____.tag = ezi__t__sl__
            d_z_nfy_____.type = PropertyType.STRING_8
            d_z_nfy_____.size = len(_jn_l____sy_) + mkkh___d_lvf
            d_z_nfy_____.is_readable = True
            d_z_nfy_____.is_writeable = True

            _d____y___bd += d_z_nfy_____.to_bytes()

            x_khmo_m_xj_ = Stream("__substg1.0_3A27" + self._e_p_wn___m_, _jn_l____sy_)
            n_b__sfzn___.append(x_khmo_m_xj_)

            ywba_d_w_y_k = Property()
            ywba_d_w_y_k.tag = 0x3A27 << 16 | self.sll__adckt__
            ywba_d_w_y_k.type = PropertyType.STRING_8
            ywba_d_w_y_k.size = len(_jn_l____sy_) + mkkh___d_lvf
            ywba_d_w_y_k.is_readable = True
            ywba_d_w_y_k.is_writeable = True

            _d____y___bd += ywba_d_w_y_k.to_bytes()
        

        if self.__ppjf_____v is not None:
        
            _u__a__v___e = self.__ppjf_____v.encode(self._gm_g__n___a)
            ____gp___q__ = Stream("__substg1.0_3A4E" + self._e_p_wn___m_, _u__a__v___e)
            n_b__sfzn___.append(____gp___q__)

            ____i_hq_fiy = Property()
            ____i_hq_fiy.tag = 0x3A4E << 16 | self.sll__adckt__
            ____i_hq_fiy.type = PropertyType.STRING_8
            ____i_hq_fiy.size = len(_u__a__v___e) + mkkh___d_lvf
            ____i_hq_fiy.is_readable = True
            ____i_hq_fiy.is_writeable = True

            _d____y___bd += ____i_hq_fiy.to_bytes()
        

        if self.____ixh_____ is not None:
        
            u_ff______s_ = self.____ixh_____.encode(self._gm_g__n___a)
            ndsvo__hpu__ = Stream("__substg1.0_3A44" + self._e_p_wn___m_, u_ff______s_)
            n_b__sfzn___.append(ndsvo__hpu__)

            __s_gi_ny__v = Property()
            __s_gi_ny__v.tag = 0x3A44 << 16 | self.sll__adckt__
            __s_gi_ny__v.type = PropertyType.STRING_8
            __s_gi_ny__v.size = len(u_ff______s_) + mkkh___d_lvf
            __s_gi_ny__v.is_readable = True
            __s_gi_ny__v.is_writeable = True

            _d____y___bd += __s_gi_ny__v.to_bytes()
        

        if self.f__fj___kg__ is not None:
        
            xb________k_ = self.f__fj___kg__.encode(self._gm_g__n___a)
            x__td_fiu_h_ = Stream("__substg1.0_3A4F" + self._e_p_wn___m_, xb________k_)
            n_b__sfzn___.append(x__td_fiu_h_)

            _zj____s_dj_ = Property()
            _zj____s_dj_.tag = 0x3A4F << 16 | self.sll__adckt__
            _zj____s_dj_.type = PropertyType.STRING_8
            _zj____s_dj_.size = len(xb________k_) + mkkh___d_lvf
            _zj____s_dj_.is_readable = True
            _zj____s_dj_.is_writeable = True

            _d____y___bd += _zj____s_dj_.to_bytes()
        

        if self.fcg__x__l_bh is not None:
        
            c_shs_____dx = self.fcg__x__l_bh.encode(self._gm_g__n___a)
            ________n_ur = Stream("__substg1.0_3A19" + self._e_p_wn___m_, c_shs_____dx)
            n_b__sfzn___.append(________n_ur)

            __abs___keiq = Property()
            __abs___keiq.tag = 0x3A19 << 16 | self.sll__adckt__
            __abs___keiq.type = PropertyType.STRING_8
            __abs___keiq.size = len(c_shs_____dx) + mkkh___d_lvf
            __abs___keiq.is_readable = True
            __abs___keiq.is_writeable = True

            _d____y___bd += __abs___keiq.to_bytes()
        

        if self.vj_b__f__u__ is not None:
        
            _l_i___ip_pr = self.vj_b__f__u__.encode(self._gm_g__n___a)
            _zrt_fatw_cw = Stream("__substg1.0_3A08" + self._e_p_wn___m_, _l_i___ip_pr)
            n_b__sfzn___.append(_zrt_fatw_cw)

            ___ot_f____y = Property()
            ___ot_f____y.tag = 0x3A08 << 16 | self.sll__adckt__
            ___ot_f____y.type = PropertyType.STRING_8
            ___ot_f____y.size = len(_l_i___ip_pr) + mkkh___d_lvf
            ___ot_f____y.is_readable = True
            ___ot_f____y.is_writeable = True

            _d____y___bd += ___ot_f____y.to_bytes()
        

        if self.hxpxy___q__z is not None:
        
            ____cp_gfuoj = self.hxpxy___q__z.encode(self._gm_g__n___a)
            d_____o___ot = Stream("__substg1.0_3A5F" + self._e_p_wn___m_, ____cp_gfuoj)
            n_b__sfzn___.append(d_____o___ot)

            v__m__stg_mc = Property()
            v__m__stg_mc.tag = 0x3A5F << 16 | self.sll__adckt__
            v__m__stg_mc.type = PropertyType.STRING_8
            v__m__stg_mc.size = len(____cp_gfuoj) + mkkh___d_lvf
            v__m__stg_mc.is_readable = True
            v__m__stg_mc.is_writeable = True

            _d____y___bd += v__m__stg_mc.to_bytes()
        

        if self.___a___sf___ is not None:
        
            __f_gadx____ = self.___a___sf___.encode(self._gm_g__n___a)
            bt_a___k____ = Stream("__substg1.0_3A60" + self._e_p_wn___m_, __f_gadx____)
            n_b__sfzn___.append(bt_a___k____)

            _q_i___uvf__ = Property()
            _q_i___uvf__.tag = 0x3A60 << 16 | self.sll__adckt__
            _q_i___uvf__.type = PropertyType.STRING_8
            _q_i___uvf__.size = len(__f_gadx____) + mkkh___d_lvf
            _q_i___uvf__.is_readable = True
            _q_i___uvf__.is_writeable = True

            _d____y___bd += _q_i___uvf__.to_bytes()
        

        if self.___l__fc_s_d is not None:
        
            _q__c____hci = self.___l__fc_s_d.encode(self._gm_g__n___a)
            __q__zyb__x_ = Stream("__substg1.0_3A61" + self._e_p_wn___m_, _q__c____hci)
            n_b__sfzn___.append(__q__zyb__x_)

            _j_k_s__hv__ = Property()
            _j_k_s__hv__.tag = 0x3A61 << 16 | self.sll__adckt__
            _j_k_s__hv__.type = PropertyType.STRING_8
            _j_k_s__hv__.size = len(_q__c____hci) + mkkh___d_lvf
            _j_k_s__hv__.is_readable = True
            _j_k_s__hv__.is_writeable = True

            _d____y___bd += _j_k_s__hv__.to_bytes()
        

        if self.t____l_e_ob_ is not None:
        
            _sikq_vtj__o = self.t____l_e_ob_.encode(self._gm_g__n___a)
            ___qc_s_k__r = Stream("__substg1.0_3A62" + self._e_p_wn___m_, _sikq_vtj__o)
            n_b__sfzn___.append(___qc_s_k__r)

            _s__jef__b__ = Property()
            _s__jef__b__.tag = 0x3A62 << 16 | self.sll__adckt__
            _s__jef__b__.type = PropertyType.STRING_8
            _s__jef__b__.size = len(_sikq_vtj__o) + mkkh___d_lvf
            _s__jef__b__.is_readable = True
            _s__jef__b__.is_writeable = True

            _d____y___bd += _s__jef__b__.to_bytes()
        

        if self.sfuq__vbny_x is not None:
        
            __ua_jmompde = self.sfuq__vbny_x.encode(self._gm_g__n___a)
            m___n___a_dp = Stream("__substg1.0_3A63" + self._e_p_wn___m_, __ua_jmompde)
            n_b__sfzn___.append(m___n___a_dp)

            _ed_q_al__s_ = Property()
            _ed_q_al__s_.tag = 0x3A63 << 16 | self.sll__adckt__
            _ed_q_al__s_.type = PropertyType.STRING_8
            _ed_q_al__s_.size = len(__ua_jmompde) + mkkh___d_lvf
            _ed_q_al__s_.is_readable = True
            _ed_q_al__s_.is_writeable = True

            _d____y___bd += _ed_q_al__s_.to_bytes()
        

        if self._ox_pj__nhnr is not None:
        
            _gl_o__cw__f = self._ox_pj__nhnr.encode(self._gm_g__n___a)
            _o_a_a_f_cr_ = Stream("__substg1.0_3A1F" + self._e_p_wn___m_, _gl_o__cw__f)
            n_b__sfzn___.append(_o_a_a_f_cr_)

            f_xonew___ll = Property()
            f_xonew___ll.tag = 0x3A1F << 16 | self.sll__adckt__
            f_xonew___ll.type = PropertyType.STRING_8
            f_xonew___ll.size = len(_gl_o__cw__f) + mkkh___d_lvf
            f_xonew___ll.is_readable = True
            f_xonew___ll.is_writeable = True

            _d____y___bd += f_xonew___ll.to_bytes()
        

        if self.__b_y_d_kqv_ is not None:
        
            _g_____d___p = self.__b_y_d_kqv_.encode(self._gm_g__n___a)
            t____r_mnuta = Stream("__substg1.0_3A21" + self._e_p_wn___m_, _g_____d___p)
            n_b__sfzn___.append(t____r_mnuta)

            _y__tjh__qnq = Property()
            _y__tjh__qnq.tag = 0x3A21 << 16 | self.sll__adckt__
            _y__tjh__qnq.type = PropertyType.STRING_8
            _y__tjh__qnq.size = len(_g_____d___p) + mkkh___d_lvf
            _y__tjh__qnq.is_readable = True
            _y__tjh__qnq.is_writeable = True

            _d____y___bd += _y__tjh__qnq.to_bytes()
        

        if self.a_akhxq__gp_ is not None:
        
            xbclq__xvwog = self.a_akhxq__gp_.encode(self._gm_g__n___a)
            _b_rkr_x_wrq = Stream("__substg1.0_3A50" + self._e_p_wn___m_, xbclq__xvwog)
            n_b__sfzn___.append(_b_rkr_x_wrq)

            ccjkczhp__n_ = Property()
            ccjkczhp__n_.tag = 0x3A50 << 16 | self.sll__adckt__
            ccjkczhp__n_.type = PropertyType.STRING_8
            ccjkczhp__n_.size = len(xbclq__xvwog) + mkkh___d_lvf
            ccjkczhp__n_.is_readable = True
            ccjkczhp__n_.is_writeable = True

            _d____y___bd += ccjkczhp__n_.to_bytes()
        

        if self.k_m_i___o__h is not None:
        
            __z___a_rhg_ = self.k_m_i___o__h.encode(self._gm_g__n___a)
            np_mxk_h_e_r = Stream("__substg1.0_3A15" + self._e_p_wn___m_, __z___a_rhg_)
            n_b__sfzn___.append(np_mxk_h_e_r)

            ruk_f_kkwed_ = Property()
            ruk_f_kkwed_.tag = 0x3A15 << 16 | self.sll__adckt__
            ruk_f_kkwed_.type = PropertyType.STRING_8
            ruk_f_kkwed_.size = len(__z___a_rhg_) + mkkh___d_lvf
            ruk_f_kkwed_.is_readable = True
            ruk_f_kkwed_.is_writeable = True

            _d____y___bd += ruk_f_kkwed_.to_bytes()
        

        if self.b_xkfy_m__v_ is not None:
        
            y_syd_j__kbs = NamedProperty()
            y_syd_j__kbs.id = 0x8048
            y_syd_j__kbs.guid = StandardPropertySet.ADDRESS
            y_syd_j__kbs.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, y_syd_j__kbs)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(y_syd_j__kbs)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __l_g_oggw__ = self.b_xkfy_m__v_.encode(self._gm_g__n___a)

            __l__k___l_d = Stream("__substg1.0_" + ____w_ah__g_, __l_g_oggw__)
            n_b__sfzn___.append(__l__k___l_d)

            _k___qi_c_r_ = Property()
            _k___qi_c_r_.tag = ezi__t__sl__
            _k___qi_c_r_.type = PropertyType.STRING_8
            _k___qi_c_r_.size = len(__l_g_oggw__) + mkkh___d_lvf
            _k___qi_c_r_.is_readable = True
            _k___qi_c_r_.is_writeable = True

            _d____y___bd += _k___qi_c_r_.to_bytes()

            ___b____s__f = Stream("__substg1.0_3A2A" + self._e_p_wn___m_, __l_g_oggw__)
            n_b__sfzn___.append(___b____s__f)

            zd___vexu__j = Property()
            zd___vexu__j.tag = 0x3A2A << 16 | self.sll__adckt__
            zd___vexu__j.type = PropertyType.STRING_8
            zd___vexu__j.size = len(__l_g_oggw__) + mkkh___d_lvf
            zd___vexu__j.is_readable = True
            zd___vexu__j.is_writeable = True

            _d____y___bd += zd___vexu__j.to_bytes()
        

        if self.qvx_e_ns____ is not None:
        
            ____bey_tut_ = self.qvx_e_ns____.encode(self._gm_g__n___a)
            _____kd_y__i = Stream("__substg1.0_3A2B" + self._e_p_wn___m_, ____bey_tut_)
            n_b__sfzn___.append(_____kd_y__i)

            __lg___lrn_n = Property()
            __lg___lrn_n.tag = 0x3A2B << 16 | self.sll__adckt__
            __lg___lrn_n.type = PropertyType.STRING_8
            __lg___lrn_n.size = len(____bey_tut_) + mkkh___d_lvf
            __lg___lrn_n.is_readable = True
            __lg___lrn_n.is_writeable = True

            _d____y___bd += __lg___lrn_n.to_bytes()
        

        if self.sba__qjh___k is not None:
        
            _____dsx____ = NamedProperty()
            _____dsx____.id = 0x8047
            _____dsx____.guid = StandardPropertySet.ADDRESS
            _____dsx____.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _____dsx____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_____dsx____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _qq_wpwx_r__ = self.sba__qjh___k.encode(self._gm_g__n___a)

            dzcz___b___f = Stream("__substg1.0_" + ____w_ah__g_, _qq_wpwx_r__)
            n_b__sfzn___.append(dzcz___b___f)

            r____e_o_t_u = Property()
            r____e_o_t_u.tag = ezi__t__sl__
            r____e_o_t_u.type = PropertyType.STRING_8
            r____e_o_t_u.size = len(_qq_wpwx_r__) + mkkh___d_lvf
            r____e_o_t_u.is_readable = True
            r____e_o_t_u.is_writeable = True

            _d____y___bd += r____e_o_t_u.to_bytes()

            t___or_ciz__ = Stream("__substg1.0_3A28" + self._e_p_wn___m_, _qq_wpwx_r__)
            n_b__sfzn___.append(t___or_ciz__)

            _ep__sxn_srl = Property()
            _ep__sxn_srl.tag = 0x3A28 << 16 | self.sll__adckt__
            _ep__sxn_srl.type = PropertyType.STRING_8
            _ep__sxn_srl.size = len(_qq_wpwx_r__) + mkkh___d_lvf
            _ep__sxn_srl.is_readable = True
            _ep__sxn_srl.is_writeable = True

            _d____y___bd += _ep__sxn_srl.to_bytes()
        

        if self.gs_m_____l__ is not None:
        
            ___de_p___g_ = NamedProperty()
            ___de_p___g_.id = 0x8045
            ___de_p___g_.guid = StandardPropertySet.ADDRESS
            ___de_p___g_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___de_p___g_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___de_p___g_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            z__odqaim_i_ = self.gs_m_____l__.encode(self._gm_g__n___a)

            _yfv___grjob = Stream("__substg1.0_" + ____w_ah__g_, z__odqaim_i_)
            n_b__sfzn___.append(_yfv___grjob)

            _____o_u_xay = Property()
            _____o_u_xay.tag = ezi__t__sl__
            _____o_u_xay.type = PropertyType.STRING_8
            _____o_u_xay.size = len(z__odqaim_i_) + mkkh___d_lvf
            _____o_u_xay.is_readable = True
            _____o_u_xay.is_writeable = True

            _d____y___bd += _____o_u_xay.to_bytes()

            __l_y___n__a = Stream("__substg1.0_3A29" + self._e_p_wn___m_, z__odqaim_i_)
            n_b__sfzn___.append(__l_y___n__a)

            __t_n_____tl = Property()
            __t_n_____tl.tag = 0x3A29 << 16 | self.sll__adckt__
            __t_n_____tl.type = PropertyType.STRING_8
            __t_n_____tl.size = len(z__odqaim_i_) + mkkh___d_lvf
            __t_n_____tl.is_readable = True
            __t_n_____tl.is_writeable = True

            _d____y___bd += __t_n_____tl.to_bytes()
        

        if self.__ju____j__c is not None:
        
            bmfbt_r____h = self.__ju____j__c.encode(self._gm_g__n___a)
            o_a_____tu__ = Stream("__substg1.0_3A23" + self._e_p_wn___m_, bmfbt_r____h)
            n_b__sfzn___.append(o_a_____tu__)

            qz____b__p_x = Property()
            qz____b__p_x.tag = 0x3A23 << 16 | self.sll__adckt__
            qz____b__p_x.type = PropertyType.STRING_8
            qz____b__p_x.size = len(bmfbt_r____h) + mkkh___d_lvf
            qz____b__p_x.is_readable = True
            qz____b__p_x.is_writeable = True

            _d____y___bd += qz____b__p_x.to_bytes()
        

        if self._p__wc_gnx_g is not None:
        
            _f__v_q_____ = self._p__wc_gnx_g.encode(self._gm_g__n___a)
            m_e_r_j_fdrw = Stream("__substg1.0_3A1A" + self._e_p_wn___m_, _f__v_q_____)
            n_b__sfzn___.append(m_e_r_j_fdrw)

            eg__xk_h___k = Property()
            eg__xk_h___k.tag = 0x3A1A << 16 | self.sll__adckt__
            eg__xk_h___k.type = PropertyType.STRING_8
            eg__xk_h___k.size = len(_f__v_q_____) + mkkh___d_lvf
            eg__xk_h___k.is_readable = True
            eg__xk_h___k.is_writeable = True

            _d____y___bd += eg__xk_h___k.to_bytes()
        

        if self.sc_gg_f____i is not None:
        
            eoeqk_x_j___ = self.sc_gg_f____i.encode(self._gm_g__n___a)
            __y_u__ma_up = Stream("__substg1.0_3A46" + self._e_p_wn___m_, eoeqk_x_j___)
            n_b__sfzn___.append(__y_u__ma_up)

            wjr_t_c__i_t = Property()
            wjr_t_c__i_t.tag = 0x3A46 << 16 | self.sll__adckt__
            wjr_t_c__i_t.type = PropertyType.STRING_8
            wjr_t_c__i_t.size = len(eoeqk_x_j___) + mkkh___d_lvf
            wjr_t_c__i_t.is_readable = True
            wjr_t_c__i_t.is_writeable = True

            _d____y___bd += wjr_t_c__i_t.to_bytes()
        

        if self.lkex____f__e is not None:
        
            __s_m__wu___ = self.lkex____f__e.encode(self._gm_g__n___a)
            _msvt___r_e_ = Stream("__substg1.0_3A1D" + self._e_p_wn___m_, __s_m__wu___)
            n_b__sfzn___.append(_msvt___r_e_)

            __r____m_f__ = Property()
            __r____m_f__.tag = 0x3A1D << 16 | self.sll__adckt__
            __r____m_f__.type = PropertyType.STRING_8
            __r____m_f__.size = len(__s_m__wu___) + mkkh___d_lvf
            __r____m_f__.is_readable = True
            __r____m_f__.is_writeable = True

            _d____y___bd += __r____m_f__.to_bytes()
        

        if self.s___b__i___o is not None:
        
            _ozc_o__m__r = self.s___b__i___o.encode(self._gm_g__n___a)
            _____q__p_kb = Stream("__substg1.0_3A48" + self._e_p_wn___m_, _ozc_o__m__r)
            n_b__sfzn___.append(_____q__p_kb)

            le__m_y_f_ts = Property()
            le__m_y_f_ts.tag = 0x3A48 << 16 | self.sll__adckt__
            le__m_y_f_ts.type = PropertyType.STRING_8
            le__m_y_f_ts.size = len(_ozc_o__m__r) + mkkh___d_lvf
            le__m_y_f_ts.is_readable = True
            le__m_y_f_ts.is_writeable = True

            _d____y___bd += le__m_y_f_ts.to_bytes()
        

        if self.lkc__aliq_g_ is not None:
        
            izgk_qwgpo_r = self.lkc__aliq_g_.encode(self._gm_g__n___a)
            uwky_zfyjvmt = Stream("__substg1.0_3A11" + self._e_p_wn___m_, izgk_qwgpo_r)
            n_b__sfzn___.append(uwky_zfyjvmt)

            _q___ftwn___ = Property()
            _q___ftwn___.tag = 0x3A11 << 16 | self.sll__adckt__
            _q___ftwn___.type = PropertyType.STRING_8
            _q___ftwn___.size = len(izgk_qwgpo_r) + mkkh___d_lvf
            _q___ftwn___.is_readable = True
            _q___ftwn___.is_writeable = True

            _d____y___bd += _q___ftwn___.to_bytes()
        

        if self._sw_lg____k_ is not None:
        
            _xet_x_ht___ = self._sw_lg____k_.encode(self._gm_g__n___a)
            z__v_v_r____ = Stream("__substg1.0_3A2C" + self._e_p_wn___m_, _xet_x_ht___)
            n_b__sfzn___.append(z__v_v_r____)

            _zkb_o______ = Property()
            _zkb_o______.tag = 0x3A2C << 16 | self.sll__adckt__
            _zkb_o______.type = PropertyType.STRING_8
            _zkb_o______.size = len(_xet_x_ht___) + mkkh___d_lvf
            _zkb_o______.is_readable = True
            _zkb_o______.is_writeable = True

            _d____y___bd += _zkb_o______.to_bytes()
        

        if self.b____ioy____ is not None:
        
            _nso_qas_emf = self.b____ioy____.encode(self._gm_g__n___a)
            z_b_____m__v = Stream("__substg1.0_3A17" + self._e_p_wn___m_, _nso_qas_emf)
            n_b__sfzn___.append(z_b_____m__v)

            _i__________ = Property()
            _i__________.tag = 0x3A17 << 16 | self.sll__adckt__
            _i__________.type = PropertyType.STRING_8
            _i__________.size = len(_nso_qas_emf) + mkkh___d_lvf
            _i__________.is_readable = True
            _i__________.is_writeable = True

            _d____y___bd += _i__________.to_bytes()
        

        if self.__j_____m_ge is not None:
        
            _u_______h__ = self.__j_____m_ge.encode(self._gm_g__n___a)
            dl___shau___ = Stream("__substg1.0_3A4B" + self._e_p_wn___m_, _u_______h__)
            n_b__sfzn___.append(dl___shau___)

            _z_uvt__k___ = Property()
            _z_uvt__k___.tag = 0x3A4B << 16 | self.sll__adckt__
            _z_uvt__k___.type = PropertyType.STRING_8
            _z_uvt__k___.size = len(_u_______h__) + mkkh___d_lvf
            _z_uvt__k___.is_readable = True
            _z_uvt__k___.is_writeable = True

            _d____y___bd += _z_uvt__k___.to_bytes()
        

        if self.u_u_t_ci___p > datetime.datetime(1901,1,1):
        
            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.u_u_t_ci___p - j____h_x_v_h).total_seconds()) * 10_000_000

            __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

            _z_auh___r_f = Property()
            _z_auh___r_f.tag = 0x3A410040
            _z_auh___r_f.type = PropertyType.TIME
            _z_auh___r_f.value = __cwx_qbk___
            _z_auh___r_f.is_readable = True
            _z_auh___r_f.is_writeable = False

            _d____y___bd += _z_auh___r_f.to_bytes()
        

        if self.bw____sz____ != Gender.NONE:
        
            v_f___la_el_ = Property()
            v_f___la_el_.tag = 0x3A4D0002
            v_f___la_el_.type = PropertyType.Integer16
            v_f___la_el_.value = int.to_bytes(EnumUtil.parse_gender(self.bw____sz____), 4, "little")
            v_f___la_el_.is_readable = True
            v_f___la_el_.is_writeable = True

            _d____y___bd += v_f___la_el_.to_bytes()
        

        if self._hle_ua_z__g != SelectedMailingAddress.NONE:
        
            yj_elx_jblg_ = NamedProperty()
            yj_elx_jblg_.id = 0x8022
            yj_elx_jblg_.guid = StandardPropertySet.ADDRESS
            yj_elx_jblg_.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, yj_elx_jblg_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(yj_elx_jblg_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0003

            w_____lw___n = Property()
            w_____lw___n.tag = ezi__t__sl__
            w_____lw___n.type = PropertyType.INTEGER_32
            w_____lw___n.value = int.to_bytes(EnumUtil.parse_selected_mailing_address(self._hle_ua_z__g), 4, "little")
            w_____lw___n.is_readable = True
            w_____lw___n.is_writeable = True

            _d____y___bd += w_____lw___n.to_bytes()
        

        if self.y__i_no____g:
        
            th_____y____ = NamedProperty()
            th_____y____.id = 0x8015
            th_____y____.guid = StandardPropertySet.ADDRESS
            th_____y____.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, th_____y____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(th_____y____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x000B

            th_____y____ = Property()
            th_____y____.tag = ezi__t__sl__
            th_____y____.type = PropertyType.BOOLEAN
            th_____y____.value = int.to_bytes(1,1,"little")
            th_____y____.is_readable = True
            th_____y____.is_writeable = True

            _d____y___bd += th_____y____.to_bytes()
        

        if self.__el_ca_i_l_ is not None:
        
            _q__lm_r____ = NamedProperty()
            _q__lm_r____.id = 0x8005
            _q__lm_r____.guid = StandardPropertySet.ADDRESS
            _q__lm_r____.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _q__lm_r____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_q__lm_r____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            vu___b_sx_h_ = self.__el_ca_i_l_.encode(self._gm_g__n___a)
            __zik_____os = Stream("__substg1.0_" + ____w_ah__g_, vu___b_sx_h_)
            n_b__sfzn___.append(__zik_____os)

            ______ok_d__ = Property()
            ______ok_d__.tag = ezi__t__sl__
            ______ok_d__.type = PropertyType.STRING_8
            ______ok_d__.size = len(vu___b_sx_h_) + mkkh___d_lvf
            ______ok_d__.is_readable = True
            ______ok_d__.is_writeable = True

            _d____y___bd += ______ok_d__.to_bytes()
        

        if self.___w___f___x is not None:
        
            ___adg__t_dy = NamedProperty()
            ___adg__t_dy.id = 0x8062
            ___adg__t_dy.guid = StandardPropertySet.ADDRESS
            ___adg__t_dy.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___adg__t_dy)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___adg__t_dy)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            ___n____ef_u = self.___w___f___x.encode(self._gm_g__n___a)
            __m____rs_t_ = Stream("__substg1.0_" + ____w_ah__g_, ___n____ef_u)
            n_b__sfzn___.append(__m____rs_t_)

            q__dv_t_____ = Property()
            q__dv_t_____.tag = ezi__t__sl__
            q__dv_t_____.type = PropertyType.STRING_8
            q__dv_t_____.size = len(___n____ef_u) + mkkh___d_lvf
            q__dv_t_____.is_readable = True
            q__dv_t_____.is_writeable = True

            _d____y___bd += q__dv_t_____.to_bytes()
        

        if self.l_a_g_kx____ is not None:
        
            c_____b_okva = NamedProperty()
            c_____b_okva.id = 0x80D8
            c_____b_okva.guid = StandardPropertySet.ADDRESS
            c_____b_okva.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, c_____b_okva)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(c_____b_okva)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _a_v_s_pu__a = self.l_a_g_kx____.encode(self._gm_g__n___a)
            _de_d__leny_ = Stream("__substg1.0_" + ____w_ah__g_, _a_v_s_pu__a)
            n_b__sfzn___.append(_de_d__leny_)

            u__xqhqk__j_ = Property()
            u__xqhqk__j_.tag = ezi__t__sl__
            u__xqhqk__j_.type = PropertyType.STRING_8
            u__xqhqk__j_.size = len(_a_v_s_pu__a) + mkkh___d_lvf
            u__xqhqk__j_.is_readable = True
            u__xqhqk__j_.is_writeable = True

            _d____y___bd += u__xqhqk__j_.to_bytes()
        

        if self.g___cd_p_do_ is not None:
        
            __q_sfpt____ = NamedProperty()
            __q_sfpt____.id = 0x801B
            __q_sfpt____.guid = StandardPropertySet.ADDRESS
            __q_sfpt____.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __q_sfpt____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__q_sfpt____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _p______ua_i = self.g___cd_p_do_.encode(self._gm_g__n___a)
            c_k____vn_bc = Stream("__substg1.0_" + ____w_ah__g_, _p______ua_i)
            n_b__sfzn___.append(c_k____vn_bc)

            _y_wz_dnrk__ = Property()
            _y_wz_dnrk__.tag = ezi__t__sl__
            _y_wz_dnrk__.type = PropertyType.STRING_8
            _y_wz_dnrk__.size = len(_p______ua_i) + mkkh___d_lvf
            _y_wz_dnrk__.is_readable = True
            _y_wz_dnrk__.is_writeable = True

            _d____y___bd += _y_wz_dnrk__.to_bytes()
        

        if self.q_j______u_u is not None:
        
            vx_qc___pfc_ = NamedProperty()
            vx_qc___pfc_.id = 0x801A
            vx_qc___pfc_.guid = StandardPropertySet.ADDRESS
            vx_qc___pfc_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, vx_qc___pfc_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(vx_qc___pfc_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            aw____smppvs = self.q_j______u_u.encode(self._gm_g__n___a)
            ______lhv___ = Stream("__substg1.0_" + ____w_ah__g_, aw____smppvs)
            n_b__sfzn___.append(______lhv___)

            ___xt_dd__m_ = Property()
            ___xt_dd__m_.tag = ezi__t__sl__
            ___xt_dd__m_.type = PropertyType.STRING_8
            ___xt_dd__m_.size = len(aw____smppvs) + mkkh___d_lvf
            ___xt_dd__m_.is_readable = True
            ___xt_dd__m_.is_writeable = True

            _d____y___bd += ___xt_dd__m_.to_bytes()
        


        if self._iwxsuk___iu is not None:
        
            _____o__iyg_ = NamedProperty()
            _____o__iyg_.id = 0x801C
            _____o__iyg_.guid = StandardPropertySet.ADDRESS
            _____o__iyg_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _____o__iyg_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_____o__iyg_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _tiz__us____ = self._iwxsuk___iu.encode(self._gm_g__n___a)
            _m__b__we___ = Stream("__substg1.0_" + ____w_ah__g_, _tiz__us____)
            n_b__sfzn___.append(_m__b__we___)

            dva___m____n = Property()
            dva___m____n.tag = ezi__t__sl__
            dva___m____n.type = PropertyType.STRING_8
            dva___m____n.size = len(_tiz__us____) + mkkh___d_lvf
            dva___m____n.is_readable = True
            dva___m____n.is_writeable = True

            _d____y___bd += dva___m____n.to_bytes()
        

        if self._d_d___jg__u is not None:
        
            ___u_v__gn_e = NamedProperty()
            ___u_v__gn_e.id = 0x8083
            ___u_v__gn_e.guid = StandardPropertySet.ADDRESS
            ___u_v__gn_e.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___u_v__gn_e)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___u_v__gn_e)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __xdkm_di___ = self._d_d___jg__u.encode(self._gm_g__n___a)
            cey__e__t__z = Stream("__substg1.0_" + ____w_ah__g_, __xdkm_di___)
            n_b__sfzn___.append(cey__e__t__z)

            h_yp______u_ = Property()
            h_yp______u_.tag = ezi__t__sl__
            h_yp______u_.type = PropertyType.STRING_8
            h_yp______u_.size = len(__xdkm_di___) + mkkh___d_lvf
            h_yp______u_.is_readable = True
            h_yp______u_.is_writeable = True

            _d____y___bd += h_yp______u_.to_bytes()
        

        if self.c_x_q___hzc_ is not None:
        
            _n_jd_h_____ = NamedProperty()
            _n_jd_h_____.id = 0x8093
            _n_jd_h_____.guid = StandardPropertySet.ADDRESS
            _n_jd_h_____.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _n_jd_h_____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_n_jd_h_____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _______i_srw = self.c_x_q___hzc_.encode(self._gm_g__n___a)
            _sb_s__i___j = Stream("__substg1.0_" + ____w_ah__g_, _______i_srw)
            n_b__sfzn___.append(_sb_s__i___j)

            e__s_q_b_bb_ = Property()
            e__s_q_b_bb_.tag = ezi__t__sl__
            e__s_q_b_bb_.type = PropertyType.STRING_8
            e__s_q_b_bb_.size = len(_______i_srw) + mkkh___d_lvf
            e__s_q_b_bb_.is_readable = True
            e__s_q_b_bb_.is_writeable = True

            _d____y___bd += e__s_q_b_bb_.to_bytes()
        

        if self._c_dcu_np_f_ is not None:
        
            __vn_rkn____ = NamedProperty()
            __vn_rkn____.id = 0x80A3
            __vn_rkn____.guid = StandardPropertySet.ADDRESS
            __vn_rkn____.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, __vn_rkn____)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(__vn_rkn____)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _mt_j__j___s = self._c_dcu_np_f_.encode(self._gm_g__n___a)
            p__r_hfkr___ = Stream("__substg1.0_" + ____w_ah__g_, _mt_j__j___s)
            n_b__sfzn___.append(p__r_hfkr___)

            h_vh__fg____ = Property()
            h_vh__fg____.tag = ezi__t__sl__
            h_vh__fg____.type = PropertyType.STRING_8
            h_vh__fg____.size = len(_mt_j__j___s) + mkkh___d_lvf
            h_vh__fg____.is_readable = True
            h_vh__fg____.is_writeable = True

            _d____y___bd += h_vh__fg____.to_bytes()
        

        if self._y_g__fjv_r_ is not None:
        
            e_j___wnq_e_ = NamedProperty()
            e_j___wnq_e_.id = 0x8084
            e_j___wnq_e_.guid = StandardPropertySet.ADDRESS
            e_j___wnq_e_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, e_j___wnq_e_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(e_j___wnq_e_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            xfmi_qrd__sw = self._y_g__fjv_r_.encode(self._gm_g__n___a)
            t_x__it_ta__ = Stream("__substg1.0_" + ____w_ah__g_, xfmi_qrd__sw)
            n_b__sfzn___.append(t_x__it_ta__)

            o_dp_qdxj__i = Property()
            o_dp_qdxj__i.tag = ezi__t__sl__
            o_dp_qdxj__i.type = PropertyType.STRING_8
            o_dp_qdxj__i.size = len(xfmi_qrd__sw) + mkkh___d_lvf
            o_dp_qdxj__i.is_readable = True
            o_dp_qdxj__i.is_writeable = True

            _d____y___bd += o_dp_qdxj__i.to_bytes()
        

        if self.____e____jg_ is not None:
        
            ___gq_____d_ = NamedProperty()
            ___gq_____d_.id = 0x8094
            ___gq_____d_.guid = StandardPropertySet.ADDRESS
            ___gq_____d_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___gq_____d_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___gq_____d_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _qat___w_e__ = self.____e____jg_.encode(self._gm_g__n___a)
            __ad_hpdu_rq = Stream("__substg1.0_" + ____w_ah__g_, _qat___w_e__)
            n_b__sfzn___.append(__ad_hpdu_rq)

            n__bvv_____p = Property()
            n__bvv_____p.tag = ezi__t__sl__
            n__bvv_____p.type = PropertyType.STRING_8
            n__bvv_____p.size = len(_qat___w_e__) + mkkh___d_lvf
            n__bvv_____p.is_readable = True
            n__bvv_____p.is_writeable = True

            _d____y___bd += n__bvv_____p.to_bytes()
        

        if self.go___g_____l is not None:
        
            _ed__fffjxl_ = NamedProperty()
            _ed__fffjxl_.id = 0x80A4
            _ed__fffjxl_.guid = StandardPropertySet.ADDRESS
            _ed__fffjxl_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _ed__fffjxl_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_ed__fffjxl_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _______sm___ = self.go___g_____l.encode(self._gm_g__n___a)
            _cc_p____u_u = Stream("__substg1.0_" + ____w_ah__g_, _______sm___)
            n_b__sfzn___.append(_cc_p____u_u)

            lu_og_bg_yla = Property()
            lu_og_bg_yla.tag = ezi__t__sl__
            lu_og_bg_yla.type = PropertyType.STRING_8
            lu_og_bg_yla.size = len(_______sm___) + mkkh___d_lvf
            lu_og_bg_yla.is_readable = True
            lu_og_bg_yla.is_writeable = True

            _d____y___bd += lu_og_bg_yla.to_bytes()
        

        if self.ypp___r__q__ is not None:
        
            ___oj___j___ = NamedProperty()
            ___oj___j___.id = 0x8080
            ___oj___j___.guid = StandardPropertySet.ADDRESS
            ___oj___j___.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___oj___j___)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___oj___j___)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __ug__b__u_u = self.ypp___r__q__.encode(self._gm_g__n___a)
            zu___x_y_x_i = Stream("__substg1.0_" + ____w_ah__g_, __ug__b__u_u)
            n_b__sfzn___.append(zu___x_y_x_i)

            ____uawac___ = Property()
            ____uawac___.tag = ezi__t__sl__
            ____uawac___.type = PropertyType.STRING_8
            ____uawac___.size = len(__ug__b__u_u) + mkkh___d_lvf
            ____uawac___.is_readable = True
            ____uawac___.is_writeable = True

            _d____y___bd += ____uawac___.to_bytes()
        

        if self.q_vxh_uz___i is not None:
        
            pxhb___eugas = NamedProperty()
            pxhb___eugas.id = 0x8090
            pxhb___eugas.guid = StandardPropertySet.ADDRESS
            pxhb___eugas.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, pxhb___eugas)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(pxhb___eugas)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            qq__e__ev_kp = self.q_vxh_uz___i.encode(self._gm_g__n___a)
            _eoc_bl____e = Stream("__substg1.0_" + ____w_ah__g_, qq__e__ev_kp)
            n_b__sfzn___.append(_eoc_bl____e)

            fscf____r___ = Property()
            fscf____r___.tag = ezi__t__sl__
            fscf____r___.type = PropertyType.STRING_8
            fscf____r___.size = len(qq__e__ev_kp) + mkkh___d_lvf
            fscf____r___.is_readable = True
            fscf____r___.is_writeable = True

            _d____y___bd += fscf____r___.to_bytes()
        

        if self.qw__y_l__p__ is not None:
        
            ___c_t_o_qi_ = NamedProperty()
            ___c_t_o_qi_.id = 0x80A0
            ___c_t_o_qi_.guid = StandardPropertySet.ADDRESS
            ___c_t_o_qi_.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ___c_t_o_qi_)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(___c_t_o_qi_)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            ______e_____ = self.qw__y_l__p__.encode(self._gm_g__n___a)
            o_____n_mj__ = Stream("__substg1.0_" + ____w_ah__g_, ______e_____)
            n_b__sfzn___.append(o_____n_mj__)

            b__el__q_u_a = Property()
            b__el__q_u_a.tag = ezi__t__sl__
            b__el__q_u_a.type = PropertyType.STRING_8
            b__el__q_u_a.size = len(______e_____) + mkkh___d_lvf
            b__el__q_u_a.is_readable = True
            b__el__q_u_a.is_writeable = True

            _d____y___bd += b__el__q_u_a.to_bytes()
        

        if self._a___u____sj is not None:
        
            ____iw_m__ng = NamedProperty()
            ____iw_m__ng.id = 0x8082
            ____iw_m__ng.guid = StandardPropertySet.ADDRESS
            ____iw_m__ng.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, ____iw_m__ng)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(____iw_m__ng)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            ____x_o__k_f = self._a___u____sj.encode(self._gm_g__n___a)
            rl_nve_t_chk = Stream("__substg1.0_" + ____w_ah__g_, ____x_o__k_f)
            n_b__sfzn___.append(rl_nve_t_chk)

            __n__tt_r___ = Property()
            __n__tt_r___.tag = ezi__t__sl__
            __n__tt_r___.type = PropertyType.STRING_8
            __n__tt_r___.size = len(____x_o__k_f) + mkkh___d_lvf
            __n__tt_r___.is_readable = True
            __n__tt_r___.is_writeable = True

            _d____y___bd += __n__tt_r___.to_bytes()
        

        if self.v__kpwt___jh is not None:
        
            au___jgu_lzg = NamedProperty()
            au___jgu_lzg.id = 0x8092
            au___jgu_lzg.guid = StandardPropertySet.ADDRESS
            au___jgu_lzg.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, au___jgu_lzg)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(au___jgu_lzg)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            __e_u_i_ym__ = self.v__kpwt___jh.encode(self._gm_g__n___a)
            _p__vb____pd = Stream("__substg1.0_" + ____w_ah__g_, __e_u_i_ym__)
            n_b__sfzn___.append(_p__vb____pd)

            _t_w_o__gj_v = Property()
            _t_w_o__gj_v.tag = ezi__t__sl__
            _t_w_o__gj_v.type = PropertyType.STRING_8
            _t_w_o__gj_v.size = len(__e_u_i_ym__) + mkkh___d_lvf
            _t_w_o__gj_v.is_readable = True
            _t_w_o__gj_v.is_writeable = True

            _d____y___bd += _t_w_o__gj_v.to_bytes()
        

        if self.v_rn_m______ is not None:
        
            m____xuxkd_t = NamedProperty()
            m____xuxkd_t.id = 0x80A2
            m____xuxkd_t.guid = StandardPropertySet.ADDRESS
            m____xuxkd_t.type = NamedPropertyType.STRING

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, m____xuxkd_t)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(m____xuxkd_t)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            u_s____yp___ = self.v_rn_m______.encode(self._gm_g__n___a)
            oaey_p__kdlg = Stream("__substg1.0_" + ____w_ah__g_, u_s____yp___)
            n_b__sfzn___.append(oaey_p__kdlg)

            dqrw_u_kyk_s = Property()
            dqrw_u_kyk_s.tag = ezi__t__sl__
            dqrw_u_kyk_s.type = PropertyType.STRING_8
            dqrw_u_kyk_s.size = len(u_s____yp___) + mkkh___d_lvf
            dqrw_u_kyk_s.is_readable = True
            dqrw_u_kyk_s.is_writeable = True

            _d____y___bd += dqrw_u_kyk_s.to_bytes()
        

        if self.kiork_z_o__p is not None:
        
            n___a_m_n_fj = NamedProperty()
            n___a_m_n_fj.id = 0x8085
            n___a_m_n_fj.guid = StandardPropertySet.ADDRESS
            n___a_m_n_fj.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, n___a_m_n_fj)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(n___a_m_n_fj)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0102
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            ___wktqhzctk = Stream("__substg1.0_" + ____w_ah__g_, self.kiork_z_o__p)
            n_b__sfzn___.append(___wktqhzctk)

            _x_mfumxoz_o = Property()
            _x_mfumxoz_o.tag = ezi__t__sl__
            _x_mfumxoz_o.type = PropertyType.INTEGER_32
            _x_mfumxoz_o.size = len(self.kiork_z_o__p)
            _x_mfumxoz_o.is_readable = True
            _x_mfumxoz_o.is_writeable = True

            _d____y___bd += _x_mfumxoz_o.to_bytes()
        

        if self.n_dl_t_l____ is not None:
        
            r_llw_ato_ym = NamedProperty()
            r_llw_ato_ym.id = 0x8095
            r_llw_ato_ym.guid = StandardPropertySet.ADDRESS
            r_llw_ato_ym.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, r_llw_ato_ym)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(r_llw_ato_ym)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0102
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            _tojh_q___u_ = Stream("__substg1.0_" + ____w_ah__g_, self.n_dl_t_l____)
            n_b__sfzn___.append(_tojh_q___u_)

            p_y_v_____fx = Property()
            p_y_v_____fx.tag = ezi__t__sl__
            p_y_v_____fx.type = PropertyType.INTEGER_32
            p_y_v_____fx.size = len(self.n_dl_t_l____)
            p_y_v_____fx.is_readable = True
            p_y_v_____fx.is_writeable = True

            _d____y___bd += p_y_v_____fx.to_bytes()
        

        if self.____cve____g is not None:
        
            _x_t_zq____i = NamedProperty()
            _x_t_zq____i.id = 0x80A5
            _x_t_zq____i.guid = StandardPropertySet.ADDRESS
            _x_t_zq____i.type = NamedPropertyType.NUMERICAL

            _tgs__ywd___ = Message.x_j__na__gbt(__d_v___a_yf, _x_t_zq____i)

            if _tgs__ywd___ == -1:
            
                __d_v___a_yf.append(_x_t_zq____i)
                _tgs__ywd___ = len(__d_v___a_yf) - 1
            

            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | 0x0102
            ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

            p__sv____b__ = Stream("__substg1.0_" + ____w_ah__g_, self.____cve____g)
            n_b__sfzn___.append(p__sv____b__)

            udo___e_j_cg = Property()
            udo___e_j_cg.tag = ezi__t__sl__
            udo___e_j_cg.type = PropertyType.INTEGER_32
            udo___e_j_cg.size = len(self.____cve____g)
            udo___e_j_cg.is_readable = True
            udo___e_j_cg.is_writeable = True

            _d____y___bd += udo___e_j_cg.to_bytes()



        for e in range(len(self._r__n__wc_bq)):

            if self._r__n__wc_bq[e].value is not None:

                y_qm____k_zb = NamedProperty()

                if isinstance(self._r__n__wc_bq[e].tag, ExtendedPropertyId):

                    l_nvq_ia___o = self._r__n__wc_bq[e].tag

                    y_qm____k_zb.id   = l_nvq_ia___o.id
                    y_qm____k_zb.guid = l_nvq_ia___o.guid
                    y_qm____k_zb.type = NamedPropertyType.NUMERICAL

                else:

                    l_nvq_ia___o = self._r__n__wc_bq[e].tag

                    y_qm____k_zb.name = l_nvq_ia___o.name
                    y_qm____k_zb.guid = l_nvq_ia___o.guid
                    y_qm____k_zb.type = NamedPropertyType.STRING

                if Message.x_j__na__gbt(__d_v___a_yf, y_qm____k_zb) == -1:

                    __d_v___a_yf.append(y_qm____k_zb)
                    _tgs__ywd___ = len(__d_v___a_yf) - 1

                    ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | Message.jozp_k____zx(self._r__n__wc_bq[e].tag.type)

                    if self._r__n__wc_bq[e].tag.type == PropertyType.BOOLEAN or self._r__n__wc_bq[e].tag.type == PropertyType.INTEGER_16 or self._r__n__wc_bq[e].tag.type == PropertyType.INTEGER_32 or self._r__n__wc_bq[e].tag.type == PropertyType.INTEGER_64 or self._r__n__wc_bq[e].tag.type == PropertyType.FLOATING_32 or self._r__n__wc_bq[e].tag.type == PropertyType.FLOATING_64 or self._r__n__wc_bq[e].tag.type == PropertyType.FLOATING_TIME or self._r__n__wc_bq[e].tag.type == PropertyType.TIME:

                        hdhurb__lfto = Property()
                        hdhurb__lfto.tag = ezi__t__sl__
                        hdhurb__lfto.type = self._r__n__wc_bq[e].tag.type
                        hdhurb__lfto.value = self._r__n__wc_bq[e].value
                        hdhurb__lfto.is_readable = True
                        hdhurb__lfto.is_writeable = True

                        _d____y___bd += hdhurb__lfto.to_bytes()

                    elif self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_CURRENCY or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_FLOATING_32 or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_FLOATING_64 or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_FLOATING_TIME or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_GUID or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_INTEGER_16 or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_INTEGER_32 or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_INTEGER_64 or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_STRING or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_STRING_8 or self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_TIME:

                        pass

                    elif self._r__n__wc_bq[e].tag.type == PropertyType.MULTIPLE_BINARY:

                        ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

                        eynjn_yv_lq_ = bytearray()

                        _m_e_mzg____ = int.from_bytes(self._r__n__wc_bq[e].value[0:4], "little")

                        ____bpd_gwl_ = [None]*(_m_e_mzg____ + 1)

                        for i in range(_m_e_mzg____):
                            ____bpd_gwl_[i] = int.from_bytes(self._r__n__wc_bq[e].value[4 + i * 4: 4 + i * 4 + 4], "little")
                
                        ____bpd_gwl_[_m_e_mzg____] = len(self._r__n__wc_bq[e].value)

                        for i in range(len(____bpd_gwl_) - 1):

                            r_c__f_f_iit = (____bpd_gwl_[i + 1] - ____bpd_gwl_[i])
                            kn__y___efn_ = int.to_bytes(r_c__f_f_iit, 8, "little")

                            eynjn_yv_lq_ += kn__y___efn_
                            _yl_f__ko___ = self._r__n__wc_bq[e].value[____bpd_gwl_[i]: ____bpd_gwl_[i] + r_c__f_f_iit]

                            _gfd_hthczv_ = "__substg1.0_" + ____w_ah__g_ + "-" + str.format("{:08X}", i)
                            
                            j___a_x_____ = Stream(_gfd_hthczv_, _yl_f__ko___)
                            
                            n_b__sfzn___.append(j___a_x_____)
                        

                        tz_v_fu__xr_ = bytes(eynjn_yv_lq_)

                        o___b_ey___j = Stream("__substg1.0_" + ____w_ah__g_, tz_v_fu__xr_)
                        n_b__sfzn___.append(o___b_ey___j)

                        x_u_mv__f_kp = Property()
                        x_u_mv__f_kp.tag = ezi__t__sl__
                        x_u_mv__f_kp.type = PropertyType.MULTIPLE_BINARY
                        x_u_mv__f_kp.size = len(tz_v_fu__xr_)
                        x_u_mv__f_kp.is_readable = True
                        x_u_mv__f_kp.is_writeable = True

                        _d____y___bd += x_u_mv__f_kp.to_bytes()

                    else:

                        _yl_f__ko___ = self._r__n__wc_bq[e].value

                        if _yl_f__ko___ is not None and self._r__n__wc_bq[e].tag.type == PropertyType.STRING and self._gm_g__n___a != self.bn_lyk_isr_a:

                            rk_e_s_mli_a = _yl_f__ko___.decode(self.bn_lyk_isr_a)
                            _yl_f__ko___ = rk_e_s_mli_a.encode(self._gm_g__n___a)

                            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__

                        elif _yl_f__ko___ is not None and self._r__n__wc_bq[e].tag.type == PropertyType.STRING_8 and self._gm_g__n___a == self.bn_lyk_isr_a:

                            rk_e_s_mli_a = _yl_f__ko___.decode(self.__z_oxrob_zv)
                            _yl_f__ko___ = rk_e_s_mli_a.encode(self._gm_g__n___a)

                            ezi__t__sl__ = (0x8000 + _tgs__ywd___) << 16 | self.sll__adckt__


                        ____w_ah__g_ = str.format("{:08X}", ezi__t__sl__)

                        ____d___z_t_ = Stream("__substg1.0_" + ____w_ah__g_, _yl_f__ko___)
                        n_b__sfzn___.append(____d___z_t_)

                        hdhurb__lfto = Property()
                        hdhurb__lfto.tag = ezi__t__sl__

                        if (self._r__n__wc_bq[e].tag.type == PropertyType.BINARY or self._r__n__wc_bq[e].tag.type == PropertyType.OBJECT):
                            hdhurb__lfto.type = PropertyType.INTEGER_32
                        else:
                            hdhurb__lfto.type = PropertyType.STRING_8

                        hdhurb__lfto.size = Message.jgpr_zs_vz__(_yl_f__ko___, self._r__n__wc_bq[e].tag.type, self._gm_g__n___a)
                        hdhurb__lfto.is_readable = True
                        hdhurb__lfto.is_writeable = True

                        _d____y___bd += hdhurb__lfto.to_bytes()


        ne__vmw_____ = Stream("__properties_version1.0", bytes(_d____y___bd))
        n_b__sfzn___.append(ne__vmw_____)

        for i in range(len(self.__g_y__yifly)):

            __e_ph__r___ = str.format("__recip_version1.0_#{:08X}", i)
            _z___q_p_i__ = Storage(__e_ph__r___)

            b__lh_eua_bp = self.__g_y__yifly[i]

            _j_t___q_rj_ = bytearray()

            n_dzkv_b_l_j = bytes(8)
            _j_t___q_rj_ += n_dzkv_b_l_j


            f_h___qa___u = Property()
            f_h___qa___u.tag = 0x30000003
            f_h___qa___u.type = PropertyType.INTEGER_32
            f_h___qa___u.value = int.to_bytes(i, 4, "little")
            f_h___qa___u.is_readable = True
            f_h___qa___u.is_writeable = True

            _j_t___q_rj_ += f_h___qa___u.to_bytes()

            if b__lh_eua_bp.display_type != DisplayType.NONE:
            
                ___lfzxd_cau = Property()
                ___lfzxd_cau.tag = 0x39000003
                ___lfzxd_cau.type = PropertyType.INTEGER_32
                ___lfzxd_cau.value = int.to_bytes(EnumUtil.parse_display_type(b__lh_eua_bp.display_type), 4, "little")
                ___lfzxd_cau.is_readable = True
                ___lfzxd_cau.is_writeable = True

                _j_t___q_rj_ += ___lfzxd_cau.to_bytes()
            

            if b__lh_eua_bp.object_type != ObjectType.NONE:
            
                _wm___g_s__j = Property()
                _wm___g_s__j.tag = 0x0FFE0003
                _wm___g_s__j.type = PropertyType.INTEGER_32
                _wm___g_s__j.value = int.to_bytes(EnumUtil.parse_object_type(b__lh_eua_bp.object_type), 4, "little")
                _wm___g_s__j.is_readable = True
                _wm___g_s__j.is_writeable = True

                _j_t___q_rj_ += _wm___g_s__j.to_bytes()
            

            if b__lh_eua_bp.recipient_type != RecipientType.NONE:
            
                _its___l_r_j = Property()
                _its___l_r_j.tag = 0x0C150003
                _its___l_r_j.type = PropertyType.INTEGER_32
                _its___l_r_j.value = int.to_bytes(EnumUtil.parse_recipient_type(b__lh_eua_bp.recipient_type), 4, "little")
                _its___l_r_j.is_readable = True
                _its___l_r_j.is_writeable = True

                _j_t___q_rj_ += _its___l_r_j.to_bytes()
            

            if b__lh_eua_bp.display_name is not None:
            
                _u__f_______ = b__lh_eua_bp.display_name.encode(self._gm_g__n___a)

                _c___rn__r__ = Stream("__substg1.0_3001" + self._e_p_wn___m_, _u__f_______)
                _z___q_p_i__.directory_entries.append(_c___rn__r__)

                ____e__v_yr_ = Property()
                ____e__v_yr_.tag = 0x3001 << 16 | self.sll__adckt__
                ____e__v_yr_.type = PropertyType.STRING_8
                ____e__v_yr_.size = len(_u__f_______) + mkkh___d_lvf
                ____e__v_yr_.is_readable = True
                ____e__v_yr_.is_writeable = True

                _j_t___q_rj_ += ____e__v_yr_.to_bytes()

                _k_ru___u___ = Stream("__substg1.0_5FF6" + self._e_p_wn___m_, _u__f_______)
                _z___q_p_i__.directory_entries.append(_k_ru___u___)

                _k_qvp___hn_ = Property()
                _k_qvp___hn_.tag = 0x5FF6 << 16 | self.sll__adckt__
                _k_qvp___hn_.type = PropertyType.STRING_8
                _k_qvp___hn_.size = len(_u__f_______) + mkkh___d_lvf
                _k_qvp___hn_.is_readable = True
                _k_qvp___hn_.is_writeable = True

                _j_t___q_rj_ += _k_qvp___hn_.to_bytes()
            

            if b__lh_eua_bp.email_address is not None:
            
                _____q_t_yj_ = b__lh_eua_bp.email_address.encode(self._gm_g__n___a)
                v__uzb__fvt_ = Stream("__substg1.0_3003" + self._e_p_wn___m_, _____q_t_yj_)
                _z___q_p_i__.directory_entries.append(v__uzb__fvt_)

                _f_c_fljui__ = Property()
                _f_c_fljui__.tag = 0x3003 << 16 | self.sll__adckt__
                _f_c_fljui__.type = PropertyType.STRING_8
                _f_c_fljui__.size = len(_____q_t_yj_) + mkkh___d_lvf
                _f_c_fljui__.is_readable = True
                _f_c_fljui__.is_writeable = True

                _j_t___q_rj_ += _f_c_fljui__.to_bytes()
            

            if b__lh_eua_bp.address_type is not None:
            
                _tr_qx_mlb_b = b__lh_eua_bp.address_type.encode(self._gm_g__n___a)
                _s__d__wxx_i = Stream("__substg1.0_3002" + self._e_p_wn___m_, _tr_qx_mlb_b)
                _z___q_p_i__.directory_entries.append(_s__d__wxx_i)

                k_cng_n___pr = Property()
                k_cng_n___pr.tag = 0x3002 << 16 | self.sll__adckt__
                k_cng_n___pr.type = PropertyType.STRING_8
                k_cng_n___pr.size = len(_tr_qx_mlb_b) + mkkh___d_lvf
                k_cng_n___pr.is_readable = True
                k_cng_n___pr.is_writeable = True

                _j_t___q_rj_ += k_cng_n___pr.to_bytes()
            

            if b__lh_eua_bp.entry_id is not None:
            
                _______zt_ct = Stream("__substg1.0_0FFF0102", b__lh_eua_bp.entry_id)
                _z___q_p_i__.directory_entries.append(_______zt_ct)

                _cr__d__m__l = Property()
                _cr__d__m__l.tag = 0x0FFF0102
                _cr__d__m__l.type = PropertyType.BINARY
                _cr__d__m__l.size = len(b__lh_eua_bp.entry_id)
                _cr__d__m__l.is_readable = True
                _cr__d__m__l.is_writeable = True

                _j_t___q_rj_ += _cr__d__m__l.to_bytes()

                hxgb__rz_bu_ = Stream("__substg1.0_5FF70102", b__lh_eua_bp.entry_id)
                _z___q_p_i__.directory_entries.append(hxgb__rz_bu_)

                aa__gzkn____ = Property()
                aa__gzkn____.tag = 0x5FF70102
                aa__gzkn____.type = PropertyType.BINARY
                aa__gzkn____.size = len(b__lh_eua_bp.entry_id)
                aa__gzkn____.is_readable = True
                aa__gzkn____.is_writeable = True

                _j_t___q_rj_ += aa__gzkn____.to_bytes()
            

            if b__lh_eua_bp.search_key is not None:
            
                ____cg______ = Stream("__substg1.0_300B0102", b__lh_eua_bp.search_key)
                _z___q_p_i__.directory_entries.append(____cg______)

                __kwr__a___d = Property()
                __kwr__a___d.tag = 0x300B0102
                __kwr__a___d.type = PropertyType.BINARY
                __kwr__a___d.size = len(b__lh_eua_bp.search_key)
                __kwr__a___d.is_readable = True
                __kwr__a___d.is_writeable = True

                _j_t___q_rj_ += __kwr__a___d.to_bytes()
            

            if b__lh_eua_bp.instance_key is not None:
            
                pl_p_v_xm_o_ = Stream("__substg1.0_0FF60102", b__lh_eua_bp.instance_key)
                _z___q_p_i__.directory_entries.append(pl_p_v_xm_o_)

                bewsm_x_____ = Property()
                bewsm_x_____.tag = 0x0FF60102
                bewsm_x_____.type = PropertyType.BINARY
                bewsm_x_____.size = len(b__lh_eua_bp.instance_key)
                bewsm_x_____.is_readable = True
                bewsm_x_____.is_writeable = True

                _j_t___q_rj_ += bewsm_x_____.to_bytes()
            

            if b__lh_eua_bp.responsibility:
            
                c__aq___ysz_ = Property()
                c__aq___ysz_.tag = 0x0E0F000B
                c__aq___ysz_.type = PropertyType.BOOLEAN
                c__aq___ysz_.value = int.to_bytes(1, 1, "little")
                c__aq___ysz_.is_readable = True
                c__aq___ysz_.is_writeable = True

                _j_t___q_rj_ += c__aq___ysz_.to_bytes()
            

            if b__lh_eua_bp.send_rich_info:
            
                u___wo_wo_iz = Property()
                u___wo_wo_iz.tag = 0x3A40000B
                u___wo_wo_iz.type = PropertyType.BOOLEAN
                u___wo_wo_iz.value = int.to_bytes(1, 1, "little")
                u___wo_wo_iz.is_readable = True
                u___wo_wo_iz.is_writeable = True

                _j_t___q_rj_ += u___wo_wo_iz.to_bytes()
            

            if b__lh_eua_bp.send_internet_encoding > 0:
            
                __vp_hf_w___ = Property()
                __vp_hf_w___.tag = 0x3A710003
                __vp_hf_w___.type = PropertyType.INTEGER_32
                __vp_hf_w___.value = int.to_bytes(b__lh_eua_bp.send_internet_encoding, 4, "little")
                __vp_hf_w___.is_readable = True
                __vp_hf_w___.is_writeable = True

                _j_t___q_rj_ += __vp_hf_w___.to_bytes()
            

            if b__lh_eua_bp.smtp_address is not None:
            
                wi__s_p_cd__ = b__lh_eua_bp.smtp_address.encode(self._gm_g__n___a)
                __di_mon__o_ = Stream("__substg1.0_39FE" + self._e_p_wn___m_, wi__s_p_cd__)
                _z___q_p_i__.directory_entries.append(__di_mon__o_)

                t__d__f____u = Property()
                t__d__f____u.tag = 0x39FE << 16 | self.sll__adckt__
                t__d__f____u.type = PropertyType.STRING_8
                t__d__f____u.size = len(wi__s_p_cd__) + mkkh___d_lvf
                t__d__f____u.is_readable = True
                t__d__f____u.is_writeable = True

                _j_t___q_rj_ += t__d__f____u.to_bytes()
            

            if b__lh_eua_bp.display_name_7bit is not None:
            
                tirgt____le_ = b__lh_eua_bp.display_name_7bit.encode(self._gm_g__n___a)
                __kk_y_ho_en = Stream("__substg1.0_39FF" + self._e_p_wn___m_, tirgt____le_)
                _z___q_p_i__.directory_entries.append(__kk_y_ho_en)

                _dlf___dt___ = Property()
                _dlf___dt___.tag = 0x39FF << 16 | self.sll__adckt__
                _dlf___dt___.type = PropertyType.STRING_8
                _dlf___dt___.size = len(tirgt____le_) + mkkh___d_lvf
                _dlf___dt___.is_readable = True
                _dlf___dt___.is_writeable = True

                _j_t___q_rj_ += _dlf___dt___.to_bytes()
            

            if b__lh_eua_bp.transmitable_display_name is not None:
            
                _y_s___i____ = b__lh_eua_bp.transmitable_display_name.encode(self._gm_g__n___a)
                x_zgkcb_s_w_ = Stream("__substg1.0_3A20" + self._e_p_wn___m_, _y_s___i____)
                _z___q_p_i__.directory_entries.append(x_zgkcb_s_w_)

                a_m_rv_f_p_s = Property()
                a_m_rv_f_p_s.tag = 0x3A20 << 16 | self.sll__adckt__
                a_m_rv_f_p_s.type = PropertyType.STRING_8
                a_m_rv_f_p_s.size = len(_y_s___i____) + mkkh___d_lvf
                a_m_rv_f_p_s.is_readable = True
                a_m_rv_f_p_s.is_writeable = True

                _j_t___q_rj_ += a_m_rv_f_p_s.to_bytes()
            

            if b__lh_eua_bp.originating_address_type is not None:
            
                _q_ap_____i_ = b__lh_eua_bp.originating_address_type.encode(self._gm_g__n___a)
                _______u____ = Stream("__substg1.0_403D" + self._e_p_wn___m_, _q_ap_____i_)
                _z___q_p_i__.directory_entries.append(_______u____)

                _bds_l_qbghi = Property()
                _bds_l_qbghi.tag = 0x403D << 16 | self.sll__adckt__
                _bds_l_qbghi.type = PropertyType.STRING_8
                _bds_l_qbghi.size = len(_q_ap_____i_) + mkkh___d_lvf
                _bds_l_qbghi.is_readable = True
                _bds_l_qbghi.is_writeable = True

                _j_t___q_rj_ += _bds_l_qbghi.to_bytes()
            

            if b__lh_eua_bp.originating_email_address is not None:
            
                ____igk_fje_ = b__lh_eua_bp.originating_email_address.encode(self._gm_g__n___a)
                ___h____d_l_ = Stream("__substg1.0_403E" + self._e_p_wn___m_, ____igk_fje_)
                _z___q_p_i__.directory_entries.append(___h____d_l_)

                ___wl__q_v__ = Property()
                ___wl__q_v__.tag = 0x403E << 16 | self.sll__adckt__
                ___wl__q_v__.type = PropertyType.STRING_8
                ___wl__q_v__.size = len(____igk_fje_) + mkkh___d_lvf
                ___wl__q_v__.is_readable = True
                ___wl__q_v__.is_writeable = True

                _j_t___q_rj_ += ___wl__q_v__.to_bytes()
            

            _____wm____u = Stream("__properties_version1.0", bytes(_j_t___q_rj_))

            _z___q_p_i__.directory_entries.append(_____wm____u)

            n_b__sfzn___.append(_z___q_p_i__)
    

        for i in range(len(self.j____d____c_)):
        
            _____f___q__ = str.format("__attach_version1.0_#{:08X}", i)
            hrj_xw_r_l_q = Storage(_____f___q__)

            o_smy__q_j_d = self.j____d____c_[i]

            c_kj__ds_qut = bytearray()

            g__jt___zo__ = bytes(8)
            c_kj__ds_qut += g__jt___zo__

            m_iz_i__bu_h = Property()
            m_iz_i__bu_h.tag = 0x0E210003
            m_iz_i__bu_h.type = PropertyType.INTEGER_32
            m_iz_i__bu_h.value = int.to_bytes(i, 4, "little")
            m_iz_i__bu_h.is_readable = True
            m_iz_i__bu_h.is_writeable = False

            c_kj__ds_qut += m_iz_i__bu_h.to_bytes()

            u___v_g_rhf_ = Property()
            u___v_g_rhf_.tag = 0x7FFA0003
            u___v_g_rhf_.type = PropertyType.INTEGER_32
            u___v_g_rhf_.value = int.to_bytes(i, 4, "little")
            u___v_g_rhf_.is_readable = True
            u___v_g_rhf_.is_writeable = True

            c_kj__ds_qut += u___v_g_rhf_.to_bytes()

            o_smy__q_j_d.record_key = int.to_bytes(i, 4, "little")
            _hpiz____bv_ = Stream("__substg1.0_0FF90102", o_smy__q_j_d.record_key)
            hrj_xw_r_l_q.directory_entries.append(_hpiz____bv_)

            __j_r__u__vy = Property()
            __j_r__u__vy.tag = 0x0FF90102
            __j_r__u__vy.type = PropertyType.BINARY
            __j_r__u__vy.size = len(o_smy__q_j_d.record_key)
            __j_r__u__vy.is_readable = True
            __j_r__u__vy.is_writeable = True

            c_kj__ds_qut += __j_r__u__vy.to_bytes()

            if o_smy__q_j_d.additional_info is not None:
            
                _v__hgh___da = Stream("__substg1.0_370F0102", o_smy__q_j_d.additional_info)
                hrj_xw_r_l_q.directory_entries.append(_v__hgh___da)

                eglp____v_c_ = Property()
                eglp____v_c_.tag = 0x370F0102
                eglp____v_c_.type = PropertyType.BINARY
                eglp____v_c_.size = len(o_smy__q_j_d.additional_info)
                eglp____v_c_.is_readable = True
                eglp____v_c_.is_writeable = True

                c_kj__ds_qut += eglp____v_c_.to_bytes()
            

            if o_smy__q_j_d.content_base is not None:
            
                s___y___c__h = o_smy__q_j_d.content_base.encode(self._gm_g__n___a)
                ___te_l__fe_ = Stream("__substg1.0_3711" + self._e_p_wn___m_, s___y___c__h)
                hrj_xw_r_l_q.directory_entries.append(___te_l__fe_)

                _p_e____iz_f = Property()
                _p_e____iz_f.tag = 0x3711 << 16 | self.sll__adckt__
                _p_e____iz_f.type = PropertyType.STRING_8
                _p_e____iz_f.size = len(s___y___c__h) + mkkh___d_lvf
                _p_e____iz_f.is_readable = True
                _p_e____iz_f.is_writeable = True

                c_kj__ds_qut += _p_e____iz_f.to_bytes()
            

            if o_smy__q_j_d.content_id is not None:
            
                q_n_n_u____d = o_smy__q_j_d.content_id.encode(self._gm_g__n___a)
                jst_d__bo___ = Stream("__substg1.0_3712" + self._e_p_wn___m_, q_n_n_u____d)
                hrj_xw_r_l_q.directory_entries.append(jst_d__bo___)

                _r____i_xx_w = Property()
                _r____i_xx_w.tag = 0x3712 << 16 | self.sll__adckt__
                _r____i_xx_w.type = PropertyType.STRING_8
                _r____i_xx_w.size = len(q_n_n_u____d) + mkkh___d_lvf
                _r____i_xx_w.is_readable = True
                _r____i_xx_w.is_writeable = True

                c_kj__ds_qut += _r____i_xx_w.to_bytes()
            

            if o_smy__q_j_d.content_location is not None:
            
                m____y__it__ = o_smy__q_j_d.content_location.encode(self._gm_g__n___a)
                _dj__ux_ds_t = Stream("__substg1.0_3713" + self._e_p_wn___m_, m____y__it__)
                hrj_xw_r_l_q.directory_entries.append(_dj__ux_ds_t)

                f_m_kags_c_z = Property()
                f_m_kags_c_z.tag = 0x3713 << 16 | self.sll__adckt__
                f_m_kags_c_z.type = PropertyType.STRING_8
                f_m_kags_c_z.size = len(m____y__it__) + mkkh___d_lvf
                f_m_kags_c_z.is_readable = True
                f_m_kags_c_z.is_writeable = True

                c_kj__ds_qut += f_m_kags_c_z.to_bytes()
            

            if o_smy__q_j_d.content_disposition is not None:
            
                u_uvph_f___x = o_smy__q_j_d.content_disposition.encode(self._gm_g__n___a)
                ___b_m__p___ = Stream("__substg1.0_3716" + self._e_p_wn___m_, u_uvph_f___x)
                hrj_xw_r_l_q.directory_entries.append(___b_m__p___)

                _____q______ = Property()
                _____q______.tag = 0x3716 << 16 | self.sll__adckt__
                _____q______.type = PropertyType.STRING_8
                _____q______.size = len(u_uvph_f___x) + mkkh___d_lvf
                _____q______.is_readable = True
                _____q______.is_writeable = True

                c_kj__ds_qut += _____q______.to_bytes()
            

            if o_smy__q_j_d.data is not None:
            
                if o_smy__q_j_d.method == AttachmentMethod.OLE:
                
                    _w__qi__hv__ = Storage("__substg1.0_3701000D")
                    hrj_xw_r_l_q.directory_entries.append(_w__qi__hv__)

                    vlsu__d___xc = bytearray(o_smy__q_j_d.data)
                    _r__tn______ = CompoundFile(vlsu__d___xc)

                    _w__qi__hv__.class_id = _r__tn______.root.class_id

                    _w__qi__hv__.directory_entries.extend(_r__tn______.root.directory_entries)                    

                    m_r_j______h = Property()
                    _____r___oa_.tag = 0x3701000D
                    m_r_j______h.type = PropertyType.OBJECT
                    m_r_j______h.size = 4_000_000_000
                    m_r_j______h.is_readable = True
                    m_r_j______h.is_writeable = True
                    _l___t__sq_o = bytearray(m_r_j______h.to_bytes())
                    _l___t__sq_o[12] = 4

                    c_kj__ds_qut += _l___t__sq_o
                
                else:
                
                    _hruar_b_mt_ = Stream("__substg1.0_37010102", o_smy__q_j_d.data)
                    hrj_xw_r_l_q.directory_entries.append(_hruar_b_mt_)

                    m_r_j______h = Property()
                    m_r_j______h.tag = 0x37010102
                    m_r_j______h.type = PropertyType.BINARY
                    m_r_j______h.size = len(o_smy__q_j_d.data)
                    m_r_j______h.is_readable = True
                    m_r_j______h.is_writeable = True

                    c_kj__ds_qut += m_r_j______h.to_bytes()


            if o_smy__q_j_d.encoding is not None:
            
                ____ta_x____ = Stream("__substg1.0_37020102", o_smy__q_j_d.encoding)
                hrj_xw_r_l_q.directory_entries.append(____ta_x____)

                d__sjm_xcn_n = Property()
                d__sjm_xcn_n.tag = 0x37020102
                d__sjm_xcn_n.type = PropertyType.BINARY
                d__sjm_xcn_n.size = len(o_smy__q_j_d.encoding)
                d__sjm_xcn_n.is_readable = True
                d__sjm_xcn_n.is_writeable = True

                c_kj__ds_qut += d__sjm_xcn_n.to_bytes()


            if o_smy__q_j_d.extension is not None:
            
                wa____o__k__ = o_smy__q_j_d.extension.encode(self._gm_g__n___a)
                _fh_u_jl_rad = Stream("__substg1.0_3703" + self._e_p_wn___m_, wa____o__k__)
                hrj_xw_r_l_q.directory_entries.append(_fh_u_jl_rad)

                _iq_bi___yi_ = Property()
                _iq_bi___yi_.tag = 0x3703 << 16 | self.sll__adckt__
                _iq_bi___yi_.type = PropertyType.STRING_8
                _iq_bi___yi_.size = len(wa____o__k__) + mkkh___d_lvf
                _iq_bi___yi_.is_readable = True
                _iq_bi___yi_.is_writeable = True

                c_kj__ds_qut += _iq_bi___yi_.to_bytes()
            

            if o_smy__q_j_d.file_name is not None:
            
                o__r__k_u___ = o_smy__q_j_d.file_name.encode(self._gm_g__n___a)
                ptkisih_ees_ = Stream("__substg1.0_3704" + self._e_p_wn___m_, o__r__k_u___)
                hrj_xw_r_l_q.directory_entries.append(ptkisih_ees_)

                _dx_r____yk_ = Property()
                _dx_r____yk_.tag = 0x3704 << 16 | self.sll__adckt__
                _dx_r____yk_.type = PropertyType.STRING_8
                _dx_r____yk_.size = len(o__r__k_u___) + mkkh___d_lvf
                _dx_r____yk_.is_readable = True
                _dx_r____yk_.is_writeable = True

                c_kj__ds_qut += _dx_r____yk_.to_bytes()
            

            if o_smy__q_j_d.flags != AttachmentFlags.NONE:
            
                jd__yn_wg_u_ = Property()
                jd__yn_wg_u_.tag = 0x37140003
                jd__yn_wg_u_.type = PropertyType.INTEGER_32
                jd__yn_wg_u_.value = int.to_bytes(EnumUtil.parse_attachment_flags(o_smy__q_j_d.flags), 4, "little")
                jd__yn_wg_u_.is_readable = True
                jd__yn_wg_u_.is_writeable = True

                c_kj__ds_qut += jd__yn_wg_u_.to_bytes()
            

            if o_smy__q_j_d.long_file_name is not None:
            
                y___xo______ = o_smy__q_j_d.long_file_name.encode(self._gm_g__n___a)
                _dnyd_qu_d__ = Stream("__substg1.0_3707" + self._e_p_wn___m_, y___xo______)
                hrj_xw_r_l_q.directory_entries.append(_dnyd_qu_d__)

                _p___dci____ = Property()
                _p___dci____.tag = 0x3707 << 16 | self.sll__adckt__
                _p___dci____.type = PropertyType.STRING_8
                _p___dci____.size = len(y___xo______) + mkkh___d_lvf
                _p___dci____.is_readable = True
                _p___dci____.is_writeable = True

                c_kj__ds_qut += _p___dci____.to_bytes()
            

            if o_smy__q_j_d.long_path_name is not None:
            
                dm_x__ago_as = o_smy__q_j_d.long_path_name.encode(self._gm_g__n___a)
                ______h_rljo = Stream("__substg1.0_370D" + self._e_p_wn___m_, dm_x__ago_as)
                hrj_xw_r_l_q.directory_entries.append(______h_rljo)

                b__c__t_e___ = Property()
                b__c__t_e___.tag = 0x370D << 16 | self.sll__adckt__
                b__c__t_e___.type = PropertyType.STRING_8
                b__c__t_e___.size = len(dm_x__ago_as) + mkkh___d_lvf
                b__c__t_e___.is_readable = True
                b__c__t_e___.is_writeable = True

                c_kj__ds_qut += b__c__t_e___.to_bytes()
            

            if o_smy__q_j_d.method != AttachmentMethod.NONE:
            
                r__q_z_aasq_ = Property()
                r__q_z_aasq_.tag = 0x37050003
                r__q_z_aasq_.type = PropertyType.INTEGER_32
                r__q_z_aasq_.value = int.to_bytes(EnumUtil.parse_attachment_method(o_smy__q_j_d.method), 4, "little")
                r__q_z_aasq_.is_readable = True
                r__q_z_aasq_.is_writeable = True

                c_kj__ds_qut += r__q_z_aasq_.to_bytes()
            

            if o_smy__q_j_d.mime_sequence > 0:
            
                va___xp_me__ = Property()
                va___xp_me__.tag = 0x37100003
                va___xp_me__.type = PropertyType.INTEGER_32
                va___xp_me__.value = int.to_bytes(o_smy__q_j_d.mime_sequence, 4, "little")
                va___xp_me__.is_readable = True
                va___xp_me__.is_writeable = True

                c_kj__ds_qut += va___xp_me__.to_bytes()
            

            if o_smy__q_j_d.mime_tag is not None:
            
                i_c_a_iv____ = o_smy__q_j_d.mime_tag.encode(self._gm_g__n___a)
                bi__n_s_w___ = Stream("__substg1.0_370E" + self._e_p_wn___m_, i_c_a_iv____)
                hrj_xw_r_l_q.directory_entries.append(bi__n_s_w___)

                ___s_v_d_fb_ = Property()
                ___s_v_d_fb_.tag = 0x370E << 16 | self.sll__adckt__
                ___s_v_d_fb_.type = PropertyType.STRING_8
                ___s_v_d_fb_.size = len(i_c_a_iv____) + mkkh___d_lvf
                ___s_v_d_fb_.is_readable = True
                ___s_v_d_fb_.is_writeable = True

                c_kj__ds_qut += ___s_v_d_fb_.to_bytes()
            

            if o_smy__q_j_d.path_name is not None:
            
                y_fjryfi____ = o_smy__q_j_d.path_name.encode(self._gm_g__n___a)
                k__aq__q___t = Stream("__substg1.0_3708" + self._e_p_wn___m_, y_fjryfi____)
                hrj_xw_r_l_q.directory_entries.append(k__aq__q___t)

                w_u_k_z_____ = Property()
                w_u_k_z_____.tag = 0x3708 << 16 | self.sll__adckt__
                w_u_k_z_____.type = PropertyType.STRING_8
                w_u_k_z_____.size = len(y_fjryfi____) + mkkh___d_lvf
                w_u_k_z_____.is_readable = True
                w_u_k_z_____.is_writeable = True

                c_kj__ds_qut += w_u_k_z_____.to_bytes()
            

            if o_smy__q_j_d.rendering is not None:
            
                cq____d__vj_ = Stream("__substg1.0_37090102", o_smy__q_j_d.rendering)
                hrj_xw_r_l_q.directory_entries.append(cq____d__vj_)

                _d___n_v___r = Property()
                _d___n_v___r.tag = 0x37090102
                _d___n_v___r.type = PropertyType.BINARY
                _d___n_v___r.size = len(o_smy__q_j_d.rendering)
                _d___n_v___r.is_readable = True
                _d___n_v___r.is_writeable = True

                c_kj__ds_qut += _d___n_v___r.to_bytes()
            

            if o_smy__q_j_d.rendering_position > 0:
            
                _imh_tvp_b_k = Property()
                _imh_tvp_b_k.tag = 0x370b0003
                _imh_tvp_b_k.type = PropertyType.INTEGER_32
                _imh_tvp_b_k.value = int.to_bytes(o_smy__q_j_d.rendering_position, 4, "little")
                _imh_tvp_b_k.is_readable = True
                _imh_tvp_b_k.is_writeable = True

                c_kj__ds_qut += _imh_tvp_b_k.to_bytes()
            

            if o_smy__q_j_d.size > 0:
            
                _nh___zvyo__ = Property()
                _nh___zvyo__.tag = 0x0E200003
                _nh___zvyo__.type = PropertyType.INTEGER_32
                _nh___zvyo__.value = int.to_bytes(o_smy__q_j_d.size, 4, "little")
                _nh___zvyo__.is_readable = True
                _nh___zvyo__.is_writeable = True

                c_kj__ds_qut += _nh___zvyo__.to_bytes()
            

            if o_smy__q_j_d.tag is not None:
            
                un____uzs_yj = Stream("__substg1.0_370A0102", o_smy__q_j_d.tag)
                hrj_xw_r_l_q.directory_entries.append(un____uzs_yj)

                _let____si__ = Property()
                _let____si__.tag = 0x370A0102
                _let____si__.type = PropertyType.BINARY
                _let____si__.size = len(o_smy__q_j_d.tag)
                _let____si__.is_readable = True
                _let____si__.is_writeable = True

                c_kj__ds_qut += _let____si__.to_bytes()
            

            if o_smy__q_j_d.transport_name is not None:
            
                t____wf__lzt = o_smy__q_j_d.transport_name.encode(self._gm_g__n___a)
                tqa___f___i_ = Stream("__substg1.0_370C" + self._e_p_wn___m_, t____wf__lzt)
                hrj_xw_r_l_q.directory_entries.append(tqa___f___i_)

                d__________d = Property()
                d__________d.tag = 0x370C << 16 | self.sll__adckt__
                d__________d.type = PropertyType.STRING_8
                d__________d.size = len(t____wf__lzt) + mkkh___d_lvf
                d__________d.is_readable = True
                d__________d.is_writeable = True

                c_kj__ds_qut += d__________d.to_bytes()
            

            if o_smy__q_j_d.display_name is not None:
            
                _u__f_______ = o_smy__q_j_d.display_name.encode(self._gm_g__n___a)
                _c___rn__r__ = Stream("__substg1.0_3001" + self._e_p_wn___m_, _u__f_______)
                hrj_xw_r_l_q.directory_entries.append(_c___rn__r__)

                ____e__v_yr_ = Property()
                ____e__v_yr_.tag = 0x3001 << 16 | self.sll__adckt__
                ____e__v_yr_.type = PropertyType.STRING_8
                ____e__v_yr_.size = len(_u__f_______) + mkkh___d_lvf
                ____e__v_yr_.is_readable = True
                ____e__v_yr_.is_writeable = True

                c_kj__ds_qut += ____e__v_yr_.to_bytes()
            

            if o_smy__q_j_d.embedded_message is not None and o_smy__q_j_d.method != AttachmentMethod.OLE:
            
                r_b_q__p___h = o_smy__q_j_d.embedded_message.__nfho_____d(__d_v___a_yf)

                ____jn____m_ = Storage("__substg1.0_3701000D")

                ____jn____m_.directory_entries.extend(r_b_q__p___h)
                
                hrj_xw_r_l_q.directory_entries.append(____jn____m_)

                jitp_kfiw___ = Property()
                jitp_kfiw___.tag = 0x3701000D
                jitp_kfiw___.type = PropertyType.OBJECT
                jitp_kfiw___.size = 4_000_000_000
                jitp_kfiw___.is_readable = True
                jitp_kfiw___.is_writeable = True

                _in__oacs__k = bytearray(jitp_kfiw___.to_bytes())
                _in__oacs__k[12] = 1

                c_kj__ds_qut += _in__oacs__k
            

            if o_smy__q_j_d.object_type != ObjectType.NONE:
            
                _wm___g_s__j = Property()
                _wm___g_s__j.tag = 0x0FFE0003
                _wm___g_s__j.type = PropertyType.INTEGER_32
                _wm___g_s__j.value = int.to_bytes(EnumUtil.parse_object_type(o_smy__q_j_d.object_type), 4, "little")
                _wm___g_s__j.is_readable = True
                _wm___g_s__j.is_writeable = True

                c_kj__ds_qut += _wm___g_s__j.to_bytes()
            

            if o_smy__q_j_d.is_hidden:
            
                isw_jy_tcw_i = Property()
                isw_jy_tcw_i.tag = 0x7FFE000B
                isw_jy_tcw_i.type = PropertyType.BOOLEAN
                isw_jy_tcw_i.value = int.to_bytes(1, 1, "little")
                isw_jy_tcw_i.is_readable = True
                isw_jy_tcw_i.is_writeable = True

                c_kj__ds_qut += isw_jy_tcw_i.to_bytes()
            

            if o_smy__q_j_d.is_contact_photo:
            
                _fhc__fb__uc = Property()
                _fhc__fb__uc.tag = 0x7FFF000B
                _fhc__fb__uc.type = PropertyType.BOOLEAN
                _fhc__fb__uc.value = int.to_bytes(1, 1, "little")
                _fhc__fb__uc.is_readable = True
                _fhc__fb__uc.is_writeable = True

                c_kj__ds_qut += _fhc__fb__uc.to_bytes()
            

            if o_smy__q_j_d.creation_time > datetime.datetime(1901,1,1):
            
                j____h_x_v_h = datetime.datetime(1601,1,1)
                i_x____hz_to = int((o_smy__q_j_d.creation_time - j____h_x_v_h).total_seconds()) * 10_000_000

                __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

                __okm_jmcx__ = Property()
                __okm_jmcx__.tag = 0x30070040
                __okm_jmcx__.type = PropertyType.TIME
                __okm_jmcx__.value = __cwx_qbk___
                __okm_jmcx__.is_readable = True
                __okm_jmcx__.is_writeable = False

                c_kj__ds_qut += __okm_jmcx__.to_bytes()
            

            if o_smy__q_j_d.last_modification_time > datetime.datetime(1901,1,1):
            
                j____h_x_v_h = datetime.datetime(1601,1,1)
                i_x____hz_to = int((o_smy__q_j_d.last_modification_time - j____h_x_v_h).total_seconds()) * 10_000_000

                __cwx_qbk___ = i_x____hz_to.to_bytes(8, "little")

                __cwx_qbk___ = int.to_bytes(i_x____hz_to, 8, "little")

                _yofpl_kej_s = Property()
                _yofpl_kej_s.tag = 0x30080040
                _yofpl_kej_s.type = PropertyType.TIME
                _yofpl_kej_s.value = __cwx_qbk___
                _yofpl_kej_s.is_readable = True
                _yofpl_kej_s.is_writeable = False

                c_kj__ds_qut += _yofpl_kej_s.to_bytes()
            

            if o_smy__q_j_d.data_object_storage is not None and o_smy__q_j_d.method == AttachmentMethod.OLE:            
                hrj_xw_r_l_q.directory_entries.append(o_smy__q_j_d.data_object_storage)
                hrj_xw_r_l_q.directory_entries.append(o_smy__q_j_d.properties_stream)            
            else:            
                a__uop__n___ = Stream("__properties_version1.0", bytes(c_kj__ds_qut))
                hrj_xw_r_l_q.directory_entries.append(a__uop__n___)
            
            n_b__sfzn___.append(hrj_xw_r_l_q)

        return n_b__sfzn___
            
    @staticmethod
    def t_z__y_g_o__(id, _____r_u__z_):
        if _____r_u__z_ is not None and len(_____r_u__z_) == 16:

            wu_d_fe__x__ = int.from_bytes(_____r_u__z_[0: 8], "little")
            __ig____b__s = int.from_bytes(_____r_u__z_[8: 16], "little")

            rk_e_s_mli_a  = str(id) + "-" + str(wu_d_fe__x__) + "-" + str(__ig____b__s)

            return rk_e_s_mli_a
        else:
            return str(id)

    @staticmethod
    def xh_nz___yzlo(reply_to):

        _____q_j__l_ = reply_to.split(';')
        eynjn_yv_lq_ = bytearray()

        for i in range(len(_____q_j__l_)):
            
            s_a__ycl____ = bytes([0x00, 0x00, 0x00, 0x00, 0x81, 0x2B, 0x1F, 0xA4, 0xBE, 0xA3, 0x10, 0x19, 0x9D, 0x6E, 0x00, 0xDD, 0x01, 0x0F, 0x54, 0x02, 0x00, 0x00, 0x01, 0x80])

            hm_u___ubmc_ = (_____q_j__l_[i] + "\0SMTP\0" + _____q_j__l_[i] + "\0").encode("utf-16-le")
            hb_______hw_ = bytes([0x00, 0x00])

            rf_k_a__e_wr = len(s_a__ycl____) + len(hm_u___ubmc_)
            
            eynjn_yv_lq_ += int.to_bytes(rf_k_a__e_wr, 4, "little")
            eynjn_yv_lq_ += s_a__ycl____
            eynjn_yv_lq_ += hm_u___ubmc_
            eynjn_yv_lq_ += hb_______hw_

        _gj_c_______ = bytearray(8 + len(eynjn_yv_lq_))

        __e____z_ew_ = len(_____q_j__l_)
        _wa_sc___co_ = len(_gj_c_______) - 8

        _gj_c_______[0:4] = int.to_bytes(__e____z_ew_, 4, "little")
        _gj_c_______[4:8] = int.to_bytes(_wa_sc___co_, 4, "little")
        _gj_c_______[8:]  = eynjn_yv_lq_[0:]

        return bytes(_gj_c_______)

    @staticmethod
    def s_____ysb_be(zs___wa____d):

        _fstrno_nso_ = "cp1252"

        _g__nvg_o___ = zs___wa____d.find("ansicpg")

        if _g__nvg_o___ > -1:

            s_e_e_hs_o__ = zs___wa____d.find("\\", _g__nvg_o___ + 7)

            if s_e_e_hs_o__ > -1:
                
                _en__duml_nk = zs___wa____d[_g__nvg_o___ + 7: s_e_e_hs_o__]

                try:
                    ____k_____l_ = int(_en__duml_nk)
                    _fstrno_nso_ = Message.qb_s_dghkmbh(____k_____l_)
                except:
                    pass


        return _fstrno_nso_

    @staticmethod
    def __e_________(__pf_dc_vs__, p__pc__npa__, f____q____f_, ___wkbztp_d_):

        ___h_bzni_b_ = __pf_dc_vs__[0: ___wkbztp_d_]
        ov__us__j_a_ = f____q____f_
        __e_bx______ = -1

        for d_______kp__ in p__pc__npa__:

            k_ymh___l__l = ___h_bzni_b_.rfind("\\" + d_______kp__)

            if k_ymh___l__l > -1 and k_ymh___l__l > __e_bx______:
                ov__us__j_a_ = p__pc__npa__[d_______kp__] if p__pc__npa__[d_______kp__] is not None else f____q____f_
                __e_bx______ = k_ymh___l__l

        return ov__us__j_a_


    @staticmethod
    def ____z___gnkj(_lsbqo__s___):

        zs___wa____d = ""

        try:
            zs___wa____d = _lsbqo__s___.decode("utf_8")
        except:
            return (None, None)
                
        ___b_xq__ed_ = Message.s_____ysb_be(zs___wa____d)
        p__pc__npa__ = Message.w__lr___t__u(zs___wa____d)

        zs___wa____d = zs___wa____d.replace("\n\r{", "{")
        
        __pf_dc_vs__ = None

        qt_s_od____i = zs___wa____d.find("{\\*\\htmltag")

        if qt_s_od____i > -1:

            __pf_dc_vs__ = zs___wa____d[qt_s_od____i:]

            gezyvt_gn__x = __pf_dc_vs__.find("\\'")

            while gezyvt_gn__x > -1:

                ov__us__j_a_ = Message.__e_________(__pf_dc_vs__, p__pc__npa__, ___b_xq__ed_, gezyvt_gn__x)
                
                xsbdlo_htw_v = __pf_dc_vs__.find("\\'", gezyvt_gn__x + 2)
                _pye__rj___g = None
                r_m____py_o_ = None

                try:

                    if xsbdlo_htw_v == gezyvt_gn__x + 4:

                        _pye__rj___g = __pf_dc_vs__[gezyvt_gn__x: gezyvt_gn__x + 8]

                        s_oi____z_j_ = _pye__rj___g[2: 4]
                        _dn____i__r_ = _pye__rj___g[6: 8]

                        __m_d_px___f = int(s_oi____z_j_, 16)
                        _____nl_s__k = int(_dn____i__r_, 16)

                        r_m____py_o_ = bytes([__m_d_px___f, _____nl_s__k])

                    else:

                        _pye__rj___g = __pf_dc_vs__[gezyvt_gn__x: gezyvt_gn__x + 4]
                        s_oi____z_j_ = _pye__rj___g[2:]
                        __m_d_px___f = int(s_oi____z_j_, 16)                    
                        r_m____py_o_ = bytes([__m_d_px___f])


                    if r_m____py_o_ is not None and _pye__rj___g is not None:

                        ___y_iqaii__ = r_m____py_o_.decode(ov__us__j_a_)                  
                        __pf_dc_vs__ = __pf_dc_vs__.replace(_pye__rj___g, ___y_iqaii__)


                except:
                    __pf_dc_vs__ = __pf_dc_vs__.replace(_pye__rj___g, _pye__rj___g[1:])

                gezyvt_gn__x = __pf_dc_vs__.find("\\'")

            __tbm_g_uq__ = 0

            while __tbm_g_uq__ > -1:

                __tbm_g_uq__ = __pf_dc_vs__.find("{\\*\\htmltag", 0)

                if __tbm_g_uq__ > -1:

                    zq_____mb_ph = __pf_dc_vs__.find("}", __tbm_g_uq__)
                    ___sge___lpr = __pf_dc_vs__.find(" ", __tbm_g_uq__)
                    dto___jyg_vm = __pf_dc_vs__.find("<", __tbm_g_uq__)

                    if dto___jyg_vm > -1 and zq_____mb_ph > -1 and dto___jyg_vm < zq_____mb_ph and dto___jyg_vm < ___sge___lpr:

                        _zk__w____l_ = __pf_dc_vs__[__tbm_g_uq__: zq_____mb_ph]
                        ____nese___x = __pf_dc_vs__[dto___jyg_vm: zq_____mb_ph]

                        __pf_dc_vs__ = __pf_dc_vs__.replace(_zk__w____l_, ____nese___x)

                    elif ___sge___lpr > -1 and zq_____mb_ph > -1 and ___sge___lpr < zq_____mb_ph:

                        _zk__w____l_ = __pf_dc_vs__[__tbm_g_uq__: zq_____mb_ph]
                        ____nese___x = __pf_dc_vs__[___sge___lpr + 1: zq_____mb_ph]

                        __pf_dc_vs__ = __pf_dc_vs__.replace(_zk__w____l_, ____nese___x)

                    else:
                        _zk__w____l_ = __pf_dc_vs__[__tbm_g_uq__: zq_____mb_ph]
                        __pf_dc_vs__ = __pf_dc_vs__.replace(_zk__w____l_, "")


            ekc__l_shzp_ = []

            _s____i___w_ = 0
            t_nk__v__i__ = 0

            while _s____i___w_ > -1 and t_nk__v__i__ > -1:

                _s____i___w_ = __pf_dc_vs__.find("\\htmlrtf", _s____i___w_)

                if _s____i___w_ > -1:

                    t_nk__v__i__ = __pf_dc_vs__.find("\\htmlrtf0", _s____i___w_)
                    zwbjfnaw_f_t = __pf_dc_vs__.find("\\htmlrtf0 ", _s____i___w_)

                    _p_iz_frd__u = 10 if t_nk__v__i__ == zwbjfnaw_f_t else 9

                    if t_nk__v__i__ > -1:

                        ekc__l_shzp_.append(_s____i___w_)
                        ekc__l_shzp_.append(t_nk__v__i__ + _p_iz_frd__u)

                        _s____i___w_ = t_nk__v__i__ + _p_iz_frd__u

                else:
                    t_nk__v__i__ = -1

            y_____f_s___ = []

            u_n______vtv = 0

            for i in range(0, len(ekc__l_shzp_) - 1, 2):

                ___x_____u_x = ekc__l_shzp_[i]
                k_q__sg___d_ = ekc__l_shzp_[i + 1]
                y_____f_s___.append(__pf_dc_vs__[u_n______vtv: ___x_____u_x])
                u_n______vtv = k_q__sg___d_


            y_____f_s___.append(__pf_dc_vs__[u_n______vtv: len(__pf_dc_vs__)])

            __pf_dc_vs__ = "".join(y_____f_s___)

            j_____tz_yr_ = []

            ____oah_xi_i = 0
            _o_i_bbu____ = 0

            while ____oah_xi_i > -1 and _o_i_bbu____ > -1:

                ____oah_xi_i = __pf_dc_vs__.find("{\\pntext", ____oah_xi_i)

                if ____oah_xi_i > -1:

                    _o_i_bbu____ = __pf_dc_vs__.find("}", ____oah_xi_i)

                    if _o_i_bbu____ > -1:

                        j_____tz_yr_.append(____oah_xi_i)
                        j_____tz_yr_.append(_o_i_bbu____ + 1)

                        ____oah_xi_i = _o_i_bbu____ + 1

                else:
                    _o_i_bbu____ = -1

            y_____f_s___ = []

            u_n______vtv = 0

            for i in  range(0, len(j_____tz_yr_) - 1, 2):
                
                ___x_____u_x = j_____tz_yr_[i]
                k_q__sg___d_ = j_____tz_yr_[i + 1]
                y_____f_s___.append(__pf_dc_vs__[u_n______vtv: ___x_____u_x])
                u_n______vtv = k_q__sg___d_


            y_____f_s___.append(__pf_dc_vs__[u_n______vtv: len(__pf_dc_vs__)])

            __pf_dc_vs__ = "".join(y_____f_s___)

            _i_i_u_y_up_ = []

            _to_rio_g_xt = __pf_dc_vs__.find("{\\*\\mhtmltag")
            _tv___pu__q_ = 0
            om_ul__i_av_ = _to_rio_g_xt

            while _to_rio_g_xt > -1:

                __qj_n_qt_be = __pf_dc_vs__.find("{", om_ul__i_av_ + 1)
                u_k_gn_m_ma_ = __pf_dc_vs__.find("}", om_ul__i_av_ + 1)

                if u_k_gn_m_ma_ == -1:
                    break

                elif _tv___pu__q_ == 0 and (u_k_gn_m_ma_ < __qj_n_qt_be or __qj_n_qt_be == -1):

                    _i_i_u_y_up_.append(_to_rio_g_xt)
                    _i_i_u_y_up_.append(u_k_gn_m_ma_)

                    om_ul__i_av_ = u_k_gn_m_ma_
                    _to_rio_g_xt = __pf_dc_vs__.find("{\\*\\mhtmltag", om_ul__i_av_ + 1)

                    om_ul__i_av_ = _to_rio_g_xt

                elif _tv___pu__q_ > 0 and (u_k_gn_m_ma_ < __qj_n_qt_be or __qj_n_qt_be == -1):

                    _tv___pu__q_ -= 1
                    om_ul__i_av_ = u_k_gn_m_ma_

                elif __qj_n_qt_be < u_k_gn_m_ma_:

                    _tv___pu__q_ += 1
                    om_ul__i_av_ = __qj_n_qt_be

            y_____f_s___ = []

            u_n______vtv = 0

            for i in range(0, len(_i_i_u_y_up_) - 1, 2):

                ___x_____u_x = _i_i_u_y_up_[i]
                k_q__sg___d_ = _i_i_u_y_up_[i + 1]

                y_____f_s___.append(__pf_dc_vs__[u_n______vtv: ___x_____u_x])

                u_n______vtv = k_q__sg___d_

            y_____f_s___.append(__pf_dc_vs__[u_n______vtv: len(__pf_dc_vs__)])

            __pf_dc_vs__ = "".join(y_____f_s___)

            __pf_dc_vs__ = __pf_dc_vs__.replace("\\{", "{")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\}", "%x7D")
            __pf_dc_vs__ = __pf_dc_vs__.replace("}", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("%x7D", "}")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\\\", "\\")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\line", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\pard", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\par", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\tab", "\t")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\plain", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\fs20", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\f0", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\f4", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\f5", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\f6", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\objattph", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\li360", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\li720", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\li1440", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\li1080", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\fi-360", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\fi-720", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\rtlch", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\ltrch", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\sb100", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\intbl", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat1", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat2", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat3", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat4", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat5", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat6", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat7", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\cbpat8", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\sb90", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\sb150", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\sb240", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\sb280", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\qc", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\qr", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\ql", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\fs18", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\b0", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\b", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\protect", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\itap2", "")
            __pf_dc_vs__ = __pf_dc_vs__.replace("\\itap3", "")

            _zc__foo__x_ = 0

            while _zc__foo__x_ > -1:

                _zc__foo__x_ = __pf_dc_vs__.find("\\u", _zc__foo__x_)

                if _zc__foo__x_ > -1:

                    qk_y_v_ozw__ = __pf_dc_vs__.find("?", _zc__foo__x_)

                    if qk_y_v_ozw__ > _zc__foo__x_ and qk_y_v_ozw__ <= _zc__foo__x_ + 8:

                        __v_ch_p_d_w = __pf_dc_vs__[_zc__foo__x_: qk_y_v_ozw__ + 1]

                        _______a___h = __pf_dc_vs__[_zc__foo__x_ + 2: qk_y_v_ozw__]

                        try:
                            _l__ca______ = str(_______a___h)
                            __pf_dc_vs__ = __pf_dc_vs__.replace(__v_ch_p_d_w, _l__ca______)
                        except:
                            __pf_dc_vs__ = __pf_dc_vs__.replace(__v_ch_p_d_w, __v_ch_p_d_w[1:])
                    
                    else:
                        _zc__foo__x_ += 1
                
                else:
                    break
                

        return (__pf_dc_vs__, ___b_xq__ed_)

    @staticmethod
    def jpbj__v_jf__(_xx_ehv___l_):

        x___v___sfa_ = "{\\rtf1\\ansi\\mac\\deff0\\deftab720{\\fonttbl;}{\\f0\\fnil \\froman \\fswiss \\fmodern \\fscript \\fdecor MS Sans SerifSymbolArialTimes New RomanCourier{\\colortbl\\red0\\green0\\blue0\n\r\\par \\pard\\plain\\f0\\fs20\\b\\i\\u\\tab\\tx"

        ___n_r_yn___ = x___v___sfa_.encode("ascii")

        cws___znk__t = None
        __q_d__czf__ = 0
        __b_h_x___t_ = 0

        if _xx_ehv___l_ is None or len(_xx_ehv___l_) < 16:
            raise Exception("Invalid PR_RTF_COMPRESSION header")

        _s____k__b__ = Message.b_xr_fga_e_q(_xx_ehv___l_, __q_d__czf__)
        __q_d__czf__ += 4

        __xs_juoi___ = Message.b_xr_fga_e_q(_xx_ehv___l_, __q_d__czf__)
        __q_d__czf__ += 4

        m_x_h__os_lq = Message.b_xr_fga_e_q(_xx_ehv___l_, __q_d__czf__)
        __q_d__czf__ += 4

        _p___un__wyp = Message.b_xr_fga_e_q(_xx_ehv___l_, __q_d__czf__)
        __q_d__czf__ += 4

        if _s____k__b__ != len(_xx_ehv___l_) - 4:
            return bytes(0)

        if m_x_h__os_lq == 0x414c454d:

            if __xs_juoi___ > len(_xx_ehv___l_) - __q_d__czf__:
                __xs_juoi___ = len(_xx_ehv___l_) - __q_d__czf__

            cws___znk__t = _xx_ehv___l_[__q_d__czf__: __q_d__czf__ + __xs_juoi___]

        elif m_x_h__os_lq == 0x75465a4c: 
            cws___znk__t = bytearray(len(___n_r_yn___) + __xs_juoi___)
            cws___znk__t[0: len(___n_r_yn___)] = ___n_r_yn___
            __b_h_x___t_ = len(___n_r_yn___)

            _ir__c_v___v = 0
            v__nm___b__u = 0

            while __b_h_x___t_ < len(cws___znk__t):

                if _ir__c_v___v % 8 == 0:
                    v__nm___b__u = Message.bs_____m__n_(_xx_ehv___l_, __q_d__czf__)
                    __q_d__czf__ += 1
                else:
                    v__nm___b__u = v__nm___b__u >> 1
                
                _ir__c_v___v += 1

                if (v__nm___b__u & 1) == 1:

                    ____m_fe__fr = Message.bs_____m__n_(_xx_ehv___l_, __q_d__czf__)
                    __q_d__czf__ += 1
                    
                    _wa_sc___co_ = Message.bs_____m__n_(_xx_ehv___l_, __q_d__czf__)
                    __q_d__czf__ += 1

                    ____m_fe__fr = (____m_fe__fr << 4) | (_wa_sc___co_ >> 4)
                    _wa_sc___co_ = (_wa_sc___co_ & 0xF) + 2
                    ____m_fe__fr = int(__b_h_x___t_ / 4096) * 4096 + ____m_fe__fr

                    if ____m_fe__fr >= __b_h_x___t_:
                        ____m_fe__fr -= 4096

                    ___wkbztp_d_ = ____m_fe__fr + _wa_sc___co_

                    while ____m_fe__fr < ___wkbztp_d_:
                        
                        try:
                            cws___znk__t[__b_h_x___t_] = cws___znk__t[____m_fe__fr]
                            __b_h_x___t_ += 1
                            ____m_fe__fr += 1
                        except:
                            return bytes(0)
            
                else:
                    try:
                        cws___znk__t[__b_h_x___t_] = _xx_ehv___l_[__q_d__czf__]
                        __b_h_x___t_ += 1
                        __q_d__czf__ += 1
                    except:
                        return bytes(0)


            _xx_ehv___l_ = cws___znk__t
            cws___znk__t = _xx_ehv___l_[len(___n_r_yn___): len(___n_r_yn___) + __xs_juoi___]

        else:
            raise Exception("Wrong magic number.")


        return cws___znk__t

    @staticmethod
    def w__lr___t__u(zs___wa____d):

        p__pc__npa__ = {}

        t_a_gx__hk__ = zs___wa____d.find("{\\fonttbl")

        if t_a_gx__hk__ > 0:

            ___wkbztp_d_ = zs___wa____d.find("}}", t_a_gx__hk__)

            if ___wkbztp_d_ > 0:

                __uaqtyk_l_k = zs___wa____d[t_a_gx__hk__ + 8: ___wkbztp_d_ + 8]
                ____o____ms_ = __uaqtyk_l_k.splitlines()
                _t_gc__s_x_w = ""

                for i in range(len(____o____ms_)):

                    _t_gc__s_x_w = ____o____ms_[i]
                    _i__yas_h_nu = _t_gc__s_x_w.find("{")

                    if _i__yas_h_nu > -1:

                        sr_y____f__t = _t_gc__s_x_w.find("}", _i__yas_h_nu)

                        if sr_y____f__t > -1:

                            _t_gc__s_x_w = _t_gc__s_x_w[_i__yas_h_nu + 1: sr_y____f__t]

                            __nyufbk____ = "".join(_t_gc__s_x_w.split()).split('\\')

                            if len(__nyufbk____) > 1 and __nyufbk____[1].startswith("f"):

                                d_______kp__ = __nyufbk____[1]
                                ___vxk_v_b__ = None

                                for i in range(2, len(__nyufbk____), 1):

                                    if __nyufbk____[i] == "fcharset128":
                                        ___vxk_v_b__ = 'shift_jis'
                                    elif __nyufbk____[i] == "fcharset129":
                                        ___vxk_v_b__ = 'cp949'
                                    elif __nyufbk____[i] == "fcharset134":
                                        ___vxk_v_b__ = 'gb2312'
                                    elif __nyufbk____[i] == "fcharset136":
                                        ___vxk_v_b__ = 'big5'
                                    elif __nyufbk____[i] == "fcharset161":
                                        ___vxk_v_b__ = 'cp1253'
                                    elif __nyufbk____[i] == "fcharset162":
                                        ___vxk_v_b__ = 'cp1254'
                                    elif __nyufbk____[i] == "fcharset163":
                                        ___vxk_v_b__ = 'cp1258'
                                    elif __nyufbk____[i] == "fcharset177":
                                        ___vxk_v_b__ = 'cp1255'
                                    elif __nyufbk____[i] == "fcharset178":
                                        ___vxk_v_b__ = 'cp1256'
                                    elif __nyufbk____[i] == "fcharset186":
                                        ___vxk_v_b__ = 'cp1257'
                                    elif __nyufbk____[i] == "fcharset204":
                                        ___vxk_v_b__ = 'cp1251'
                                    elif __nyufbk____[i] == "fcharset222":
                                        ___vxk_v_b__ = 'cp874'
                                    elif __nyufbk____[i] == "fcharset238":
                                        ___vxk_v_b__ = 'cp1250'

                                if d_______kp__ not in p__pc__npa__:
                                    p__pc__npa__[d_______kp__] = ___vxk_v_b__


        return p__pc__npa__

    @staticmethod
    def x_j__na__gbt(__d_v___a_yf, y_qm____k_zb):

        if len(__d_v___a_yf) == 0:
            return -1

        jgz__ma_____ = False

        for i in range(len(__d_v___a_yf)):

            ____u_e_iy_l = __d_v___a_yf[i]

            if y_qm____k_zb.name is not None and ____u_e_iy_l.name == y_qm____k_zb.name:
                jgz__ma_____ = True
            elif ____u_e_iy_l.id == y_qm____k_zb.id and y_qm____k_zb.type == NamedPropertyType.NUMERICAL:
                jgz__ma_____ = True

            if jgz__ma_____:

                abva_____x_x = True

                if ____u_e_iy_l.guid is not None and y_qm____k_zb.guid is not None and len(____u_e_iy_l.guid) == len(y_qm____k_zb.guid):

                    for j in range(len(____u_e_iy_l.guid)):

                        if ____u_e_iy_l.guid[j] != y_qm____k_zb.guid[j]:
                            abva_____x_x = False

                else:
                    abva_____x_x = False

                if abva_____x_x:
                    return i

        return -1

    @staticmethod
    def jgpr_zs_vz__(value, type, encoding):

        if value is None and (type == PropertyType.STRING or type == PropertyType.STRING_8):
            return 1
        elif value is not None and (type == PropertyType.STRING or type == PropertyType.STRING_8):
            return len(value) + len("\0".encode(encoding))
        elif value is None:
            return 0
        else:
            return len(value)

    @staticmethod
    def __g__j__gx__(p_k___db_qt_, h_u_wgs____i):

        if p_k___db_qt_ is not None:

            for l in range(len(h_u_wgs____i)):

                _____e____b_ = h_u_wgs____i[l]
                _s__i_bnx__e = True

                for i in range(16):
                
                    if p_k___db_qt_[i] != _____e____b_[i]:
                        _s__i_bnx__e = False
                        break

                if _s__i_bnx__e:
                    return l

        return -1  

    @staticmethod
    def jozp_k____zx(type):

        if type == PropertyType.INTEGER_16:    
            return 0x0002    
        elif type == PropertyType.INTEGER_32:    
            return 0x0003    
        elif type == PropertyType.FLOATING_32:    
            return 0x0004    
        elif type == PropertyType.FLOATING_64:    
            return 0x0005    
        elif type == PropertyType.CURRENCY:    
            return 0x0006    
        elif type == PropertyType.FLOATING_TIME:    
            return 0x0007    
        elif type == PropertyType.BOOLEAN:    
            return 0x000B    
        elif type == PropertyType.OBJECT:    
            return 0x000D    
        elif type == PropertyType.INTEGER_64:    
            return 0x0014    
        elif type == PropertyType.STRING_8:    
            return 0x001E    
        elif type == PropertyType.STRING:    
            return 0x001F
        elif type == PropertyType.TIME:    
            return 0x0040    
        elif type == PropertyType.GUID:    
            return 0x0048    
        elif type == PropertyType.BINARY:    
            return 0x0102    
        elif type == PropertyType.MULTIPLE_INTEGER_16:    
            return 0x1002    
        elif type == PropertyType.MULTIPLE_INTEGER_32:    
            return 0x1003    
        elif type == PropertyType.MULTIPLE_FLOATING_32:    
            return 0x1004    
        elif type == PropertyType.MULTIPLE_FLOATING_64:    
            return 0x1005    
        elif type == PropertyType.MULTIPLE_CURRENCY:    
            return 0x1006    
        elif type == PropertyType.MULTIPLE_FLOATING_TIME:    
            return 0x1007    
        elif type == PropertyType.MULTIPLE_INTEGER_64:    
            return 0x1014    
        elif type == PropertyType.MULTIPLE_STRING_8:    
            return 0x101E    
        elif type == PropertyType.MULTIPLE_STRING:    
            return 0x101F    
        elif type == PropertyType.MULTIPLE_TIME:    
            return 0x1040    
        elif type == PropertyType.MULTIPLE_GUID:    
            return 0x1048    
        elif type == PropertyType.MULTIPLE_BINARY:    
            return 0x1102    
        else:  
            return 0x001E                

    @staticmethod
    def qb_s_dghkmbh(code_page):

        if code_page == 37:
            return 'cp037'
        elif code_page == 437:
            return 'cp437'
        elif code_page == 500:
            return 'cp500'
        elif code_page == 775:
            return 'cp775'
        elif code_page == 850:
            return 'cp850'
        elif code_page == 852:
            return 'cp852'
        elif code_page == 855:
            return 'cp855'
        elif code_page == 856:
            return 'cp856'
        elif code_page == 857:
            return 'cp857'
        elif code_page == 858:
            return 'cp858'
        elif code_page == 860:
            return 'cp860'
        elif code_page == 861:
            return 'cp861'
        elif code_page == 862:
            return 'cp862'
        elif code_page == 863:
            return 'cp863'
        elif code_page == 864:
            return 'cp864'
        elif code_page == 865:
            return 'cp865'
        elif code_page == 866:
            return 'cp866'
        elif code_page == 869:
            return 'cp869'
        elif code_page == 870:
            return 'IBM870'
        elif code_page == 874:
            return 'cp874'
        elif code_page == 875:
            return 'cp875'
        elif code_page == 932:
            return 'shift_jis'
        elif code_page == 936:
            return 'gb2312'
        elif code_page == 950:
            return 'big5'
        elif code_page == 1250:
            return 'cp437'
        elif code_page == 1251:
            return 'cp1251'
        elif code_page == 1252:
            return 'cp1252'
        elif code_page == 1253:
            return 'cp1253'
        elif code_page == 1254:
            return 'cp1254'
        elif code_page == 1255:
            return 'cp1255'
        elif code_page == 1256:
            return 'cp1256'
        elif code_page == 1257:
            return 'cp1257'
        elif code_page == 1258:
            return 'cp1258'
        elif code_page == 20866:
            return 'koi8_r'
        elif code_page == 20932:
            return 'euc_jp'
        elif code_page == 28591:
            return 'latin_1'
        elif code_page == 28592:
            return 'iso8859_2'
        elif code_page == 28593:
            return 'iso8859_3'
        elif code_page == 28594:
            return 'iso8859_4'
        elif code_page == 28595:
            return 'iso8859_5'
        elif code_page == 28596:
            return 'iso8859_6'
        elif code_page == 28597:
            return 'iso8859_7'
        elif code_page == 28598:
            return 'iso8859_8'
        elif code_page == 28599:
            return 'iso8859_9'
        elif code_page == 28603:
            return 'iso8859_13'
        elif code_page == 28605:
            return 'iso8859_15'
        elif code_page == 50220:
            return 'iso2022_jp'
        elif code_page == 50221:
            return 'iso2022_jp_1'
        elif code_page == 50222:
            return 'iso2022_jp_2'
        elif code_page == 50225:
            return 'iso2022_kr'
        else:
            return 'utf_8'

    @staticmethod    
    def _j__y____u__(utc_datetime):
        offset = datetime.datetime.fromtimestamp(utc_datetime.timestamp()) - datetime.datetime.utcfromtimestamp(utc_datetime.timestamp())
        return utc_datetime + offset   

    @staticmethod
    def pc____k_j___(value):
        return (value & 0x8000) | (value & 0x7fff)

    @staticmethod
    def bs_____m__n_(buf, offset):
        return buf[offset] & 0xFF

    @staticmethod
    def k______s__i_(b1, b2):
        return ((b1 & 0xFF) | ((b2 & 0xFF) << 8)) & 0xFFFF

    @staticmethod
    def b_xr_fga_e_q(buf, offset):
        return ((buf[offset] & 0xFF) | ((buf[offset + 1] & 0xFF) << 8) | ((buf[offset + 2] & 0xFF) << 16) | ((buf[offset + 3] & 0xFF) << 24)) & 0x00000000FFFFFFFF

    def to_bytes(self):
        return self.p_zygsk___y_()

    def to_bytes(self):
        return self.kon_r_h___t_()

    def save(self, file_path):

        if(file_path is not None):
            file = open(file_path, "wb")
            file.write(self.to_bytes())
            file.close

    @property
    def body_rtf(self):

        if self.i_f__lcbcp__ is not None and len(self.i_f__lcbcp__) > 0:
            return Message.jpbj__v_jf__(self.i_f__lcbcp__)
        else:
            return None

    @body_rtf.setter
    def body_rtf(self, value):
        
        if value is not None:

            eynjn_yv_lq_ = bytearray()
           
            eynjn_yv_lq_ += int.to_bytes(len(value) + 12, 4, "little")
            eynjn_yv_lq_ += int.to_bytes(len(value), 4, "little")
            eynjn_yv_lq_ += int.to_bytes(0x414c454d, 4, "little")

            hputte_____p = Crc()
            hputte_____p.update(value)

            eynjn_yv_lq_ += int.to_bytes(hputte_____p.value, 4, "little")
            eynjn_yv_lq_ += value

            self.i_f__lcbcp__ = bytes(eynjn_yv_lq_)
            self._h_____pvsgq = True

    @property
    def body_html(self):

        if self.j_ka_nrf____ is None and self.i_f__lcbcp__ is not None and len(self.i_f__lcbcp__) > 0:

            e___i_b__od_ = Message.jpbj__v_jf__(self.i_f__lcbcp__)
            
            __pf_dc_vs__, ___b_xq__ed_ = Message.____z___gnkj(e___i_b__od_)

            if __pf_dc_vs__ is not None:
                return __pf_dc_vs__.encode("utf_8")
            else:
                return None

        else:
            return self.j_ka_nrf____

    @body_html.setter
    def body_html(self, value):
        self.j_ka_nrf____ = value

    @property
    def body_html_text(self):

        if self.j_ka_nrf____ is not None:
            
            if self.b_s_cu_d_ovr > 0:

                ___k__yc_v_n = Message.qb_s_dghkmbh(self.b_s_cu_d_ovr)

                _g___xd__irl = self.j_ka_nrf____.decode(___k__yc_v_n)

                return _g___xd__irl

            else:

                _g___xd__irl = self.j_ka_nrf____.decode("utf_8")

                return _g___xd__irl

        else:

            tf_iwe_p_ltd = self.body_rtf

            if tf_iwe_p_ltd is not None and len(tf_iwe_p_ltd) > 0:

                __pf_dc_vs__, ___b_xq__ed_ = Message.____z___gnkj(tf_iwe_p_ltd)

                if __pf_dc_vs__ is not None:
                    return __pf_dc_vs__.encode("utf_8")
                else:
                    return None  

            return None

    @body_html_text.setter
    def body_html_text(self, value):

        if value is not None:
            self.j_ka_nrf____ = value.encode("utf_8")

    @property
    def property_table(self):
        return self.u___cz_sn___

    @property_table.setter
    def property_table(self, value):
        self.u___cz_sn___ = value

    @property
    def message_class(self):
        return self.___t_lgsh__n

    @message_class.setter
    def message_class(self, value):
        self.___t_lgsh__n = value

    @property
    def subject(self):
        return self.b_t___b_q_xu

    @subject.setter
    def subject(self, value):
        self.b_t___b_q_xu = value

    @property
    def subject_prefix(self):
        return self._______c__ty

    @subject_prefix.setter
    def subject_prefix(self, value):
        self._______c__ty = value

    @property
    def conversation_topic(self):
        return self._s_k_n_jb___

    @conversation_topic.setter
    def conversation_topic(self, value):
        self._s_k_n_jb___ = value

    @property
    def display_bcc(self):
        return self.w__teeli____

    @display_bcc.setter
    def display_bcc(self, value):
        self.w__teeli____ = value

    @property
    def display_cc(self):
        return self.qj_wgu_zzu_s

    @display_cc.setter
    def display_cc(self, value):
        self.qj_wgu_zzu_s = value

    @property
    def display_to(self):
        return self.qw_____z__u_

    @display_to.setter
    def display_to(self, value):
        self.qw_____z__u_ = value

    @property
    def original_display_to(self):
        return self.p____t__w_g_

    @original_display_to.setter
    def original_display_to(self, value):
        self.p____t__w_g_ = value

    @property
    def reply_to(self):
        return self.cx_p_u___h_i

    @reply_to.setter
    def reply_to(self, value):
        self.cx_p_u___h_i = value

    @property
    def normalized_subject(self):
        return self.j__kfc___d_g

    @normalized_subject.setter
    def normalized_subject(self, value):
        self.j__kfc___d_g = value

    @property
    def body(self):
        return self.p__w___rx_bo

    @body.setter
    def body(self, value):
        self.p__w___rx_bo = value

    @property
    def rtf_compressed(self):
        return self.i_f__lcbcp__

    @rtf_compressed.setter
    def rtf_compressed(self, value):
        self.i_f__lcbcp__ = value

    @property
    def search_key(self):
        return self.kh_____k_y_g

    @search_key.setter
    def search_key(self, value):
        self.kh_____k_y_g = value

    @property
    def change_key(self):
        return self.__zr_cn_k__x

    @change_key.setter
    def change_key(self, value):
        self.__zr_cn_k__x = value

    @property
    def entry_id(self):
        return self._fz___ad_f__

    @entry_id.setter
    def entry_id(self, value):
        self._fz___ad_f__ = value

    @property
    def read_receipt_entry_id(self):
        return self.a_uk__ilatjb

    @read_receipt_entry_id.setter
    def read_receipt_entry_id(self, value):
        self.a_uk__ilatjb = value

    @property
    def read_receipt_search_key(self):
        return self.____gw__e_a_

    @read_receipt_search_key.setter
    def read_receipt_search_key(self, value):
        self.____gw__e_a_ = value

    @property
    def creation_time(self):
        return self.__z_j__au_m_

    @creation_time.setter
    def creation_time(self, value):
        self.__z_j__au_m_ = value

    @property
    def last_modification_time(self):
        return self.i_zt_m_sm__i

    @last_modification_time.setter
    def last_modification_time(self, value):
        self.i_zt_m_sm__i = value

    @property
    def message_delivery_time(self):
        return self.___ud_______

    @message_delivery_time.setter
    def message_delivery_time(self, value):
        self.___ud_______ = value

    @property
    def client_submit_time(self):
        return self._w______i_dp

    @client_submit_time.setter
    def client_submit_time(self, value):
        self._w______i_dp = value

    @property
    def deferred_delivery_time(self):
        return self._e__gxx__h_u

    @deferred_delivery_time.setter
    def deferred_delivery_time(self, value):
        self._e__gxx__h_u = value

    @property
    def provider_submit_time(self):
        return self.__g__h_iwita

    @provider_submit_time.setter
    def provider_submit_time(self, value):
        self.__g__h_iwita = value

    @property
    def report_time(self):
        return self.y_ze__l___u_

    @report_time.setter
    def report_time(self, value):
        self.y_ze__l___u_ = value

    @property
    def report_text(self):
        return self.__okvntl__d_

    @report_text.setter
    def report_text(self, value):
        self.__okvntl__d_ = value

    @property
    def creator_name(self):
        return self.____l__er___

    @creator_name.setter
    def creator_name(self, value):
        self.____l__er___ = value

    @property
    def last_modifier_name(self):
        return self.wo___yi_w__x

    @last_modifier_name.setter
    def last_modifier_name(self, value):
        self.wo___yi_w__x = value

    @property
    def internet_message_id(self):
        return self._so__s_lu_o_

    @internet_message_id.setter
    def internet_message_id(self, value):
        self._so__s_lu_o_ = value

    @property
    def in_reply_to(self):
        return self.j_a_______a_

    @in_reply_to.setter
    def in_reply_to(self, value):
        self.j_a_______a_ = value

    @property
    def internet_references(self):
        return self._r_h__rjorsu

    @internet_references.setter
    def internet_references(self, value):
        self._r_h__rjorsu = value

    @property
    def message_code_page(self):
        return self._f__a___jm_p

    @message_code_page.setter
    def message_code_page(self, value):
        self._f__a___jm_p = value

    @property
    def icon_index(self):
        return self.__y__kwxb___

    @icon_index.setter
    def icon_index(self, value):
        self.__y__kwxb___ = value

    @property
    def message_size(self):
        return self.c_dv__cjvvx_

    @message_size.setter
    def message_size(self, value):
        self.c_dv__cjvvx_ = value

    @property
    def internet_code_page(self):
        return self.b_s_cu_d_ovr

    @internet_code_page.setter
    def internet_code_page(self, value):
        self.b_s_cu_d_ovr = value

    @property
    def conversation_index(self):
        return self.wto_g_dk_qpf

    @conversation_index.setter
    def conversation_index(self, value):
        self.wto_g_dk_qpf = value

    @property
    def is_hidden(self):
        return self.____zm_r_ip_

    @is_hidden.setter
    def is_hidden(self, value):
        self.____zm_r_ip_ = value

    @property
    def is_read_only(self):
        return self.__m__df_ka_l

    @is_read_only.setter
    def is_read_only(self, value):
        self.__m__df_ka_l = value

    @property
    def is_system(self):
        return self.veb_bv_____o

    @is_system.setter
    def is_system(self, value):
        self.veb_bv_____o = value

    @property
    def disable_full_fidelity(self):
        return self.i___d_zbbg__

    @disable_full_fidelity.setter
    def disable_full_fidelity(self, value):
        self.i___d_zbbg__ = value

    @property
    def has_attachment(self):
        return self.r__gl__wj_yq

    @has_attachment.setter
    def has_attachment(self, value):
        self.r__gl__wj_yq = value

    @property
    def rtf_in_sync(self):
        return self._h_____pvsgq

    @rtf_in_sync.setter
    def rtf_in_sync(self, value):
        self._h_____pvsgq = value

    @property
    def read_receipt_requested(self):
        return self._qvy_dii__st

    @read_receipt_requested.setter
    def read_receipt_requested(self, value):
        self._qvy_dii__st = value

    @property
    def delivery_report_requested(self):
        return self.________k___

    @delivery_report_requested.setter
    def delivery_report_requested(self, value):
        self.________k___ = value

    @property
    def sensitivity(self):
        return self._g_h__sre__k

    @sensitivity.setter
    def sensitivity(self, value):
        self._g_h__sre__k = value

    @property
    def importance(self):
        return self.___ot__i_wup

    @importance.setter
    def importance(self, value):
        self.___ot__i_wup = value

    @property
    def priority(self):
        return self._ff___oikg_n

    @priority.setter
    def priority(self, value):
        self._ff___oikg_n = value

    @property
    def flag_icon(self):
        return self._dhn__eqsl_x

    @flag_icon.setter
    def flag_icon(self, value):
        self._dhn__eqsl_x = value

    @property
    def flag_status(self):
        return self.j_e_m__r_qgm

    @flag_status.setter
    def flag_status(self, value):
        self.j_e_m__r_qgm = value

    @property
    def object_type(self):
        return self.uubu___mqh__

    @object_type.setter
    def object_type(self, value):
        self.uubu___mqh__ = value

    @property
    def received_representing_address_type(self):
        return self._dn_pem__l__

    @received_representing_address_type.setter
    def received_representing_address_type(self, value):
        self._dn_pem__l__ = value

    @property
    def received_representing_email_address(self):
        return self.li_leu_wgzg_

    @received_representing_email_address.setter
    def received_representing_email_address(self, value):
        self.li_leu_wgzg_ = value

    @property
    def received_representing_entry_id(self):
        return self._vezy_n_ikln

    @received_representing_entry_id.setter
    def received_representing_entry_id(self, value):
        self._vezy_n_ikln = value

    @property
    def received_representing_name(self):
        return self.q__q_k_r_cw_

    @received_representing_name.setter
    def received_representing_name(self, value):
        self.q__q_k_r_cw_ = value

    @property
    def received_representing_search_key(self):
        return self.i_r___noho_c

    @received_representing_search_key.setter
    def received_representing_search_key(self, value):
        self.i_r___noho_c = value

    @property
    def received_by_address_type(self):
        return self._ze__u_auq__

    @received_by_address_type.setter
    def received_by_address_type(self, value):
        self._ze__u_auq__ = value

    @property
    def received_by_email_address(self):
        return self.g__nj___m__u

    @received_by_email_address.setter
    def received_by_email_address(self, value):
        self.g__nj___m__u = value

    @property
    def received_by_entry_id(self):
        return self.k_l_bco_s_jv

    @received_by_entry_id.setter
    def received_by_entry_id(self, value):
        self.k_l_bco_s_jv = value

    @property
    def received_by_name(self):
        return self.__xh_ve_____

    @received_by_name.setter
    def received_by_name(self, value):
        self.__xh_ve_____ = value

    @property
    def received_by_search_key(self):
        return self.____uw__pp__

    @received_by_search_key.setter
    def received_by_search_key(self, value):
        self.____uw__pp__ = value

    @property
    def sender_address_type(self):
        return self.___onygff_yd

    @sender_address_type.setter
    def sender_address_type(self, value):
        self.___onygff_yd = value

    @property
    def sender_email_address(self):
        return self._p_y__of_ma_

    @sender_email_address.setter
    def sender_email_address(self, value):
        self._p_y__of_ma_ = value

    @property
    def sender_smtp_address(self):
        return self.p_k_wh_____c

    @sender_smtp_address.setter
    def sender_smtp_address(self, value):
        self.p_k_wh_____c = value

    @property
    def sender_entry_id(self):
        return self.___yu____xb_

    @sender_entry_id.setter
    def sender_entry_id(self, value):
        self.___yu____xb_ = value

    @property
    def sender_name(self):
        return self.___xm__ne_t_

    @sender_name.setter
    def sender_name(self, value):
        self.___xm__ne_t_ = value

    @property
    def sender_search_key(self):
        return self.___s_iffiu__

    @sender_search_key.setter
    def sender_search_key(self, value):
        self.___s_iffiu__ = value

    @property
    def sent_representing_address_type(self):
        return self.__w_y_scz_u_

    @sent_representing_address_type.setter
    def sent_representing_address_type(self, value):
        self.__w_y_scz_u_ = value

    @property
    def sent_representing_email_address(self):
        return self.______z_____

    @sent_representing_email_address.setter
    def sent_representing_email_address(self, value):
        self.______z_____ = value

    @property
    def sent_representing_smtp_address(self):
        return self.y______e___l

    @sent_representing_smtp_address.setter
    def sent_representing_smtp_address(self, value):
        self.y______e___l = value

    @property
    def sent_representing_entry_id(self):
        return self.dqgxw_hnt__k

    @sent_representing_entry_id.setter
    def sent_representing_entry_id(self, value):
        self.dqgxw_hnt__k = value

    @property
    def sent_representing_name(self):
        return self._o_wcivl____

    @sent_representing_name.setter
    def sent_representing_name(self, value):
        self._o_wcivl____ = value

    @property
    def sent_representing_search_key(self):
        return self.__dq___iif_g

    @sent_representing_search_key.setter
    def sent_representing_search_key(self, value):
        self.__dq___iif_g = value

    @property
    def transport_message_headers(self):
        return self.___i___cdtv_

    @transport_message_headers.setter
    def transport_message_headers(self, value):
        self.___i___cdtv_ = value

    @property
    def last_verb_execution_time(self):
        return self.s_jwv_w__ng_

    @last_verb_execution_time.setter
    def last_verb_execution_time(self, value):
        self.s_jwv_w__ng_ = value

    @property
    def last_verb_executed(self):
        return self.i__n____fy__

    @last_verb_executed.setter
    def last_verb_executed(self, value):
        self.i__n____fy__ = value

    @property
    def message_flags(self):
        return self.r_w_jc__qzn_

    @message_flags.setter
    def message_flags(self, value):
        self.r_w_jc__qzn_ = value

    @property
    def store_support_masks(self):
        return self.s__f__m_okw_

    @store_support_masks.setter
    def store_support_masks(self, value):
        self.s__f__m_okw_ = value

    @property
    def outlook_version(self):
        return self.___r_____tvp

    @outlook_version.setter
    def outlook_version(self, value):
        self.___r_____tvp = value

    @property
    def outlook_internal_version(self):
        return self._hv_i__xj___

    @outlook_internal_version.setter
    def outlook_internal_version(self, value):
        self._hv_i__xj___ = value

    @property
    def common_start_time(self):
        return self.cr_xv___r_qv

    @common_start_time.setter
    def common_start_time(self, value):
        self.cr_xv___r_qv = value

    @property
    def common_end_time(self):
        return self.egv____dws__

    @common_end_time.setter
    def common_end_time(self, value):
        self.egv____dws__ = value

    @property
    def flag_due_by(self):
        return self._i_n________

    @flag_due_by.setter
    def flag_due_by(self, value):
        self._i_n________ = value

    @property
    def is_recurring(self):
        return self.s__a_____uwe

    @is_recurring.setter
    def is_recurring(self, value):
        self.s__a_____uwe = value

    @property
    def reminder_time(self):
        return self._fusob_vbnex

    @reminder_time.setter
    def reminder_time(self, value):
        self._fusob_vbnex = value

    @property
    def reminder_minutes_before_start(self):
        return self._k__nlldizui

    @reminder_minutes_before_start.setter
    def reminder_minutes_before_start(self, value):
        self._k__nlldizui = value

    @property
    def companies(self):
        return self.k__q__s__kb_

    @companies.setter
    def companies(self, value):
        self.k__q__s__kb_ = value

    @property
    def contact_names(self):
        return self._ycq__y_lj__

    @contact_names.setter
    def contact_names(self, value):
        self._ycq__y_lj__ = value

    @property
    def keywords(self):
        return self.v__c___fhx_s

    @keywords.setter
    def keywords(self, value):
        self.v__c___fhx_s = value

    @property
    def billing_information(self):
        return self.__c_kkkbm_zh

    @billing_information.setter
    def billing_information(self, value):
        self.__c_kkkbm_zh = value

    @property
    def mileage(self):
        return self._______ii___

    @mileage.setter
    def mileage(self, value):
        self._______ii___ = value

    @property
    def reminder_sound_file(self):
        return self.z___xyhng_ev

    @reminder_sound_file.setter
    def reminder_sound_file(self, value):
        self.z___xyhng_ev = value

    @property
    def is_private(self):
        return self.__pmh__t___j

    @is_private.setter
    def is_private(self, value):
        self.__pmh__t___j = value

    @property
    def is_reminder_set(self):
        return self.il__q_yhe___

    @is_reminder_set.setter
    def is_reminder_set(self, value):
        self.il__q_yhe___ = value

    @property
    def reminder_override_default(self):
        return self._y__h_t_h___

    @reminder_override_default.setter
    def reminder_override_default(self, value):
        self._y__h_t_h___ = value

    @property
    def reminder_play_sound(self):
        return self.q___st__n__j

    @reminder_play_sound.setter
    def reminder_play_sound(self, value):
        self.q___st__n__j = value

    @property
    def internet_account_name(self):
        return self.__wn_______l

    @internet_account_name.setter
    def internet_account_name(self, value):
        self.__wn_______l = value

    @property
    def appointment_start_time(self):
        return self._l__p__mwm_q

    @appointment_start_time.setter
    def appointment_start_time(self, value):
        self._l__p__mwm_q = value

    @property
    def appointment_end_time(self):
        return self.__ma_m___ciq

    @appointment_end_time.setter
    def appointment_end_time(self, value):
        self.__ma_m___ciq = value

    @property
    def is_all_day_event(self):
        return self.sw__fy_____w

    @is_all_day_event.setter
    def is_all_day_event(self, value):
        self.sw__fy_____w = value

    @property
    def location(self):
        return self._____q__c_v_

    @location.setter
    def location(self, value):
        self._____q__c_v_ = value

    @property
    def busy_status(self):
        return self.__q__v_af___

    @busy_status.setter
    def busy_status(self, value):
        self.__q__v_af___ = value

    @property
    def meeting_status(self):
        return self.w_h_gqfnzf_i

    @meeting_status.setter
    def meeting_status(self, value):
        self.w_h_gqfnzf_i = value

    @property
    def response_status(self):
        return self.neh_l__xlj__

    @response_status.setter
    def response_status(self, value):
        self.neh_l__xlj__ = value

    @property
    def recurrence_type(self):
        return self.umc_fo_____x

    @recurrence_type.setter
    def recurrence_type(self, value):
        self.umc_fo_____x = value

    @property
    def appointment_message_class(self):
        return self.___d_l___xct

    @appointment_message_class.setter
    def appointment_message_class(self, value):
        self.___d_l___xct = value

    @property
    def time_zone(self):
        return self.____uf_h_uu_

    @time_zone.setter
    def time_zone(self, value):
        self.____uf_h_uu_ = value

    @property
    def recurrence_pattern_description(self):
        return self.m__zc_il___y

    @recurrence_pattern_description.setter
    def recurrence_pattern_description(self, value):
        self.m__zc_il___y = value

    @property
    def recurrence_pattern(self):
        return self.r___af_zj_r_

    @recurrence_pattern.setter
    def recurrence_pattern(self, value):
        self.r___af_zj_r_ = value

    @property
    def guid(self):
        return self.____y___frl_

    @guid.setter
    def guid(self, value):
        self.____y___frl_ = value

    @property
    def label(self):
        return self._g___ehew___

    @label.setter
    def label(self, value):
        self._g___ehew___ = value

    @property
    def duration(self):
        return self.cy__hhh_jv__

    @duration.setter
    def duration(self, value):
        self.cy__hhh_jv__ = value

    @property
    def task_start_date(self):
        return self.q________c_r

    @task_start_date.setter
    def task_start_date(self, value):
        self.q________c_r = value

    @property
    def task_due_date(self):
        return self.x___asp___iv

    @task_due_date.setter
    def task_due_date(self, value):
        self.x___asp___iv = value

    @property
    def owner(self):
        return self.__wxx__pych_

    @owner.setter
    def owner(self, value):
        self.__wxx__pych_ = value

    @property
    def delegator(self):
        return self.rpu_b_xx__u_

    @delegator.setter
    def delegator(self, value):
        self.rpu_b_xx__u_ = value

    @property
    def percent_complete(self):
        return self.____narlie_r

    @percent_complete.setter
    def percent_complete(self, value):
        self.____narlie_r = value

    @property
    def actual_work(self):
        return self._m__f_j__e_i

    @actual_work.setter
    def actual_work(self, value):
        self._m__f_j__e_i = value

    @property
    def total_work(self):
        return self.____v_y_n___

    @total_work.setter
    def total_work(self, value):
        self.____v_y_n___ = value

    @property
    def is_team_task(self):
        return self.__hk___s__ux

    @is_team_task.setter
    def is_team_task(self, value):
        self.__hk___s__ux = value

    @property
    def is_complete(self):
        return self._n_ad___dz__

    @is_complete.setter
    def is_complete(self, value):
        self._n_ad___dz__ = value

    @property
    def date_completed(self):
        return self._gfko_gic___

    @date_completed.setter
    def date_completed(self, value):
        self._gfko_gic___ = value

    @property
    def task_status(self):
        return self.__t___l__g__

    @task_status.setter
    def task_status(self, value):
        self.__t___l__g__ = value

    @property
    def task_ownership(self):
        return self.___pp__l____

    @task_ownership.setter
    def task_ownership(self, value):
        self.___pp__l____ = value

    @property
    def task_delegation_state(self):
        return self._____xn_oymn

    @task_delegation_state.setter
    def task_delegation_state(self, value):
        self._____xn_oymn = value

    @property
    def note_width(self):
        return self._____f_t_h__

    @note_width.setter
    def note_width(self, value):
        self._____f_t_h__ = value

    @property
    def note_height(self):
        return self.___e_p_s___a

    @note_height.setter
    def note_height(self, value):
        self.___e_p_s___a = value

    @property
    def note_left(self):
        return self._mxah_ge__t_

    @note_left.setter
    def note_left(self, value):
        self._mxah_ge__t_ = value

    @property
    def note_top(self):
        return self.m_rdx____o__

    @note_top.setter
    def note_top(self, value):
        self.m_rdx____o__ = value

    @property
    def note_color(self):
        return self.__zuaq___k_g

    @note_color.setter
    def note_color(self, value):
        self.__zuaq___k_g = value

    @property
    def journal_start_time(self):
        return self.c_p_irtpd___

    @journal_start_time.setter
    def journal_start_time(self, value):
        self.c_p_irtpd___ = value

    @property
    def journal_end_time(self):
        return self.fyg_hq__zqla

    @journal_end_time.setter
    def journal_end_time(self, value):
        self.fyg_hq__zqla = value

    @property
    def journal_type(self):
        return self._n___mr_t_pn

    @journal_type.setter
    def journal_type(self, value):
        self._n___mr_t_pn = value

    @property
    def journal_type_description(self):
        return self.cbw_______xx

    @journal_type_description.setter
    def journal_type_description(self, value):
        self.cbw_______xx = value

    @property
    def journal_duration(self):
        return self.w__c_rjwf_j_

    @journal_duration.setter
    def journal_duration(self, value):
        self.w__c_rjwf_j_ = value

    @property
    def birthday(self):
        return self.f___v_bof__x

    @birthday.setter
    def birthday(self, value):
        self.f___v_bof__x = value

    @property
    def children_names(self):
        return self.__c__cw_h__a

    @children_names.setter
    def children_names(self, value):
        self.__c__cw_h__a = value

    @property
    def assistent_name(self):
        return self.__e__w_t_p_q

    @assistent_name.setter
    def assistent_name(self, value):
        self.__e__w_t_p_q = value

    @property
    def assistent_phone(self):
        return self._f_ha_w___mw

    @assistent_phone.setter
    def assistent_phone(self, value):
        self._f_ha_w___mw = value

    @property
    def business_phone(self):
        return self.vj_b__f__u__

    @business_phone.setter
    def business_phone(self, value):
        self.vj_b__f__u__ = value

    @property
    def business_phone2(self):
        return self.hy_wucpf_c_j

    @business_phone2.setter
    def business_phone2(self, value):
        self.hy_wucpf_c_j = value

    @property
    def business_fax(self):
        return self._km___gfyym_

    @business_fax.setter
    def business_fax(self, value):
        self._km___gfyym_ = value

    @property
    def business_home_page(self):
        return self.hhk__zyd_d__

    @business_home_page.setter
    def business_home_page(self, value):
        self.hhk__zyd_d__ = value

    @property
    def callback_phone(self):
        return self.bun___q__o__

    @callback_phone.setter
    def callback_phone(self, value):
        self.bun___q__o__ = value

    @property
    def car_phone(self):
        return self.___zpfq_tz__

    @car_phone.setter
    def car_phone(self, value):
        self.___zpfq_tz__ = value

    @property
    def cellular_phone(self):
        return self.__x_r_e_yh__

    @cellular_phone.setter
    def cellular_phone(self, value):
        self.__x_r_e_yh__ = value

    @property
    def company_main_phone(self):
        return self.q_ob_____ij_

    @company_main_phone.setter
    def company_main_phone(self, value):
        self.q_ob_____ij_ = value

    @property
    def company_name(self):
        return self.__f_fqzb___i

    @company_name.setter
    def company_name(self, value):
        self.__f_fqzb___i = value

    @property
    def computer_network_name(self):
        return self.y_b_h___p___

    @computer_network_name.setter
    def computer_network_name(self, value):
        self.y_b_h___p___ = value

    @property
    def customer_id(self):
        return self.n____j____xe

    @customer_id.setter
    def customer_id(self, value):
        self.n____j____xe = value

    @property
    def department_name(self):
        return self.___yr__bvg__

    @department_name.setter
    def department_name(self, value):
        self.___yr__bvg__ = value

    @property
    def display_name(self):
        return self.__jjr_pc__t_

    @display_name.setter
    def display_name(self, value):
        self.__jjr_pc__t_ = value

    @property
    def display_name_prefix(self):
        return self.d_lurjyi___x

    @display_name_prefix.setter
    def display_name_prefix(self, value):
        self.d_lurjyi___x = value

    @property
    def ftp_site(self):
        return self.__jra_lp____

    @ftp_site.setter
    def ftp_site(self, value):
        self.__jra_lp____ = value

    @property
    def generation(self):
        return self.____iiu_h__i

    @generation.setter
    def generation(self, value):
        self.____iiu_h__i = value

    @property
    def given_name(self):
        return self._y______e___

    @given_name.setter
    def given_name(self, value):
        self._y______e___ = value

    @property
    def government_id(self):
        return self.ol____d_r__y

    @government_id.setter
    def government_id(self, value):
        self.ol____d_r__y = value

    @property
    def hobbies(self):
        return self.__t_j_op_tt_

    @hobbies.setter
    def hobbies(self, value):
        self.__t_j_op_tt_ = value

    @property
    def home_phone2(self):
        return self._m___i______

    @home_phone2.setter
    def home_phone2(self, value):
        self._m___i______ = value

    @property
    def home_address_city(self):
        return self.z__b________

    @home_address_city.setter
    def home_address_city(self, value):
        self.z__b________ = value

    @property
    def home_address_country(self):
        return self.jg____s__g_s

    @home_address_country.setter
    def home_address_country(self, value):
        self.jg____s__g_s = value

    @property
    def home_address_postal_code(self):
        return self.gmy_g__pb__d

    @home_address_postal_code.setter
    def home_address_postal_code(self, value):
        self.gmy_g__pb__d = value

    @property
    def home_address_post_office_box(self):
        return self._pro__frgm__

    @home_address_post_office_box.setter
    def home_address_post_office_box(self, value):
        self._pro__frgm__ = value

    @property
    def home_address_state(self):
        return self.___s__yjk_q_

    @home_address_state.setter
    def home_address_state(self, value):
        self.___s__yjk_q_ = value

    @property
    def home_address_street(self):
        return self.kzdmh__i__y_

    @home_address_street.setter
    def home_address_street(self, value):
        self.kzdmh__i__y_ = value

    @property
    def home_fax(self):
        return self.p__lj__pay_g

    @home_fax.setter
    def home_fax(self, value):
        self.p__lj__pay_g = value

    @property
    def home_phone(self):
        return self.vo___j____gl

    @home_phone.setter
    def home_phone(self, value):
        self.vo___j____gl = value

    @property
    def initials(self):
        return self.z_w_qqxyx___

    @initials.setter
    def initials(self, value):
        self.z_w_qqxyx___ = value

    @property
    def isdn(self):
        return self.___w__pydr__

    @isdn.setter
    def isdn(self, value):
        self.___w__pydr__ = value

    @property
    def manager_name(self):
        return self.__ppjf_____v

    @manager_name.setter
    def manager_name(self, value):
        self.__ppjf_____v = value

    @property
    def middle_name(self):
        return self.____ixh_____

    @middle_name.setter
    def middle_name(self, value):
        self.____ixh_____ = value

    @property
    def nickname(self):
        return self.f__fj___kg__

    @nickname.setter
    def nickname(self, value):
        self.f__fj___kg__ = value

    @property
    def office_location(self):
        return self.fcg__x__l_bh

    @office_location.setter
    def office_location(self, value):
        self.fcg__x__l_bh = value

    @property
    def other_address_city(self):
        return self.hxpxy___q__z

    @other_address_city.setter
    def other_address_city(self, value):
        self.hxpxy___q__z = value

    @property
    def other_address_country(self):
        return self.___a___sf___

    @other_address_country.setter
    def other_address_country(self, value):
        self.___a___sf___ = value

    @property
    def other_address_postal_code(self):
        return self.___l__fc_s_d

    @other_address_postal_code.setter
    def other_address_postal_code(self, value):
        self.___l__fc_s_d = value

    @property
    def other_address_state(self):
        return self.t____l_e_ob_

    @other_address_state.setter
    def other_address_state(self, value):
        self.t____l_e_ob_ = value

    @property
    def other_address_street(self):
        return self.sfuq__vbny_x

    @other_address_street.setter
    def other_address_street(self, value):
        self.sfuq__vbny_x = value

    @property
    def other_phone(self):
        return self._ox_pj__nhnr

    @other_phone.setter
    def other_phone(self, value):
        self._ox_pj__nhnr = value

    @property
    def pager(self):
        return self.__b_y_d_kqv_

    @pager.setter
    def pager(self, value):
        self.__b_y_d_kqv_ = value

    @property
    def personal_home_page(self):
        return self.a_akhxq__gp_

    @personal_home_page.setter
    def personal_home_page(self, value):
        self.a_akhxq__gp_ = value

    @property
    def postal_address(self):
        return self.k_m_i___o__h

    @postal_address.setter
    def postal_address(self, value):
        self.k_m_i___o__h = value

    @property
    def business_address_country(self):
        return self._e___sik_flm

    @business_address_country.setter
    def business_address_country(self, value):
        self._e___sik_flm = value

    @property
    def business_address_city(self):
        return self.lp_y_____s__

    @business_address_city.setter
    def business_address_city(self, value):
        self.lp_y_____s__ = value

    @property
    def business_address_postal_code(self):
        return self.b_xkfy_m__v_

    @business_address_postal_code.setter
    def business_address_postal_code(self, value):
        self.b_xkfy_m__v_ = value

    @property
    def business_address_post_office_box(self):
        return self.qvx_e_ns____

    @business_address_post_office_box.setter
    def business_address_post_office_box(self, value):
        self.qvx_e_ns____ = value

    @property
    def business_address_state(self):
        return self.sba__qjh___k

    @business_address_state.setter
    def business_address_state(self, value):
        self.sba__qjh___k = value

    @property
    def business_address_street(self):
        return self.gs_m_____l__

    @business_address_street.setter
    def business_address_street(self, value):
        self.gs_m_____l__ = value

    @property
    def primary_fax(self):
        return self.__ju____j__c

    @primary_fax.setter
    def primary_fax(self, value):
        self.__ju____j__c = value

    @property
    def primary_phone(self):
        return self._p__wc_gnx_g

    @primary_phone.setter
    def primary_phone(self, value):
        self._p__wc_gnx_g = value

    @property
    def profession(self):
        return self.sc_gg_f____i

    @profession.setter
    def profession(self, value):
        self.sc_gg_f____i = value

    @property
    def radio_phone(self):
        return self.lkex____f__e

    @radio_phone.setter
    def radio_phone(self, value):
        self.lkex____f__e = value

    @property
    def spouse_name(self):
        return self.s___b__i___o

    @spouse_name.setter
    def spouse_name(self, value):
        self.s___b__i___o = value

    @property
    def surname(self):
        return self.lkc__aliq_g_

    @surname.setter
    def surname(self, value):
        self.lkc__aliq_g_ = value

    @property
    def telex(self):
        return self._sw_lg____k_

    @telex.setter
    def telex(self, value):
        self._sw_lg____k_ = value

    @property
    def title(self):
        return self.b____ioy____

    @title.setter
    def title(self, value):
        self.b____ioy____ = value

    @property
    def tty_tdd_phone(self):
        return self.__j_____m_ge

    @tty_tdd_phone.setter
    def tty_tdd_phone(self, value):
        self.__j_____m_ge = value

    @property
    def wedding_anniversary(self):
        return self.u_u_t_ci___p

    @wedding_anniversary.setter
    def wedding_anniversary(self, value):
        self.u_u_t_ci___p = value

    @property
    def gender(self):
        return self.bw____sz____

    @gender.setter
    def gender(self, value):
        self.bw____sz____ = value

    @property
    def selected_mailing_address(self):
        return self._hle_ua_z__g

    @selected_mailing_address.setter
    def selected_mailing_address(self, value):
        self._hle_ua_z__g = value

    @property
    def contact_has_picture(self):
        return self.y__i_no____g

    @contact_has_picture.setter
    def contact_has_picture(self, value):
        self.y__i_no____g = value

    @property
    def file_as(self):
        return self.__el_ca_i_l_

    @file_as.setter
    def file_as(self, value):
        self.__el_ca_i_l_ = value

    @property
    def instant_messenger_address(self):
        return self.___w___f___x

    @instant_messenger_address.setter
    def instant_messenger_address(self, value):
        self.___w___f___x = value

    @property
    def internet_free_busy_address(self):
        return self.l_a_g_kx____

    @internet_free_busy_address.setter
    def internet_free_busy_address(self, value):
        self.l_a_g_kx____ = value

    @property
    def business_address(self):
        return self.g___cd_p_do_

    @business_address.setter
    def business_address(self, value):
        self.g___cd_p_do_ = value

    @property
    def home_address(self):
        return self.q_j______u_u

    @home_address.setter
    def home_address(self, value):
        self.q_j______u_u = value

    @property
    def other_address(self):
        return self._iwxsuk___iu

    @other_address.setter
    def other_address(self, value):
        self._iwxsuk___iu = value

    @property
    def email1_address(self):
        return self._d_d___jg__u

    @email1_address.setter
    def email1_address(self, value):
        self._d_d___jg__u = value

    @property
    def email2_address(self):
        return self.c_x_q___hzc_

    @email2_address.setter
    def email2_address(self, value):
        self.c_x_q___hzc_ = value

    @property
    def email3_address(self):
        return self._c_dcu_np_f_

    @email3_address.setter
    def email3_address(self, value):
        self._c_dcu_np_f_ = value

    @property
    def email1_display_name(self):
        return self._y_g__fjv_r_

    @email1_display_name.setter
    def email1_display_name(self, value):
        self._y_g__fjv_r_ = value

    @property
    def email2_display_name(self):
        return self.____e____jg_

    @email2_display_name.setter
    def email2_display_name(self, value):
        self.____e____jg_ = value

    @property
    def email3_display_name(self):
        return self.go___g_____l

    @email3_display_name.setter
    def email3_display_name(self, value):
        self.go___g_____l = value

    @property
    def email1_display_as(self):
        return self.ypp___r__q__

    @email1_display_as.setter
    def email1_display_as(self, value):
        self.ypp___r__q__ = value

    @property
    def email2_display_as(self):
        return self.q_vxh_uz___i

    @email2_display_as.setter
    def email2_display_as(self, value):
        self.q_vxh_uz___i = value

    @property
    def email3_display_as(self):
        return self.qw__y_l__p__

    @email3_display_as.setter
    def email3_display_as(self, value):
        self.qw__y_l__p__ = value

    @property
    def email1_type(self):
        return self._a___u____sj

    @email1_type.setter
    def email1_type(self, value):
        self._a___u____sj = value

    @property
    def email2_type(self):
        return self.v__kpwt___jh

    @email2_type.setter
    def email2_type(self, value):
        self.v__kpwt___jh = value

    @property
    def email3_type(self):
        return self.v_rn_m______

    @email3_type.setter
    def email3_type(self, value):
        self.v_rn_m______ = value

    @property
    def email1_entry_id(self):
        return self.kiork_z_o__p

    @email1_entry_id.setter
    def email1_entry_id(self, value):
        self.kiork_z_o__p = value

    @property
    def email2_entry_id(self):
        return self.n_dl_t_l____

    @email2_entry_id.setter
    def email2_entry_id(self, value):
        self.n_dl_t_l____ = value

    @property
    def email3_entry_id(self):
        return self.____cve____g

    @email3_entry_id.setter
    def email3_entry_id(self, value):
        self.____cve____g = value

    @property
    def recipients(self):
        return self.__g_y__yifly

    @recipients.setter
    def recipients(self, value):
        self.__g_y__yifly = value

    @property
    def attachments(self):
        return self.j____d____c_

    @attachments.setter
    def attachments(self, value):
        self.j____d____c_ = value

    @property
    def extended_properties(self):
        return self._r__n__wc_bq

    @extended_properties.setter
    def extended_properties(self, value):
        self._r__n__wc_bq = value

    @property
    def named_properties(self):
        return self._m_rz____h__

    @named_properties.setter
    def named_properties(self, value):
        self._m_rz____h__ = value

    @property
    def encoding(self):
        return self._gm_g__n___a

    @encoding.setter
    def encoding(self, value):
        self._gm_g__n___a = value

    @property
    def is_embedded(self):
        return self.ulyx_zb_hrlu

    @is_embedded.setter
    def is_embedded(self, value):
        self.ulyx_zb_hrlu = value



class Crc:

    def __init__(self):

        self.crc = 0
        self.crc_table = [	0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419,
							0x706AF48F, 0xE963A535, 0x9E6495A3, 0x0EDB8832, 0x79DCB8A4,
							0xE0D5E91E, 0x97D2D988, 0x09B64C2B, 0x7EB17CBD, 0xE7B82D07,
							0x90BF1D91, 0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE,
							0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7, 0x136C9856,
							0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9,
							0xFA0F3D63, 0x8D080DF5, 0x3B6E20C8, 0x4C69105E, 0xD56041E4,
							0xA2677172, 0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B,
							0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940, 0x32D86CE3,
							0x45DF5C75, 0xDCD60DCF, 0xABD13D59, 0x26D930AC, 0x51DE003A,
							0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423, 0xCFBA9599,
							0xB8BDA50F, 0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924,
							0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D, 0x76DC4190,
							0x01DB7106, 0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F,
							0x9FBFE4A5, 0xE8B8D433, 0x7807C9A2, 0x0F00F934, 0x9609A88E,
							0xE10E9818, 0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01,
							0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E, 0x6C0695ED,
							0x1B01A57B, 0x8208F4C1, 0xF50FC457, 0x65B0D9C6, 0x12B7E950,
							0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3,
							0xFBD44C65, 0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2,
							0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB, 0x4369E96A,
							0x346ED9FC, 0xAD678846, 0xDA60B8D0, 0x44042D73, 0x33031DE5,
							0xAA0A4C5F, 0xDD0D7CC9, 0x5005713C, 0x270241AA, 0xBE0B1010,
							0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
							0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17,
							0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD, 0xEDB88320, 0x9ABFB3B6,
							0x03B6E20C, 0x74B1D29A, 0xEAD54739, 0x9DD277AF, 0x04DB2615,
							0x73DC1683, 0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8,
							0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1, 0xF00F9344,
							0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB,
							0x196C3671, 0x6E6B06E7, 0xFED41B76, 0x89D32BE0, 0x10DA7A5A,
							0x67DD4ACC, 0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5,
							0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1,
							0xA6BC5767, 0x3FB506DD, 0x48B2364B, 0xD80D2BDA, 0xAF0A1B4C,
							0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55, 0x316E8EEF,
							0x4669BE79, 0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236,
							0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F, 0xC5BA3BBE,
							0xB2BD0B28, 0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31,
							0x2CD99E8B, 0x5BDEAE1D, 0x9B64C2B0, 0xEC63F226, 0x756AA39C,
							0x026D930A, 0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713,
							0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38, 0x92D28E9B,
							0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21, 0x86D3D2D4, 0xF1D4E242,
							0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1,
							0x18B74777, 0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C,
							0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45, 0xA00AE278,
							0xD70DD2EE, 0x4E048354, 0x3903B3C2, 0xA7672661, 0xD06016F7,
							0x4969474D, 0x3E6E77DB, 0xAED16A4A, 0xD9D65ADC, 0x40DF0B66,
							0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
							0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605,
							0xCDD70693, 0x54DE5729, 0x23D967BF, 0xB3667A2E, 0xC4614AB8,
							0x5D681B02, 0x2A6F2B94, 0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B,
							0x2D02EF8D ]

    @property
    def value(self):
        return self.crc

    def reset(self):
        crc = 0

    def update(self, buffer):

        offset = 0
        length = len(buffer)

        self.crc ^= 4294967295
        length -= 1

        while (length >= 0):
            self.crc = self.crc_table[(self.crc ^ buffer[offset]) & 0xFF] ^ (self.crc >> 8)
            length -= 1
            offset += 1

        self.crc ^= 4294967295
        

class Attachment:

    def __init__(self, file_path = None, buffer = None):

        self.additional_info = None
        self.content_base = None
        self.content_id = None
        self.content_location = None
        self.content_disposition = None
        self.data = None
        self.data_object = None
        self.encoding = None
        self.record_key = None
        self.extension = None
        self.file_name = None
        self.flags = AttachmentFlags.NONE
        self.long_file_name = None
        self.long_path_name = None
        self.method = AttachmentMethod.ATTACH_BY_VALUE
        self.mime_sequence = 0
        self.mime_tag = None
        self.path_name = None
        self.rendering = None
        self.rendering_position = 0
        self.size = 0
        self.tag = None
        self.transport_name = None
        self.display_name = None
        self.embedded_message = None
        self.object_type = ObjectType.NONE
        self.is_hidden = False
        self.is_contact_photo = False
        self.creation_time = datetime.datetime(1,1,1)
        self.last_modification_time = datetime.datetime(1,1,1)
        self.data_object_storage = None
        self.properties_stream = None

        if file_path is not None: 
            f = open(file_path, 'rb')
            self.file_name = os.path.basename(file_path)
            self.display_name = os.path.basename(file_path)
            self.long_file_name = os.path.basename(file_path)
            self.data = f.read()
            f.close()

        elif buffer != None:
            self.data = buffer

    def to_bytes(self):
        if self.data is not None:
            return self.data
        elif self.data_object is not None:
            return self.data_object
        else:
            return None

    def save(self, file_path):

        if file_path is not None and self.to_bytes() is not None:
            file = open(file_path, "wb")
            file.write(self.to_bytes())
            file.close

class Recipient:

    def __init__(self):

        self.display_name = None
        self.email_address = None
        self.address_type = None
        self.object_type = ObjectType.NONE
        self.recipient_type = RecipientType.NONE
        self.display_type = DisplayType.NONE
        self.entry_id = None
        self.instance_key = None
        self.search_key = None
        self.responsibility = False
        self.smtp_address = None
        self.display_name_7bit = None
        self.transmitable_display_name = None
        self.send_rich_info = False
        self.send_internet_encoding = 0
        self.originating_address_type = None
        self.originating_email_address = None

class RecurrencePattern:

    def __init__(self, buffer = None):

        self.frequency = RecurrencePatternFrequency.DAILY
        self.type = RecurrencePatternType.DAY
        self.period = 0
        self.day_of_week = []
        self.day_of_week_index = DayOfWeekIndex.NONE
        self.day_of_month = 0
        self.end_type = RecurrenceEndType.NEVER_END
        self.occurence_count = 0
        self.first_day_of_week = DayOfWeek.SUNDAY
        self.deleted_instance_count = 0
        self.deleted_instance_dates = []
        self.modified_instance_count = 0
        self.modified_instance_dates = []
        self.start_date = datetime.datetime(1,1,1)
        self.end_date = datetime.datetime(1,1,1)

        if buffer is not None:
            self.jo__bob__g__(buffer)

    def jo__bob__g__(self, buffer):

        if len(buffer) < 22:
            return

        frequency_value = int.from_bytes(buffer[4: 6], "little")
        self.frequency = EnumUtil.parse_recurrence_pattern_frequency(frequency_value)

        type_value = int.from_bytes(buffer[6: 8], "little")
        self.type = EnumUtil.parse_recurrence_pattern_type(type_value)

        calendar_type_value = int.from_bytes(buffer[8: 10], "little")
        self.calendar_type = EnumUtil.parse_calendar_type(calendar_type_value)

        first_date_time_value = int.from_bytes(buffer[10: 12], "little")        
        period =  int.from_bytes(buffer[14: 16], "little")

        next_position = 22

        if self.type == RecurrencePatternType.DAY:
            pass
        elif self.type == RecurrencePatternType.WEEK:

            day_of_week_value = int.from_bytes(buffer[next_position: next_position + 4], "little")     
            next_position += 4

            self.day_of_week = []

            if (day_of_week_value & 0x00000001) == 0x00000001:
                self.day_of_week.append(DayOfWeek.SUNDAY)

            if (day_of_week_value & 0x00000002) == 0x00000002:
                self.day_of_week.append(DayOfWeek.MONDAY)

            if (day_of_week_value & 0x00000004) == 0x00000004:
                self.day_of_week.append(DayOfWeek.TUESDAY)

            if (day_of_week_value & 0x00000008) == 0x00000008:
                self.day_of_week.append(DayOfWeek.WEDNESDAY)

            if (day_of_week_value & 0x00000010) == 0x00000010:
                self.day_of_week.append(DayOfWeek.THURSDAY)

            if (day_of_week_value & 0x00000020) == 0x00000020:
                self.day_of_week.append(DayOfWeek.FRIDAY)

            if (day_of_week_value & 0x00000040) == 0x00000040:
                self.day_of_week.append(DayOfWeek.SATURDAY)

        elif self.type == RecurrencePatternType.MONTH or self.type == RecurrencePatternType.HIJRI_MONTH:
            self.day_of_month = int.from_bytes(buffer[next_position: next_position + 4], "little")     
            nextPosition += 4

        elif self.type == RecurrencePatternType.MONTH_END or self.type == RecurrencePatternType.HIJRI_MONTH_END or self.type == RecurrencePatternType.MONTH_NTH or self.type == RecurrencePatternType.HIJRI_MONTH_NTH:
            
            if len(buffer) < 50:
                return

            day_of_week_value = int.from_bytes(buffer[next_position: next_position + 4], "little")     
            next_position += 4

            day_of_week_index_value = int.from_bytes(buffer[next_position: next_position + 4], "little")     
            next_position += 4

            self.day_of_week = []

            if (day_of_week_value & 0x00000001) == 0x00000001:
                self.day_of_week.append(DayOfWeek.SUNDAY)

            if (day_of_week_value & 0x00000002) == 0x00000002:
                self.day_of_week.append(DayOfWeek.MONDAY)

            if (day_of_week_value & 0x00000004) == 0x00000004:
                self.day_of_week.append(DayOfWeek.TUESDAY)

            if (day_of_week_value & 0x00000008) == 0x00000008:
                self.day_of_week.append(DayOfWeek.WEDNESDAY)

            if (day_of_week_value & 0x00000010) == 0x00000010:
                self.day_of_week.append(DayOfWeek.THURSDAY)

            if (day_of_week_value & 0x00000020) == 0x00000020:
                self.day_of_week.append(DayOfWeek.FRIDAY)

            if (day_of_week_value & 0x00000040) == 0x00000040:
                self.day_of_week.append(DayOfWeek.SATURDAY)

            if day_of_week_index_value == 0x00000001:
                self.day_of_week_index  = DayOfWeekIndex.FIRST
            elif day_of_week_index_value == 0x00000002:
                self.day_of_week_index  = DayOfWeekIndex.SECOND
            elif day_of_week_index_value == 0x00000003:
                self.day_of_week_index  = DayOfWeekIndex.THIRD
            elif day_of_week_index_value == 0x00000004:
                self.day_of_week_index  = DayOfWeekIndex.FOURTH
            elif day_of_week_index_value == 0x00000005:
                self.day_of_week_index = DayOfWeekIndex.LAST
        

        end_type_value = int.from_bytes(buffer[next_position: next_position + 4], "little")     
        next_position += 4

        self.end_type = EnumUtil.parse_recurrence_end_type(end_type_value)
        
        self.occurence_count = int.from_bytes(buffer[next_position: next_position + 4], "little")     
        next_position += 4

        first_day_of_week_value = int.from_bytes(buffer[next_position: next_position + 4], "little")  
        next_position += 4

        self.firstDayOfWeek = EnumUtil.parse_day_of_week(first_day_of_week_value)

        self.deleted_instance_count = int.from_bytes(buffer[next_position: next_position + 4], "little")  
        next_position += 4

        if self.deleted_instance_count > 0:

            self.deleted_instance_dates = []

            for i in range(self.deleted_instance_count):

                if len(buffer) < next_position + 4:
                    return

                minutes = int.from_bytes(buffer[next_position: next_position + 4], "little")  
                next_position += 4

                self.deleted_instance_dates.append(RecurrencePattern.r_erp_ic____(minutes))            

        self.modified_instance_count = int.from_bytes(buffer[next_position: next_position + 4], "little") 
        next_position += 4

        if self.modified_instance_count > 0:

            self.modified_instance_dates = []

            for i in range(self.modified_instance_count):

                if len(buffer) < next_position + 4:
                    return

                minutes = int.from_bytes(buffer[next_position: next_position + 4], "little")  
                next_position += 4

                self.modified_instance_dates.append(RecurrencePattern.r_erp_ic____(minutes))   

        if len(buffer) < next_position + 4:
            return

        start_date_minutes =  int.from_bytes(buffer[next_position: next_position + 4], "little")  
        next_position += 4

        self.start_date = RecurrencePattern.r_erp_ic____(start_date_minutes)

        end_date_minutes = int.from_bytes(buffer[next_position: next_position + 4], "little")  

        self.end_date = RecurrencePattern.r_erp_ic____(end_date_minutes)

    @staticmethod
    def r_erp_ic____(i________ofl):

        b__ej____p__ = datetime.datetime(1901,1,1)

        try:
            j____h_x_v_h = datetime.datetime(1601,1,1)
            b______q___a = i________ofl * 60 * 1000
            b__ej____p__ = j____h_x_v_h + datetime.timedelta(b______q___a)
        except:
            pass

        return b__ej____p__

class Property:

    def __init__(self, buffer = None):

        self.tag = 0
        self.type = PropertyType.INTEGER_16
        self.size = 0
        self.value = None
        self.is_mandatory = False
        self.is_readable = False
        self.is_writeable = False

        if buffer is not None:
            self.tag = int.from_bytes(buffer[0: 4], "little")
            self.type = EnumUtil.parse_property_type(self.tag)
            
            flags = int.from_bytes(buffer[4: 8], "little")

            if flags == 1:
                self.is_mandatory = True
            elif flags == 2:
                self.is_readable = True
            elif flags == 3:
                self.is_mandatory = True
                self.is_readable = True
            elif flags == 4:
                self.is_writeable = True
            elif flags == 5:
                self.is_mandatory = True
                self.is_writeable = True
            elif flags == 6:
                self.is_readable = True
                self.is_writeable = True
            elif flags == 7:
                self.is_mandatory = True
                self.is_readable = True
                self.is_writeable = True
        
            if self.type == PropertyType.INTEGER_16:
                self.value = buffer[8: 10]
            elif self.type == PropertyType.INTEGER_32:
                self.value = buffer[8: 12]
            elif self.type == PropertyType.INTEGER_64:
                self.value = buffer[8: 16]
            elif self.type == PropertyType.FLOATING_32:
                self.value = buffer[8: 12]
            elif self.type == PropertyType.FLOATING_64:
                self.value = buffer[8: 16]
            elif self.type == PropertyType.CURRENCY:
                self.value = buffer[8: 16]
            elif self.type == PropertyType.FLOATING_TIME:
                self.value = buffer[8: 16]
            elif self.type == PropertyType.ERROR_CODE:
                self.value = buffer[8: 12]
            elif self.type == PropertyType.BOOLEAN:
                self.value = buffer[8: 10]
            elif self.type == PropertyType.TIME:
                self.value = buffer[8: 16]
            else:
                self.size = int.from_bytes(buffer[8: 12], "little")

    def to_bytes(self):

        memory_stream = bytearray(16)
        position = 0

        memory_stream[position: position + 4] = int.to_bytes(self.tag, 4, "little")
        position += 4

        flags = 0

        if self.is_mandatory:
            flags += 1

        if self.is_readable:
            flags += 2

        if self.is_writeable:
            flags += 4

        memory_stream[position: position + 4] = int.to_bytes(flags, 4, "little")
        position += 4
        
        if self.size > 0:
            memory_stream[position: position + 4] = int.to_bytes(self.size, 4, "little")
            position += 4
        elif self.value is not None and len(self.value) > 0:
            memory_stream[position: position + len(self.value)] = self.value

        return bytes(memory_stream)


class ExtendedProperty:

    def __init__(self, tag = None, value = None):

        self.tag = tag
        self.value = value

class ExtendedPropertyTag:

    def __init__(self, guid = None, type = None):

        self.guid = guid
        self.type = type

class ExtendedPropertyName(ExtendedPropertyTag):

    def __init__(self, name = None, guid = None, type = None):

        super().__init__(guid, type)
        self.name = name

    def __str__(self):
        return self.id

class ExtendedPropertyId(ExtendedPropertyTag):

    def __init__(self, id = 0, guid = None, type = None):

        super().__init__(guid, type)
        self.id = id

    def __str__(self):
        return self.id

class NamedProperty:

    def __init__(self):

        self.id = 0
        self.name = None
        self.guid = None
        self.type = NamedPropertyType.STRING

class EnumUtil:

    @staticmethod
    def parse_gender(gender):

        if isinstance(gender, Gender): 
            if gender == Gender.FEMALE:
                return 1
            elif gender == Gender.MALE:
                return 2
            else:
                return 0
        else:
            if gender == 1:
                return Gender.FEMALE
            elif gender == 2:
                return Gender.MALE
            else:
                return Gender.NONE

    @staticmethod
    def parse_last_verb_executed(verb):
        
        if isinstance(verb, LastVerbExecuted): 
            if verb == LastVerbExecuted.REPLY_TO_SENDER:
                return 102
            elif verb == LastVerbExecuted.REPLY_TO_ALL:
                return 103
            elif verb == LastVerbExecuted.FORWARD:
                return 104
            else:
                return 0
        else:
            if verb == 102:
                return LastVerbExecuted.REPLY_TO_SENDER
            elif verb == 103:
                return LastVerbExecuted.REPLY_TO_ALL
            elif verb == 104:
                return LastVerbExecuted.FORWARD
            else:
                return LastVerbExecuted.NONE

    @staticmethod
    def parse_object_type(type):

        if isinstance(type, ObjectType): 
            if type == ObjectType.MESSAGE_STORE:
                return 1
            elif type == ObjectType.ADDRESS_BOOK:
                return 2
            elif type == ObjectType.FOLDER:
                return 3
            elif type == ObjectType.ADDRESS_BOOK_CONTAINER:
                return 4
            elif type == ObjectType.MESSAGE:
                return 5
            elif type == ObjectType.MAIL_USER:
                return 6
            elif type == ObjectType.ATTACHMENT:
                return 7
            elif type == ObjectType.DISTRIBUTION_LIST:
                return 8
            elif type == ObjectType.PROFILE_SELECTION:
                return 9
            elif type == ObjectType.STATUS:
                return 0x0000000A
            elif type == ObjectType.SESSION:
                return 0x0000000B
            elif type == ObjectType.FORM:
                return 0x0000000C
            else:
                return 0
        else:
            if type == 1:
                return ObjectType.MESSAGE_STORE
            elif type == 2:
                return ObjectType.ADDRESS_BOOK
            elif type == 3:
                return ObjectType.FOLDER
            elif type == 4:
                return ObjectType.ADDRESS_BOOK_CONTAINER
            elif type == 5:
                return ObjectType.MESSAGE
            elif type == 6:
                return ObjectType.MAIL_USER
            elif type == 7:
                return ObjectType.ATTACHMENT
            elif type == 8:
                return ObjectType.DISTRIBUTION_LIST
            elif type == 9:
                return ObjectType.PROFILE_SELECTION
            elif type == 0x0000000A:
                return ObjectType.STATUS
            elif type == 0x0000000B:
                return ObjectType.SESSION
            elif type == 0x0000000C:
                return ObjectType.FORM
            else:
                return ObjectType.NONE

    @staticmethod
    def parse_store_support_mask(mask):

        if isinstance(mask, list):

            store_support_masks = 0

            for i in range(len(mask)):

                current_mask = mask[i]

                if current_mask == StoreSupportMask.ANSI:
                    store_support_masks += 0x00020000
                elif current_mask == StoreSupportMask.ATTACHMENTS:
                    store_support_masks += 0x00000020
                elif current_mask == StoreSupportMask.CATEGORIZE:
                    store_support_masks += 0x00000400
                elif current_mask == StoreSupportMask.CREATE:
                    store_support_masks += 0x00000010
                elif current_mask == StoreSupportMask.HTML:
                    store_support_masks += 0x00010000
                elif current_mask == StoreSupportMask.ITEM_PROC:
                    store_support_masks += 0x00200000
                elif current_mask == StoreSupportMask.LOCAL_STORE:
                    store_support_masks += 0x00080000
                elif current_mask == StoreSupportMask.MODIFY:
                    store_support_masks += 0x00000008
                elif current_mask == StoreSupportMask.MULTI_VALUE_PROPERTIES:
                    store_support_masks += 0x00000200
                elif current_mask == StoreSupportMask.NOTIFY:
                    store_support_masks += 0x00000100
                elif current_mask == StoreSupportMask.OLE:
                    store_support_masks += 0x00000040
                elif current_mask == StoreSupportMask.PUBLIC_FOLDERS:
                    store_support_masks += 0x00004000
                elif current_mask == StoreSupportMask.PUSHER:
                    store_support_masks += 0x00800000
                elif current_mask == StoreSupportMask.READ_ONLY:
                    store_support_masks += 0x00000002
                elif current_mask == StoreSupportMask.RESTRICTIONS:
                    store_support_masks += 0x00001000
                elif current_mask == StoreSupportMask.RTF:
                    store_support_masks += 0x00000800
                elif current_mask == StoreSupportMask.SEARCH:
                    store_support_masks += 0x00000004
                elif current_mask == StoreSupportMask.SORT:
                    store_support_masks += 0x00002000
                elif current_mask == StoreSupportMask.SUBMIT:
                    store_support_masks += 0x00000080
                elif current_mask == StoreSupportMask.UNCOMPRESSED_RTF:
                    store_support_masks += 0x00008000
                elif current_mask == StoreSupportMask.UNICODE:
                    store_support_masks += 0x00040000
            
            return store_support_masks

        else:

            mask_list = []

            if mask & 0x00020000 == 0x00020000:
                mask_list.append(StoreSupportMask.ANSI)

            if mask & 0x00000020 == 0x00000020:
                mask_list.append(StoreSupportMask.ATTACHMENTS)

            if mask & 0x00000400 == 0x00000400:
                mask_list.append(StoreSupportMask.CATEGORIZE)

            if mask & 0x00000010 == 0x00000010:
                mask_list.append(StoreSupportMask.CREATE)

            if mask & 0x00010000 == 0x00010000:
                mask_list.append(StoreSupportMask.HTML)

            if mask & 0x00200000 == 0x00200000:
                mask_list.append(StoreSupportMask.ITEM_PROC)
            
            if mask & 0x00080000 == 0x00080000:
                mask_list.append(StoreSupportMask.LOCAL_STORE)

            if mask & 0x00000008 == 0x00000008:
                mask_list.append(StoreSupportMask.MODIFY)

            if mask & 0x00000200 == 0x00000200:
                mask_list.append(StoreSupportMask.MULTI_VALUE_PROPERTIES)

            if mask & 0x00000100 == 0x00000100:
                mask_list.append(StoreSupportMask.NOTIFY)

            if mask & 0x00000040 == 0x00000040:
                mask_list.append(StoreSupportMask.OLE)

            if mask & 0x00004000 == 0x00004000:
                mask_list.append(StoreSupportMask.PUBLIC_FOLDERS)
            
            if mask & 0x00800000 == 0x00800000:
                mask_list.append(StoreSupportMask.PUSHER)

            if mask & 0x00000002 == 0x00000002:
                mask_list.append(StoreSupportMask.READ_ONLY)

            if mask & 0x00001000 == 0x00001000:
                mask_list.append(StoreSupportMask.RESTRICTIONS)

            if mask & 0x00000800 == 0x00000800:
                mask_list.append(StoreSupportMask.RTF)

            if mask & 0x00000004 == 0x00000004:
                mask_list.append(StoreSupportMask.SEARCH)

            if mask & 0x00002000 == 0x00002000:
                mask_list.append(StoreSupportMask.SORT)

            if mask & 0x00000080 == 0x00000080:
                mask_list.append(StoreSupportMask.SUBMIT)

            if mask & 0x00008000 == 0x00008000:
                mask_list.append(StoreSupportMask.UNCOMPRESSED_RTF)

            if mask & 0x00040000 == 0x00040000:
                mask_list.append(StoreSupportMask.UNICODE)

            return mask_list
            
    @staticmethod
    def parse_message_flag(flags):

        if isinstance(flags, list):

            message_flags = 0

            for i in range(len(flags)):

                current_message_flag = flags[i]

                if current_message_flag == MessageFlag.ASSOCIATED:
                    message_flags += 0x00000040
                elif current_message_flag == MessageFlag.FROM_ME:
                    message_flags += 0x00000020
                elif current_message_flag == MessageFlag.HAS_ATTACHMENT:
                    message_flags += 0x00000010
                elif current_message_flag == MessageFlag.NON_READ_REPORT_PENDING:
                    message_flags += 0x00000200
                elif current_message_flag == MessageFlag.ORIGIN_INTERNET:
                    message_flags += 0x00002000
                elif current_message_flag == MessageFlag.ORIGIN_MISC_EXTERNAL:
                    message_flags += 0x00008000
                elif current_message_flag == MessageFlag.ORIGIN_X400:
                    message_flags += 0x00001000
                elif current_message_flag == MessageFlag.READ:
                    message_flags += 0x00000001
                elif current_message_flag == MessageFlag.RESEND:
                    message_flags += 0x00000080
                elif current_message_flag == MessageFlag.READ_REPORT_PENDING:
                    message_flags += 0x00000100
                elif current_message_flag == MessageFlag.SUBMIT:
                    message_flags += 0x00000004
                elif current_message_flag == MessageFlag.UNMODIFIED:
                    message_flags += 0x00000002
                elif current_message_flag == MessageFlag.UNSENT:
                    message_flags += 0x00000008
        
            return message_flags

        else:

            flag_list = []

            if flags & 0x00000040 == 0x00000040:
                flag_list.append(MessageFlag.ASSOCIATED)

            if flags & 0x00000020 == 0x00000020:
                flag_list.append(MessageFlag.FROM_ME)

            if flags & 0x00000010 == 0x00000010:
                flag_list.append(MessageFlag.HAS_ATTACHMENT)

            if flags & 0x00000200 == 0x00000200:
                flag_list.append(MessageFlag.NON_READ_REPORT_PENDING)

            if flags & 0x00002000 == 0x00002000:
                flag_list.append(MessageFlag.ORIGIN_INTERNET)

            if flags & 0x00008000 == 0x00008000:
                flag_list.append(MessageFlag.ORIGIN_MISC_EXTERNAL)

            if flags & 0x00001000 == 0x00001000:
                flag_list.append(MessageFlag.ORIGIN_X400)

            if flags & 0x00000001 == 0x00000001:
                flag_list.append(MessageFlag.READ)

            if flags & 0x00000080 == 0x00000080:
                flag_list.append(MessageFlag.RESEND)

            if flags & 0x00000100 == 0x00000100:
                flag_list.append(MessageFlag.READ_REPORT_PENDING)

            if flags & 0x00000004 == 0x00000004:
                flag_list.append(MessageFlag.SUBMIT)

            if flags & 0x00000002 == 0x00000002:
                flag_list.append(MessageFlag.UNMODIFIED)

            if flags & 0x00000008 == 0x00000008:
                flag_list.append(MessageFlag.UNSENT)

            return flag_list

    @staticmethod
    def parse_recurrence_pattern_frequency(frequency):
        
        if frequency == 0x200A:
            return RecurrencePatternFrequency.DAILY
        elif frequency == 0x200B:
            return RecurrencePatternFrequency.WEEKLY
        elif frequency == 0x200C:
            return RecurrencePatternFrequency.MONTHLY
        else:
            return RecurrencePatternFrequency.YEARLY

    @staticmethod
    def parse_day_of_week(dayOfWeek):
    
        if dayOfWeek == 0x00000000:
            return DayOfWeek.SUNDAY
        elif dayOfWeek == 0x00000001:
            return DayOfWeek.MONDAY
        elif dayOfWeek == 0x00000002:
            return DayOfWeek.TUESDAY
        elif dayOfWeek == 0x00000003:
            return DayOfWeek.WEDNESDAY
        elif dayOfWeek == 0x00000004:
            return DayOfWeek.THURSDAY
        elif dayOfWeek == 0x00000005:
            return DayOfWeek.FRIDAY
        else:
            return DayOfWeek.SATURDAY

    @staticmethod
    def parse_day_of_week_index(index):
    
        if index == 0x00000001:
            return DayOfWeekIndex.FIRST
        elif index == 0x00000002:
            return DayOfWeekIndex.SECOND
        elif index == 0x00000003:
            return DayOfWeekIndex.THIRD
        elif index == 0x00000004:
            return DayOfWeekIndex.FOURTH
        else:
            return DayOfWeekIndex.LAST

    @staticmethod
    def parse_recurrence_end_type(end):
    
        if end == 0x00002021:
            return RecurrenceEndType.END_AFTER_DATE
        elif end == 0x00002022:
            return RecurrenceEndType.END_AFTER_N_OCCURRENCES
        else:
            return RecurrenceEndType.NEVER_END

    @staticmethod
    def parse_recurrence_pattern_type(type):
    
        if type == 0x0000:
            return RecurrencePatternType.DAY
        elif type == 0x0001:
            return RecurrencePatternType.WEEK
        elif type == 0x0002:
            return RecurrencePatternType.MONTH
        elif type == 0x0003:
            return RecurrencePatternType.MONTH_END
        elif type == 0x0004:
            return RecurrencePatternType.MONTH_NTH
        elif type == 0x200A:
            return RecurrencePatternType.HIJRI_MONTH
        elif type == 0x200B:
            return RecurrencePatternType.HIJRI_MONTH_END
        else:
            return RecurrencePatternType.HIJRI_MONTH_NTH

    @staticmethod
    def parse_calendar_type(type):
    
        if type == 0x0001:
            return CalendarType.GREGORIAN
        elif type == 0x0002:
            return CalendarType.GREGORIAN_US
        elif type == 0x0003:
            return CalendarType.JAPANESE_EMPOROR_ERA
        elif type == 0x0004:
            return CalendarType.TAIWAN
        elif type == 0x0005:
            return CalendarType.KOREAN_TUNGUN_ERA
        elif type == 0x0006:
            return CalendarType.HIJRI
        elif type == 0x0007:
            return CalendarType.THAI
        elif type == 0x0008:
            return CalendarType.HEBREW_LUNAR
        elif type == 0x0009:
            return CalendarType.GREGORIAN_MIDDLE_EAST_FRENCH
        elif type == 0x000A:
            return CalendarType.GREGORIAN_ARABIC
        elif type == 0x000B:
            return CalendarType.GREGORIAN_TRANSLITERATED_ENGLISH
        elif type == 0x000C:
            return CalendarType.GREGORIAN_TRANSLITERATED_FRENCH
        elif type == 0x000E:
            return CalendarType.JAPANESE_LUNAR
        elif type == 0x000F:
            return CalendarType.CHINESE_LUNAR
        elif type == 0x0010:
            return CalendarType.SAKA_ERA
        elif type == 0x0011:
            return CalendarType.LUNAR_ETO_CHINESE
        elif type == 0x0012:
            return CalendarType.LUNAR_ETO_KOREAN
        elif type == 0x0013:
            return CalendarType.LUNAR_ROKUYOU
        elif type == 0x0014:
            return CalendarType.KOREAN_LUNAR
        elif type == 0x0017:
            return CalendarType.UM_AL_QURA
        else:
            return CalendarType.NONE

    @staticmethod
    def parse_flag_icon(icon):
        
        if isinstance(icon, FlagIcon): 
            if icon == FlagIcon.PURPLE:
                return 1
            elif icon == FlagIcon.ORANGE:
                return 2
            elif icon == FlagIcon.GREEN:
                return 3
            elif icon == FlagIcon.YELLOW:
                return 4
            elif icon == FlagIcon.BLUE:
                return 5
            elif icon == FlagIcon.RED:
                return 6
            else:
                return 0
        else:
            if icon == 1:
                return FlagIcon.PURPLE
            elif icon == 2:
                return FlagIcon.ORANGE
            elif icon == 3:
                return FlagIcon.GREEN
            elif icon == 4:
                return FlagIcon.YELLOW
            elif icon == 5:
                return FlagIcon.BLUE
            elif icon == 6:
                return FlagIcon.RED
            else:
                return FlagIcon.NONE

    @staticmethod
    def parse_selected_mailing_address(address):
        
        if isinstance(address, SelectedMailingAddress): 
            if address == SelectedMailingAddress.HOME:
                return 1
            elif address == SelectedMailingAddress.BUSSINESS:
                return 2
            elif address == SelectedMailingAddress.OTHER:
                return 3
            else:
                return 0
        else:
            if address == 1:
                return SelectedMailingAddress.HOME
            elif address == 2:
                return SelectedMailingAddress.BUSSINESS
            elif address == 3:
                return SelectedMailingAddress.OTHER
            else:
                return SelectedMailingAddress.NONE

    @staticmethod
    def parse_flag_status(status):
        
        if isinstance(status, FlagStatus): 
            if status == FlagStatus.COMPLETE:
                return 1
            elif status == FlagStatus.MARKED:
                return 2
            else:
                return 0
        else:
            if status == 1:
                return FlagStatus.COMPLETE
            elif status == 2:
                return FlagStatus.MARKED
            else:
                return FlagStatus.NONE

    @staticmethod
    def parse_display_type(type):
        
        if isinstance(type, DisplayType): 
            if type == DisplayType.MAIL_USER:
                return 0
            elif type == DisplayType.DISTRIBUTION_LIST:
                return 1
            elif type == DisplayType.FORUM:
                return 2
            elif type == DisplayType.AGENT:
                return 3
            elif type == DisplayType.ORGANIZATION:
                return 4
            elif type == DisplayType.PRIVATE_DISTRIBUTION_LIST:
                return 5
            elif type == DisplayType.REMOTE_MAIL_USER:
                return 6
            elif type == DisplayType.FOLDER:
                return 0x01000000
            elif type == DisplayType.FOLDER_LINK:
                return 0x02000000
            elif type == DisplayType.FOLDER_SPECIAL:
                return 0x04000000
            elif type == DisplayType.MODIFIABLE:
                return 0x00010000
            elif type == DisplayType.GLOBAL_ADDRESS_BOOK:
                return 0x00020000
            elif type == DisplayType.LOCAL_ADDRESS_BOOK:
                return 0x00030000
            elif type == DisplayType.WIDE_AREA_NETWORK_ADDRESS_BOOK:
                return 0x00040000
            elif type == DisplayType.NOT_SPECIFIC:
                return 0x00050000
            else:
                return 0
        else:
            if type == 0:
                return DisplayType.MAIL_USER
            elif type == 1:
                return DisplayType.DISTRIBUTION_LIST
            elif type == 2:
                return DisplayType.FORUM
            elif type == 3:
                return DisplayType.AGENT
            elif type == 4:
                return DisplayType.ORGANIZATION
            elif type == 5:
                return DisplayType.PRIVATE_DISTRIBUTION_LIST
            elif type == 6:
                return DisplayType.REMOTE_MAIL_USER
            elif type == 0x01000000:
                return DisplayType.FOLDER
            elif type == 0x02000000:
                return DisplayType.FOLDER_LINK
            elif type == 0x04000000:
                return DisplayType.FOLDER_SPECIAL
            elif type == 0x00010000:
                return DisplayType.MODIFIABLE
            elif type == 0x00020000:
                return DisplayType.GLOBAL_ADDRESS_BOOK
            elif type == 0x00030000:
                return DisplayType.LOCAL_ADDRESS_BOOK
            elif type == 0x00040000:
                return DisplayType.WIDE_AREA_NETWORK_ADDRESS_BOOK
            elif type == 0x00050000:
                return DisplayType.NOT_SPECIFIC
            else:
                return DisplayType.NONE

    @staticmethod
    def parse_note_color(color):
        
        if isinstance(color, NoteColor): 
            if color == NoteColor.BLUE:
                return 0
            elif color == NoteColor.GREEN:
                return 1
            elif color == NoteColor.PINK:
                return 2
            elif color == NoteColor.YELLOW:
                return 3
            elif color == NoteColor.WHITE:
                return 4
            else:
                return 0
        else:
            return color

    @staticmethod
    def parse_recipient_type(type):
        
        if isinstance(type, RecipientType): 
            if type == RecipientType.TO:
                return 1
            elif type == RecipientType.CC:
                return 2
            elif type == RecipientType.BCC:
                return 3
            elif type == RecipientType.P1:
                return 0x10000000
            else:
                return 0
        else:
            if type == 1:
                return RecipientType.TO
            elif type == 2:
                return RecipientType.CC
            elif type == 3:
                return RecipientType.BCC
            elif type == 0x10000000:
                return RecipientType.P1
            else:
                return RecipientType.NONE

    @staticmethod
    def parse_priority(priority):
        
        if isinstance(priority, Priority): 
            if priority == Priority.LOW:
                return 0xFFFFFFFF
            elif priority == Priority.HIGH:
                return 1
            else:
                return 0
        else:
            if priority == 0xFFFFFFFF:
                return Priority.LOW
            elif priority == 1:
                return Priority.HIGH
            elif priority == 0:
                return Priority.NORMAL
            else:
                return Priority.NONE

    @staticmethod
    def parse_sensitivity(sensitivity):
        
        if isinstance(sensitivity, Sensitivity): 
            if sensitivity == Sensitivity.PERSONAL:
                return 1
            elif sensitivity == Sensitivity.PRIVATE:
                return 2
            elif sensitivity == Sensitivity.CONFIDENTIAL:
                return 3
            else:
                return 0
        else:
            if sensitivity == 1:
                return Sensitivity.PERSONAL
            elif sensitivity == 2:
                return Sensitivity.PRIVATE
            elif sensitivity == 3:
                return Sensitivity.CONFIDENTIAL
            else:
                return Sensitivity.NONE

    @staticmethod
    def parse_importance(importance):
        
        if isinstance(importance, Importance): 
            if importance == Importance.NORMAL:
                return 1
            elif importance == Importance.HIGH:
                return 2
            elif importance == Importance.LOW:
                return 0
            else:
                return 1
        else:
            if importance == 1:
                return Importance.NORMAL
            elif importance == 2:
                return Importance.HIGH
            elif importance == 0:
                return Importance.LOW
            else:
                return Importance.NONE

    @staticmethod
    def parse_task_ownership(ownership):
        
        if isinstance(ownership, TaskOwnership): 
            if ownership == TaskOwnership.NEW:
                return 0
            elif ownership == TaskOwnership.DELEGATED:
                return 1
            elif ownership == TaskOwnership.OWN:
                return 2
            else:
                return 0
        else:
            if ownership == 0:
                return TaskOwnership.NEW
            elif ownership == 1:
                return TaskOwnership.DELEGATED
            elif ownership == 2:
                return TaskOwnership.OWN
            else:
                return TaskOwnership.NONE

    @staticmethod
    def parse_task_delegation_state(state):
        
        if isinstance(state, TaskDelegationState): 
            if state == TaskDelegationState.OWNED:
                return 0
            elif state == TaskDelegationState.OWN_NEW:
                return 1
            elif state == TaskDelegationState.ACCEPTED:
                return 2
            elif state == TaskDelegationState.DECLINED:
                return 3
            elif state == TaskDelegationState.NO_MATCH:
                return 4
            else:
                return 0
        else:
            if state == 0:
                return TaskDelegationState.OWNED
            elif state == 1:
                return TaskDelegationState.OWNED
            elif state == 2:
                return TaskDelegationState.ACCEPTED
            elif state == 3:
                return TaskDelegationState.DECLINED
            elif state == 4:
                return TaskDelegationState.NO_MATCH
            else:
                return TaskDelegationState.NONE

    @staticmethod
    def parse_task_delegation_state(state):
        
        if isinstance(state, TaskDelegationState): 
            if state == TaskDelegationState.OWNED:
                return 0
            elif state == TaskDelegationState.OWN_NEW:
                return 1
            elif state == TaskDelegationState.ACCEPTED:
                return 2
            elif state == TaskDelegationState.DECLINED:
                return 3
            elif state == TaskDelegationState.NO_MATCH:
                return 4
            else:
                return 0
        else:
            if state == 0:
                return TaskDelegationState.OWNED
            elif state == 1:
                return TaskDelegationState.OWNED
            elif state == 2:
                return TaskDelegationState.ACCEPTED
            elif state == 3:
                return TaskDelegationState.DECLINED
            elif state == 4:
                return TaskDelegationState.NO_MATCH
            else:
                return TaskDelegationState.NONE

    @staticmethod
    def parse_busy_status(status):
        
        if isinstance(status, BusyStatus): 
            if status == BusyStatus.FREE:
                return 0
            elif status == BusyStatus.TENTATIVE:
                return 1
            elif status == BusyStatus.BUSY:
                return 2
            elif status == BusyStatus.OUT_OF_OFFICE:
                return 3
            else:
                return 0
        else:
            if status == 0:
                return BusyStatus.FREE
            elif status == 1:
                return BusyStatus.TENTATIVE
            elif status == 2:
                return BusyStatus.BUSY
            elif status == 3:
                return BusyStatus.OUT_OF_OFFICE
            else:
                return BusyStatus.NONE

    @staticmethod
    def parse_recurrence_type(type):
        
        if isinstance(type, RecurrenceType): 
            if type == RecurrenceType.DAILY:
                return 1
            elif type == RecurrenceType.WEEKLY:
                return 2
            elif type == RecurrenceType.MONTHLY:
                return 3
            elif type == RecurrenceType.YEARLY:
                return 4
            elif type == RecurrenceType.MONTHLY_NTH:
                return 5
            elif type == RecurrenceType.YEARLY_NTH:
                return 6
            else:
                return 0
        else:
            if type == 1:
                return RecurrenceType.DAILY
            elif type == 2:
                return RecurrenceType.WEEKLY
            elif type == 3:
                return RecurrenceType.MONTHLY
            elif type == 4:
                return RecurrenceType.YEARLY
            elif type == 5:
                return RecurrenceType.MONTHLY_NTH
            elif type == 6:
                return RecurrenceType.YEARLY_NTH
            else:
                return RecurrenceType.NONE

    @staticmethod
    def parse_response_status(status):
        
        if isinstance(status, ResponseStatus): 
            if status == ResponseStatus.ORGANIZED:
                return 1
            elif status == ResponseStatus.TENTATIVE:
                return 2
            elif status == ResponseStatus.ACCEPTED:
                return 3
            elif status == ResponseStatus.DECLINED:
                return 4
            elif status == ResponseStatus.NOT_RESPONDED:
                return 5
            else:
                return 0
        else:
            if status == 1:
                return ResponseStatus.ORGANIZED
            elif status == 2:
                return ResponseStatus.TENTATIVE
            elif status == 3:
                return ResponseStatus.ACCEPTED
            elif status == 4:
                return ResponseStatus.DECLINED
            elif status == 5:
                return ResponseStatus.NOT_RESPONDED
            else:
                return ResponseStatus.NONE

    @staticmethod
    def parse_meeting_status(status):
        
        if isinstance(status, MeetingStatus): 
            if status == MeetingStatus.NON_MEETING:
                return 0
            elif status == MeetingStatus.MEETING:
                return 1
            elif status == MeetingStatus.RECEIVED:
                return 3
            elif status == MeetingStatus.CANCELED_ORGANIZER:
                return 4
            elif status == MeetingStatus.CANCELED:
                return 5
            else:
                return 0
        else:
            if status == 0:
                return MeetingStatus.NON_MEETING
            elif status == 1:
                return MeetingStatus.MEETING
            elif status == 3:
                return MeetingStatus.RECEIVED
            elif status == 4:
                return MeetingStatus.CANCELED_ORGANIZER
            elif status == 5:
                return MeetingStatus.CANCELED
            else:
                return MeetingStatus.NONE

    @staticmethod
    def parse_task_status(status):
        
        if isinstance(status, TaskStatus): 
            if status == TaskStatus.NOT_STARTED:
                return 0
            elif status == TaskStatus.IN_PROGRESS:
                return 1
            elif status == TaskStatus.COMPLETED:
                return 2
            elif status == TaskStatus.WAITING_ON_OTHERS:
                return 3
            elif status == TaskStatus.DEFERRED:
                return 4
            else:
                return 0
        else:
            if status == 0:
                return TaskStatus.NOT_STARTED
            elif status == 1:
                return TaskStatus.IN_PROGRESS
            elif status == 2:
                return TaskStatus.COMPLETED
            elif status == 3:
                return TaskStatus.WAITING_ON_OTHERS
            elif status == 4:
                return TaskStatus.DEFERRED
            else:
                return TaskStatus.NONE

    @staticmethod
    def parse_attachment_method(method):
        
        if isinstance(method, AttachmentMethod): 
            if method == AttachmentMethod.NO_ATTACHMENT:
                return 0
            elif method == AttachmentMethod.ATTACH_BY_VALUE:
                return 1
            elif method == AttachmentMethod.ATTACH_BY_REFERENCE:
                return 2
            elif method == AttachmentMethod.ATTACH_BY_REFERENCE_RESOLVE:
                return 3
            elif method == AttachmentMethod.ATTACH_BY_REFERENCE_ONLY:
                return 4
            elif method == AttachmentMethod.EMBEDDED_MESSAGE:
                return 5
            elif method == AttachmentMethod.OLE:
                return 6
            else:
                return 0
        else:
            if method == 0:
                return AttachmentMethod.NO_ATTACHMENT
            elif method == 1:
                return AttachmentMethod.ATTACH_BY_VALUE
            elif method == 2:
                return AttachmentMethod.ATTACH_BY_REFERENCE
            elif method == 3:
                return AttachmentMethod.ATTACH_BY_REFERENCE_RESOLVE
            elif method == 4:
                return AttachmentMethod.ATTACH_BY_REFERENCE_ONLY
            elif method == 5:
                return AttachmentMethod.EMBEDDED_MESSAGE
            elif method == 6:
                return AttachmentMethod.OLE
            else:
                return AttachmentMethod.NONE

    @staticmethod
    def parse_attachment_flags(flags):
        
        if isinstance(flags, AttachmentFlags): 
            if flags == AttachmentFlags.INVISIBLE_IN_HTML:
                return 1
            elif flags == AttachmentFlags.INVISIBLE_IN_RTF:
                return 2
            else:
                return 0
        else:
            if flags == 1:
                return AttachmentFlags.INVISIBLE_IN_HTML
            elif flags == 2:
                return AttachmentFlags.INVISIBLE_IN_RTF
            else:
                return AttachmentFlags.NONE

    @staticmethod
    def parse_property_type(tag):
        
        type_value = tag & 0xFFFF
        raw_type_value = type_value & 0x0FFF

        type = PropertyType.STRING

        if type_value & 0xF000 != 0: 

            if raw_type_value == 2:
                return PropertyType.MULTIPLE_INTEGER_16
            elif raw_type_value == 3:
                return PropertyType.MULTIPLE_INTEGER_32
            elif raw_type_value == 4:
                return PropertyType.MULTIPLE_FLOATING_32
            elif raw_type_value == 5:
                return PropertyType.MULTIPLE_FLOATING_64
            elif raw_type_value == 6:
                return PropertyType.MULTIPLE_CURRENCY
            elif raw_type_value == 7:
                return PropertyType.MULTIPLE_FLOATING_TIME
            elif raw_type_value == 0x14:
                return PropertyType.MULTIPLE_INTEGER_64
            elif raw_type_value == 0x1E:
                return PropertyType.MULTIPLE_STRING_8
            elif raw_type_value == 0x1F:
                return PropertyType.MULTIPLE_STRING
            elif raw_type_value == 0x40:
                return PropertyType.MULTIPLE_TIME
            elif raw_type_value == 0x48:
                return PropertyType.MULTIPLE_GUID
            elif raw_type_value == 0x102:
                return PropertyType.MULTIPLE_BINARY
            else:
                return PropertyType.MULTIPLE_STRING
        else:

            if raw_type_value == 2:
                return PropertyType.INTEGER_16
            elif raw_type_value == 3:
                return PropertyType.INTEGER_32
            elif raw_type_value == 4:
                return PropertyType.FLOATING_32
            elif raw_type_value == 5:
                return PropertyType.FLOATING_64
            elif raw_type_value == 6:
                return PropertyType.CURRENCY
            elif raw_type_value == 7:
                return PropertyType.FLOATING_TIME
            elif raw_type_value == 7:
                return PropertyType.ERROR_CODE
            elif raw_type_value == 0xB:
                return PropertyType.BOOLEAN
            elif raw_type_value == 0xD:
                return PropertyType.OBJECT
            elif raw_type_value == 0x14:
                return PropertyType.INTEGER_64
            elif raw_type_value == 0x1E:
                return PropertyType.STRING_8
            elif raw_type_value == 0x1F:
                return PropertyType.STRING
            elif raw_type_value == 0x40:
                return PropertyType.TIME
            elif raw_type_value == 0x48:
                return PropertyType.GUID
            elif raw_type_value == 0x102:
                return PropertyType.BINARY
            else:
                return PropertyType.STRING


class StandardPropertySet:
    MAPI = bytes([40, 3, 2, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    PUBLIC_STRINGS = bytes([41, 3, 2, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    INTERNET_HEADERS = bytes([134, 3, 2, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    APPOINTMENT = bytes([2, 32, 6, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    TASK = bytes([3, 32, 6, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    ADDRESS = bytes([4, 32, 6, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    COMMON = bytes([8, 32, 6, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    NOTE = bytes([14, 32, 6, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])
    JOURNAL = bytes([10, 32, 6, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])

class Sensitivity(Enum):
    PERSONAL = 1
    PRIVATE = 2
    CONFIDENTIAL = 3
    NONE = 0

class NamedPropertyType(Enum):
    NUMERICAL = 1
    STRING = 2

class Priority(Enum):
    LOW = 0xFFFFFFFF
    NORMAL = 0
    HIGH = 1
    NONE = 999

class MeetingStatus(Enum):
    NON_MEETING = 0
    MEETING = 1
    RECEIVED = 3
    CANCELED_ORGANIZER = 4
    CANCELED = 5
    NONE = -1

class LastVerbExecuted(Enum):
    REPLY_TO_SENDER = 102
    REPLY_TO_ALL = 103
    FORWARD = 104
    NONE = 0

class Importance(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    NONE = -1

class Gender(Enum):
    FEMALE = 1
    MALE = 2
    NONE = 0
    
class FlagStatus(Enum):
    COMPLETE = 1
    MARKED = 2
    NONE = 0

class FlagIcon(Enum):
    PURPLE = 1
    ORANGE = 2
    GREEN = 3
    YELLOW = 4
    BLUE = 5
    RED = 6
    NONE = 0

class DisplayType(Enum):
    MAIL_USER = 0
    DISTRIBUTION_LIST = 1
    FORUM = 2
    AGENT = 3
    ORGANIZATION = 4
    PRIVATE_DISTRIBUTION_LIST = 5
    REMOTE_MAIL_USER = 6
    FOLDER = 0x01000000
    FOLDER_LINK = 0x02000000
    FOLDER_SPECIAL = 0x04000000
    MODIFIABLE = 0x00010000
    GLOBAL_ADDRESS_BOOK = 0x00020000
    LOCAL_ADDRESS_BOOK = 0x00030000
    WIDE_AREA_NETWORK_ADDRESS_BOOK = 0x00040000
    NOT_SPECIFIC = 0x00050000
    NONE = -1

class DayOfWeek(Enum):
    SUNDAY = 0x00000000
    MONDAY = 0x00000001
    TUESDAY = 0x00000002
    WEDNESDAY = 0x00000003
    THURSDAY = 0x00000004
    FRIDAY = 0x00000005
    SATURDAY = 0x00000006
    NONE = -1

class DayOfWeekIndex(Enum):
    FIRST = 0x00000001
    SECOND = 0x00000002 
    THIRD = 0x00000003
    FOURTH = 0x00000004
    LAST = -1
    NONE = 0

class CalendarType(Enum):
    GREGORIAN = 0x0001
    GREGORIAN_US = 0x0002
    JAPANESE_EMPOROR_ERA = 0x0003
    TAIWAN = 0x0004
    KOREAN_TUNGUN_ERA = 0x0005
    HIJIRI = 0x0006
    THAI = 0x0007
    HEBREW_LUNAR = 0x0008
    GREGORIAN_MIDDLE_EAST_FRENCH = 0x0009
    GREGORIAN_ARABIC = 0x000A
    GREGORIAN_TRANSLITERATED_ENGLISH = 0x000B
    GREGORIAN_TRANSLITERATED_FRENCH = 0x000C
    JAPANESE_LUNAR = 0x000E
    CHINESE_LUNAR = 0x000F
    SAKA_ERA = 0x0010
    LUNAR_ETO_CHINESE = 0x0011
    LUNAR_ETO_KOREAN = 0x0012
    LUNAR_ROKUYOU = 0x0013
    KOREAN_LUNAR = 0x0014
    UM_AL_QURA = 0x0017
    NONE = 0

class BusyStatus(Enum):
    FREE = 0
    TENTATIVE = 1
    BUSY = 2
    OUT_OF_OFFICE = 3
    NONE = -1

class AttachmentMethod(Enum):
    NO_ATTACHMENT = 0
    ATTACH_BY_VALUE = 1
    ATTACH_BY_REFERENCE = 2
    ATTACH_BY_REFERENCE_RESOLVE = 3
    ATTACH_BY_REFERENCE_ONLY = 4
    EMBEDDED_MESSAGE = 5
    OLE = 6
    NONE = -1

class AttachmentFlags(Enum):
    INVISIBLE_IN_HTML = 1
    INVISIBLE_IN_RTF = 2
    NONE = 0

class MessageFlag(Enum):
    ASSOCIATED = 0x00000040
    FROM_ME = 0x00000020
    HAS_ATTACHMENT = 0x00000010
    NON_READ_REPORT_PENDING = 0x00000200
    ORIGIN_INTERNET = 0x00002000
    ORIGIN_MISC_EXTERNAL = 0x00008000
    ORIGIN_X400 = 0x00001000
    READ = 0x00000001
    RESEND = 0x00000080
    READ_REPORT_PENDING = 0x00000100
    SUBMIT = 0x00000004
    UNMODIFIED = 0x00000002
    UNSENT = 0x00000008

class NamedPropertyType(Enum):
    NUMERICAL = 1
    STRING = 2

class NoteColor(Enum):
    BLUE = 0
    GREEN = 1
    PINK = 2
    YELLOW = 3
    WHITE = 4
    NONE = -1

class ObjectType(Enum):
    MESSAGE_STORE = 1
    ADDRESS_BOOK = 2
    FOLDER = 3
    ADDRESS_BOOK_CONTAINER = 4
    MESSAGE = 5
    MAIL_USER = 6
    ATTACHMENT = 7
    DISTRIBUTION_LIST = 8
    PROFILE_SELECTION = 9
    STATUS = 10
    SESSION = 11
    FORM = 12
    NONE = 0

    
class PropertyType(Enum):
    INTEGER_16 = 1
    INTEGER_32 = 2
    FLOATING_32 = 3
    FLOATING_64 = 4
    CURRENCY = 5
    FLOATING_TIME = 6
    ERROR_CODE = 7
    BOOLEAN = 8
    INTEGER_64 = 9
    TIME = 10

    STRING = 11
    BINARY = 12
    STRING_8 = 13
    GUID = 14
    OBJECT = 15
    
    MULTIPLE_INTEGER_16 = 16
    MULTIPLE_INTEGER_32 = 17
    MULTIPLE_FLOATING_32 = 18
    MULTIPLE_FLOATING_64 = 19
    MULTIPLE_CURRENCY = 20
    MULTIPLE_FLOATING_TIME = 21
    MULTIPLE_INTEGER_64 = 22
    MULTIPLE_GUID = 23
    MULTIPLE_TIME = 24

    MULTIPLE_STRING = 25
    MULTIPLE_BINARY = 26
    MULTIPLE_STRING_8 = 27

class RecipientType(Enum):
    TO = 1
    CC = 2
    BCC = 3
    P1 = 0x10000000
    NONE = 0

class RecurrenceEndType(Enum):
    END_AFTER_DATE = 0x00002021
    END_AFTER_N_OCCURRENCES = 0x00002022
    NEVER_END = 0

class RecurrencePatternFrequency(Enum):
    DAILY = 0x200A
    WEEKLY = 0x200B
    MONTHLY = 0x200C
    YEARLY = 0x200D

class RecurrencePatternType(Enum):
    DAY = 0x0000
    WEEK = 0x0001
    MONTH = 0x0002
    MONTH_END = 0x0003
    MONTH_NTH = 0x0004
    HIJRI_MONTH = 0x200A
    HIJRI_MONTH_END = 0x200B
    HIJRI_MONTH_NTH = 0x200C

class RecurrenceType(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    MONTHLY_NTH = 4
    YEARLY = 5
    YEARLY_NTH = 6
    NONE = 0

class ResponseStatus(Enum):
    ORGANIZED = 1
    TENTATIVE = 2
    ACCEPTED = 3
    DECLINED = 4
    NOT_RESPONDED = 5
    NONE = 0

class SelectedMailingAddress(Enum):
    BUSSINESS = 1
    HOME = 2
    OTHER = 3
    NONE = 0

class StoreSupportMask(Enum):
    ANSI = 0x00020000
    ATTACHMENTS = 0x00000020
    CATEGORIZE = 0x00000400
    CREATE = 0x00000010
    HTML = 0x00010000
    ITEM_PROC = 0x00200000
    LOCAL_STORE = 0x00080000
    MODIFY = 0x00000008
    MULTI_VALUE_PROPERTIES = 0x00000200
    NOTIFY = 0x00000100
    OLE = 0x00000040
    PUBLIC_FOLDERS = 0x00004000
    PUSHER = 0x00800000
    READ_ONLY = 0x00000002
    RESTRICTIONS = 0x00001000
    RTF = 0x00000800
    SEARCH = 0x00000004
    SORT = 0x00002000
    SUBMIT = 0x00000080
    UNCOMPRESSED_RTF = 0x00008000
    UNICODE = 0x00040000

class TaskDelegationState(Enum):
    OWNED = 0
    OWN_NEW = 1
    ACCEPTED = 2
    DECLINED = 3
    NO_MATCH = 4
    NONE = -1

class TaskOwnership(Enum):
    NEW = 0
    DELEGATED = 1
    OWN = 2
    NONE = -1

class TaskStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    WAITING_ON_OTHERS = 3
    DEFERRED = 4
    NONE = -1

class CompoundFile:

    def __init__(self, file_path = None, buffer = None):
        self.cjni_p______ = Header()
        self.__el__s__b_y = RootDirectoryEntry()

        if file_path is not None:
            f = open(file_path, 'rb')
            buffer = f.read()
            self.jo__bob__g__(buffer)
            f.close()

        elif buffer != None:
            self.jo__bob__g__(buffer)

    def jo__bob__g__(self, __o_yqq_m_og):
        self.cjni_p______ = Header(__o_yqq_m_og)
        
        i_g__vecijb_ = self._ayb____d__c(__o_yqq_m_og)
        
        _fa__l___moi = self.__tbikvs_aye(__o_yqq_m_og, i_g__vecijb_) 

        if self.header.first_mini_fat_sector != 0xFFFFFFFE:
            ___wsi_ni___ = self._jhe_h_som_o(__o_yqq_m_og, _fa__l___moi)

        xpd_h_q___oc = []
    
        z_k____cv___ = self.header.first_directory_sector
        xpd_h_q___oc.append(z_k____cv___)

        while True:
            z_k____cv___ = _fa__l___moi[z_k____cv___]

            if z_k____cv___ != 0xFFFFFFFE:
                xpd_h_q___oc.append(z_k____cv___)
            else:
                break

        d_ln___ud__v = bytearray()

        for i in range(len(xpd_h_q___oc)):
            _e_hl_yyhb__ = xpd_h_q___oc[i]
            k_ymh___l__l = _e_hl_yyhb__ * self.header.sector_size + self.header.sector_size

            __fyrzu_____ = __o_yqq_m_og[k_ymh___l__l: k_ymh___l__l + self.header.sector_size]
            k_ymh___l__l += self.header.sector_size

            d_ln___ud__v += bytearray(__fyrzu_____)
        
        self.__el__s__b_y = DirectoryEntry.parse(bytes(d_ln___ud__v), 0)

        n_b__sfzn___ = {}

        n_b__sfzn___[0] = self.__el__s__b_y

        if (self.__el__s__b_y.child_sid != 0xFFFFFFFF):
            
            k_ymh___l__l = self.__el__s__b_y.child_sid * 128
            __ay___pl___ = DirectoryEntry.parse(bytes(d_ln___ud__v), k_ymh___l__l)

            n_b__sfzn___[self.__el__s__b_y.child_sid] = __ay___pl___
                
            self.__el__s__b_y.directory_entries.append(__ay___pl___)
            __ay___pl___.parent = self.__el__s__b_y

            wbe____w_r__  = []
            _r_zo_at__y_ = []
            ___uv____jk_ = []

            wbe____w_r__.append(__ay___pl___)
            _r_zo_at__y_.append(__ay___pl___)
            ___uv____jk_.append(__ay___pl___)

            while (len(wbe____w_r__) > 0 or len(_r_zo_at__y_) > 0 or len(___uv____jk_) > 0 ):
                
                if (len(wbe____w_r__) > 0):
                    ________ill_ = wbe____w_r__.pop()

                    if (________ill_.left_sibling_sid != 0xFFFFFFFF and ________ill_.left_sibling_sid not in n_b__sfzn___):
                        k_ymh___l__l = ________ill_.left_sibling_sid * 128
                        __ay___pl___ = DirectoryEntry.parse(bytes(d_ln___ud__v), k_ymh___l__l)

                        n_b__sfzn___[________ill_.left_sibling_sid] = __ay___pl___
                        
                        ________ill_.parent.directory_entries.append(__ay___pl___)
                        __ay___pl___.parent = ________ill_.parent

                        wbe____w_r__.append(__ay___pl___)
                        _r_zo_at__y_.append(__ay___pl___)
                        ___uv____jk_.append(__ay___pl___)

                        continue

                if (len(_r_zo_at__y_) > 0):
                    ________ill_ = _r_zo_at__y_.pop()

                    if (________ill_.right_sibling_sid != 0xFFFFFFFF and ________ill_.right_sibling_sid not in n_b__sfzn___):
                        k_ymh___l__l = ________ill_.right_sibling_sid * 128
                        __ay___pl___ = DirectoryEntry.parse(bytes(d_ln___ud__v), k_ymh___l__l)

                        n_b__sfzn___[________ill_.right_sibling_sid] = __ay___pl___
                        
                        ________ill_.parent.directory_entries.append(__ay___pl___)
                        __ay___pl___.parent = ________ill_.parent

                        wbe____w_r__.append(__ay___pl___)
                        _r_zo_at__y_.append(__ay___pl___)
                        ___uv____jk_.append(__ay___pl___)

                        continue

                if (len(___uv____jk_) > 0):
                    ________ill_ = ___uv____jk_.pop()

                    if (________ill_.child_sid != 0xFFFFFFFF and ________ill_.child_sid not in n_b__sfzn___):
                        k_ymh___l__l = ________ill_.child_sid * 128
                        __ay___pl___ = DirectoryEntry.parse(bytes(d_ln___ud__v), k_ymh___l__l)

                        n_b__sfzn___[________ill_.child_sid] = __ay___pl___
                        
                        ________ill_.directory_entries.append(__ay___pl___)
                        __ay___pl___.parent = ________ill_

                        wbe____w_r__.append(__ay___pl___)
                        _r_zo_at__y_.append(__ay___pl___)
                        ___uv____jk_.append(__ay___pl___)

                        continue
           
            ______y_vx__ = []
            
            for _n_r__rwuf_e in n_b__sfzn___.values():
                
                if (_n_r__rwuf_e is self.__el__s__b_y):
                    ______y_vx__.insert(0, _n_r__rwuf_e)
                else:
                    ______y_vx__.append(_n_r__rwuf_e)

            qq_q___iwxz_ = bytearray()

            for i in range(len(______y_vx__)):
                _eokn___n_g_ = ______y_vx__[i]

                if(_eokn___n_g_.type is not DirectoryEntryType.STORAGE):
                    if(_eokn___n_g_.type is not DirectoryEntryType.ROOT and _eokn___n_g_.size > 0 and _eokn___n_g_.size < self.header.mini_stream_max_size):
                        ______o__aes = []

                        jnfz_gxo_r__ = _eokn___n_g_.start_sector
                        ______o__aes.append(jnfz_gxo_r__)

                        while True:
                            jnfz_gxo_r__ = ___wsi_ni___[jnfz_gxo_r__]

                            if (jnfz_gxo_r__ != 0xFFFFFFFC and jnfz_gxo_r__ != 0xFFFFFFFD and jnfz_gxo_r__ != 0xFFFFFFFE and jnfz_gxo_r__ != 0xFFFFFFFF and jnfz_gxo_r__ != ___wsi_ni___[jnfz_gxo_r__]):
                                ______o__aes.append(jnfz_gxo_r__)
                            else:
                                break

                        urdcske_wvlq = bytearray()

                        for j in range(len(______o__aes)):
                            ___nd_l_____ = ______o__aes[j]
                            k_ymh___l__l = ___nd_l_____ * 64

                            __fyrzu_____ = qq_q___iwxz_[k_ymh___l__l: k_ymh___l__l + 64]
                            k_ymh___l__l += 64

                            urdcske_wvlq += __fyrzu_____

                        __cyk_pl____ = min(len(urdcske_wvlq), _eokn___n_g_.size)
                        _eokn___n_g_.buffer = urdcske_wvlq[0: __cyk_pl____]

                    elif (_eokn___n_g_.size > 0):
                        ______o__aes = []

                        jnfz_gxo_r__ = _eokn___n_g_.start_sector
                        ______o__aes.append(jnfz_gxo_r__)

                        while True:
                            jnfz_gxo_r__ = _fa__l___moi[jnfz_gxo_r__]

                            if (jnfz_gxo_r__ != 0xFFFFFFFC and jnfz_gxo_r__ != 0xFFFFFFFD and jnfz_gxo_r__ != 0xFFFFFFFE and jnfz_gxo_r__ != 0xFFFFFFFF and jnfz_gxo_r__ != _fa__l___moi[jnfz_gxo_r__]):
                                ______o__aes.append(jnfz_gxo_r__)
                            else:
                                break

                        urdcske_wvlq = bytearray()

                        for j in range(len(______o__aes)):
                            ___nd_l_____ = ______o__aes[j]
                            k_ymh___l__l = ___nd_l_____ * self.header.sector_size + self.header.sector_size

                            __fyrzu_____ = __o_yqq_m_og[k_ymh___l__l: k_ymh___l__l + self.header.sector_size]
                            k_ymh___l__l += self.header.sector_size

                            urdcske_wvlq += __fyrzu_____

                        __cyk_pl____ = min(len(urdcske_wvlq), _eokn___n_g_.size)
                        _eokn___n_g_.buffer = urdcske_wvlq[0: __cyk_pl____]

                        if (_eokn___n_g_ is self.__el__s__b_y and self.__el__s__b_y.buffer is not None):
                            qq_q___iwxz_ += self.__el__s__b_y.buffer
                        
            
    def _jhe_h_som_o(self, __o_yqq_m_og, _fa__l___moi):

        _n___v_b_lj_ = int(self.header.sector_size / 4)
        ___wsi_ni___ = [0] * self.header.mini_fat_sector_count * _n___v_b_lj_
        _e___f__hrg_ = []

        q____lhtb_b_ = self.header.first_mini_fat_sector
        _e___f__hrg_.append(q____lhtb_b_)

        while True:
            q____lhtb_b_ = _fa__l___moi[q____lhtb_b_]

            if q____lhtb_b_ != 0xFFFFFFFE:
                _e___f__hrg_.append(q____lhtb_b_)
            else:
                break

        __e____z_ew_ = 0

        for i in range(len(_e___f__hrg_)):
            k_ymh___l__l = _e___f__hrg_[i] * self.header.sector_size + self.header.sector_size

            for _ in range(_n___v_b_lj_):
                ___wsi_ni___[__e____z_ew_] = int.from_bytes(__o_yqq_m_og[k_ymh___l__l: k_ymh___l__l + 4], "little")
                k_ymh___l__l += 4
                __e____z_ew_ += 1

        return ___wsi_ni___

    def _ayb____d__c(self, __o_yqq_m_og):

        if self.header.fat_sector_count <= 109:

            i_g__vecijb_ = [0] * self.header.fat_sector_count
            
            for i in range(self.header.fat_sector_count):
                i_g__vecijb_[i] = self.header.difat[i]

            return i_g__vecijb_

        else:
            _n___v_b_lj_ = int(self.header.sector_size / 4)
            tk_v_ahe_k_l = [0] * _n___v_b_lj_
            i_g__vecijb_ = [0] * self.header.fat_sector_count 

            for i in range(109):
                i_g__vecijb_[i] = self.header.difat[i]

            k_ymh___l__l = self.header.first_difat_sector * self.header.sector_size + self.header.sector_size
            __e____z_ew_ = 109

            while True:

                for i in range(_n___v_b_lj_):
                    tk_v_ahe_k_l[i] = int.from_bytes(__o_yqq_m_og[k_ymh___l__l: k_ymh___l__l + 4], "little")
                    k_ymh___l__l += 4

                for i in range(_n___v_b_lj_ - 1):
                    if tk_v_ahe_k_l[i] != 0xFFFFFFFF and __e____z_ew_ < len(i_g__vecijb_):
                        i_g__vecijb_[__e____z_ew_] = tk_v_ahe_k_l[i]
                        __e____z_ew_ += 1

                if tk_v_ahe_k_l[_n___v_b_lj_ - 1] != 0xFFFFFFFE and __e____z_ew_ < len(i_g__vecijb_):
                    k_ymh___l__l = tk_v_ahe_k_l[_n___v_b_lj_ - 1] * self.header.sector_size + self.header.sector_size
                else:
                    break

            return i_g__vecijb_

    def __tbikvs_aye(self, __o_yqq_m_og, i_g__vecijb_):

        _n___v_b_lj_ = int(self.header.sector_size / 4)
        _fa__l___moi = [0] * self.header.fat_sector_count * _n___v_b_lj_
        __e____z_ew_ = 0

        for i in range(len(i_g__vecijb_)):
            k_ymh___l__l = i_g__vecijb_[i] * self.header.sector_size + self.header.sector_size

            for _ in range(_n___v_b_lj_):
                _fa__l___moi[__e____z_ew_] = int.from_bytes(__o_yqq_m_og[k_ymh___l__l: k_ymh___l__l + 4], "little")
                __e____z_ew_ += 1
                k_ymh___l__l += 4

        return _fa__l___moi

    def ___zp_____o_(self):

        _a_etpx_gt_j = datetime.datetime.now()

        _ux__oa_sw__ = [] 
        _fa__l___moi = [] 
        ___wsi_ni___ = [] 

        _l_s__l_bjn_ = 0xFFFFFFFE
        _vm______z_f = 0xFFFFFFFE
        _rgz____m__k = 0

        ____p_o_e_v_ = bytearray()

        self.__el__s__b_y.color = Color.RED
        self.__el__s__b_y.type = DirectoryEntryType.ROOT
        self.__el__s__b_y.buffer = None
        self.__el__s__b_y.left_sibling_sid = 0xFFFFFFFF
        self.__el__s__b_y.right_sibling_sid = 0xFFFFFFFF           
        self.__el__s__b_y.created_time = datetime.datetime(1,1,1)
        self.__el__s__b_y.last_modified_time = datetime.datetime(1,1,1)
        self.__el__s__b_y.size = 0
        self.__el__s__b_y.start_sector = 0

        _ux__oa_sw__.append(self.__el__s__b_y)
        self.__np__of____(self.__el__s__b_y, _ux__oa_sw__, _a_etpx_gt_j)
                
        _hruar_b_mt_ = bytearray()
        qq_q___iwxz_ = bytearray()

        for i in range(len(_ux__oa_sw__) - 1, -1, -1):
            _eokn___n_g_ = _ux__oa_sw__[i]

            if (_eokn___n_g_.buffer is not None):
                _eokn___n_g_.size = len(_eokn___n_g_.buffer)
            else:
                _eokn___n_g_.size = 0

            if (i == 0 and len(qq_q___iwxz_) > 0):
                _eokn___n_g_.buffer = bytes(qq_q___iwxz_)
                _eokn___n_g_.size = len(_eokn___n_g_.buffer)
                      

            if (i > 0 and _eokn___n_g_.size > 0 and _eokn___n_g_.size < self.header.mini_stream_max_size):
                _eokn___n_g_.start_sector = len(___wsi_ni___)

                for ____m_fe__fr in range(0, len(_eokn___n_g_.buffer), self.header.mini_sector_size):
                    _a_g__sq__a_ = bytearray(self.header.mini_sector_size)                    
                    __n__h_e__fc = len(_a_g__sq__a_)

                    if (len(_eokn___n_g_.buffer) < ____m_fe__fr + self.header.mini_sector_size):
                        __n__h_e__fc = len(_eokn___n_g_.buffer) - ____m_fe__fr
    
                    _a_g__sq__a_[0: __n__h_e__fc] = _eokn___n_g_.buffer[____m_fe__fr: ____m_fe__fr + __n__h_e__fc]
                    qq_q___iwxz_ += _a_g__sq__a_

                    if (____m_fe__fr + self.header.mini_sector_size < len(_eokn___n_g_.buffer)):
                        ___wsi_ni___.append(len(___wsi_ni___) + 1)
                    else:
                        ___wsi_ni___.append(0xFFFFFFFE)

            elif (i > 0 and _eokn___n_g_.size > 0 and _eokn___n_g_.size >= self.header.mini_stream_max_size):
                _eokn___n_g_.start_sector = len(_fa__l___moi)

                for ____m_fe__fr in range(0, len(_eokn___n_g_.buffer), self.header.sector_size):
                    _a_g__sq__a_ = bytearray(self.header.sector_size)                    
                    __n__h_e__fc = len(_a_g__sq__a_)

                    if (len(_eokn___n_g_.buffer) < ____m_fe__fr + self.header.sector_size):
                        __n__h_e__fc = len(_eokn___n_g_.buffer) - ____m_fe__fr

                    _a_g__sq__a_[0: __n__h_e__fc] = _eokn___n_g_.buffer[____m_fe__fr: ____m_fe__fr + __n__h_e__fc]
                    _hruar_b_mt_ += _a_g__sq__a_

                    if (____m_fe__fr + self.header.sector_size < len(_eokn___n_g_.buffer)):
                        _fa__l___moi.append(len(_fa__l___moi) + 1)
                    else:
                        _fa__l___moi.append(0xFFFFFFFE)

        ______w_aap_ = self.header.sector_size / self.header.mini_sector_size
        dyy______s__ = 0
        x__v__p_d_fv = False

        _vm______z_f = len(_fa__l___moi)

        if (len(qq_q___iwxz_) > 0):
            __g_w__jn__i = bytes(qq_q___iwxz_)
            _a_g__sq__a_ = bytearray(self.header.sector_size)

            for ____m_fe__fr in range(0, len(__g_w__jn__i), self.header.mini_sector_size):
                __n__h_e__fc = self.header.mini_sector_size

                if (len(__g_w__jn__i) < ____m_fe__fr + self.header.mini_sector_size):
                    __n__h_e__fc = len(qq_q___iwxz_) - ____m_fe__fr

                _a_g__sq__a_[dyy______s__ * self.header.mini_sector_size: dyy______s__ * self.header.mini_sector_size + __n__h_e__fc] = __g_w__jn__i[____m_fe__fr: ____m_fe__fr + __n__h_e__fc]
                dyy______s__ += 1

                if (____m_fe__fr + self.header.mini_sector_size >= len(__g_w__jn__i)):
                    x__v__p_d_fv = True

                if (x__v__p_d_fv or dyy______s__ == ______w_aap_):
                    dyy______s__ = 0
                    _hruar_b_mt_ += bytes(_a_g__sq__a_)

                    if (not x__v__p_d_fv):
                        _fa__l___moi.append(len(_fa__l___moi) + 1)
                    else:
                        _fa__l___moi.append(0xFFFFFFFE)


            _pij_o___l__ = int(self.header.sector_size / 4)
            _l_s__l_bjn_ = len(_fa__l___moi)

            for i in range(0, len(___wsi_ni___), _pij_o___l__):
                b__fj____hf_ = bytearray(self.header.sector_size)

                for j in range(_pij_o___l__):
                    if (i + j < len(___wsi_ni___)):
                        ______f__u__ = ___wsi_ni___[i + j]
                        _e__v_______ = ______f__u__.to_bytes(4, "little")
                        b__fj____hf_[j * 4: j * 4 + 4] = _e__v_______[0:4]
                    else:
                        _e__v_______ = 0xFFFFFFFF.to_bytes(4, "little")
                        b__fj____hf_[j * 4: j * 4 + 4] = _e__v_______[0:4]

                _hruar_b_mt_ += bytes(b__fj____hf_)
                _rgz____m__k += 1

                if (i + _pij_o___l__ < len(___wsi_ni___)):
                    _fa__l___moi.append(len(_fa__l___moi) + 1)
                else:
                    _fa__l___moi.append(0xFFFFFFFE) 
        
        ____p_o_e_v_ += bytes(_hruar_b_mt_)

        self.header.first_directory_sector = len(_fa__l___moi)

        _lo__b___ii_ = 0

        _xd__rihbo_z = int(self.header.sector_size / 128)

        for i in range (0, len(_ux__oa_sw__), _xd__rihbo_z):

            if (_ux__oa_sw__[i] is self.__el__s__b_y and _vm______z_f != 0xFFFFFFFE):
                    self.__el__s__b_y.start_sector = _vm______z_f

            z_k____cv___ = bytearray(self.header.sector_size)

            for j in range(_xd__rihbo_z):

                if (i + j < len(_ux__oa_sw__)):
                    _eokn___n_g_ = _ux__oa_sw__[i + j]
                    z_k____cv___[j * 128: j * 128 + 128] = _eokn___n_g_.to_bytes()

            ____p_o_e_v_ += bytes(z_k____cv___)
            _lo__b___ii_ += 1

            if (i + _xd__rihbo_z < len(_ux__oa_sw__)):
                _fa__l___moi.append(len(_fa__l___moi) + 1)
            else:
                _fa__l___moi.append(0xFFFFFFFE)

        if (self.header.major_version == 4):
            self.header.directory_sector_count = _lo__b___ii_


        _u_x_ra_h_sp = int(self.header.sector_size / 4)
        __q___of____ = int(len(_fa__l___moi) / _u_x_ra_h_sp)

        if (__q___of____ * _u_x_ra_h_sp < len(_fa__l___moi)):
            __q___of____ = __q___of____ + 1

        __q___of____ = int((len(_fa__l___moi) + __q___of____) / _u_x_ra_h_sp)

        if (__q___of____ * _u_x_ra_h_sp < len(_fa__l___moi) + __q___of____):
            __q___of____ = __q___of____ + 1

        ___z_rfsfm__ = int((__q___of____ - 109) / (_u_x_ra_h_sp - 1))

        if (___z_rfsfm__ * _u_x_ra_h_sp < (__q___of____ - 109)):
            ___z_rfsfm__ = ___z_rfsfm__ + 1

        self.header.fat_sector_count = __q___of____
        
        nymw__nkx__w = []
        _v__e__bakzg = []

        for i in range(__q___of____):
            _fa__l___moi.append(0xFFFFFFFD) 
            k_ymh___l__l = len(_fa__l___moi) - 1

            if (i < 109):
                nymw__nkx__w.append(k_ymh___l__l)
            else:
                _v__e__bakzg.append(k_ymh___l__l)
 

        for i in range(___z_rfsfm__):
            _fa__l___moi.append(0xFFFFFFFC)
        
        for i in range(0, len(_fa__l___moi), _u_x_ra_h_sp):

            wvcn_iy____g = bytearray(self.header.sector_size)

            for j in range(_u_x_ra_h_sp):

                if ((i + j) < len(_fa__l___moi)):
                    wvcn_iy____g[j * 4: j * 4 + 4] = _fa__l___moi[i + j].to_bytes(4, "little")
                else:
                    wvcn_iy____g[j * 4: j * 4 + 4] = 0xFFFFFFFF.to_bytes(4, "little")

            ____p_o_e_v_ += wvcn_iy____g

        if (___z_rfsfm__ > 0):
            self.header.first_difat_sector = int(len(____p_o_e_v_) / self.header.sector_size)
        else:
            self.header.first_difat_sector = 0xFFFFFFFE

        self.header.difat_sector_count = ___z_rfsfm__

        for i in range(len(nymw__nkx__w)):
            self.header.difat[i] = nymw__nkx__w[i]
  
        for i in range(len(nymw__nkx__w), 109, 1):
            self.header.difat[i] = 0xFFFFFFFF

        ___x____dd_c = 1

        for i in range(0, len(_v__e__bakzg), _u_x_ra_h_sp - 1):
            wvcn_iy____g = bytearray(self.header.sector_size)

            for j in range(_u_x_ra_h_sp - 1):

                if (i + j < len(_v__e__bakzg)):
                    wvcn_iy____g[j * 4: j * 4 + 4] = _v__e__bakzg[i + j].to_bytes(4, "little")
                else:
                    wvcn_iy____g[j * 4: j * 4 + 4] = 0xFFFFFFFF.to_bytes(4, "little")

            if (i + (_u_x_ra_h_sp - 1) < len(_v__e__bakzg)):
                p__c_u_wdic_ = int.to_bytes(self.header.first_difat_sector + ___x____dd_c, 4, "little")
                wvcn_iy____g[(_u_x_ra_h_sp - 1) * 4: (_u_x_ra_h_sp - 1) * 4 + 4] = p__c_u_wdic_
                ___x____dd_c += 1
            else:
                wvcn_iy____g[(_u_x_ra_h_sp - 1) * 4: (_u_x_ra_h_sp - 1) * 4 + 4] = 0xFFFFFFFE.to_bytes(4, "little")

            ____p_o_e_v_ += wvcn_iy____g


        self.header.first_mini_fat_sector = _l_s__l_bjn_
        self.header.mini_fat_sector_count = _rgz____m__k

        ____p_o_e_v_ = self.header.to_bytes() + ____p_o_e_v_

        return bytes(____p_o_e_v_)

    def __np__of____(self, ___g__on___b, _ux__oa_sw__, _a_etpx_gt_j):
        if (len(___g__on___b.directory_entries) > 0):
            ___g__on___b.directory_entries.sort()

            ___iaz_g____ = int(len(___g__on___b.directory_entries) / 2)
            _zq_b__i___u = ___g__on___b.directory_entries[___iaz_g____]

            if (___g__on___b.color == Color.BLACK):
                _zq_b__i___u.color = Color.RED
            else:
                _zq_b__i___u.color = Color.BLACK
                
            _zq_b__i___u.created_time = _zq_b__i___u.last_modified_time = _a_etpx_gt_j

            if (_zq_b__i___u.buffer is not None):
                _zq_b__i___u.size = len(_zq_b__i___u.buffer)
            else:
                _zq_b__i___u.size = 0

            _zq_b__i___u.start_sector = 0

            _zq_b__i___u.left_sibling_sid = 0xFFFFFFFF
            _zq_b__i___u.right_sibling_sid = 0xFFFFFFFF
            _zq_b__i___u.child_sid = 0xFFFFFFFF

            _ux__oa_sw__.append(_zq_b__i___u)
            ___g__on___b.child_sid = len(_ux__oa_sw__) - 1

            _c_jp__d__o_ = _zq_b__i___u

            for l in range(___iaz_g____ - 1, -1, -1):
                _u_oz___n_la = ___g__on___b.directory_entries[l]

                if (___g__on___b.color == Color.BLACK):
                    _u_oz___n_la.color = Color.RED
                else:
                    _u_oz___n_la.color = Color.BLACK

                _u_oz___n_la.created_time = _u_oz___n_la.last_modified_time = _a_etpx_gt_j

                if (_u_oz___n_la.buffer is not None):
                    _u_oz___n_la.size = len(_u_oz___n_la.buffer)
                else:
                    _u_oz___n_la.size = 0

                _u_oz___n_la.left_sibling_sid = 0xFFFFFFFF
                _u_oz___n_la.right_sibling_sid = 0xFFFFFFFF
                _u_oz___n_la.child_sid = 0xFFFFFFFF

                _ux__oa_sw__.append(_u_oz___n_la)
                _c_jp__d__o_.left_sibling_sid = len(_ux__oa_sw__) - 1
                _c_jp__d__o_ = _u_oz___n_la

                if (isinstance(_u_oz___n_la, Storage)):
                    self.__np__of____(_u_oz___n_la, _ux__oa_sw__, _a_etpx_gt_j)

            _c_jp__d__o_ = _zq_b__i___u

            for r in range(___iaz_g____ + 1, len(___g__on___b.directory_entries)):
                k_p___f_____ = ___g__on___b.directory_entries[r]

                if (___g__on___b.color == Color.BLACK):
                    k_p___f_____.color = Color.RED
                else:
                    k_p___f_____.color = Color.BLACK

                k_p___f_____.created_time = k_p___f_____.last_modified_time = _a_etpx_gt_j

                if (k_p___f_____.buffer is not None):
                    k_p___f_____.size = len(k_p___f_____.buffer)
                else:
                    k_p___f_____.size = 0

                k_p___f_____.left_sibling_sid = 0xFFFFFFFF
                k_p___f_____.right_sibling_sid = 0xFFFFFFFF
                k_p___f_____.child_sid = 0xFFFFFFFF

                _ux__oa_sw__.append(k_p___f_____)
                _c_jp__d__o_.right_sibling_sid = len(_ux__oa_sw__) - 1
                _c_jp__d__o_ = k_p___f_____

                if (isinstance(k_p___f_____, Storage)):
                    self.__np__of____(k_p___f_____, _ux__oa_sw__, _a_etpx_gt_j)
           
            if (isinstance(_zq_b__i___u, Storage)):
                self.__np__of____(_zq_b__i___u, _ux__oa_sw__, _a_etpx_gt_j)

    def to_bytes(self):
        return self.___zp_____o_()

    def save(self, file_path):

        if(file_path is not None):
            file = open(file_path, "wb")
            file.write(self.to_bytes())
            file.close

    @property
    def header(self):
        return self.cjni_p______

    @property
    def root(self):
        return self.__el__s__b_y


class DirectoryEntry:

    def __init__(self):
        self.__name = None
        self._j___xwggn_w = DirectoryEntryType.INVALID
        self._x_x_i_qs_g_ = Color.BLACK
        self.py__r___c_c_ = 0
        self.y__r____kw__ = 0
        self.__bts____p_g = 0
        self.oo_e_gmn__ru = bytes(16)
        self.__iy__fox__k = 0
        self.g_r__z_jm_x_ = datetime.datetime(1,1,1)
        self.o___gqz_ln__ = datetime.datetime(1,1,1)
        self._fn__xr_wjhc = 0
        self._kv_js____l_ = 0
        self.s____oqem__x = 0
        self.iy__________ = None
        self.po__g__o____ = []
        self.___jr_q__w_s = None 

    def __eq__(self, other):
        return self._bnvfa_yici_(other)

    def __lt__(self, other):
        return self._bnvfa_yici_(other)

    def __gt__(self, other):
        return self._bnvfa_yici_(other)

    def __repr__(self):
        return "%s" % (self.name)

    def __str__(self):
        return "%s" % (self.name)

    def _bnvfa_yici_(self, other):

        if other is not None:
            if (len(self.name) == len(other.name)):

                for i in range(len(self.name)):            
                    if(ord(self.name[i]) < ord(other.name[i])):
                        return True
                    elif (ord(self.name[i]) > ord(other.name[i])):
                        return False
                        
            elif (len(self.name) < len(other.name)):
                return True

        return False

    @staticmethod    
    def parse(buffer, position):
        
        __i_h__stg_x  = buffer[position: position + 64] 
        position += 64

        _b___h_y_z__ = int.from_bytes(buffer[position: position + 2], "little")
        position += 2

        _h__v_yn__yl = None

        if (_b___h_y_z__ > 1):
            __x_z_b_xu__ = __i_h__stg_x[0: _b___h_y_z__ - 2]
            _h__v_yn__yl = __x_z_b_xu__.decode('utf-16-le')

        type_value = int.from_bytes(buffer[position: position + 1], "little")
        position += 1

        type = DirectoryEntryType(type_value)

        color_value = int.from_bytes(buffer[position: position + 1], "little")
        position += 1

        color = Color(color_value)

        left_sibling_sid = int.from_bytes(buffer[position: position + 4], "little")
        position += 4
        
        right_sibling_sid = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        child_sid = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        class_id = buffer[position: position + 16]
        position += 16

        user_flags = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        osxq__miv__g = int.from_bytes(buffer[position: position + 4], "little")
        position += 4
        
        hp___h__uc__ = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        u____v__z_u_ = datetime.datetime(1,1,1)
        ob_oy_a_thob = datetime.datetime(1,1,1)

        if (hp___h__uc__ > 0):
            i_x____hz_to = osxq__miv__g + (hp___h__uc__ << 32)
            j____h_x_v_h = datetime.datetime(1601,1,1)   

            try:    
                u____v__z_u_ = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                u____v__z_u_ = DirectoryEntry._j__y____u__(u____v__z_u_)
            except:
                pass

        _z__k_cm_p_j = int.from_bytes(buffer[position: position + 4], "little")
        position += 4
        
        m____ol_i_v_ = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        if (m____ol_i_v_ > 0):
            i_x____hz_to = _z__k_cm_p_j + (m____ol_i_v_ << 32)
            j____h_x_v_h = datetime.datetime(1601,1,1)

            try:    
                ob_oy_a_thob = j____h_x_v_h + datetime.timedelta(milliseconds = i_x____hz_to / 10000)               
                ob_oy_a_thob = DirectoryEntry._j__y____u__(last_modified_time)
            except:
                pass

        start_sector = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        size = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        if (type == DirectoryEntryType.ROOT):            
            entry = RootDirectoryEntry()
            entry.__name = _h__v_yn__yl
            entry._j___xwggn_w = DirectoryEntryType.ROOT
            entry._x_x_i_qs_g_ = color
            entry.py__r___c_c_ = left_sibling_sid
            entry.y__r____kw__ = right_sibling_sid
            entry.__bts____p_g = child_sid
            entry.oo_e_gmn__ru = class_id
            entry.__iy__fox__k = user_flags
            entry.g_r__z_jm_x_ = u____v__z_u_
            entry.o___gqz_ln__ = ob_oy_a_thob
            entry._fn__xr_wjhc = start_sector
            entry._kv_js____l_ = size
            entry.s____oqem__x = 0
            entry.iy__________ = None
            entry.po__g__o____ = []
            entry.___jr_q__w_s = None
        
            return entry
        elif (type == DirectoryEntryType.STREAM):
            entry = Stream()
            entry.__name = _h__v_yn__yl
            entry._j___xwggn_w = DirectoryEntryType.STREAM
            entry._x_x_i_qs_g_ = color
            entry.py__r___c_c_ = left_sibling_sid
            entry.y__r____kw__ = right_sibling_sid
            entry.__bts____p_g = child_sid
            entry.oo_e_gmn__ru = class_id
            entry.__iy__fox__k = user_flags
            entry.g_r__z_jm_x_ = u____v__z_u_
            entry.o___gqz_ln__ = ob_oy_a_thob
            entry._fn__xr_wjhc = start_sector
            entry._kv_js____l_ = size
            entry.s____oqem__x = 0
            entry.iy__________ = None
            entry.po__g__o____ = []
            entry.___jr_q__w_s = None
        
            return entry                        
        elif (type == DirectoryEntryType.STORAGE):
            entry = Storage()
            entry.__name = _h__v_yn__yl
            entry._j___xwggn_w = DirectoryEntryType.STORAGE
            entry._x_x_i_qs_g_ = color
            entry.py__r___c_c_ = left_sibling_sid
            entry.y__r____kw__ = right_sibling_sid
            entry.__bts____p_g = child_sid
            entry.oo_e_gmn__ru = class_id
            entry.__iy__fox__k = user_flags
            entry.g_r__z_jm_x_ = u____v__z_u_
            entry.o___gqz_ln__ = ob_oy_a_thob
            entry._fn__xr_wjhc = start_sector
            entry._kv_js____l_ = size
            entry.s____oqem__x = 0
            entry.iy__________ = None
            entry.po__g__o____ = []
            entry.___jr_q__w_s = None
        
            return entry
        else:
            entry = Storage()
            entry.__name = _h__v_yn__yl
            entry._j___xwggn_w = DirectoryEntryType.INVALID
            entry._x_x_i_qs_g_ = color
            entry.py__r___c_c_ = left_sibling_sid
            entry.y__r____kw__ = right_sibling_sid
            entry.__bts____p_g = child_sid
            entry.oo_e_gmn__ru = class_id
            entry.__iy__fox__k = user_flags
            entry.g_r__z_jm_x_ = u____v__z_u_
            entry.o___gqz_ln__ = ob_oy_a_thob
            entry._fn__xr_wjhc = start_sector
            entry._kv_js____l_ = size
            entry.s____oqem__x = 0
            entry.iy__________ = None
            entry.po__g__o____ = []
            entry.___jr_q__w_s = None
        
            return entry

    def to_bytes(self):

        buffer = bytearray(128)
        position = 0

        unicode_name_buffer = self.__name.encode('utf-16-le')

        buffer[0: len(unicode_name_buffer)] = unicode_name_buffer
        position += 64

        buffer[position: position + 2] = int.to_bytes((len(self.__name) + 1) * 2, 2, "little")
        position += 2
        
        buffer[position: position + 1] = int.to_bytes(self._j___xwggn_w.value, 1, "little")
        position += 1

        buffer[position: position + 1] = int.to_bytes(self._x_x_i_qs_g_.value, 1, "little")
        position += 1

        buffer[position: position + 4] = int.to_bytes(self.py__r___c_c_, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.y__r____kw__, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.__bts____p_g, 4, "little")
        position += 4

        buffer[position: position + 16] = self.oo_e_gmn__ru
        position += 16

        buffer[position: position + 4] = int.to_bytes(self.__iy__fox__k, 4, "little")
        position += 4

        if (self.g_r__z_jm_x_ is not None and self.g_r__z_jm_x_ > datetime.datetime(1601,1,1)):

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.g_r__z_jm_x_ - j____h_x_v_h).total_seconds()) * 10_000_000

            w_s_h_o_j___ = i_x____hz_to.to_bytes(8, "little")

            buffer[position: position + 4] = w_s_h_o_j___[0:4]
            position += 4
            buffer[position: position + 4] = w_s_h_o_j___[4:8]
            position += 4
        else:
            buffer[position: position + 4] = bytes(4)
            position += 4
            buffer[position: position + 4] = bytes(4)
            position += 4

        if (self.o___gqz_ln__ is not None and self.o___gqz_ln__ > datetime.datetime(1601,1,1)):

            j____h_x_v_h = datetime.datetime(1601,1,1)
            i_x____hz_to = int((self.o___gqz_ln__ - j____h_x_v_h).total_seconds()) * 10_000_000

            w_s_h_o_j___ = i_x____hz_to.to_bytes(8, "little")

            buffer[position: position + 4] = w_s_h_o_j___[0:4]
            position += 4
            buffer[position: position + 4] = w_s_h_o_j___[4:8]
            position += 4
        else:
            buffer[position: position + 4] = bytes(4)
            position += 4
            buffer[position: position + 4] = bytes(4)
            position += 4


        buffer[position: position + 4] = int.to_bytes(self._fn__xr_wjhc, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self._kv_js____l_, 4, "little")
        position += 4

        return buffer

    def get_entry(self, name):

        for entry in self.directory_entries:            
            if entry.name == name:
                return entry

        return None

    @staticmethod    
    def _j__y____u__(utc_datetime):
        offset = datetime.datetime.fromtimestamp(utc_datetime.timestamp()) - datetime.datetime.utcfromtimestamp(utc_datetime.timestamp())
        return utc_datetime + offset  

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def type(self):
        return self._j___xwggn_w

    @type.setter
    def type(self, value):
        self._j___xwggn_w = value

    @property
    def color(self):
        return self._x_x_i_qs_g_

    @color.setter
    def color(self, value):
        self._x_x_i_qs_g_ = value

    @property
    def left_sibling_sid(self):
        return self.py__r___c_c_

    @left_sibling_sid.setter
    def left_sibling_sid(self, value):
        self.py__r___c_c_ = value

    @property
    def right_sibling_sid(self):
        return self.y__r____kw__

    @right_sibling_sid.setter
    def right_sibling_sid(self, value):
        self.y__r____kw__ = value

    @property
    def child_sid(self):
        return self.__bts____p_g

    @child_sid.setter
    def child_sid(self, value):
        self.__bts____p_g = value

    @property
    def class_id(self):
        return self.oo_e_gmn__ru

    @class_id.setter
    def class_id(self, value):
        self.oo_e_gmn__ru = value

    @property
    def created_time(self):
        return self.g_r__z_jm_x_

    @created_time.setter
    def created_time(self, value):
        self.g_r__z_jm_x_ = value

    @property
    def last_modified_time(self):
        return self.o___gqz_ln__

    @last_modified_time.setter
    def last_modified_time(self, value):
        self.o___gqz_ln__ = value

    @property
    def start_sector(self):
        return self._fn__xr_wjhc

    @start_sector.setter
    def start_sector(self, value):
        self._fn__xr_wjhc = value

    @property
    def size(self):
        return self._kv_js____l_

    @size.setter
    def size(self, value):
        self._kv_js____l_ = value

    @property
    def buffer(self):
        return self.iy__________

    @buffer.setter
    def buffer(self, value):
        self.iy__________ = value

    @property
    def directory_entries(self):
        return self.po__g__o____

    @property
    def parent(self):
        return self.___jr_q__w_s

    @parent.setter
    def parent(self, value):
        self.___jr_q__w_s = value

class RootDirectoryEntry(DirectoryEntry):
    
    def __init__(self, name = 'Root'):
        super().__init__()
        self.type = DirectoryEntryType.ROOT
        self.name = name

class Stream(DirectoryEntry):
    
    def __init__(self, name = None, buffer = None):
        super().__init__()
        self.type = DirectoryEntryType.STREAM
        self.name = name
        self.buffer = buffer

class Storage(DirectoryEntry):
    
    def __init__(self, name = None):
        super().__init__()
        self.type = DirectoryEntryType.STORAGE
        self.name = name

class DirectoryEntryType(Enum):
    INVALID = 0
    STORAGE = 1
    STREAM = 2
    LOCK_BYTES = 3
    PROPERTY = 4,
    ROOT = 5

class Color(Enum):
    RED = 0
    BLACK = 1


class Header:
    v__y____if_e = bytes([0xd0, 0xcf, 0x11, 0xe0, 0xa1, 0xb1, 0x1a, 0xe1])

    def __init__(self, buffer = None):

        self.oo_e_gmn__ru = bytes(16)
        self.____b___a_g_ = 0x003E
        self.____y__el___ = 0x0003
        self.d__wj___t_h_ = 0xFFFE
        self.o___fij____n = 0x0009
        self._uc_y_e_xwug = 0x0006
        self._e___t_g____ = 0x0
        self.b_jlz__i___q = 0x0
        self.n___jfu__f_w = 0x0
        self.wo_n__c_t_ed = 0x0
        self.___uyf__rv__ = 0x0
        self.a_vnqx__f__r = 0x0
        self.q_tm__b____m = 4096
        self.wrjo_i__x_gj = 0x0
        self.___jk___aq_d = 0x0
        self.m__r____m_i_ = 0x0
        self.a__h_rkye__j = 0x0
        self._cv_qy_____i = []

        for i in range(109):
            self._cv_qy_____i.append(0)

        if buffer is not None:
           
            position = 0

            test_signature = buffer[position: position + 8]
            position += 8

            for i in range(8):
                if test_signature[i] != Header.v__y____if_e[i]:
                    raise Exception("Invalid file format.")

            self.oo_e_gmn__ru = buffer[position: position + 16]
            position += 16

            self.____b___a_g_ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.____y__el___ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.d__wj___t_h_ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.o___fij____n = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self._uc_y_e_xwug = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self._e___t_g____ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.b_jlz__i___q = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.n___jfu__f_w = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.wo_n__c_t_ed = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.___uyf__rv__ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.a_vnqx__f__r = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.q_tm__b____m = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.wrjo_i__x_gj = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.___jk___aq_d = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.m__r____m_i_ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.a__h_rkye__j = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self._cv_qy_____i = []

            for i in range(109):
                self._cv_qy_____i.append(int.from_bytes(buffer[position: position + 4], "little"))
                position += 4

    def to_bytes(self):

        buffer = bytearray(self.sector_size)
        position = 0

        buffer[position: position + 8] = self.v__y____if_e
        position += 8

        buffer[position: position + 16] = self.oo_e_gmn__ru
        position += 16

        buffer[position: position + 2] = int.to_bytes(self.____b___a_g_, 2, "little")
        position += 2
        
        buffer[position: position + 2] = int.to_bytes(self.____y__el___, 2, "little")
        position += 2

        buffer[position: position + 2] = int.to_bytes(self.d__wj___t_h_, 2, "little")
        position += 2
        
        buffer[position: position + 2] = int.to_bytes(self.o___fij____n, 2, "little")
        position += 2

        buffer[position: position + 2] = int.to_bytes(self._uc_y_e_xwug, 2, "little")
        position += 2
        
        buffer[position: position + 2] = int.to_bytes(self._e___t_g____, 2, "little")
        position += 2

        buffer[position: position + 4] = int.to_bytes(self.b_jlz__i___q, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.n___jfu__f_w, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.wo_n__c_t_ed, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.___uyf__rv__, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.a_vnqx__f__r, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.q_tm__b____m, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.wrjo_i__x_gj, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.___jk___aq_d, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.m__r____m_i_, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.a__h_rkye__j, 4, "little")
        position += 4

        for i in range(109):
            buffer[position: position + 4] = int.to_bytes(self._cv_qy_____i[i], 4, "little")
            position += 4

        return buffer

    @property
    def class_id(self):
        return self.oo_e_gmn__ru

    @property
    def minor_version(self):
        return self.____b___a_g_

    @minor_version.setter
    def minor_version(self, value):
        self.____b___a_g_ = value

    @property
    def major_version(self):
        return self.____y__el___

    @major_version.setter
    def major_version(self, value):
        if (value == 3):
            self.____y__el___ = value
            self.o___fij____n = 0x0009
        else:
            self.____y__el___ = value
            self.o___fij____n = 0x000C
    
    @property
    def byte_order(self):
        return self.d__wj___t_h_

    @property
    def sector_size(self):
        if self.o___fij____n == 9:
            return 512
        else:
            return 4096

    @property
    def mini_sector_size(self):
        return 64

    @property
    def directory_sector_count(self):
        return self.n___jfu__f_w

    @directory_sector_count.setter
    def directory_sector_count(self, value):
        self.n___jfu__f_w = value

    @property
    def fat_sector_count(self):
        return self.wo_n__c_t_ed

    @fat_sector_count.setter
    def fat_sector_count(self, value):
        self.wo_n__c_t_ed = value

    @property
    def first_directory_sector(self):
        return self.___uyf__rv__

    @first_directory_sector.setter
    def first_directory_sector(self, value):
        self.___uyf__rv__ = value

    @property
    def transaction_signature(self):
        return self.a_vnqx__f__r

    @property
    def mini_stream_max_size(self):
        return self.q_tm__b____m

    @property
    def first_mini_fat_sector(self):
        return self.wrjo_i__x_gj

    @first_mini_fat_sector.setter
    def first_mini_fat_sector(self, value):
        self.wrjo_i__x_gj = value

    @property
    def mini_fat_sector_count(self):
        return self.___jk___aq_d

    @mini_fat_sector_count.setter
    def mini_fat_sector_count(self, value):
        self.___jk___aq_d = value

    @property
    def first_difat_sector(self):
        return self.m__r____m_i_

    @first_difat_sector.setter
    def first_difat_sector(self, value):
        self.m__r____m_i_ = value

    @property
    def difat_sector_count(self):
        return self.a__h_rkye__j

    @difat_sector_count.setter
    def difat_sector_count(self, value):
        self.a__h_rkye__j = value

    @property
    def difat(self):
        return self._cv_qy_____i