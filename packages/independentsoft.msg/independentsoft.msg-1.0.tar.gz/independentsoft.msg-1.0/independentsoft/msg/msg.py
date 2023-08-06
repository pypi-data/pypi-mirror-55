import struct
import datetime
from enum import Enum

class Message:

    def __init__(self, file_path = None, buffer = None, parent = None):

        self.lh_______ysy = None        
        self._pq_o______n = "IPM.Note"
        self._xv_y___o___ = None
        self._u__q__z___b = None
        self._rz_mvr_yf_p = None
        self.f_pfu__g_o_p = None
        self._nfg_ljsz_d_ = None
        self.v_xe_s_yi_bp = None
        self.p_j_________ = None
        self.na___bd__o_a = None
        self.d_w____xbnru = None
        self.____y_gej_ly = None
        self._h_b_v_d____ = None
        self.__i___m_ncy_ = None
        self.fhgy_b_an_h_ = None
        self.__j__stw_l_u = None
        self.___k________ = None
        self.vbn_jd_xc_c_ = None
        self.__v_r_____n_ = datetime.datetime(1,1,1)
        self._onw__vy_til = datetime.datetime(1,1,1)
        self.p__ia_c_i_i_ = datetime.datetime(1,1,1)
        self.o_d_dh_dp_z_ = datetime.datetime(1,1,1)
        self._____ngk_oi_ = datetime.datetime(1,1,1)
        self._anq_obd_oq_ = datetime.datetime(1,1,1)
        self.tl_tqbr__xyq = datetime.datetime(1,1,1)
        self.twqm_____n_r = None
        self.____y_kuq__q = None
        self.___zp_upib__ = None
        self.____w_h_sni_ = None
        self._______eft__ = None
        self._fio_i_c_few = None
        self.juou_jp_axl_ = 0
        self.kw_x_qi_w_s_ = 0
        self.d__m___n____ = 0
        self._x_____y___i = 0
        self.k_kt_xqc____ = None
        self.o__ic_zjug_e = False
        self.__kpffcnr___ = False
        self.we__f_y__hbo = False
        self.xa_____a___v = False
        self.__le______q_ = False
        self.___g_ta__tfn = False
        self.sg_____x____ = False
        self._vhmwqhr__cd = False
        self.zpz__r____ji = None
        self.___wh_qn____ = Sensitivity.NONE
        self._b_ue__y_z__ = Importance.NONE
        self._ci_____r_uk = Priority.NONE
        self.w__hc___o___ = FlagIcon.NONE
        self._b_a_v___hjn = FlagStatus.NONE
        self.v___w_dliib_ = ObjectType.NONE
        self._vry_n_v_d_g = None
        self.___x_ry__twg = None
        self.___h_____oo_ = None
        self.b_o_l__vz__j = None
        self.ehp_zo_hnnk_ = None
        self._k__vn_qvf__ = None
        self._x___qkj___e = None
        self.__ynoc______ = None
        self.nn__l___z_p_ = None
        self.d_vn__f____i = None
        self.t___f_____hz = None
        self.__rfliczcge_ = None
        self.______qcsd_d = None
        self.insn_u______ = None
        self.v_x__v____fh = None
        self._a__y_vf_eib = None
        self.xep__h_t__f_ = None
        self._w_tq___xpkm = None
        self.__tl__v__h__ = None
        self.rle_hef_uum_ = None
        self.____d_yy__gy = None
        self._fb_znz_lkv_ = None
        self.__z__nhb_s__ = None
        self.om____q_____ = datetime.datetime(1,1,1)
        self._ox_qg_e____ = LastVerbExecuted.NONE
        self.c______ny_uq = []
        self._y__ti__u__a = []
        self.__naz_____bg = None
        self.ikw_q___t_ck = 0
        self.u_wj__bz__ue = datetime.datetime(1,1,1)
        self._pcg__fmli__ = datetime.datetime(1,1,1)
        self.w__j_w______ = datetime.datetime(1,1,1)
        self.__bbqh_x____ = False
        self._______vx_ok = datetime.datetime(1,1,1)
        self.__qhz__ecaho = 0
        self.lb_im_l__ptk = []
        self._____kd_o_cn = []
        self._mk___k_rw_y = []
        self.giyc___g__o_ = None
        self._t__expt_i_d = None
        self.____za___j_w = None
        self._st_____rh_q = False
        self._ca___k_ub_x = False
        self._o__________ = False
        self.r____dmo__a_ = False
        self._et__ia_vcjd = None
        self.cq_m_axum___ = datetime.datetime(1,1,1)
        self.zr___i__g_q_ = datetime.datetime(1,1,1)
        self._mr_j__yp__f = False
        self.w_yd__qc_q__ = None
        self.yl__e__fnwt_ = BusyStatus.NONE
        self.__w_uoq___s_ = MeetingStatus.NONE
        self.____f_kom_m_ = ResponseStatus.NONE
        self.___utdtdt_yw = RecurrenceType.NONE
        self.h_o_z_mo_h__ = None
        self._____egyzai_ = None
        self._vs_t_ntls_l = None
        self._s_egzvgujz_ = None
        self._oi___li_yx_ = None
        self.ls_m_lek_i_c = -1
        self.j__vi__y_vh_ = 0
        self.kn_va_____zr = datetime.datetime(1,1,1)
        self.drg_hha_bdef = datetime.datetime(1,1,1)
        self.ug__bxm__u__ = None
        self._dznn_vo__f_ = None
        self.cw_z___z____ = 0
        self.__c_q_q____g = 0
        self.kk____qaf_je = 0
        self.hd____j__j__ = False
        self.__gn_p___y__ = False
        self._il_______cr = datetime.datetime(1,1,1)
        self.____ueit___l = TaskStatus.NONE
        self.p__f_s_____t = TaskOwnership.NONE
        self._c__v___wqqb = TaskDelegationState.NONE
        self.g__tp___yb__ = 0
        self.qi______kjo_ = 0
        self.__no__s_vsl_ = 0
        self.om_u__xna_q_ = 0
        self.j____bexpm__ = NoteColor.NONE
        self.__i_b_kq_iap = datetime.datetime(1,1,1)
        self.rq__k____jkt = datetime.datetime(1,1,1)
        self._s______z_yx = None
        self.va_uignshqy_ = None
        self._jnlqe_____v = 0
        self.hsu__s____k_ = datetime.datetime(1,1,1)
        self._v__e__f____ = []
        self.m__vg_n__ze_ = None
        self.__x_____x__h = None
        self.h_w_j_lt_u_n = None
        self.t__w_nqk____ = None
        self.__rom_q__nzu = None
        self.h_a_x____w_j = None
        self.ul_l_qtt___p = None
        self.__m__tcaw___ = None
        self.owjw_l_is_fs = None
        self.____v__n___r = None
        self.e_s_i__m____ = None
        self.______rz___k = None
        self._____li__w__ = None
        self.hgsi_u__j__v = None
        self.__j___op_s__ = None
        self._pudmbn_y_qy = None
        self._x_b_d_u__hg = None
        self.gd_n__q___qg = None
        self._ks__k_____f = None
        self.tb_____r_t__ = None
        self.________zntw = None
        self.__rvw_yhfi_g = None
        self.__y_____aw__ = None
        self._____lc_g_h_ = None
        self.d__ol_f_a_i_ = None
        self.__xc__e_i___ = None
        self.v_s____jaf__ = None
        self.___h_r__f_d_ = None
        self.w___u___r_fm = None
        self.v__pel_bkku_ = None
        self.____s_a_ddga = None
        self._k__dsw_fx_j = None
        self._h_sxo__l_h_ = None
        self.fxo_h_yp____ = None
        self.r_____xd__nn = None
        self.xh_n_w_ab_q_ = None
        self.p___p__ch_nr = None
        self.x__za__bvxv_ = None
        self.b___w_g__t__ = None
        self._n___kc___xe = None
        self.t___m_b___qg = None
        self.o___h_f_ey_j = None
        self.w_qf___ld___ = None
        self.__v_cyc_____ = None
        self.h__l____bnit = None
        self.ks___x_ef_l_ = None
        self.g_k_____pg__ = None
        self.___c_d_i__l_ = None
        self.acu_i__mj_b_ = None
        self.__dyk_vx_w__ = None
        self._q___u__q_u_ = None
        self.hl_z____eu_u = None
        self.__br___ty__q = None
        self.mma_d_p_ijv_ = None
        self.p___m__s_toa = None
        self.reycs___h__f = None
        self.__zl_e_zx___ = None
        self.j_i_g__k____ = None
        self._x___k_b____ = None
        self.jvd_z__mk__k = None
        self.__g___vgx_da = datetime.datetime(1,1,1)
        self.o_y_e___dh__ = Gender.NONE
        self._______w_a__ = SelectedMailingAddress.NONE
        self.______yi_a_r = False
        self.a____h_d_m__ = None
        self.___p___m_x__ = None
        self.a__yb______q = None
        self._in__an_yv__ = None
        self.kwi_e__ffg__ = None
        self.___ym__z_v__ = None
        self.s__b____or_b = None
        self._us___o__z__ = None
        self._cf__c_q__c_ = None
        self.y___cq__rk__ = None
        self.w_g_ag_b_w__ = None
        self.j_t_u__f____ = None
        self._z___m__jkqj = None
        self.m__nj____x__ = None
        self.h_k_lm______ = None
        self._f__lx__ayl_ = None
        self.s__g_h__crxw = None
        self.e_o__a__mz_s = None
        self._g_l_bu__r__ = None
        self.kw_r____n__e = None
        self.ti__vpygof_h = None

        self.__w_e______y = []
        self.uj_c_u_uy___ = []
        self.fmuyou__mciw = []
        self.__qwshy_x_o_ = []

        self.m__zli___l_b = "001E"
        self.wiqwtada__v_ = 0x001E
        self.h______id_ai = "101E"
        self._wet__k__o__ = 0x101E

        self.nsifr_q_er__ = 'utf_8'
        self._x_q___iqwz_ = 'utf_8'
        self.h_c_rs_lkt__ = 'utf-16-le'
        self.t__n_____ev_ = False

        if file_path is not None: 
            f = open(file_path, 'rb')
            buffer = f.read()
            self._____j______(buffer)
            f.close()

        elif buffer != None:
            self._____j______(buffer)
        elif parent != None:
            self.t__n_____ev_ = True
            self.__qyb_kxw__b(parent)
        else:
            self._y__ti__u__a.append(StoreSupportMask.ATTACHMENTS)
            self._y__ti__u__a.append(StoreSupportMask.CATEGORIZE)
            self._y__ti__u__a.append(StoreSupportMask.CREATE)
            self._y__ti__u__a.append(StoreSupportMask.HTML)
            self._y__ti__u__a.append(StoreSupportMask.ITEM_PROC)
            self._y__ti__u__a.append(StoreSupportMask.MODIFY)
            self._y__ti__u__a.append(StoreSupportMask.MULTI_VALUE_PROPERTIES)
            self._y__ti__u__a.append(StoreSupportMask.NOTIFY)
            self._y__ti__u__a.append(StoreSupportMask.OLE)
            self._y__ti__u__a.append(StoreSupportMask.PUSHER)
            self._y__ti__u__a.append(StoreSupportMask.READ_ONLY)
            self._y__ti__u__a.append(StoreSupportMask.RESTRICTIONS)
            self._y__ti__u__a.append(StoreSupportMask.RTF)
            self._y__ti__u__a.append(StoreSupportMask.SEARCH)
            self._y__ti__u__a.append(StoreSupportMask.SORT)
            self._y__ti__u__a.append(StoreSupportMask.SUBMIT)
            self._y__ti__u__a.append(StoreSupportMask.UNCOMPRESSED_RTF)
            self._y__ti__u__a.append(StoreSupportMask.UNICODE)

    def _____j______(self, _s___oubc___):

            __iq_pf_pm_j = CompoundFile(file_path = None, buffer = _s___oubc___)

            gfp__ufh____ =  __iq_pf_pm_j.root.get_entry("__nameid_version1.0")

            ___cdb______ = gfp__ufh____.get_entry("__substg1.0_00020102")
            __dp_i_zi_on = gfp__ufh____.get_entry("__substg1.0_00030102")
            t_zr__jz__uj = gfp__ufh____.get_entry("__substg1.0_00040102")

            _lm___l_x__c = {}
            self.__qwshy_x_o_ = []

            if __dp_i_zi_on is not None:

                dpy_e__u_p_r = int(__dp_i_zi_on.size / 8)
                s_c_______t_ = __dp_i_zi_on.buffer

                for i in range(dpy_e__u_p_r):

                    i__d__usa___ = int.from_bytes(s_c_______t_[i * 8: i * 8 + 4], "little")
                    mj_tgux_g___ = int.from_bytes(s_c_______t_[i * 8 + 4: i * 8 + 8], "little")

                    ___w_q___lm_ = Message.__u_cjujm___(mj_tgux_g___ >> 16)
                    hlcjgtq_hdv_ = Message.__u_cjujm___((mj_tgux_g___ << 16) >> 16)
                    _wa___td__sd = Message.__u_cjujm___(hlcjgtq_hdv_ >> 1)
                    puwre______t = Message.__u_cjujm___(hlcjgtq_hdv_ << 15)

                    _i_toah_o_y_ = NamedProperty()

                    if puwre______t == 0: 
                        _jha____nf__ = i__d__usa___

                        _i_toah_o_y_.id = _jha____nf__
                        _i_toah_o_y_.type = NamedPropertyType.NUMERICAL
                   
                    else:

                        j_ui_rk_yf_e = i__d__usa___
                        _bl_____y__u = t_zr__jz__uj.buffer
                        
                        aceh_ssnxcg_ = int.from_bytes(_bl_____y__u[j_ui_rk_yf_e: j_ui_rk_yf_e + 4], "little")

                        ___k_f__l_z_ = None

                        if (aceh_ssnxcg_ > 0):
                            t_l____xg__t = _bl_____y__u[j_ui_rk_yf_e + 4: j_ui_rk_yf_e + 4 + aceh_ssnxcg_]
                            ___k_f__l_z_ = t_l____xg__t.decode('utf-16-le')

                        _i_toah_o_y_.name = ___k_f__l_z_
                        _i_toah_o_y_.type = NamedPropertyType.STRING

                    if _wa___td__sd == 1:
                        _i_toah_o_y_.guid = StandardPropertySet.MAPI
                    elif _wa___td__sd == 2:
                        _i_toah_o_y_.guid = StandardPropertySet.PUBLIC_STRINGS
                    elif _wa___td__sd > 2:
                        
                        ___fv__jf_vk = _wa___td__sd - 3

                        c_ekl___ri_v = ___cdb______.buffer
                        _x_ono_wsf_e = c_ekl___ri_v[___fv__jf_vk * 16: ___fv__jf_vk * 16 + 16]

                        _i_toah_o_y_.guid = _x_ono_wsf_e
                    
                    if _i_toah_o_y_.id > 0:

                        d_e_ox___y__ = Message.x_t_w_mm____(_i_toah_o_y_.id, _i_toah_o_y_.guid)
                        es_yempff___ = str.format("{:04X}", 0x8000 + ___w_q___lm_)

                        if d_e_ox___y__ not in _lm___l_x__c: 
                            _lm___l_x__c[d_e_ox___y__] = es_yempff___

                    elif (_i_toah_o_y_.name is not None):

                        d_e_ox___y__ = Message.x_t_w_mm____(_i_toah_o_y_.name, _i_toah_o_y_.guid)
                        es_yempff___ = str.format("{:04X}", 0x8000 + ___w_q___lm_)

                        if d_e_ox___y__ not in _lm___l_x__c: 
                            _lm___l_x__c[d_e_ox___y__] = es_yempff___
         
                    self.__qwshy_x_o_.append(_i_toah_o_y_)


            for n in range(len(self.__qwshy_x_o_)):

                _t_fl______u = self.__qwshy_x_o_[n]

                if _t_fl______u.name is not None:
                    __x____v__t_ = ExtendedPropertyName(_t_fl______u.name, _t_fl______u.guid)
                    tx__g_gl___q = ExtendedProperty(__x____v__t_)
                    self.fmuyou__mciw.append(tx__g_gl___q)

                elif _t_fl______u.id > 0:
                    y__r_fd_m___ = ExtendedPropertyId(_t_fl______u.id, _t_fl______u.guid)
                    tx__g_gl___q = ExtendedProperty(y__r_fd_m___)
                    self.fmuyou__mciw.append(tx__g_gl___q)           

            self.__qyb_kxw__b(__iq_pf_pm_j.root, _lm___l_x__c)

    def __qyb_kxw__b(self, vi_h__c____n, _lm___l_x__c = None):
        self.________fqfa = 24
        self.lh_______ysy = {}

        ch_tqnyok___ = vi_h__c____n.get_entry("__properties_version1.0")

        z_______z__r = 0
        y___ftj_ixrh = 0

        if ch_tqnyok___ is not None:
            ey__bf__tmt_ = int.from_bytes(ch_tqnyok___.buffer[0:4], "little")
            o___ikcjbv_b = int.from_bytes(ch_tqnyok___.buffer[4:8], "little")
            jka___bla_a_ = int.from_bytes(ch_tqnyok___.buffer[8:12], "little")
            _______jvm_p = int.from_bytes(ch_tqnyok___.buffer[12:16], "little")
            z_______z__r = int.from_bytes(ch_tqnyok___.buffer[16:20], "little")
            y___ftj_ixrh = int.from_bytes(ch_tqnyok___.buffer[20:24], "little")

        if not self.t__n_____ev_:
            
            if ch_tqnyok___ is not None:
                ta___l_r_l__ = int.from_bytes(ch_tqnyok___.buffer[24:28], "little")
                pa___zh_mk_s = int.from_bytes(ch_tqnyok___.buffer[28:32], "little")

            self.________fqfa = 32

        if ch_tqnyok___ is not None and ch_tqnyok___.buffer is not None:
            
            for i in range(self.________fqfa, len(ch_tqnyok___.buffer) - 15, 16):

                rw__o_d_x___ = ch_tqnyok___.buffer[i: i+16]

                __p_fzml____ = Property(rw__o_d_x___)

                if __p_fzml____.size > 0:

                    _bgfbumjdrpp = "__substg1.0_" + str.format("{:08X}", __p_fzml____.tag)

                    n_nw___j__u_ = vi_h__c____n.get_entry(_bgfbumjdrpp)

                    if n_nw___j__u_ is not None and n_nw___j__u_.buffer is not None and len(n_nw___j__u_.buffer) > 0:
                        __p_fzml____.value = n_nw___j__u_.buffer[0: len(n_nw___j__u_.buffer)]                         
   
                zfe_fb_up___ = str.format("{:08X}", __p_fzml____.tag)

                try:
                    self.lh_______ysy[zfe_fb_up___] = __p_fzml____
                except:
                    pass


        e_hi__pq___s = self.lh_______ysy["3FDE0003"] if "3FDE0003" in self.lh_______ysy else None

        if e_hi__pq___s is not None and e_hi__pq___s.value is not None:
            self._x_____y___i = int.from_bytes(e_hi__pq___s.value[0:4], "little")

        dnqo_elc____ =  self.lh_______ysy["3FFD0003"] if "3FFD0003" in self.lh_______ysy else None

        if dnqo_elc____ is not None and dnqo_elc____.value is not None:
            self.juou_jp_axl_ = int.from_bytes(dnqo_elc____.value[0:4], "little")
        
        if self.juou_jp_axl_ > 0:
        
            try:
                self.nsifr_q_er__ = Message.uw_u___c_l__(self.juou_jp_axl_)
            except:
                pass 

        elif self._x_____y___i > 0:

            try:
                self.nsifr_q_er__ = Message.uw_u___c_l__(self._x_____y___i)
            except:
                pass

        _e__yn___l_v = self.lh_______ysy["340D0003"] if "340D0003" in self.lh_______ysy else None

        if _e__yn___l_v is not None and _e__yn___l_v.value is not None:

            v______j_i__ = int.from_bytes(_e__yn___l_v.value[0: 4], "little")

            self._y__ti__u__a = EnumUtil.parse_store_support_mask(v______j_i__)

            if (v______j_i__ & 0x00040000) == 0x00040000:

                self.nsifr_q_er__ = "utf-16-le"
                self.m__zli___l_b = "001F"
                self.wiqwtada__v_ = 0x001F
                self.h______id_ai = "101F"
                self._wet__k__o__ = 0x101F

       
        x_m_sky_gz__ = len("\0".encode(self.nsifr_q_er__))

        mmbq__b_gylp = self.lh_______ysy["30070040"] if "30070040" in self.lh_______ysy else None

        if mmbq__b_gylp is not None and mmbq__b_gylp.value is not None:

            j_t_rhesbt__ = int.from_bytes(mmbq__b_gylp.value[0: 4], "little")
            f_f__pqry___ = int.from_bytes(mmbq__b_gylp.value[4: 8], "little")

            if f_f__pqry___ > 0:
                _fi_km_v____ = j_t_rhesbt__ + (f_f__pqry___ << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)  

                try:    
                    self.__v_r_____n_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.__v_r_____n_ = Message.v_____omf__x(self.__v_r_____n_)
                except:
                    pass

        o_pkf_syr_jf = self.lh_______ysy["30080040"] if "30080040" in self.lh_______ysy else None

        if o_pkf_syr_jf is not None and o_pkf_syr_jf.value is not None:

            _wdtvfms_yl_ = int.from_bytes(o_pkf_syr_jf.value[0: 4], "little")
            _______s_llz = int.from_bytes(o_pkf_syr_jf.value[4: 8], "little")

            if _______s_llz > 0:
                _fi_km_v____ = _wdtvfms_yl_ + (_______s_llz << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)   

                try:    
                    self._onw__vy_til = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self._onw__vy_til = Message.v_____omf__x(self._onw__vy_til)
                except:
                    pass

        e_o__v__t__e = self.lh_______ysy["0E060040"] if "0E060040" in self.lh_______ysy else None

        if e_o__v__t__e is not None and e_o__v__t__e.value is not None:

            _gij____p___ = int.from_bytes(e_o__v__t__e.value[0: 4], "little")
            bbl__q_npt__ = int.from_bytes(e_o__v__t__e.value[4: 8], "little")

            if bbl__q_npt__ > 0:
                _fi_km_v____ = _gij____p___ + (bbl__q_npt__ << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)

                try:    
                    self.p__ia_c_i_i_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.p__ia_c_i_i_ = Message.v_____omf__x(self.p__ia_c_i_i_)
                except:
                    pass

        _r__ug______ = self.lh_______ysy["00390040"] if "00390040" in self.lh_______ysy else None

        if _r__ug______ is not None and _r__ug______.value is not None:

            g__n__hfpo__ = int.from_bytes(_r__ug______.value[0: 4], "little")
            _keg__n__of_ = int.from_bytes(_r__ug______.value[4: 8], "little")

            if _keg__n__of_ > 0:
                _fi_km_v____ = g__n__hfpo__ + (_keg__n__of_ << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)

                try:    
                    self.o_d_dh_dp_z_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.o_d_dh_dp_z_ = Message.v_____omf__x(self.o_d_dh_dp_z_)
                except:
                    pass 

        _i__y___iz_v = self.lh_______ysy["000F0040"] if "000F0040" in self.lh_______ysy else None

        if _i__y___iz_v is not None and _i__y___iz_v.value is not None:

            g_gx___r__bx = int.from_bytes(_i__y___iz_v.value[0: 4], "little")
            hnfs________ = int.from_bytes(_i__y___iz_v.value[4: 8], "little")

            if hnfs________ > 0:
                _fi_km_v____ = g_gx___r__bx + (hnfs________ << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)

                try:    
                    self._____ngk_oi_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self._____ngk_oi_ = Message.v_____omf__x(self._____ngk_oi_)
                except:
                    pass 

        we__z_wr____ = self.lh_______ysy["00480040"] if "00480040" in self.lh_______ysy else None

        if we__z_wr____ is not None and we__z_wr____.value is not None:

            __wpix____v_ = int.from_bytes(we__z_wr____.value[0: 4], "little")
            _d_i____lwsg = int.from_bytes(we__z_wr____.value[4: 8], "little")

            if _d_i____lwsg > 0:
                _fi_km_v____ = __wpix____v_ + (_d_i____lwsg << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)

                try:    
                    self._anq_obd_oq_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self._anq_obd_oq_ = Message.v_____omf__x(self._anq_obd_oq_)
                except:
                    pass 

        _huadg_e___t = self.lh_______ysy["00320040"] if "00320040" in self.lh_______ysy else None

        if _huadg_e___t is not None and _huadg_e___t.value is not None:

            uhdh__wwrfsv = int.from_bytes(_huadg_e___t.value[0: 4], "little")
            tpv___i_o__q = int.from_bytes(_huadg_e___t.value[4: 8], "little")

            if tpv___i_o__q > 0:
                _fi_km_v____ = uhdh__wwrfsv + (tpv___i_o__q << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)   

                try:    
                    self.tl_tqbr__xyq = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.tl_tqbr__xyq = Message.v_____omf__x(self.tl_tqbr__xyq)
                except:
                    pass 


        _xz___fgon_v = self.lh_______ysy["10820040"] if "10820040" in self.lh_______ysy else None

        if _xz___fgon_v is not None and _xz___fgon_v.value is not None:

            w__o__r__w__ = int.from_bytes(_xz___fgon_v.value[0: 4], "little")
            __e__m_rcaw_ = int.from_bytes(_xz___fgon_v.value[4: 8], "little")

            if __e__m_rcaw_ > 0:
                _fi_km_v____ = w__o__r__w__ + (__e__m_rcaw_ << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)      

                try:    
                    self.om____q_____ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.om____q_____ = Message.v_____omf__x(self.om____q_____)
                except:
                    pass 

        ___sm___ad__ = self.lh_______ysy["10800003"] if "10800003" in self.lh_______ysy else None

        if ___sm___ad__ is not None and ___sm___ad__.value is not None:
            self.kw_x_qi_w_s_ = int.from_bytes(___sm___ad__.value[0:4], "little")

        _fyve___m_jr = self.lh_______ysy["0E080003"] if "0E080003" in self.lh_______ysy else None

        if _fyve___m_jr is not None and _fyve___m_jr.value is not None:
            self.d__m___n____ = int.from_bytes(_fyve___m_jr.value[0:4], "little")

        q__v_ow___ct = self.lh_______ysy["0E070003"] if "0E070003" in self.lh_______ysy else None

        if q__v_ow___ct is not None and q__v_ow___ct.value is not None:
            _ljpa__j___d = int.from_bytes(q__v_ow___ct.value[0:4], "little")
            self.c______ny_uq = EnumUtil.parse_message_flag(_ljpa__j___d)

        gabuuneaq___ = self.lh_______ysy["10F4000B"] if "10F4000B" in self.lh_______ysy else None

        if gabuuneaq___ is not None and gabuuneaq___.value is not None:
            ______qg__r_ = int.from_bytes(gabuuneaq___.value[0:2], "little")
            
            if ______qg__r_ > 0:
                self.o__ic_zjug_e = True

        _qf__v_h_u_o = self.lh_______ysy["10F6000B"] if "10F6000B" in self.lh_______ysy else None

        if _qf__v_h_u_o is not None and _qf__v_h_u_o.value is not None:
            q_fk_j______ = int.from_bytes(_qf__v_h_u_o.value[0:2], "little")
            
            if q_fk_j______ > 0:
                self.__kpffcnr___ = True

        _______ta_d_ = self.lh_______ysy["10F5000B"] if "10F5000B" in self.lh_______ysy else None

        if _______ta_d_ is not None and _______ta_d_.value is not None:
            hhs_z_gvu_d_ = int.from_bytes(_______ta_d_.value[0:2], "little")
            
            if hhs_z_gvu_d_ > 0:
                self.we__f_y__hbo = True

        __w__g___asu = self.lh_______ysy["10F2000B"] if "10F2000B" in self.lh_______ysy else None

        if __w__g___asu is not None and __w__g___asu.value is not None:
            l_bzp_l_i__y = int.from_bytes(__w__g___asu.value[0:2], "little")
            
            if l_bzp_l_i__y > 0:
                self.xa_____a___v = True

        t_f_a__qvieg = self.lh_______ysy["0E1B000B"] if "0E1B000B" in self.lh_______ysy else None

        if t_f_a__qvieg is not None and t_f_a__qvieg.value is not None:
            i_______de_f = int.from_bytes(t_f_a__qvieg.value[0:2], "little")
            
            if i_______de_f > 0:
                self.__le______q_ = True

        z_f_crftu__q = self.lh_______ysy["0E1F000B"] if "0E1F000B" in self.lh_______ysy else None

        if z_f_crftu__q is not None and z_f_crftu__q.value is not None:
            a___ag___hi_ = int.from_bytes(z_f_crftu__q.value[0:2], "little")
            
            if a___ag___hi_ > 0:
                self.___g_ta__tfn = True

        _v_g_h_z__q_ = self.lh_______ysy["0029000B"] if "0029000B" in self.lh_______ysy else None

        if _v_g_h_z__q_ is not None and _v_g_h_z__q_.value is not None:
            _lkn_t_i___w = int.from_bytes(_v_g_h_z__q_.value[0:2], "little")
            
            if _lkn_t_i___w > 0:
                self.sg_____x____ = True

        u_skkn__nu__ = self.lh_______ysy["0023000B"] if "0023000B" in self.lh_______ysy else None

        if u_skkn__nu__ is not None and u_skkn__nu__.value is not None:
            g_ytiaa___m_ = int.from_bytes(u_skkn__nu__.value[0:2], "little")
            
            if g_ytiaa___m_ > 0:
                self._vhmwqhr__cd = True

        ___oxca_yr_p = self.lh_______ysy["00360003"] if "00360003" in self.lh_______ysy else None

        if ___oxca_yr_p is not None and ___oxca_yr_p.value is not None:
            nti_tq__f__r = int.from_bytes(___oxca_yr_p.value[0:4], "little")
            
            self.___wh_qn____ = EnumUtil.parse_sensitivity(nti_tq__f__r)

        m_____x_syjn = self.lh_______ysy["10810003"] if "10810003" in self.lh_______ysy else None

        if m_____x_syjn is not None and m_____x_syjn.value is not None:
            _v_s_m_i_h_j = int.from_bytes(m_____x_syjn.value[0:4], "little")
            
            self._ox_qg_e____ = EnumUtil.parse_last_verb_executed(_v_s_m_i_h_j)

        _ngdhn__wjxi = self.lh_______ysy["00170003"] if "00170003" in self.lh_______ysy else None

        if _ngdhn__wjxi is not None and _ngdhn__wjxi.value is not None:
            _b_jfw_nf__i = int.from_bytes(_ngdhn__wjxi.value[0:4], "little")
            
            self._b_ue__y_z__ = EnumUtil.parse_importance(_b_jfw_nf__i)

        __j_ome__k_a = self.lh_______ysy["00260003"] if "00260003" in self.lh_______ysy else None

        if __j_ome__k_a is not None and __j_ome__k_a.value is not None:
            __bi___d__x_ = int.from_bytes(__j_ome__k_a.value[0:4], "little")
            
            self._ci_____r_uk = EnumUtil.parse_priority(__bi___d__x_)

        b__x_el___n_ = self.lh_______ysy["10950003"] if "10950003" in self.lh_______ysy else None

        if b__x_el___n_ is not None and b__x_el___n_.value is not None:
            ____tux___r_ = int.from_bytes(b__x_el___n_.value[0:4], "little")
            
            self.w__hc___o___ = EnumUtil.parse_flag_icon(____tux___r_)

        w_u_____kc_b = self.lh_______ysy["10950003"] if "10950003" in self.lh_______ysy else None

        if w_u_____kc_b is not None and w_u_____kc_b.value is not None:
            a_u___sg__zp = int.from_bytes(w_u_____kc_b.value[0:4], "little")
            
            self._b_a_v___hjn = EnumUtil.parse_flag_status(a_u___sg__zp)

        o______jc_u_ = self.lh_______ysy["0FFE0003"] if "0FFE0003" in self.lh_______ysy else None

        if o______jc_u_ is not None and o______jc_u_.value is not None:
            vq___c__c___ = int.from_bytes(o______jc_u_.value[0:4], "little")
            
            self.v___w_dliib_ = EnumUtil.parse_object_type(vq___c__c___)


        lemyut__e__t = 0x8554
        _et_cv_wxdsk = StandardPropertySet.COMMON

        psq__yqijv__ = Message.x_t_w_mm____(lemyut__e__t, _et_cv_wxdsk)

        if _lm___l_x__c is not None and psq__yqijv__ in _lm___l_x__c and _lm___l_x__c[psq__yqijv__] is not None:
            
            d___iy_gftw_ = _lm___l_x__c[psq__yqijv__]
            d___iy_gftw_ = d___iy_gftw_ + self.m__zli___l_b

            a_w_mg_a_g__ = self.lh_______ysy[d___iy_gftw_] if d___iy_gftw_ in self.lh_______ysy else None

            if a_w_mg_a_g__ is not None and a_w_mg_a_g__.value is not None:
                self.__naz_____bg = a_w_mg_a_g__.value.decode(self.nsifr_q_er__)


        _pf_go_x__r_ = 0x8552
        _qhhm___o_i_ = StandardPropertySet.COMMON

        _o_dgl_rb___ = Message.x_t_w_mm____(_pf_go_x__r_, _qhhm___o_i_)

        if _lm___l_x__c is not None and _o_dgl_rb___ in _lm___l_x__c and _lm___l_x__c[_o_dgl_rb___] is not None:
            
            ___in_______ = _lm___l_x__c[_o_dgl_rb___]
            ___in_______ = ___in_______ + "0003"

            k_knlf_np_e_ = self.lh_______ysy[___in_______] if ___in_______ in self.lh_______ysy else None

            if k_knlf_np_e_ is not None and k_knlf_np_e_.value is not None:
                self.ikw_q___t_ck = name = int.from_bytes(k_knlf_np_e_.value[0:4], "little")


        __h_f_p_zq_i = 0x8516
        v_uwh____g_k = StandardPropertySet.COMMON

        jx____z_____ = Message.x_t_w_mm____(__h_f_p_zq_i, v_uwh____g_k)

        if _lm___l_x__c is not None and jx____z_____ in _lm___l_x__c and _lm___l_x__c[jx____z_____] is not None:
            
            _cf___nlpzpp = _lm___l_x__c[jx____z_____]
            _cf___nlpzpp = _cf___nlpzpp + "0040"

            _zt__qi_cd_k = self.lh_______ysy[_cf___nlpzpp] if _cf___nlpzpp in self.lh_______ysy else None

            if _zt__qi_cd_k is not None and _zt__qi_cd_k.value is not None:

                r_ur______e_ = int.from_bytes(_zt__qi_cd_k.value[0: 4], "little")
                __u__o__q__c = int.from_bytes(_zt__qi_cd_k.value[4: 8], "little")

                if __u__o__q__c > 0:
                    _fi_km_v____ = r_ur______e_ + (__u__o__q__c << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)

                    try:    
                        self.u_wj__bz__ue = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.u_wj__bz__ue = Message.v_____omf__x(self.u_wj__bz__ue)
                    except:
                        pass 

        ____j_meb_nq = 0x8517
        e__p_tm___s_ = StandardPropertySet.COMMON

        i__n__phy__p = Message.x_t_w_mm____(____j_meb_nq, e__p_tm___s_)

        if _lm___l_x__c is not None and i__n__phy__p in _lm___l_x__c and _lm___l_x__c[i__n__phy__p] is not None:
            
            m_od_n______ = _lm___l_x__c[i__n__phy__p]
            m_od_n______ = m_od_n______ + "0040"

            h_rk___q_q_l = self.lh_______ysy[m_od_n______] if m_od_n______ in self.lh_______ysy else None

            if h_rk___q_q_l is not None and h_rk___q_q_l.value is not None:

                __i___f_____ = int.from_bytes(h_rk___q_q_l.value[0: 4], "little")
                z_f_g___m_sn = int.from_bytes(h_rk___q_q_l.value[4: 8], "little")

                if z_f_g___m_sn > 0:
                    _fi_km_v____ = __i___f_____ + (z_f_g___m_sn << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)

                    try:    
                        self._pcg__fmli__ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self._pcg__fmli__ = Message.v_____omf__x(self._pcg__fmli__)
                    except:
                        pass 


        ___kp___ou_b = 0x8560
        ____m__wfanb = StandardPropertySet.COMMON

        _vq____f___m = Message.x_t_w_mm____(___kp___ou_b, ____m__wfanb)

        if _lm___l_x__c is not None and _vq____f___m in _lm___l_x__c and _lm___l_x__c[_vq____f___m] is not None:
            
            td_hse_o_c__ = _lm___l_x__c[_vq____f___m]
            td_hse_o_c__ = td_hse_o_c__ + "0040"

            _b__r_da____ = self.lh_______ysy[td_hse_o_c__] if td_hse_o_c__ in self.lh_______ysy else None

            if _b__r_da____ is not None and _b__r_da____.value is not None:

                qj___gs__fom = int.from_bytes(_b__r_da____.value[0: 4], "little")
                dqmkgr___h__ = int.from_bytes(_b__r_da____.value[4: 8], "little")

                if dqmkgr___h__ > 0:
                    _fi_km_v____ = qj___gs__fom + (dqmkgr___h__ << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)      
                    
                    try:
                        self.w__j_w______ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)
                        self.w__j_w______ = Message.v_____omf__x(self.w__j_w______)
                    except:
                        pass 


        jl___t__z_ip = 0x8539
        nl____w__t_s = StandardPropertySet.COMMON

        a_t_____t___ = Message.x_t_w_mm____(jl___t__z_ip, nl____w__t_s)

        if _lm___l_x__c is not None and a_t_____t___ in _lm___l_x__c and _lm___l_x__c[a_t_____t___] is not None:
            
            _____f_mad_o = _lm___l_x__c[a_t_____t___]
            _____f_mad_o = td_hse_o_c__ + self.h______id_ai

            ___s___u_d_b = self.lh_______ysy[_____f_mad_o] if _____f_mad_o in self.lh_______ysy else None

            if ___s___u_d_b is not None and ___s___u_d_b.value is not None:

                wud_wp__mgd_ = int(___s___u_d_b.size / 4)

                self.lb_im_l__ptk = []

                for i in range(wud_wp__mgd_):

                    mok_o__e_wpq = "__substg1.0_" + _____f_mad_o + "-" + str.format("{:08X}", i)

                    qew__vs_j_hm = vi_h__c____n.get_entry(mok_o__e_wpq)

                    if qew__vs_j_hm is not None and qew__vs_j_hm.buffer is not None:

                        __nj__u_wmvc = qew__vs_j_hm.buffer[0: len(qew__vs_j_hm.buffer) - x_m_sky_gz__].decode(self.nsifr_q_er__)
                        self.lb_im_l__ptk.append(__nj__u_wmvc)


        _z_waann___y = 0x853A
        _e__yz__j_xi = StandardPropertySet.COMMON

        qagox___t_fg = Message.x_t_w_mm____(_z_waann___y, _e__yz__j_xi)

        if _lm___l_x__c is not None and qagox___t_fg in _lm___l_x__c and _lm___l_x__c[qagox___t_fg] is not None:
            
            _w_q_____xk_ = _lm___l_x__c[qagox___t_fg]
            _w_q_____xk_ = td_hse_o_c__ + self.h______id_ai

            hehqu_hdgl_b = self.lh_______ysy[_w_q_____xk_] if _w_q_____xk_ in self.lh_______ysy else None

            if hehqu_hdgl_b is not None and hehqu_hdgl_b.value is not None:

                _wg______pz_ = int(hehqu_hdgl_b.size / 4)

                self._____kd_o_cn = []

                for i in range(_wg______pz_):

                    mok_o__e_wpq = "__substg1.0_" + _w_q_____xk_ + "-" + str.format("{:08X}", i)

                    qew__vs_j_hm = vi_h__c____n.get_entry(mok_o__e_wpq)

                    if qew__vs_j_hm is not None and qew__vs_j_hm.buffer is not None:

                        dy__g_______ = qew__vs_j_hm.buffer[0: len(qew__vs_j_hm.buffer) - x_m_sky_gz__].decode(self.nsifr_q_er__)
                        self._____kd_o_cn.append(dy__g_______)


        __w_b_r_____ = "Keywords"
        ___tkq______ = StandardPropertySet.PUBLIC_STRINGS

        u___alop_we_ = Message.x_t_w_mm____(__w_b_r_____, ___tkq______)

        if _lm___l_x__c is not None and u___alop_we_ in _lm___l_x__c and _lm___l_x__c[u___alop_we_] is not None:
            
            v_____z_____ = _lm___l_x__c[u___alop_we_]
            v_____z_____ = v_____z_____ + self.h______id_ai

            __fik_m__wt_ = self.lh_______ysy[v_____z_____] if v_____z_____ in self.lh_______ysy else None

            if __fik_m__wt_ is not None and __fik_m__wt_.value is not None:

                cmw_z_b_____ = int(__fik_m__wt_.size / 4)

                self._mk___k_rw_y = []

                for i in range(cmw_z_b_____):

                    mok_o__e_wpq = "__substg1.0_" + v_____z_____ + "-" + str.format("{:08X}", i)

                    qew__vs_j_hm = vi_h__c____n.get_entry(mok_o__e_wpq)

                    if qew__vs_j_hm is not None and qew__vs_j_hm.buffer is not None:

                        _wumb_____bt = qew__vs_j_hm.buffer[0: len(qew__vs_j_hm.buffer) - x_m_sky_gz__].decode(self.nsifr_q_er__)
                        self._mk___k_rw_y.append(_wumb_____bt)


        ________vjd_ = 0x8535
        _mlfn___sv__ = StandardPropertySet.COMMON

        _b_a____dy_t = Message.x_t_w_mm____(________vjd_, _mlfn___sv__)

        if _lm___l_x__c is not None and _b_a____dy_t in _lm___l_x__c and _lm___l_x__c[_b_a____dy_t] is not None:
            
            __ug_rg_tlk_ = _lm___l_x__c[_b_a____dy_t]
            __ug_rg_tlk_ = __ug_rg_tlk_ + self.m__zli___l_b

            _qv_on_de_wa = self.lh_______ysy[__ug_rg_tlk_] if __ug_rg_tlk_ in self.lh_______ysy else None

            if _qv_on_de_wa is not None and _qv_on_de_wa.value is not None:
                self.giyc___g__o_ = _qv_on_de_wa.value.decode(self.nsifr_q_er__)


        _immb_m_i_b_ = 0x8534
        ___n_va_____ = StandardPropertySet.COMMON

        o_b______ss_ = Message.x_t_w_mm____(_immb_m_i_b_, ___n_va_____)

        if _lm___l_x__c is not None and o_b______ss_ in _lm___l_x__c and _lm___l_x__c[o_b______ss_] is not None:
            
            ___eeca_f_iw = _lm___l_x__c[o_b______ss_]
            ___eeca_f_iw = ___eeca_f_iw + self.m__zli___l_b

            fi__h____cb_ = self.lh_______ysy[___eeca_f_iw] if ___eeca_f_iw in self.lh_______ysy else None

            if fi__h____cb_ is not None and fi__h____cb_.value is not None:
                self._t__expt_i_d = fi__h____cb_.value.decode(self.nsifr_q_er__)

        
        e____ew_____ = 0x8580
        gy_m__tl_zpq = StandardPropertySet.COMMON

        __np_q__v_rh = Message.x_t_w_mm____(e____ew_____, gy_m__tl_zpq)

        if _lm___l_x__c is not None and __np_q__v_rh in _lm___l_x__c and _lm___l_x__c[__np_q__v_rh] is not None:
            
            _s__o___fm__ = _lm___l_x__c[__np_q__v_rh]
            _s__o___fm__ = _s__o___fm__ + self.m__zli___l_b

            b__u___z_tmq = self.lh_______ysy[_s__o___fm__] if _s__o___fm__ in self.lh_______ysy else None

            if b__u___z_tmq is not None and b__u___z_tmq.value is not None:
                self._et__ia_vcjd = b__u___z_tmq.value.decode(self.nsifr_q_er__)


        uqju_p___qjh = 0x851F
        _cgeo__x__o_ = StandardPropertySet.COMMON

        _n_alqv_t___ = Message.x_t_w_mm____(uqju_p___qjh, _cgeo__x__o_)

        if _lm___l_x__c is not None and _n_alqv_t___ in _lm___l_x__c and _lm___l_x__c[_n_alqv_t___] is not None:
            
            nwrr_eu_nb__ = _lm___l_x__c[_n_alqv_t___]
            nwrr_eu_nb__ = nwrr_eu_nb__ + self.m__zli___l_b

            _vrk_ymyk___ = self.lh_______ysy[nwrr_eu_nb__] if nwrr_eu_nb__ in self.lh_______ysy else None

            if _vrk_ymyk___ is not None and _vrk_ymyk___.value is not None:
                self.____za___j_w = _vrk_ymyk___.value.decode(self.nsifr_q_er__)


        fbnwoszcf___ = 0x8506
        v____l_h____ = StandardPropertySet.COMMON

        ____________ = Message.x_t_w_mm____(fbnwoszcf___, v____l_h____)

        if _lm___l_x__c is not None and ____________ in _lm___l_x__c and _lm___l_x__c[____________] is not None:
            
            k__cc__uw_ke = _lm___l_x__c[____________]
            k__cc__uw_ke = k__cc__uw_ke + "000B"

            _bam__q__gsh = self.lh_______ysy[k__cc__uw_ke] if k__cc__uw_ke in self.lh_______ysy else None

            if _bam__q__gsh is not None and _bam__q__gsh.value is not None:

                _rvc_v__jq__ = int.from_bytes(_bam__q__gsh.value[0:2], "little")
                
                if _rvc_v__jq__ > 0:
                    self._st_____rh_q = True
        

        _uvh_gt__y__ = 0x851C
        zly____gnkf_ = StandardPropertySet.COMMON

        w__uqa_w__r_ = Message.x_t_w_mm____(_uvh_gt__y__, zly____gnkf_)

        if _lm___l_x__c is not None and w__uqa_w__r_ in _lm___l_x__c and _lm___l_x__c[w__uqa_w__r_] is not None:
            
            b__y__fvptzd = _lm___l_x__c[w__uqa_w__r_]
            b__y__fvptzd = b__y__fvptzd + "000B"

            n_v_zmm_v_o_ = self.lh_______ysy[b__y__fvptzd] if b__y__fvptzd in self.lh_______ysy else None

            if n_v_zmm_v_o_ is not None and n_v_zmm_v_o_.value is not None:

                __wri__zm___ = int.from_bytes(n_v_zmm_v_o_.value[0:2], "little")
                
                if __wri__zm___ > 0:
                    self._o__________ = True


        h________d__ = 0x851E
        sb_nzo_ogsqa = StandardPropertySet.COMMON

        _cs_f_e___vt = Message.x_t_w_mm____(h________d__, sb_nzo_ogsqa)

        if _lm___l_x__c is not None and _cs_f_e___vt in _lm___l_x__c and _lm___l_x__c[_cs_f_e___vt] is not None:
            
            __nl__b_x___ = _lm___l_x__c[_cs_f_e___vt]
            __nl__b_x___ = __nl__b_x___ + "000B"

            ____ecj_pb_o = self.lh_______ysy[__nl__b_x___] if __nl__b_x___ in self.lh_______ysy else None

            if ____ecj_pb_o is not None and ____ecj_pb_o.value is not None:

                quet___ux___ = int.from_bytes(____ecj_pb_o.value[0:2], "little")
                
                if quet___ux___ > 0:
                    self.r____dmo__a_ = True


        xgjiot__e___ = 0x820D
        ddv__e_____r = StandardPropertySet.APPOINTMENT

        i___au_pxm__ = Message.x_t_w_mm____(xgjiot__e___, ddv__e_____r)

        if _lm___l_x__c is not None and i___au_pxm__ in _lm___l_x__c and _lm___l_x__c[i___au_pxm__] is not None:
            
            wbc_qq_v____ = _lm___l_x__c[i___au_pxm__]
            wbc_qq_v____ = wbc_qq_v____ + "0040"

            _b_k_____x_l = self.lh_______ysy[wbc_qq_v____] if wbc_qq_v____ in self.lh_______ysy else None

            if _b_k_____x_l is not None and _b_k_____x_l.value is not None:

                __f__qsxa___ = int.from_bytes(_b_k_____x_l.value[0: 4], "little")
                __e_n__w____ = int.from_bytes(_b_k_____x_l.value[4: 8], "little")

                if __e_n__w____ > 0:
                    _fi_km_v____ = __f__qsxa___ + (__e_n__w____ << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)  

                    try:    
                        self.cq_m_axum___ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.cq_m_axum___ = Message.v_____omf__x(self.cq_m_axum___)
                    except:
                        pass 

        ___ww___p_vt = 0x820E
        o_l___ip__nl = StandardPropertySet.APPOINTMENT

        l__y___q__w_ = Message.x_t_w_mm____(___ww___p_vt, o_l___ip__nl)

        if _lm___l_x__c is not None and l__y___q__w_ in _lm___l_x__c and _lm___l_x__c[l__y___q__w_] is not None:
            
            ___y_m__fb_e = _lm___l_x__c[l__y___q__w_]
            ___y_m__fb_e = ___y_m__fb_e + "0040"

            __s_m_lw_t_a = self.lh_______ysy[___y_m__fb_e] if ___y_m__fb_e in self.lh_______ysy else None

            if __s_m_lw_t_a is not None and __s_m_lw_t_a.value is not None:

                _i_mc_____k_ = int.from_bytes(__s_m_lw_t_a.value[0: 4], "little")
                xig_b_r___sv = int.from_bytes(__s_m_lw_t_a.value[4: 8], "little")

                if xig_b_r___sv > 0:
                    _fi_km_v____ = _i_mc_____k_ + (xig_b_r___sv << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)

                    try:    
                        self.zr___i__g_q_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.zr___i__g_q_ = Message.v_____omf__x(self.zr___i__g_q_)
                    except:
                        pass 


        ___p__t_akh_ = 0x8208
        _s___x___qsx = StandardPropertySet.APPOINTMENT

        _fvg___l_kb_ = Message.x_t_w_mm____(___p__t_akh_, _s___x___qsx)

        if _lm___l_x__c is not None and _fvg___l_kb_ in _lm___l_x__c and _lm___l_x__c[_fvg___l_kb_] is not None:
            
            __we_z_fb___ = _lm___l_x__c[_fvg___l_kb_]
            __we_z_fb___ = __we_z_fb___ + self.m__zli___l_b

            _n_e______lt = self.lh_______ysy[__we_z_fb___] if __we_z_fb___ in self.lh_______ysy else None

            if _n_e______lt is not None and _n_e______lt.value is not None:
                self.w_yd__qc_q__ = _n_e______lt.value.decode(self.nsifr_q_er__)


        e__vd____v_u =  0x24
        __s__ke_k_g_ = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5])

        _kt_y_______ = Message.x_t_w_mm____(e__vd____v_u, __s__ke_k_g_)

        if _lm___l_x__c is not None and _kt_y_______ in _lm___l_x__c and _lm___l_x__c[_kt_y_______] is not None:
            
            m__f_h____i_ = _lm___l_x__c[_kt_y_______]
            m__f_h____i_ = m__f_h____i_ + self.m__zli___l_b

            __f__k____dy = self.lh_______ysy[m__f_h____i_] if m__f_h____i_ in self.lh_______ysy else None

            if __f__k____dy is not None and __f__k____dy.value is not None:
                self.h_o_z_mo_h__ = __f__k____dy.value.decode(self.nsifr_q_er__)


        _pwk__siz___ = 0x8234
        _mdf_nz__g__ = StandardPropertySet.APPOINTMENT

        _____kl_d__g = Message.x_t_w_mm____(_pwk__siz___, _mdf_nz__g__)

        if _lm___l_x__c is not None and _____kl_d__g in _lm___l_x__c and _lm___l_x__c[_____kl_d__g] is not None:
            
            __wr__sc_izl = _lm___l_x__c[_____kl_d__g]
            __wr__sc_izl = __wr__sc_izl + self.m__zli___l_b

            twuxoxg_____ = self.lh_______ysy[__wr__sc_izl] if __wr__sc_izl in self.lh_______ysy else None

            if twuxoxg_____ is not None and twuxoxg_____.value is not None:
                self._____egyzai_ = twuxoxg_____.value.decode(self.nsifr_q_er__)


        dfz_mhxy_i_c = 0x8232
        _j____l__hxg = StandardPropertySet.APPOINTMENT

        mqcnn__hqi__ = Message.x_t_w_mm____(dfz_mhxy_i_c, _j____l__hxg)

        if _lm___l_x__c is not None and mqcnn__hqi__ in _lm___l_x__c and _lm___l_x__c[mqcnn__hqi__] is not None:
            
            __r_iv____x_ = _lm___l_x__c[mqcnn__hqi__]
            __r_iv____x_ = __r_iv____x_ + self.m__zli___l_b

            _w___i__x_rb = self.lh_______ysy[__r_iv____x_] if __r_iv____x_ in self.lh_______ysy else None

            if _w___i__x_rb is not None and _w___i__x_rb.value is not None:
                self._vs_t_ntls_l = _w___i__x_rb.value.decode(self.nsifr_q_er__)


        _______m__sg = 0x8216
        lab_is_ru__n = StandardPropertySet.APPOINTMENT

        _c__id__i__f = Message.x_t_w_mm____(_______m__sg, lab_is_ru__n)

        if _lm___l_x__c is not None and _c__id__i__f in _lm___l_x__c and _lm___l_x__c[_c__id__i__f] is not None:
            
            s____pl____t = _lm___l_x__c[_c__id__i__f]
            s____pl____t = s____pl____t + "0102"

            bpcs__di_tu_ = self.lh_______ysy[s____pl____t] if s____pl____t in self.lh_______ysy else None

            if bpcs__di_tu_ is not None and bpcs__di_tu_.value is not None:
                self._s_egzvgujz_ = RecurrencePattern(bpcs__di_tu_.value)


        __ky_q___mma = 0x8116
        x_yo_z__ukai = StandardPropertySet.TASK

        _________jaa = Message.x_t_w_mm____(__ky_q___mma, x_yo_z__ukai)

        if _lm___l_x__c is not None and _________jaa in _lm___l_x__c and _lm___l_x__c[_________jaa] is not None:
            
            k_ojp__l_dbx = _lm___l_x__c[_________jaa]
            k_ojp__l_dbx = k_ojp__l_dbx + "0102"

            itt_ze_n_jgn = self.lh_______ysy[k_ojp__l_dbx] if k_ojp__l_dbx in self.lh_______ysy else None

            if itt_ze_n_jgn is not None and itt_ze_n_jgn.value is not None:
                self.____lg___p__ = RecurrencePattern(itt_ze_n_jgn.value)


        __u_a_w_b__l = 0x8205
        _xjod__mp___ = StandardPropertySet.APPOINTMENT

        tk_pbv_kw_rg = Message.x_t_w_mm____(__u_a_w_b__l, _xjod__mp___)

        if _lm___l_x__c is not None and tk_pbv_kw_rg in _lm___l_x__c and _lm___l_x__c[tk_pbv_kw_rg] is not None:
            
            eh____r_o_t_ = _lm___l_x__c[tk_pbv_kw_rg]
            eh____r_o_t_ = eh____r_o_t_ + "0003"

            __l_x___p___ = self.lh_______ysy[eh____r_o_t_] if eh____r_o_t_ in self.lh_______ysy else None

            if __l_x___p___ is not None and __l_x___p___.value is not None:

                ___m_li_j___ = int.from_bytes(__l_x___p___.value[0:4], "little")

                self.yl__e__fnwt_ = EnumUtil.parse_busy_status(___m_li_j___)


        ___lxe_h_k_w = 0x8217
        m______oni_c = StandardPropertySet.APPOINTMENT

        _revt_____g_ = Message.x_t_w_mm____(___lxe_h_k_w, m______oni_c)

        if _lm___l_x__c is not None and _revt_____g_ in _lm___l_x__c and _lm___l_x__c[_revt_____g_] is not None:
            
            _j__f_______ = _lm___l_x__c[_revt_____g_]
            _j__f_______ = _j__f_______ + "0003"

            w__x__t_u_wn = self.lh_______ysy[_j__f_______] if _j__f_______ in self.lh_______ysy else None

            if w__x__t_u_wn is not None and w__x__t_u_wn.value is not None:

                ___nflfe_msn = int.from_bytes(w__x__t_u_wn.value[0:4], "little")

                self.__w_uoq___s_ = EnumUtil.parse_meeting_status(___nflfe_msn)


        __e___t_eds_ = 0x8218
        _j_o_s__rq__ = StandardPropertySet.APPOINTMENT

        ___h_ww_x_p_ = Message.x_t_w_mm____(__e___t_eds_, _j_o_s__rq__)

        if _lm___l_x__c is not None and ___h_ww_x_p_ in _lm___l_x__c and _lm___l_x__c[___h_ww_x_p_] is not None:
            
            _y__r_y___at = _lm___l_x__c[___h_ww_x_p_]
            _y__r_y___at = _y__r_y___at + "0003"

            _qs_co__pu__ = self.lh_______ysy[_y__r_y___at] if _y__r_y___at in self.lh_______ysy else None

            if _qs_co__pu__ is not None and _qs_co__pu__.value is not None:

                fb____z_m_gc = int.from_bytes(_qs_co__pu__.value[0:4], "little")

                self.____f_kom_m_ = EnumUtil.parse_response_status(fb____z_m_gc)

    
        _w____uvcw_j = 0x8231
        p____hao_t__ = StandardPropertySet.APPOINTMENT

        qqs_____d_w_ = Message.x_t_w_mm____(_w____uvcw_j, p____hao_t__)

        if _lm___l_x__c is not None and qqs_____d_w_ in _lm___l_x__c and _lm___l_x__c[qqs_____d_w_] is not None:
            
            khc_o____ju_ = _lm___l_x__c[qqs_____d_w_]
            khc_o____ju_ = khc_o____ju_ + "0003"

            u__nx_fqjcs_ = self.lh_______ysy[khc_o____ju_] if khc_o____ju_ in self.lh_______ysy else None

            if u__nx_fqjcs_ is not None and u__nx_fqjcs_.value is not None:

                _s__dk__doh_ = int.from_bytes(u__nx_fqjcs_.value[0:4], "little")

                self.___utdtdt_yw = EnumUtil.parse_recurrence_type(_s__dk__doh_)


        d___izw_e___ = 0x3
        _af_z__an___ = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5])

        kd___dxhc___ = Message.x_t_w_mm____(d___izw_e___, _af_z__an___)

        if _lm___l_x__c is not None and kd___dxhc___ in _lm___l_x__c and _lm___l_x__c[kd___dxhc___] is not None:
            
            i_szk_s___dd = _lm___l_x__c[kd___dxhc___]
            i_szk_s___dd = i_szk_s___dd + "0102"

            ___uf___j__y = self.lh_______ysy[i_szk_s___dd] if i_szk_s___dd in self.lh_______ysy else None

            if ___uf___j__y is not None and ___uf___j__y.value is not None:

                self._oi___li_yx_ = ___uf___j__y.value


        r_w_ftder__z = 0x8214
        _q_f_____s_d = StandardPropertySet.APPOINTMENT

        t__l_p_r____ = Message.x_t_w_mm____(r_w_ftder__z, _q_f_____s_d)

        if _lm___l_x__c is not None and t__l_p_r____ in _lm___l_x__c and _lm___l_x__c[t__l_p_r____] is not None:
            
            nmy_xxt___db = _lm___l_x__c[t__l_p_r____]
            nmy_xxt___db = nmy_xxt___db + "0003"

            __g_____zq_c = self.lh_______ysy[nmy_xxt___db] if nmy_xxt___db in self.lh_______ysy else None

            if __g_____zq_c is not None and __g_____zq_c.value is not None:

                self.ls_m_lek_i_c = int.from_bytes(__g_____zq_c.value[0:4], "little")


        g___b_je__v_ = 0x8213
        d_c_beg__f_p = StandardPropertySet.APPOINTMENT

        _q____b_i___ = Message.x_t_w_mm____(g___b_je__v_, d_c_beg__f_p)

        if _lm___l_x__c is not None and _q____b_i___ in _lm___l_x__c and _lm___l_x__c[_q____b_i___] is not None:
            
            __trdn_l_g__ = _lm___l_x__c[_q____b_i___]
            __trdn_l_g__ = __trdn_l_g__ + "0003"

            __j_o_xa____ = self.lh_______ysy[__trdn_l_g__] if __trdn_l_g__ in self.lh_______ysy else None

            if __j_o_xa____ is not None and __j_o_xa____.value is not None:

                self.j__vi__y_vh_ = int.from_bytes(__j_o_xa____.value[0:4], "little")


        vs_________x = 0x811F
        m_l_pfxh____ = StandardPropertySet.TASK

        t___n_n_jfn_ = Message.x_t_w_mm____(vs_________x, m_l_pfxh____)

        if _lm___l_x__c is not None and t___n_n_jfn_ in _lm___l_x__c and _lm___l_x__c[t___n_n_jfn_] is not None:
            
            f_byiyl_e_f_ = _lm___l_x__c[t___n_n_jfn_]
            f_byiyl_e_f_ = f_byiyl_e_f_ + self.m__zli___l_b

            ___x_aulj__i = self.lh_______ysy[f_byiyl_e_f_] if f_byiyl_e_f_ in self.lh_______ysy else None

            if ___x_aulj__i is not None and ___x_aulj__i.value is not None:

                self.ug__bxm__u__ = ___x_aulj__i.value.decode(self.nsifr_q_er__)


        _____vd___fi = 0x8121
        cs_xl___q__c = StandardPropertySet.TASK

        _de__am____s = Message.x_t_w_mm____(_____vd___fi, cs_xl___q__c)

        if _lm___l_x__c is not None and _de__am____s in _lm___l_x__c and _lm___l_x__c[_de__am____s] is not None:
            
            jegyr_jrl___ = _lm___l_x__c[_de__am____s]
            jegyr_jrl___ = jegyr_jrl___ + self.m__zli___l_b

            ___ydzf_____ = self.lh_______ysy[jegyr_jrl___] if jegyr_jrl___ in self.lh_______ysy else None

            if ___ydzf_____ is not None and ___ydzf_____.value is not None:

                self._dznn_vo__f_ = ___ydzf_____.value.decode(self.nsifr_q_er__)


        __mu_i__ibcn = 0x8102
        ______n___wx = StandardPropertySet.TASK

        __r___l_vlll = Message.x_t_w_mm____(__mu_i__ibcn, ______n___wx)

        if _lm___l_x__c is not None and __r___l_vlll in _lm___l_x__c and _lm___l_x__c[__r___l_vlll] is not None:
            
            d_zucy______ = _lm___l_x__c[__r___l_vlll]
            d_zucy______ = d_zucy______ + "0005"

            m__i____h_rw = self.lh_______ysy[d_zucy______] if d_zucy______ in self.lh_______ysy else None

            if m__i____h_rw is not None and m__i____h_rw.value is not None:

                ______e_z_sp = struct.unpack('<d', m__i____h_rw.value[0:8])

                if ______e_z_sp is not None:
                    self.cw_z___z____ = ______e_z_sp[0]
                  
                
        _mno_e__yu__ = 0x8110
        uoouynk_b___ = StandardPropertySet.TASK

        s__rczf____r = Message.x_t_w_mm____(_mno_e__yu__, uoouynk_b___)

        if _lm___l_x__c is not None and s__rczf____r in _lm___l_x__c and _lm___l_x__c[s__rczf____r] is not None:
            
            u____kqc__cc = _lm___l_x__c[s__rczf____r]
            u____kqc__cc = u____kqc__cc + "0003"

            _z______dv_w = self.lh_______ysy[u____kqc__cc] if u____kqc__cc in self.lh_______ysy else None

            if _z______dv_w is not None and _z______dv_w.value is not None:

                self.__c_q_q____g = int.from_bytes(_z______dv_w.value[0:4], "little")


        f_um_pk__c_m = 0x8111
        _l____lt__e_ = StandardPropertySet.TASK

        _yec_c_cgmn_ = Message.x_t_w_mm____(f_um_pk__c_m, _l____lt__e_)

        if _lm___l_x__c is not None and _yec_c_cgmn_ in _lm___l_x__c and _lm___l_x__c[_yec_c_cgmn_] is not None:
            
            _szo_w___t__ = _lm___l_x__c[_yec_c_cgmn_]
            _szo_w___t__ = _szo_w___t__ + "0003"

            jg___n_t_n__ = self.lh_______ysy[_szo_w___t__] if _szo_w___t__ in self.lh_______ysy else None

            if jg___n_t_n__ is not None and jg___n_t_n__.value is not None:

                self.kk____qaf_je = int.from_bytes(jg___n_t_n__.value[0:4], "little")


        _jts__x_ojqd = 0x8103
        bcmixshei_y_ = StandardPropertySet.TASK

        __w__l_yi__k = Message.x_t_w_mm____(_jts__x_ojqd, bcmixshei_y_)

        if _lm___l_x__c is not None and __w__l_yi__k in _lm___l_x__c and _lm___l_x__c[__w__l_yi__k] is not None:
            
            __yfpje_zx__ = _lm___l_x__c[__w__l_yi__k]
            __yfpje_zx__ = __yfpje_zx__ + "000B"

            ad_sug_fq_ns = self.lh_______ysy[__yfpje_zx__] if __yfpje_zx__ in self.lh_______ysy else None

            if ad_sug_fq_ns is not None and ad_sug_fq_ns.value is not None:

                is_team_value = int.from_bytes(ad_sug_fq_ns.value[0:2], "little")

                if is_team_value > 0:
                    self.hd____j__j__ = True


        ____c_sp_hld = 0x811C
        n_b_k____ea_ = StandardPropertySet.TASK

        _____t_nm_y_ = Message.x_t_w_mm____(____c_sp_hld, n_b_k____ea_)

        if _lm___l_x__c is not None and _____t_nm_y_ in _lm___l_x__c and _lm___l_x__c[_____t_nm_y_] is not None:
            
            vekfka__aml_ = _lm___l_x__c[_____t_nm_y_]
            vekfka__aml_ = vekfka__aml_ + "000B"

            _x__mdz_____ = self.lh_______ysy[vekfka__aml_] if vekfka__aml_ in self.lh_______ysy else None

            if _x__mdz_____ is not None and _x__mdz_____.value is not None:

                k_rm________ = int.from_bytes(_x__mdz_____.value[0:2], "little")

                if k_rm________ > 0:
                    self._s__y_pbgfp_ = True


        vxbn__h_at__ = 0x8223
        se_g____amt_ = StandardPropertySet.APPOINTMENT

        _lt__h______ = Message.x_t_w_mm____(vxbn__h_at__, se_g____amt_)

        if _lm___l_x__c is not None and _lt__h______ in _lm___l_x__c and _lm___l_x__c[_lt__h______] is not None:
            
            _ewb_og__rs_ = _lm___l_x__c[_lt__h______]
            _ewb_og__rs_ = _ewb_og__rs_ + "000B"

            lp____fv_iu_ = self.lh_______ysy[_ewb_og__rs_] if _ewb_og__rs_ in self.lh_______ysy else None

            if lp____fv_iu_ is not None and lp____fv_iu_.value is not None:

                wos__cc___wu = int.from_bytes(lp____fv_iu_.value[0:2], "little")

                if wos__cc___wu > 0:
                    self.do_jfaa_bk__ = True


        __rp_icd__h_ = 0x8215
        as_w___e__i_ = StandardPropertySet.APPOINTMENT

        _hus__fvxf__ = Message.x_t_w_mm____(__rp_icd__h_, as_w___e__i_)

        if _lm___l_x__c is not None and _hus__fvxf__ in _lm___l_x__c and _lm___l_x__c[_hus__fvxf__] is not None:
            
            __l___l_mpdr = _lm___l_x__c[_hus__fvxf__]
            __l___l_mpdr = __l___l_mpdr + "000B"

            _hw_ziipqpla = self.lh_______ysy[__l___l_mpdr] if __l___l_mpdr in self.lh_______ysy else None

            if _hw_ziipqpla is not None and _hw_ziipqpla.value is not None:

                o_d_b___b_s_ = int.from_bytes(_hw_ziipqpla.value[0:2], "little")

                if o_d_b___b_s_ > 0:
                    self.__e_r_tsv_av = True


        __mps_p___j_ = 0x8503
        __dm___ql_ra = StandardPropertySet.COMMON

        j______bamlp = Message.x_t_w_mm____(__mps_p___j_, __dm___ql_ra)

        if _lm___l_x__c is not None and j______bamlp in _lm___l_x__c and _lm___l_x__c[j______bamlp] is not None:
            
            ___iozw__d__ = _lm___l_x__c[j______bamlp]
            ___iozw__d__ = ___iozw__d__ + "000B"

            ms_uh__rvzgb = self.lh_______ysy[___iozw__d__] if ___iozw__d__ in self.lh_______ysy else None

            if ms_uh__rvzgb is not None and ms_uh__rvzgb.value is not None:

                _kq__wx_____ = int.from_bytes(ms_uh__rvzgb.value[0:2], "little")

                if _kq__wx_____ > 0:
                    self.__kdt_j__kw_ = True


        __e_q_pvgx__ = 0x8502
        mcnm_fdvnojx = StandardPropertySet.COMMON

        __rq__j__m_v = Message.x_t_w_mm____(__e_q_pvgx__, mcnm_fdvnojx)

        if _lm___l_x__c is not None and __rq__j__m_v in _lm___l_x__c and _lm___l_x__c[__rq__j__m_v] is not None:
            
            _kc___xmi_qv = _lm___l_x__c[__rq__j__m_v]
            _kc___xmi_qv = _kc___xmi_qv + "0040"

            y_d___i_____ = self.lh_______ysy[_kc___xmi_qv] if _kc___xmi_qv in self.lh_______ysy else None

            if y_d___i_____ is not None and y_d___i_____.value is not None:

                __r_b_____go = int.from_bytes(y_d___i_____.value[0: 4], "little")
                e___tdyc__q_ = int.from_bytes(y_d___i_____.value[4: 8], "little")

                if e___tdyc__q_ > 0:
                    _fi_km_v____ = __r_b_____go + (e___tdyc__q_ << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)      

                    try:    
                        self._______vx_ok = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self._______vx_ok = Message.v_____omf__x(self._______vx_ok)
                    except:
                        pass 


        ba_fu_rf_d_l = 0x8501
        jy_n_t_jtt_h = StandardPropertySet.COMMON

        ws_b_q___rn_ = Message.x_t_w_mm____(ba_fu_rf_d_l, jy_n_t_jtt_h)

        if _lm___l_x__c is not None and ws_b_q___rn_ in _lm___l_x__c and _lm___l_x__c[ws_b_q___rn_] is not None:
            
            __bmsc_____x = _lm___l_x__c[ws_b_q___rn_]
            __bmsc_____x = __bmsc_____x + "0003"

            __a____mtal_ = self.lh_______ysy[__bmsc_____x] if __bmsc_____x in self.lh_______ysy else None

            if __a____mtal_ is not None and __a____mtal_.value is not None:

                self.__qhz__ecaho = int.from_bytes(__a____mtal_.value[0:4], "little")


        _lkgno______ = 0x8104
        hl_gs_ma____ = StandardPropertySet.TASK

        fv__f___r__n = Message.x_t_w_mm____(_lkgno______, hl_gs_ma____)

        if _lm___l_x__c is not None and fv__f___r__n in _lm___l_x__c and _lm___l_x__c[fv__f___r__n] is not None:
            
            j__t_u_a_f_k = _lm___l_x__c[fv__f___r__n]
            j__t_u_a_f_k = j__t_u_a_f_k + "0040"

            ______tu_xn_ = self.lh_______ysy[j__t_u_a_f_k] if j__t_u_a_f_k in self.lh_______ysy else None

            if ______tu_xn_ is not None and ______tu_xn_.value is not None:

                _____a_____r = int.from_bytes(______tu_xn_.value[0: 4], "little")
                kqw_l_______ = int.from_bytes(______tu_xn_.value[4: 8], "little")

                if kqw_l_______ > 0:
                    _fi_km_v____ = _____a_____r + (kqw_l_______ << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)   

                    try:    
                        self.kn_va_____zr = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.kn_va_____zr = Message.v_____omf__x(self.kn_va_____zr)
                    except:
                        pass 


        __w______h__ = 0x8105
        __d_k_ak_e_k = StandardPropertySet.TASK

        _ab_k___d_km = Message.x_t_w_mm____(__w______h__, __d_k_ak_e_k)

        if _lm___l_x__c is not None and _ab_k___d_km in _lm___l_x__c and _lm___l_x__c[_ab_k___d_km] is not None:
            
            _jw__p__d___ = _lm___l_x__c[_ab_k___d_km]
            _jw__p__d___ = _jw__p__d___ + "0040"

            tsfkn___b___ = self.lh_______ysy[_jw__p__d___] if _jw__p__d___ in self.lh_______ysy else None

            if tsfkn___b___ is not None and tsfkn___b___.value is not None:

                __a__a__bb_p = int.from_bytes(tsfkn___b___.value[0: 4], "little")
                ______a_h_sv = int.from_bytes(tsfkn___b___.value[4: 8], "little")

                if ______a_h_sv > 0:
                    _fi_km_v____ = __a__a__bb_p + (______a_h_sv << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)  

                    try:    
                        self.drg_hha_bdef = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.drg_hha_bdef = Message.v_____omf__x(self.drg_hha_bdef)
                    except:
                        pass 


        aeom__whcxej = 0x810F
        sux_o_i_e__z = StandardPropertySet.TASK

        z_fj_wj_h_lm = Message.x_t_w_mm____(aeom__whcxej, sux_o_i_e__z)

        if _lm___l_x__c is not None and z_fj_wj_h_lm in _lm___l_x__c and _lm___l_x__c[z_fj_wj_h_lm] is not None:
            
            kv___jp_dc__ = _lm___l_x__c[z_fj_wj_h_lm]
            kv___jp_dc__ = kv___jp_dc__ + "0040"

            c__zbvis_a__ = self.lh_______ysy[kv___jp_dc__] if kv___jp_dc__ in self.lh_______ysy else None

            if c__zbvis_a__ is not None and c__zbvis_a__.value is not None:

                _____h__zk_o = int.from_bytes(c__zbvis_a__.value[0: 4], "little")
                _ws___zz_ecv = int.from_bytes(c__zbvis_a__.value[4: 8], "little")

                if _ws___zz_ecv > 0:
                    _fi_km_v____ = _____h__zk_o + (_ws___zz_ecv << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)

                    try:    
                        self._il_______cr = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self._il_______cr = Message.v_____omf__x(self._il_______cr)
                    except:
                        pass


        __mnnceo_i_t = 0x8101
        q___hy_a_n__ = StandardPropertySet.TASK

        __pwn_v_ope_ = Message.x_t_w_mm____(__mnnceo_i_t, q___hy_a_n__)

        if _lm___l_x__c is not None and __pwn_v_ope_ in _lm___l_x__c and _lm___l_x__c[__pwn_v_ope_] is not None:
            
            t_a_ff__epm_ = _lm___l_x__c[__pwn_v_ope_]
            t_a_ff__epm_ = t_a_ff__epm_ + "0003"

            ____y_cpvee_ = self.lh_______ysy[t_a_ff__epm_] if t_a_ff__epm_ in self.lh_______ysy else None

            if ____y_cpvee_ is not None and ____y_cpvee_.value is not None:

                _____dd_v___ = int.from_bytes(____y_cpvee_.value[0:4], "little")

                self.____ueit___l = EnumUtil.parse_task_status(_____dd_v___)


        dz_s_______r = 0x8129
        o__b__y_uoh_ = StandardPropertySet.TASK

        ___m_qn_____ = Message.x_t_w_mm____(dz_s_______r, o__b__y_uoh_)

        if _lm___l_x__c is not None and ___m_qn_____ in _lm___l_x__c and _lm___l_x__c[___m_qn_____] is not None:
            
            __bk_ajmaw__ = _lm___l_x__c[___m_qn_____]
            __bk_ajmaw__ = __bk_ajmaw__ + "0003"

            _______a_f_q = self.lh_______ysy[__bk_ajmaw__] if __bk_ajmaw__ in self.lh_______ysy else None

            if _______a_f_q is not None and _______a_f_q.value is not None:

                a__is_dk_p__ = int.from_bytes(_______a_f_q.value[0:4], "little")

                self.p__f_s_____t = EnumUtil.parse_task_ownership(a__is_dk_p__)


        _e_o______d_ = 0x812A
        _mfnir___r__ = StandardPropertySet.TASK

        ______q_____ = Message.x_t_w_mm____(_e_o______d_, _mfnir___r__)

        if _lm___l_x__c is not None and ______q_____ in _lm___l_x__c and _lm___l_x__c[______q_____] is not None:
            
            bt___w_omw_o = _lm___l_x__c[______q_____]
            bt___w_omw_o = bt___w_omw_o + "0003"

            __oja__qn__d = self.lh_______ysy[bt___w_omw_o] if bt___w_omw_o in self.lh_______ysy else None

            if __oja__qn__d is not None and __oja__qn__d.value is not None:

                _o__e___i___ = int.from_bytes(__oja__qn__d.value[0:4], "little")

                self._c__v___wqqb = EnumUtil.parse_task_delegation_state(_o__e___i___)


        c_ua___y_y__ = 0x8B05
        cp__rj_l__ho = StandardPropertySet.NOTE

        u__bws__v_sz = Message.x_t_w_mm____(c_ua___y_y__, cp__rj_l__ho)

        if _lm___l_x__c is not None and u__bws__v_sz in _lm___l_x__c and _lm___l_x__c[u__bws__v_sz] is not None:
            
            o_ujzr__j__j = _lm___l_x__c[u__bws__v_sz]
            o_ujzr__j__j = o_ujzr__j__j + "0003"

            _gc___n_w_m_ = self.lh_______ysy[o_ujzr__j__j] if o_ujzr__j__j in self.lh_______ysy else None

            if _gc___n_w_m_ is not None and _gc___n_w_m_.value is not None:

                self.om_u__xna_q_ = int.from_bytes(_gc___n_w_m_.value[0:4], "little")


        ___v__z_pt__ = 0x8B04
        __z__e__qoh_ = StandardPropertySet.NOTE

        b__e_eoec_c_ = Message.x_t_w_mm____(___v__z_pt__, __z__e__qoh_)

        if _lm___l_x__c is not None and b__e_eoec_c_ in _lm___l_x__c and _lm___l_x__c[b__e_eoec_c_] is not None:
            
            __f_tkxbw_bg = _lm___l_x__c[b__e_eoec_c_]
            __f_tkxbw_bg = __f_tkxbw_bg + "0003"

            th__d___wc_w = self.lh_______ysy[__f_tkxbw_bg] if __f_tkxbw_bg in self.lh_______ysy else None

            if th__d___wc_w is not None and th__d___wc_w.value is not None:

                self.__no__s_vsl_ = int.from_bytes(th__d___wc_w.value[0:4], "little")


        _heri_j_np__ = 0x8B03
        _f__j_rilrr_ = StandardPropertySet.NOTE

        sel__vdnkdfs = Message.x_t_w_mm____(_heri_j_np__, _f__j_rilrr_)

        if _lm___l_x__c is not None and sel__vdnkdfs in _lm___l_x__c and _lm___l_x__c[sel__vdnkdfs] is not None:
            
            i____rr___r_ = _lm___l_x__c[sel__vdnkdfs]
            i____rr___r_ = i____rr___r_ + "0003"

            ___b__k_____ = self.lh_______ysy[i____rr___r_] if i____rr___r_ in self.lh_______ysy else None

            if ___b__k_____ is not None and ___b__k_____.value is not None:

                self.qi______kjo_ = int.from_bytes(___b__k_____.value[0:4], "little")


        ykibj_w___w_ = 0x8B02
        sxpk___l_j__ = StandardPropertySet.NOTE

        _y_u_assmrg_ = Message.x_t_w_mm____(ykibj_w___w_, sxpk___l_j__)

        if _lm___l_x__c is not None and _y_u_assmrg_ in _lm___l_x__c and _lm___l_x__c[_y_u_assmrg_] is not None:
            
            m_ujs______o = _lm___l_x__c[_y_u_assmrg_]
            m_ujs______o = m_ujs______o + "0003"

            _p_bbn_yc__j = self.lh_______ysy[m_ujs______o] if m_ujs______o in self.lh_______ysy else None

            if _p_bbn_yc__j is not None and _p_bbn_yc__j.value is not None:

                self.g__tp___yb__ = int.from_bytes(_p_bbn_yc__j.value[0:4], "little")


        __uqn_xk____ = 0x8B00
        ___y___yo__n = StandardPropertySet.NOTE

        ks__p__m__hf = Message.x_t_w_mm____(__uqn_xk____, ___y___yo__n)

        if _lm___l_x__c is not None and ks__p__m__hf in _lm___l_x__c and _lm___l_x__c[ks__p__m__hf] is not None:
            
            i_____pxz_c_ = _lm___l_x__c[ks__p__m__hf]
            i_____pxz_c_ = i_____pxz_c_ + "0003"

            _oi_coj_____ = self.lh_______ysy[i_____pxz_c_] if i_____pxz_c_ in self.lh_______ysy else None

            if _oi_coj_____ is not None and _oi_coj_____.value is not None:

                self.j____bexpm__ = int.from_bytes(_oi_coj_____.value[0:4], "little")


        t_bi_p_l___m = 0x8706
        hj_g_jm_omsc = StandardPropertySet.JOURNAL

        ___w_amh_gaw = Message.x_t_w_mm____(t_bi_p_l___m, hj_g_jm_omsc)

        if _lm___l_x__c is not None and ___w_amh_gaw in _lm___l_x__c and _lm___l_x__c[___w_amh_gaw] is not None:
            
            _c__n_iy_o__ = _lm___l_x__c[___w_amh_gaw]
            _c__n_iy_o__ = _c__n_iy_o__ + "0040"

            f_______pq_b = self.lh_______ysy[_c__n_iy_o__] if _c__n_iy_o__ in self.lh_______ysy else None

            if f_______pq_b is not None and f_______pq_b.value is not None:

                _x_y___a_dv_ = int.from_bytes(f_______pq_b.value[0: 4], "little")
                __vyp__c__m_ = int.from_bytes(f_______pq_b.value[4: 8], "little")

                if __vyp__c__m_ > 0:
                    _fi_km_v____ = _x_y___a_dv_ + (__vyp__c__m_ << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)

                    try:    
                        self.__i_b_kq_iap = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.__i_b_kq_iap = Message.v_____omf__x(self.__i_b_kq_iap)
                    except:
                        pass 

        tp_pwh_g__uj = 0x8708
        ky____emm__a = StandardPropertySet.JOURNAL

        ___zs___m___ = Message.x_t_w_mm____(tp_pwh_g__uj, ky____emm__a)

        if _lm___l_x__c is not None and ___zs___m___ in _lm___l_x__c and _lm___l_x__c[___zs___m___] is not None:
            
            _s_tt_i__m_b = _lm___l_x__c[___zs___m___]
            _s_tt_i__m_b = _s_tt_i__m_b + "0040"

            _________g__ = self.lh_______ysy[_s_tt_i__m_b] if _s_tt_i__m_b in self.lh_______ysy else None

            if _________g__ is not None and _________g__.value is not None:

                q_q_vnrba_qy = int.from_bytes(_________g__.value[0: 4], "little")
                a_m__o___b__ = int.from_bytes(_________g__.value[4: 8], "little")

                if a_m__o___b__ > 0:
                    _fi_km_v____ = q_q_vnrba_qy + (a_m__o___b__ << 32)
                    jgv__c_h___y = datetime.datetime(1601,1,1)

                    try:    
                        self.rq__k____jkt = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                        self.rq__k____jkt = Message.v_____omf__x(self.rq__k____jkt)
                    except:
                        pass 


        ___c__tqa_w_ = 0x8700
        _a_luq____pl = StandardPropertySet.JOURNAL

        v_r___llrb_w = Message.x_t_w_mm____(___c__tqa_w_, _a_luq____pl)

        if _lm___l_x__c is not None and v_r___llrb_w in _lm___l_x__c and _lm___l_x__c[v_r___llrb_w] is not None:
            
            u__f_as_j__s = _lm___l_x__c[v_r___llrb_w]
            u__f_as_j__s = u__f_as_j__s + self.m__zli___l_b

            d_____rb_b_n = self.lh_______ysy[u__f_as_j__s] if u__f_as_j__s in self.lh_______ysy else None

            if d_____rb_b_n is not None and d_____rb_b_n.value is not None:

                self._s______z_yx = d_____rb_b_n.value.decode(self.nsifr_q_er__)

        
        __d__ob_____ = 0x8712
        _h_o_siyb___ = StandardPropertySet.JOURNAL

        _s__o_pc_ux_ = Message.x_t_w_mm____(__d__ob_____, _h_o_siyb___)

        if _lm___l_x__c is not None and _s__o_pc_ux_ in _lm___l_x__c and _lm___l_x__c[_s__o_pc_ux_] is not None:
            
            _l_y_je_x_n_ = _lm___l_x__c[_s__o_pc_ux_]
            _l_y_je_x_n_ = _l_y_je_x_n_ + self.m__zli___l_b

            _s__n_______ = self.lh_______ysy[_l_y_je_x_n_] if _l_y_je_x_n_ in self.lh_______ysy else None

            if _s__n_______ is not None and _s__n_______.value is not None:

                self.va_uignshqy_ = _s__n_______.value.decode(self.nsifr_q_er__)


        ___f_____o__ = 0x8707
        cb__fp__n__e = StandardPropertySet.JOURNAL

        ______wf____ = Message.x_t_w_mm____(___f_____o__, cb__fp__n__e)

        if _lm___l_x__c is not None and ______wf____ in _lm___l_x__c and _lm___l_x__c[______wf____] is not None:
            
            ____k_w__so_ = _lm___l_x__c[______wf____]
            ____k_w__so_ = ____k_w__so_ + "0003"

            butkxg__edxj = self.lh_______ysy[____k_w__so_] if ____k_w__so_ in self.lh_______ysy else None

            if butkxg__edxj is not None and butkxg__edxj.value is not None:

                self._jnlqe_____v = int.from_bytes(butkxg__edxj.value[0:4], "little")


        ______fuz_ii = self.lh_______ysy["3A420040"] if "3A420040" in self.lh_______ysy else None

        if ______fuz_ii is not None and ______fuz_ii.value is not None:

            ___du___qiwd = int.from_bytes(______fuz_ii.value[0: 4], "little")
            __ji_w_l__v_ = int.from_bytes(______fuz_ii.value[4: 8], "little")

            if __ji_w_l__v_ > 0:
                _fi_km_v____ = ___du___qiwd + (__ji_w_l__v_ << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)     

                try:    
                    self.hsu__s____k_ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.hsu__s____k_ = Message.v_____omf__x(self.hsu__s____k_)
                except:
                    pass 


        _yhm____fo_x = self.lh_______ysy["3A58" + self.h______id_ai] if "3A58" + self.h______id_ai in self.lh_______ysy else None

        if _yhm____fo_x is not None and _yhm____fo_x.value is not None:

            _u_k_ho_x__y = int(_yhm____fo_x.size / 4)

            self._v__e__f____ = []

            for i in range(_u_k_ho_x__y):

                mok_o__e_wpq = "__substg1.0_3A58" + self.h______id_ai + "-" + str.format("{:08X}", i)

                qew__vs_j_hm = vi_h__c____n.get_entry(mok_o__e_wpq)

                if qew__vs_j_hm is not None and qew__vs_j_hm.buffer is not None:

                    ________g_i_ = qew__vs_j_hm.buffer[0: len(qew__vs_j_hm.buffer) - x_m_sky_gz__].decode(self.nsifr_q_er__)
                    self._v__e__f____.append(________g_i_)


        aubugl_np__n = self.lh_______ysy["3A410040"] if "3A410040" in self.lh_______ysy else None

        if aubugl_np__n is not None and aubugl_np__n.value is not None:

            _l_s__h_cki_ = int.from_bytes(aubugl_np__n.value[0: 4], "little")
            _____dv_cidn = int.from_bytes(aubugl_np__n.value[4: 8], "little")

            if _____dv_cidn > 0:
                _fi_km_v____ = _l_s__h_cki_ + (_____dv_cidn << 32)
                jgv__c_h___y = datetime.datetime(1601,1,1)   

                try:    
                    self.__g___vgx_da = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                    self.__g___vgx_da = Message.v_____omf__x(self.__g___vgx_da)
                except:
                    pass 

        _co___r__lyc = self.lh_______ysy["3A4D0002"] if "3A4D0002" in self.lh_______ysy else None

        if _co___r__lyc is not None and _co___r__lyc.value is not None:

            r_bf_v_zppm_ = int.from_bytes(_co___r__lyc.value[0:4], "little")

            self.o_y_e___dh__ = EnumUtil.parse_gender(r_bf_v_zppm_)


        uo_v_u__e_e_ = 0x8022
        ____b_n_gucz = StandardPropertySet.ADDRESS

        o_o_eyaojpum = Message.x_t_w_mm____(uo_v_u__e_e_, ____b_n_gucz)

        if _lm___l_x__c is not None and o_o_eyaojpum in _lm___l_x__c and _lm___l_x__c[o_o_eyaojpum] is not None:
            
            _v___h_x_z__ = _lm___l_x__c[o_o_eyaojpum]
            _v___h_x_z__ = _v___h_x_z__ + "0003"

            ___________n = self.lh_______ysy[_v___h_x_z__] if _v___h_x_z__ in self.lh_______ysy else None

            if ___________n is not None and ___________n.value is not None:

                _ao_r__m_de_ = int.from_bytes(___________n.value[0:4], "little")

                self._______w_a__ = EnumUtil.parse_selected_mailing_address(_ao_r__m_de_)


        e_a____h___v = 0x8015
        unfw_y_____y = StandardPropertySet.ADDRESS

        _____l_hus__ = Message.x_t_w_mm____(e_a____h___v, unfw_y_____y)

        if _lm___l_x__c is not None and _____l_hus__ in _lm___l_x__c and _lm___l_x__c[_____l_hus__] is not None:
            
            l__ezfd__g__ = _lm___l_x__c[_____l_hus__]
            l__ezfd__g__ = l__ezfd__g__ + "000B"

            yjn___z_l__s = self.lh_______ysy[l__ezfd__g__] if l__ezfd__g__ in self.lh_______ysy else None

            if yjn___z_l__s is not None and yjn___z_l__s.value is not None:

                pg__x____ymx = int.from_bytes(yjn___z_l__s.value[0:2], "little")

                if pg__x____ymx > 0:
                    self.__pj_e__hzgb = True

        cax_c_ne_uk_ = 0x8005
        ______lm_w_t = StandardPropertySet.ADDRESS

        q__xb_______ = Message.x_t_w_mm____(cax_c_ne_uk_, ______lm_w_t)

        if _lm___l_x__c is not None and q__xb_______ in _lm___l_x__c and _lm___l_x__c[q__xb_______] is not None:
            
            __j_b____jxi = _lm___l_x__c[q__xb_______]
            __j_b____jxi = __j_b____jxi + self.m__zli___l_b

            ratz_c_j____ = self.lh_______ysy[__j_b____jxi] if __j_b____jxi in self.lh_______ysy else None

            if ratz_c_j____ is not None and ratz_c_j____.value is not None:

                self.a____h_d_m__ = ratz_c_j____.value.decode(self.nsifr_q_er__)


        __hs_h___x__ = 0x8062
        _ns_tn_wzr__ = StandardPropertySet.ADDRESS

        lxznw___bfjj = Message.x_t_w_mm____(__hs_h___x__, _ns_tn_wzr__)

        if _lm___l_x__c is not None and lxznw___bfjj in _lm___l_x__c and _lm___l_x__c[lxznw___bfjj] is not None:
            
            __m__wn__h_e = _lm___l_x__c[lxznw___bfjj]
            __m__wn__h_e = __m__wn__h_e + self.m__zli___l_b

            _tzpzvps__p_ = self.lh_______ysy[__m__wn__h_e] if __m__wn__h_e in self.lh_______ysy else None

            if _tzpzvps__p_ is not None and _tzpzvps__p_.value is not None:

                self.___p___m_x__ = _tzpzvps__p_.value.decode(self.nsifr_q_er__)


        n__wpe___iws = 0x80D8
        ____kf__p_pg = StandardPropertySet.ADDRESS

        ___q_brfyr__ = Message.x_t_w_mm____(n__wpe___iws, ____kf__p_pg)

        if _lm___l_x__c is not None and ___q_brfyr__ in _lm___l_x__c and _lm___l_x__c[___q_brfyr__] is not None:
            
            __nvm_x__vli = _lm___l_x__c[___q_brfyr__]
            __nvm_x__vli = __nvm_x__vli + self.m__zli___l_b

            ___bmzl___fp = self.lh_______ysy[__nvm_x__vli] if __nvm_x__vli in self.lh_______ysy else None

            if ___bmzl___fp is not None and ___bmzl___fp.value is not None:

                self.a__yb______q = ___bmzl___fp.value.decode(self.nsifr_q_er__)


        ry__________ = 0x801B
        eh_tt_x_fg__ = StandardPropertySet.ADDRESS

        __k_tfgwvuz_ = Message.x_t_w_mm____(ry__________, eh_tt_x_fg__)

        if _lm___l_x__c is not None and __k_tfgwvuz_ in _lm___l_x__c and _lm___l_x__c[__k_tfgwvuz_] is not None:
            
            _h_ac___r_z_ = _lm___l_x__c[__k_tfgwvuz_]
            _h_ac___r_z_ = _h_ac___r_z_ + self.m__zli___l_b

            _lcbvddqo___ = self.lh_______ysy[_h_ac___r_z_] if _h_ac___r_z_ in self.lh_______ysy else None

            if _lcbvddqo___ is not None and _lcbvddqo___.value is not None:

                self._in__an_yv__ = _lcbvddqo___.value.decode(self.nsifr_q_er__)


        x_f_l_____qn = 0x8045
        _____x__eqa_ = StandardPropertySet.ADDRESS

        ix_eztaf_pdc = Message.x_t_w_mm____(x_f_l_____qn, _____x__eqa_)

        if _lm___l_x__c is not None and ix_eztaf_pdc in _lm___l_x__c and _lm___l_x__c[ix_eztaf_pdc] is not None:
            
            ____f_____r_ = _lm___l_x__c[ix_eztaf_pdc]
            ____f_____r_ = ____f_____r_ + self.m__zli___l_b

            nb__ni__so__ = self.lh_______ysy[____f_____r_] if ____f_____r_ in self.lh_______ysy else None

            if nb__ni__so__ is not None and nb__ni__so__.value is not None:

                self._q___u__q_u_ = nb__ni__so__.value.decode(self.nsifr_q_er__)


        b_ox_____b_t = 0x8046
        _z__cy____a_ = StandardPropertySet.ADDRESS

        jn____dzfuw_ = Message.x_t_w_mm____(b_ox_____b_t, _z__cy____a_)

        if _lm___l_x__c is not None and jn____dzfuw_ in _lm___l_x__c and _lm___l_x__c[jn____dzfuw_] is not None:
            
            _j__v____g_q = _lm___l_x__c[jn____dzfuw_]
            _j__v____g_q = _j__v____g_q + self.m__zli___l_b

            xpa__y___h__ = self.lh_______ysy[_j__v____g_q] if _j__v____g_q in self.lh_______ysy else None

            if xpa__y___h__ is not None and xpa__y___h__.value is not None:

                self.g_k_____pg__ = xpa__y___h__.value.decode(self.nsifr_q_er__)


        _qasz__q__t_ = 0x8047
        __t__ri__gh_ = StandardPropertySet.ADDRESS

        zderr___i_nh = Message.x_t_w_mm____(_qasz__q__t_, __t__ri__gh_)

        if _lm___l_x__c is not None and zderr___i_nh in _lm___l_x__c and _lm___l_x__c[zderr___i_nh] is not None:
            
            r___fr__nurj = _lm___l_x__c[zderr___i_nh]
            r___fr__nurj = r___fr__nurj + self.m__zli___l_b

            rh_f_fcio_xp = self.lh_______ysy[r___fr__nurj] if r___fr__nurj in self.lh_______ysy else None

            if rh_f_fcio_xp is not None and rh_f_fcio_xp.value is not None:

                self.__dyk_vx_w__ = rh_f_fcio_xp.value.decode(self.nsifr_q_er__)


        zi_____cg_t_ = 0x8048
        dc_sy__p__fx = StandardPropertySet.ADDRESS

        ___t_oz__hek = Message.x_t_w_mm____(zi_____cg_t_, dc_sy__p__fx)

        if _lm___l_x__c is not None and ___t_oz__hek in _lm___l_x__c and _lm___l_x__c[___t_oz__hek] is not None:
            
            y_anv_____j_ = _lm___l_x__c[___t_oz__hek]
            y_anv_____j_ = y_anv_____j_ + self.m__zli___l_b

            _vjuuo_k_qp_ = self.lh_______ysy[y_anv_____j_] if y_anv_____j_ in self.lh_______ysy else None

            if _vjuuo_k_qp_ is not None and _vjuuo_k_qp_.value is not None:

                self.___c_d_i__l_ = _vjuuo_k_qp_.value.decode(self.nsifr_q_er__)


        ___xnmbf__hu = 0x8049
        ___s____mv__ = StandardPropertySet.ADDRESS

        j_e__to_z_kv = Message.x_t_w_mm____(___xnmbf__hu, ___s____mv__)

        if _lm___l_x__c is not None and j_e__to_z_kv in _lm___l_x__c and _lm___l_x__c[j_e__to_z_kv] is not None:
            
            h_mot__nt__v = _lm___l_x__c[j_e__to_z_kv]
            h_mot__nt__v = h_mot__nt__v + self.m__zli___l_b

            h___v___m_xk = self.lh_______ysy[h_mot__nt__v] if h_mot__nt__v in self.lh_______ysy else None

            if h___v___m_xk is not None and h___v___m_xk.value is not None:

                self.ks___x_ef_l_ = h___v___m_xk.value.decode(self.nsifr_q_er__)


        _g_ay___fp_b = 0x801A
        _d_nx____zj_ = StandardPropertySet.ADDRESS

        ______b_y_hu = Message.x_t_w_mm____(_g_ay___fp_b, _d_nx____zj_)

        if _lm___l_x__c is not None and ______b_y_hu in _lm___l_x__c and _lm___l_x__c[______b_y_hu] is not None:
            
            cvc_kxgoovpr = _lm___l_x__c[______b_y_hu]
            cvc_kxgoovpr = cvc_kxgoovpr + self.m__zli___l_b

            j___w__b__h_ = self.lh_______ysy[cvc_kxgoovpr] if cvc_kxgoovpr in self.lh_______ysy else None

            if j___w__b__h_ is not None and j___w__b__h_.value is not None:

                self.kwi_e__ffg__ = j___w__b__h_.value.decode(self.nsifr_q_er__)


        _n____r___s_ = 0x801C
        __pm__kd_cg_ = StandardPropertySet.ADDRESS

        _k__u_e_____ = Message.x_t_w_mm____(_n____r___s_, __pm__kd_cg_)

        if _lm___l_x__c is not None and _k__u_e_____ in _lm___l_x__c and _lm___l_x__c[_k__u_e_____] is not None:
            
            h_ic___h____ = _lm___l_x__c[_k__u_e_____]
            h_ic___h____ = h_ic___h____ + self.m__zli___l_b

            km_s__n_m_vj = self.lh_______ysy[h_ic___h____] if h_ic___h____ in self.lh_______ysy else None

            if km_s__n_m_vj is not None and km_s__n_m_vj.value is not None:

                self.___ym__z_v__ = km_s__n_m_vj.value.decode(self.nsifr_q_er__)


        k____sqhogb_ = 0x8083
        _ed___o_g_mc = StandardPropertySet.ADDRESS

        __k_r_s_____ = Message.x_t_w_mm____(k____sqhogb_, _ed___o_g_mc)

        if _lm___l_x__c is not None and __k_r_s_____ in _lm___l_x__c and _lm___l_x__c[__k_r_s_____] is not None:
            
            _lg____szorg = _lm___l_x__c[__k_r_s_____]
            _lg____szorg = _lg____szorg + self.m__zli___l_b

            x_f_cdelhdv_ = self.lh_______ysy[_lg____szorg] if _lg____szorg in self.lh_______ysy else None

            if x_f_cdelhdv_ is not None and x_f_cdelhdv_.value is not None:

                self.s__b____or_b = x_f_cdelhdv_.value.decode(self.nsifr_q_er__)


        j__w__snw_fp = 0x8093
        __r__h_q___z = StandardPropertySet.ADDRESS

        dhxoqgcj__dw = Message.x_t_w_mm____(j__w__snw_fp, __r__h_q___z)

        if _lm___l_x__c is not None and dhxoqgcj__dw in _lm___l_x__c and _lm___l_x__c[dhxoqgcj__dw] is not None:
            
            t__r_______j = _lm___l_x__c[dhxoqgcj__dw]
            t__r_______j = t__r_______j + self.m__zli___l_b

            __tqj___xr_g = self.lh_______ysy[t__r_______j] if t__r_______j in self.lh_______ysy else None

            if __tqj___xr_g is not None and __tqj___xr_g.value is not None:

                self._us___o__z__ = __tqj___xr_g.value.decode(self.nsifr_q_er__)


        __y__z____yf = 0x80A3
        _o__v___i_vr = StandardPropertySet.ADDRESS

        h__hyb___b_r = Message.x_t_w_mm____(__y__z____yf, _o__v___i_vr)

        if _lm___l_x__c is not None and h__hyb___b_r in _lm___l_x__c and _lm___l_x__c[h__hyb___b_r] is not None:
            
            sr_d_e__hk_w = _lm___l_x__c[h__hyb___b_r]
            sr_d_e__hk_w = sr_d_e__hk_w + self.m__zli___l_b

            __n_k_bkm___ = self.lh_______ysy[sr_d_e__hk_w] if sr_d_e__hk_w in self.lh_______ysy else None

            if __n_k_bkm___ is not None and __n_k_bkm___.value is not None:

                self._cf__c_q__c_ = __n_k_bkm___.value.decode(self.nsifr_q_er__)


        _vn_wvd_qnbb = 0x8084
        _z__e____f__ = StandardPropertySet.ADDRESS

        ______q__x_d = Message.x_t_w_mm____(_vn_wvd_qnbb, _z__e____f__)

        if _lm___l_x__c is not None and ______q__x_d in _lm___l_x__c and _lm___l_x__c[______q__x_d] is not None:
            
            __aqo____gk_ = _lm___l_x__c[______q__x_d]
            __aqo____gk_ = __aqo____gk_ + self.m__zli___l_b

            obh___vj__l_ = self.lh_______ysy[__aqo____gk_] if __aqo____gk_ in self.lh_______ysy else None

            if obh___vj__l_ is not None and obh___vj__l_.value is not None:

                self.y___cq__rk__ = obh___vj__l_.value.decode(self.nsifr_q_er__)


        ______pi_w__ = 0x8094
        ___a__zufsv_ = StandardPropertySet.ADDRESS

        _jq_d__r_l__ = Message.x_t_w_mm____(______pi_w__, ___a__zufsv_)

        if _lm___l_x__c is not None and _jq_d__r_l__ in _lm___l_x__c and _lm___l_x__c[_jq_d__r_l__] is not None:
            
            _p_rs___j__e = _lm___l_x__c[_jq_d__r_l__]
            _p_rs___j__e = _p_rs___j__e + self.m__zli___l_b

            ______k_y__t = self.lh_______ysy[_p_rs___j__e] if _p_rs___j__e in self.lh_______ysy else None

            if ______k_y__t is not None and ______k_y__t.value is not None:

                self.w_g_ag_b_w__ = ______k_y__t.value.decode(self.nsifr_q_er__)


        jmr_w______c = 0x80A4
        v__o_____rsb = StandardPropertySet.ADDRESS

        unt__n___fhy = Message.x_t_w_mm____(jmr_w______c, v__o_____rsb)

        if _lm___l_x__c is not None and unt__n___fhy in _lm___l_x__c and _lm___l_x__c[unt__n___fhy] is not None:
            
            r_____b___id = _lm___l_x__c[unt__n___fhy]
            r_____b___id = r_____b___id + self.m__zli___l_b

            ____n_p__q__ = self.lh_______ysy[r_____b___id] if r_____b___id in self.lh_______ysy else None

            if ____n_p__q__ is not None and ____n_p__q__.value is not None:

                self.j_t_u__f____ = ____n_p__q__.value.decode(self.nsifr_q_er__)


        ___z__p_e__d = 0x8080
        a_____t_f_lb = StandardPropertySet.ADDRESS

        __wz_fl_eefx = Message.x_t_w_mm____(___z__p_e__d, a_____t_f_lb)

        if _lm___l_x__c is not None and __wz_fl_eefx in _lm___l_x__c and _lm___l_x__c[__wz_fl_eefx] is not None:
            
            tot__xrj_h_v = _lm___l_x__c[__wz_fl_eefx]
            tot__xrj_h_v = tot__xrj_h_v + self.m__zli___l_b

            b_nqg_____id = self.lh_______ysy[tot__xrj_h_v] if tot__xrj_h_v in self.lh_______ysy else None

            if b_nqg_____id is not None and b_nqg_____id.value is not None:

                self._z___m__jkqj = b_nqg_____id.value.decode(self.nsifr_q_er__)


        i____ns_ydsp = 0x8090
        af___e_j__yr = StandardPropertySet.ADDRESS

        __t___jscc_r = Message.x_t_w_mm____(i____ns_ydsp, af___e_j__yr)

        if _lm___l_x__c is not None and __t___jscc_r in _lm___l_x__c and _lm___l_x__c[__t___jscc_r] is not None:
            
            _p_b__lko___ = _lm___l_x__c[__t___jscc_r]
            _p_b__lko___ = _p_b__lko___ + self.m__zli___l_b

            sx__jazci___ = self.lh_______ysy[_p_b__lko___] if _p_b__lko___ in self.lh_______ysy else None

            if sx__jazci___ is not None and sx__jazci___.value is not None:

                self.m__nj____x__ = sx__jazci___.value.decode(self.nsifr_q_er__)


        ___t___s__iz = 0x80A0
        n_r__g___qz_ = StandardPropertySet.ADDRESS

        r__mfj_bj_j_ = Message.x_t_w_mm____(___t___s__iz, n_r__g___qz_)

        if _lm___l_x__c is not None and r__mfj_bj_j_ in _lm___l_x__c and _lm___l_x__c[r__mfj_bj_j_] is not None:
            
            ___vg___brki = _lm___l_x__c[r__mfj_bj_j_]
            ___vg___brki = ___vg___brki + self.m__zli___l_b

            te__wrs____u = self.lh_______ysy[___vg___brki] if ___vg___brki in self.lh_______ysy else None

            if te__wrs____u is not None and te__wrs____u.value is not None:

                self.h_k_lm______ = te__wrs____u.value.decode(self.nsifr_q_er__)


        f_______ggi_ = 0x8082
        ___v___ijdn_ = StandardPropertySet.ADDRESS

        ir_tj__eqs__ = Message.x_t_w_mm____(f_______ggi_, ___v___ijdn_)

        if _lm___l_x__c is not None and ir_tj__eqs__ in _lm___l_x__c and _lm___l_x__c[ir_tj__eqs__] is not None:
            
            iv_d_n_ht_mk = _lm___l_x__c[ir_tj__eqs__]
            iv_d_n_ht_mk = iv_d_n_ht_mk + self.m__zli___l_b

            _u_k__bni__nwbj_tl_ = self.lh_______ysy[iv_d_n_ht_mk] if iv_d_n_ht_mk in self.lh_______ysy else None

            if _u_k__bni__nwbj_tl_ is not None and _u_k__bni__nwbj_tl_.value is not None:

                self._f__lx__ayl_ = _u_k__bni__nwbj_tl_.value.decode(self.nsifr_q_er__)


        _um_b__p_gxo = 0x8092
        k_ncl__to_w_ = StandardPropertySet.ADDRESS

        z__fy_f_h___ = Message.x_t_w_mm____(_um_b__p_gxo, k_ncl__to_w_)

        if _lm___l_x__c is not None and z__fy_f_h___ in _lm___l_x__c and _lm___l_x__c[z__fy_f_h___] is not None:
            
            ___j_r_kqv__ = _lm___l_x__c[z__fy_f_h___]
            ___j_r_kqv__ = ___j_r_kqv__ + self.m__zli___l_b

            __f_iufq__s_ = self.lh_______ysy[___j_r_kqv__] if ___j_r_kqv__ in self.lh_______ysy else None

            if __f_iufq__s_ is not None and __f_iufq__s_.value is not None:

                self.s__g_h__crxw = __f_iufq__s_.value.decode(self.nsifr_q_er__)


        _z_t_w__kkea = 0x80A2
        _rt___k_thtq = StandardPropertySet.ADDRESS

        v_da________ = Message.x_t_w_mm____(_z_t_w__kkea, _rt___k_thtq)

        if _lm___l_x__c is not None and v_da________ in _lm___l_x__c and _lm___l_x__c[v_da________] is not None:
            
            _q_l___rg___ = _lm___l_x__c[v_da________]
            _q_l___rg___ = _q_l___rg___ + self.m__zli___l_b

            _w_w___dhico = self.lh_______ysy[_q_l___rg___] if _q_l___rg___ in self.lh_______ysy else None

            if _w_w___dhico is not None and _w_w___dhico.value is not None:

                self.e_o__a__mz_s = _w_w___dhico.value.decode(self.nsifr_q_er__)   


        j______nu_z_ = 0x8085
        __tuue_k_u__ = StandardPropertySet.ADDRESS

        __f___xj_lx_ = Message.x_t_w_mm____(j______nu_z_, __tuue_k_u__)

        if _lm___l_x__c is not None and __f___xj_lx_ in _lm___l_x__c and _lm___l_x__c[__f___xj_lx_] is not None:
            
            _____qznl_l_ = _lm___l_x__c[__f___xj_lx_]
            _____qznl_l_ = _____qznl_l_ + self.m__zli___l_b

            hvapvy__u__h = self.lh_______ysy[_____qznl_l_] if _____qznl_l_ in self.lh_______ysy else None

            if hvapvy__u__h is not None and hvapvy__u__h.value is not None:

                self._g_l_bu__r__ = hvapvy__u__h.value.decode(self.nsifr_q_er__)


        __l_____vpm_ = 0x8095
        we__x__u_is_ = StandardPropertySet.ADDRESS

        _u_cae__qany = Message.x_t_w_mm____(__l_____vpm_, we__x__u_is_)

        if _lm___l_x__c is not None and _u_cae__qany in _lm___l_x__c and _lm___l_x__c[_u_cae__qany] is not None:
            
            k___m_m_z_w_ = _lm___l_x__c[_u_cae__qany]
            k___m_m_z_w_ = k___m_m_z_w_ + self.m__zli___l_b

            ___u_n___yt_ = self.lh_______ysy[k___m_m_z_w_] if k___m_m_z_w_ in self.lh_______ysy else None

            if ___u_n___yt_ is not None and ___u_n___yt_.value is not None:

                self.kw_r____n__e = ___u_n___yt_.value.decode(self.nsifr_q_er__)


        h______b__g_ = 0x80A5
        ca_knv__it__ = StandardPropertySet.ADDRESS

        ____xjsj_otk = Message.x_t_w_mm____(h______b__g_, ca_knv__it__)

        if _lm___l_x__c is not None and ____xjsj_otk in _lm___l_x__c and _lm___l_x__c[____xjsj_otk] is not None:
            
            _corg_z_pk__ = _lm___l_x__c[____xjsj_otk]
            _corg_z_pk__ = _corg_z_pk__ + self.m__zli___l_b

            y_lsz____g__ = self.lh_______ysy[_corg_z_pk__] if _corg_z_pk__ in self.lh_______ysy else None

            if y_lsz____g__ is not None and y_lsz____g__.value is not None:

                self.ti__vpygof_h = y_lsz____g__.value.decode(self.nsifr_q_er__)  


        for e in range(len(self.fmuyou__mciw)):
            
            _j_c____e___ = None

            if isinstance(self.fmuyou__mciw[e].tag, ExtendedPropertyId):
                bs_bf_____w_ = self.fmuyou__mciw[e].tag
                _j_c____e___ = Message.x_t_w_mm____(bs_bf_____w_.id, bs_bf_____w_.guid)

            else:
                bs_bf_____w_ = self.fmuyou__mciw[e].tag
                _j_c____e___ = Message.x_t_w_mm____(bs_bf_____w_.name, bs_bf_____w_.guid)
            
            if _lm___l_x__c is not None and _j_c____e___ in _lm___l_x__c and _lm___l_x__c[_j_c____e___] is not None:

                y__r_fd_m___ = _lm___l_x__c[_j_c____e___]

                for ____t__izh__ in self.lh_______ysy:

                    if ____t__izh__.startswith(y__r_fd_m___):

                        __p_fzml____ = self.lh_______ysy[____t__izh__]

                        self.fmuyou__mciw[e].tag.type = __p_fzml____.type

                        if self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_BINARY:

                            y__r_fd_m___ = y__r_fd_m___ + "1102"

                            if __p_fzml____ is not None and __p_fzml____.value is not None:

                                g_p_h_kt_d_b = int(__p_fzml____.size / 8)

                                _r_dpm_wliij = []

                                for i in range(g_p_h_kt_d_b):

                                    mok_o__e_wpq = "__substg1.0_" + y__r_fd_m___ + "-" + str.format("{:08X}", i)

                                    qew__vs_j_hm = vi_h__c____n.get_entry(mok_o__e_wpq)

                                    if qew__vs_j_hm is not None and qew__vs_j_hm.buffer is not None:
                                        _r_dpm_wliij.append(qew__vs_j_hm.buffer)

                                if len(_r_dpm_wliij) > 0:

                                    l__i___n_i__ = bytearray()

                                    __mubo_xv__l = int.to_bytes(len(_r_dpm_wliij), 4, "little")
                                    l__i___n_i__ += __mubo_xv__l

                                    __s_i___h_rk = 0

                                    for i in range(len(_r_dpm_wliij)):

                                        _s___oubc___ = _r_dpm_wliij[i]
                                        ibc___u_up_v = int.to_bytes(4 + len(_r_dpm_wliij) * 4 + __s_i___h_rk, 4, "little")
                                        l__i___n_i__ += ibc___u_up_v

                                        __s_i___h_rk += len(_s___oubc___)
                  
                                    for i in range(len(_r_dpm_wliij)):

                                        _s___oubc___ = _r_dpm_wliij[i]
                                        l__i___n_i__ += _s___oubc___
                  
                                    self.fmuyou__mciw[e].value = bytes(l__i___n_i__)

                        else:
                            self.fmuyou__mciw[e].value = __p_fzml____.value


        yz___fo__kfu = vi_h__c____n.get_entry("__substg1.0_001A" + self.m__zli___l_b)
        ___l____n_v_ = vi_h__c____n.get_entry("__substg1.0_0037" + self.m__zli___l_b)
        ___d_taq___q = vi_h__c____n.get_entry("__substg1.0_003D" + self.m__zli___l_b)
        x__hpwb____t = vi_h__c____n.get_entry("__substg1.0_0070" + self.m__zli___l_b)
        hju_rvw__s__ = vi_h__c____n.get_entry("__substg1.0_0E02" + self.m__zli___l_b)
        nxz_y____q__ = vi_h__c____n.get_entry("__substg1.0_0E03" + self.m__zli___l_b)
        co__t_enjx_h = vi_h__c____n.get_entry("__substg1.0_0E04" + self.m__zli___l_b)
        __n___th___w = vi_h__c____n.get_entry("__substg1.0_0074" + self.m__zli___l_b)
        l___ca___con = vi_h__c____n.get_entry("__substg1.0_0050" + self.m__zli___l_b)
        __f__ll__ili = vi_h__c____n.get_entry("__substg1.0_0E1D" + self.m__zli___l_b)
        i_c__r_v_z__ = vi_h__c____n.get_entry("__substg1.0_1000" + self.m__zli___l_b)
        yegf_me___g_ = vi_h__c____n.get_entry("__substg1.0_10090102")
        ___f_ct___mk = vi_h__c____n.get_entry("__substg1.0_300B0102")
        iz_vlt_w_uk_ = vi_h__c____n.get_entry("__substg1.0_65E20102")
        _u_me_c___rv = vi_h__c____n.get_entry("__substg1.0_0FFF0102")
        binyx_j__eo_ = vi_h__c____n.get_entry("__substg1.0_00460102")
        kprqnqfykb__ = vi_h__c____n.get_entry("__substg1.0_00530102")
        __u_j_tu_lfu = vi_h__c____n.get_entry("__substg1.0_1001" + self.m__zli___l_b)
        zcu_tlz_k___ = vi_h__c____n.get_entry("__substg1.0_3FF8" + self.m__zli___l_b)
        u_zro__oz__a = vi_h__c____n.get_entry("__substg1.0_3FFA" + self.m__zli___l_b)
        ys_hwx____n_ = vi_h__c____n.get_entry("__substg1.0_1035" + self.m__zli___l_b)
        _m___u__qq__ = vi_h__c____n.get_entry("__substg1.0_1042" + self.m__zli___l_b)
        ____cx_u_z_r = vi_h__c____n.get_entry("__substg1.0_1039" + self.m__zli___l_b)
        n_dk_k__ls_l = vi_h__c____n.get_entry("__substg1.0_00710102")
        v___w_lcyv_g = vi_h__c____n.get_entry("__substg1.0_10130102")
        _z___jhku__e = vi_h__c____n.get_entry("__substg1.0_1013" + self.m__zli___l_b)
        __r_rmj_l_o_ = vi_h__c____n.get_entry("__substg1.0_0077" + self.m__zli___l_b)
        kaoy__kg___y = vi_h__c____n.get_entry("__substg1.0_0078" + self.m__zli___l_b)
        z_b_x_____lr = vi_h__c____n.get_entry("__substg1.0_00430102")
        ___ujx_l__g_ = vi_h__c____n.get_entry("__substg1.0_0044" + self.m__zli___l_b)
        ______da_k_i = vi_h__c____n.get_entry("__substg1.0_00520102")
        z_nl_bc_hi__ = vi_h__c____n.get_entry("__substg1.0_0075" + self.m__zli___l_b)
        tgurf_l_____ = vi_h__c____n.get_entry("__substg1.0_0076" + self.m__zli___l_b)
        x_ov_maw_t__ = vi_h__c____n.get_entry("__substg1.0_003F0102")
        ___ur_j__rf_ = vi_h__c____n.get_entry("__substg1.0_0040" + self.m__zli___l_b)
        _as_w__ei__w = vi_h__c____n.get_entry("__substg1.0_00510102")
        kdr_______r_ = vi_h__c____n.get_entry("__substg1.0_0C1E" + self.m__zli___l_b)
        _hp_f___vjg_ = vi_h__c____n.get_entry("__substg1.0_0C1F" + self.m__zli___l_b)
        a____h___t__ = vi_h__c____n.get_entry("__substg1.0_5D01" + self.m__zli___l_b)
        _arld_rt_v_h = vi_h__c____n.get_entry("__substg1.0_0C190102")
        _____ft_v___ = vi_h__c____n.get_entry("__substg1.0_0C1A" + self.m__zli___l_b)
        _p_tchg___pg = vi_h__c____n.get_entry("__substg1.0_0C1D0102")
        ____n_t_w___ = vi_h__c____n.get_entry("__substg1.0_0064" + self.m__zli___l_b)
        __z_x_ny_t__ = vi_h__c____n.get_entry("__substg1.0_0065" + self.m__zli___l_b)
        o_icic_ll__y = vi_h__c____n.get_entry("__substg1.0_5D02" + self.m__zli___l_b)
        __et_qh_____ = vi_h__c____n.get_entry("__substg1.0_00410102")
        yfd__eaoh_d_ = vi_h__c____n.get_entry("__substg1.0_0042" + self.m__zli___l_b)
        ___xn___sgd_ = vi_h__c____n.get_entry("__substg1.0_003B0102")
        t_w_t__ny_eq = vi_h__c____n.get_entry("__substg1.0_007D" + self.m__zli___l_b)
        __xi__v_noq_ = vi_h__c____n.get_entry("__substg1.0_3A30" + self.m__zli___l_b)
        _befxk_cdu__ = vi_h__c____n.get_entry("__substg1.0_3A2E" + self.m__zli___l_b)
        _c_a___o_n__ = vi_h__c____n.get_entry("__substg1.0_3A1B" + self.m__zli___l_b)
        b___benu_c_i = vi_h__c____n.get_entry("__substg1.0_3A24" + self.m__zli___l_b)
        l__u___h_kx_ = vi_h__c____n.get_entry("__substg1.0_3A51" + self.m__zli___l_b)
        g__yh_a__f_u = vi_h__c____n.get_entry("__substg1.0_3A02" + self.m__zli___l_b)
        ___ka___kt_d = vi_h__c____n.get_entry("__substg1.0_3A1E" + self.m__zli___l_b)
        orv___v_glnz = vi_h__c____n.get_entry("__substg1.0_3A1C" + self.m__zli___l_b)
        _a__iv___b__ = vi_h__c____n.get_entry("__substg1.0_3A57" + self.m__zli___l_b)
        v__iu__ntg__ = vi_h__c____n.get_entry("__substg1.0_3A16" + self.m__zli___l_b)
        __f__ydi_e_i = vi_h__c____n.get_entry("__substg1.0_3A49" + self.m__zli___l_b)
        _df___a_d___ = vi_h__c____n.get_entry("__substg1.0_3A4A" + self.m__zli___l_b)
        q__z___fpep_ = vi_h__c____n.get_entry("__substg1.0_3A18" + self.m__zli___l_b)
        au___tv___a_ = vi_h__c____n.get_entry("__substg1.0_3001" + self.m__zli___l_b)
        wkd_s___s___ = vi_h__c____n.get_entry("__substg1.0_3A45" + self.m__zli___l_b)
        _d__o_ngk__w = vi_h__c____n.get_entry("__substg1.0_3A4C" + self.m__zli___l_b)
        f_nv_v___ek_ = vi_h__c____n.get_entry("__substg1.0_3A05" + self.m__zli___l_b)
        __g___orinth = vi_h__c____n.get_entry("__substg1.0_3A06" + self.m__zli___l_b)
        az___mp____e = vi_h__c____n.get_entry("__substg1.0_3A07" + self.m__zli___l_b)
        s__i__uf___b = vi_h__c____n.get_entry("__substg1.0_3A43" + self.m__zli___l_b)
        _______s__yn = vi_h__c____n.get_entry("__substg1.0_3A2F" + self.m__zli___l_b)
        wti_g_poh___ = vi_h__c____n.get_entry("__substg1.0_3A59" + self.m__zli___l_b)
        _fh___w_l_oa = vi_h__c____n.get_entry("__substg1.0_3A5A" + self.m__zli___l_b)
        _w_x__urdpkp = vi_h__c____n.get_entry("__substg1.0_3A5B" + self.m__zli___l_b)
        sy_______vxo = vi_h__c____n.get_entry("__substg1.0_3A5E" + self.m__zli___l_b)
        x___tk__g_ju = vi_h__c____n.get_entry("__substg1.0_3A5C" + self.m__zli___l_b)
        w_h_dc___n_v = vi_h__c____n.get_entry("__substg1.0_3A5D" + self.m__zli___l_b)
        c_n__l___w__ = vi_h__c____n.get_entry("__substg1.0_3A25" + self.m__zli___l_b)
        ____nkyq__wf = vi_h__c____n.get_entry("__substg1.0_3A09" + self.m__zli___l_b)
        ______v_k__g = vi_h__c____n.get_entry("__substg1.0_3A0A" + self.m__zli___l_b)
        i_____q___kv = vi_h__c____n.get_entry("__substg1.0_3A2D" + self.m__zli___l_b)
        _g_td__m___t = vi_h__c____n.get_entry("__substg1.0_3A4E" + self.m__zli___l_b)
        pttvre_i__fr = vi_h__c____n.get_entry("__substg1.0_3A44" + self.m__zli___l_b)
        _dp_ay_sk___ = vi_h__c____n.get_entry("__substg1.0_3A4F" + self.m__zli___l_b)
        _vjpbarm_nk_ = vi_h__c____n.get_entry("__substg1.0_3A19" + self.m__zli___l_b)
        _____p_wg_aj = vi_h__c____n.get_entry("__substg1.0_3A08" + self.m__zli___l_b)
        _____q_uk_ec = vi_h__c____n.get_entry("__substg1.0_3A5F" + self.m__zli___l_b)
        ___egn____j_ = vi_h__c____n.get_entry("__substg1.0_3A60" + self.m__zli___l_b)
        n_r_g_om__it = vi_h__c____n.get_entry("__substg1.0_3A61" + self.m__zli___l_b)
        ___xb_d__u__ = vi_h__c____n.get_entry("__substg1.0_3A62" + self.m__zli___l_b)
        h___x_pl_ey_ = vi_h__c____n.get_entry("__substg1.0_3A63" + self.m__zli___l_b)
        ptyh_q__um__ = vi_h__c____n.get_entry("__substg1.0_3A1F" + self.m__zli___l_b)
        k_c_u__uu__d = vi_h__c____n.get_entry("__substg1.0_3A21" + self.m__zli___l_b)
        yp_pb_q____a = vi_h__c____n.get_entry("__substg1.0_3A50" + self.m__zli___l_b)
        _kvxht___gc_ = vi_h__c____n.get_entry("__substg1.0_3A15" + self.m__zli___l_b)
        bwk_ctaye_qh = vi_h__c____n.get_entry("__substg1.0_3A27" + self.m__zli___l_b)
        __ks____j___ = vi_h__c____n.get_entry("__substg1.0_3A26" + self.m__zli___l_b)
        __rt_mq__t__ = vi_h__c____n.get_entry("__substg1.0_3A2A" + self.m__zli___l_b)
        f_h__pamd___ = vi_h__c____n.get_entry("__substg1.0_3A2B" + self.m__zli___l_b)
        __dqk___ug__ = vi_h__c____n.get_entry("__substg1.0_3A28" + self.m__zli___l_b)
        r_fy__ekt_fm = vi_h__c____n.get_entry("__substg1.0_3A29" + self.m__zli___l_b)
        __y_l__i_e_o = vi_h__c____n.get_entry("__substg1.0_3A23" + self.m__zli___l_b)
        d_qr___qk_ye = vi_h__c____n.get_entry("__substg1.0_3A1A" + self.m__zli___l_b)
        ___u_v_q__pw = vi_h__c____n.get_entry("__substg1.0_3A46" + self.m__zli___l_b)
        ____r__uj___ = vi_h__c____n.get_entry("__substg1.0_3A1D" + self.m__zli___l_b)
        _pn__g_w___a = vi_h__c____n.get_entry("__substg1.0_3A48" + self.m__zli___l_b)
        int__d_a_b_q = vi_h__c____n.get_entry("__substg1.0_3A11" + self.m__zli___l_b)
        _vu_dk_d_t__ = vi_h__c____n.get_entry("__substg1.0_3A2C" + self.m__zli___l_b)
        _gb_o__z_ln_ = vi_h__c____n.get_entry("__substg1.0_3A17" + self.m__zli___l_b)
        ____lhfm__nj = vi_h__c____n.get_entry("__substg1.0_3A4B" + self.m__zli___l_b)


        if yz___fo__kfu is not None and yz___fo__kfu.buffer is not None:
            self._pq_o______n = yz___fo__kfu.buffer.decode(self.nsifr_q_er__)  

        if ___l____n_v_  is not None and ___l____n_v_ .buffer is not None:
            self._xv_y___o___ = ___l____n_v_.buffer.decode(self.nsifr_q_er__)  

        if ___d_taq___q is not None and ___d_taq___q.buffer is not None:
            self._u__q__z___b = ___d_taq___q.buffer.decode(self.nsifr_q_er__)  

        if x__hpwb____t is not None and x__hpwb____t.buffer is not None:
            self._rz_mvr_yf_p = x__hpwb____t.buffer.decode(self.nsifr_q_er__)  

        if hju_rvw__s__ is not None and hju_rvw__s__.buffer is not None:
            self.f_pfu__g_o_p = hju_rvw__s__.buffer.decode(self.nsifr_q_er__)  

        if nxz_y____q__ is not None and nxz_y____q__.buffer is not None:
            self._nfg_ljsz_d_ = nxz_y____q__.buffer.decode(self.nsifr_q_er__)  

        if co__t_enjx_h is not None and co__t_enjx_h.buffer is not None:
            self.v_xe_s_yi_bp = co__t_enjx_h.buffer.decode(self.nsifr_q_er__)  

        if __n___th___w is not None and __n___th___w.buffer is not None:
            self.p_j_________ = __n___th___w.buffer.decode(self.nsifr_q_er__)  

        if l___ca___con is not None and l___ca___con.buffer is not None:
            self.na___bd__o_a = l___ca___con.buffer.decode(self.nsifr_q_er__)  

        if __f__ll__ili is not None and __f__ll__ili.buffer is not None:
            self.d_w____xbnru = __f__ll__ili.buffer.decode(self.nsifr_q_er__)  

        if i_c__r_v_z__ is not None and i_c__r_v_z__.buffer is not None:
            self.____y_gej_ly = i_c__r_v_z__.buffer.decode(self.nsifr_q_er__) 

        if yegf_me___g_ is not None and yegf_me___g_.buffer is not None:
            self._h_b_v_d____ = yegf_me___g_.buffer

        if ___f_ct___mk is not None and ___f_ct___mk.buffer is not None:
            self.__i___m_ncy_ = ___f_ct___mk.buffer

        if iz_vlt_w_uk_ is not None and iz_vlt_w_uk_.buffer is not None:
            self.fhgy_b_an_h_ = iz_vlt_w_uk_.buffer

        if _u_me_c___rv is not None and _u_me_c___rv.buffer is not None:
            self.__j__stw_l_u = _u_me_c___rv.buffer

        if binyx_j__eo_ is not None and binyx_j__eo_.buffer is not None:
            self.___k________ = binyx_j__eo_.buffer

        if kprqnqfykb__ is not None and kprqnqfykb__.buffer is not None:
            self.vbn_jd_xc_c_ = kprqnqfykb__.buffer

        if __u_j_tu_lfu is not None and __u_j_tu_lfu.buffer is not None:
            self.twqm_____n_r = __u_j_tu_lfu.buffer.decode(self.nsifr_q_er__)  

        if zcu_tlz_k___ is not None and zcu_tlz_k___.buffer is not None:
            self.____y_kuq__q = zcu_tlz_k___.buffer.decode(self.nsifr_q_er__)  

        if u_zro__oz__a is not None and u_zro__oz__a.buffer is not None:
            self.___zp_upib__ = u_zro__oz__a.buffer.decode(self.nsifr_q_er__)  

        if ys_hwx____n_ is not None and ys_hwx____n_.buffer is not None:
            self.____w_h_sni_ = ys_hwx____n_.buffer.decode(self.nsifr_q_er__)  

        if _m___u__qq__ is not None and _m___u__qq__.buffer is not None:
            self._______eft__ = _m___u__qq__.buffer.decode(self.nsifr_q_er__)  

        if ____cx_u_z_r is not None and ____cx_u_z_r.buffer is not None:
            self._fio_i_c_few = ____cx_u_z_r.buffer.decode(self.nsifr_q_er__)  

        if n_dk_k__ls_l is not None and n_dk_k__ls_l.buffer is not None:
            self.k_kt_xqc____ = n_dk_k__ls_l.buffer

        if _u_me_c___rv is not None and _u_me_c___rv.buffer is not None:
            self.__j__stw_l_u = _u_me_c___rv.buffer

        if v___w_lcyv_g is not None and v___w_lcyv_g.buffer is not None:
            self.zpz__r____ji = v___w_lcyv_g.buffer
        elif _z___jhku__e is not None and _z___jhku__e.buffer is not None:
            
            if self._x_____y___i > 0:

                chbyt_vax___ = _ghfeuhr____(self._x_____y___i)

                __z_s_f_lu__ = _z___jhku__e.buffer.decode(chbyt_vax___)
                self.zpz__r____ji = __z_s_f_lu__.decode(chbyt_vax___)

            else:
                __z_s_f_lu__ = _z___jhku__e.buffer.decode(self._x_q___iqwz_)
                self.zpz__r____ji = __z_s_f_lu__.decode(self._x_q___iqwz_)


        if __r_rmj_l_o_ is not None and __r_rmj_l_o_.buffer is not None:
            self._vry_n_v_d_g = __r_rmj_l_o_.buffer.decode(self.nsifr_q_er__) 

        if kaoy__kg___y is not None and kaoy__kg___y.buffer is not None:
            self.___x_ry__twg = kaoy__kg___y.buffer.decode(self.nsifr_q_er__) 

        if z_b_x_____lr is not None and z_b_x_____lr.buffer is not None:
            self.___h_____oo_ = z_b_x_____lr.buffer

        if ___ujx_l__g_ is not None and ___ujx_l__g_.buffer is not None:
            self.b_o_l__vz__j = ___ujx_l__g_.buffer.decode(self.nsifr_q_er__) 

        if ______da_k_i is not None and ______da_k_i.buffer is not None:
            self.ehp_zo_hnnk_ = ______da_k_i.buffer

        if z_nl_bc_hi__ is not None and z_nl_bc_hi__.buffer is not None:
            self._k__vn_qvf__ = z_nl_bc_hi__.buffer.decode(self.nsifr_q_er__) 

        if tgurf_l_____ is not None and tgurf_l_____.buffer is not None:
            self._x___qkj___e = tgurf_l_____.buffer.decode(self.nsifr_q_er__) 

        if x_ov_maw_t__ is not None and x_ov_maw_t__.buffer is not None:
            self.__ynoc______ = x_ov_maw_t__.buffer

        if ___ur_j__rf_ is not None and ___ur_j__rf_.buffer is not None:
            self.nn__l___z_p_ = ___ur_j__rf_.buffer.decode(self.nsifr_q_er__) 

        if _as_w__ei__w is not None and _as_w__ei__w.buffer is not None:
            self.d_vn__f____i = _as_w__ei__w.buffer

        if kdr_______r_ is not None and kdr_______r_.buffer is not None:
            self.t___f_____hz = kdr_______r_.buffer.decode(self.nsifr_q_er__) 

        if _hp_f___vjg_ is not None and _hp_f___vjg_.buffer is not None:
            self.__rfliczcge_ = _hp_f___vjg_.buffer.decode(self.nsifr_q_er__)

        if a____h___t__ is not None and a____h___t__.buffer is not None:
            self.______qcsd_d = a____h___t__.buffer.decode(self.nsifr_q_er__) 

        if _arld_rt_v_h is not None and _arld_rt_v_h.buffer is not None:
            self.insn_u______ = _arld_rt_v_h.buffer

        if _____ft_v___ is not None and _____ft_v___.buffer is not None:
            self.v_x__v____fh = _____ft_v___.buffer.decode(self.nsifr_q_er__) 

        if _p_tchg___pg is not None and _p_tchg___pg.buffer is not None:
            self._a__y_vf_eib = _p_tchg___pg.buffer

        if ____n_t_w___ is not None and ____n_t_w___.buffer is not None:
            self.xep__h_t__f_ = ____n_t_w___.buffer.decode(self.nsifr_q_er__) 

        if __z_x_ny_t__ is not None and __z_x_ny_t__.buffer is not None:
            self._w_tq___xpkm = __z_x_ny_t__.buffer.decode(self.nsifr_q_er__)

        if o_icic_ll__y is not None and o_icic_ll__y.buffer is not None:
            self.__tl__v__h__ = o_icic_ll__y.buffer.decode(self.nsifr_q_er__) 

        if __et_qh_____ is not None and __et_qh_____.buffer is not None:
            self.rle_hef_uum_ = __et_qh_____.buffer

        if yfd__eaoh_d_ is not None and yfd__eaoh_d_.buffer is not None:
            self.____d_yy__gy = yfd__eaoh_d_.buffer.decode(self.nsifr_q_er__) 

        if ___xn___sgd_ is not None and ___xn___sgd_.buffer is not None:
            self._fb_znz_lkv_ = ___xn___sgd_.buffer

        if t_w_t__ny_eq is not None and t_w_t__ny_eq.buffer is not None:
            self.__z__nhb_s__ = t_w_t__ny_eq.buffer.decode(self.nsifr_q_er__) 

        if __xi__v_noq_ is not None and __xi__v_noq_.buffer is not None:
            self.m__vg_n__ze_ = __xi__v_noq_.buffer.decode(self.nsifr_q_er__)

        if _befxk_cdu__ is not None and _befxk_cdu__.buffer is not None:
            self.__x_____x__h = _befxk_cdu__.buffer.decode(self.nsifr_q_er__) 

        if _c_a___o_n__ is not None and _c_a___o_n__.buffer is not None:
            self.t__w_nqk____ = _c_a___o_n__.buffer.decode(self.nsifr_q_er__) 

        if b___benu_c_i is not None and b___benu_c_i.buffer is not None:
            self.__rom_q__nzu = b___benu_c_i.buffer.decode(self.nsifr_q_er__) 

        if l__u___h_kx_ is not None and l__u___h_kx_.buffer is not None:
            self.h_a_x____w_j = l__u___h_kx_.buffer.decode(self.nsifr_q_er__) 

        if g__yh_a__f_u is not None and g__yh_a__f_u.buffer is not None:
            self.ul_l_qtt___p = g__yh_a__f_u.buffer.decode(self.nsifr_q_er__) 

        if ___ka___kt_d is not None and ___ka___kt_d.buffer is not None:
            self.__m__tcaw___ = ___ka___kt_d.buffer.decode(self.nsifr_q_er__)

        if orv___v_glnz is not None and orv___v_glnz.buffer is not None:
            self.owjw_l_is_fs = orv___v_glnz.buffer.decode(self.nsifr_q_er__) 

        if _a__iv___b__ is not None and _a__iv___b__.buffer is not None:
            self.____v__n___r = _a__iv___b__.buffer.decode(self.nsifr_q_er__) 

        if v__iu__ntg__ is not None and v__iu__ntg__.buffer is not None:
            self.e_s_i__m____ = v__iu__ntg__.buffer.decode(self.nsifr_q_er__) 

        if __f__ydi_e_i is not None and __f__ydi_e_i.buffer is not None:
            self.______rz___k = __f__ydi_e_i.buffer.decode(self.nsifr_q_er__) 

        if _df___a_d___ is not None and _df___a_d___.buffer is not None:
            self._____li__w__ = _df___a_d___.buffer.decode(self.nsifr_q_er__) 

        if q__z___fpep_ is not None and q__z___fpep_.buffer is not None:
            self.hgsi_u__j__v = q__z___fpep_.buffer.decode(self.nsifr_q_er__)

        if au___tv___a_ is not None and au___tv___a_.buffer is not None:
            self.__j___op_s__ = au___tv___a_.buffer.decode(self.nsifr_q_er__) 

        if wkd_s___s___ is not None and wkd_s___s___.buffer is not None:
            self._pudmbn_y_qy = wkd_s___s___.buffer.decode(self.nsifr_q_er__) 

        if _d__o_ngk__w is not None and _d__o_ngk__w.buffer is not None:
            self._x_b_d_u__hg = _d__o_ngk__w.buffer.decode(self.nsifr_q_er__) 

        if f_nv_v___ek_ is not None and f_nv_v___ek_.buffer is not None:
            self.gd_n__q___qg = f_nv_v___ek_.buffer.decode(self.nsifr_q_er__) 

        if __g___orinth is not None and __g___orinth.buffer is not None:
            self._ks__k_____f = __g___orinth.buffer.decode(self.nsifr_q_er__)

        if az___mp____e is not None and az___mp____e.buffer is not None:
            self.tb_____r_t__ = az___mp____e.buffer.decode(self.nsifr_q_er__)

        if s__i__uf___b is not None and s__i__uf___b.buffer is not None:
            self.________zntw = s__i__uf___b.buffer.decode(self.nsifr_q_er__) 

        if _______s__yn is not None and _______s__yn.buffer is not None:
            self.__rvw_yhfi_g = _______s__yn.buffer.decode(self.nsifr_q_er__) 

        if wti_g_poh___ is not None and wti_g_poh___.buffer is not None:
            self.__y_____aw__ = wti_g_poh___.buffer.decode(self.nsifr_q_er__) 

        if _fh___w_l_oa is not None and _fh___w_l_oa.buffer is not None:
            self._____lc_g_h_ = _fh___w_l_oa.buffer.decode(self.nsifr_q_er__) 

        if _w_x__urdpkp is not None and _w_x__urdpkp.buffer is not None:
            self.d__ol_f_a_i_ = _w_x__urdpkp.buffer.decode(self.nsifr_q_er__) 

        if sy_______vxo is not None and sy_______vxo.buffer is not None:
            self.__xc__e_i___ = sy_______vxo.buffer.decode(self.nsifr_q_er__)

        if x___tk__g_ju is not None and x___tk__g_ju.buffer is not None:
            self.v_s____jaf__ = x___tk__g_ju.buffer.decode(self.nsifr_q_er__) 

        if w_h_dc___n_v is not None and w_h_dc___n_v.buffer is not None:
            self.___h_r__f_d_ = w_h_dc___n_v.buffer.decode(self.nsifr_q_er__) 

        if c_n__l___w__ is not None and c_n__l___w__.buffer is not None:
            self.w___u___r_fm = c_n__l___w__.buffer.decode(self.nsifr_q_er__) 

        if ____nkyq__wf is not None and ____nkyq__wf.buffer is not None:
            self.v__pel_bkku_ = ____nkyq__wf.buffer.decode(self.nsifr_q_er__) 

        if ______v_k__g is not None and ______v_k__g.buffer is not None:
            self.____s_a_ddga = ______v_k__g.buffer.decode(self.nsifr_q_er__) 

        if i_____q___kv is not None and i_____q___kv.buffer is not None:
            self._k__dsw_fx_j = i_____q___kv.buffer.decode(self.nsifr_q_er__)

        if _g_td__m___t is not None and _g_td__m___t.buffer is not None:
            self._h_sxo__l_h_ = _g_td__m___t.buffer.decode(self.nsifr_q_er__) 

        if pttvre_i__fr is not None and pttvre_i__fr.buffer is not None:
            self.fxo_h_yp____ = pttvre_i__fr.buffer.decode(self.nsifr_q_er__) 

        if _dp_ay_sk___ is not None and _dp_ay_sk___.buffer is not None:
            self.r_____xd__nn = _dp_ay_sk___.buffer.decode(self.nsifr_q_er__) 

        if _vjpbarm_nk_ is not None and _vjpbarm_nk_.buffer is not None:
            self.xh_n_w_ab_q_ = _vjpbarm_nk_.buffer.decode(self.nsifr_q_er__) 

        if _____p_wg_aj is not None and _____p_wg_aj.buffer is not None:
            self.h_w_j_lt_u_n = _____p_wg_aj.buffer.decode(self.nsifr_q_er__) 

        if _____q_uk_ec is not None and _____q_uk_ec.buffer is not None:
            self.p___p__ch_nr = _____q_uk_ec.buffer.decode(self.nsifr_q_er__)

        if ___egn____j_ is not None and ___egn____j_.buffer is not None:
            self.x__za__bvxv_ = ___egn____j_.buffer.decode(self.nsifr_q_er__) 

        if n_r_g_om__it is not None and n_r_g_om__it.buffer is not None:
            self.b___w_g__t__ = n_r_g_om__it.buffer.decode(self.nsifr_q_er__) 

        if ___xb_d__u__ is not None and ___xb_d__u__.buffer is not None:
            self._n___kc___xe = ___xb_d__u__.buffer.decode(self.nsifr_q_er__) 

        if h___x_pl_ey_ is not None and h___x_pl_ey_.buffer is not None:
            self.t___m_b___qg = h___x_pl_ey_.buffer.decode(self.nsifr_q_er__) 

        if ptyh_q__um__ is not None and ptyh_q__um__.buffer is not None:
            self.o___h_f_ey_j = ptyh_q__um__.buffer.decode(self.nsifr_q_er__) 

        if k_c_u__uu__d is not None and k_c_u__uu__d.buffer is not None:
            self.w_qf___ld___ = k_c_u__uu__d.buffer.decode(self.nsifr_q_er__)

        if yp_pb_q____a is not None and yp_pb_q____a.buffer is not None:
            self.__v_cyc_____ = yp_pb_q____a.buffer.decode(self.nsifr_q_er__) 

        if _kvxht___gc_ is not None and _kvxht___gc_.buffer is not None:
            self.h__l____bnit = _kvxht___gc_.buffer.decode(self.nsifr_q_er__) 

        if bwk_ctaye_qh is not None and bwk_ctaye_qh.buffer is not None:
            self.g_k_____pg__ = bwk_ctaye_qh.buffer.decode(self.nsifr_q_er__) 

        if __ks____j___ is not None and __ks____j___.buffer is not None:
            self.ks___x_ef_l_ = __ks____j___.buffer.decode(self.nsifr_q_er__) 

        if __rt_mq__t__ is not None and __rt_mq__t__.buffer is not None:
            self.___c_d_i__l_ = __rt_mq__t__.buffer.decode(self.nsifr_q_er__) 

        if f_h__pamd___ is not None and f_h__pamd___.buffer is not None:
            self.acu_i__mj_b_ = f_h__pamd___.buffer.decode(self.nsifr_q_er__)

        if __dqk___ug__ is not None and __dqk___ug__.buffer is not None:
            self.__dyk_vx_w__ = __dqk___ug__.buffer.decode(self.nsifr_q_er__) 

        if r_fy__ekt_fm is not None and r_fy__ekt_fm.buffer is not None:
            self._q___u__q_u_ = r_fy__ekt_fm.buffer.decode(self.nsifr_q_er__) 

        if __y_l__i_e_o is not None and __y_l__i_e_o.buffer is not None:
            self.hl_z____eu_u = __y_l__i_e_o.buffer.decode(self.nsifr_q_er__) 

        if d_qr___qk_ye is not None and d_qr___qk_ye.buffer is not None:
            self.__br___ty__q = d_qr___qk_ye.buffer.decode(self.nsifr_q_er__) 

        if ___u_v_q__pw is not None and ___u_v_q__pw.buffer is not None:
            self.mma_d_p_ijv_ = ___u_v_q__pw.buffer.decode(self.nsifr_q_er__) 

        if ____r__uj___ is not None and ____r__uj___.buffer is not None:
            self.p___m__s_toa = ____r__uj___.buffer.decode(self.nsifr_q_er__)

        if _pn__g_w___a is not None and _pn__g_w___a.buffer is not None:
            self.reycs___h__f = _pn__g_w___a.buffer.decode(self.nsifr_q_er__) 

        if int__d_a_b_q is not None and int__d_a_b_q.buffer is not None:
            self.__zl_e_zx___ = int__d_a_b_q.buffer.decode(self.nsifr_q_er__) 

        if _vu_dk_d_t__ is not None and _vu_dk_d_t__.buffer is not None:
            self.j_i_g__k____ = _vu_dk_d_t__.buffer.decode(self.nsifr_q_er__) 

        if _gb_o__z_ln_ is not None and _gb_o__z_ln_.buffer is not None:
            self._x___k_b____ = _gb_o__z_ln_.buffer.decode(self.nsifr_q_er__) 

        if ____lhfm__nj is not None and ____lhfm__nj.buffer is not None:
            self.jvd_z__mk__k = ____lhfm__nj.buffer.decode(self.nsifr_q_er__) 


        for i in range(z_______z__r):

            mo_______p_r = {}
            ___fb_____c_ = str.format("__recip_version1.0_#{:08X}", i)

            o__qtb_____p = vi_h__c____n.get_entry(___fb_____c_)

            if o__qtb_____p is None:
                continue

            ___d_______y = o__qtb_____p.get_entry("__properties_version1.0")

            if ___d_______y is not None and ___d_______y.buffer is not None:

                for j in range(8, len(___d_______y.buffer), 16):

                    ot______m_ea = ___d_______y.buffer[j: j + 16]
                    nd___acldb__ = Property(ot______m_ea)

                    if nd___acldb__.size > 0:                       
                        __nn__yp_h_y = "__substg1.0_" + str.format("{:08X}", nd___acldb__.tag)
                        _fs____gs__g = o__qtb_____p.get_entry(__nn__yp_h_y)

                        if _fs____gs__g is not None and _fs____gs__g.buffer is not None and len(_fs____gs__g.buffer) > 0:            
                            nd___acldb__.value = _fs____gs__g.buffer

                    _n_____ylb__ = str.format("{:08X}", nd___acldb__.tag)
                    mo_______p_r[_n_____ylb__] = nd___acldb__


            b_n__qu_z_ve = Recipient()

            _yt_ht_io__w = mo_______p_r["39000003"] if "39000003" in mo_______p_r else None

            if _yt_ht_io__w is not None and _yt_ht_io__w.value is not None:
                __plecf_fb__ = int.from_bytes(_yt_ht_io__w.value[0:4], "little")
                b_n__qu_z_ve.display_type = EnumUtil.parse_display_type(__plecf_fb__)

            _f___kv_z__z = mo_______p_r["0FFE0003"] if "0FFE0003" in mo_______p_r else None

            if _f___kv_z__z is not None and _f___kv_z__z.value is not None:
                v_fea_q_l___ = int.from_bytes(_f___kv_z__z.value[0:4], "little")
                b_n__qu_z_ve.object_type = EnumUtil.parse_object_type(v_fea_q_l___)

            ___cb__na_gv = mo_______p_r["0C150003"] if "0C150003" in mo_______p_r else None

            if ___cb__na_gv is not None and ___cb__na_gv.value is not None:
                w____ysl____ = int.from_bytes(___cb__na_gv.value[0:4], "little")
                b_n__qu_z_ve.recipient_type = EnumUtil.parse_recipient_type(w____ysl____)

            _k_exwy_____ = mo_______p_r["0E0F000B"] if "0E0F000B" in mo_______p_r else None

            if _k_exwy_____ is not None and _k_exwy_____.value is not None:
                _e__k_vw____ = int.from_bytes(_k_exwy_____.value[0:2], "little")

                if _e__k_vw____ > 0:
                    b_n__qu_z_ve.responsibility = True

            _j____j___k_ = mo_______p_r["3A40000B"] if "3A40000B" in mo_______p_r else None

            if _j____j___k_ is not None and _j____j___k_.value is not None:
                i__h_d___xoc = int.from_bytes(_j____j___k_.value[0:2], "little")

                if i__h_d___xoc > 0:
                    b_n__qu_z_ve.send_rich_info = True

            ___pte__dqp_ = mo_______p_r["3A710003"] if "3A710003" in mo_______p_r else None

            if ___pte__dqp_ is not None and ___pte__dqp_.value is not None:
                b_n__qu_z_ve.send_internet_encoding = int.from_bytes(___pte__dqp_.value[0:4], "little")

            _mkvwta_____ = o__qtb_____p.get_entry("__substg1.0_3001" + self.m__zli___l_b)
            ____zio_brtb = o__qtb_____p.get_entry("__substg1.0_3002" + self.m__zli___l_b)
            __rl_om_p___ = o__qtb_____p.get_entry("__substg1.0_3003" + self.m__zli___l_b)
            ____r_aj_ab_ = o__qtb_____p.get_entry("__substg1.0_39FE" + self.m__zli___l_b)
            p__ow_xs___y = o__qtb_____p.get_entry("__substg1.0_39FF" + self.m__zli___l_b)
            n__q__c_lpwd = o__qtb_____p.get_entry("__substg1.0_3A20" + self.m__zli___l_b)
            b__ghxmd_x__ = o__qtb_____p.get_entry("__substg1.0_403D" + self.m__zli___l_b)
            v__tw_z__g__ = o__qtb_____p.get_entry("__substg1.0_403E" + self.m__zli___l_b)
            _gnin__ie_qe = o__qtb_____p.get_entry("__substg1.0_0FFF0102")
            w_ka_v___vkg = o__qtb_____p.get_entry("__substg1.0_300B0102")
            me_u_qbxsh__ = o__qtb_____p.get_entry("__substg1.0_0FF60102")

            if _mkvwta_____ is not None and _mkvwta_____.buffer is not None:
                b_n__qu_z_ve.display_name = _mkvwta_____.buffer.decode(self.nsifr_q_er__)

            if ____zio_brtb is not None and ____zio_brtb.buffer is not None:
                b_n__qu_z_ve.address_type = ____zio_brtb.buffer.decode(self.nsifr_q_er__) 

            if __rl_om_p___ is not None and __rl_om_p___.buffer is not None:
                b_n__qu_z_ve.email_address = __rl_om_p___.buffer.decode(self.nsifr_q_er__) 

            if ____r_aj_ab_ is not None and ____r_aj_ab_.buffer is not None:
                b_n__qu_z_ve.smtp_address = ____r_aj_ab_.buffer.decode(self.nsifr_q_er__) 

            if p__ow_xs___y is not None and p__ow_xs___y.buffer is not None:
                b_n__qu_z_ve.display_name_7bit = p__ow_xs___y.buffer.decode(self.nsifr_q_er__) 

            if n__q__c_lpwd is not None and n__q__c_lpwd.buffer is not None:
                b_n__qu_z_ve.transmitable_display_name = n__q__c_lpwd.buffer.decode(self.nsifr_q_er__) 

            if b__ghxmd_x__ is not None and b__ghxmd_x__.buffer is not None:
                b_n__qu_z_ve.originating_address_type = b__ghxmd_x__.buffer.decode(self.nsifr_q_er__) 

            if v__tw_z__g__ is not None and v__tw_z__g__.buffer is not None:
                b_n__qu_z_ve.originating_email_address = v__tw_z__g__.buffer.decode(self.nsifr_q_er__) 

            if _gnin__ie_qe is not None and _gnin__ie_qe.buffer is not None:
                b_n__qu_z_ve.entry_id = _gnin__ie_qe.buffer

            if w_ka_v___vkg is not None and w_ka_v___vkg.buffer is not None:
                b_n__qu_z_ve.search_key = w_ka_v___vkg.buffer

            if me_u_qbxsh__ is not None and me_u_qbxsh__.buffer is not None:
                b_n__qu_z_ve.instance_key = me_u_qbxsh__.buffer

            self.__w_e______y.append(b_n__qu_z_ve)
        
        ___v__z__w_n = 0

        for s in range(len(vi_h__c____n.directory_entries)):

            if isinstance(vi_h__c____n.directory_entries[s], Storage):
                ___v__z__w_n += 1


        for i in range(y___ftj_ixrh):

            hgf_rl_x__j_ = {}
            v_xaz_____o_ = str.format("__attach_version1.0_#{:08X}", i)

            _u___wzy_exl = vi_h__c____n.get_entry(v_xaz_____o_)

            if _u___wzy_exl is None:
                y___ftj_ixrh += 1

                if y___ftj_ixrh > ___v__z__w_n:
                    break

            else:

                ___f_hzd____ = _u___wzy_exl.get_entry("__properties_version1.0")

                u_b__at__inv = Attachment()

                if ___f_hzd____ is not None and ___f_hzd____.buffer is not None:

                    for j in range(8, len(___f_hzd____.buffer), 16):

                        ___z__v__pzg = ___f_hzd____.buffer[j: j + 16]
                        b_c_s____i__ = Property(___z__v__pzg)

                        if b_c_s____i__.size > 0:

                            _____fjs____ = "__substg1.0_" + str.format("{:08X}", b_c_s____i__.tag)

                            if isinstance(_u___wzy_exl.get_entry(_____fjs____), Stream):

                                _y__x___q__b = _u___wzy_exl.get_entry(_____fjs____)

                                if _y__x___q__b is not None and _y__x___q__b.buffer is not None and len(_y__x___q__b.buffer) > 0:
                                    b_c_s____i__.value = _y__x___q__b.buffer

                            elif isinstance(_u___wzy_exl.get_entry(_____fjs____), Storage):

                                th_k_asp_gr_ = _u___wzy_exl.get_entry(_____fjs____)

                                if th_k_asp_gr_ is not None and th_k_asp_gr_.get_entry("__properties_version1.0") is not None:
                                    
                                    _um_djyh_s_u = Message(file_path = None, buffer = None, parent = th_k_asp_gr_)
                                    u_b__at__inv.embedded_message = _um_djyh_s_u

                        nbh__gx____r = str.format("{:08X}", b_c_s____i__.tag)

                        if nbh__gx____r not in hgf_rl_x__j_:
                            hgf_rl_x__j_[nbh__gx____r] = b_c_s____i__
                        

                _vpdd_______ = hgf_rl_x__j_["37140003"] if "37140003" in hgf_rl_x__j_ else None

                if _vpdd_______ is not None and _vpdd_______.value is not None:
                    ycdk____utz_ = int.from_bytes(_vpdd_______.value[0:4], "little")
                    u_b__at__inv.flags = EnumUtil.parse_attachment_flags(ycdk____utz_)
            
                _ob__c___m_j = hgf_rl_x__j_["37050003"] if "37050003" in hgf_rl_x__j_ else None

                if _ob__c___m_j is not None and _ob__c___m_j.value is not None:
                    _zs___wse__o = int.from_bytes(_ob__c___m_j.value[0:4], "little")
                    u_b__at__inv.method = EnumUtil.parse_attachment_method(_zs___wse__o)

                f_____aug_r_ = hgf_rl_x__j_["37100003"] if "37100003" in hgf_rl_x__j_ else None

                if f_____aug_r_ is not None and f_____aug_r_.value is not None:
                    u_b__at__inv.mime_sequence = int.from_bytes(f_____aug_r_.value[0:4], "little")

                __z_m_x__i_g = hgf_rl_x__j_["370B0003"] if "370B0003" in hgf_rl_x__j_ else None

                if __z_m_x__i_g is not None and __z_m_x__i_g.value is not None:
                    u_b__at__inv.rendering_position = int.from_bytes(__z_m_x__i_g.value[0:4], "little")

                g__q____s_bz = hgf_rl_x__j_["0E200003"] if "0E200003" in hgf_rl_x__j_ else None

                if g__q____s_bz is not None and g__q____s_bz.value is not None:
                    u_b__at__inv.size = int.from_bytes(g__q____s_bz.value[0:4], "little")

                ___u__tw_v__ = hgf_rl_x__j_["0FFE0003"] if "0FFE0003" in hgf_rl_x__j_ else None

                if ___u__tw_v__ is not None and ___u__tw_v__.value is not None:
                    _o_hne_f_rh_ = int.from_bytes(___u__tw_v__.value[0:4], "little")
                    u_b__at__inv.object_type = EnumUtil.parse_object_type(_o_hne_f_rh_)

                __gu_______a = hgf_rl_x__j_["7FFE000B"] if "7FFE000B" in hgf_rl_x__j_ else None

                if __gu_______a is not None and __gu_______a.value is not None:
                    __bu___a_u_b = int.from_bytes(__gu_______a.value[0:2], "little")

                    if __bu___a_u_b > 0:
                        u_b__at__inv.is_hidden = True

                _i_thi_e_f_q = hgf_rl_x__j_["7FFF000B"] if "7FFF000B" in hgf_rl_x__j_ else None

                if _i_thi_e_f_q is not None and _i_thi_e_f_q.value is not None:
                    wp_mvm___l_i = int.from_bytes(_i_thi_e_f_q.value[0:4], "little")

                    if wp_mvm___l_i > 0:
                        u_b__at__inv.is_contact_photo = True

                ___s___zs___ = hgf_rl_x__j_["30070040"] if "30070040" in hgf_rl_x__j_ else None

                if ___s___zs___ is not None and ___s___zs___.value is not None:
                    __y__p__pcp_ = int.from_bytes(___s___zs___.value[0: 4], "little")
                    r_b_qx_xblys = int.from_bytes(___s___zs___.value[4: 8], "little")

                    if r_b_qx_xblys > 0:
                        _fi_km_v____ = __y__p__pcp_ + (r_b_qx_xblys << 32)
                        jgv__c_h___y = datetime.datetime(1601,1,1)   

                        try:    
                            u_b__at__inv.creation_time = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                            u_b__at__inv.creation_time = Message.v_____omf__x(u_b__at__inv.creation_time)
                        except:
                            pass 

                eh_____p_f_e = hgf_rl_x__j_["30080040"] if "30080040" in hgf_rl_x__j_ else None

                if eh_____p_f_e is not None and eh_____p_f_e.value is not None:
                    _p__g_n_qkv_ = int.from_bytes(eh_____p_f_e.value[0: 4], "little")
                    _joi___k__pj = int.from_bytes(eh_____p_f_e.value[4: 8], "little")

                    if _joi___k__pj > 0:
                        _fi_km_v____ = _p__g_n_qkv_ + (_joi___k__pj << 32)
                        jgv__c_h___y = datetime.datetime(1601,1,1)   

                        try:    
                            u_b__at__inv.last_modification_time = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                            u_b__at__inv.last_modification_time = Message.v_____omf__x(u_b__at__inv.last_modification_time)
                        except:
                            pass 


                x____ag____d = _u___wzy_exl.get_entry("__substg1.0_370F0102")
                d_w___rm____ = _u___wzy_exl.get_entry("__substg1.0_3711" + self.m__zli___l_b)
                _a_jl_l__wd_ = _u___wzy_exl.get_entry("__substg1.0_3712" + self.m__zli___l_b)
                _b__r__u_t_l = _u___wzy_exl.get_entry("__substg1.0_3713" + self.m__zli___l_b)
                y_gg_w_____g = _u___wzy_exl.get_entry("__substg1.0_3716" + self.m__zli___l_b)
                h__l_s_xg__u = _u___wzy_exl.get_entry("__substg1.0_37010102")
                __w_n__ebi__ = _u___wzy_exl.get_entry("__substg1.0_37020102")
                l_r_____sy_n = _u___wzy_exl.get_entry("__substg1.0_3703" + self.m__zli___l_b)
                z____id_pmfo = _u___wzy_exl.get_entry("__substg1.0_3704" + self.m__zli___l_b)
                _l__sd__i_ty = _u___wzy_exl.get_entry("__substg1.0_3707" + self.m__zli___l_b)
                qgv___m___jv = _u___wzy_exl.get_entry("__substg1.0_370D" + self.m__zli___l_b)
                _tn_qo_g__h_ = _u___wzy_exl.get_entry("__substg1.0_370E" + self.m__zli___l_b)
                j_n__wb_hu__ = _u___wzy_exl.get_entry("__substg1.0_3708" + self.m__zli___l_b)
                ______kd__ov = _u___wzy_exl.get_entry("__substg1.0_37090102")
                b_f_vk____ys = _u___wzy_exl.get_entry("__substg1.0_370A0102")
                __kd_q_y_t__ = _u___wzy_exl.get_entry("__substg1.0_370C" + self.m__zli___l_b)
                xvan_vd__g_l = _u___wzy_exl.get_entry("__substg1.0_3001" + self.m__zli___l_b)  

                if _u___wzy_exl.get_entry("__substg1.0_3701000D") is not None and isinstance(_u___wzy_exl.get_entry("__substg1.0_3701000D"), Storage):
                    mu_l___h_k_n = _u___wzy_exl.get_entry("__substg1.0_3701000D")
                    u_b__at__inv.data_object_storage = mu_l___h_k_n
                    u_b__at__inv.properties_stream = ___f_hzd____

                if x____ag____d is not None and x____ag____d.buffer is not None:
                    u_b__at__inv.additional_info = x____ag____d.buffer

                if d_w___rm____ is not None and d_w___rm____.buffer is not None:
                    u_b__at__inv.content_base = d_w___rm____.buffer.decode(self.nsifr_q_er__)

                if _a_jl_l__wd_ is not None and _a_jl_l__wd_.buffer is not None:
                    u_b__at__inv.content_id = _a_jl_l__wd_.buffer.decode(self.nsifr_q_er__) 

                if _b__r__u_t_l is not None and _b__r__u_t_l.buffer is not None:
                    u_b__at__inv.content_location = _b__r__u_t_l.buffer.decode(self.nsifr_q_er__) 

                if y_gg_w_____g is not None and y_gg_w_____g.buffer is not None:
                    u_b__at__inv.content_disposition = y_gg_w_____g.buffer.decode(self.nsifr_q_er__) 

                if h__l_s_xg__u is not None and h__l_s_xg__u.buffer is not None:
                    u_b__at__inv.data = h__l_s_xg__u.buffer 

                if __w_n__ebi__ is not None and __w_n__ebi__.buffer is not None:
                    u_b__at__inv.encoding = __w_n__ebi__.buffer

                if l_r_____sy_n is not None and l_r_____sy_n.buffer is not None:
                    u_b__at__inv.extension = l_r_____sy_n.buffer.decode(self.nsifr_q_er__) 

                if z____id_pmfo is not None and z____id_pmfo.buffer is not None:
                    u_b__at__inv.file_name = z____id_pmfo.buffer.decode(self.nsifr_q_er__) 

                if _l__sd__i_ty is not None and _l__sd__i_ty.buffer is not None:
                    u_b__at__inv.long_file_name = _l__sd__i_ty.buffer.decode(self.nsifr_q_er__) 

                if qgv___m___jv is not None and qgv___m___jv.buffer is not None:
                    u_b__at__inv.long_path_name = qgv___m___jv.buffer.decode(self.nsifr_q_er__) 

                if _tn_qo_g__h_ is not None and _tn_qo_g__h_.buffer is not None:
                    u_b__at__inv.mime_tag = _tn_qo_g__h_.buffer.decode(self.nsifr_q_er__) 

                if j_n__wb_hu__ is not None and j_n__wb_hu__.buffer is not None:
                    u_b__at__inv.path_name = j_n__wb_hu__.buffer.decode(self.nsifr_q_er__) 

                if ______kd__ov is not None and ______kd__ov.buffer is not None:
                    u_b__at__inv.rendering = ______kd__ov.buffer

                if b_f_vk____ys is not None and b_f_vk____ys.buffer is not None:
                    u_b__at__inv.tag = b_f_vk____ys.buffer

                if __kd_q_y_t__ is not None and __kd_q_y_t__.buffer is not None:
                    u_b__at__inv.transport_name = __kd_q_y_t__.buffer.decode(self.nsifr_q_er__) 

                if xvan_vd__g_l is not None and xvan_vd__g_l.buffer is not None:
                    u_b__at__inv.display_name = xvan_vd__g_l.buffer.decode(self.nsifr_q_er__)

                if u_b__at__inv.data is not None or u_b__at__inv.data_object is not None or u_b__at__inv.data_object_storage is not None or u_b__at__inv.embedded_message is not None:
                    self.uj_c_u_uy___.append(u_b__at__inv)

    def __y_yb____hm(self):

        __iq_pf_pm_j = CompoundFile()
        __iq_pf_pm_j.major_version = 4
        __iq_pf_pm_j.root.class_id = bytes([11, 13, 2, 0, 0, 0, 0, 0, 192, 0, 0, 0, 0, 0, 0, 70])

        k_____chk___ = bytearray()
        wh_e__s___v_ = bytearray()
        ___eq_b_qmb_ = bytearray()

        _jte_gt____a = []

        _jte_gt____a.append(bytes(16))
        _jte_gt____a.append(StandardPropertySet.MAPI)
        _jte_gt____a.append(StandardPropertySet.PUBLIC_STRINGS)

        ______t_vfw_ = []
        y__to_g_____ = {}

        self.__qwshy_x_o_ = []

        b__a___oie__ = self.__tdra____oj(self.__qwshy_x_o_)

        j_ui_rk_yf_e = 0

        for i in range(len(self.__qwshy_x_o_)):
        
            _wa___td__sd = Message.lcuthwob___r(self.__qwshy_x_o_[i].guid, _jte_gt____a)

            if _wa___td__sd == -1 and self.__qwshy_x_o_[i].guid is not None:
            
                _jte_gt____a.append(self.__qwshy_x_o_[i].guid)
                _wa___td__sd = len(_jte_gt____a) - 1
            
            i__d__usa___ = 0
            puwre______t = 0

            if self.__qwshy_x_o_[i].name is not None:
            
                ______t_vfw_.append(self.__qwshy_x_o_[i].name)
                puwre______t = 1

                i__d__usa___ = j_ui_rk_yf_e
            
            else:           
                i__d__usa___ = self.__qwshy_x_o_[i].id            

            ___w_q___lm_ = i

            mj_tgux_g___ = ___w_q___lm_ << 16
            hlcjgtq_hdv_ = _wa___td__sd << 1

            if puwre______t == 1:
                hlcjgtq_hdv_ = hlcjgtq_hdv_ + 1
            
            mj_tgux_g___ = mj_tgux_g___ + hlcjgtq_hdv_

            s_c_______t_ = bytearray(8)
            _h__trr_kix_ = int.to_bytes(i__d__usa___, 4, "little")
            y_____l_____ = int.to_bytes(mj_tgux_g___, 4, "little")

            s_c_______t_[0: 4] = _h__trr_kix_
            s_c_______t_[4: 8] = y_____l_____

            wh_e__s___v_ += s_c_______t_

            if puwre______t == 0:
            
                vyqg_c___ni_ = (0x1000 + ((self.__qwshy_x_o_[i].id ^ _wa___td__sd << 1) % 0x1F))
                vyqg_c___ni_ = (vyqg_c___ni_ << 16) | 0x00000102

                _q__or_ip_dt = str.format("{:08X}", vyqg_c___ni_)
                _q__or_ip_dt = "__substg1.0_" + _q__or_ip_dt

                if _q__or_ip_dt in y__to_g_____:                
                    l__i___n_i__ = y__to_g_____[_q__or_ip_dt]
                    l__i___n_i__ += s_c_______t_
                
                else:                
                    y__to_g_____[_q__or_ip_dt] = s_c_______t_                
            
            else:
            
                ____ffj__m_a = Crc()
                
                ____ffj__m_a.update(self.__qwshy_x_o_[i].name.encode(self.nsifr_q_er__))
                _w__hq_wfaq_ = ____ffj__m_a.value

                vyqg_c___ni_ = (0x1000 + ((_w__hq_wfaq_ ^ ((_wa___td__sd << 1) | 1)) % 0x1F))
                vyqg_c___ni_ = (vyqg_c___ni_ << 16) | 0x00000102

                _q__or_ip_dt = str.format("{:08X}", vyqg_c___ni_)
                _q__or_ip_dt = "__substg1.0_" + _q__or_ip_dt

                if _q__or_ip_dt in y__to_g_____:                
                    l__i___n_i__ = y__to_g_____[_q__or_ip_dt]
                    l__i___n_i__ += s_c_______t_
                
                else:                
                    y__to_g_____[_q__or_ip_dt] = s_c_______t_            

            if self.__qwshy_x_o_[i].name is not None:            
                _bl_____y__u = self.__qwshy_x_o_[i].name.encode(self.h_c_rs_lkt__)
                yb_of___wl_z = len(_bl_____y__u) % 4
                j_ui_rk_yf_e += len(_bl_____y__u) + yb_of___wl_z + 4


        _mm_____tmce = Storage("__nameid_version1.0")

        __dp_i_zi_on = Stream("__substg1.0_00030102", bytes(wh_e__s___v_))

        for i in range(3, len(_jte_gt____a), 1):     
            c_ekl___ri_v = _jte_gt____a[i]
            k_____chk___ += c_ekl___ri_v
        

        ___cdb______ = Stream("__substg1.0_00020102", bytes(k_____chk___))

        for i in range(len(______t_vfw_)):
        
            _bl_____y__u = ______t_vfw_[i].encode(self.h_c_rs_lkt__)
            jgk_vi__jk__ = int.to_bytes(len(_bl_____y__u), 4, "little")

            ___eq_b_qmb_ += jgk_vi__jk__[0: 4]
            ___eq_b_qmb_ += _bl_____y__u

            yb_of___wl_z = len(_bl_____y__u) % 4

            if yb_of___wl_z > 0:
            
                _l_h__d__kbz = bytes(yb_of___wl_z)
                ___eq_b_qmb_ += _l_h__d__kbz
        

        t_zr__jz__uj = Stream("__substg1.0_00040102", bytes(___eq_b_qmb_))

        _mm_____tmce.directory_entries.append(___cdb______)
        _mm_____tmce.directory_entries.append(__dp_i_zi_on)
        _mm_____tmce.directory_entries.append(t_zr__jz__uj)

        for ____t__izh__ in y__to_g_____:
        
            l__i___n_i__ = y__to_g_____[____t__izh__]
            _ui____yc__w = Stream(____t__izh__, l__i___n_i__)
            _mm_____tmce.directory_entries.append(_ui____yc__w)
        

        __iq_pf_pm_j.root.directory_entries.extend(b__a___oie__)        

        __iq_pf_pm_j.root.directory_entries.append(_mm_____tmce)

        return __iq_pf_pm_j.to_bytes()

    def __tdra____oj(self, ou______p___):

        ___xv_ab__p_ = []
        ______oh_ul_ = bytearray()
        x_m_sky_gz__ = len("\0".encode(self.nsifr_q_er__))


        _____h__h__l = 0
        _h_zvq____k_ = int.to_bytes(_____h__h__l, 4, "little")
        _ovkl__ur___ = int.to_bytes(len(self.__w_e______y), 4, "little")
        v__yv______g = int.to_bytes(len(self.uj_c_u_uy___), 4, "little")

        ______oh_ul_ += _h_zvq____k_
        ______oh_ul_ += _h_zvq____k_
        ______oh_ul_ += _ovkl__ur___
        ______oh_ul_ += v__yv______g
        ______oh_ul_ += _ovkl__ur___
        ______oh_ul_ += v__yv______g

        if not self.t__n_____ev_:
            ______oh_ul_ += _h_zvq____k_
            ______oh_ul_ += _h_zvq____k_

        if self.nsifr_q_er__ == self.h_c_rs_lkt__:
            self.m__zli___l_b = "001F"
            self.wiqwtada__v_ = 0x001F
            self.h______id_ai = "101F"
            self._wet__k__o__ = 0x101F

            if StoreSupportMask.UNICODE not in self._y__ti__u__a:
                self._y__ti__u__a.append(StoreSupportMask.UNICODE)

        elif StoreSupportMask.UNICODE in self._y__ti__u__a:
            self._y__ti__u__a.remove(StoreSupportMask.UNICODE)

        if self._y__ti__u__a is not None:
        
            _e__yn___l_v = Property()
            _e__yn___l_v.tag = 0x340D0003
            _e__yn___l_v.type = PropertyType.INTEGER_32
            _e__yn___l_v.value = int.to_bytes(EnumUtil.parse_store_support_mask(self._y__ti__u__a), 4, "little")
            _e__yn___l_v.is_readable = True
            _e__yn___l_v.is_writeable = True

            ______oh_ul_ += _e__yn___l_v.to_bytes()
        

        if self._pq_o______n is not None:
        
            __god__p_s__ = self._pq_o______n.encode(self.nsifr_q_er__)
            yz___fo__kfu = Stream("__substg1.0_001A" + self.m__zli___l_b, __god__p_s__)
            ___xv_ab__p_.append(yz___fo__kfu)

            h_a__o_k___j = Property()
            h_a__o_k___j.tag = 0x001A << 16 | self.wiqwtada__v_
            h_a__o_k___j.type = PropertyType.STRING_8
            h_a__o_k___j.size = len(__god__p_s__) + x_m_sky_gz__
            h_a__o_k___j.is_readable = True
            h_a__o_k___j.is_writeable = True

            ______oh_ul_ += h_a__o_k___j.to_bytes()
        

        if self._xv_y___o___ is not None:
        
            dgq___afua_d = self._xv_y___o___.encode(self.nsifr_q_er__)
            ___l____n_v_ = Stream("__substg1.0_0037" + self.m__zli___l_b, dgq___afua_d)
            ___xv_ab__p_.append(___l____n_v_)

            z_______zqo_ = Property()
            z_______zqo_.tag = 0x0037 << 16 | self.wiqwtada__v_
            z_______zqo_.type = PropertyType.STRING_8
            z_______zqo_.size = len(dgq___afua_d) + x_m_sky_gz__
            z_______zqo_.is_readable = True
            z_______zqo_.is_writeable = True

            ______oh_ul_ += z_______zqo_.to_bytes()
        

        if self._u__q__z___b is not None:
        
            __q____y____ = self._u__q__z___b.encode(self.nsifr_q_er__)
            ___d_taq___q = Stream("__substg1.0_003D" + self.m__zli___l_b, __q____y____)
            ___xv_ab__p_.append(___d_taq___q)

            z_f_g__qs___ = Property()
            z_f_g__qs___.tag = 0x003D << 16 | self.wiqwtada__v_
            z_f_g__qs___.type = PropertyType.STRING_8
            z_f_g__qs___.size = len(__q____y____) + x_m_sky_gz__
            z_f_g__qs___.is_readable = True
            z_f_g__qs___.is_writeable = True

            ______oh_ul_ += z_f_g__qs___.to_bytes()
        

        if self._rz_mvr_yf_p is not None:
        
            ____v___p__h = self._rz_mvr_yf_p.encode(self.nsifr_q_er__)
            x__hpwb____t = Stream("__substg1.0_0070" + self.m__zli___l_b, ____v___p__h)
            ___xv_ab__p_.append(x__hpwb____t)

            __n_uq__umg_ = Property()
            __n_uq__umg_.tag = 0x0070 << 16 | self.wiqwtada__v_
            __n_uq__umg_.type = PropertyType.STRING_8
            __n_uq__umg_.size = len(____v___p__h) + x_m_sky_gz__
            __n_uq__umg_.is_readable = True
            __n_uq__umg_.is_writeable = True

            ______oh_ul_ += __n_uq__umg_.to_bytes()
        

        if self.f_pfu__g_o_p is not None:
        
            mc__jf__j_bm = self.f_pfu__g_o_p.encode(self.nsifr_q_er__)
            hju_rvw__s__ = Stream("__substg1.0_0E02" + self.m__zli___l_b, mc__jf__j_bm)
            ___xv_ab__p_.append(hju_rvw__s__)

            mz____u__s_k = Property()
            mz____u__s_k.tag = 0x0E02 << 16 | self.wiqwtada__v_
            mz____u__s_k.type = PropertyType.STRING_8
            mz____u__s_k.size = len(mc__jf__j_bm) + x_m_sky_gz__
            mz____u__s_k.is_readable = True
            mz____u__s_k.is_writeable = True

            ______oh_ul_ += mz____u__s_k.to_bytes()
        

        if self._nfg_ljsz_d_ is not None:
        
            __xq__s_pk__ = self._nfg_ljsz_d_.encode(self.nsifr_q_er__)
            nxz_y____q__ = Stream("__substg1.0_0E03" + self.m__zli___l_b, __xq__s_pk__)
            ___xv_ab__p_.append(nxz_y____q__)

            ____w_b_n_yz = Property()
            ____w_b_n_yz.tag = 0x0E03 << 16 | self.wiqwtada__v_
            ____w_b_n_yz.type = PropertyType.STRING_8
            ____w_b_n_yz.size = len(__xq__s_pk__) + x_m_sky_gz__
            ____w_b_n_yz.is_readable = True
            ____w_b_n_yz.is_writeable = True

            ______oh_ul_ += ____w_b_n_yz.to_bytes()
        

        if self.v_xe_s_yi_bp is not None:
        
            _d_zu___m__k = self.v_xe_s_yi_bp.encode(self.nsifr_q_er__)
            co__t_enjx_h = Stream("__substg1.0_0E04" + self.m__zli___l_b, _d_zu___m__k)
            ___xv_ab__p_.append(co__t_enjx_h)

            __ctt_lz__qs = Property()
            __ctt_lz__qs.tag = 0x0E04 << 16 | self.wiqwtada__v_
            __ctt_lz__qs.type = PropertyType.STRING_8
            __ctt_lz__qs.size = len(_d_zu___m__k) + x_m_sky_gz__
            __ctt_lz__qs.is_readable = True
            __ctt_lz__qs.is_writeable = True

            ______oh_ul_ += __ctt_lz__qs.to_bytes()
        

        if self.p_j_________ is not None:
        
            ibf___wncc__ = self.p_j_________.encode(self.nsifr_q_er__)
            __n___th___w = Stream("__substg1.0_0074" + self.m__zli___l_b, ibf___wncc__)
            ___xv_ab__p_.append(__n___th___w)

            hzk__s_zucm_ = Property()
            hzk__s_zucm_.tag = 0x0074 << 16 | self.wiqwtada__v_
            hzk__s_zucm_.type = PropertyType.STRING_8
            hzk__s_zucm_.size = len(ibf___wncc__) + x_m_sky_gz__
            hzk__s_zucm_.is_readable = True
            hzk__s_zucm_.is_writeable = True

            ______oh_ul_ += hzk__s_zucm_.to_bytes()
        

        if self.na___bd__o_a is not None:
        
            __i_p_n_s__j = self.na___bd__o_a.encode(self.nsifr_q_er__)
            l___ca___con = Stream("__substg1.0_0050" + self.m__zli___l_b, __i_p_n_s__j)
            ___xv_ab__p_.append(l___ca___con)

            ____i_z_reb_ = Property()
            ____i_z_reb_.tag = 0x0050 << 16 | self.wiqwtada__v_
            ____i_z_reb_.type = PropertyType.STRING_8
            ____i_z_reb_.size = len(__i_p_n_s__j) + x_m_sky_gz__
            ____i_z_reb_.is_readable = True
            ____i_z_reb_.is_writeable = True

            ______oh_ul_ += ____i_z_reb_.to_bytes()


            _u_____t__mt = Message._q_l_tivr__j(self.na___bd__o_a)

            qq_lo_z__m_z = Stream("__substg1.0_004F0102", _u_____t__mt)
            ___xv_ab__p_.append(qq_lo_z__m_z)

            dkb_x___xe__ = Property()
            dkb_x___xe__.tag = 0x004F0102
            dkb_x___xe__.type = PropertyType.BINARY
            dkb_x___xe__.size = len(_u_____t__mt)
            dkb_x___xe__.is_readable = True
            dkb_x___xe__.is_writeable = True

            ______oh_ul_ += dkb_x___xe__.to_bytes()
        

        if self.d_w____xbnru is not None:
        
            __rhqf__u__p = self.d_w____xbnru.encode(self.nsifr_q_er__)
            __f__ll__ili = Stream("__substg1.0_0E1D" + self.m__zli___l_b, __rhqf__u__p)
            ___xv_ab__p_.append(__f__ll__ili)

            y___ke__uhjn = Property()
            y___ke__uhjn.tag = 0x0E1D << 16 | self.wiqwtada__v_
            y___ke__uhjn.type = PropertyType.STRING_8
            y___ke__uhjn.size = len(__rhqf__u__p) + x_m_sky_gz__
            y___ke__uhjn.is_readable = True
            y___ke__uhjn.is_writeable = True

            ______oh_ul_ += y___ke__uhjn.to_bytes()
        

        if self.____y_gej_ly is not None:
        
            _rs___ha_d__ = self.____y_gej_ly.encode(self.nsifr_q_er__)
            i_c__r_v_z__ = Stream("__substg1.0_1000" + self.m__zli___l_b, _rs___ha_d__)
            ___xv_ab__p_.append(i_c__r_v_z__)

            ___q__s__cf_ = Property()
            ___q__s__cf_.tag = 0x1000 << 16 | self.wiqwtada__v_
            ___q__s__cf_.type = PropertyType.STRING_8
            ___q__s__cf_.size =len(_rs___ha_d__) + x_m_sky_gz__
            ___q__s__cf_.is_readable = True
            ___q__s__cf_.is_writeable = True

            ______oh_ul_ += ___q__s__cf_.to_bytes()
        

        if self._h_b_v_d____ is not None:
        
            yegf_me___g_ = Stream("__substg1.0_10090102", self._h_b_v_d____)
            ___xv_ab__p_.append(yegf_me___g_)

            uv___d_p_xgw = Property()
            uv___d_p_xgw.tag = 0x10090102
            uv___d_p_xgw.type = PropertyType.BINARY
            uv___d_p_xgw.size = len(self._h_b_v_d____)
            uv___d_p_xgw.is_readable = True
            uv___d_p_xgw.is_writeable = True

            ______oh_ul_ += uv___d_p_xgw.to_bytes()
        

        if self.__i___m_ncy_ is not None:
        
            lhku_o___e__ = Stream("__substg1.0_300B0102", self.__i___m_ncy_)
            ___xv_ab__p_.append(lhku_o___e__)

            xlq_brmbqs__ = Property()
            xlq_brmbqs__.tag = 0x300B0102
            xlq_brmbqs__.type = PropertyType.BINARY
            xlq_brmbqs__.size = len(self.__i___m_ncy_)
            xlq_brmbqs__.is_readable = True
            xlq_brmbqs__.is_writeable = True

            ______oh_ul_ += xlq_brmbqs__.to_bytes()
        

        if self.fhgy_b_an_h_ is not None:
        
            i__atoqs__d_ = Stream("__substg1.0_65E20102", self.fhgy_b_an_h_)
            ___xv_ab__p_.append(i__atoqs__d_)

            q___ku____kj = Property()
            q___ku____kj.tag = 0x65E20102
            q___ku____kj.type = PropertyType.BINARY
            q___ku____kj.size = len(self.fhgy_b_an_h_)
            q___ku____kj.is_readable = True
            q___ku____kj.is_writeable = True

            ______oh_ul_ += q___ku____kj.to_bytes()
        

        if self.__j__stw_l_u is not None:
        
            _u_me_c___rv = Stream("__substg1.0_0FFF0102", self.__j__stw_l_u)
            ___xv_ab__p_.append(_u_me_c___rv)

            vg__a__cy___ = Property()
            vg__a__cy___.tag = 0x0FFF0102
            vg__a__cy___.type = PropertyType.BINARY
            vg__a__cy___.size = len(self.__j__stw_l_u)
            vg__a__cy___.is_readable = True
            vg__a__cy___.is_writeable = True

            ______oh_ul_ += vg__a__cy___.to_bytes()
        

        if self.___k________ is not None:
        
            __f_wp_z_zaf = Stream("__substg1.0_00460102", self.___k________)
            ___xv_ab__p_.append(__f_wp_z_zaf)

            _z__g__a____ = Property()
            _z__g__a____.tag = 0x00460102
            _z__g__a____.type = PropertyType.BINARY
            _z__g__a____.size = len(self.___k________)
            _z__g__a____.is_readable = True
            _z__g__a____.is_writeable = True

            ______oh_ul_ += _z__g__a____.to_bytes()
        

        if self.vbn_jd_xc_c_ is not None:
        
            kprqnqfykb__ = Stream("__substg1.0_00530102", self.vbn_jd_xc_c_)
            ___xv_ab__p_.append(kprqnqfykb__)

            fmi_w____p_j = Property()
            fmi_w____p_j.tag = 0x00530102
            fmi_w____p_j.type = PropertyType.BINARY
            fmi_w____p_j.size = len(self.vbn_jd_xc_c_)
            fmi_w____p_j.is_readable = True
            fmi_w____p_j.is_writeable = True

            ______oh_ul_ += fmi_w____p_j.to_bytes()
        

        if self.__v_r_____n_ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            mmbq__b_gylp = Property()
            mmbq__b_gylp.tag = 0x30070040
            mmbq__b_gylp.type = PropertyType.TIME
            mmbq__b_gylp.value = du___g__abr_
            mmbq__b_gylp.is_readable = True
            mmbq__b_gylp.is_writeable = False

            ______oh_ul_ += mmbq__b_gylp.to_bytes()
        

        if self._onw__vy_til > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._onw__vy_til - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            o_pkf_syr_jf = Property()
            o_pkf_syr_jf.tag = 0x30080040
            o_pkf_syr_jf.type = PropertyType.TIME
            o_pkf_syr_jf.value = du___g__abr_
            o_pkf_syr_jf.is_readable = True
            o_pkf_syr_jf.is_writeable = False

            ______oh_ul_ += o_pkf_syr_jf.to_bytes()
        

        if self.p__ia_c_i_i_ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.p__ia_c_i_i_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            e_o__v__t__e = Property()
            e_o__v__t__e.tag = 0x0E060040
            e_o__v__t__e.type = PropertyType.TIME
            e_o__v__t__e.value = du___g__abr_
            e_o__v__t__e.is_readable = True
            e_o__v__t__e.is_writeable = True

            ______oh_ul_ += e_o__v__t__e.to_bytes()
        

        if self.o_d_dh_dp_z_ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.o_d_dh_dp_z_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _r__ug______ = Property()
            _r__ug______.tag = 0x00390040
            _r__ug______.type = PropertyType.TIME
            _r__ug______.value = du___g__abr_
            _r__ug______.is_readable = True
            _r__ug______.is_writeable = True

            ______oh_ul_ += _r__ug______.to_bytes()
        

        if self._____ngk_oi_ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._____ngk_oi_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _i__y___iz_v = Property()
            _i__y___iz_v.tag = 0x000F0040
            _i__y___iz_v.type = PropertyType.TIME
            _i__y___iz_v.value = du___g__abr_
            _i__y___iz_v.is_readable = True
            _i__y___iz_v.is_writeable = True

            ______oh_ul_ += _i__y___iz_v.to_bytes()
        

        if self._anq_obd_oq_ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._anq_obd_oq_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            we__z_wr____ = Property()
            we__z_wr____.tag = 0x00480040
            we__z_wr____.type = PropertyType.TIME
            we__z_wr____.value = du___g__abr_
            we__z_wr____.is_readable = True
            we__z_wr____.is_writeable = True

            ______oh_ul_ += we__z_wr____.to_bytes()
        

        if self.tl_tqbr__xyq > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.tl_tqbr__xyq - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _huadg_e___t = Property()
            _huadg_e___t.tag = 0x00320040
            _huadg_e___t.type = PropertyType.TIME
            _huadg_e___t.value = du___g__abr_
            _huadg_e___t.is_readable = True
            _huadg_e___t.is_writeable = True

            ______oh_ul_ += _huadg_e___t.to_bytes()
        

        if self.om____q_____ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.om____q_____ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _xz___fgon_v = Property()
            _xz___fgon_v.tag = 0x10820040
            _xz___fgon_v.type = PropertyType.TIME
            _xz___fgon_v.value = du___g__abr_
            _xz___fgon_v.is_readable = True
            _xz___fgon_v.is_writeable = True

            ______oh_ul_ += _xz___fgon_v.to_bytes()
        

        if self.twqm_____n_r is not None:
        
            knts______x_ = self.twqm_____n_r.encode(self.nsifr_q_er__)
            __u_j_tu_lfu = Stream("__substg1.0_1001" + self.m__zli___l_b, knts______x_)
            ___xv_ab__p_.append(__u_j_tu_lfu)

            _rgbx_rw__s_ = Property()
            _rgbx_rw__s_.tag = 0x1001 << 16 | self.wiqwtada__v_
            _rgbx_rw__s_.type = PropertyType.STRING_8
            _rgbx_rw__s_.size = len(knts______x_) + x_m_sky_gz__
            _rgbx_rw__s_.is_readable = True
            _rgbx_rw__s_.is_writeable = True

            ______oh_ul_ += _rgbx_rw__s_.to_bytes()
        

        if self.____y_kuq__q is not None:
        
            __eexe_v_pe_ = self.____y_kuq__q.encode(self.nsifr_q_er__)
            zcu_tlz_k___ = Stream("__substg1.0_3FF8" + self.m__zli___l_b, __eexe_v_pe_)
            ___xv_ab__p_.append(zcu_tlz_k___)

            __z_i_nk__h_ = Property()
            __z_i_nk__h_.tag = 0x3FF8 << 16 | self.wiqwtada__v_
            __z_i_nk__h_.type = PropertyType.STRING_8
            __z_i_nk__h_.size = len(__eexe_v_pe_) + x_m_sky_gz__
            __z_i_nk__h_.is_readable = True
            __z_i_nk__h_.is_writeable = True

            ______oh_ul_ += __z_i_nk__h_.to_bytes()
        

        if self.___zp_upib__ is not None:
        
            w___c___a_bm = self.___zp_upib__.encode(self.nsifr_q_er__)
            u_zro__oz__a = Stream("__substg1.0_3FFA" + self.m__zli___l_b, w___c___a_bm)
            ___xv_ab__p_.append(u_zro__oz__a)

            _m_eay_g__pg = Property()
            _m_eay_g__pg.tag = 0x3FFA << 16 | self.wiqwtada__v_
            _m_eay_g__pg.type = PropertyType.STRING_8
            _m_eay_g__pg.size = len(w___c___a_bm) + x_m_sky_gz__
            _m_eay_g__pg.is_readable = True
            _m_eay_g__pg.is_writeable = True

            ______oh_ul_ += _m_eay_g__pg.to_bytes()
        

        if self.____w_h_sni_ is not None:
        
            ___lehhv_fid = self.____w_h_sni_.encode(self.nsifr_q_er__)
            ys_hwx____n_ = Stream("__substg1.0_1035" + self.m__zli___l_b, ___lehhv_fid)
            ___xv_ab__p_.append(ys_hwx____n_)

            ____b___r___ = Property()
            ____b___r___.tag = 0x1035 << 16 | self.wiqwtada__v_
            ____b___r___.type = PropertyType.STRING_8
            ____b___r___.size = len(___lehhv_fid) + x_m_sky_gz__
            ____b___r___.is_readable = True
            ____b___r___.is_writeable = True

            ______oh_ul_ += ____b___r___.to_bytes()
        

        if self._______eft__ is not None:
        
            jyg_da_qiw__ = self._______eft__.encode(self.nsifr_q_er__)
            _m___u__qq__ = Stream("__substg1.0_1042" + self.m__zli___l_b, jyg_da_qiw__)
            ___xv_ab__p_.append(_m___u__qq__)

            w_l_dlo___s_ = Property()
            w_l_dlo___s_.tag = 0x1042 << 16 | self.wiqwtada__v_
            w_l_dlo___s_.type = PropertyType.STRING_8
            w_l_dlo___s_.size = len(jyg_da_qiw__) + x_m_sky_gz__
            w_l_dlo___s_.is_readable = True
            w_l_dlo___s_.is_writeable = True

            ______oh_ul_ += w_l_dlo___s_.to_bytes()
        

        if self._fio_i_c_few is not None:
        
            mnsz___v_ac_ = self._fio_i_c_few.encode(self.nsifr_q_er__)
            ____cx_u_z_r = Stream("__substg1.0_1039" + self.m__zli___l_b, mnsz___v_ac_)
            ___xv_ab__p_.append(____cx_u_z_r)

            zp_r_r_v___l = Property()
            zp_r_r_v___l.tag = 0x1039 << 16 | self.wiqwtada__v_
            zp_r_r_v___l.type = PropertyType.STRING_8
            zp_r_r_v___l.size = len(mnsz___v_ac_) + x_m_sky_gz__
            zp_r_r_v___l.is_readable = True
            zp_r_r_v___l.is_writeable = True

            ______oh_ul_ += zp_r_r_v___l.to_bytes()
        

        if self.juou_jp_axl_ > 0:
        
            dnqo_elc____ = Property()
            dnqo_elc____.tag = 0x3FFD0003
            dnqo_elc____.type = PropertyType.INTEGER_32
            dnqo_elc____.value = int.to_bytes(self.juou_jp_axl_, 4, "little")
            dnqo_elc____.is_readable = True
            dnqo_elc____.is_writeable = True

            ______oh_ul_ += dnqo_elc____.to_bytes()
        

        if self.kw_x_qi_w_s_ > 0:
        
            ___sm___ad__ = Property()
            ___sm___ad__.tag = 0x10800003
            ___sm___ad__.type = PropertyType.INTEGER_32
            ___sm___ad__.value = int.to_bytes(self.kw_x_qi_w_s_, 4, "little")
            ___sm___ad__.is_readable = True
            ___sm___ad__.is_writeable = True

            ______oh_ul_ += ___sm___ad__.to_bytes()
        

        if self.d__m___n____ > 0:
        
            _fyve___m_jr = Property()
            _fyve___m_jr.tag = 0x0E080003
            _fyve___m_jr.type = PropertyType.INTEGER_32
            _fyve___m_jr.value = int.to_bytes(self.d__m___n____, 4, "little")
            _fyve___m_jr.is_readable = True
            _fyve___m_jr.is_writeable = True

            ______oh_ul_ += _fyve___m_jr.to_bytes()
        

        if self.c______ny_uq is not None and len(self.c______ny_uq) > 0:
        
            q__v_ow___ct = Property()
            q__v_ow___ct.tag = 0x0E070003
            q__v_ow___ct.type = PropertyType.INTEGER_32
            q__v_ow___ct.value = int.to_bytes(EnumUtil.parse_message_flag(self.c______ny_uq), 4, "little")
            q__v_ow___ct.is_readable = True
            q__v_ow___ct.is_writeable = True

            ______oh_ul_ += q__v_ow___ct.to_bytes()
        

        if self._x_____y___i > 0:
        
            e_hi__pq___s = Property()
            e_hi__pq___s.tag = 0x3FDE0003
            e_hi__pq___s.type = PropertyType.INTEGER_32
            e_hi__pq___s.value = int.to_bytes(self._x_____y___i, 4, "little")
            e_hi__pq___s.is_readable = True
            e_hi__pq___s.is_writeable = True

            ______oh_ul_ += e_hi__pq___s.to_bytes()
        

        if self.k_kt_xqc____ is not None:
        
            n_dk_k__ls_l = Stream("__substg1.0_00710102", self.k_kt_xqc____)
            ___xv_ab__p_.append(n_dk_k__ls_l)

            __d__gzp__q_ = Property()
            __d__gzp__q_.tag = 0x00710102
            __d__gzp__q_.type = PropertyType.BINARY
            __d__gzp__q_.size = len(self.k_kt_xqc____)
            __d__gzp__q_.is_readable = True
            __d__gzp__q_.is_writeable = True

            ______oh_ul_ += __d__gzp__q_.to_bytes()
        

        if self.o__ic_zjug_e:
        
            gabuuneaq___ = Property()
            gabuuneaq___.tag = 0x10F4000B
            gabuuneaq___.type = PropertyType.BOOLEAN
            gabuuneaq___.value = int.to_bytes(1,1,"little")
            gabuuneaq___.is_readable = True
            gabuuneaq___.is_writeable = True

            ______oh_ul_ += gabuuneaq___.to_bytes()
        

        if self.__kpffcnr___:
        
            _qf__v_h_u_o = Property()
            _qf__v_h_u_o.tag = 0x10F6000B
            _qf__v_h_u_o.type = PropertyType.BOOLEAN
            _qf__v_h_u_o.value = int.to_bytes(1,1,"little")
            _qf__v_h_u_o.is_readable = True
            _qf__v_h_u_o.is_writeable = True

            ______oh_ul_ += _qf__v_h_u_o.to_bytes()
        

        if self.we__f_y__hbo:
        
            _______ta_d_ = Property()
            _______ta_d_.tag = 0x10F5000B
            _______ta_d_.type = PropertyType.BOOLEAN
            _______ta_d_.value = int.to_bytes(1,1,"little")
            _______ta_d_.is_readable = True
            _______ta_d_.is_writeable = True

            ______oh_ul_ += _______ta_d_.to_bytes()
        

        if self.xa_____a___v:
        
            __w__g___asu = Property()
            __w__g___asu.tag = 0x10F2000B
            __w__g___asu.type = PropertyType.BOOLEAN
            __w__g___asu.value = int.to_bytes(1,1,"little")
            __w__g___asu.is_readable = True
            __w__g___asu.is_writeable = True

            ______oh_ul_ += __w__g___asu.to_bytes()
        

        if len(self.uj_c_u_uy___) > 0:
        
            t_f_a__qvieg = Property()
            t_f_a__qvieg.tag = 0x0E1B000B
            t_f_a__qvieg.type = PropertyType.BOOLEAN
            t_f_a__qvieg.value = int.to_bytes(1,1,"little")
            t_f_a__qvieg.is_readable = True
            t_f_a__qvieg.is_writeable = True

            ______oh_ul_ += t_f_a__qvieg.to_bytes()
        

        if self.___g_ta__tfn:
        
            z_f_crftu__q = Property()
            z_f_crftu__q.tag = 0x0E1F000B
            z_f_crftu__q.type = PropertyType.BOOLEAN
            z_f_crftu__q.value = int.to_bytes(1,1,"little")
            z_f_crftu__q.is_readable = True
            z_f_crftu__q.is_writeable = True

            ______oh_ul_ += z_f_crftu__q.to_bytes()
        

        if self.sg_____x____:
        
            _v_g_h_z__q_ = Property()
            _v_g_h_z__q_.tag = 0x0029000B
            _v_g_h_z__q_.type = PropertyType.BOOLEAN
            _v_g_h_z__q_.value = int.to_bytes(1,1,"little")
            _v_g_h_z__q_.is_readable = True
            _v_g_h_z__q_.is_writeable = True

            ______oh_ul_ += _v_g_h_z__q_.to_bytes()
        

        if self._vhmwqhr__cd:
        
            u_skkn__nu__ = Property()
            u_skkn__nu__.tag = 0x0023000B
            u_skkn__nu__.type = PropertyType.BOOLEAN
            u_skkn__nu__.value = int.to_bytes(1,1,"little")
            u_skkn__nu__.is_readable = True
            u_skkn__nu__.is_writeable = True

            ______oh_ul_ += u_skkn__nu__.to_bytes()
        

        if self.zpz__r____ji is not None:
        
            v___w_lcyv_g = Stream("__substg1.0_10130102", self.zpz__r____ji)
            ___xv_ab__p_.append(v___w_lcyv_g)

            __l_____g_y_ = Property()
            __l_____g_y_.tag = 0x10130102
            __l_____g_y_.type = PropertyType.BINARY
            __l_____g_y_.size = len(self.zpz__r____ji)
            __l_____g_y_.is_readable = True
            __l_____g_y_.is_writeable = True

            ______oh_ul_ += __l_____g_y_.to_bytes()
        

        if self.___wh_qn____ is not Sensitivity.NONE:
        
            ___oxca_yr_p = Property()
            ___oxca_yr_p.tag = 0x00360003
            ___oxca_yr_p.type = PropertyType.INTEGER_32
            ___oxca_yr_p.value = int.to_bytes(EnumUtil.parse_sensitivity(self.___wh_qn____), 4, "little")
            ___oxca_yr_p.is_readable = True
            ___oxca_yr_p.is_writeable = True

            ______oh_ul_ += ___oxca_yr_p.to_bytes()
        

        if self._ox_qg_e____ is not LastVerbExecuted.NONE:
        
            m_____x_syjn = Property()
            m_____x_syjn.tag = 0x10810003
            m_____x_syjn.type = PropertyType.INTEGER_32
            m_____x_syjn.value = int.to_bytes(EnumUtil.parse_last_verb_executed(self._ox_qg_e____), 4, "little")
            m_____x_syjn.is_readable = True
            m_____x_syjn.is_writeable = True

            ______oh_ul_ += m_____x_syjn.to_bytes()
        

        if self._b_ue__y_z__ is not Importance.NONE:
        
            _ngdhn__wjxi = Property()
            _ngdhn__wjxi.tag = 0x00170003
            _ngdhn__wjxi.type = PropertyType.INTEGER_32
            _ngdhn__wjxi.value = int.to_bytes(EnumUtil.parse_importance(self._b_ue__y_z__), 4, "little")
            _ngdhn__wjxi.is_readable = True
            _ngdhn__wjxi.is_writeable = True

            ______oh_ul_ += _ngdhn__wjxi.to_bytes()
        

        if self._ci_____r_uk is not Priority.NONE:
        
            __j_ome__k_a = Property()
            __j_ome__k_a.tag = 0x00260003
            __j_ome__k_a.type = PropertyType.INTEGER_32
            __j_ome__k_a.value = int.to_bytes(EnumUtil.parse_priority(self._ci_____r_uk), 4, "little")
            __j_ome__k_a.is_readable = True
            __j_ome__k_a.is_writeable = True

            ______oh_ul_ += __j_ome__k_a.to_bytes()
        

        if self.w__hc___o___ is not FlagIcon.NONE:
        
            b__x_el___n_ = Property()
            b__x_el___n_.tag = 0x10950003
            b__x_el___n_.type = PropertyType.INTEGER_32
            b__x_el___n_.value = int.to_bytes(EnumUtil.parse_flag_icon(self.w__hc___o___), 4, "little")
            b__x_el___n_.is_readable = True
            b__x_el___n_.is_writeable = True

            ______oh_ul_ += b__x_el___n_.to_bytes()
        

        if self._b_a_v___hjn is not FlagStatus.NONE:
        
            w_u_____kc_b = Property()
            w_u_____kc_b.tag = 0x10900003
            w_u_____kc_b.type = PropertyType.INTEGER_32
            w_u_____kc_b.value = int.to_bytes(EnumUtil.parse_flag_status(self._b_a_v___hjn), 4, "little")
            w_u_____kc_b.is_readable = True
            w_u_____kc_b.is_writeable = True

            ______oh_ul_ += w_u_____kc_b.to_bytes()
        

        if self.v___w_dliib_ is not ObjectType.NONE:
        
            o______jc_u_ = Property()
            o______jc_u_.tag = 0x0FFE0003
            o______jc_u_.type = PropertyType.INTEGER_32
            o______jc_u_.value = int.to_bytes(EnumUtil.parse_object_type(self.v___w_dliib_), 4, "little")
            o______jc_u_.is_readable = True
            o______jc_u_.is_writeable = True

            ______oh_ul_ += o______jc_u_.to_bytes()
        

        if self._vry_n_v_d_g is not None:
        
            jub_s____w__ = self._vry_n_v_d_g.encode(self.nsifr_q_er__)
            __r_rmj_l_o_ = Stream("__substg1.0_0077" + self.m__zli___l_b, jub_s____w__)
            ___xv_ab__p_.append(__r_rmj_l_o_)

            x_g_____d___ = Property()
            x_g_____d___.tag = 0x0077 << 16 | self.wiqwtada__v_
            x_g_____d___.type = PropertyType.STRING_8
            x_g_____d___.size = len(jub_s____w__) + x_m_sky_gz__
            x_g_____d___.is_readable = True
            x_g_____d___.is_writeable = True

            ______oh_ul_ += x_g_____d___.to_bytes()
        

        if self.___x_ry__twg is not None:
        
            z_vv_kt_k__c = self.___x_ry__twg.encode(self.nsifr_q_er__)
            kaoy__kg___y = Stream("__substg1.0_0078" + self.m__zli___l_b, z_vv_kt_k__c)
            ___xv_ab__p_.append(kaoy__kg___y)

            _s_y_myn____ = Property()
            _s_y_myn____.tag = 0x0078 << 16 | self.wiqwtada__v_
            _s_y_myn____.type = PropertyType.STRING_8
            _s_y_myn____.size = len(z_vv_kt_k__c) + x_m_sky_gz__
            _s_y_myn____.is_readable = True
            _s_y_myn____.is_writeable = True

            ______oh_ul_ += _s_y_myn____.to_bytes()
        

        if self.___h_____oo_ is not None:
        
            z_b_x_____lr = Stream("__substg1.0_00430102", self.___h_____oo_)
            ___xv_ab__p_.append(z_b_x_____lr)

            ___ct__g__y_ = Property()
            ___ct__g__y_.tag = 0x00430102
            ___ct__g__y_.type = PropertyType.BINARY
            ___ct__g__y_.size = len(self.___h_____oo_)
            ___ct__g__y_.is_readable = True
            ___ct__g__y_.is_writeable = True

            ______oh_ul_ += ___ct__g__y_.to_bytes()
        

        if self.b_o_l__vz__j is not None:
        
            ___o_xam_jqb = self.b_o_l__vz__j.encode(self.nsifr_q_er__)
            ___ujx_l__g_ = Stream("__substg1.0_0044" + self.m__zli___l_b, ___o_xam_jqb)
            ___xv_ab__p_.append(___ujx_l__g_)

            __k____j_ybo = Property()
            __k____j_ybo.tag = 0x0044 << 16 | self.wiqwtada__v_
            __k____j_ybo.type = PropertyType.STRING_8
            __k____j_ybo.size = len(___o_xam_jqb) + x_m_sky_gz__
            __k____j_ybo.is_readable = True
            __k____j_ybo.is_writeable = True

            ______oh_ul_ += __k____j_ybo.to_bytes()
        

        if self.ehp_zo_hnnk_ is not None:
        
            ______da_k_i = Stream("__substg1.0_00520102", self.ehp_zo_hnnk_)
            ___xv_ab__p_.append(______da_k_i)

            e___g____s__ = Property()
            e___g____s__.tag = 0x00520102
            e___g____s__.type = PropertyType.BINARY
            e___g____s__.size = len(self.ehp_zo_hnnk_)
            e___g____s__.is_readable = True
            e___g____s__.is_writeable = True

            ______oh_ul_ += e___g____s__.to_bytes()
        

        if self._k__vn_qvf__ is not None:
        
            _uv______q__ = self._k__vn_qvf__.encode(self.nsifr_q_er__)
            ___r__r_t_a_ = Stream("__substg1.0_0075" + self.m__zli___l_b, _uv______q__)
            ___xv_ab__p_.append(___r__r_t_a_)

            k___aztn_m__ = Property()
            k___aztn_m__.tag = 0x0075 << 16 | self.wiqwtada__v_
            k___aztn_m__.type = PropertyType.STRING_8
            k___aztn_m__.size = len(_uv______q__) + x_m_sky_gz__
            k___aztn_m__.is_readable = True
            k___aztn_m__.is_writeable = True

            ______oh_ul_ += k___aztn_m__.to_bytes()
        

        if self._x___qkj___e is not None:
        
            d____sn__bsn = self._x___qkj___e.encode(self.nsifr_q_er__)
            tgurf_l_____ = Stream("__substg1.0_0076" + self.m__zli___l_b, d____sn__bsn)
            ___xv_ab__p_.append(tgurf_l_____)

            _w___r_hggsp = Property()
            _w___r_hggsp.tag = 0x0076 << 16 | self.wiqwtada__v_
            _w___r_hggsp.type = PropertyType.STRING_8
            _w___r_hggsp.size = len(d____sn__bsn) + x_m_sky_gz__
            _w___r_hggsp.is_readable = True
            _w___r_hggsp.is_writeable = True

            ______oh_ul_ += _w___r_hggsp.to_bytes()
        

        if self.__ynoc______ is not None:
        
            x_ov_maw_t__ = Stream("__substg1.0_003F0102", self.__ynoc______)
            ___xv_ab__p_.append(x_ov_maw_t__)

            llj_jh__x_it = Property()
            llj_jh__x_it.tag = 0x003F0102
            llj_jh__x_it.type = PropertyType.BINARY
            llj_jh__x_it.size = len(self.__ynoc______)
            llj_jh__x_it.is_readable = True
            llj_jh__x_it.is_writeable = True

            ______oh_ul_ += llj_jh__x_it.to_bytes()
        

        if self.nn__l___z_p_ is not None:
        
            _frva__a___i = self.nn__l___z_p_.encode(self.nsifr_q_er__)
            ___ur_j__rf_ = Stream("__substg1.0_0040" + self.m__zli___l_b, _frva__a___i)
            ___xv_ab__p_.append(___ur_j__rf_)

            ___qv__e_i__ = Property()
            ___qv__e_i__.tag = 0x0040 << 16 | self.wiqwtada__v_
            ___qv__e_i__.type = PropertyType.STRING_8
            ___qv__e_i__.size = len(_frva__a___i) + x_m_sky_gz__
            ___qv__e_i__.is_readable = True
            ___qv__e_i__.is_writeable = True

            ______oh_ul_ += ___qv__e_i__.to_bytes()
        

        if self.d_vn__f____i is not None:
        
            _as_w__ei__w = Stream("__substg1.0_00510102", self.d_vn__f____i)
            ___xv_ab__p_.append(_as_w__ei__w)

            _j_n_p_dy___ = Property()
            _j_n_p_dy___.tag = 0x00510102
            _j_n_p_dy___.type = PropertyType.BINARY
            _j_n_p_dy___.size = len(self.d_vn__f____i)
            _j_n_p_dy___.is_readable = True
            _j_n_p_dy___.is_writeable = True

            ______oh_ul_ += _j_n_p_dy___.to_bytes()
        

        if self.t___f_____hz is not None:
        
            __y__fm___qn = self.t___f_____hz.encode(self.nsifr_q_er__)
            kdr_______r_ = Stream("__substg1.0_0C1E" + self.m__zli___l_b, __y__fm___qn)
            ___xv_ab__p_.append(kdr_______r_)

            _w_k____sus_ = Property()
            _w_k____sus_.tag = 0x0C1E << 16 | self.wiqwtada__v_
            _w_k____sus_.type = PropertyType.STRING_8
            _w_k____sus_.size = len(__y__fm___qn) + x_m_sky_gz__
            _w_k____sus_.is_readable = True
            _w_k____sus_.is_writeable = True

            ______oh_ul_ += _w_k____sus_.to_bytes()
        

        if self.__rfliczcge_ is not None:
        
            ___sjz____f_ = self.__rfliczcge_.encode(self.nsifr_q_er__)
            _hp_f___vjg_ = Stream("__substg1.0_0C1F" + self.m__zli___l_b, ___sjz____f_)
            ___xv_ab__p_.append(_hp_f___vjg_)

            ___m_cb_ml_s = Property()
            ___m_cb_ml_s.tag = 0x0C1F << 16 | self.wiqwtada__v_
            ___m_cb_ml_s.type = PropertyType.STRING_8
            ___m_cb_ml_s.size = len(___sjz____f_) + x_m_sky_gz__
            ___m_cb_ml_s.is_readable = True
            ___m_cb_ml_s.is_writeable = True

            ______oh_ul_ += ___m_cb_ml_s.to_bytes()
        

        if self.______qcsd_d is not None:
        
            itos__l_____ = self.______qcsd_d.encode(self.nsifr_q_er__)
            a____h___t__ = Stream("__substg1.0_5D01" + self.m__zli___l_b, itos__l_____)
            ___xv_ab__p_.append(a____h___t__)

            __txn_k__l_x = Property()
            __txn_k__l_x.tag = 0x5D01 << 16 | self.wiqwtada__v_
            __txn_k__l_x.type = PropertyType.STRING_8
            __txn_k__l_x.size = len(itos__l_____) + x_m_sky_gz__
            __txn_k__l_x.is_readable = True
            __txn_k__l_x.is_writeable = True

            ______oh_ul_ += __txn_k__l_x.to_bytes()
        

        if self.insn_u______ is not None:
        
            _arld_rt_v_h = Stream("__substg1.0_0C190102", self.insn_u______)
            ___xv_ab__p_.append(_arld_rt_v_h)

            rv__nl_py_mw = Property()
            rv__nl_py_mw.tag = 0x0C190102
            rv__nl_py_mw.type = PropertyType.BINARY
            rv__nl_py_mw.size = len(self.insn_u______)
            rv__nl_py_mw.is_readable = True
            rv__nl_py_mw.is_writeable = True

            ______oh_ul_ += rv__nl_py_mw.to_bytes()
        

        if self.v_x__v____fh is not None:
        
            xh___m__sghl = self.v_x__v____fh.encode(self.nsifr_q_er__)
            _____ft_v___ = Stream("__substg1.0_0C1A" + self.m__zli___l_b, xh___m__sghl)
            ___xv_ab__p_.append(_____ft_v___)

            _d__in___r__ = Property()
            _d__in___r__.tag = 0x0C1A << 16 | self.wiqwtada__v_
            _d__in___r__.type = PropertyType.STRING_8
            _d__in___r__.size = len(xh___m__sghl) + x_m_sky_gz__
            _d__in___r__.is_readable = True
            _d__in___r__.is_writeable = True

            ______oh_ul_ += _d__in___r__.to_bytes()
        

        if self._a__y_vf_eib is not None:
        
            _p_tchg___pg = Stream("__substg1.0_0C1D0102", self._a__y_vf_eib)
            ___xv_ab__p_.append(_p_tchg___pg)

            m_yejr_z____ = Property()
            m_yejr_z____.tag = 0x0C1D0102
            m_yejr_z____.type = PropertyType.BINARY
            m_yejr_z____.size = len(self._a__y_vf_eib)
            m_yejr_z____.is_readable = True
            m_yejr_z____.is_writeable = True

            ______oh_ul_ += m_yejr_z____.to_bytes()
        

        if self.xep__h_t__f_ is not None:
        
            v_s_x_yxx_zh = self.xep__h_t__f_.encode(self.nsifr_q_er__)
            ____n_t_w___ = Stream("__substg1.0_0064" + self.m__zli___l_b, v_s_x_yxx_zh)
            ___xv_ab__p_.append(____n_t_w___)

            _t__oz_crbd_ = Property()
            _t__oz_crbd_.tag = 0x0064 << 16 | self.wiqwtada__v_
            _t__oz_crbd_.type = PropertyType.STRING_8
            _t__oz_crbd_.size = len(v_s_x_yxx_zh) + x_m_sky_gz__
            _t__oz_crbd_.is_readable = True
            _t__oz_crbd_.is_writeable = True

            ______oh_ul_ += _t__oz_crbd_.to_bytes()
        

        if self._w_tq___xpkm is not None:
        
            h__e_s____bn = self._w_tq___xpkm.encode(self.nsifr_q_er__)
            __z_x_ny_t__ = Stream("__substg1.0_0065" + self.m__zli___l_b, h__e_s____bn)
            ___xv_ab__p_.append(__z_x_ny_t__)

            o__gb_b_z___ = Property()
            o__gb_b_z___.tag = 0x0065 << 16 | self.wiqwtada__v_
            o__gb_b_z___.type = PropertyType.STRING_8
            o__gb_b_z___.size = len(h__e_s____bn) + x_m_sky_gz__
            o__gb_b_z___.is_readable = True
            o__gb_b_z___.is_writeable = True

            ______oh_ul_ += o__gb_b_z___.to_bytes()
        

        if self.__tl__v__h__ is not None:
        
            ___nekg____c = self.__tl__v__h__.encode(self.nsifr_q_er__)
            o_icic_ll__y = Stream("__substg1.0_5D02" + self.m__zli___l_b, ___nekg____c)
            ___xv_ab__p_.append(o_icic_ll__y)

            r_n_fty___z_ = Property()
            r_n_fty___z_.tag = 0x5D02 << 16 | self.wiqwtada__v_
            r_n_fty___z_.type = PropertyType.STRING_8
            r_n_fty___z_.size = len(___nekg____c) + x_m_sky_gz__
            r_n_fty___z_.is_readable = True
            r_n_fty___z_.is_writeable = True

            ______oh_ul_ += r_n_fty___z_.to_bytes()
        

        if self.rle_hef_uum_ is not None:
        
            __et_qh_____ = Stream("__substg1.0_00410102", self.rle_hef_uum_)
            ___xv_ab__p_.append(__et_qh_____)

            c_ea_ff_mkk_ = Property()
            c_ea_ff_mkk_.tag = 0x00410102
            c_ea_ff_mkk_.type = PropertyType.BINARY
            c_ea_ff_mkk_.size = len(self.rle_hef_uum_)
            c_ea_ff_mkk_.is_readable = True
            c_ea_ff_mkk_.is_writeable = True

            ______oh_ul_ += c_ea_ff_mkk_.to_bytes()
        

        if self.____d_yy__gy is not None:
        
            _______l_yev = self.____d_yy__gy.encode(self.nsifr_q_er__)
            yfd__eaoh_d_ = Stream("__substg1.0_0042" + self.m__zli___l_b, _______l_yev)
            ___xv_ab__p_.append(yfd__eaoh_d_)

            i__o_ldg__l_ = Property()
            i__o_ldg__l_.tag = 0x0042 << 16 | self.wiqwtada__v_
            i__o_ldg__l_.type = PropertyType.STRING_8
            i__o_ldg__l_.size = len(_______l_yev) + x_m_sky_gz__
            i__o_ldg__l_.is_readable = True
            i__o_ldg__l_.is_writeable = True

            ______oh_ul_ += i__o_ldg__l_.to_bytes()
        

        if self._fb_znz_lkv_ is not None:
        
            ___xn___sgd_ = Stream("__substg1.0_003B0102", self._fb_znz_lkv_)
            ___xv_ab__p_.append(___xn___sgd_)

            ___m_____wo_ = Property()
            ___m_____wo_.tag = 0x003B0102
            ___m_____wo_.type = PropertyType.BINARY
            ___m_____wo_.size = len(self._fb_znz_lkv_)
            ___m_____wo_.is_readable = True
            ___m_____wo_.is_writeable = True

            ______oh_ul_ += ___m_____wo_.to_bytes()
        

        if self.__z__nhb_s__ is not None:
        
            yfr_om____ud = self.__z__nhb_s__.encode(self.nsifr_q_er__)
            t_w_t__ny_eq = Stream("__substg1.0_007D" + self.m__zli___l_b, yfr_om____ud)
            ___xv_ab__p_.append(t_w_t__ny_eq)

            _ff_jkf___o_ = Property()
            _ff_jkf___o_.tag = 0x007D << 16 | self.wiqwtada__v_
            _ff_jkf___o_.type = PropertyType.STRING_8
            _ff_jkf___o_.size = len(yfr_om____ud) + x_m_sky_gz__
            _ff_jkf___o_.is_readable = True
            _ff_jkf___o_.is_writeable = True

            ______oh_ul_ += _ff_jkf___o_.to_bytes()
        

        if self.__naz_____bg is not None:
        
            y_______r__m = NamedProperty()
            y_______r__m.id = 0x8554
            y_______r__m.guid = StandardPropertySet.COMMON
            y_______r__m.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, y_______r__m)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(y_______r__m)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            eyg_bo_____h = self.__naz_____bg.encode(self.nsifr_q_er__)
            rzrn____oq_o = Stream("__substg1.0_" + o__n_l__j__v, eyg_bo_____h)
            ___xv_ab__p_.append(rzrn____oq_o)

            a_w_mg_a_g__ = Property()
            a_w_mg_a_g__.tag = __rud_dv_c_t
            a_w_mg_a_g__.type = PropertyType.STRING_8
            a_w_mg_a_g__.size = len(eyg_bo_____h) + x_m_sky_gz__
            a_w_mg_a_g__.is_readable = True
            a_w_mg_a_g__.is_writeable = True

            ______oh_ul_ += a_w_mg_a_g__.to_bytes()
        

        if self.ikw_q___t_ck > 0:
        
            k___dl_vgr__ = NamedProperty()
            k___dl_vgr__.id = 0x8552
            k___dl_vgr__.guid = StandardPropertySet.COMMON
            k___dl_vgr__.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, k___dl_vgr__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(k___dl_vgr__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            k_knlf_np_e_ = Property()
            k_knlf_np_e_.tag = __rud_dv_c_t
            k_knlf_np_e_.type = PropertyType.INTEGER_32
            k_knlf_np_e_.value = int.to_bytes(self.ikw_q___t_ck, 4, "little")
            k_knlf_np_e_.is_readable = True
            k_knlf_np_e_.is_writeable = True

            ______oh_ul_ += k_knlf_np_e_.to_bytes()
        

        if self.u_wj__bz__ue > datetime.datetime(1901,1,1):
        
            _us____z_xe_ = NamedProperty()
            _us____z_xe_.id = 0x8516
            _us____z_xe_.guid = StandardPropertySet.COMMON
            _us____z_xe_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _us____z_xe_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_us____z_xe_)
                ___w_q___lm_ = len(ou______p___) - 1
            
            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _zt__qi_cd_k = Property()
            _zt__qi_cd_k.tag = __rud_dv_c_t
            _zt__qi_cd_k.type = PropertyType.TIME
            _zt__qi_cd_k.value = du___g__abr_
            _zt__qi_cd_k.is_readable = True
            _zt__qi_cd_k.is_writeable = True

            ______oh_ul_ += _zt__qi_cd_k.to_bytes()
        

        if self._pcg__fmli__ > datetime.datetime(1901,1,1):
        
            _____a_y_u_s = NamedProperty()
            _____a_y_u_s.id = 0x8517
            _____a_y_u_s.guid = StandardPropertySet.COMMON
            _____a_y_u_s.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _____a_y_u_s)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_____a_y_u_s)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            h_rk___q_q_l = Property()
            h_rk___q_q_l.tag = __rud_dv_c_t
            h_rk___q_q_l.type = PropertyType.TIME
            h_rk___q_q_l.value = du___g__abr_
            h_rk___q_q_l.is_readable = True
            h_rk___q_q_l.is_writeable = True

            ______oh_ul_ += h_rk___q_q_l.to_bytes()
        

        if self.w__j_w______ > datetime.datetime(1901,1,1):
        
            qm____h_x_sd = NamedProperty()
            qm____h_x_sd.id = 0x8560
            qm____h_x_sd.guid = StandardPropertySet.COMMON
            qm____h_x_sd.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, qm____h_x_sd)

            if ___w_q___lm_ == -1:

                ou______p___.append(qm____h_x_sd)
                ___w_q___lm_ = len(ou______p___) - 1          

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _b__r_da____ = Property()
            _b__r_da____.tag = __rud_dv_c_t
            _b__r_da____.type = PropertyType.TIME
            _b__r_da____.value = du___g__abr_
            _b__r_da____.is_readable = True
            _b__r_da____.is_writeable = True

            ______oh_ul_ += _b__r_da____.to_bytes()
        

        if len(self.lb_im_l__ptk) > 0:
        
            ______r___g_ = NamedProperty()
            ______r___g_.id = 0x8539
            ______r___g_.guid = StandardPropertySet.COMMON
            ______r___g_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ______r___g_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(______r___g_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self._wet__k__o__
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _ixa____a__k = bytearray()

            for i in range(len(self.lb_im_l__ptk)):
            
                ydr___u_____ = (self.lb_im_l__ptk[i] + "\0").encode(self.nsifr_q_er__)
                w__ar_s__m__ = len(ydr___u_____)
                zy______o___ = int.to_bytes(w__ar_s__m__, 4, "little")

                _ixa____a__k += zy______o___

                _q__or_ip_dt = "__substg1.0_" + o__n_l__j__v + "-" + str.format("{:08X}", i)

                ce_______bq_ = Stream(_q__or_ip_dt, ydr___u_____)
                ___xv_ab__p_.append(ce_______bq_)
            

            _____k_fbsih = bytes(_ixa____a__k)

            _a_y_r_m__pn = Stream("__substg1.0_" + o__n_l__j__v, _____k_fbsih)
            ___xv_ab__p_.append(_a_y_r_m__pn)

            j_jd_sx_p_mz = Property()
            j_jd_sx_p_mz.tag = __rud_dv_c_t
            j_jd_sx_p_mz.type = PropertyType.MULTIPLE_STRING_8
            j_jd_sx_p_mz.size = len(_____k_fbsih)
            j_jd_sx_p_mz.is_readable = True
            j_jd_sx_p_mz.is_writeable = True

            ______oh_ul_ += j_jd_sx_p_mz.to_bytes()
        

        if len(self._____kd_o_cn) > 0:
        
            __pv___z____ = NamedProperty()
            __pv___z____.id = 0x853A
            __pv___z____.guid = StandardPropertySet.COMMON
            __pv___z____.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __pv___z____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__pv___z____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self._wet__k__o__
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ma____j__gde = bytearray()

            for i in range(len(self._____kd_o_cn)):
            
                _____cp____t = (self._____kd_o_cn[i] + "\0").encode(self.nsifr_q_er__)
                w__ar_s__m__ = len(_____cp____t)
                zy______o___ = int.to_bytes(w__ar_s__m__, 4, "little")

                ma____j__gde += zy______o___

                _q__or_ip_dt = "__substg1.0_" + o__n_l__j__v + "-" + str.format("{:08X}", i)

                _nv_rk_clqa_ = Stream(_q__or_ip_dt, _____cp____t)
                ___xv_ab__p_.append(_nv_rk_clqa_)
            

            vrgpss__ge__ = bytes(ma____j__gde)

            y__l__o_org_ = Stream("__substg1.0_" + o__n_l__j__v, vrgpss__ge__)
            ___xv_ab__p_.append(y__l__o_org_)

            _mv__n__k_ay = Property()
            _mv__n__k_ay.tag = __rud_dv_c_t
            _mv__n__k_ay.type = PropertyType.MULTIPLE_STRING_8
            _mv__n__k_ay.size = len(vrgpss__ge__)
            _mv__n__k_ay.is_readable = True
            _mv__n__k_ay.is_writeable = True

            ______oh_ul_ += _mv__n__k_ay.to_bytes()
        

        if len(self._mk___k_rw_y) > 0:
        
            r_d__lm___p_ = NamedProperty()
            r_d__lm___p_.Name = "Keywords"
            r_d__lm___p_.guid = StandardPropertySet.PUBLIC_STRINGS
            r_d__lm___p_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, r_d__lm___p_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(r_d__lm___p_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self._wet__k__o__
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            m__s_______v = bytearray()

            for i in range(len(self._mk___k_rw_y)):
            
                s___lp_kh__r = (self._mk___k_rw_y[i] + "\0").encode(self.nsifr_q_er__)
                w__ar_s__m__ = len(s___lp_kh__r)
                zy______o___ = int.to_bytes(w__ar_s__m__, 4, "little")

                m__s_______v += zy______o___

                _q__or_ip_dt = "__substg1.0_" + o__n_l__j__v + "-" + str.format("{:08X}", i)

                g__a___d_hy_ = Stream(_q__or_ip_dt, s___lp_kh__r)
                ___xv_ab__p_.append(g__a___d_hy_)
            

            _x_____t____ = bytes(m__s_______v)

            hj___k_f____ = Stream("__substg1.0_" + o__n_l__j__v, _x_____t____)
            ___xv_ab__p_.append(hj___k_f____)

            iix__a______ = Property()
            iix__a______.tag = __rud_dv_c_t
            iix__a______.type = PropertyType.MULTIPLE_STRING_8
            iix__a______.size = len(_x_____t____)
            iix__a______.is_readable = True
            iix__a______.is_writeable = True

            ______oh_ul_ += iix__a______.to_bytes()
        

        if self.giyc___g__o_ is not None:
        
            _e_i__ue_kl_ = NamedProperty()
            _e_i__ue_kl_.id = 0x8535
            _e_i__ue_kl_.guid = StandardPropertySet.COMMON
            _e_i__ue_kl_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _e_i__ue_kl_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_e_i__ue_kl_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _kv__y______ = self.giyc___g__o_.encode(self.nsifr_q_er__)
            _krn____iul_ = Stream("__substg1.0_" + o__n_l__j__v, _kv__y______)
            ___xv_ab__p_.append(_krn____iul_)

            _qv_on_de_wa = Property()
            _qv_on_de_wa.tag = __rud_dv_c_t
            _qv_on_de_wa.type = PropertyType.STRING_8
            _qv_on_de_wa.size = len(_kv__y______) + x_m_sky_gz__
            _qv_on_de_wa.is_readable = True
            _qv_on_de_wa.is_writeable = True

            ______oh_ul_ += _qv_on_de_wa.to_bytes()
        

        if self._t__expt_i_d is not None:
        
            _p____o__ox_ = NamedProperty()
            _p____o__ox_.id = 0x8534
            _p____o__ox_.guid = StandardPropertySet.COMMON
            _p____o__ox_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _p____o__ox_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_p____o__ox_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            __xxd_p__ek_ = self._t__expt_i_d.encode(self.nsifr_q_er__)
            _u_bde_____m = Stream("__substg1.0_" + o__n_l__j__v, __xxd_p__ek_)
            ___xv_ab__p_.append(_u_bde_____m)

            fi__h____cb_ = Property()
            fi__h____cb_.tag = __rud_dv_c_t
            fi__h____cb_.type = PropertyType.STRING_8
            fi__h____cb_.size = len(__xxd_p__ek_) + x_m_sky_gz__
            fi__h____cb_.is_readable = True
            fi__h____cb_.is_writeable = True

            ______oh_ul_ += fi__h____cb_.to_bytes()
        

        if self._et__ia_vcjd is not None:
        
            _rv_o_idsq_g = NamedProperty()
            _rv_o_idsq_g.id = 0x8580
            _rv_o_idsq_g.guid = StandardPropertySet.COMMON
            _rv_o_idsq_g.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _rv_o_idsq_g)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_rv_o_idsq_g)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ____q_rsc_e_ = self._et__ia_vcjd.encode(self.nsifr_q_er__)
            ef_yr__g___o = Stream("__substg1.0_" + o__n_l__j__v, ____q_rsc_e_)
            ___xv_ab__p_.append(ef_yr__g___o)

            b__u___z_tmq = Property()
            b__u___z_tmq.tag = __rud_dv_c_t
            b__u___z_tmq.type = PropertyType.STRING_8
            b__u___z_tmq.size = len(____q_rsc_e_) + x_m_sky_gz__
            b__u___z_tmq.is_readable = True
            b__u___z_tmq.is_writeable = True

            ______oh_ul_ += b__u___z_tmq.to_bytes()
        

        if self.____za___j_w is not None:
        
            _m__ukvytq_m = NamedProperty()
            _m__ukvytq_m.id = 0x851F
            _m__ukvytq_m.guid = StandardPropertySet.COMMON
            _m__ukvytq_m.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _m__ukvytq_m)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_m__ukvytq_m)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ___la____t__ = self.____za___j_w.encode(self.nsifr_q_er__)
            __p_wiqg___i = Stream("__substg1.0_" + o__n_l__j__v, ___la____t__)
            ___xv_ab__p_.append(__p_wiqg___i)

            _vrk_ymyk___ = Property()
            _vrk_ymyk___.tag = __rud_dv_c_t
            _vrk_ymyk___.type = PropertyType.STRING_8
            _vrk_ymyk___.size = len(___la____t__) + x_m_sky_gz__
            _vrk_ymyk___.is_readable = True
            _vrk_ymyk___.is_writeable = True

            ______oh_ul_ += _vrk_ymyk___.to_bytes()
        

        if self._st_____rh_q:
        
            _k_y___w___a = NamedProperty()
            _k_y___w___a.id = 0x8506
            _k_y___w___a.guid = StandardPropertySet.COMMON
            _k_y___w___a.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _k_y___w___a)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_k_y___w___a)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            _bam__q__gsh = Property()
            _bam__q__gsh.tag = __rud_dv_c_t
            _bam__q__gsh.type = PropertyType.BOOLEAN
            _bam__q__gsh.value = int.to_bytes(1,1,"little")
            _bam__q__gsh.is_readable = True
            _bam__q__gsh.is_writeable = True

            ______oh_ul_ += _bam__q__gsh.to_bytes()
        

        if self._o__________:
        
            __ry__nh_q_d = NamedProperty()
            __ry__nh_q_d.id = 0x851C
            __ry__nh_q_d.guid = StandardPropertySet.COMMON
            __ry__nh_q_d.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __ry__nh_q_d)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__ry__nh_q_d)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            n_v_zmm_v_o_ = Property()
            n_v_zmm_v_o_.tag = __rud_dv_c_t
            n_v_zmm_v_o_.type = PropertyType.BOOLEAN
            n_v_zmm_v_o_.value = int.to_bytes(1,1,"little")
            n_v_zmm_v_o_.is_readable = True
            n_v_zmm_v_o_.is_writeable = True

            ______oh_ul_ += n_v_zmm_v_o_.to_bytes()
        

        if self.r____dmo__a_:
        
            ___x_____oy_ = NamedProperty()
            ___x_____oy_.id = 0x851E
            ___x_____oy_.guid = StandardPropertySet.COMMON
            ___x_____oy_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ___x_____oy_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(___x_____oy_) 
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            ____ecj_pb_o = Property()
            ____ecj_pb_o.tag = __rud_dv_c_t
            ____ecj_pb_o.type = PropertyType.BOOLEAN
            ____ecj_pb_o.value = int.to_bytes(1,1,"little")
            ____ecj_pb_o.is_readable = True
            ____ecj_pb_o.is_writeable = True

            ______oh_ul_ += ____ecj_pb_o.to_bytes()
        

        if self.cq_m_axum___ > datetime.datetime(1901,1,1):
        
            _d__gxxn__u_ = NamedProperty()
            _d__gxxn__u_.id = 0x820D
            _d__gxxn__u_.guid = StandardPropertySet.APPOINTMENT
            _d__gxxn__u_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _d__gxxn__u_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_d__gxxn__u_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _b_k_____x_l = Property()
            _b_k_____x_l.tag = __rud_dv_c_t
            _b_k_____x_l.type = PropertyType.TIME
            _b_k_____x_l.value = du___g__abr_
            _b_k_____x_l.is_readable = True
            _b_k_____x_l.is_writeable = True

            ______oh_ul_ += _b_k_____x_l.to_bytes()
        

        if self.zr___i__g_q_ > datetime.datetime(1901,1,1):
        
            jg_v_l__z__q = NamedProperty()
            jg_v_l__z__q.id = 0x820E
            jg_v_l__z__q.guid = StandardPropertySet.APPOINTMENT
            jg_v_l__z__q.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, jg_v_l__z__q)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(jg_v_l__z__q)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            __s_m_lw_t_a = Property()
            __s_m_lw_t_a.tag = __rud_dv_c_t
            __s_m_lw_t_a.type = PropertyType.TIME
            __s_m_lw_t_a.value = du___g__abr_
            __s_m_lw_t_a.is_readable = True
            __s_m_lw_t_a.is_writeable = True

            ______oh_ul_ += __s_m_lw_t_a.to_bytes()
        

        if self.w_yd__qc_q__ is not None:
        
            x_m_ix___b_d = NamedProperty()
            x_m_ix___b_d.id = 0x8208
            x_m_ix___b_d.guid = StandardPropertySet.APPOINTMENT
            x_m_ix___b_d.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, x_m_ix___b_d)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(x_m_ix___b_d)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            p_l____xxpdc = self.w_yd__qc_q__.encode(self.nsifr_q_er__)
            z_gv__tf___m = Stream("__substg1.0_" + o__n_l__j__v, p_l____xxpdc)
            ___xv_ab__p_.append(z_gv__tf___m)

            _n_e______lt = Property()
            _n_e______lt.tag = __rud_dv_c_t
            _n_e______lt.type = PropertyType.STRING_8
            _n_e______lt.size = len(p_l____xxpdc) + x_m_sky_gz__
            _n_e______lt.is_readable = True
            _n_e______lt.is_writeable = True

            ______oh_ul_ += _n_e______lt.to_bytes()
        

        if self.h_o_z_mo_h__ is not None:
        
            i_ka__zow_qr = NamedProperty()
            i_ka__zow_qr.id = 0x24
            i_ka__zow_qr.guid = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5])
            i_ka__zow_qr.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, i_ka__zow_qr)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(i_ka__zow_qr)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _a_hzrowj__p = self.h_o_z_mo_h__.encode(self.nsifr_q_er__)
            __p___rb_jn_ = Stream("__substg1.0_" + o__n_l__j__v, _a_hzrowj__p)
            ___xv_ab__p_.append(__p___rb_jn_)

            __f__k____dy = Property()
            __f__k____dy.tag = __rud_dv_c_t
            __f__k____dy.type = PropertyType.STRING_8
            __f__k____dy.size = len(_a_hzrowj__p) + x_m_sky_gz__
            __f__k____dy.is_readable = True
            __f__k____dy.is_writeable = True

            ______oh_ul_ += __f__k____dy.to_bytes()
        

        if self._____egyzai_ is not None:
        
            _x____y____c = NamedProperty()
            _x____y____c.id = 0x8234
            _x____y____c.guid = StandardPropertySet.APPOINTMENT
            _x____y____c.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _x____y____c)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_x____y____c)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ___q__t_gb__ = self._____egyzai_.encode(self.nsifr_q_er__)
            __flv__p____ = Stream("__substg1.0_" + o__n_l__j__v, ___q__t_gb__)
            ___xv_ab__p_.append(__flv__p____)

            twuxoxg_____ = Property()
            twuxoxg_____.tag = __rud_dv_c_t
            twuxoxg_____.type = PropertyType.STRING_8
            twuxoxg_____.size = len(___q__t_gb__) + x_m_sky_gz__
            twuxoxg_____.is_readable = True
            twuxoxg_____.is_writeable = True

            ______oh_ul_ += twuxoxg_____.to_bytes()
        

        if self._vs_t_ntls_l is not None:
        
            _w___i__x_rb = NamedProperty()
            _w___i__x_rb.id = 0x8232
            _w___i__x_rb.guid = StandardPropertySet.APPOINTMENT
            _w___i__x_rb.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _w___i__x_rb)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_w___i__x_rb)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _or__h_b_m_k = self._vs_t_ntls_l.encode(self.nsifr_q_er__)
            ____r_j_____ = Stream("__substg1.0_" + o__n_l__j__v, _or__h_b_m_k)
            ___xv_ab__p_.append(____r_j_____)

            _w___i__x_rb = Property()
            _w___i__x_rb.tag = __rud_dv_c_t
            _w___i__x_rb.type = PropertyType.STRING_8
            _w___i__x_rb.size = len(_or__h_b_m_k) + x_m_sky_gz__
            _w___i__x_rb.is_readable = True
            _w___i__x_rb.is_writeable = True

            ______oh_ul_ += _w___i__x_rb.to_bytes()
        

        if self.yl__e__fnwt_ != BusyStatus.NONE:
        
            cw___wb_pj__ = NamedProperty()
            cw___wb_pj__.id = 0x8205
            cw___wb_pj__.guid = StandardPropertySet.APPOINTMENT
            cw___wb_pj__.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, cw___wb_pj__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(cw___wb_pj__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            __l_x___p___ = Property()
            __l_x___p___.tag = __rud_dv_c_t
            __l_x___p___.type = PropertyType.INTEGER_32
            __l_x___p___.value = int.to_bytes(EnumUtil.parse_busy_status(self.yl__e__fnwt_), 4, "little")
            __l_x___p___.is_readable = True
            __l_x___p___.is_writeable = True

            ______oh_ul_ += __l_x___p___.to_bytes()
        

        if self.__w_uoq___s_ != MeetingStatus.NONE:
        
            bmq__hb__s_v = NamedProperty()
            bmq__hb__s_v.id = 0x8217
            bmq__hb__s_v.guid = StandardPropertySet.APPOINTMENT
            bmq__hb__s_v.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, bmq__hb__s_v)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(bmq__hb__s_v)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            w__x__t_u_wn = Property()
            w__x__t_u_wn.tag = __rud_dv_c_t
            w__x__t_u_wn.type = PropertyType.INTEGER_32
            w__x__t_u_wn.value = int.to_bytes(EnumUtil.parse_meeting_status(self.__w_uoq___s_), 4, "little")
            w__x__t_u_wn.is_readable = True
            w__x__t_u_wn.is_writeable = True

            ______oh_ul_ += w__x__t_u_wn.to_bytes()
        

        if self.____f_kom_m_ != ResponseStatus.NONE:
        
            q_rgmslv_ds_ = NamedProperty()
            q_rgmslv_ds_.id = 0x8218
            q_rgmslv_ds_.guid = StandardPropertySet.APPOINTMENT
            q_rgmslv_ds_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, q_rgmslv_ds_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(q_rgmslv_ds_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            _qs_co__pu__ = Property()
            _qs_co__pu__.tag = __rud_dv_c_t
            _qs_co__pu__.type = PropertyType.INTEGER_32
            _qs_co__pu__.value = int.to_bytes(EnumUtil.parse_response_status(self.____f_kom_m_), 4, "little")
            _qs_co__pu__.is_readable = True
            _qs_co__pu__.is_writeable = True

            ______oh_ul_ += _qs_co__pu__.to_bytes()
        

        if self.___utdtdt_yw != RecurrenceType.NONE:
        
            _hxi__x_____ = NamedProperty()
            _hxi__x_____.id = 0x8231
            _hxi__x_____.guid = StandardPropertySet.APPOINTMENT
            _hxi__x_____.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _hxi__x_____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_hxi__x_____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            u__nx_fqjcs_ = Property()
            u__nx_fqjcs_.tag = __rud_dv_c_t
            u__nx_fqjcs_.type = PropertyType.INTEGER_32
            u__nx_fqjcs_.value = int.to_bytes(EnumUtil.parse_recurrence_type(self.___utdtdt_yw), 4, "little")
            u__nx_fqjcs_.is_readable = True
            u__nx_fqjcs_.is_writeable = True

            ______oh_ul_ += u__nx_fqjcs_.to_bytes()
        

        if self._oi___li_yx_ is not None:
        
            ___w__a_z_bh = NamedProperty()
            ___w__a_z_bh.id = 0x3
            ___w__a_z_bh.guid = bytes([144, 218, 216, 110, 11, 69, 27, 16, 152, 218, 0, 170, 0, 63, 19, 5]) 
            ___w__a_z_bh.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ___w__a_z_bh)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(___w__a_z_bh)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0102
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ___cdb______ = Stream("__substg1.0_" + o__n_l__j__v, self._oi___li_yx_)
            ___xv_ab__p_.append(___cdb______)

            ___uf___j__y = Property()
            ___uf___j__y.tag = __rud_dv_c_t
            ___uf___j__y.type = PropertyType.INTEGER_32
            ___uf___j__y.size = len(self._oi___li_yx_)
            ___uf___j__y.is_readable = True
            ___uf___j__y.is_writeable = True

            ______oh_ul_ += ___uf___j__y.to_bytes()
        

        if self.ls_m_lek_i_c > -1:
        
            __wui_jid_ch = NamedProperty()
            __wui_jid_ch.id = 0x8214
            __wui_jid_ch.guid = StandardPropertySet.APPOINTMENT
            __wui_jid_ch.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __wui_jid_ch)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__wui_jid_ch)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            __g_____zq_c = Property()
            __g_____zq_c.tag = __rud_dv_c_t
            __g_____zq_c.type = PropertyType.INTEGER_32
            __g_____zq_c.value = int.to_bytes(self.ls_m_lek_i_c, 4, "little")
            __g_____zq_c.is_readable = True
            __g_____zq_c.is_writeable = True

            ______oh_ul_ += __g_____zq_c.to_bytes()
        

        if self.j__vi__y_vh_ > 0:
        
            _z_____rl___ = NamedProperty()
            _z_____rl___.id = 0x8213
            _z_____rl___.guid = StandardPropertySet.APPOINTMENT
            _z_____rl___.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _z_____rl___)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_z_____rl___)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            __j_o_xa____ = Property()
            __j_o_xa____.tag = __rud_dv_c_t
            __j_o_xa____.type = PropertyType.INTEGER_32
            __j_o_xa____.value = int.to_bytes(self.j__vi__y_vh_, 4, "little")
            __j_o_xa____.is_readable = True
            __j_o_xa____.is_writeable = True

            ______oh_ul_ += __j_o_xa____.to_bytes()       


        if self.ug__bxm__u__ is not None:
        
            ___ks__e___g = NamedProperty()
            ___ks__e___g.id = 0x811F
            ___ks__e___g.guid = StandardPropertySet.TASK
            ___ks__e___g.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ___ks__e___g)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(___ks__e___g)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _k__c_b__tb_ = self.ug__bxm__u__.encode(self.nsifr_q_er__)
            ____y__q__b_ = Stream("__substg1.0_" + o__n_l__j__v, _k__c_b__tb_)
            ___xv_ab__p_.append(____y__q__b_)

            ___x_aulj__i = Property()
            ___x_aulj__i.tag = __rud_dv_c_t
            ___x_aulj__i.type = PropertyType.STRING_8
            ___x_aulj__i.size = len(_k__c_b__tb_) + x_m_sky_gz__
            ___x_aulj__i.is_readable = True
            ___x_aulj__i.is_writeable = True

            ______oh_ul_ += ___x_aulj__i.to_bytes()
        

        if self._dznn_vo__f_ is not None:
        
            _v__k_iu_poh = NamedProperty()
            _v__k_iu_poh.id = 0x8121
            _v__k_iu_poh.guid = StandardPropertySet.TASK
            _v__k_iu_poh.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _v__k_iu_poh)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_v__k_iu_poh)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            __e_c_henbhz = self._dznn_vo__f_.encode(self.nsifr_q_er__)
            __v_y_p____g = Stream("__substg1.0_" + o__n_l__j__v, __e_c_henbhz)
            ___xv_ab__p_.append(__v_y_p____g)

            ___ydzf_____ = Property()
            ___ydzf_____.tag = __rud_dv_c_t
            ___ydzf_____.type = PropertyType.STRING_8
            ___ydzf_____.size = len(__e_c_henbhz) + x_m_sky_gz__
            ___ydzf_____.is_readable = True
            ___ydzf_____.is_writeable = True

            ______oh_ul_ += ___ydzf_____.to_bytes()
        

        if self.cw_z___z____ > 0:
        
            _heww_g_i___ = NamedProperty()
            _heww_g_i___.id = 0x8102
            _heww_g_i___.guid = StandardPropertySet.TASK
            _heww_g_i___.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _heww_g_i___)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_heww_g_i___)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0005

            m__i____h_rw = Property()
            m__i____h_rw.tag = __rud_dv_c_t
            m__i____h_rw.type = PropertyType.FLOATING_64
            m__i____h_rw.value = int.to_bytes(0, 8, "little")
            m__i____h_rw.is_readable = True
            m__i____h_rw.is_writeable = True

            ______oh_ul_ += m__i____h_rw.to_bytes()
        

        if self.__c_q_q____g > 0:
        
            m___q__ydjkz = NamedProperty()
            m___q__ydjkz.id = 0x8110
            m___q__ydjkz.guid = StandardPropertySet.TASK
            m___q__ydjkz.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, m___q__ydjkz)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(m___q__ydjkz)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            _z______dv_w = Property()
            _z______dv_w.tag = __rud_dv_c_t
            _z______dv_w.type = PropertyType.INTEGER_32
            _z______dv_w.value = int.to_bytes(self.__c_q_q____g, 4, "little")
            _z______dv_w.is_readable = True
            _z______dv_w.is_writeable = True

            ______oh_ul_ += _z______dv_w.to_bytes()
        

        if self.kk____qaf_je > 0:
        
            s___c_____il = NamedProperty()
            s___c_____il.id = 0x8111
            s___c_____il.guid = StandardPropertySet.TASK
            s___c_____il.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, s___c_____il)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(s___c_____il)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            jg___n_t_n__ = Property()
            jg___n_t_n__.tag = __rud_dv_c_t
            jg___n_t_n__.type = PropertyType.INTEGER_32
            jg___n_t_n__.value = int.to_bytes(self.kk____qaf_je, 4, "little")
            jg___n_t_n__.is_readable = True
            jg___n_t_n__.is_writeable = True

            ______oh_ul_ += jg___n_t_n__.to_bytes()
        

        if self.hd____j__j__:
        
            __ezw__t_f__ = NamedProperty()
            __ezw__t_f__.id = 0x8103
            __ezw__t_f__.guid = StandardPropertySet.TASK
            __ezw__t_f__.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __ezw__t_f__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__ezw__t_f__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            _______w_b__ = Property()
            _______w_b__.tag = __rud_dv_c_t
            _______w_b__.type = PropertyType.BOOLEAN
            _______w_b__.value = int.to_bytes(1,1,"little")
            _______w_b__.is_readable = True
            _______w_b__.is_writeable = True

            ______oh_ul_ += _______w_b__.to_bytes()
        

        if self.__gn_p___y__:
        
            _i__xee_ab__ = NamedProperty()
            _i__xee_ab__.id = 0x811C
            _i__xee_ab__.guid = StandardPropertySet.TASK
            _i__xee_ab__.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _i__xee_ab__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_i__xee_ab__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            _x__mdz_____ = Property()
            _x__mdz_____.tag = __rud_dv_c_t
            _x__mdz_____.type = PropertyType.BOOLEAN
            _x__mdz_____.value = int.to_bytes(1,1,"little")
            _x__mdz_____.is_readable = True
            _x__mdz_____.is_writeable = True

            ______oh_ul_ += _x__mdz_____.to_bytes()
        

        if self.__bbqh_x____:
        
            __jp_z_y___y = NamedProperty()
            __jp_z_y___y.id = 0x8223
            __jp_z_y___y.guid = StandardPropertySet.APPOINTMENT
            __jp_z_y___y.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __jp_z_y___y)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__jp_z_y___y)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            lp____fv_iu_ = Property()
            lp____fv_iu_.tag = __rud_dv_c_t
            lp____fv_iu_.type = PropertyType.BOOLEAN
            lp____fv_iu_.value = int.to_bytes(1,1,"little")
            lp____fv_iu_.is_readable = True
            lp____fv_iu_.is_writeable = True

            ______oh_ul_ += lp____fv_iu_.to_bytes()
        

        if self._mr_j__yp__f:
        
            ____ejb_y___ = NamedProperty()
            ____ejb_y___.id = 0x8215
            ____ejb_y___.guid = StandardPropertySet.APPOINTMENT
            ____ejb_y___.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ____ejb_y___)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(____ejb_y___)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            __nprgk__i_c = Property()
            __nprgk__i_c.tag = __rud_dv_c_t
            __nprgk__i_c.type = PropertyType.BOOLEAN
            __nprgk__i_c.value = int.to_bytes(1,1,"little")
            __nprgk__i_c.is_readable = True
            __nprgk__i_c.is_writeable = True

            ______oh_ul_ += __nprgk__i_c.to_bytes()
        

        if self._ca___k_ub_x:
        
            kb_qe_ov__za = NamedProperty()
            kb_qe_ov__za.id = 0x8503
            kb_qe_ov__za.guid = StandardPropertySet.COMMON
            kb_qe_ov__za.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, kb_qe_ov__za)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(kb_qe_ov__za)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            ms_uh__rvzgb = Property()
            ms_uh__rvzgb.tag = __rud_dv_c_t
            ms_uh__rvzgb.type = PropertyType.BOOLEAN
            ms_uh__rvzgb.value = int.to_bytes(1,1,"little")
            ms_uh__rvzgb.is_readable = True
            ms_uh__rvzgb.is_writeable = True

            ______oh_ul_ += ms_uh__rvzgb.to_bytes()
        

        if self._______vx_ok > datetime.datetime(1901,1,1):
        
            _tyok__nptju = NamedProperty()
            _tyok__nptju.id = 0x8502
            _tyok__nptju.guid = StandardPropertySet.COMMON
            _tyok__nptju.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _tyok__nptju)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_tyok__nptju)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._______vx_ok - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            y_d___i_____ = Property()
            y_d___i_____.tag = __rud_dv_c_t
            y_d___i_____.type = PropertyType.TIME
            y_d___i_____.value = du___g__abr_
            y_d___i_____.is_readable = True
            y_d___i_____.is_writeable = True

            ______oh_ul_ += y_d___i_____.to_bytes()
        

        if self.__qhz__ecaho > 0:
        
            _n_kf____zne = NamedProperty()
            _n_kf____zne.id = 0x8501
            _n_kf____zne.guid = StandardPropertySet.COMMON
            _n_kf____zne.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _n_kf____zne)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_n_kf____zne)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            __a____mtal_ = Property()
            __a____mtal_.tag = __rud_dv_c_t
            __a____mtal_.type = PropertyType.INTEGER_32
            __a____mtal_.value = int.to_bytes(self.__qhz__ecaho, 4, "little")
            __a____mtal_.is_readable = True
            __a____mtal_.is_writeable = True

            ______oh_ul_ += __a____mtal_.to_bytes()
        

        if self.kn_va_____zr > datetime.datetime(1901,1,1):
        
            ___f______b_ = NamedProperty()
            ___f______b_.id = 0x8104
            ___f______b_.guid = StandardPropertySet.TASK
            ___f______b_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ___f______b_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(___f______b_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.kn_va_____zr - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            ______tu_xn_ = Property()
            ______tu_xn_.tag = __rud_dv_c_t
            ______tu_xn_.type = PropertyType.TIME
            ______tu_xn_.value = du___g__abr_
            ______tu_xn_.is_readable = True
            ______tu_xn_.is_writeable = True

            ______oh_ul_ += ______tu_xn_.to_bytes()
        

        if self.drg_hha_bdef > datetime.datetime(1901,1,1):
        
            gt_n__g_____ = NamedProperty()
            gt_n__g_____.id = 0x8105
            gt_n__g_____.guid = StandardPropertySet.TASK
            gt_n__g_____.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, gt_n__g_____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(gt_n__g_____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.drg_hha_bdef - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            tsfkn___b___ = Property()
            tsfkn___b___.tag = __rud_dv_c_t
            tsfkn___b___.type = PropertyType.TIME
            tsfkn___b___.value = du___g__abr_
            tsfkn___b___.is_readable = True
            tsfkn___b___.is_writeable = True

            ______oh_ul_ += tsfkn___b___.to_bytes()
        

        if self._il_______cr > datetime.datetime(1901,1,1):
        
            ____t____a_e = NamedProperty()
            ____t____a_e.id = 0x810F
            ____t____a_e.guid = StandardPropertySet.TASK
            ____t____a_e.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ____t____a_e)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(____t____a_e)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._il_______cr - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            c__zbvis_a__ = Property()
            c__zbvis_a__.tag = __rud_dv_c_t
            c__zbvis_a__.type = PropertyType.TIME
            c__zbvis_a__.value = du___g__abr_
            c__zbvis_a__.is_readable = True
            c__zbvis_a__.is_writeable = True

            ______oh_ul_ += c__zbvis_a__.to_bytes()
        

        if self.____ueit___l != TaskStatus.NONE:

            q_d__cm___xc = NamedProperty()
            q_d__cm___xc.id = 0x8101
            q_d__cm___xc.guid = StandardPropertySet.TASK
            q_d__cm___xc.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, q_d__cm___xc)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(q_d__cm___xc)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            ____y_cpvee_ = Property()
            ____y_cpvee_.tag = __rud_dv_c_t
            ____y_cpvee_.type = PropertyType.INTEGER_32
            ____y_cpvee_.value = int.to_bytes(EnumUtil.parse_task_status(self.____ueit___l), 4, "little")
            ____y_cpvee_.is_readable = True
            ____y_cpvee_.is_writeable = True

            ______oh_ul_ += ____y_cpvee_.to_bytes()
        

        if self.p__f_s_____t != TaskOwnership.NONE:
        
            co__li__pe_z = NamedProperty()
            co__li__pe_z.id = 0x8129
            co__li__pe_z.guid = StandardPropertySet.TASK
            co__li__pe_z.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, co__li__pe_z)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(co__li__pe_z)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            _______a_f_q = Property()
            _______a_f_q.tag = __rud_dv_c_t
            _______a_f_q.type = PropertyType.INTEGER_32
            _______a_f_q.value = int.to_bytes(EnumUtil.parse_task_ownership(self.p__f_s_____t), 4, "little")
            _______a_f_q.is_readable = True
            _______a_f_q.is_writeable = True

            ______oh_ul_ += _______a_f_q.to_bytes()
        

        if self._c__v___wqqb != TaskDelegationState.NONE:
        
            uzi_w_j___r_ = NamedProperty()
            uzi_w_j___r_.id = 0x812A
            uzi_w_j___r_.guid = StandardPropertySet.TASK
            uzi_w_j___r_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, uzi_w_j___r_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(uzi_w_j___r_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            __oja__qn__d = Property()
            __oja__qn__d.tag = __rud_dv_c_t
            __oja__qn__d.type = PropertyType.INTEGER_32
            __oja__qn__d.value = int.to_bytes(EnumUtil.parse_task_delegation_state(self._c__v___wqqb), 4, "little")
            __oja__qn__d.is_readable = True
            __oja__qn__d.is_writeable = True

            ______oh_ul_ += __oja__qn__d.to_bytes()
        

        if self.om_u__xna_q_ > 0:
        
            zyw______g_a = NamedProperty()
            zyw______g_a.id = 0x8B05
            zyw______g_a.guid = StandardPropertySet.NOTE
            zyw______g_a.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, zyw______g_a)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(zyw______g_a)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            _gc___n_w_m_ = Property()
            _gc___n_w_m_.tag = __rud_dv_c_t
            _gc___n_w_m_.type = PropertyType.INTEGER_32
            _gc___n_w_m_.value = int.to_bytes(self.om_u__xna_q_, 4, "little")
            _gc___n_w_m_.is_readable = True
            _gc___n_w_m_.is_writeable = True

            ______oh_ul_ += _gc___n_w_m_.to_bytes()
        

        if self.__no__s_vsl_ > 0:
        
            b_j_____zd__ = NamedProperty()
            b_j_____zd__.id = 0x8B04
            b_j_____zd__.guid = StandardPropertySet.NOTE
            b_j_____zd__.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, b_j_____zd__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(b_j_____zd__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            th__d___wc_w = Property()
            th__d___wc_w.tag = __rud_dv_c_t
            th__d___wc_w.type = PropertyType.INTEGER_32
            th__d___wc_w.value = int.to_bytes(self.__no__s_vsl_, 4, "little")
            th__d___wc_w.is_readable = True
            th__d___wc_w.is_writeable = True

            ______oh_ul_ += th__d___wc_w.to_bytes()
        

        if self.qi______kjo_ > 0:
        
            do_bsr_n__j_ = NamedProperty()
            do_bsr_n__j_.id = 0x8B03
            do_bsr_n__j_.guid = StandardPropertySet.NOTE
            do_bsr_n__j_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, do_bsr_n__j_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(do_bsr_n__j_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            ___b__k_____ = Property()
            ___b__k_____.tag = __rud_dv_c_t
            ___b__k_____.type = PropertyType.INTEGER_32
            ___b__k_____.value = int.to_bytes(self.qi______kjo_, 4, "little")
            ___b__k_____.is_readable = True
            ___b__k_____.is_writeable = True

            ______oh_ul_ += ___b__k_____.to_bytes()
        

        if self.g__tp___yb__ > 0:
        
            _nk_s__p_ipd = NamedProperty()
            _nk_s__p_ipd.id = 0x8B02
            _nk_s__p_ipd.guid = StandardPropertySet.NOTE
            _nk_s__p_ipd.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _nk_s__p_ipd)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_nk_s__p_ipd)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            _p_bbn_yc__j = Property()
            _p_bbn_yc__j.tag = __rud_dv_c_t
            _p_bbn_yc__j.type = PropertyType.INTEGER_32
            _p_bbn_yc__j.value = int.to_bytes(self.g__tp___yb__, 4, "little")
            _p_bbn_yc__j.is_readable = True
            _p_bbn_yc__j.is_writeable = True

            ______oh_ul_ += _p_bbn_yc__j.to_bytes()
        

        if self.j____bexpm__ != NoteColor.NONE:
        
            __ll________ = NamedProperty()
            __ll________.id = 0x8B00
            __ll________.guid = StandardPropertySet.NOTE
            __ll________.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __ll________)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__ll________)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            _oi_coj_____ = Property()
            _oi_coj_____.tag = __rud_dv_c_t
            _oi_coj_____.type = PropertyType.INTEGER_32
            _oi_coj_____.value = int.to_bytes(EnumUtil.parse_note_color(self.j____bexpm__), 4, "little")
            _oi_coj_____.is_readable = True
            _oi_coj_____.is_writeable = True

            ______oh_ul_ += _oi_coj_____.to_bytes()
        

        if self.__i_b_kq_iap > datetime.datetime(1901,1,1):
        
            __xe__c_p__j = NamedProperty()
            __xe__c_p__j.id = 0x8706
            __xe__c_p__j.guid = StandardPropertySet.JOURNAL
            __xe__c_p__j.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __xe__c_p__j)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__xe__c_p__j)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__i_b_kq_iap - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            f_______pq_b = Property()
            f_______pq_b.tag = __rud_dv_c_t
            f_______pq_b.type = PropertyType.TIME
            f_______pq_b.value = du___g__abr_
            f_______pq_b.is_readable = True
            f_______pq_b.is_writeable = True

            ______oh_ul_ += f_______pq_b.to_bytes()
        

        if self.rq__k____jkt > datetime.datetime(1901,1,1):
        
            ___yuc_____x = NamedProperty()
            ___yuc_____x.id = 0x8708
            ___yuc_____x.guid = StandardPropertySet.JOURNAL
            ___yuc_____x.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ___yuc_____x)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(___yuc_____x)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0040

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__v_r_____n_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            _________g__ = Property()
            _________g__.tag = __rud_dv_c_t
            _________g__.type = PropertyType.TIME
            _________g__.value = du___g__abr_
            _________g__.is_readable = True
            _________g__.is_writeable = True

            ______oh_ul_ += _________g__.to_bytes()
        

        if self._s______z_yx is not None:
        
            m_dve__ularo = NamedProperty()
            m_dve__ularo.id = 0x8700
            m_dve__ularo.guid = StandardPropertySet.JOURNAL
            m_dve__ularo.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, m_dve__ularo)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(m_dve__ularo)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            s_____bn_o_r = self._s______z_yx.encode(self.nsifr_q_er__)
            ___xqt_k_a_d = Stream("__substg1.0_" + o__n_l__j__v, s_____bn_o_r)
            ___xv_ab__p_.append(___xqt_k_a_d)

            d_____rb_b_n = Property()
            d_____rb_b_n.tag = __rud_dv_c_t
            d_____rb_b_n.type = PropertyType.STRING_8
            d_____rb_b_n.size = len(s_____bn_o_r) + x_m_sky_gz__
            d_____rb_b_n.is_readable = True
            d_____rb_b_n.is_writeable = True

            ______oh_ul_ += d_____rb_b_n.to_bytes()
        

        if self.va_uignshqy_ is not None:
        
            __q_______bo = NamedProperty()
            __q_______bo.id = 0x8712
            __q_______bo.guid = StandardPropertySet.JOURNAL
            __q_______bo.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __q_______bo)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__q_______bo)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ___hs__z___c = self.va_uignshqy_.encode(self.nsifr_q_er__)
            z____btvv_e_ = Stream("__substg1.0_" + o__n_l__j__v, ___hs__z___c)
            ___xv_ab__p_.append(z____btvv_e_)

            _s__n_______ = Property()
            _s__n_______.tag = __rud_dv_c_t
            _s__n_______.type = PropertyType.STRING_8
            _s__n_______.size = len(___hs__z___c) + x_m_sky_gz__
            _s__n_______.is_readable = True
            _s__n_______.is_writeable = True

            ______oh_ul_ += _s__n_______.to_bytes()
        

        if self._jnlqe_____v > 0:
        
            i___d_owx___ = NamedProperty()
            i___d_owx___.id = 0x8707
            i___d_owx___.guid = StandardPropertySet.JOURNAL
            i___d_owx___.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, i___d_owx___)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(i___d_owx___)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            butkxg__edxj = Property()
            butkxg__edxj.tag = __rud_dv_c_t
            butkxg__edxj.type = PropertyType.INTEGER_32
            butkxg__edxj.value = int.to_bytes(self._jnlqe_____v, 4, "little")
            butkxg__edxj.is_readable = True
            butkxg__edxj.is_writeable = True

            ______oh_ul_ += butkxg__edxj.to_bytes()
        

        if self.hsu__s____k_ > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.hsu__s____k_ - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            ______fuz_ii = Property()
            ______fuz_ii.tag = 0x3A420040
            ______fuz_ii.type = PropertyType.TIME
            ______fuz_ii.value = du___g__abr_
            ______fuz_ii.is_readable = True
            ______fuz_ii.is_writeable = False

            ______oh_ul_ += ______fuz_ii.to_bytes()
        

        if len(self._v__e__f____) > 0:
        
            yc___ir_it_r = bytearray()

            for i in range(len(self._v__e__f____)):
            
                z____yoec___ = (self._v__e__f____[i] + "\0").encode(self.nsifr_q_er__)
                w__ar_s__m__ = len(z____yoec___)
                zy______o___ = int.to_bytes(w__ar_s__m__, 4, "little")

                yc___ir_it_r += zy______o___

                _q__or_ip_dt = "__substg1.0_3A58" + self.h______id_ai + "-" + str.format("{:08X}", i)

                z_ig_vio_c__ = Stream(_q__or_ip_dt, z____yoec___)
                ___xv_ab__p_.append(z_ig_vio_c__)
            
            tc__d__h___b = bytes(yc___ir_it_r)

            _sjns__zv_k_ = Stream("__substg1.0_3A58" + self.h______id_ai, tc__d__h___b)
            ___xv_ab__p_.append(_sjns__zv_k_)

            _yhm____fo_x = Property()
            _yhm____fo_x.tag = 0x3A58 << 16 | self._wet__k__o__
            _yhm____fo_x.type = PropertyType.MULTIPLE_STRING_8
            _yhm____fo_x.size = len(tc__d__h___b)
            _yhm____fo_x.is_readable = True
            _yhm____fo_x.is_writeable = True

            ______oh_ul_ += _yhm____fo_x.to_bytes()
        

        if self.m__vg_n__ze_ is not None:
        
            _ib___she_y_ = self.m__vg_n__ze_.encode(self.nsifr_q_er__)
            __xi__v_noq_ = Stream("__substg1.0_3A30" + self.m__zli___l_b, _ib___she_y_)
            ___xv_ab__p_.append(__xi__v_noq_)

            fc__ko_____i = Property()
            fc__ko_____i.tag = 0x3A30 << 16 | self.wiqwtada__v_
            fc__ko_____i.type = PropertyType.STRING_8
            fc__ko_____i.size = len(_ib___she_y_) + x_m_sky_gz__
            fc__ko_____i.is_readable = True
            fc__ko_____i.is_writeable = True

            ______oh_ul_ += fc__ko_____i.to_bytes()
        

        if self.__x_____x__h is not None:
        
            _____mm____y = self.__x_____x__h.encode(self.nsifr_q_er__)
            _befxk_cdu__ = Stream("__substg1.0_3A2E" + self.m__zli___l_b, _____mm____y)
            ___xv_ab__p_.append(_befxk_cdu__)

            d__rtl_i__ot = Property()
            d__rtl_i__ot.tag = 0x3A2E << 16 | self.wiqwtada__v_
            d__rtl_i__ot.type = PropertyType.STRING_8
            d__rtl_i__ot.size = len(_____mm____y) + x_m_sky_gz__
            d__rtl_i__ot.is_readable = True
            d__rtl_i__ot.is_writeable = True

            ______oh_ul_ += d__rtl_i__ot.to_bytes()
        

        if self.t__w_nqk____ is not None:
        
            __rjjn_l_c_t = self.t__w_nqk____.encode(self.nsifr_q_er__)
            _c_a___o_n__ = Stream("__substg1.0_3A1B" + self.m__zli___l_b, __rjjn_l_c_t)
            ___xv_ab__p_.append(_c_a___o_n__)

            qjej__xn_y_k = Property()
            qjej__xn_y_k.tag = 0x3A1B << 16 | self.wiqwtada__v_
            qjej__xn_y_k.type = PropertyType.STRING_8
            qjej__xn_y_k.size = len(__rjjn_l_c_t) + x_m_sky_gz__
            qjej__xn_y_k.is_readable = True
            qjej__xn_y_k.is_writeable = True

            ______oh_ul_ += qjej__xn_y_k.to_bytes()
        

        if self.__rom_q__nzu is not None:
        
            n_r__cb___cl = self.__rom_q__nzu.encode(self.nsifr_q_er__)
            b___benu_c_i = Stream("__substg1.0_3A24" + self.m__zli___l_b, n_r__cb___cl)
            ___xv_ab__p_.append(b___benu_c_i)

            _ropr_kko_k_ = Property()
            _ropr_kko_k_.tag = 0x3A24 << 16 | self.wiqwtada__v_
            _ropr_kko_k_.type = PropertyType.STRING_8
            _ropr_kko_k_.size = len(n_r__cb___cl) + x_m_sky_gz__
            _ropr_kko_k_.is_readable = True
            _ropr_kko_k_.is_writeable = True

            ______oh_ul_ += _ropr_kko_k_.to_bytes()
        

        if self.h_a_x____w_j is not None:
        
            bwyy__d_am_t = self.h_a_x____w_j.encode(self.nsifr_q_er__)
            l__u___h_kx_ = Stream("__substg1.0_3A51" + self.m__zli___l_b, bwyy__d_am_t)
            ___xv_ab__p_.append(l__u___h_kx_)

            omtr_fhjr___ = Property()
            omtr_fhjr___.tag = 0x3A51 << 16 | self.wiqwtada__v_
            omtr_fhjr___.type = PropertyType.STRING_8
            omtr_fhjr___.size = len(bwyy__d_am_t) + x_m_sky_gz__
            omtr_fhjr___.is_readable = True
            omtr_fhjr___.is_writeable = True

            ______oh_ul_ += omtr_fhjr___.to_bytes()
        

        if self.ul_l_qtt___p is not None:
        
            j____qbwq__b = self.ul_l_qtt___p.encode(self.nsifr_q_er__)
            g__yh_a__f_u = Stream("__substg1.0_3A02" + self.m__zli___l_b, j____qbwq__b)
            ___xv_ab__p_.append(g__yh_a__f_u)

            ja_l_c___mz_ = Property()
            ja_l_c___mz_.tag = 0x3A02 << 16 | self.wiqwtada__v_
            ja_l_c___mz_.type = PropertyType.STRING_8
            ja_l_c___mz_.size = len(j____qbwq__b) + x_m_sky_gz__
            ja_l_c___mz_.is_readable = True
            ja_l_c___mz_.is_writeable = True

            ______oh_ul_ += ja_l_c___mz_.to_bytes()
        

        if self.__m__tcaw___ is not None:
        
            __v___oi_p__ = self.__m__tcaw___.encode(self.nsifr_q_er__)
            ___ka___kt_d = Stream("__substg1.0_3A1E" + self.m__zli___l_b, __v___oi_p__)
            ___xv_ab__p_.append(___ka___kt_d)

            _g__gkokq___ = Property()
            _g__gkokq___.tag = 0x3A1E << 16 | self.wiqwtada__v_
            _g__gkokq___.type = PropertyType.STRING_8
            _g__gkokq___.size = len(__v___oi_p__) + x_m_sky_gz__
            _g__gkokq___.is_readable = True
            _g__gkokq___.is_writeable = True

            ______oh_ul_ += _g__gkokq___.to_bytes()
        

        if self.owjw_l_is_fs is not None:
        
            tq___k______ = self.owjw_l_is_fs.encode(self.nsifr_q_er__)
            orv___v_glnz = Stream("__substg1.0_3A1C" + self.m__zli___l_b, tq___k______)
            ___xv_ab__p_.append(orv___v_glnz)

            t_sp_o___y__ = Property()
            t_sp_o___y__.tag = 0x3A1C << 16 | self.wiqwtada__v_
            t_sp_o___y__.type = PropertyType.STRING_8
            t_sp_o___y__.size = len(tq___k______) + x_m_sky_gz__
            t_sp_o___y__.is_readable = True
            t_sp_o___y__.is_writeable = True

            ______oh_ul_ += t_sp_o___y__.to_bytes()
        

        if self.____v__n___r is not None:
        
            ________e__u = self.____v__n___r.encode(self.nsifr_q_er__)
            _a__iv___b__ = Stream("__substg1.0_3A57" + self.m__zli___l_b, ________e__u)
            ___xv_ab__p_.append(_a__iv___b__)

            c__a____gbv_ = Property()
            c__a____gbv_.tag = 0x3A57 << 16 | self.wiqwtada__v_
            c__a____gbv_.type = PropertyType.STRING_8
            c__a____gbv_.size = len(________e__u) + x_m_sky_gz__
            c__a____gbv_.is_readable = True
            c__a____gbv_.is_writeable = True

            ______oh_ul_ += c__a____gbv_.to_bytes()
        

        if self.e_s_i__m____ is not None:
        
            _g__tylfp___ = self.e_s_i__m____.encode(self.nsifr_q_er__)
            v__iu__ntg__ = Stream("__substg1.0_3A16" + self.m__zli___l_b, _g__tylfp___)
            ___xv_ab__p_.append(v__iu__ntg__)

            _pfui_qnzn_f = Property()
            _pfui_qnzn_f.tag = 0x3A16 << 16 | self.wiqwtada__v_
            _pfui_qnzn_f.type = PropertyType.STRING_8
            _pfui_qnzn_f.size = len(_g__tylfp___) + x_m_sky_gz__
            _pfui_qnzn_f.is_readable = True
            _pfui_qnzn_f.is_writeable = True

            ______oh_ul_ += _pfui_qnzn_f.to_bytes()
        

        if self.______rz___k is not None:
        
            iv___u_cm___ = self.______rz___k.encode(self.nsifr_q_er__)
            __f__ydi_e_i = Stream("__substg1.0_3A49" + self.m__zli___l_b, iv___u_cm___)
            ___xv_ab__p_.append(__f__ydi_e_i)

            ___n_a_fiicy = Property()
            ___n_a_fiicy.tag = 0x3A49 << 16 | self.wiqwtada__v_
            ___n_a_fiicy.type = PropertyType.STRING_8
            ___n_a_fiicy.size = len(iv___u_cm___) + x_m_sky_gz__
            ___n_a_fiicy.is_readable = True
            ___n_a_fiicy.is_writeable = True

            ______oh_ul_ += ___n_a_fiicy.to_bytes()
        

        if self.ks___x_ef_l_ is not None:
        
            sfq_ln_z___v = NamedProperty()
            sfq_ln_z___v.id = 0x8049
            sfq_ln_z___v.guid = StandardPropertySet.ADDRESS
            sfq_ln_z___v.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, sfq_ln_z___v)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(sfq_ln_z___v)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            t_wpoe_f___u = self.ks___x_ef_l_.encode(self.nsifr_q_er__)

            m_m_kbc____j = Stream("__substg1.0_" + o__n_l__j__v, t_wpoe_f___u)
            ___xv_ab__p_.append(m_m_kbc____j)

            y_b_y_c_an_r = Property()
            y_b_y_c_an_r.tag = __rud_dv_c_t
            y_b_y_c_an_r.type = PropertyType.STRING_8
            y_b_y_c_an_r.size = len(t_wpoe_f___u) + x_m_sky_gz__
            y_b_y_c_an_r.is_readable = True
            y_b_y_c_an_r.is_writeable = True

            ______oh_ul_ += y_b_y_c_an_r.to_bytes()

            _qb___qksvsz = Stream("__substg1.0_3A26" + self.m__zli___l_b, t_wpoe_f___u)
            ___xv_ab__p_.append(_qb___qksvsz)

            ___j_zippz__ = Property()
            ___j_zippz__.tag = 0x3A26 << 16 | self.wiqwtada__v_
            ___j_zippz__.type = PropertyType.STRING_8
            ___j_zippz__.size = len(t_wpoe_f___u) + x_m_sky_gz__
            ___j_zippz__.is_readable = True
            ___j_zippz__.is_writeable = True

            ______oh_ul_ += ___j_zippz__.to_bytes()
        

        if self._____li__w__ is not None:
        
            q__tbj_i__q_ = self._____li__w__.encode(self.nsifr_q_er__)
            _df___a_d___ = Stream("__substg1.0_3A4A" + self.m__zli___l_b, q__tbj_i__q_)
            ___xv_ab__p_.append(_df___a_d___)

            gt_____k_f__ = Property()
            gt_____k_f__.tag = 0x3A4A << 16 | self.wiqwtada__v_
            gt_____k_f__.type = PropertyType.STRING_8
            gt_____k_f__.size = len(q__tbj_i__q_) + x_m_sky_gz__
            gt_____k_f__.is_readable = True
            gt_____k_f__.is_writeable = True

            ______oh_ul_ += gt_____k_f__.to_bytes()
        

        if self.hgsi_u__j__v is not None:
        
            ____n______z = self.hgsi_u__j__v.encode(self.nsifr_q_er__)
            q__z___fpep_ = Stream("__substg1.0_3A18" + self.m__zli___l_b, ____n______z)
            ___xv_ab__p_.append(q__z___fpep_)

            n_z_a_r_qw_o = Property()
            n_z_a_r_qw_o.tag = 0x3A18 << 16 | self.wiqwtada__v_
            n_z_a_r_qw_o.type = PropertyType.STRING_8
            n_z_a_r_qw_o.size = len(____n______z) + x_m_sky_gz__
            n_z_a_r_qw_o.is_readable = True
            n_z_a_r_qw_o.is_writeable = True

            ______oh_ul_ += n_z_a_r_qw_o.to_bytes()
        

        if self.__j___op_s__ is not None:
        
            __wb____mxat = self.__j___op_s__.encode(self.nsifr_q_er__)
            au___tv___a_ = Stream("__substg1.0_3001" + self.m__zli___l_b, __wb____mxat)
            ___xv_ab__p_.append(au___tv___a_)

            nb__opljqv__ = Property()
            nb__opljqv__.tag = 0x3001 << 16 | self.wiqwtada__v_
            nb__opljqv__.type = PropertyType.STRING_8
            nb__opljqv__.size = len(__wb____mxat) + x_m_sky_gz__
            nb__opljqv__.is_readable = True
            nb__opljqv__.is_writeable = True

            ______oh_ul_ += nb__opljqv__.to_bytes()
        

        if self._pudmbn_y_qy is not None:
        
            ___h__qs___j = self._pudmbn_y_qy.encode(self.nsifr_q_er__)
            wkd_s___s___ = Stream("__substg1.0_3A45" + self.m__zli___l_b, ___h__qs___j)
            ___xv_ab__p_.append(wkd_s___s___)

            l___ai___o__ = Property()
            l___ai___o__.tag = 0x3A45 << 16 | self.wiqwtada__v_
            l___ai___o__.type = PropertyType.STRING_8
            l___ai___o__.size = len(___h__qs___j) + x_m_sky_gz__
            l___ai___o__.is_readable = True
            l___ai___o__.is_writeable = True

            ______oh_ul_ += l___ai___o__.to_bytes()
        

        if self._x_b_d_u__hg is not None:
        
            ___t__riqc_u = self._x_b_d_u__hg.encode(self.nsifr_q_er__)
            _d__o_ngk__w = Stream("__substg1.0_3A4C" + self.m__zli___l_b, ___t__riqc_u)
            ___xv_ab__p_.append(_d__o_ngk__w)

            _____n_s__a_ = Property()
            _____n_s__a_.tag = 0x3A4C << 16 | self.wiqwtada__v_
            _____n_s__a_.type = PropertyType.STRING_8
            _____n_s__a_.size = len(___t__riqc_u) + x_m_sky_gz__
            _____n_s__a_.is_readable = True
            _____n_s__a_.is_writeable = True

            ______oh_ul_ += _____n_s__a_.to_bytes()
        

        if self.gd_n__q___qg is not None:
        
            _t___x__rp_b = self.gd_n__q___qg.encode(self.nsifr_q_er__)
            f_nv_v___ek_ = Stream("__substg1.0_3A05" + self.m__zli___l_b, _t___x__rp_b)
            ___xv_ab__p_.append(f_nv_v___ek_)

            l_c_u___a__m = Property()
            l_c_u___a__m.tag = 0x3A05 << 16 | self.wiqwtada__v_
            l_c_u___a__m.type = PropertyType.STRING_8
            l_c_u___a__m.size = len(_t___x__rp_b) + x_m_sky_gz__
            l_c_u___a__m.is_readable = True
            l_c_u___a__m.is_writeable = True

            ______oh_ul_ += l_c_u___a__m.to_bytes()
        

        if self._ks__k_____f is not None:
        
            ___t__cdgjm_ = self._ks__k_____f.encode(self.nsifr_q_er__)
            __g___orinth = Stream("__substg1.0_3A06" + self.m__zli___l_b, ___t__cdgjm_)
            ___xv_ab__p_.append(__g___orinth)

            _nwv_p___es_ = Property()
            _nwv_p___es_.tag = 0x3A06 << 16 | self.wiqwtada__v_
            _nwv_p___es_.type = PropertyType.STRING_8
            _nwv_p___es_.size = len(___t__cdgjm_) + x_m_sky_gz__
            _nwv_p___es_.is_readable = True
            _nwv_p___es_.is_writeable = True

            ______oh_ul_ += _nwv_p___es_.to_bytes()
        

        if self.tb_____r_t__ is not None:
        
            __mt__eya_ms = self.tb_____r_t__.encode(self.nsifr_q_er__)
            az___mp____e = Stream("__substg1.0_3A07" + self.m__zli___l_b, __mt__eya_ms)
            ___xv_ab__p_.append(az___mp____e)

            __xz___pvnj_ = Property()
            __xz___pvnj_.tag = 0x3A07 << 16 | self.wiqwtada__v_
            __xz___pvnj_.type = PropertyType.STRING_8
            __xz___pvnj_.size = len(__mt__eya_ms) + x_m_sky_gz__
            __xz___pvnj_.is_readable = True
            __xz___pvnj_.is_writeable = True

            ______oh_ul_ += __xz___pvnj_.to_bytes()
        

        if self.________zntw is not None:
        
            l_x_eftg_age = self.________zntw.encode(self.nsifr_q_er__)
            s__i__uf___b = Stream("__substg1.0_3A43" + self.m__zli___l_b, l_x_eftg_age)
            ___xv_ab__p_.append(s__i__uf___b)

            q__hc__nsnsx = Property()
            q__hc__nsnsx.tag = 0x3A43 << 16 | self.wiqwtada__v_
            q__hc__nsnsx.type = PropertyType.STRING_8
            q__hc__nsnsx.size = len(l_x_eftg_age) + x_m_sky_gz__
            q__hc__nsnsx.is_readable = True
            q__hc__nsnsx.is_writeable = True

            ______oh_ul_ += q__hc__nsnsx.to_bytes()
        

        if self.__rvw_yhfi_g is not None:
        
            rxpqk___p___ = self.__rvw_yhfi_g.encode(self.nsifr_q_er__)
            _______s__yn = Stream("__substg1.0_3A2F" + self.m__zli___l_b, rxpqk___p___)
            ___xv_ab__p_.append(_______s__yn)

            __ta__nwq___ = Property()
            __ta__nwq___.tag = 0x3A2F << 16 | self.wiqwtada__v_
            __ta__nwq___.type = PropertyType.STRING_8
            __ta__nwq___.size = len(rxpqk___p___) + x_m_sky_gz__
            __ta__nwq___.is_readable = True
            __ta__nwq___.is_writeable = True

            ______oh_ul_ += __ta__nwq___.to_bytes()
        

        if self.__y_____aw__ is not None:
        
            k___ap_qy_td = self.__y_____aw__.encode(self.nsifr_q_er__)
            wti_g_poh___ = Stream("__substg1.0_3A59" + self.m__zli___l_b, k___ap_qy_td)
            ___xv_ab__p_.append(wti_g_poh___)

            vg_p_c_k____ = Property()
            vg_p_c_k____.tag = 0x3A59 << 16 | self.wiqwtada__v_
            vg_p_c_k____.type = PropertyType.STRING_8
            vg_p_c_k____.size = len(k___ap_qy_td) + x_m_sky_gz__
            vg_p_c_k____.is_readable = True
            vg_p_c_k____.is_writeable = True

            ______oh_ul_ += vg_p_c_k____.to_bytes()
        

        if self._____lc_g_h_ is not None:
        
            __s_dq__g___ = self._____lc_g_h_.encode(self.nsifr_q_er__)
            _fh___w_l_oa = Stream("__substg1.0_3A5A" + self.m__zli___l_b, __s_dq__g___)
            ___xv_ab__p_.append(_fh___w_l_oa)

            ___x_xf_avw_ = Property()
            ___x_xf_avw_.tag = 0x3A5A << 16 | self.wiqwtada__v_
            ___x_xf_avw_.type = PropertyType.STRING_8
            ___x_xf_avw_.size = len(__s_dq__g___) + x_m_sky_gz__
            ___x_xf_avw_.is_readable = True
            ___x_xf_avw_.is_writeable = True

            ______oh_ul_ += ___x_xf_avw_.to_bytes()
        

        if self.d__ol_f_a_i_ is not None:
        
            xw__x_vw____ = self.d__ol_f_a_i_.encode(self.nsifr_q_er__)
            _w_x__urdpkp = Stream("__substg1.0_3A5B" + self.m__zli___l_b, xw__x_vw____)
            ___xv_ab__p_.append(_w_x__urdpkp)

            _e_d__b__l__ = Property()
            _e_d__b__l__.tag = 0x3A5B << 16 | self.wiqwtada__v_
            _e_d__b__l__.type = PropertyType.STRING_8
            _e_d__b__l__.size = len(xw__x_vw____) + x_m_sky_gz__
            _e_d__b__l__.is_readable = True
            _e_d__b__l__.is_writeable = True

            ______oh_ul_ += _e_d__b__l__.to_bytes()
        

        if self.__xc__e_i___ is not None:
        
            v_m_mu__j_a_ = self.__xc__e_i___.encode(self.nsifr_q_er__)
            sy_______vxo = Stream("__substg1.0_3A5E" + self.m__zli___l_b, v_m_mu__j_a_)
            ___xv_ab__p_.append(sy_______vxo)

            xhd__j__i_ts = Property()
            xhd__j__i_ts.tag = 0x3A5E << 16 | self.wiqwtada__v_
            xhd__j__i_ts.type = PropertyType.STRING_8
            xhd__j__i_ts.size = len(v_m_mu__j_a_) + x_m_sky_gz__
            xhd__j__i_ts.is_readable = True
            xhd__j__i_ts.is_writeable = True

            ______oh_ul_ += xhd__j__i_ts.to_bytes()
        

        if self.v_s____jaf__ is not None:
        
            _ylx____l__g = self.v_s____jaf__.encode(self.nsifr_q_er__)
            __m_r__ic___ = Stream("__substg1.0_3A5C" + self.m__zli___l_b, _ylx____l__g)
            ___xv_ab__p_.append(__m_r__ic___)

            ott__r_yi___ = Property()
            ott__r_yi___.tag = 0x3A5C << 16 | self.wiqwtada__v_
            ott__r_yi___.type = PropertyType.STRING_8
            ott__r_yi___.size = len(_ylx____l__g) + x_m_sky_gz__
            ott__r_yi___.is_readable = True
            ott__r_yi___.is_writeable = True

            ______oh_ul_ += ott__r_yi___.to_bytes()
        

        if self.___h_r__f_d_ is not None:
        
            _____u_ct_d_ = self.___h_r__f_d_.encode(self.nsifr_q_er__)
            w_h_dc___n_v = Stream("__substg1.0_3A5D" + self.m__zli___l_b, _____u_ct_d_)
            ___xv_ab__p_.append(w_h_dc___n_v)

            i___g__m_i__ = Property()
            i___g__m_i__.tag = 0x3A5D << 16 | self.wiqwtada__v_
            i___g__m_i__.type = PropertyType.STRING_8
            i___g__m_i__.size = len(_____u_ct_d_) + x_m_sky_gz__
            i___g__m_i__.is_readable = True
            i___g__m_i__.is_writeable = True

            ______oh_ul_ += i___g__m_i__.to_bytes()
        

        if self.w___u___r_fm is not None:
        
            _ot__slb__ou = self.w___u___r_fm.encode(self.nsifr_q_er__)
            c_n__l___w__ = Stream("__substg1.0_3A25" + self.m__zli___l_b, _ot__slb__ou)
            ___xv_ab__p_.append(c_n__l___w__)

            _j_lewj___ix = Property()
            _j_lewj___ix.tag = 0x3A25 << 16 | self.wiqwtada__v_
            _j_lewj___ix.type = PropertyType.STRING_8
            _j_lewj___ix.size = len(_ot__slb__ou) + x_m_sky_gz__
            _j_lewj___ix.is_readable = True
            _j_lewj___ix.is_writeable = True

            ______oh_ul_ += _j_lewj___ix.to_bytes()
        

        if self.v__pel_bkku_ is not None:
        
            ___z______e_ = self.v__pel_bkku_.encode(self.nsifr_q_er__)
            ____nkyq__wf = Stream("__substg1.0_3A09" + self.m__zli___l_b, ___z______e_)
            ___xv_ab__p_.append(____nkyq__wf)

            ____vs__fre_ = Property()
            ____vs__fre_.tag = 0x3A09 << 16 | self.wiqwtada__v_
            ____vs__fre_.type = PropertyType.STRING_8
            ____vs__fre_.size = len(___z______e_) + x_m_sky_gz__
            ____vs__fre_.is_readable = True
            ____vs__fre_.is_writeable = True

            ______oh_ul_ += ____vs__fre_.to_bytes()
        

        if self.____s_a_ddga is not None:
        
            v_p_aivx___h = self.____s_a_ddga.encode(self.nsifr_q_er__)
            ______v_k__g = Stream("__substg1.0_3A0A" + self.m__zli___l_b, v_p_aivx___h)
            ___xv_ab__p_.append(______v_k__g)

            kf_xo_i___xm = Property()
            kf_xo_i___xm.tag = 0x3A0A << 16 | self.wiqwtada__v_
            kf_xo_i___xm.type = PropertyType.STRING_8
            kf_xo_i___xm.size = len(v_p_aivx___h) + x_m_sky_gz__
            kf_xo_i___xm.is_readable = True
            kf_xo_i___xm.is_writeable = True

            ______oh_ul_ += kf_xo_i___xm.to_bytes()
        

        if self._k__dsw_fx_j is not None:
        
            _ezs___zyo__ = self._k__dsw_fx_j.encode(self.nsifr_q_er__)
            i_____q___kv = Stream("__substg1.0_3A2D" + self.m__zli___l_b, _ezs___zyo__)
            ___xv_ab__p_.append(i_____q___kv)

            _p_ufe__ioza = Property()
            _p_ufe__ioza.tag = 0x3A2D << 16 | self.wiqwtada__v_
            _p_ufe__ioza.type = PropertyType.STRING_8
            _p_ufe__ioza.size = len(_ezs___zyo__) + x_m_sky_gz__
            _p_ufe__ioza.is_readable = True
            _p_ufe__ioza.is_writeable = True

            ______oh_ul_ += _p_ufe__ioza.to_bytes()
        

        if self.g_k_____pg__ is not None:
        
            _qb_wi_z____ = NamedProperty()
            _qb_wi_z____.id = 0x8046
            _qb_wi_z____.guid = StandardPropertySet.ADDRESS
            _qb_wi_z____.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _qb_wi_z____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_qb_wi_z____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ab__ba_yq_z_ = self.g_k_____pg__.encode(self.nsifr_q_er__)

            jgb_sd_j__m_ = Stream("__substg1.0_" + o__n_l__j__v, ab__ba_yq_z_)
            ___xv_ab__p_.append(jgb_sd_j__m_)

            w_yg_____k_x = Property()
            w_yg_____k_x.tag = __rud_dv_c_t
            w_yg_____k_x.type = PropertyType.STRING_8
            w_yg_____k_x.size = len(ab__ba_yq_z_) + x_m_sky_gz__
            w_yg_____k_x.is_readable = True
            w_yg_____k_x.is_writeable = True

            ______oh_ul_ += w_yg_____k_x.to_bytes()

            _fe_u_____q_ = Stream("__substg1.0_3A27" + self.m__zli___l_b, ab__ba_yq_z_)
            ___xv_ab__p_.append(_fe_u_____q_)

            _n_vuwq_z_wp = Property()
            _n_vuwq_z_wp.tag = 0x3A27 << 16 | self.wiqwtada__v_
            _n_vuwq_z_wp.type = PropertyType.STRING_8
            _n_vuwq_z_wp.size = len(ab__ba_yq_z_) + x_m_sky_gz__
            _n_vuwq_z_wp.is_readable = True
            _n_vuwq_z_wp.is_writeable = True

            ______oh_ul_ += _n_vuwq_z_wp.to_bytes()
        

        if self._h_sxo__l_h_ is not None:
        
            _wcyux_wu___ = self._h_sxo__l_h_.encode(self.nsifr_q_er__)
            _g_td__m___t = Stream("__substg1.0_3A4E" + self.m__zli___l_b, _wcyux_wu___)
            ___xv_ab__p_.append(_g_td__m___t)

            o_wj____z___ = Property()
            o_wj____z___.tag = 0x3A4E << 16 | self.wiqwtada__v_
            o_wj____z___.type = PropertyType.STRING_8
            o_wj____z___.size = len(_wcyux_wu___) + x_m_sky_gz__
            o_wj____z___.is_readable = True
            o_wj____z___.is_writeable = True

            ______oh_ul_ += o_wj____z___.to_bytes()
        

        if self.fxo_h_yp____ is not None:
        
            _________gq_ = self.fxo_h_yp____.encode(self.nsifr_q_er__)
            pttvre_i__fr = Stream("__substg1.0_3A44" + self.m__zli___l_b, _________gq_)
            ___xv_ab__p_.append(pttvre_i__fr)

            _x__dq_c_c_c = Property()
            _x__dq_c_c_c.tag = 0x3A44 << 16 | self.wiqwtada__v_
            _x__dq_c_c_c.type = PropertyType.STRING_8
            _x__dq_c_c_c.size = len(_________gq_) + x_m_sky_gz__
            _x__dq_c_c_c.is_readable = True
            _x__dq_c_c_c.is_writeable = True

            ______oh_ul_ += _x__dq_c_c_c.to_bytes()
        

        if self.r_____xd__nn is not None:
        
            q__m____r_t_ = self.r_____xd__nn.encode(self.nsifr_q_er__)
            _dp_ay_sk___ = Stream("__substg1.0_3A4F" + self.m__zli___l_b, q__m____r_t_)
            ___xv_ab__p_.append(_dp_ay_sk___)

            v__pkn_fd_s_ = Property()
            v__pkn_fd_s_.tag = 0x3A4F << 16 | self.wiqwtada__v_
            v__pkn_fd_s_.type = PropertyType.STRING_8
            v__pkn_fd_s_.size = len(q__m____r_t_) + x_m_sky_gz__
            v__pkn_fd_s_.is_readable = True
            v__pkn_fd_s_.is_writeable = True

            ______oh_ul_ += v__pkn_fd_s_.to_bytes()
        

        if self.xh_n_w_ab_q_ is not None:
        
            k_js_f__h_k_ = self.xh_n_w_ab_q_.encode(self.nsifr_q_er__)
            _vjpbarm_nk_ = Stream("__substg1.0_3A19" + self.m__zli___l_b, k_js_f__h_k_)
            ___xv_ab__p_.append(_vjpbarm_nk_)

            i_ru_h_vonr_ = Property()
            i_ru_h_vonr_.tag = 0x3A19 << 16 | self.wiqwtada__v_
            i_ru_h_vonr_.type = PropertyType.STRING_8
            i_ru_h_vonr_.size = len(k_js_f__h_k_) + x_m_sky_gz__
            i_ru_h_vonr_.is_readable = True
            i_ru_h_vonr_.is_writeable = True

            ______oh_ul_ += i_ru_h_vonr_.to_bytes()
        

        if self.h_w_j_lt_u_n is not None:
        
            c_imr_______ = self.h_w_j_lt_u_n.encode(self.nsifr_q_er__)
            _____p_wg_aj = Stream("__substg1.0_3A08" + self.m__zli___l_b, c_imr_______)
            ___xv_ab__p_.append(_____p_wg_aj)

            _oplp_emn___ = Property()
            _oplp_emn___.tag = 0x3A08 << 16 | self.wiqwtada__v_
            _oplp_emn___.type = PropertyType.STRING_8
            _oplp_emn___.size = len(c_imr_______) + x_m_sky_gz__
            _oplp_emn___.is_readable = True
            _oplp_emn___.is_writeable = True

            ______oh_ul_ += _oplp_emn___.to_bytes()
        

        if self.p___p__ch_nr is not None:
        
            k___dg_ev_m_ = self.p___p__ch_nr.encode(self.nsifr_q_er__)
            _____q_uk_ec = Stream("__substg1.0_3A5F" + self.m__zli___l_b, k___dg_ev_m_)
            ___xv_ab__p_.append(_____q_uk_ec)

            d_n_d_k_we_e = Property()
            d_n_d_k_we_e.tag = 0x3A5F << 16 | self.wiqwtada__v_
            d_n_d_k_we_e.type = PropertyType.STRING_8
            d_n_d_k_we_e.size = len(k___dg_ev_m_) + x_m_sky_gz__
            d_n_d_k_we_e.is_readable = True
            d_n_d_k_we_e.is_writeable = True

            ______oh_ul_ += d_n_d_k_we_e.to_bytes()
        

        if self.x__za__bvxv_ is not None:
        
            _lys__j_orzd = self.x__za__bvxv_.encode(self.nsifr_q_er__)
            ___egn____j_ = Stream("__substg1.0_3A60" + self.m__zli___l_b, _lys__j_orzd)
            ___xv_ab__p_.append(___egn____j_)

            __rgrg___ug_ = Property()
            __rgrg___ug_.tag = 0x3A60 << 16 | self.wiqwtada__v_
            __rgrg___ug_.type = PropertyType.STRING_8
            __rgrg___ug_.size = len(_lys__j_orzd) + x_m_sky_gz__
            __rgrg___ug_.is_readable = True
            __rgrg___ug_.is_writeable = True

            ______oh_ul_ += __rgrg___ug_.to_bytes()
        

        if self.b___w_g__t__ is not None:
        
            eomveyng___i = self.b___w_g__t__.encode(self.nsifr_q_er__)
            n_r_g_om__it = Stream("__substg1.0_3A61" + self.m__zli___l_b, eomveyng___i)
            ___xv_ab__p_.append(n_r_g_om__it)

            _cj_fz__c_p_ = Property()
            _cj_fz__c_p_.tag = 0x3A61 << 16 | self.wiqwtada__v_
            _cj_fz__c_p_.type = PropertyType.STRING_8
            _cj_fz__c_p_.size = len(eomveyng___i) + x_m_sky_gz__
            _cj_fz__c_p_.is_readable = True
            _cj_fz__c_p_.is_writeable = True

            ______oh_ul_ += _cj_fz__c_p_.to_bytes()
        

        if self._n___kc___xe is not None:
        
            _kmjf_z__i__ = self._n___kc___xe.encode(self.nsifr_q_er__)
            ___xb_d__u__ = Stream("__substg1.0_3A62" + self.m__zli___l_b, _kmjf_z__i__)
            ___xv_ab__p_.append(___xb_d__u__)

            ___j____hn__ = Property()
            ___j____hn__.tag = 0x3A62 << 16 | self.wiqwtada__v_
            ___j____hn__.type = PropertyType.STRING_8
            ___j____hn__.size = len(_kmjf_z__i__) + x_m_sky_gz__
            ___j____hn__.is_readable = True
            ___j____hn__.is_writeable = True

            ______oh_ul_ += ___j____hn__.to_bytes()
        

        if self.t___m_b___qg is not None:
        
            hq_tmr_e____ = self.t___m_b___qg.encode(self.nsifr_q_er__)
            h___x_pl_ey_ = Stream("__substg1.0_3A63" + self.m__zli___l_b, hq_tmr_e____)
            ___xv_ab__p_.append(h___x_pl_ey_)

            vghl_e_g_rnj = Property()
            vghl_e_g_rnj.tag = 0x3A63 << 16 | self.wiqwtada__v_
            vghl_e_g_rnj.type = PropertyType.STRING_8
            vghl_e_g_rnj.size = len(hq_tmr_e____) + x_m_sky_gz__
            vghl_e_g_rnj.is_readable = True
            vghl_e_g_rnj.is_writeable = True

            ______oh_ul_ += vghl_e_g_rnj.to_bytes()
        

        if self.o___h_f_ey_j is not None:
        
            _nz___rh_n__ = self.o___h_f_ey_j.encode(self.nsifr_q_er__)
            ptyh_q__um__ = Stream("__substg1.0_3A1F" + self.m__zli___l_b, _nz___rh_n__)
            ___xv_ab__p_.append(ptyh_q__um__)

            _zw____qs_y_ = Property()
            _zw____qs_y_.tag = 0x3A1F << 16 | self.wiqwtada__v_
            _zw____qs_y_.type = PropertyType.STRING_8
            _zw____qs_y_.size = len(_nz___rh_n__) + x_m_sky_gz__
            _zw____qs_y_.is_readable = True
            _zw____qs_y_.is_writeable = True

            ______oh_ul_ += _zw____qs_y_.to_bytes()
        

        if self.w_qf___ld___ is not None:
        
            ___p__x____o = self.w_qf___ld___.encode(self.nsifr_q_er__)
            k_c_u__uu__d = Stream("__substg1.0_3A21" + self.m__zli___l_b, ___p__x____o)
            ___xv_ab__p_.append(k_c_u__uu__d)

            a_aziu__bp__ = Property()
            a_aziu__bp__.tag = 0x3A21 << 16 | self.wiqwtada__v_
            a_aziu__bp__.type = PropertyType.STRING_8
            a_aziu__bp__.size = len(___p__x____o) + x_m_sky_gz__
            a_aziu__bp__.is_readable = True
            a_aziu__bp__.is_writeable = True

            ______oh_ul_ += a_aziu__bp__.to_bytes()
        

        if self.__v_cyc_____ is not None:
        
            ___lo__k_p__ = self.__v_cyc_____.encode(self.nsifr_q_er__)
            yp_pb_q____a = Stream("__substg1.0_3A50" + self.m__zli___l_b, ___lo__k_p__)
            ___xv_ab__p_.append(yp_pb_q____a)

            _gvbw__hl_wo = Property()
            _gvbw__hl_wo.tag = 0x3A50 << 16 | self.wiqwtada__v_
            _gvbw__hl_wo.type = PropertyType.STRING_8
            _gvbw__hl_wo.size = len(___lo__k_p__) + x_m_sky_gz__
            _gvbw__hl_wo.is_readable = True
            _gvbw__hl_wo.is_writeable = True

            ______oh_ul_ += _gvbw__hl_wo.to_bytes()
        

        if self.h__l____bnit is not None:
        
            h____v_g_mv_ = self.h__l____bnit.encode(self.nsifr_q_er__)
            _kvxht___gc_ = Stream("__substg1.0_3A15" + self.m__zli___l_b, h____v_g_mv_)
            ___xv_ab__p_.append(_kvxht___gc_)

            k__qmwi_m__y = Property()
            k__qmwi_m__y.tag = 0x3A15 << 16 | self.wiqwtada__v_
            k__qmwi_m__y.type = PropertyType.STRING_8
            k__qmwi_m__y.size = len(h____v_g_mv_) + x_m_sky_gz__
            k__qmwi_m__y.is_readable = True
            k__qmwi_m__y.is_writeable = True

            ______oh_ul_ += k__qmwi_m__y.to_bytes()
        

        if self.___c_d_i__l_ is not None:
        
            _vjuuo_k_qp_ = NamedProperty()
            _vjuuo_k_qp_.id = 0x8048
            _vjuuo_k_qp_.guid = StandardPropertySet.ADDRESS
            _vjuuo_k_qp_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _vjuuo_k_qp_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_vjuuo_k_qp_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _u_y_n___q_y = self.___c_d_i__l_.encode(self.nsifr_q_er__)

            au___j_mtzxx = Stream("__substg1.0_" + o__n_l__j__v, _u_y_n___q_y)
            ___xv_ab__p_.append(au___j_mtzxx)

            __v_j_on__e_ = Property()
            __v_j_on__e_.tag = __rud_dv_c_t
            __v_j_on__e_.type = PropertyType.STRING_8
            __v_j_on__e_.size = len(_u_y_n___q_y) + x_m_sky_gz__
            __v_j_on__e_.is_readable = True
            __v_j_on__e_.is_writeable = True

            ______oh_ul_ += __v_j_on__e_.to_bytes()

            x_d_g___hp__ = Stream("__substg1.0_3A2A" + self.m__zli___l_b, _u_y_n___q_y)
            ___xv_ab__p_.append(x_d_g___hp__)

            ___s_y_ft__p = Property()
            ___s_y_ft__p.tag = 0x3A2A << 16 | self.wiqwtada__v_
            ___s_y_ft__p.type = PropertyType.STRING_8
            ___s_y_ft__p.size = len(_u_y_n___q_y) + x_m_sky_gz__
            ___s_y_ft__p.is_readable = True
            ___s_y_ft__p.is_writeable = True

            ______oh_ul_ += ___s_y_ft__p.to_bytes()
        

        if self.acu_i__mj_b_ is not None:
        
            _h_ji__o__q_ = self.acu_i__mj_b_.encode(self.nsifr_q_er__)
            f_h__pamd___ = Stream("__substg1.0_3A2B" + self.m__zli___l_b, _h_ji__o__q_)
            ___xv_ab__p_.append(f_h__pamd___)

            _xma___p____ = Property()
            _xma___p____.tag = 0x3A2B << 16 | self.wiqwtada__v_
            _xma___p____.type = PropertyType.STRING_8
            _xma___p____.size = len(_h_ji__o__q_) + x_m_sky_gz__
            _xma___p____.is_readable = True
            _xma___p____.is_writeable = True

            ______oh_ul_ += _xma___p____.to_bytes()
        

        if self.__dyk_vx_w__ is not None:
        
            rvppjs_mpa__ = NamedProperty()
            rvppjs_mpa__.id = 0x8047
            rvppjs_mpa__.guid = StandardPropertySet.ADDRESS
            rvppjs_mpa__.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, rvppjs_mpa__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(rvppjs_mpa__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _____g_k_o_j = self.__dyk_vx_w__.encode(self.nsifr_q_er__)

            __nem__e____ = Stream("__substg1.0_" + o__n_l__j__v, _____g_k_o_j)
            ___xv_ab__p_.append(__nem__e____)

            ____zl__a_eq = Property()
            ____zl__a_eq.tag = __rud_dv_c_t
            ____zl__a_eq.type = PropertyType.STRING_8
            ____zl__a_eq.size = len(_____g_k_o_j) + x_m_sky_gz__
            ____zl__a_eq.is_readable = True
            ____zl__a_eq.is_writeable = True

            ______oh_ul_ += ____zl__a_eq.to_bytes()

            iq__fbgi_epg = Stream("__substg1.0_3A28" + self.m__zli___l_b, _____g_k_o_j)
            ___xv_ab__p_.append(iq__fbgi_epg)

            h__pdanq_i__ = Property()
            h__pdanq_i__.tag = 0x3A28 << 16 | self.wiqwtada__v_
            h__pdanq_i__.type = PropertyType.STRING_8
            h__pdanq_i__.size = len(_____g_k_o_j) + x_m_sky_gz__
            h__pdanq_i__.is_readable = True
            h__pdanq_i__.is_writeable = True

            ______oh_ul_ += h__pdanq_i__.to_bytes()
        

        if self._q___u__q_u_ is not None:
        
            __cy__dz_xb_ = NamedProperty()
            __cy__dz_xb_.id = 0x8045
            __cy__dz_xb_.guid = StandardPropertySet.ADDRESS
            __cy__dz_xb_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __cy__dz_xb_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__cy__dz_xb_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            __xwkf_vu___ = self._q___u__q_u_.encode(self.nsifr_q_er__)

            ____j_cf____ = Stream("__substg1.0_" + o__n_l__j__v, __xwkf_vu___)
            ___xv_ab__p_.append(____j_cf____)

            ______k_l__h = Property()
            ______k_l__h.tag = __rud_dv_c_t
            ______k_l__h.type = PropertyType.STRING_8
            ______k_l__h.size = len(__xwkf_vu___) + x_m_sky_gz__
            ______k_l__h.is_readable = True
            ______k_l__h.is_writeable = True

            ______oh_ul_ += ______k_l__h.to_bytes()

            __yv_av__q__ = Stream("__substg1.0_3A29" + self.m__zli___l_b, __xwkf_vu___)
            ___xv_ab__p_.append(__yv_av__q__)

            kf_s___uuu_g = Property()
            kf_s___uuu_g.tag = 0x3A29 << 16 | self.wiqwtada__v_
            kf_s___uuu_g.type = PropertyType.STRING_8
            kf_s___uuu_g.size = len(__xwkf_vu___) + x_m_sky_gz__
            kf_s___uuu_g.is_readable = True
            kf_s___uuu_g.is_writeable = True

            ______oh_ul_ += kf_s___uuu_g.to_bytes()
        

        if self.hl_z____eu_u is not None:
        
            l_q_rug_sebw = self.hl_z____eu_u.encode(self.nsifr_q_er__)
            __y_l__i_e_o = Stream("__substg1.0_3A23" + self.m__zli___l_b, l_q_rug_sebw)
            ___xv_ab__p_.append(__y_l__i_e_o)

            s_i_hwoa_pr_ = Property()
            s_i_hwoa_pr_.tag = 0x3A23 << 16 | self.wiqwtada__v_
            s_i_hwoa_pr_.type = PropertyType.STRING_8
            s_i_hwoa_pr_.size = len(l_q_rug_sebw) + x_m_sky_gz__
            s_i_hwoa_pr_.is_readable = True
            s_i_hwoa_pr_.is_writeable = True

            ______oh_ul_ += s_i_hwoa_pr_.to_bytes()
        

        if self.__br___ty__q is not None:
        
            _j___k___jt_ = self.__br___ty__q.encode(self.nsifr_q_er__)
            d_qr___qk_ye = Stream("__substg1.0_3A1A" + self.m__zli___l_b, _j___k___jt_)
            ___xv_ab__p_.append(d_qr___qk_ye)

            x_ibhu___v_i = Property()
            x_ibhu___v_i.tag = 0x3A1A << 16 | self.wiqwtada__v_
            x_ibhu___v_i.type = PropertyType.STRING_8
            x_ibhu___v_i.size = len(_j___k___jt_) + x_m_sky_gz__
            x_ibhu___v_i.is_readable = True
            x_ibhu___v_i.is_writeable = True

            ______oh_ul_ += x_ibhu___v_i.to_bytes()
        

        if self.mma_d_p_ijv_ is not None:
        
            ___oveyjp_qh = self.mma_d_p_ijv_.encode(self.nsifr_q_er__)
            ___u_v_q__pw = Stream("__substg1.0_3A46" + self.m__zli___l_b, ___oveyjp_qh)
            ___xv_ab__p_.append(___u_v_q__pw)

            jj__gv___do_ = Property()
            jj__gv___do_.tag = 0x3A46 << 16 | self.wiqwtada__v_
            jj__gv___do_.type = PropertyType.STRING_8
            jj__gv___do_.size = len(___oveyjp_qh) + x_m_sky_gz__
            jj__gv___do_.is_readable = True
            jj__gv___do_.is_writeable = True

            ______oh_ul_ += jj__gv___do_.to_bytes()
        

        if self.p___m__s_toa is not None:
        
            __wfyj___e_x = self.p___m__s_toa.encode(self.nsifr_q_er__)
            ____r__uj___ = Stream("__substg1.0_3A1D" + self.m__zli___l_b, __wfyj___e_x)
            ___xv_ab__p_.append(____r__uj___)

            _qcc___xuvll = Property()
            _qcc___xuvll.tag = 0x3A1D << 16 | self.wiqwtada__v_
            _qcc___xuvll.type = PropertyType.STRING_8
            _qcc___xuvll.size = len(__wfyj___e_x) + x_m_sky_gz__
            _qcc___xuvll.is_readable = True
            _qcc___xuvll.is_writeable = True

            ______oh_ul_ += _qcc___xuvll.to_bytes()
        

        if self.reycs___h__f is not None:
        
            _l_ua_i__j_n = self.reycs___h__f.encode(self.nsifr_q_er__)
            _pn__g_w___a = Stream("__substg1.0_3A48" + self.m__zli___l_b, _l_ua_i__j_n)
            ___xv_ab__p_.append(_pn__g_w___a)

            _mq_k_ghwvtn = Property()
            _mq_k_ghwvtn.tag = 0x3A48 << 16 | self.wiqwtada__v_
            _mq_k_ghwvtn.type = PropertyType.STRING_8
            _mq_k_ghwvtn.size = len(_l_ua_i__j_n) + x_m_sky_gz__
            _mq_k_ghwvtn.is_readable = True
            _mq_k_ghwvtn.is_writeable = True

            ______oh_ul_ += _mq_k_ghwvtn.to_bytes()
        

        if self.__zl_e_zx___ is not None:
        
            _sm____um_no = self.__zl_e_zx___.encode(self.nsifr_q_er__)
            int__d_a_b_q = Stream("__substg1.0_3A11" + self.m__zli___l_b, _sm____um_no)
            ___xv_ab__p_.append(int__d_a_b_q)

            _h________r_ = Property()
            _h________r_.tag = 0x3A11 << 16 | self.wiqwtada__v_
            _h________r_.type = PropertyType.STRING_8
            _h________r_.size = len(_sm____um_no) + x_m_sky_gz__
            _h________r_.is_readable = True
            _h________r_.is_writeable = True

            ______oh_ul_ += _h________r_.to_bytes()
        

        if self.j_i_g__k____ is not None:
        
            __c_n__u__nv = self.j_i_g__k____.encode(self.nsifr_q_er__)
            _vu_dk_d_t__ = Stream("__substg1.0_3A2C" + self.m__zli___l_b, __c_n__u__nv)
            ___xv_ab__p_.append(_vu_dk_d_t__)

            qn_f__bu_qt_ = Property()
            qn_f__bu_qt_.tag = 0x3A2C << 16 | self.wiqwtada__v_
            qn_f__bu_qt_.type = PropertyType.STRING_8
            qn_f__bu_qt_.size = len(__c_n__u__nv) + x_m_sky_gz__
            qn_f__bu_qt_.is_readable = True
            qn_f__bu_qt_.is_writeable = True

            ______oh_ul_ += qn_f__bu_qt_.to_bytes()
        

        if self._x___k_b____ is not None:
        
            _____d_cx_sz = self._x___k_b____.encode(self.nsifr_q_er__)
            _gb_o__z_ln_ = Stream("__substg1.0_3A17" + self.m__zli___l_b, _____d_cx_sz)
            ___xv_ab__p_.append(_gb_o__z_ln_)

            d_m_d__zex_c = Property()
            d_m_d__zex_c.tag = 0x3A17 << 16 | self.wiqwtada__v_
            d_m_d__zex_c.type = PropertyType.STRING_8
            d_m_d__zex_c.size = len(_____d_cx_sz) + x_m_sky_gz__
            d_m_d__zex_c.is_readable = True
            d_m_d__zex_c.is_writeable = True

            ______oh_ul_ += d_m_d__zex_c.to_bytes()
        

        if self.jvd_z__mk__k is not None:
        
            yaic_faj__tg = self.jvd_z__mk__k.encode(self.nsifr_q_er__)
            ____lhfm__nj = Stream("__substg1.0_3A4B" + self.m__zli___l_b, yaic_faj__tg)
            ___xv_ab__p_.append(____lhfm__nj)

            __zs_snf__q_ = Property()
            __zs_snf__q_.tag = 0x3A4B << 16 | self.wiqwtada__v_
            __zs_snf__q_.type = PropertyType.STRING_8
            __zs_snf__q_.size = len(yaic_faj__tg) + x_m_sky_gz__
            __zs_snf__q_.is_readable = True
            __zs_snf__q_.is_writeable = True

            ______oh_ul_ += __zs_snf__q_.to_bytes()
        

        if self.__g___vgx_da > datetime.datetime(1901,1,1):
        
            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self.__g___vgx_da - jgv__c_h___y).total_seconds()) * 10_000_000

            du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

            aubugl_np__n = Property()
            aubugl_np__n.tag = 0x3A410040
            aubugl_np__n.type = PropertyType.TIME
            aubugl_np__n.value = du___g__abr_
            aubugl_np__n.is_readable = True
            aubugl_np__n.is_writeable = False

            ______oh_ul_ += aubugl_np__n.to_bytes()
        

        if self.o_y_e___dh__ != Gender.NONE:
        
            _co___r__lyc = Property()
            _co___r__lyc.tag = 0x3A4D0002
            _co___r__lyc.type = PropertyType.Integer16
            _co___r__lyc.value = int.to_bytes(EnumUtil.parse_gender(self.o_y_e___dh__), 4, "little")
            _co___r__lyc.is_readable = True
            _co___r__lyc.is_writeable = True

            ______oh_ul_ += _co___r__lyc.to_bytes()
        

        if self._______w_a__ != SelectedMailingAddress.NONE:
        
            x___xe_uv_u_ = NamedProperty()
            x___xe_uv_u_.id = 0x8022
            x___xe_uv_u_.guid = StandardPropertySet.ADDRESS
            x___xe_uv_u_.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, x___xe_uv_u_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(x___xe_uv_u_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0003

            ___________n = Property()
            ___________n.tag = __rud_dv_c_t
            ___________n.type = PropertyType.INTEGER_32
            ___________n.value = int.to_bytes(EnumUtil.parse_selected_mailing_address(self._______w_a__), 4, "little")
            ___________n.is_readable = True
            ___________n.is_writeable = True

            ______oh_ul_ += ___________n.to_bytes()
        

        if self.______yi_a_r:
        
            _lgf_xm_____ = NamedProperty()
            _lgf_xm_____.id = 0x8015
            _lgf_xm_____.guid = StandardPropertySet.ADDRESS
            _lgf_xm_____.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _lgf_xm_____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_lgf_xm_____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x000B

            _lgf_xm_____ = Property()
            _lgf_xm_____.tag = __rud_dv_c_t
            _lgf_xm_____.type = PropertyType.BOOLEAN
            _lgf_xm_____.value = int.to_bytes(1,1,"little")
            _lgf_xm_____.is_readable = True
            _lgf_xm_____.is_writeable = True

            ______oh_ul_ += _lgf_xm_____.to_bytes()
        

        if self.a____h_d_m__ is not None:
        
            __z___la_anx = NamedProperty()
            __z___la_anx.id = 0x8005
            __z___la_anx.guid = StandardPropertySet.ADDRESS
            __z___la_anx.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, __z___la_anx)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(__z___la_anx)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            h_aw___xip__ = self.a____h_d_m__.encode(self.nsifr_q_er__)
            of___v_w_a_w = Stream("__substg1.0_" + o__n_l__j__v, h_aw___xip__)
            ___xv_ab__p_.append(of___v_w_a_w)

            ratz_c_j____ = Property()
            ratz_c_j____.tag = __rud_dv_c_t
            ratz_c_j____.type = PropertyType.STRING_8
            ratz_c_j____.size = len(h_aw___xip__) + x_m_sky_gz__
            ratz_c_j____.is_readable = True
            ratz_c_j____.is_writeable = True

            ______oh_ul_ += ratz_c_j____.to_bytes()
        

        if self.___p___m_x__ is not None:
        
            nvswf_o_ftek = NamedProperty()
            nvswf_o_ftek.id = 0x8062
            nvswf_o_ftek.guid = StandardPropertySet.ADDRESS
            nvswf_o_ftek.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, nvswf_o_ftek)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(nvswf_o_ftek)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            __y___j__qcw = self.___p___m_x__.encode(self.nsifr_q_er__)
            c____nds___j = Stream("__substg1.0_" + o__n_l__j__v, __y___j__qcw)
            ___xv_ab__p_.append(c____nds___j)

            _tzpzvps__p_ = Property()
            _tzpzvps__p_.tag = __rud_dv_c_t
            _tzpzvps__p_.type = PropertyType.STRING_8
            _tzpzvps__p_.size = len(__y___j__qcw) + x_m_sky_gz__
            _tzpzvps__p_.is_readable = True
            _tzpzvps__p_.is_writeable = True

            ______oh_ul_ += _tzpzvps__p_.to_bytes()
        

        if self.a__yb______q is not None:
        
            _ob______p_g = NamedProperty()
            _ob______p_g.id = 0x80D8
            _ob______p_g.guid = StandardPropertySet.ADDRESS
            _ob______p_g.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _ob______p_g)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_ob______p_g)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _mxwot_v_h__ = self.a__yb______q.encode(self.nsifr_q_er__)
            i_zcbf_dg_w_ = Stream("__substg1.0_" + o__n_l__j__v, _mxwot_v_h__)
            ___xv_ab__p_.append(i_zcbf_dg_w_)

            ___bmzl___fp = Property()
            ___bmzl___fp.tag = __rud_dv_c_t
            ___bmzl___fp.type = PropertyType.STRING_8
            ___bmzl___fp.size = len(_mxwot_v_h__) + x_m_sky_gz__
            ___bmzl___fp.is_readable = True
            ___bmzl___fp.is_writeable = True

            ______oh_ul_ += ___bmzl___fp.to_bytes()
        

        if self._in__an_yv__ is not None:
        
            zmp__e____ll = NamedProperty()
            zmp__e____ll.id = 0x801B
            zmp__e____ll.guid = StandardPropertySet.ADDRESS
            zmp__e____ll.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, zmp__e____ll)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(zmp__e____ll)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            a_gkv___ms__ = self._in__an_yv__.encode(self.nsifr_q_er__)
            vr_ua_dh_iw_ = Stream("__substg1.0_" + o__n_l__j__v, a_gkv___ms__)
            ___xv_ab__p_.append(vr_ua_dh_iw_)

            _lcbvddqo___ = Property()
            _lcbvddqo___.tag = __rud_dv_c_t
            _lcbvddqo___.type = PropertyType.STRING_8
            _lcbvddqo___.size = len(a_gkv___ms__) + x_m_sky_gz__
            _lcbvddqo___.is_readable = True
            _lcbvddqo___.is_writeable = True

            ______oh_ul_ += _lcbvddqo___.to_bytes()
        

        if self.kwi_e__ffg__ is not None:
        
            ud_h_____v_g = NamedProperty()
            ud_h_____v_g.id = 0x801A
            ud_h_____v_g.guid = StandardPropertySet.ADDRESS
            ud_h_____v_g.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ud_h_____v_g)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(ud_h_____v_g)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ____uomx__a_ = self.kwi_e__ffg__.encode(self.nsifr_q_er__)
            geckwhna___c = Stream("__substg1.0_" + o__n_l__j__v, ____uomx__a_)
            ___xv_ab__p_.append(geckwhna___c)

            j___w__b__h_ = Property()
            j___w__b__h_.tag = __rud_dv_c_t
            j___w__b__h_.type = PropertyType.STRING_8
            j___w__b__h_.size = len(____uomx__a_) + x_m_sky_gz__
            j___w__b__h_.is_readable = True
            j___w__b__h_.is_writeable = True

            ______oh_ul_ += j___w__b__h_.to_bytes()
        


        if self.___ym__z_v__ is not None:
        
            so___ty____z = NamedProperty()
            so___ty____z.id = 0x801C
            so___ty____z.guid = StandardPropertySet.ADDRESS
            so___ty____z.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, so___ty____z)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(so___ty____z)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _v_q_onz__m_ = self.___ym__z_v__.encode(self.nsifr_q_er__)
            ____b_iv__i_ = Stream("__substg1.0_" + o__n_l__j__v, _v_q_onz__m_)
            ___xv_ab__p_.append(____b_iv__i_)

            km_s__n_m_vj = Property()
            km_s__n_m_vj.tag = __rud_dv_c_t
            km_s__n_m_vj.type = PropertyType.STRING_8
            km_s__n_m_vj.size = len(_v_q_onz__m_) + x_m_sky_gz__
            km_s__n_m_vj.is_readable = True
            km_s__n_m_vj.is_writeable = True

            ______oh_ul_ += km_s__n_m_vj.to_bytes()
        

        if self.s__b____or_b is not None:
        
            _m_f___a_b__ = NamedProperty()
            _m_f___a_b__.id = 0x8083
            _m_f___a_b__.guid = StandardPropertySet.ADDRESS
            _m_f___a_b__.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _m_f___a_b__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_m_f___a_b__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            x___________ = self.s__b____or_b.encode(self.nsifr_q_er__)
            __by___v_q_t = Stream("__substg1.0_" + o__n_l__j__v, x___________)
            ___xv_ab__p_.append(__by___v_q_t)

            x_f_cdelhdv_ = Property()
            x_f_cdelhdv_.tag = __rud_dv_c_t
            x_f_cdelhdv_.type = PropertyType.STRING_8
            x_f_cdelhdv_.size = len(x___________) + x_m_sky_gz__
            x_f_cdelhdv_.is_readable = True
            x_f_cdelhdv_.is_writeable = True

            ______oh_ul_ += x_f_cdelhdv_.to_bytes()
        

        if self._us___o__z__ is not None:
        
            ____qt__rcz_ = NamedProperty()
            ____qt__rcz_.id = 0x8093
            ____qt__rcz_.guid = StandardPropertySet.ADDRESS
            ____qt__rcz_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ____qt__rcz_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(____qt__rcz_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _u_g__m__p__ = self._us___o__z__.encode(self.nsifr_q_er__)
            __ss__vu___k = Stream("__substg1.0_" + o__n_l__j__v, _u_g__m__p__)
            ___xv_ab__p_.append(__ss__vu___k)

            __tqj___xr_g = Property()
            __tqj___xr_g.tag = __rud_dv_c_t
            __tqj___xr_g.type = PropertyType.STRING_8
            __tqj___xr_g.size = len(_u_g__m__p__) + x_m_sky_gz__
            __tqj___xr_g.is_readable = True
            __tqj___xr_g.is_writeable = True

            ______oh_ul_ += __tqj___xr_g.to_bytes()
        

        if self._cf__c_q__c_ is not None:
        
            d_h__l__jg_i = NamedProperty()
            d_h__l__jg_i.id = 0x80A3
            d_h__l__jg_i.guid = StandardPropertySet.ADDRESS
            d_h__l__jg_i.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, d_h__l__jg_i)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(d_h__l__jg_i)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            x___xc_qstd_ = self._cf__c_q__c_.encode(self.nsifr_q_er__)
            _je___u_rz__ = Stream("__substg1.0_" + o__n_l__j__v, x___xc_qstd_)
            ___xv_ab__p_.append(_je___u_rz__)

            __n_k_bkm___ = Property()
            __n_k_bkm___.tag = __rud_dv_c_t
            __n_k_bkm___.type = PropertyType.STRING_8
            __n_k_bkm___.size = len(x___xc_qstd_) + x_m_sky_gz__
            __n_k_bkm___.is_readable = True
            __n_k_bkm___.is_writeable = True

            ______oh_ul_ += __n_k_bkm___.to_bytes()
        

        if self.y___cq__rk__ is not None:
        
            q____x____qk = NamedProperty()
            q____x____qk.id = 0x8084
            q____x____qk.guid = StandardPropertySet.ADDRESS
            q____x____qk.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, q____x____qk)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(q____x____qk)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _d__cm____ca = self.y___cq__rk__.encode(self.nsifr_q_er__)
            __ca_l__xvc_ = Stream("__substg1.0_" + o__n_l__j__v, _d__cm____ca)
            ___xv_ab__p_.append(__ca_l__xvc_)

            obh___vj__l_ = Property()
            obh___vj__l_.tag = __rud_dv_c_t
            obh___vj__l_.type = PropertyType.STRING_8
            obh___vj__l_.size = len(_d__cm____ca) + x_m_sky_gz__
            obh___vj__l_.is_readable = True
            obh___vj__l_.is_writeable = True

            ______oh_ul_ += obh___vj__l_.to_bytes()
        

        if self.w_g_ag_b_w__ is not None:
        
            mg_wc_q_g___ = NamedProperty()
            mg_wc_q_g___.id = 0x8094
            mg_wc_q_g___.guid = StandardPropertySet.ADDRESS
            mg_wc_q_g___.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, mg_wc_q_g___)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(mg_wc_q_g___)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _i_w_w__i__k = self.w_g_ag_b_w__.encode(self.nsifr_q_er__)
            c_g__fj__k_q = Stream("__substg1.0_" + o__n_l__j__v, _i_w_w__i__k)
            ___xv_ab__p_.append(c_g__fj__k_q)

            ______k_y__t = Property()
            ______k_y__t.tag = __rud_dv_c_t
            ______k_y__t.type = PropertyType.STRING_8
            ______k_y__t.size = len(_i_w_w__i__k) + x_m_sky_gz__
            ______k_y__t.is_readable = True
            ______k_y__t.is_writeable = True

            ______oh_ul_ += ______k_y__t.to_bytes()
        

        if self.j_t_u__f____ is not None:
        
            _d_nc_sd___d = NamedProperty()
            _d_nc_sd___d.id = 0x80A4
            _d_nc_sd___d.guid = StandardPropertySet.ADDRESS
            _d_nc_sd___d.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _d_nc_sd___d)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_d_nc_sd___d)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            g_a__fwivj_p = self.j_t_u__f____.encode(self.nsifr_q_er__)
            _____yyr____ = Stream("__substg1.0_" + o__n_l__j__v, g_a__fwivj_p)
            ___xv_ab__p_.append(_____yyr____)

            ____n_p__q__ = Property()
            ____n_p__q__.tag = __rud_dv_c_t
            ____n_p__q__.type = PropertyType.STRING_8
            ____n_p__q__.size = len(g_a__fwivj_p) + x_m_sky_gz__
            ____n_p__q__.is_readable = True
            ____n_p__q__.is_writeable = True

            ______oh_ul_ += ____n_p__q__.to_bytes()
        

        if self._z___m__jkqj is not None:
        
            _______us_wr = NamedProperty()
            _______us_wr.id = 0x8080
            _______us_wr.guid = StandardPropertySet.ADDRESS
            _______us_wr.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _______us_wr)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_______us_wr)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ___wsm_h__p_ = self._z___m__jkqj.encode(self.nsifr_q_er__)
            _oaljc__q___ = Stream("__substg1.0_" + o__n_l__j__v, ___wsm_h__p_)
            ___xv_ab__p_.append(_oaljc__q___)

            b_nqg_____id = Property()
            b_nqg_____id.tag = __rud_dv_c_t
            b_nqg_____id.type = PropertyType.STRING_8
            b_nqg_____id.size = len(___wsm_h__p_) + x_m_sky_gz__
            b_nqg_____id.is_readable = True
            b_nqg_____id.is_writeable = True

            ______oh_ul_ += b_nqg_____id.to_bytes()
        

        if self.m__nj____x__ is not None:
        
            j__h___d_h__ = NamedProperty()
            j__h___d_h__.id = 0x8090
            j__h___d_h__.guid = StandardPropertySet.ADDRESS
            j__h___d_h__.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, j__h___d_h__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(j__h___d_h__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _tyd__b__s_r = self.m__nj____x__.encode(self.nsifr_q_er__)
            _q_g__r___b_ = Stream("__substg1.0_" + o__n_l__j__v, _tyd__b__s_r)
            ___xv_ab__p_.append(_q_g__r___b_)

            sx__jazci___ = Property()
            sx__jazci___.tag = __rud_dv_c_t
            sx__jazci___.type = PropertyType.STRING_8
            sx__jazci___.size = len(_tyd__b__s_r) + x_m_sky_gz__
            sx__jazci___.is_readable = True
            sx__jazci___.is_writeable = True

            ______oh_ul_ += sx__jazci___.to_bytes()
        

        if self.h_k_lm______ is not None:
        
            jd_d_x_w_nq_ = NamedProperty()
            jd_d_x_w_nq_.id = 0x80A0
            jd_d_x_w_nq_.guid = StandardPropertySet.ADDRESS
            jd_d_x_w_nq_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, jd_d_x_w_nq_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(jd_d_x_w_nq_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _x_flcv_x__x = self.h_k_lm______.encode(self.nsifr_q_er__)
            h_j_uh___n__ = Stream("__substg1.0_" + o__n_l__j__v, _x_flcv_x__x)
            ___xv_ab__p_.append(h_j_uh___n__)

            te__wrs____u = Property()
            te__wrs____u.tag = __rud_dv_c_t
            te__wrs____u.type = PropertyType.STRING_8
            te__wrs____u.size = len(_x_flcv_x__x) + x_m_sky_gz__
            te__wrs____u.is_readable = True
            te__wrs____u.is_writeable = True

            ______oh_ul_ += te__wrs____u.to_bytes()
        

        if self._f__lx__ayl_ is not None:
        
            xdn___ry____ = NamedProperty()
            xdn___ry____.id = 0x8082
            xdn___ry____.guid = StandardPropertySet.ADDRESS
            xdn___ry____.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, xdn___ry____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(xdn___ry____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            xvlhj_e_a_o_ = self._f__lx__ayl_.encode(self.nsifr_q_er__)
            b__o__pxi__i = Stream("__substg1.0_" + o__n_l__j__v, xvlhj_e_a_o_)
            ___xv_ab__p_.append(b__o__pxi__i)

            _u_k__bni__nwbj_tl_ = Property()
            _u_k__bni__nwbj_tl_.tag = __rud_dv_c_t
            _u_k__bni__nwbj_tl_.type = PropertyType.STRING_8
            _u_k__bni__nwbj_tl_.size = len(xvlhj_e_a_o_) + x_m_sky_gz__
            _u_k__bni__nwbj_tl_.is_readable = True
            _u_k__bni__nwbj_tl_.is_writeable = True

            ______oh_ul_ += _u_k__bni__nwbj_tl_.to_bytes()
        

        if self.s__g_h__crxw is not None:
        
            _xkt___yv___ = NamedProperty()
            _xkt___yv___.id = 0x8092
            _xkt___yv___.guid = StandardPropertySet.ADDRESS
            _xkt___yv___.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _xkt___yv___)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_xkt___yv___)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            _y_o______c_ = self.s__g_h__crxw.encode(self.nsifr_q_er__)
            _dt___tav___ = Stream("__substg1.0_" + o__n_l__j__v, _y_o______c_)
            ___xv_ab__p_.append(_dt___tav___)

            __f_iufq__s_ = Property()
            __f_iufq__s_.tag = __rud_dv_c_t
            __f_iufq__s_.type = PropertyType.STRING_8
            __f_iufq__s_.size = len(_y_o______c_) + x_m_sky_gz__
            __f_iufq__s_.is_readable = True
            __f_iufq__s_.is_writeable = True

            ______oh_ul_ += __f_iufq__s_.to_bytes()
        

        if self.e_o__a__mz_s is not None:
        
            ___a_jfzj_q_ = NamedProperty()
            ___a_jfzj_q_.id = 0x80A2
            ___a_jfzj_q_.guid = StandardPropertySet.ADDRESS
            ___a_jfzj_q_.type = NamedPropertyType.STRING

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, ___a_jfzj_q_)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(___a_jfzj_q_)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            lr________v_ = self.e_o__a__mz_s.encode(self.nsifr_q_er__)
            __hx__y_a___ = Stream("__substg1.0_" + o__n_l__j__v, lr________v_)
            ___xv_ab__p_.append(__hx__y_a___)

            _w_w___dhico = Property()
            _w_w___dhico.tag = __rud_dv_c_t
            _w_w___dhico.type = PropertyType.STRING_8
            _w_w___dhico.size = len(lr________v_) + x_m_sky_gz__
            _w_w___dhico.is_readable = True
            _w_w___dhico.is_writeable = True

            ______oh_ul_ += _w_w___dhico.to_bytes()
        

        if self._g_l_bu__r__ is not None:
        
            n_w_b__a_bji = NamedProperty()
            n_w_b__a_bji.id = 0x8085
            n_w_b__a_bji.guid = StandardPropertySet.ADDRESS
            n_w_b__a_bji.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, n_w_b__a_bji)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(n_w_b__a_bji)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0102
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            ue__bd____f_ = Stream("__substg1.0_" + o__n_l__j__v, self._g_l_bu__r__)
            ___xv_ab__p_.append(ue__bd____f_)

            hvapvy__u__h = Property()
            hvapvy__u__h.tag = __rud_dv_c_t
            hvapvy__u__h.type = PropertyType.INTEGER_32
            hvapvy__u__h.size = len(self._g_l_bu__r__)
            hvapvy__u__h.is_readable = True
            hvapvy__u__h.is_writeable = True

            ______oh_ul_ += hvapvy__u__h.to_bytes()
        

        if self.kw_r____n__e is not None:
        
            _myk__fnhw__ = NamedProperty()
            _myk__fnhw__.id = 0x8095
            _myk__fnhw__.guid = StandardPropertySet.ADDRESS
            _myk__fnhw__.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, _myk__fnhw__)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(_myk__fnhw__)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0102
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            o_____d_____ = Stream("__substg1.0_" + o__n_l__j__v, self.kw_r____n__e)
            ___xv_ab__p_.append(o_____d_____)

            ___u_n___yt_ = Property()
            ___u_n___yt_.tag = __rud_dv_c_t
            ___u_n___yt_.type = PropertyType.INTEGER_32
            ___u_n___yt_.size = len(self.kw_r____n__e)
            ___u_n___yt_.is_readable = True
            ___u_n___yt_.is_writeable = True

            ______oh_ul_ += ___u_n___yt_.to_bytes()
        

        if self.ti__vpygof_h is not None:
        
            t__wdo_p____ = NamedProperty()
            t__wdo_p____.id = 0x80A5
            t__wdo_p____.guid = StandardPropertySet.ADDRESS
            t__wdo_p____.type = NamedPropertyType.NUMERICAL

            ___w_q___lm_ = Message.a_____gq_r__(ou______p___, t__wdo_p____)

            if ___w_q___lm_ == -1:
            
                ou______p___.append(t__wdo_p____)
                ___w_q___lm_ = len(ou______p___) - 1
            

            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | 0x0102
            o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

            g_zx_mhn_bx_ = Stream("__substg1.0_" + o__n_l__j__v, self.ti__vpygof_h)
            ___xv_ab__p_.append(g_zx_mhn_bx_)

            y_lsz____g__ = Property()
            y_lsz____g__.tag = __rud_dv_c_t
            y_lsz____g__.type = PropertyType.INTEGER_32
            y_lsz____g__.size = len(self.ti__vpygof_h)
            y_lsz____g__.is_readable = True
            y_lsz____g__.is_writeable = True

            ______oh_ul_ += y_lsz____g__.to_bytes()



        for e in range(len(self.fmuyou__mciw)):

            if self.fmuyou__mciw[e].value is not None:

                _i_toah_o_y_ = NamedProperty()

                if isinstance(self.fmuyou__mciw[e].tag, ExtendedPropertyId):

                    bs_bf_____w_ = self.fmuyou__mciw[e].tag

                    _i_toah_o_y_.id   = bs_bf_____w_.id
                    _i_toah_o_y_.guid = bs_bf_____w_.guid
                    _i_toah_o_y_.type = NamedPropertyType.NUMERICAL

                else:

                    bs_bf_____w_ = self.fmuyou__mciw[e].tag

                    _i_toah_o_y_.name = bs_bf_____w_.name
                    _i_toah_o_y_.guid = bs_bf_____w_.guid
                    _i_toah_o_y_.type = NamedPropertyType.STRING

                if Message.a_____gq_r__(ou______p___, _i_toah_o_y_) == -1:

                    ou______p___.append(_i_toah_o_y_)
                    ___w_q___lm_ = len(ou______p___) - 1

                    __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | Message.___wg___smt_(self.fmuyou__mciw[e].tag.type)

                    if self.fmuyou__mciw[e].tag.type == PropertyType.BOOLEAN or self.fmuyou__mciw[e].tag.type == PropertyType.INTEGER_16 or self.fmuyou__mciw[e].tag.type == PropertyType.INTEGER_32 or self.fmuyou__mciw[e].tag.type == PropertyType.INTEGER_64 or self.fmuyou__mciw[e].tag.type == PropertyType.FLOATING_32 or self.fmuyou__mciw[e].tag.type == PropertyType.FLOATING_64 or self.fmuyou__mciw[e].tag.type == PropertyType.FLOATING_TIME or self.fmuyou__mciw[e].tag.type == PropertyType.TIME:

                        tx__g_gl___q = Property()
                        tx__g_gl___q.tag = __rud_dv_c_t
                        tx__g_gl___q.type = self.fmuyou__mciw[e].tag.type
                        tx__g_gl___q.value = self.fmuyou__mciw[e].value
                        tx__g_gl___q.is_readable = True
                        tx__g_gl___q.is_writeable = True

                        ______oh_ul_ += tx__g_gl___q.to_bytes()

                    elif self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_CURRENCY or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_FLOATING_32 or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_FLOATING_64 or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_FLOATING_TIME or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_GUID or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_INTEGER_16 or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_INTEGER_32 or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_INTEGER_64 or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_STRING or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_STRING_8 or self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_TIME:

                        pass

                    elif self.fmuyou__mciw[e].tag.type == PropertyType.MULTIPLE_BINARY:

                        o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

                        l__i___n_i__ = bytearray()

                        ivwgq_u_qjrl = int.from_bytes(self.fmuyou__mciw[e].value[0:4], "little")

                        b_kd_____v__ = [None]*(ivwgq_u_qjrl + 1)

                        for i in range(ivwgq_u_qjrl):
                            b_kd_____v__[i] = int.from_bytes(self.fmuyou__mciw[e].value[4 + i * 4: 4 + i * 4 + 4], "little")
                
                        b_kd_____v__[ivwgq_u_qjrl] = len(self.fmuyou__mciw[e].value)

                        for i in range(len(b_kd_____v__) - 1):

                            w__ar_s__m__ = (b_kd_____v__[i + 1] - b_kd_____v__[i])
                            zy______o___ = int.to_bytes(w__ar_s__m__, 8, "little")

                            l__i___n_i__ += zy______o___
                            ____t___sh_c = self.fmuyou__mciw[e].value[b_kd_____v__[i]: b_kd_____v__[i] + w__ar_s__m__]

                            _q__or_ip_dt = "__substg1.0_" + o__n_l__j__v + "-" + str.format("{:08X}", i)
                            
                            qew__vs_j_hm = Stream(_q__or_ip_dt, ____t___sh_c)
                            
                            ___xv_ab__p_.append(qew__vs_j_hm)
                        

                        _u_ws_p_s_o_ = bytes(l__i___n_i__)

                        iqsezii___zt = Stream("__substg1.0_" + o__n_l__j__v, _u_ws_p_s_o_)
                        ___xv_ab__p_.append(iqsezii___zt)

                        yn_e_cunkz_s = Property()
                        yn_e_cunkz_s.tag = __rud_dv_c_t
                        yn_e_cunkz_s.type = PropertyType.MULTIPLE_BINARY
                        yn_e_cunkz_s.size = len(_u_ws_p_s_o_)
                        yn_e_cunkz_s.is_readable = True
                        yn_e_cunkz_s.is_writeable = True

                        ______oh_ul_ += yn_e_cunkz_s.to_bytes()

                    else:

                        ____t___sh_c = self.fmuyou__mciw[e].value

                        if ____t___sh_c is not None and self.fmuyou__mciw[e].tag.type == PropertyType.STRING and self.nsifr_q_er__ != self.h_c_rs_lkt__:

                            _rdjx_____e_ = ____t___sh_c.decode(self.h_c_rs_lkt__)
                            ____t___sh_c = _rdjx_____e_.encode(self.nsifr_q_er__)

                            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_

                        elif ____t___sh_c is not None and self.fmuyou__mciw[e].tag.type == PropertyType.STRING_8 and self.nsifr_q_er__ == self.h_c_rs_lkt__:

                            _rdjx_____e_ = ____t___sh_c.decode(self._x_q___iqwz_)
                            ____t___sh_c = _rdjx_____e_.encode(self.nsifr_q_er__)

                            __rud_dv_c_t = (0x8000 + ___w_q___lm_) << 16 | self.wiqwtada__v_


                        o__n_l__j__v = str.format("{:08X}", __rud_dv_c_t)

                        q__d____cu__ = Stream("__substg1.0_" + o__n_l__j__v, ____t___sh_c)
                        ___xv_ab__p_.append(q__d____cu__)

                        tx__g_gl___q = Property()
                        tx__g_gl___q.tag = __rud_dv_c_t

                        if (self.fmuyou__mciw[e].tag.type == PropertyType.BINARY or self.fmuyou__mciw[e].tag.type == PropertyType.OBJECT):
                            tx__g_gl___q.type = PropertyType.INTEGER_32
                        else:
                            tx__g_gl___q.type = PropertyType.STRING_8

                        tx__g_gl___q.size = Message._bo_e__n___q(____t___sh_c, self.fmuyou__mciw[e].tag.type, self.nsifr_q_er__)
                        tx__g_gl___q.is_readable = True
                        tx__g_gl___q.is_writeable = True

                        ______oh_ul_ += tx__g_gl___q.to_bytes()


        ch_tqnyok___ = Stream("__properties_version1.0", bytes(______oh_ul_))
        ___xv_ab__p_.append(ch_tqnyok___)

        for i in range(len(self.__w_e______y)):

            ___fb_____c_ = str.format("__recip_version1.0_#{:08X}", i)
            o__qtb_____p = Storage(___fb_____c_)

            b_n__qu_z_ve = self.__w_e______y[i]

            ___h_w___w__ = bytearray()

            it___cv_rgc_ = bytes(8)
            ___h_w___w__ += it___cv_rgc_


            u___tek_p__t = Property()
            u___tek_p__t.tag = 0x30000003
            u___tek_p__t.type = PropertyType.INTEGER_32
            u___tek_p__t.value = int.to_bytes(i, 4, "little")
            u___tek_p__t.is_readable = True
            u___tek_p__t.is_writeable = True

            ___h_w___w__ += u___tek_p__t.to_bytes()

            if b_n__qu_z_ve.display_type != DisplayType.NONE:
            
                y_yqp_w____l = Property()
                y_yqp_w____l.tag = 0x39000003
                y_yqp_w____l.type = PropertyType.INTEGER_32
                y_yqp_w____l.value = int.to_bytes(EnumUtil.parse_display_type(b_n__qu_z_ve.display_type), 4, "little")
                y_yqp_w____l.is_readable = True
                y_yqp_w____l.is_writeable = True

                ___h_w___w__ += y_yqp_w____l.to_bytes()
            

            if b_n__qu_z_ve.object_type != ObjectType.NONE:
            
                o______jc_u_ = Property()
                o______jc_u_.tag = 0x0FFE0003
                o______jc_u_.type = PropertyType.INTEGER_32
                o______jc_u_.value = int.to_bytes(EnumUtil.parse_object_type(b_n__qu_z_ve.object_type), 4, "little")
                o______jc_u_.is_readable = True
                o______jc_u_.is_writeable = True

                ___h_w___w__ += o______jc_u_.to_bytes()
            

            if b_n__qu_z_ve.recipient_type != RecipientType.NONE:
            
                ______oq____ = Property()
                ______oq____.tag = 0x0C150003
                ______oq____.type = PropertyType.INTEGER_32
                ______oq____.value = int.to_bytes(EnumUtil.parse_recipient_type(b_n__qu_z_ve.recipient_type), 4, "little")
                ______oq____.is_readable = True
                ______oq____.is_writeable = True

                ___h_w___w__ += ______oq____.to_bytes()
            

            if b_n__qu_z_ve.display_name is not None:
            
                __wb____mxat = b_n__qu_z_ve.display_name.encode(self.nsifr_q_er__)

                au___tv___a_ = Stream("__substg1.0_3001" + self.m__zli___l_b, __wb____mxat)
                o__qtb_____p.directory_entries.append(au___tv___a_)

                nb__opljqv__ = Property()
                nb__opljqv__.tag = 0x3001 << 16 | self.wiqwtada__v_
                nb__opljqv__.type = PropertyType.STRING_8
                nb__opljqv__.size = len(__wb____mxat) + x_m_sky_gz__
                nb__opljqv__.is_readable = True
                nb__opljqv__.is_writeable = True

                ___h_w___w__ += nb__opljqv__.to_bytes()

                _mkvwta_____ = Stream("__substg1.0_5FF6" + self.m__zli___l_b, __wb____mxat)
                o__qtb_____p.directory_entries.append(_mkvwta_____)

                _apx__sme__n = Property()
                _apx__sme__n.tag = 0x5FF6 << 16 | self.wiqwtada__v_
                _apx__sme__n.type = PropertyType.STRING_8
                _apx__sme__n.size = len(__wb____mxat) + x_m_sky_gz__
                _apx__sme__n.is_readable = True
                _apx__sme__n.is_writeable = True

                ___h_w___w__ += _apx__sme__n.to_bytes()
            

            if b_n__qu_z_ve.email_address is not None:
            
                yws___xy___z = b_n__qu_z_ve.email_address.encode(self.nsifr_q_er__)
                ___x_yufie__ = Stream("__substg1.0_3003" + self.m__zli___l_b, yws___xy___z)
                o__qtb_____p.directory_entries.append(___x_yufie__)

                _____h_ay_p_ = Property()
                _____h_ay_p_.tag = 0x3003 << 16 | self.wiqwtada__v_
                _____h_ay_p_.type = PropertyType.STRING_8
                _____h_ay_p_.size = len(yws___xy___z) + x_m_sky_gz__
                _____h_ay_p_.is_readable = True
                _____h_ay_p_.is_writeable = True

                ___h_w___w__ += _____h_ay_p_.to_bytes()
            

            if b_n__qu_z_ve.address_type is not None:
            
                _p_x__q___x_ = b_n__qu_z_ve.address_type.encode(self.nsifr_q_er__)
                _t_of_dh____ = Stream("__substg1.0_3002" + self.m__zli___l_b, _p_x__q___x_)
                o__qtb_____p.directory_entries.append(_t_of_dh____)

                i__pwo_h__zl = Property()
                i__pwo_h__zl.tag = 0x3002 << 16 | self.wiqwtada__v_
                i__pwo_h__zl.type = PropertyType.STRING_8
                i__pwo_h__zl.size = len(_p_x__q___x_) + x_m_sky_gz__
                i__pwo_h__zl.is_readable = True
                i__pwo_h__zl.is_writeable = True

                ___h_w___w__ += i__pwo_h__zl.to_bytes()
            

            if b_n__qu_z_ve.entry_id is not None:
            
                _u_me_c___rv = Stream("__substg1.0_0FFF0102", b_n__qu_z_ve.entry_id)
                o__qtb_____p.directory_entries.append(_u_me_c___rv)

                vg__a__cy___ = Property()
                vg__a__cy___.tag = 0x0FFF0102
                vg__a__cy___.type = PropertyType.BINARY
                vg__a__cy___.size = len(b_n__qu_z_ve.entry_id)
                vg__a__cy___.is_readable = True
                vg__a__cy___.is_writeable = True

                ___h_w___w__ += vg__a__cy___.to_bytes()

                _gnin__ie_qe = Stream("__substg1.0_5FF70102", b_n__qu_z_ve.entry_id)
                o__qtb_____p.directory_entries.append(_gnin__ie_qe)

                i_f__jaystmz = Property()
                i_f__jaystmz.tag = 0x5FF70102
                i_f__jaystmz.type = PropertyType.BINARY
                i_f__jaystmz.size = len(b_n__qu_z_ve.entry_id)
                i_f__jaystmz.is_readable = True
                i_f__jaystmz.is_writeable = True

                ___h_w___w__ += i_f__jaystmz.to_bytes()
            

            if b_n__qu_z_ve.search_key is not None:
            
                ___f_ct___mk = Stream("__substg1.0_300B0102", b_n__qu_z_ve.search_key)
                o__qtb_____p.directory_entries.append(___f_ct___mk)

                xlq_brmbqs__ = Property()
                xlq_brmbqs__.tag = 0x300B0102
                xlq_brmbqs__.type = PropertyType.BINARY
                xlq_brmbqs__.size = len(b_n__qu_z_ve.search_key)
                xlq_brmbqs__.is_readable = True
                xlq_brmbqs__.is_writeable = True

                ___h_w___w__ += xlq_brmbqs__.to_bytes()
            

            if b_n__qu_z_ve.instance_key is not None:
            
                tsb_h___cdnr = Stream("__substg1.0_0FF60102", b_n__qu_z_ve.instance_key)
                o__qtb_____p.directory_entries.append(tsb_h___cdnr)

                __c__pk_fydg = Property()
                __c__pk_fydg.tag = 0x0FF60102
                __c__pk_fydg.type = PropertyType.BINARY
                __c__pk_fydg.size = len(b_n__qu_z_ve.instance_key)
                __c__pk_fydg.is_readable = True
                __c__pk_fydg.is_writeable = True

                ___h_w___w__ += __c__pk_fydg.to_bytes()
            

            if b_n__qu_z_ve.responsibility:
            
                kiwxnyl_p_bs = Property()
                kiwxnyl_p_bs.tag = 0x0E0F000B
                kiwxnyl_p_bs.type = PropertyType.BOOLEAN
                kiwxnyl_p_bs.value = int.to_bytes(1, 1, "little")
                kiwxnyl_p_bs.is_readable = True
                kiwxnyl_p_bs.is_writeable = True

                ___h_w___w__ += kiwxnyl_p_bs.to_bytes()
            

            if b_n__qu_z_ve.send_rich_info:
            
                _______exgds = Property()
                _______exgds.tag = 0x3A40000B
                _______exgds.type = PropertyType.BOOLEAN
                _______exgds.value = int.to_bytes(1, 1, "little")
                _______exgds.is_readable = True
                _______exgds.is_writeable = True

                ___h_w___w__ += _______exgds.to_bytes()
            

            if b_n__qu_z_ve.send_internet_encoding > 0:
            
                ov_ptvco____ = Property()
                ov_ptvco____.tag = 0x3A710003
                ov_ptvco____.type = PropertyType.INTEGER_32
                ov_ptvco____.value = int.to_bytes(b_n__qu_z_ve.send_internet_encoding, 4, "little")
                ov_ptvco____.is_readable = True
                ov_ptvco____.is_writeable = True

                ___h_w___w__ += ov_ptvco____.to_bytes()
            

            if b_n__qu_z_ve.smtp_address is not None:
            
                ij____v_z_r_ = b_n__qu_z_ve.smtp_address.encode(self.nsifr_q_er__)
                _z___u______ = Stream("__substg1.0_39FE" + self.m__zli___l_b, ij____v_z_r_)
                o__qtb_____p.directory_entries.append(_z___u______)

                ____hkm_n_f_ = Property()
                ____hkm_n_f_.tag = 0x39FE << 16 | self.wiqwtada__v_
                ____hkm_n_f_.type = PropertyType.STRING_8
                ____hkm_n_f_.size = len(ij____v_z_r_) + x_m_sky_gz__
                ____hkm_n_f_.is_readable = True
                ____hkm_n_f_.is_writeable = True

                ___h_w___w__ += ____hkm_n_f_.to_bytes()
            

            if b_n__qu_z_ve.display_name_7bit is not None:
            
                _ko___crmz__ = b_n__qu_z_ve.display_name_7bit.encode(self.nsifr_q_er__)
                o_q______i_f = Stream("__substg1.0_39FF" + self.m__zli___l_b, _ko___crmz__)
                o__qtb_____p.directory_entries.append(o_q______i_f)

                _o__b_l_iwoi = Property()
                _o__b_l_iwoi.tag = 0x39FF << 16 | self.wiqwtada__v_
                _o__b_l_iwoi.type = PropertyType.STRING_8
                _o__b_l_iwoi.size = len(_ko___crmz__) + x_m_sky_gz__
                _o__b_l_iwoi.is_readable = True
                _o__b_l_iwoi.is_writeable = True

                ___h_w___w__ += _o__b_l_iwoi.to_bytes()
            

            if b_n__qu_z_ve.transmitable_display_name is not None:
            
                ane__e_cw_h_ = b_n__qu_z_ve.transmitable_display_name.encode(self.nsifr_q_er__)
                _v_z____t_ex = Stream("__substg1.0_3A20" + self.m__zli___l_b, ane__e_cw_h_)
                o__qtb_____p.directory_entries.append(_v_z____t_ex)

                vb__mrs_____ = Property()
                vb__mrs_____.tag = 0x3A20 << 16 | self.wiqwtada__v_
                vb__mrs_____.type = PropertyType.STRING_8
                vb__mrs_____.size = len(ane__e_cw_h_) + x_m_sky_gz__
                vb__mrs_____.is_readable = True
                vb__mrs_____.is_writeable = True

                ___h_w___w__ += vb__mrs_____.to_bytes()
            

            if b_n__qu_z_ve.originating_address_type is not None:
            
                i__a_d_osnu_ = b_n__qu_z_ve.originating_address_type.encode(self.nsifr_q_er__)
                _w__g_lffx__ = Stream("__substg1.0_403D" + self.m__zli___l_b, i__a_d_osnu_)
                o__qtb_____p.directory_entries.append(_w__g_lffx__)

                __us_cw_mq__ = Property()
                __us_cw_mq__.tag = 0x403D << 16 | self.wiqwtada__v_
                __us_cw_mq__.type = PropertyType.STRING_8
                __us_cw_mq__.size = len(i__a_d_osnu_) + x_m_sky_gz__
                __us_cw_mq__.is_readable = True
                __us_cw_mq__.is_writeable = True

                ___h_w___w__ += __us_cw_mq__.to_bytes()
            

            if b_n__qu_z_ve.originating_email_address is not None:
            
                a_uw_ri___k_ = b_n__qu_z_ve.originating_email_address.encode(self.nsifr_q_er__)
                __vf__m___j_ = Stream("__substg1.0_403E" + self.m__zli___l_b, a_uw_ri___k_)
                o__qtb_____p.directory_entries.append(__vf__m___j_)

                qe_v_jl__p_y = Property()
                qe_v_jl__p_y.tag = 0x403E << 16 | self.wiqwtada__v_
                qe_v_jl__p_y.type = PropertyType.STRING_8
                qe_v_jl__p_y.size = len(a_uw_ri___k_) + x_m_sky_gz__
                qe_v_jl__p_y.is_readable = True
                qe_v_jl__p_y.is_writeable = True

                ___h_w___w__ += qe_v_jl__p_y.to_bytes()
            

            ___d_______y = Stream("__properties_version1.0", bytes(___h_w___w__))

            o__qtb_____p.directory_entries.append(___d_______y)

            ___xv_ab__p_.append(o__qtb_____p)
    

        for i in range(len(self.uj_c_u_uy___)):
        
            v_xaz_____o_ = str.format("__attach_version1.0_#{:08X}", i)
            _u___wzy_exl = Storage(v_xaz_____o_)

            u_b__at__inv = self.uj_c_u_uy___[i]

            _sq_c_pgm_pj = bytearray()

            __qot_o__f__ = bytes(8)
            _sq_c_pgm_pj += __qot_o__f__

            _c____ohm___ = Property()
            _c____ohm___.tag = 0x0E210003
            _c____ohm___.type = PropertyType.INTEGER_32
            _c____ohm___.value = int.to_bytes(i, 4, "little")
            _c____ohm___.is_readable = True
            _c____ohm___.is_writeable = False

            _sq_c_pgm_pj += _c____ohm___.to_bytes()

            lpna_vbu__x_ = Property()
            lpna_vbu__x_.tag = 0x7FFA0003
            lpna_vbu__x_.type = PropertyType.INTEGER_32
            lpna_vbu__x_.value = int.to_bytes(i, 4, "little")
            lpna_vbu__x_.is_readable = True
            lpna_vbu__x_.is_writeable = True

            _sq_c_pgm_pj += lpna_vbu__x_.to_bytes()

            u_b__at__inv.record_key = int.to_bytes(i, 4, "little")
            pk_xaa___i__ = Stream("__substg1.0_0FF90102", u_b__at__inv.record_key)
            _u___wzy_exl.directory_entries.append(pk_xaa___i__)

            ___a__kfu_o_ = Property()
            ___a__kfu_o_.tag = 0x0FF90102
            ___a__kfu_o_.type = PropertyType.BINARY
            ___a__kfu_o_.size = len(u_b__at__inv.record_key)
            ___a__kfu_o_.is_readable = True
            ___a__kfu_o_.is_writeable = True

            _sq_c_pgm_pj += ___a__kfu_o_.to_bytes()

            if u_b__at__inv.additional_info is not None:
            
                ha___z_b___k = Stream("__substg1.0_370F0102", u_b__at__inv.additional_info)
                _u___wzy_exl.directory_entries.append(ha___z_b___k)

                bq_____ia__g = Property()
                bq_____ia__g.tag = 0x370F0102
                bq_____ia__g.type = PropertyType.BINARY
                bq_____ia__g.size = len(u_b__at__inv.additional_info)
                bq_____ia__g.is_readable = True
                bq_____ia__g.is_writeable = True

                _sq_c_pgm_pj += bq_____ia__g.to_bytes()
            

            if u_b__at__inv.content_base is not None:
            
                ___l_pj____o = u_b__at__inv.content_base.encode(self.nsifr_q_er__)
                e_xjz__h__rk = Stream("__substg1.0_3711" + self.m__zli___l_b, ___l_pj____o)
                _u___wzy_exl.directory_entries.append(e_xjz__h__rk)

                mhuqhn____vw = Property()
                mhuqhn____vw.tag = 0x3711 << 16 | self.wiqwtada__v_
                mhuqhn____vw.type = PropertyType.STRING_8
                mhuqhn____vw.size = len(___l_pj____o) + x_m_sky_gz__
                mhuqhn____vw.is_readable = True
                mhuqhn____vw.is_writeable = True

                _sq_c_pgm_pj += mhuqhn____vw.to_bytes()
            

            if u_b__at__inv.content_id is not None:
            
                _xfcs____i_j = u_b__at__inv.content_id.encode(self.nsifr_q_er__)
                _j_t_o__v_d_ = Stream("__substg1.0_3712" + self.m__zli___l_b, _xfcs____i_j)
                _u___wzy_exl.directory_entries.append(_j_t_o__v_d_)

                c_l_q____cj_ = Property()
                c_l_q____cj_.tag = 0x3712 << 16 | self.wiqwtada__v_
                c_l_q____cj_.type = PropertyType.STRING_8
                c_l_q____cj_.size = len(_xfcs____i_j) + x_m_sky_gz__
                c_l_q____cj_.is_readable = True
                c_l_q____cj_.is_writeable = True

                _sq_c_pgm_pj += c_l_q____cj_.to_bytes()
            

            if u_b__at__inv.content_location is not None:
            
                ygi_l____rs_ = u_b__at__inv.content_location.encode(self.nsifr_q_er__)
                f____jm_____ = Stream("__substg1.0_3713" + self.m__zli___l_b, ygi_l____rs_)
                _u___wzy_exl.directory_entries.append(f____jm_____)

                ef___i_rotb_ = Property()
                ef___i_rotb_.tag = 0x3713 << 16 | self.wiqwtada__v_
                ef___i_rotb_.type = PropertyType.STRING_8
                ef___i_rotb_.size = len(ygi_l____rs_) + x_m_sky_gz__
                ef___i_rotb_.is_readable = True
                ef___i_rotb_.is_writeable = True

                _sq_c_pgm_pj += ef___i_rotb_.to_bytes()
            

            if u_b__at__inv.content_disposition is not None:
            
                e__p___fjm__ = u_b__at__inv.content_disposition.encode(self.nsifr_q_er__)
                to__m__s_g_i = Stream("__substg1.0_3716" + self.m__zli___l_b, e__p___fjm__)
                _u___wzy_exl.directory_entries.append(to__m__s_g_i)

                t_jkn__li_g_ = Property()
                t_jkn__li_g_.tag = 0x3716 << 16 | self.wiqwtada__v_
                t_jkn__li_g_.type = PropertyType.STRING_8
                t_jkn__li_g_.size = len(e__p___fjm__) + x_m_sky_gz__
                t_jkn__li_g_.is_readable = True
                t_jkn__li_g_.is_writeable = True

                _sq_c_pgm_pj += t_jkn__li_g_.to_bytes()
            

            if u_b__at__inv.data is not None:
            
                if u_b__at__inv.method == AttachmentMethod.OLE:
                
                    iic__rf_sesh = Storage("__substg1.0_3701000D")
                    _u___wzy_exl.directory_entries.append(iic__rf_sesh)

                    _r_g________ = bytearray(u_b__at__inv.data)
                    d__jumw_vdl_ = CompoundFile(_r_g________)

                    iic__rf_sesh.class_id = d__jumw_vdl_.root.class_id

                    iic__rf_sesh.directory_entries.extend(d__jumw_vdl_.root.directory_entries)                    

                    ________prmq = Property()
                    _o__nv_oz___.tag = 0x3701000D
                    ________prmq.type = PropertyType.OBJECT
                    ________prmq.size = 4_000_000_000
                    ________prmq.is_readable = True
                    ________prmq.is_writeable = True
                    r_zr_k___bl_ = bytearray(________prmq.to_bytes())
                    r_zr_k___bl_[12] = 4

                    _sq_c_pgm_pj += r_zr_k___bl_
                
                else:
                
                    h_vf_ys__y_u = Stream("__substg1.0_37010102", u_b__at__inv.data)
                    _u___wzy_exl.directory_entries.append(h_vf_ys__y_u)

                    ________prmq = Property()
                    ________prmq.tag = 0x37010102
                    ________prmq.type = PropertyType.BINARY
                    ________prmq.size = len(u_b__at__inv.data)
                    ________prmq.is_readable = True
                    ________prmq.is_writeable = True

                    _sq_c_pgm_pj += ________prmq.to_bytes()


            if u_b__at__inv.encoding is not None:
            
                cx__an______ = Stream("__substg1.0_37020102", u_b__at__inv.encoding)
                _u___wzy_exl.directory_entries.append(cx__an______)

                fh_cfl_c_g__ = Property()
                fh_cfl_c_g__.tag = 0x37020102
                fh_cfl_c_g__.type = PropertyType.BINARY
                fh_cfl_c_g__.size = len(u_b__at__inv.encoding)
                fh_cfl_c_g__.is_readable = True
                fh_cfl_c_g__.is_writeable = True

                _sq_c_pgm_pj += fh_cfl_c_g__.to_bytes()


            if u_b__at__inv.extension is not None:
            
                aiwjj_vmg_ts = u_b__at__inv.extension.encode(self.nsifr_q_er__)
                rd_o_q____y_ = Stream("__substg1.0_3703" + self.m__zli___l_b, aiwjj_vmg_ts)
                _u___wzy_exl.directory_entries.append(rd_o_q____y_)

                b__ap______l = Property()
                b__ap______l.tag = 0x3703 << 16 | self.wiqwtada__v_
                b__ap______l.type = PropertyType.STRING_8
                b__ap______l.size = len(aiwjj_vmg_ts) + x_m_sky_gz__
                b__ap______l.is_readable = True
                b__ap______l.is_writeable = True

                _sq_c_pgm_pj += b__ap______l.to_bytes()
            

            if u_b__at__inv.file_name is not None:
            
                k___yo_____k = u_b__at__inv.file_name.encode(self.nsifr_q_er__)
                __s___k__pa_ = Stream("__substg1.0_3704" + self.m__zli___l_b, k___yo_____k)
                _u___wzy_exl.directory_entries.append(__s___k__pa_)

                _i__h___e_es = Property()
                _i__h___e_es.tag = 0x3704 << 16 | self.wiqwtada__v_
                _i__h___e_es.type = PropertyType.STRING_8
                _i__h___e_es.size = len(k___yo_____k) + x_m_sky_gz__
                _i__h___e_es.is_readable = True
                _i__h___e_es.is_writeable = True

                _sq_c_pgm_pj += _i__h___e_es.to_bytes()
            

            if u_b__at__inv.flags != AttachmentFlags.NONE:
            
                f__xv___eis_ = Property()
                f__xv___eis_.tag = 0x37140003
                f__xv___eis_.type = PropertyType.INTEGER_32
                f__xv___eis_.value = int.to_bytes(EnumUtil.parse_attachment_flags(u_b__at__inv.flags), 4, "little")
                f__xv___eis_.is_readable = True
                f__xv___eis_.is_writeable = True

                _sq_c_pgm_pj += f__xv___eis_.to_bytes()
            

            if u_b__at__inv.long_file_name is not None:
            
                x_x___ei__wg = u_b__at__inv.long_file_name.encode(self.nsifr_q_er__)
                qsf______a_n = Stream("__substg1.0_3707" + self.m__zli___l_b, x_x___ei__wg)
                _u___wzy_exl.directory_entries.append(qsf______a_n)

                _ah_kt___o_p = Property()
                _ah_kt___o_p.tag = 0x3707 << 16 | self.wiqwtada__v_
                _ah_kt___o_p.type = PropertyType.STRING_8
                _ah_kt___o_p.size = len(x_x___ei__wg) + x_m_sky_gz__
                _ah_kt___o_p.is_readable = True
                _ah_kt___o_p.is_writeable = True

                _sq_c_pgm_pj += _ah_kt___o_p.to_bytes()
            

            if u_b__at__inv.long_path_name is not None:
            
                fxyr_____sdl = u_b__at__inv.long_path_name.encode(self.nsifr_q_er__)
                _srkme__i_pt = Stream("__substg1.0_370D" + self.m__zli___l_b, fxyr_____sdl)
                _u___wzy_exl.directory_entries.append(_srkme__i_pt)

                bc_q__jo__bb = Property()
                bc_q__jo__bb.tag = 0x370D << 16 | self.wiqwtada__v_
                bc_q__jo__bb.type = PropertyType.STRING_8
                bc_q__jo__bb.size = len(fxyr_____sdl) + x_m_sky_gz__
                bc_q__jo__bb.is_readable = True
                bc_q__jo__bb.is_writeable = True

                _sq_c_pgm_pj += bc_q__jo__bb.to_bytes()
            

            if u_b__at__inv.method != AttachmentMethod.NONE:
            
                cu_______i_q = Property()
                cu_______i_q.tag = 0x37050003
                cu_______i_q.type = PropertyType.INTEGER_32
                cu_______i_q.value = int.to_bytes(EnumUtil.parse_attachment_method(u_b__at__inv.method), 4, "little")
                cu_______i_q.is_readable = True
                cu_______i_q.is_writeable = True

                _sq_c_pgm_pj += cu_______i_q.to_bytes()
            

            if u_b__at__inv.mime_sequence > 0:
            
                c___w_w__gio = Property()
                c___w_w__gio.tag = 0x37100003
                c___w_w__gio.type = PropertyType.INTEGER_32
                c___w_w__gio.value = int.to_bytes(u_b__at__inv.mime_sequence, 4, "little")
                c___w_w__gio.is_readable = True
                c___w_w__gio.is_writeable = True

                _sq_c_pgm_pj += c___w_w__gio.to_bytes()
            

            if u_b__at__inv.mime_tag is not None:
            
                ___vszr_u___ = u_b__at__inv.mime_tag.encode(self.nsifr_q_er__)
                do___h__ikeq = Stream("__substg1.0_370E" + self.m__zli___l_b, ___vszr_u___)
                _u___wzy_exl.directory_entries.append(do___h__ikeq)

                dws__th_ga__ = Property()
                dws__th_ga__.tag = 0x370E << 16 | self.wiqwtada__v_
                dws__th_ga__.type = PropertyType.STRING_8
                dws__th_ga__.size = len(___vszr_u___) + x_m_sky_gz__
                dws__th_ga__.is_readable = True
                dws__th_ga__.is_writeable = True

                _sq_c_pgm_pj += dws__th_ga__.to_bytes()
            

            if u_b__at__inv.path_name is not None:
            
                ___usa_w____ = u_b__at__inv.path_name.encode(self.nsifr_q_er__)
                lvu_co_o_mgg = Stream("__substg1.0_3708" + self.m__zli___l_b, ___usa_w____)
                _u___wzy_exl.directory_entries.append(lvu_co_o_mgg)

                ___g__ownt_s = Property()
                ___g__ownt_s.tag = 0x3708 << 16 | self.wiqwtada__v_
                ___g__ownt_s.type = PropertyType.STRING_8
                ___g__ownt_s.size = len(___usa_w____) + x_m_sky_gz__
                ___g__ownt_s.is_readable = True
                ___g__ownt_s.is_writeable = True

                _sq_c_pgm_pj += ___g__ownt_s.to_bytes()
            

            if u_b__at__inv.rendering is not None:
            
                _t____hj_ah_ = Stream("__substg1.0_37090102", u_b__at__inv.rendering)
                _u___wzy_exl.directory_entries.append(_t____hj_ah_)

                fax__em___kr = Property()
                fax__em___kr.tag = 0x37090102
                fax__em___kr.type = PropertyType.BINARY
                fax__em___kr.size = len(u_b__at__inv.rendering)
                fax__em___kr.is_readable = True
                fax__em___kr.is_writeable = True

                _sq_c_pgm_pj += fax__em___kr.to_bytes()
            

            if u_b__at__inv.rendering_position > 0:
            
                _____mp__f__ = Property()
                _____mp__f__.tag = 0x370b0003
                _____mp__f__.type = PropertyType.INTEGER_32
                _____mp__f__.value = int.to_bytes(u_b__at__inv.rendering_position, 4, "little")
                _____mp__f__.is_readable = True
                _____mp__f__.is_writeable = True

                _sq_c_pgm_pj += _____mp__f__.to_bytes()
            

            if u_b__at__inv.size > 0:
            
                _n_aqew___yp = Property()
                _n_aqew___yp.tag = 0x0E200003
                _n_aqew___yp.type = PropertyType.INTEGER_32
                _n_aqew___yp.value = int.to_bytes(u_b__at__inv.size, 4, "little")
                _n_aqew___yp.is_readable = True
                _n_aqew___yp.is_writeable = True

                _sq_c_pgm_pj += _n_aqew___yp.to_bytes()
            

            if u_b__at__inv.tag is not None:
            
                t_p_t_v__x_o = Stream("__substg1.0_370A0102", u_b__at__inv.tag)
                _u___wzy_exl.directory_entries.append(t_p_t_v__x_o)

                ___xjrahl_pj = Property()
                ___xjrahl_pj.tag = 0x370A0102
                ___xjrahl_pj.type = PropertyType.BINARY
                ___xjrahl_pj.size = len(u_b__at__inv.tag)
                ___xjrahl_pj.is_readable = True
                ___xjrahl_pj.is_writeable = True

                _sq_c_pgm_pj += ___xjrahl_pj.to_bytes()
            

            if u_b__at__inv.transport_name is not None:
            
                _n__u___m_kb = u_b__at__inv.transport_name.encode(self.nsifr_q_er__)
                __zs___bkz_w = Stream("__substg1.0_370C" + self.m__zli___l_b, _n__u___m_kb)
                _u___wzy_exl.directory_entries.append(__zs___bkz_w)

                t_i__yz__v__ = Property()
                t_i__yz__v__.tag = 0x370C << 16 | self.wiqwtada__v_
                t_i__yz__v__.type = PropertyType.STRING_8
                t_i__yz__v__.size = len(_n__u___m_kb) + x_m_sky_gz__
                t_i__yz__v__.is_readable = True
                t_i__yz__v__.is_writeable = True

                _sq_c_pgm_pj += t_i__yz__v__.to_bytes()
            

            if u_b__at__inv.display_name is not None:
            
                __wb____mxat = u_b__at__inv.display_name.encode(self.nsifr_q_er__)
                au___tv___a_ = Stream("__substg1.0_3001" + self.m__zli___l_b, __wb____mxat)
                _u___wzy_exl.directory_entries.append(au___tv___a_)

                nb__opljqv__ = Property()
                nb__opljqv__.tag = 0x3001 << 16 | self.wiqwtada__v_
                nb__opljqv__.type = PropertyType.STRING_8
                nb__opljqv__.size = len(__wb____mxat) + x_m_sky_gz__
                nb__opljqv__.is_readable = True
                nb__opljqv__.is_writeable = True

                _sq_c_pgm_pj += nb__opljqv__.to_bytes()
            

            if u_b__at__inv.embedded_message is not None and u_b__at__inv.method != AttachmentMethod.OLE:
            
                ____og_qbc__ = u_b__at__inv.embedded_message.__tdra____oj(ou______p___)

                ____dv_tvo__ = Storage("__substg1.0_3701000D")

                ____dv_tvo__.directory_entries.extend(____og_qbc__)
                
                _u___wzy_exl.directory_entries.append(____dv_tvo__)

                _gizyp__j__e = Property()
                _gizyp__j__e.tag = 0x3701000D
                _gizyp__j__e.type = PropertyType.OBJECT
                _gizyp__j__e.size = 4_000_000_000
                _gizyp__j__e.is_readable = True
                _gizyp__j__e.is_writeable = True

                ___sr______f = bytearray(_gizyp__j__e.to_bytes())
                ___sr______f[12] = 1

                _sq_c_pgm_pj += ___sr______f
            

            if u_b__at__inv.object_type != ObjectType.NONE:
            
                o______jc_u_ = Property()
                o______jc_u_.tag = 0x0FFE0003
                o______jc_u_.type = PropertyType.INTEGER_32
                o______jc_u_.value = int.to_bytes(EnumUtil.parse_object_type(u_b__at__inv.object_type), 4, "little")
                o______jc_u_.is_readable = True
                o______jc_u_.is_writeable = True

                _sq_c_pgm_pj += o______jc_u_.to_bytes()
            

            if u_b__at__inv.is_hidden:
            
                gabuuneaq___ = Property()
                gabuuneaq___.tag = 0x7FFE000B
                gabuuneaq___.type = PropertyType.BOOLEAN
                gabuuneaq___.value = int.to_bytes(1, 1, "little")
                gabuuneaq___.is_readable = True
                gabuuneaq___.is_writeable = True

                _sq_c_pgm_pj += gabuuneaq___.to_bytes()
            

            if u_b__at__inv.is_contact_photo:
            
                _i___p___i__ = Property()
                _i___p___i__.tag = 0x7FFF000B
                _i___p___i__.type = PropertyType.BOOLEAN
                _i___p___i__.value = int.to_bytes(1, 1, "little")
                _i___p___i__.is_readable = True
                _i___p___i__.is_writeable = True

                _sq_c_pgm_pj += _i___p___i__.to_bytes()
            

            if u_b__at__inv.creation_time > datetime.datetime(1901,1,1):
            
                jgv__c_h___y = datetime.datetime(1601,1,1)
                _fi_km_v____ = int((u_b__at__inv.creation_time - jgv__c_h___y).total_seconds()) * 10_000_000

                du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

                mmbq__b_gylp = Property()
                mmbq__b_gylp.tag = 0x30070040
                mmbq__b_gylp.type = PropertyType.TIME
                mmbq__b_gylp.value = du___g__abr_
                mmbq__b_gylp.is_readable = True
                mmbq__b_gylp.is_writeable = False

                _sq_c_pgm_pj += mmbq__b_gylp.to_bytes()
            

            if u_b__at__inv.last_modification_time > datetime.datetime(1901,1,1):
            
                jgv__c_h___y = datetime.datetime(1601,1,1)
                _fi_km_v____ = int((u_b__at__inv.last_modification_time - jgv__c_h___y).total_seconds()) * 10_000_000

                du___g__abr_ = _fi_km_v____.to_bytes(8, "little")

                du___g__abr_ = int.to_bytes(_fi_km_v____, 8, "little")

                o_pkf_syr_jf = Property()
                o_pkf_syr_jf.tag = 0x30080040
                o_pkf_syr_jf.type = PropertyType.TIME
                o_pkf_syr_jf.value = du___g__abr_
                o_pkf_syr_jf.is_readable = True
                o_pkf_syr_jf.is_writeable = False

                _sq_c_pgm_pj += o_pkf_syr_jf.to_bytes()
            

            if u_b__at__inv.data_object_storage is not None and u_b__at__inv.method == AttachmentMethod.OLE:            
                _u___wzy_exl.directory_entries.append(u_b__at__inv.data_object_storage)
                _u___wzy_exl.directory_entries.append(u_b__at__inv.properties_stream)            
            else:            
                ___f_hzd____ = Stream("__properties_version1.0", bytes(_sq_c_pgm_pj))
                _u___wzy_exl.directory_entries.append(___f_hzd____)
            
            ___xv_ab__p_.append(_u___wzy_exl)

        return ___xv_ab__p_
            
    @staticmethod
    def x_t_w_mm____(id, _x_ono_wsf_e):
        if _x_ono_wsf_e is not None and len(_x_ono_wsf_e) == 16:

            _k__i_______ = int.from_bytes(_x_ono_wsf_e[0: 8], "little")
            ___bv_______ = int.from_bytes(_x_ono_wsf_e[8: 16], "little")

            _rdjx_____e_  = str(id) + "-" + str(_k__i_______) + "-" + str(___bv_______)

            return _rdjx_____e_
        else:
            return str(id)

    @staticmethod
    def _q_l_tivr__j(reply_to):

        t_z____unij_ = reply_to.split(';')
        l__i___n_i__ = bytearray()

        for i in range(len(t_z____unij_)):
            
            __onhw__b__q = bytes([0x00, 0x00, 0x00, 0x00, 0x81, 0x2B, 0x1F, 0xA4, 0xBE, 0xA3, 0x10, 0x19, 0x9D, 0x6E, 0x00, 0xDD, 0x01, 0x0F, 0x54, 0x02, 0x00, 0x00, 0x01, 0x80])

            _r_x__u__ik_ = (t_z____unij_[i] + "\0SMTP\0" + t_z____unij_[i] + "\0").encode("utf-16-le")
            jlkf__f__r_k = bytes([0x00, 0x00])

            q_____a_xj__ = len(__onhw__b__q) + len(_r_x__u__ik_)
            
            l__i___n_i__ += int.to_bytes(q_____a_xj__, 4, "little")
            l__i___n_i__ += __onhw__b__q
            l__i___n_i__ += _r_x__u__ik_
            l__i___n_i__ += jlkf__f__r_k

        k_nlj_____u_ = bytearray(8 + len(l__i___n_i__))

        e___i_u_wg__ = len(t_z____unij_)
        ___hz______t = len(k_nlj_____u_) - 8

        k_nlj_____u_[0:4] = int.to_bytes(e___i_u_wg__, 4, "little")
        k_nlj_____u_[4:8] = int.to_bytes(___hz______t, 4, "little")
        k_nlj_____u_[8:]  = l__i___n_i__[0:]

        return bytes(k_nlj_____u_)

    @staticmethod
    def svhh___rr___(yxqo__o_k_m_):

        q_h_u_rhzcz_ = "cp1252"

        ______zoq___ = yxqo__o_k_m_.find("ansicpg")

        if ______zoq___ > -1:

            __r_____b__h = yxqo__o_k_m_.find("\\", ______zoq___ + 7)

            if __r_____b__h > -1:
                
                ____hq______ = yxqo__o_k_m_[______zoq___ + 7: __r_____b__h]

                try:
                    uqk_rec_hb_d = int(____hq______)
                    q_h_u_rhzcz_ = Message.uw_u___c_l__(uqk_rec_hb_d)
                except:
                    pass


        return q_h_u_rhzcz_

    @staticmethod
    def ___gw__h_l__(q___s__q__v_, s__lzrk_stq_, _pm_h_m_____, s_s__p_d_r__):

        qcd____z__vn = q___s__q__v_[0: s_s__p_d_r__]
        __ov____dwms = _pm_h_m_____
        kv__tva_a_nn = -1

        for yhh_auu_pg__ in s__lzrk_stq_:

            h___ve___f__ = qcd____z__vn.rfind("\\" + yhh_auu_pg__)

            if h___ve___f__ > -1 and h___ve___f__ > kv__tva_a_nn:
                __ov____dwms = s__lzrk_stq_[yhh_auu_pg__] if s__lzrk_stq_[yhh_auu_pg__] is not None else _pm_h_m_____
                kv__tva_a_nn = h___ve___f__

        return __ov____dwms


    @staticmethod
    def m__txiz___q_(w_n_bk_nnowd):

        yxqo__o_k_m_ = ""

        try:
            yxqo__o_k_m_ = w_n_bk_nnowd.decode("utf_8")
        except:
            return (None, None)
                
        ___p___k_g_q = Message.svhh___rr___(yxqo__o_k_m_)
        s__lzrk_stq_ = Message.___a____n___(yxqo__o_k_m_)

        yxqo__o_k_m_ = yxqo__o_k_m_.replace("\n\r{", "{")
        
        q___s__q__v_ = None

        k_q____fb_ov = yxqo__o_k_m_.find("{\\*\\htmltag")

        if k_q____fb_ov > -1:

            q___s__q__v_ = yxqo__o_k_m_[k_q____fb_ov:]

            w__kd____d__ = q___s__q__v_.find("\\'")

            while w__kd____d__ > -1:

                __ov____dwms = Message.___gw__h_l__(q___s__q__v_, s__lzrk_stq_, ___p___k_g_q, w__kd____d__)
                
                ___zj__v_p_t = q___s__q__v_.find("\\'", w__kd____d__ + 2)
                c__p_zx__kia = None
                _oo_w______x = None

                try:

                    if ___zj__v_p_t == w__kd____d__ + 4:

                        c__p_zx__kia = q___s__q__v_[w__kd____d__: w__kd____d__ + 8]

                        ra__sdji___l = c__p_zx__kia[2: 4]
                        cnytq_ld__qu = c__p_zx__kia[6: 8]

                        _j_yy_p_____ = int(ra__sdji___l, 16)
                        _k_mm__fgd__ = int(cnytq_ld__qu, 16)

                        _oo_w______x = bytes([_j_yy_p_____, _k_mm__fgd__])

                    else:

                        c__p_zx__kia = q___s__q__v_[w__kd____d__: w__kd____d__ + 4]
                        ra__sdji___l = c__p_zx__kia[2:]
                        _j_yy_p_____ = int(ra__sdji___l, 16)                    
                        _oo_w______x = bytes([_j_yy_p_____])


                    if _oo_w______x is not None and c__p_zx__kia is not None:

                        _______vkpfy = _oo_w______x.decode(__ov____dwms)                  
                        q___s__q__v_ = q___s__q__v_.replace(c__p_zx__kia, _______vkpfy)


                except:
                    q___s__q__v_ = q___s__q__v_.replace(c__p_zx__kia, c__p_zx__kia[1:])

                w__kd____d__ = q___s__q__v_.find("\\'")

            ____k_i_ew_i = 0

            while ____k_i_ew_i > -1:

                ____k_i_ew_i = q___s__q__v_.find("{\\*\\htmltag", 0)

                if ____k_i_ew_i > -1:

                    x_cwm____wjw = q___s__q__v_.find("}", ____k_i_ew_i)
                    e_g_sitj__o_ = q___s__q__v_.find(" ", ____k_i_ew_i)
                    ___on____vmf = q___s__q__v_.find("<", ____k_i_ew_i)

                    if ___on____vmf > -1 and x_cwm____wjw > -1 and ___on____vmf < x_cwm____wjw and ___on____vmf < e_g_sitj__o_:

                        ____lr__q___ = q___s__q__v_[____k_i_ew_i: x_cwm____wjw]
                        rgt__a___csn = q___s__q__v_[___on____vmf: x_cwm____wjw]

                        q___s__q__v_ = q___s__q__v_.replace(____lr__q___, rgt__a___csn)

                    elif e_g_sitj__o_ > -1 and x_cwm____wjw > -1 and e_g_sitj__o_ < x_cwm____wjw:

                        ____lr__q___ = q___s__q__v_[____k_i_ew_i: x_cwm____wjw]
                        rgt__a___csn = q___s__q__v_[e_g_sitj__o_ + 1: x_cwm____wjw]

                        q___s__q__v_ = q___s__q__v_.replace(____lr__q___, rgt__a___csn)

                    else:
                        ____lr__q___ = q___s__q__v_[____k_i_ew_i: x_cwm____wjw]
                        q___s__q__v_ = q___s__q__v_.replace(____lr__q___, "")


            _mvgmc___cy_ = []

            _l__agl__n__ = 0
            _hz__lp___d_ = 0

            while _l__agl__n__ > -1 and _hz__lp___d_ > -1:

                _l__agl__n__ = q___s__q__v_.find("\\htmlrtf", _l__agl__n__)

                if _l__agl__n__ > -1:

                    _hz__lp___d_ = q___s__q__v_.find("\\htmlrtf0", _l__agl__n__)
                    _o_el_m_____ = q___s__q__v_.find("\\htmlrtf0 ", _l__agl__n__)

                    w_p_u_______ = 10 if _hz__lp___d_ == _o_el_m_____ else 9

                    if _hz__lp___d_ > -1:

                        _mvgmc___cy_.append(_l__agl__n__)
                        _mvgmc___cy_.append(_hz__lp___d_ + w_p_u_______)

                        _l__agl__n__ = _hz__lp___d_ + w_p_u_______

                else:
                    _hz__lp___d_ = -1

            _bni__nwbj_t = []

            ak_n_____kuf = 0

            for i in range(0, len(_mvgmc___cy_) - 1, 2):

                __e______jm_ = _mvgmc___cy_[i]
                __poi_b__e__ = _mvgmc___cy_[i + 1]
                _bni__nwbj_t.append(q___s__q__v_[ak_n_____kuf: __e______jm_])
                ak_n_____kuf = __poi_b__e__


            _bni__nwbj_t.append(q___s__q__v_[ak_n_____kuf: len(q___s__q__v_)])

            q___s__q__v_ = "".join(_bni__nwbj_t)

            _pq__v_m_bbl = []

            xsckq___ym__ = 0
            _______bke__ = 0

            while xsckq___ym__ > -1 and _______bke__ > -1:

                xsckq___ym__ = q___s__q__v_.find("{\\pntext", xsckq___ym__)

                if xsckq___ym__ > -1:

                    _______bke__ = q___s__q__v_.find("}", xsckq___ym__)

                    if _______bke__ > -1:

                        _pq__v_m_bbl.append(xsckq___ym__)
                        _pq__v_m_bbl.append(_______bke__ + 1)

                        xsckq___ym__ = _______bke__ + 1

                else:
                    _______bke__ = -1

            _bni__nwbj_t = []

            ak_n_____kuf = 0

            for i in  range(0, len(_pq__v_m_bbl) - 1, 2):
                
                __e______jm_ = _pq__v_m_bbl[i]
                __poi_b__e__ = _pq__v_m_bbl[i + 1]
                _bni__nwbj_t.append(q___s__q__v_[ak_n_____kuf: __e______jm_])
                ak_n_____kuf = __poi_b__e__


            _bni__nwbj_t.append(q___s__q__v_[ak_n_____kuf: len(q___s__q__v_)])

            q___s__q__v_ = "".join(_bni__nwbj_t)

            ird__m_rh_z_ = []

            h_g_bw___ei_ = q___s__q__v_.find("{\\*\\mhtmltag")
            _____q_f__vl = 0
            i__g_k_x____ = h_g_bw___ei_

            while h_g_bw___ei_ > -1:

                ___pv_f_____ = q___s__q__v_.find("{", i__g_k_x____ + 1)
                t_____jdtc_i = q___s__q__v_.find("}", i__g_k_x____ + 1)

                if t_____jdtc_i == -1:
                    break

                elif _____q_f__vl == 0 and (t_____jdtc_i < ___pv_f_____ or ___pv_f_____ == -1):

                    ird__m_rh_z_.append(h_g_bw___ei_)
                    ird__m_rh_z_.append(t_____jdtc_i)

                    i__g_k_x____ = t_____jdtc_i
                    h_g_bw___ei_ = q___s__q__v_.find("{\\*\\mhtmltag", i__g_k_x____ + 1)

                    i__g_k_x____ = h_g_bw___ei_

                elif _____q_f__vl > 0 and (t_____jdtc_i < ___pv_f_____ or ___pv_f_____ == -1):

                    _____q_f__vl -= 1
                    i__g_k_x____ = t_____jdtc_i

                elif ___pv_f_____ < t_____jdtc_i:

                    _____q_f__vl += 1
                    i__g_k_x____ = ___pv_f_____

            _bni__nwbj_t = []

            ak_n_____kuf = 0

            for i in range(0, len(ird__m_rh_z_) - 1, 2):

                __e______jm_ = ird__m_rh_z_[i]
                __poi_b__e__ = ird__m_rh_z_[i + 1]

                _bni__nwbj_t.append(q___s__q__v_[ak_n_____kuf: __e______jm_])

                ak_n_____kuf = __poi_b__e__

            _bni__nwbj_t.append(q___s__q__v_[ak_n_____kuf: len(q___s__q__v_)])

            q___s__q__v_ = "".join(_bni__nwbj_t)

            q___s__q__v_ = q___s__q__v_.replace("\\{", "{")
            q___s__q__v_ = q___s__q__v_.replace("\\}", "%x7D")
            q___s__q__v_ = q___s__q__v_.replace("}", "")
            q___s__q__v_ = q___s__q__v_.replace("%x7D", "}")
            q___s__q__v_ = q___s__q__v_.replace("\\\\", "\\")
            q___s__q__v_ = q___s__q__v_.replace("\\line", "")
            q___s__q__v_ = q___s__q__v_.replace("\\pard", "")
            q___s__q__v_ = q___s__q__v_.replace("\\par", "")
            q___s__q__v_ = q___s__q__v_.replace("\\tab", "\t")
            q___s__q__v_ = q___s__q__v_.replace("\\plain", "")
            q___s__q__v_ = q___s__q__v_.replace("\\fs20", "")
            q___s__q__v_ = q___s__q__v_.replace("\\f0", "")
            q___s__q__v_ = q___s__q__v_.replace("\\f4", "")
            q___s__q__v_ = q___s__q__v_.replace("\\f5", "")
            q___s__q__v_ = q___s__q__v_.replace("\\f6", "")
            q___s__q__v_ = q___s__q__v_.replace("\\objattph", "")
            q___s__q__v_ = q___s__q__v_.replace("\\li360", "")
            q___s__q__v_ = q___s__q__v_.replace("\\li720", "")
            q___s__q__v_ = q___s__q__v_.replace("\\li1440", "")
            q___s__q__v_ = q___s__q__v_.replace("\\li1080", "")
            q___s__q__v_ = q___s__q__v_.replace("\\fi-360", "")
            q___s__q__v_ = q___s__q__v_.replace("\\fi-720", "")
            q___s__q__v_ = q___s__q__v_.replace("\\rtlch", "")
            q___s__q__v_ = q___s__q__v_.replace("\\ltrch", "")
            q___s__q__v_ = q___s__q__v_.replace("\\sb100", "")
            q___s__q__v_ = q___s__q__v_.replace("\\intbl", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat1", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat2", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat3", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat4", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat5", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat6", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat7", "")
            q___s__q__v_ = q___s__q__v_.replace("\\cbpat8", "")
            q___s__q__v_ = q___s__q__v_.replace("\\sb90", "")
            q___s__q__v_ = q___s__q__v_.replace("\\sb150", "")
            q___s__q__v_ = q___s__q__v_.replace("\\sb240", "")
            q___s__q__v_ = q___s__q__v_.replace("\\sb280", "")
            q___s__q__v_ = q___s__q__v_.replace("\\qc", "")
            q___s__q__v_ = q___s__q__v_.replace("\\qr", "")
            q___s__q__v_ = q___s__q__v_.replace("\\ql", "")
            q___s__q__v_ = q___s__q__v_.replace("\\fs18", "")
            q___s__q__v_ = q___s__q__v_.replace("\\b0", "")
            q___s__q__v_ = q___s__q__v_.replace("\\b", "")
            q___s__q__v_ = q___s__q__v_.replace("\\protect", "")
            q___s__q__v_ = q___s__q__v_.replace("\\itap2", "")
            q___s__q__v_ = q___s__q__v_.replace("\\itap3", "")

            __y_tyuf___v = 0
            __w_z_n__u__ = 0

            while __y_tyuf___v > -1 and len(q___s__q__v_) > __w_z_n__u__:

                __y_tyuf___v = q___s__q__v_.find("\\u", __w_z_n__u__)

                if __y_tyuf___v > -1 and len(q___s__q__v_) >= __y_tyuf___v + 8:

                    s_b______ykx = q___s__q__v_[__y_tyuf___v: __y_tyuf___v + 8]
                    enes_x___h__ = s_b______ykx[2: 6]

                    try:
                        d_wqrtksq_k_ = str(enes_x___h__)
                        q___s__q__v_ = q___s__q__v_.replace(s_b______ykx, d_wqrtksq_k_)
                    except:
                        q___s__q__v_ = q___s__q__v_.replace(s_b______ykx, s_b______ykx[1:])

                    __w_z_n__u__ = __y_tyuf___v + 8

        return (q___s__q__v_, ___p___k_g_q)

    @staticmethod
    def __o____cc__q(__s_z__l___p):

        _rj_n_mr_z_q = "{\\rtf1\\ansi\\mac\\deff0\\deftab720{\\fonttbl;}{\\f0\\fnil \\froman \\fswiss \\fmodern \\fscript \\fdecor MS Sans SerifSymbolArialTimes New RomanCourier{\\colortbl\\red0\\green0\\blue0\n\r\\par \\pard\\plain\\f0\\fs20\\b\\i\\u\\tab\\tx"

        x_r___ey__l_ = _rj_n_mr_z_q.encode("ascii")

        _zdhjs_b_f__ = None
        __q___nk___e = 0
        pb_pz_vr_t_u = 0

        if __s_z__l___p is None or len(__s_z__l___p) < 16:
            raise Exception("Invalid PR_RTF_COMPRESSION header")

        ___y_ansc_tu = Message._t_hr____m__(__s_z__l___p, __q___nk___e)
        __q___nk___e += 4

        xc____s_sq_o = Message._t_hr____m__(__s_z__l___p, __q___nk___e)
        __q___nk___e += 4

        __u_rwnxj___ = Message._t_hr____m__(__s_z__l___p, __q___nk___e)
        __q___nk___e += 4

        n_pr____ntv_ = Message._t_hr____m__(__s_z__l___p, __q___nk___e)
        __q___nk___e += 4

        if ___y_ansc_tu != len(__s_z__l___p) - 4:
            return bytes(0)

        if __u_rwnxj___ == 0x414c454d:

            if xc____s_sq_o > len(__s_z__l___p) - __q___nk___e:
                xc____s_sq_o = len(__s_z__l___p) - __q___nk___e

            _zdhjs_b_f__ = __s_z__l___p[__q___nk___e: __q___nk___e + xc____s_sq_o]

        elif __u_rwnxj___ == 0x75465a4c: 
            _zdhjs_b_f__ = bytearray(len(x_r___ey__l_) + xc____s_sq_o)
            _zdhjs_b_f__[0: len(x_r___ey__l_)] = x_r___ey__l_
            pb_pz_vr_t_u = len(x_r___ey__l_)

            _o__lrk___l_ = 0
            tva__o_r__wh = 0

            while pb_pz_vr_t_u < len(_zdhjs_b_f__):

                if _o__lrk___l_ % 8 == 0:
                    tva__o_r__wh = Message.__rc_pn_tj_v(__s_z__l___p, __q___nk___e)
                    __q___nk___e += 1
                else:
                    tva__o_r__wh = tva__o_r__wh >> 1
                
                _o__lrk___l_ += 1

                if (tva__o_r__wh & 1) == 1:

                    __s_i___h_rk = Message.__rc_pn_tj_v(__s_z__l___p, __q___nk___e)
                    __q___nk___e += 1
                    
                    ___hz______t = Message.__rc_pn_tj_v(__s_z__l___p, __q___nk___e)
                    __q___nk___e += 1

                    __s_i___h_rk = (__s_i___h_rk << 4) | (___hz______t >> 4)
                    ___hz______t = (___hz______t & 0xF) + 2
                    __s_i___h_rk = int(pb_pz_vr_t_u / 4096) * 4096 + __s_i___h_rk

                    if __s_i___h_rk >= pb_pz_vr_t_u:
                        __s_i___h_rk -= 4096

                    s_s__p_d_r__ = __s_i___h_rk + ___hz______t

                    while __s_i___h_rk < s_s__p_d_r__:
                        
                        try:
                            _zdhjs_b_f__[pb_pz_vr_t_u] = _zdhjs_b_f__[__s_i___h_rk]
                            pb_pz_vr_t_u += 1
                            __s_i___h_rk += 1
                        except:
                            return bytes(0)
            
                else:
                    try:
                        _zdhjs_b_f__[pb_pz_vr_t_u] = __s_z__l___p[__q___nk___e]
                        pb_pz_vr_t_u += 1
                        __q___nk___e += 1
                    except:
                        return bytes(0)


            __s_z__l___p = _zdhjs_b_f__
            _zdhjs_b_f__ = __s_z__l___p[len(x_r___ey__l_): len(x_r___ey__l_) + xc____s_sq_o]

        else:
            raise Exception("Wrong magic number.")


        return _zdhjs_b_f__

    @staticmethod
    def ___a____n___(yxqo__o_k_m_):

        s__lzrk_stq_ = {}

        _f__a__tr__v = yxqo__o_k_m_.find("{\\fonttbl")

        if _f__a__tr__v > 0:

            s_s__p_d_r__ = yxqo__o_k_m_.find("}}", _f__a__tr__v)

            if s_s__p_d_r__ > 0:

                l___r_cr_i__ = yxqo__o_k_m_[_f__a__tr__v + 8: s_s__p_d_r__ + 8]
                ___ds____brz = l___r_cr_i__.splitlines()
                _h_wz_lx_rxh = ""

                for i in range(len(___ds____brz)):

                    _h_wz_lx_rxh = ___ds____brz[i]
                    ek_q_b_z_hnt = _h_wz_lx_rxh.find("{")

                    if ek_q_b_z_hnt > -1:

                        y_m____ww_ny = _h_wz_lx_rxh.find("}", ek_q_b_z_hnt)

                        if y_m____ww_ny > -1:

                            _h_wz_lx_rxh = _h_wz_lx_rxh[ek_q_b_z_hnt + 1: y_m____ww_ny]

                            m_v_k__fp___ = "".join(_h_wz_lx_rxh.split()).split('\\')

                            if len(m_v_k__fp___) > 1 and m_v_k__fp___[1].startswith("f"):

                                yhh_auu_pg__ = m_v_k__fp___[1]
                                _______ff___ = None

                                for i in range(2, len(m_v_k__fp___), 1):

                                    if m_v_k__fp___[i] == "fcharset128":
                                        _______ff___ = 'shift_jis'
                                    elif m_v_k__fp___[i] == "fcharset129":
                                        _______ff___ = 'cp949'
                                    elif m_v_k__fp___[i] == "fcharset134":
                                        _______ff___ = 'gb2312'
                                    elif m_v_k__fp___[i] == "fcharset136":
                                        _______ff___ = 'big5'
                                    elif m_v_k__fp___[i] == "fcharset161":
                                        _______ff___ = 'cp1253'
                                    elif m_v_k__fp___[i] == "fcharset162":
                                        _______ff___ = 'cp1254'
                                    elif m_v_k__fp___[i] == "fcharset163":
                                        _______ff___ = 'cp1258'
                                    elif m_v_k__fp___[i] == "fcharset177":
                                        _______ff___ = 'cp1255'
                                    elif m_v_k__fp___[i] == "fcharset178":
                                        _______ff___ = 'cp1256'
                                    elif m_v_k__fp___[i] == "fcharset186":
                                        _______ff___ = 'cp1257'
                                    elif m_v_k__fp___[i] == "fcharset204":
                                        _______ff___ = 'cp1251'
                                    elif m_v_k__fp___[i] == "fcharset222":
                                        _______ff___ = 'cp874'
                                    elif m_v_k__fp___[i] == "fcharset238":
                                        _______ff___ = 'cp1250'

                                if yhh_auu_pg__ not in s__lzrk_stq_:
                                    s__lzrk_stq_[yhh_auu_pg__] = _______ff___


        return s__lzrk_stq_

    @staticmethod
    def a_____gq_r__(ou______p___, _i_toah_o_y_):

        if len(ou______p___) == 0:
            return -1

        io__qc__k__t = False

        for i in range(len(ou______p___)):

            x____fbaft_v = ou______p___[i]

            if _i_toah_o_y_.name is not None and x____fbaft_v.name == _i_toah_o_y_.name:
                io__qc__k__t = True
            elif x____fbaft_v.id == _i_toah_o_y_.id and _i_toah_o_y_.type == NamedPropertyType.NUMERICAL:
                io__qc__k__t = True

            if io__qc__k__t:

                _______e_bk_ = True

                if x____fbaft_v.guid is not None and _i_toah_o_y_.guid is not None and len(x____fbaft_v.guid) == len(_i_toah_o_y_.guid):

                    for j in range(len(x____fbaft_v.guid)):

                        if x____fbaft_v.guid[j] != _i_toah_o_y_.guid[j]:
                            _______e_bk_ = False

                else:
                    _______e_bk_ = False

                if _______e_bk_:
                    return i

        return -1

    @staticmethod
    def _bo_e__n___q(value, type, encoding):

        if value is None and (type == PropertyType.STRING or type == PropertyType.STRING_8):
            return 1
        elif value is not None and (type == PropertyType.STRING or type == PropertyType.STRING_8):
            return len(value) + len("\0".encode(encoding))
        elif value is None:
            return 0
        else:
            return len(value)

    @staticmethod
    def lcuthwob___r(ad__________, _jte_gt____a):

        if ad__________ is not None:

            for l in range(len(_jte_gt____a)):

                _z_v__k___gm = _jte_gt____a[l]
                _xrt_oj__g_s = True

                for i in range(16):
                
                    if ad__________[i] != _z_v__k___gm[i]:
                        _xrt_oj__g_s = False
                        break

                if _xrt_oj__g_s:
                    return l

        return -1  

    @staticmethod
    def ___wg___smt_(type):

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
    def _ghfeuhr____(code_page):

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
    def v_____omf__x(utc_datetime):
        offset = datetime.datetime.fromtimestamp(utc_datetime.timestamp()) - datetime.datetime.utcfromtimestamp(utc_datetime.timestamp())
        return utc_datetime + offset   

    @staticmethod
    def __u_cjujm___(value):
        return (value & 0x8000) | (value & 0x7fff)

    @staticmethod
    def __rc_pn_tj_v(buf, offset):
        return buf[offset] & 0xFF

    @staticmethod
    def _ulyl_q_w__s(b1, b2):
        return ((b1 & 0xFF) | ((b2 & 0xFF) << 8)) & 0xFFFF

    @staticmethod
    def _t_hr____m__(buf, offset):
        return ((buf[offset] & 0xFF) | ((buf[offset + 1] & 0xFF) << 8) | ((buf[offset + 2] & 0xFF) << 16) | ((buf[offset + 3] & 0xFF) << 24)) & 0x00000000FFFFFFFF

    def to_bytes(self):
        return self.p_zygsk___y_()

    def to_bytes(self):
        return self.__y_yb____hm()

    def save(self, file_path):

        if(file_path is not None):
            file = open(file_path, "wb")
            file.write(self.to_bytes())
            file.close

    @property
    def body_rtf(self):

        if self._h_b_v_d____ is not None and len(self._h_b_v_d____) > 0:
            return Message.__o____cc__q(self._h_b_v_d____)
        else:
            return None

    @body_rtf.setter
    def body_rtf(self, value):
        
        if value is not None:

            l__i___n_i__ = bytearray()
           
            l__i___n_i__.append(int.to_bytes(len(value) + 12, 4, "little"))
            l__i___n_i__.append(int.to_bytes(len(value), 4, "little"))
            l__i___n_i__.append(int.to_bytes(0x414c454d, 4, "little"))

            ____ffj__m_a = Crc()
            ____ffj__m_a.update(value)

            l__i___n_i__.append(____ffj__m_a.value)
            l__i___n_i__.append(value)

            self._h_b_v_d____ = bytes(l__i___n_i__)
            self.___g_ta__tfn = True

    @property
    def body_html(self):

        if self.zpz__r____ji is None and self._h_b_v_d____ is not None and len(self._h_b_v_d____) > 0:

            d____l_h__ro = Message.__o____cc__q(self._h_b_v_d____)
            
            q___s__q__v_, ___p___k_g_q = Message.m__txiz___q_(d____l_h__ro)

            if q___s__q__v_ is not None:
                return q___s__q__v_.encode("utf_8")
            else:
                return None

        else:
            return self.zpz__r____ji

    @body_html.setter
    def body_html(self, value):
        self.zpz__r____ji = value

    @property
    def body_html_text(self):

        if self.zpz__r____ji is not None:
            
            if self._x_____y___i > 0:

                goyi_s_ia_s_ = Message.uw_u___c_l__(self._x_____y___i)

                __z_s_f_lu__ = self.zpz__r____ji.decode(goyi_s_ia_s_)

                return __z_s_f_lu__

            else:

                __z_s_f_lu__ = self.zpz__r____ji.decode("utf_8")

                return __z_s_f_lu__

        else:

            k______kdt__ = self.body_rtf

            if k______kdt__ is not None and len(k______kdt__) > 0:

                q___s__q__v_, ___p___k_g_q = Message.m__txiz___q_(k______kdt__)

                if q___s__q__v_ is not None:
                    return q___s__q__v_.encode("utf_8")
                else:
                    return None  

            return None

    @body_html_text.setter
    def body_html_text(self, value):

        if value is not None:
            self.zpz__r____ji = value.encode("utf_8")

    @property
    def property_table(self):
        return self.lh_______ysy

    @property_table.setter
    def property_table(self, value):
        self.lh_______ysy = value

    @property
    def message_class(self):
        return self._pq_o______n

    @message_class.setter
    def message_class(self, value):
        self._pq_o______n = value

    @property
    def subject(self):
        return self._xv_y___o___

    @subject.setter
    def subject(self, value):
        self._xv_y___o___ = value

    @property
    def subject_prefix(self):
        return self._u__q__z___b

    @subject_prefix.setter
    def subject_prefix(self, value):
        self._u__q__z___b = value

    @property
    def conversation_topic(self):
        return self._rz_mvr_yf_p

    @conversation_topic.setter
    def conversation_topic(self, value):
        self._rz_mvr_yf_p = value

    @property
    def display_bcc(self):
        return self.f_pfu__g_o_p

    @display_bcc.setter
    def display_bcc(self, value):
        self.f_pfu__g_o_p = value

    @property
    def display_cc(self):
        return self._nfg_ljsz_d_

    @display_cc.setter
    def display_cc(self, value):
        self._nfg_ljsz_d_ = value

    @property
    def display_to(self):
        return self.v_xe_s_yi_bp

    @display_to.setter
    def display_to(self, value):
        self.v_xe_s_yi_bp = value

    @property
    def original_display_to(self):
        return self.p_j_________

    @original_display_to.setter
    def original_display_to(self, value):
        self.p_j_________ = value

    @property
    def reply_to(self):
        return self.na___bd__o_a

    @reply_to.setter
    def reply_to(self, value):
        self.na___bd__o_a = value

    @property
    def normalized_subject(self):
        return self.d_w____xbnru

    @normalized_subject.setter
    def normalized_subject(self, value):
        self.d_w____xbnru = value

    @property
    def body(self):
        return self.____y_gej_ly

    @body.setter
    def body(self, value):
        self.____y_gej_ly = value

    @property
    def rtf_compressed(self):
        return self._h_b_v_d____

    @rtf_compressed.setter
    def rtf_compressed(self, value):
        self._h_b_v_d____ = value

    @property
    def search_key(self):
        return self.__i___m_ncy_

    @search_key.setter
    def search_key(self, value):
        self.__i___m_ncy_ = value

    @property
    def change_key(self):
        return self.fhgy_b_an_h_

    @change_key.setter
    def change_key(self, value):
        self.fhgy_b_an_h_ = value

    @property
    def entry_id(self):
        return self.__j__stw_l_u

    @entry_id.setter
    def entry_id(self, value):
        self.__j__stw_l_u = value

    @property
    def read_receipt_entry_id(self):
        return self.___k________

    @read_receipt_entry_id.setter
    def read_receipt_entry_id(self, value):
        self.___k________ = value

    @property
    def read_receipt_search_key(self):
        return self.vbn_jd_xc_c_

    @read_receipt_search_key.setter
    def read_receipt_search_key(self, value):
        self.vbn_jd_xc_c_ = value

    @property
    def creation_time(self):
        return self.__v_r_____n_

    @creation_time.setter
    def creation_time(self, value):
        self.__v_r_____n_ = value

    @property
    def last_modification_time(self):
        return self._onw__vy_til

    @last_modification_time.setter
    def last_modification_time(self, value):
        self._onw__vy_til = value

    @property
    def message_delivery_time(self):
        return self.p__ia_c_i_i_

    @message_delivery_time.setter
    def message_delivery_time(self, value):
        self.p__ia_c_i_i_ = value

    @property
    def client_submit_time(self):
        return self.o_d_dh_dp_z_

    @client_submit_time.setter
    def client_submit_time(self, value):
        self.o_d_dh_dp_z_ = value

    @property
    def deferred_delivery_time(self):
        return self._____ngk_oi_

    @deferred_delivery_time.setter
    def deferred_delivery_time(self, value):
        self._____ngk_oi_ = value

    @property
    def provider_submit_time(self):
        return self._anq_obd_oq_

    @provider_submit_time.setter
    def provider_submit_time(self, value):
        self._anq_obd_oq_ = value

    @property
    def report_time(self):
        return self.tl_tqbr__xyq

    @report_time.setter
    def report_time(self, value):
        self.tl_tqbr__xyq = value

    @property
    def report_text(self):
        return self.twqm_____n_r

    @report_text.setter
    def report_text(self, value):
        self.twqm_____n_r = value

    @property
    def creator_name(self):
        return self.____y_kuq__q

    @creator_name.setter
    def creator_name(self, value):
        self.____y_kuq__q = value

    @property
    def last_modifier_name(self):
        return self.___zp_upib__

    @last_modifier_name.setter
    def last_modifier_name(self, value):
        self.___zp_upib__ = value

    @property
    def internet_message_id(self):
        return self.____w_h_sni_

    @internet_message_id.setter
    def internet_message_id(self, value):
        self.____w_h_sni_ = value

    @property
    def in_reply_to(self):
        return self._______eft__

    @in_reply_to.setter
    def in_reply_to(self, value):
        self._______eft__ = value

    @property
    def internet_references(self):
        return self._fio_i_c_few

    @internet_references.setter
    def internet_references(self, value):
        self._fio_i_c_few = value

    @property
    def message_code_page(self):
        return self.juou_jp_axl_

    @message_code_page.setter
    def message_code_page(self, value):
        self.juou_jp_axl_ = value

    @property
    def icon_index(self):
        return self.kw_x_qi_w_s_

    @icon_index.setter
    def icon_index(self, value):
        self.kw_x_qi_w_s_ = value

    @property
    def message_size(self):
        return self.d__m___n____

    @message_size.setter
    def message_size(self, value):
        self.d__m___n____ = value

    @property
    def internet_code_page(self):
        return self._x_____y___i

    @internet_code_page.setter
    def internet_code_page(self, value):
        self._x_____y___i = value

    @property
    def conversation_index(self):
        return self.k_kt_xqc____

    @conversation_index.setter
    def conversation_index(self, value):
        self.k_kt_xqc____ = value

    @property
    def is_hidden(self):
        return self.o__ic_zjug_e

    @is_hidden.setter
    def is_hidden(self, value):
        self.o__ic_zjug_e = value

    @property
    def is_read_only(self):
        return self.__kpffcnr___

    @is_read_only.setter
    def is_read_only(self, value):
        self.__kpffcnr___ = value

    @property
    def is_system(self):
        return self.we__f_y__hbo

    @is_system.setter
    def is_system(self, value):
        self.we__f_y__hbo = value

    @property
    def disable_full_fidelity(self):
        return self.xa_____a___v

    @disable_full_fidelity.setter
    def disable_full_fidelity(self, value):
        self.xa_____a___v = value

    @property
    def has_attachment(self):
        return self.__le______q_

    @has_attachment.setter
    def has_attachment(self, value):
        self.__le______q_ = value

    @property
    def rtf_in_sync(self):
        return self.___g_ta__tfn

    @rtf_in_sync.setter
    def rtf_in_sync(self, value):
        self.___g_ta__tfn = value

    @property
    def read_receipt_requested(self):
        return self.sg_____x____

    @read_receipt_requested.setter
    def read_receipt_requested(self, value):
        self.sg_____x____ = value

    @property
    def delivery_report_requested(self):
        return self._vhmwqhr__cd

    @delivery_report_requested.setter
    def delivery_report_requested(self, value):
        self._vhmwqhr__cd = value

    @property
    def sensitivity(self):
        return self.___wh_qn____

    @sensitivity.setter
    def sensitivity(self, value):
        self.___wh_qn____ = value

    @property
    def importance(self):
        return self._b_ue__y_z__

    @importance.setter
    def importance(self, value):
        self._b_ue__y_z__ = value

    @property
    def priority(self):
        return self._ci_____r_uk

    @priority.setter
    def priority(self, value):
        self._ci_____r_uk = value

    @property
    def flag_icon(self):
        return self.w__hc___o___

    @flag_icon.setter
    def flag_icon(self, value):
        self.w__hc___o___ = value

    @property
    def flag_status(self):
        return self._b_a_v___hjn

    @flag_status.setter
    def flag_status(self, value):
        self._b_a_v___hjn = value

    @property
    def object_type(self):
        return self.v___w_dliib_

    @object_type.setter
    def object_type(self, value):
        self.v___w_dliib_ = value

    @property
    def received_representing_address_type(self):
        return self._vry_n_v_d_g

    @received_representing_address_type.setter
    def received_representing_address_type(self, value):
        self._vry_n_v_d_g = value

    @property
    def received_representing_email_address(self):
        return self.___x_ry__twg

    @received_representing_email_address.setter
    def received_representing_email_address(self, value):
        self.___x_ry__twg = value

    @property
    def received_representing_entry_id(self):
        return self.___h_____oo_

    @received_representing_entry_id.setter
    def received_representing_entry_id(self, value):
        self.___h_____oo_ = value

    @property
    def received_representing_name(self):
        return self.b_o_l__vz__j

    @received_representing_name.setter
    def received_representing_name(self, value):
        self.b_o_l__vz__j = value

    @property
    def received_representing_search_key(self):
        return self.ehp_zo_hnnk_

    @received_representing_search_key.setter
    def received_representing_search_key(self, value):
        self.ehp_zo_hnnk_ = value

    @property
    def received_by_address_type(self):
        return self._k__vn_qvf__

    @received_by_address_type.setter
    def received_by_address_type(self, value):
        self._k__vn_qvf__ = value

    @property
    def received_by_email_address(self):
        return self._x___qkj___e

    @received_by_email_address.setter
    def received_by_email_address(self, value):
        self._x___qkj___e = value

    @property
    def received_by_entry_id(self):
        return self.__ynoc______

    @received_by_entry_id.setter
    def received_by_entry_id(self, value):
        self.__ynoc______ = value

    @property
    def received_by_name(self):
        return self.nn__l___z_p_

    @received_by_name.setter
    def received_by_name(self, value):
        self.nn__l___z_p_ = value

    @property
    def received_by_search_key(self):
        return self.d_vn__f____i

    @received_by_search_key.setter
    def received_by_search_key(self, value):
        self.d_vn__f____i = value

    @property
    def sender_address_type(self):
        return self.t___f_____hz

    @sender_address_type.setter
    def sender_address_type(self, value):
        self.t___f_____hz = value

    @property
    def sender_email_address(self):
        return self.__rfliczcge_

    @sender_email_address.setter
    def sender_email_address(self, value):
        self.__rfliczcge_ = value

    @property
    def sender_smtp_address(self):
        return self.______qcsd_d

    @sender_smtp_address.setter
    def sender_smtp_address(self, value):
        self.______qcsd_d = value

    @property
    def sender_entry_id(self):
        return self.insn_u______

    @sender_entry_id.setter
    def sender_entry_id(self, value):
        self.insn_u______ = value

    @property
    def sender_name(self):
        return self.v_x__v____fh

    @sender_name.setter
    def sender_name(self, value):
        self.v_x__v____fh = value

    @property
    def sender_search_key(self):
        return self._a__y_vf_eib

    @sender_search_key.setter
    def sender_search_key(self, value):
        self._a__y_vf_eib = value

    @property
    def sent_representing_address_type(self):
        return self.xep__h_t__f_

    @sent_representing_address_type.setter
    def sent_representing_address_type(self, value):
        self.xep__h_t__f_ = value

    @property
    def sent_representing_email_address(self):
        return self._w_tq___xpkm

    @sent_representing_email_address.setter
    def sent_representing_email_address(self, value):
        self._w_tq___xpkm = value

    @property
    def sent_representing_smtp_address(self):
        return self.__tl__v__h__

    @sent_representing_smtp_address.setter
    def sent_representing_smtp_address(self, value):
        self.__tl__v__h__ = value

    @property
    def sent_representing_entry_id(self):
        return self.rle_hef_uum_

    @sent_representing_entry_id.setter
    def sent_representing_entry_id(self, value):
        self.rle_hef_uum_ = value

    @property
    def sent_representing_name(self):
        return self.____d_yy__gy

    @sent_representing_name.setter
    def sent_representing_name(self, value):
        self.____d_yy__gy = value

    @property
    def sent_representing_search_key(self):
        return self._fb_znz_lkv_

    @sent_representing_search_key.setter
    def sent_representing_search_key(self, value):
        self._fb_znz_lkv_ = value

    @property
    def transport_message_headers(self):
        return self.__z__nhb_s__

    @transport_message_headers.setter
    def transport_message_headers(self, value):
        self.__z__nhb_s__ = value

    @property
    def last_verb_execution_time(self):
        return self.om____q_____

    @last_verb_execution_time.setter
    def last_verb_execution_time(self, value):
        self.om____q_____ = value

    @property
    def last_verb_executed(self):
        return self._ox_qg_e____

    @last_verb_executed.setter
    def last_verb_executed(self, value):
        self._ox_qg_e____ = value

    @property
    def message_flags(self):
        return self.c______ny_uq

    @message_flags.setter
    def message_flags(self, value):
        self.c______ny_uq = value

    @property
    def store_support_masks(self):
        return self._y__ti__u__a

    @store_support_masks.setter
    def store_support_masks(self, value):
        self._y__ti__u__a = value

    @property
    def outlook_version(self):
        return self.__naz_____bg

    @outlook_version.setter
    def outlook_version(self, value):
        self.__naz_____bg = value

    @property
    def outlook_internal_version(self):
        return self.ikw_q___t_ck

    @outlook_internal_version.setter
    def outlook_internal_version(self, value):
        self.ikw_q___t_ck = value

    @property
    def common_start_time(self):
        return self.u_wj__bz__ue

    @common_start_time.setter
    def common_start_time(self, value):
        self.u_wj__bz__ue = value

    @property
    def common_end_time(self):
        return self._pcg__fmli__

    @common_end_time.setter
    def common_end_time(self, value):
        self._pcg__fmli__ = value

    @property
    def flag_due_by(self):
        return self.w__j_w______

    @flag_due_by.setter
    def flag_due_by(self, value):
        self.w__j_w______ = value

    @property
    def is_recurring(self):
        return self.__bbqh_x____

    @is_recurring.setter
    def is_recurring(self, value):
        self.__bbqh_x____ = value

    @property
    def reminder_time(self):
        return self._______vx_ok

    @reminder_time.setter
    def reminder_time(self, value):
        self._______vx_ok = value

    @property
    def reminder_minutes_before_start(self):
        return self.__qhz__ecaho

    @reminder_minutes_before_start.setter
    def reminder_minutes_before_start(self, value):
        self.__qhz__ecaho = value

    @property
    def companies(self):
        return self.lb_im_l__ptk

    @companies.setter
    def companies(self, value):
        self.lb_im_l__ptk = value

    @property
    def contact_names(self):
        return self._____kd_o_cn

    @contact_names.setter
    def contact_names(self, value):
        self._____kd_o_cn = value

    @property
    def keywords(self):
        return self._mk___k_rw_y

    @keywords.setter
    def keywords(self, value):
        self._mk___k_rw_y = value

    @property
    def billing_information(self):
        return self.giyc___g__o_

    @billing_information.setter
    def billing_information(self, value):
        self.giyc___g__o_ = value

    @property
    def mileage(self):
        return self._t__expt_i_d

    @mileage.setter
    def mileage(self, value):
        self._t__expt_i_d = value

    @property
    def reminder_sound_file(self):
        return self.____za___j_w

    @reminder_sound_file.setter
    def reminder_sound_file(self, value):
        self.____za___j_w = value

    @property
    def is_private(self):
        return self._st_____rh_q

    @is_private.setter
    def is_private(self, value):
        self._st_____rh_q = value

    @property
    def is_reminder_set(self):
        return self._ca___k_ub_x

    @is_reminder_set.setter
    def is_reminder_set(self, value):
        self._ca___k_ub_x = value

    @property
    def reminder_override_default(self):
        return self._o__________

    @reminder_override_default.setter
    def reminder_override_default(self, value):
        self._o__________ = value

    @property
    def reminder_play_sound(self):
        return self.r____dmo__a_

    @reminder_play_sound.setter
    def reminder_play_sound(self, value):
        self.r____dmo__a_ = value

    @property
    def internet_account_name(self):
        return self._et__ia_vcjd

    @internet_account_name.setter
    def internet_account_name(self, value):
        self._et__ia_vcjd = value

    @property
    def appointment_start_time(self):
        return self.cq_m_axum___

    @appointment_start_time.setter
    def appointment_start_time(self, value):
        self.cq_m_axum___ = value

    @property
    def appointment_end_time(self):
        return self.zr___i__g_q_

    @appointment_end_time.setter
    def appointment_end_time(self, value):
        self.zr___i__g_q_ = value

    @property
    def is_all_day_event(self):
        return self._mr_j__yp__f

    @is_all_day_event.setter
    def is_all_day_event(self, value):
        self._mr_j__yp__f = value

    @property
    def location(self):
        return self.w_yd__qc_q__

    @location.setter
    def location(self, value):
        self.w_yd__qc_q__ = value

    @property
    def busy_status(self):
        return self.yl__e__fnwt_

    @busy_status.setter
    def busy_status(self, value):
        self.yl__e__fnwt_ = value

    @property
    def meeting_status(self):
        return self.__w_uoq___s_

    @meeting_status.setter
    def meeting_status(self, value):
        self.__w_uoq___s_ = value

    @property
    def response_status(self):
        return self.____f_kom_m_

    @response_status.setter
    def response_status(self, value):
        self.____f_kom_m_ = value

    @property
    def recurrence_type(self):
        return self.___utdtdt_yw

    @recurrence_type.setter
    def recurrence_type(self, value):
        self.___utdtdt_yw = value

    @property
    def appointment_message_class(self):
        return self.h_o_z_mo_h__

    @appointment_message_class.setter
    def appointment_message_class(self, value):
        self.h_o_z_mo_h__ = value

    @property
    def time_zone(self):
        return self._____egyzai_

    @time_zone.setter
    def time_zone(self, value):
        self._____egyzai_ = value

    @property
    def recurrence_pattern_description(self):
        return self._vs_t_ntls_l

    @recurrence_pattern_description.setter
    def recurrence_pattern_description(self, value):
        self._vs_t_ntls_l = value

    @property
    def recurrence_pattern(self):
        return self._s_egzvgujz_

    @recurrence_pattern.setter
    def recurrence_pattern(self, value):
        self._s_egzvgujz_ = value

    @property
    def guid(self):
        return self._oi___li_yx_

    @guid.setter
    def guid(self, value):
        self._oi___li_yx_ = value

    @property
    def label(self):
        return self.ls_m_lek_i_c

    @label.setter
    def label(self, value):
        self.ls_m_lek_i_c = value

    @property
    def duration(self):
        return self.j__vi__y_vh_

    @duration.setter
    def duration(self, value):
        self.j__vi__y_vh_ = value

    @property
    def task_start_date(self):
        return self.kn_va_____zr

    @task_start_date.setter
    def task_start_date(self, value):
        self.kn_va_____zr = value

    @property
    def task_due_date(self):
        return self.drg_hha_bdef

    @task_due_date.setter
    def task_due_date(self, value):
        self.drg_hha_bdef = value

    @property
    def owner(self):
        return self.ug__bxm__u__

    @owner.setter
    def owner(self, value):
        self.ug__bxm__u__ = value

    @property
    def delegator(self):
        return self._dznn_vo__f_

    @delegator.setter
    def delegator(self, value):
        self._dznn_vo__f_ = value

    @property
    def percent_complete(self):
        return self.cw_z___z____

    @percent_complete.setter
    def percent_complete(self, value):
        self.cw_z___z____ = value

    @property
    def actual_work(self):
        return self.__c_q_q____g

    @actual_work.setter
    def actual_work(self, value):
        self.__c_q_q____g = value

    @property
    def total_work(self):
        return self.kk____qaf_je

    @total_work.setter
    def total_work(self, value):
        self.kk____qaf_je = value

    @property
    def is_team_task(self):
        return self.hd____j__j__

    @is_team_task.setter
    def is_team_task(self, value):
        self.hd____j__j__ = value

    @property
    def is_complete(self):
        return self.__gn_p___y__

    @is_complete.setter
    def is_complete(self, value):
        self.__gn_p___y__ = value

    @property
    def date_completed(self):
        return self._il_______cr

    @date_completed.setter
    def date_completed(self, value):
        self._il_______cr = value

    @property
    def task_status(self):
        return self.____ueit___l

    @task_status.setter
    def task_status(self, value):
        self.____ueit___l = value

    @property
    def task_ownership(self):
        return self.p__f_s_____t

    @task_ownership.setter
    def task_ownership(self, value):
        self.p__f_s_____t = value

    @property
    def task_delegation_state(self):
        return self._c__v___wqqb

    @task_delegation_state.setter
    def task_delegation_state(self, value):
        self._c__v___wqqb = value

    @property
    def note_width(self):
        return self.g__tp___yb__

    @note_width.setter
    def note_width(self, value):
        self.g__tp___yb__ = value

    @property
    def note_height(self):
        return self.qi______kjo_

    @note_height.setter
    def note_height(self, value):
        self.qi______kjo_ = value

    @property
    def note_left(self):
        return self.__no__s_vsl_

    @note_left.setter
    def note_left(self, value):
        self.__no__s_vsl_ = value

    @property
    def note_top(self):
        return self.om_u__xna_q_

    @note_top.setter
    def note_top(self, value):
        self.om_u__xna_q_ = value

    @property
    def note_color(self):
        return self.j____bexpm__

    @note_color.setter
    def note_color(self, value):
        self.j____bexpm__ = value

    @property
    def journal_start_time(self):
        return self.__i_b_kq_iap

    @journal_start_time.setter
    def journal_start_time(self, value):
        self.__i_b_kq_iap = value

    @property
    def journal_end_time(self):
        return self.rq__k____jkt

    @journal_end_time.setter
    def journal_end_time(self, value):
        self.rq__k____jkt = value

    @property
    def journal_type(self):
        return self._s______z_yx

    @journal_type.setter
    def journal_type(self, value):
        self._s______z_yx = value

    @property
    def journal_type_description(self):
        return self.va_uignshqy_

    @journal_type_description.setter
    def journal_type_description(self, value):
        self.va_uignshqy_ = value

    @property
    def journal_duration(self):
        return self._jnlqe_____v

    @journal_duration.setter
    def journal_duration(self, value):
        self._jnlqe_____v = value

    @property
    def birthday(self):
        return self.hsu__s____k_

    @birthday.setter
    def birthday(self, value):
        self.hsu__s____k_ = value

    @property
    def children_names(self):
        return self._v__e__f____

    @children_names.setter
    def children_names(self, value):
        self._v__e__f____ = value

    @property
    def assistent_name(self):
        return self.m__vg_n__ze_

    @assistent_name.setter
    def assistent_name(self, value):
        self.m__vg_n__ze_ = value

    @property
    def assistent_phone(self):
        return self.__x_____x__h

    @assistent_phone.setter
    def assistent_phone(self, value):
        self.__x_____x__h = value

    @property
    def business_phone(self):
        return self.h_w_j_lt_u_n

    @business_phone.setter
    def business_phone(self, value):
        self.h_w_j_lt_u_n = value

    @property
    def business_phone2(self):
        return self.t__w_nqk____

    @business_phone2.setter
    def business_phone2(self, value):
        self.t__w_nqk____ = value

    @property
    def business_fax(self):
        return self.__rom_q__nzu

    @business_fax.setter
    def business_fax(self, value):
        self.__rom_q__nzu = value

    @property
    def business_home_page(self):
        return self.h_a_x____w_j

    @business_home_page.setter
    def business_home_page(self, value):
        self.h_a_x____w_j = value

    @property
    def callback_phone(self):
        return self.ul_l_qtt___p

    @callback_phone.setter
    def callback_phone(self, value):
        self.ul_l_qtt___p = value

    @property
    def car_phone(self):
        return self.__m__tcaw___

    @car_phone.setter
    def car_phone(self, value):
        self.__m__tcaw___ = value

    @property
    def cellular_phone(self):
        return self.owjw_l_is_fs

    @cellular_phone.setter
    def cellular_phone(self, value):
        self.owjw_l_is_fs = value

    @property
    def company_main_phone(self):
        return self.____v__n___r

    @company_main_phone.setter
    def company_main_phone(self, value):
        self.____v__n___r = value

    @property
    def company_name(self):
        return self.e_s_i__m____

    @company_name.setter
    def company_name(self, value):
        self.e_s_i__m____ = value

    @property
    def computer_network_name(self):
        return self.______rz___k

    @computer_network_name.setter
    def computer_network_name(self, value):
        self.______rz___k = value

    @property
    def customer_id(self):
        return self._____li__w__

    @customer_id.setter
    def customer_id(self, value):
        self._____li__w__ = value

    @property
    def department_name(self):
        return self.hgsi_u__j__v

    @department_name.setter
    def department_name(self, value):
        self.hgsi_u__j__v = value

    @property
    def display_name(self):
        return self.__j___op_s__

    @display_name.setter
    def display_name(self, value):
        self.__j___op_s__ = value

    @property
    def display_name_prefix(self):
        return self._pudmbn_y_qy

    @display_name_prefix.setter
    def display_name_prefix(self, value):
        self._pudmbn_y_qy = value

    @property
    def ftp_site(self):
        return self._x_b_d_u__hg

    @ftp_site.setter
    def ftp_site(self, value):
        self._x_b_d_u__hg = value

    @property
    def generation(self):
        return self.gd_n__q___qg

    @generation.setter
    def generation(self, value):
        self.gd_n__q___qg = value

    @property
    def given_name(self):
        return self._ks__k_____f

    @given_name.setter
    def given_name(self, value):
        self._ks__k_____f = value

    @property
    def government_id(self):
        return self.tb_____r_t__

    @government_id.setter
    def government_id(self, value):
        self.tb_____r_t__ = value

    @property
    def hobbies(self):
        return self.________zntw

    @hobbies.setter
    def hobbies(self, value):
        self.________zntw = value

    @property
    def home_phone2(self):
        return self.__rvw_yhfi_g

    @home_phone2.setter
    def home_phone2(self, value):
        self.__rvw_yhfi_g = value

    @property
    def home_address_city(self):
        return self.__y_____aw__

    @home_address_city.setter
    def home_address_city(self, value):
        self.__y_____aw__ = value

    @property
    def home_address_country(self):
        return self._____lc_g_h_

    @home_address_country.setter
    def home_address_country(self, value):
        self._____lc_g_h_ = value

    @property
    def home_address_postal_code(self):
        return self.d__ol_f_a_i_

    @home_address_postal_code.setter
    def home_address_postal_code(self, value):
        self.d__ol_f_a_i_ = value

    @property
    def home_address_post_office_box(self):
        return self.__xc__e_i___

    @home_address_post_office_box.setter
    def home_address_post_office_box(self, value):
        self.__xc__e_i___ = value

    @property
    def home_address_state(self):
        return self.v_s____jaf__

    @home_address_state.setter
    def home_address_state(self, value):
        self.v_s____jaf__ = value

    @property
    def home_address_street(self):
        return self.___h_r__f_d_

    @home_address_street.setter
    def home_address_street(self, value):
        self.___h_r__f_d_ = value

    @property
    def home_fax(self):
        return self.w___u___r_fm

    @home_fax.setter
    def home_fax(self, value):
        self.w___u___r_fm = value

    @property
    def home_phone(self):
        return self.v__pel_bkku_

    @home_phone.setter
    def home_phone(self, value):
        self.v__pel_bkku_ = value

    @property
    def initials(self):
        return self.____s_a_ddga

    @initials.setter
    def initials(self, value):
        self.____s_a_ddga = value

    @property
    def isdn(self):
        return self._k__dsw_fx_j

    @isdn.setter
    def isdn(self, value):
        self._k__dsw_fx_j = value

    @property
    def manager_name(self):
        return self._h_sxo__l_h_

    @manager_name.setter
    def manager_name(self, value):
        self._h_sxo__l_h_ = value

    @property
    def middle_name(self):
        return self.fxo_h_yp____

    @middle_name.setter
    def middle_name(self, value):
        self.fxo_h_yp____ = value

    @property
    def nickname(self):
        return self.r_____xd__nn

    @nickname.setter
    def nickname(self, value):
        self.r_____xd__nn = value

    @property
    def office_location(self):
        return self.xh_n_w_ab_q_

    @office_location.setter
    def office_location(self, value):
        self.xh_n_w_ab_q_ = value

    @property
    def other_address_city(self):
        return self.p___p__ch_nr

    @other_address_city.setter
    def other_address_city(self, value):
        self.p___p__ch_nr = value

    @property
    def other_address_country(self):
        return self.x__za__bvxv_

    @other_address_country.setter
    def other_address_country(self, value):
        self.x__za__bvxv_ = value

    @property
    def other_address_postal_code(self):
        return self.b___w_g__t__

    @other_address_postal_code.setter
    def other_address_postal_code(self, value):
        self.b___w_g__t__ = value

    @property
    def other_address_state(self):
        return self._n___kc___xe

    @other_address_state.setter
    def other_address_state(self, value):
        self._n___kc___xe = value

    @property
    def other_address_street(self):
        return self.t___m_b___qg

    @other_address_street.setter
    def other_address_street(self, value):
        self.t___m_b___qg = value

    @property
    def other_phone(self):
        return self.o___h_f_ey_j

    @other_phone.setter
    def other_phone(self, value):
        self.o___h_f_ey_j = value

    @property
    def pager(self):
        return self.w_qf___ld___

    @pager.setter
    def pager(self, value):
        self.w_qf___ld___ = value

    @property
    def personal_home_page(self):
        return self.__v_cyc_____

    @personal_home_page.setter
    def personal_home_page(self, value):
        self.__v_cyc_____ = value

    @property
    def postal_address(self):
        return self.h__l____bnit

    @postal_address.setter
    def postal_address(self, value):
        self.h__l____bnit = value

    @property
    def business_address_country(self):
        return self.ks___x_ef_l_

    @business_address_country.setter
    def business_address_country(self, value):
        self.ks___x_ef_l_ = value

    @property
    def business_address_city(self):
        return self.g_k_____pg__

    @business_address_city.setter
    def business_address_city(self, value):
        self.g_k_____pg__ = value

    @property
    def business_address_postal_code(self):
        return self.___c_d_i__l_

    @business_address_postal_code.setter
    def business_address_postal_code(self, value):
        self.___c_d_i__l_ = value

    @property
    def business_address_post_office_box(self):
        return self.acu_i__mj_b_

    @business_address_post_office_box.setter
    def business_address_post_office_box(self, value):
        self.acu_i__mj_b_ = value

    @property
    def business_address_state(self):
        return self.__dyk_vx_w__

    @business_address_state.setter
    def business_address_state(self, value):
        self.__dyk_vx_w__ = value

    @property
    def business_address_street(self):
        return self._q___u__q_u_

    @business_address_street.setter
    def business_address_street(self, value):
        self._q___u__q_u_ = value

    @property
    def primary_fax(self):
        return self.hl_z____eu_u

    @primary_fax.setter
    def primary_fax(self, value):
        self.hl_z____eu_u = value

    @property
    def primary_phone(self):
        return self.__br___ty__q

    @primary_phone.setter
    def primary_phone(self, value):
        self.__br___ty__q = value

    @property
    def profession(self):
        return self.mma_d_p_ijv_

    @profession.setter
    def profession(self, value):
        self.mma_d_p_ijv_ = value

    @property
    def radio_phone(self):
        return self.p___m__s_toa

    @radio_phone.setter
    def radio_phone(self, value):
        self.p___m__s_toa = value

    @property
    def spouse_name(self):
        return self.reycs___h__f

    @spouse_name.setter
    def spouse_name(self, value):
        self.reycs___h__f = value

    @property
    def surname(self):
        return self.__zl_e_zx___

    @surname.setter
    def surname(self, value):
        self.__zl_e_zx___ = value

    @property
    def telex(self):
        return self.j_i_g__k____

    @telex.setter
    def telex(self, value):
        self.j_i_g__k____ = value

    @property
    def title(self):
        return self._x___k_b____

    @title.setter
    def title(self, value):
        self._x___k_b____ = value

    @property
    def tty_tdd_phone(self):
        return self.jvd_z__mk__k

    @tty_tdd_phone.setter
    def tty_tdd_phone(self, value):
        self.jvd_z__mk__k = value

    @property
    def wedding_anniversary(self):
        return self.__g___vgx_da

    @wedding_anniversary.setter
    def wedding_anniversary(self, value):
        self.__g___vgx_da = value

    @property
    def gender(self):
        return self.o_y_e___dh__

    @gender.setter
    def gender(self, value):
        self.o_y_e___dh__ = value

    @property
    def selected_mailing_address(self):
        return self._______w_a__

    @selected_mailing_address.setter
    def selected_mailing_address(self, value):
        self._______w_a__ = value

    @property
    def contact_has_picture(self):
        return self.______yi_a_r

    @contact_has_picture.setter
    def contact_has_picture(self, value):
        self.______yi_a_r = value

    @property
    def file_as(self):
        return self.a____h_d_m__

    @file_as.setter
    def file_as(self, value):
        self.a____h_d_m__ = value

    @property
    def instant_messenger_address(self):
        return self.___p___m_x__

    @instant_messenger_address.setter
    def instant_messenger_address(self, value):
        self.___p___m_x__ = value

    @property
    def internet_free_busy_address(self):
        return self.a__yb______q

    @internet_free_busy_address.setter
    def internet_free_busy_address(self, value):
        self.a__yb______q = value

    @property
    def business_address(self):
        return self._in__an_yv__

    @business_address.setter
    def business_address(self, value):
        self._in__an_yv__ = value

    @property
    def home_address(self):
        return self.kwi_e__ffg__

    @home_address.setter
    def home_address(self, value):
        self.kwi_e__ffg__ = value

    @property
    def other_address(self):
        return self.___ym__z_v__

    @other_address.setter
    def other_address(self, value):
        self.___ym__z_v__ = value

    @property
    def email1_address(self):
        return self.s__b____or_b

    @email1_address.setter
    def email1_address(self, value):
        self.s__b____or_b = value

    @property
    def email2_address(self):
        return self._us___o__z__

    @email2_address.setter
    def email2_address(self, value):
        self._us___o__z__ = value

    @property
    def email3_address(self):
        return self._cf__c_q__c_

    @email3_address.setter
    def email3_address(self, value):
        self._cf__c_q__c_ = value

    @property
    def email1_display_name(self):
        return self.y___cq__rk__

    @email1_display_name.setter
    def email1_display_name(self, value):
        self.y___cq__rk__ = value

    @property
    def email2_display_name(self):
        return self.w_g_ag_b_w__

    @email2_display_name.setter
    def email2_display_name(self, value):
        self.w_g_ag_b_w__ = value

    @property
    def email3_display_name(self):
        return self.j_t_u__f____

    @email3_display_name.setter
    def email3_display_name(self, value):
        self.j_t_u__f____ = value

    @property
    def email1_display_as(self):
        return self._z___m__jkqj

    @email1_display_as.setter
    def email1_display_as(self, value):
        self._z___m__jkqj = value

    @property
    def email2_display_as(self):
        return self.m__nj____x__

    @email2_display_as.setter
    def email2_display_as(self, value):
        self.m__nj____x__ = value

    @property
    def email3_display_as(self):
        return self.h_k_lm______

    @email3_display_as.setter
    def email3_display_as(self, value):
        self.h_k_lm______ = value

    @property
    def email1_type(self):
        return self._f__lx__ayl_

    @email1_type.setter
    def email1_type(self, value):
        self._f__lx__ayl_ = value

    @property
    def email2_type(self):
        return self.s__g_h__crxw

    @email2_type.setter
    def email2_type(self, value):
        self.s__g_h__crxw = value

    @property
    def email3_type(self):
        return self.e_o__a__mz_s

    @email3_type.setter
    def email3_type(self, value):
        self.e_o__a__mz_s = value

    @property
    def email1_entry_id(self):
        return self._g_l_bu__r__

    @email1_entry_id.setter
    def email1_entry_id(self, value):
        self._g_l_bu__r__ = value

    @property
    def email2_entry_id(self):
        return self.kw_r____n__e

    @email2_entry_id.setter
    def email2_entry_id(self, value):
        self.kw_r____n__e = value

    @property
    def email3_entry_id(self):
        return self.ti__vpygof_h

    @email3_entry_id.setter
    def email3_entry_id(self, value):
        self.ti__vpygof_h = value

    @property
    def recipients(self):
        return self.__w_e______y

    @recipients.setter
    def recipients(self, value):
        self.__w_e______y = value

    @property
    def attachments(self):
        return self.uj_c_u_uy___

    @attachments.setter
    def attachments(self, value):
        self.uj_c_u_uy___ = value

    @property
    def extended_properties(self):
        return self.fmuyou__mciw

    @extended_properties.setter
    def extended_properties(self, value):
        self.fmuyou__mciw = value

    @property
    def named_properties(self):
        return self.__qwshy_x_o_

    @named_properties.setter
    def named_properties(self, value):
        self.__qwshy_x_o_ = value

    @property
    def encoding(self):
        return self.nsifr_q_er__

    @encoding.setter
    def encoding(self, value):
        self.nsifr_q_er__ = value

    @property
    def is_embedded(self):
        return self.t__n_____ev_

    @is_embedded.setter
    def is_embedded(self, value):
        self.t__n_____ev_ = value



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

    def __init__(self):

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
            self._____j______(buffer)

    def _____j______(self, buffer):

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

                self.deleted_instance_dates.append(RecurrencePattern.__h__on_on_j(minutes))            

        self.modified_instance_count = int.from_bytes(buffer[next_position: next_position + 4], "little") 
        next_position += 4

        if self.modified_instance_count > 0:

            self.modified_instance_dates = []

            for i in range(self.modified_instance_count):

                if len(buffer) < next_position + 4:
                    return

                minutes = int.from_bytes(buffer[next_position: next_position + 4], "little")  
                next_position += 4

                self.modified_instance_dates.append(RecurrencePattern.__h__on_on_j(minutes))   

        if len(buffer) < next_position + 4:
            return

        start_date_minutes =  int.from_bytes(buffer[next_position: next_position + 4], "little")  
        next_position += 4

        self.start_date = RecurrencePattern.__h__on_on_j(start_date_minutes)

        end_date_minutes = int.from_bytes(buffer[next_position: next_position + 4], "little")  

        self.end_date = RecurrencePattern.__h__on_on_j(end_date_minutes)

    @staticmethod
    def __h__on_on_j(_e___frx___s):

        __e__g__r__o = datetime.datetime(1901,1,1)

        try:
            jgv__c_h___y = datetime.datetime(1601,1,1)
            __m_o_nnnh_z = _e___frx___s * 60 * 1000
            __e__g__r__o = jgv__c_h___y + datetime.timedelta(__m_o_nnnh_z)
        except:
            pass

        return __e__g__r__o

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
        self.___iat_p_dyf = Header()
        self.gz_l_hqialu_ = RootDirectoryEntry()

        if file_path is not None:
            f = open(file_path, 'rb')
            buffer = f.read()
            self._____j______(buffer)
            f.close()

        elif buffer != None:
            self._____j______(buffer)

    def _____j______(self, _s___oubc___):
        self.___iat_p_dyf = Header(_s___oubc___)
        
        __m_rz_y__e_ = self._z_c______a_(_s___oubc___)
        
        __wm_kg___cj = self.uc_uf____zp_(_s___oubc___, __m_rz_y__e_) 

        if self.header.first_mini_fat_sector != 0xFFFFFFFE:
            rm___j_p__kt = self.x_mx_q__cwd_(_s___oubc___, __wm_kg___cj)

        ____xfp__paq = []
    
        s_p_o_o__e_f = self.header.first_directory_sector
        ____xfp__paq.append(s_p_o_o__e_f)

        while True:
            s_p_o_o__e_f = __wm_kg___cj[s_p_o_o__e_f]

            if s_p_o_o__e_f != 0xFFFFFFFE:
                ____xfp__paq.append(s_p_o_o__e_f)
            else:
                break

        hpxwt__l_d_j = bytearray()

        for i in range(len(____xfp__paq)):
            ___d__aij___ = ____xfp__paq[i]
            h___ve___f__ = ___d__aij___ * self.header.sector_size + self.header.sector_size

            _y__l_udjh__ = _s___oubc___[h___ve___f__: h___ve___f__ + self.header.sector_size]
            h___ve___f__ += self.header.sector_size

            hpxwt__l_d_j += bytearray(_y__l_udjh__)
        
        self.gz_l_hqialu_ = DirectoryEntry.parse(bytes(hpxwt__l_d_j), 0)

        ___xv_ab__p_ = {}

        ___xv_ab__p_[0] = self.gz_l_hqialu_

        if (self.gz_l_hqialu_.child_sid != 0xFFFFFFFF):
            
            h___ve___f__ = self.gz_l_hqialu_.child_sid * 128
            jtk___tmh__o = DirectoryEntry.parse(bytes(hpxwt__l_d_j), h___ve___f__)

            ___xv_ab__p_[self.gz_l_hqialu_.child_sid] = jtk___tmh__o
                
            self.gz_l_hqialu_.directory_entries.append(jtk___tmh__o)
            jtk___tmh__o.parent = self.gz_l_hqialu_

            j__p_r_gp_b_  = []
            __k_bervcb_f = []
            _j_nssx___p_ = []

            j__p_r_gp_b_.append(jtk___tmh__o)
            __k_bervcb_f.append(jtk___tmh__o)
            _j_nssx___p_.append(jtk___tmh__o)

            while (len(j__p_r_gp_b_) > 0 or len(__k_bervcb_f) > 0 or len(_j_nssx___p_) > 0 ):
                
                if (len(j__p_r_gp_b_) > 0):
                    _q__g__a_z__ = j__p_r_gp_b_.pop()

                    if (_q__g__a_z__.left_sibling_sid != 0xFFFFFFFF and _q__g__a_z__.left_sibling_sid not in ___xv_ab__p_):
                        h___ve___f__ = _q__g__a_z__.left_sibling_sid * 128
                        jtk___tmh__o = DirectoryEntry.parse(bytes(hpxwt__l_d_j), h___ve___f__)

                        ___xv_ab__p_[_q__g__a_z__.left_sibling_sid] = jtk___tmh__o
                        
                        _q__g__a_z__.parent.directory_entries.append(jtk___tmh__o)
                        jtk___tmh__o.parent = _q__g__a_z__.parent

                        j__p_r_gp_b_.append(jtk___tmh__o)
                        __k_bervcb_f.append(jtk___tmh__o)
                        _j_nssx___p_.append(jtk___tmh__o)

                        continue

                if (len(__k_bervcb_f) > 0):
                    _q__g__a_z__ = __k_bervcb_f.pop()

                    if (_q__g__a_z__.right_sibling_sid != 0xFFFFFFFF and _q__g__a_z__.right_sibling_sid not in ___xv_ab__p_):
                        h___ve___f__ = _q__g__a_z__.right_sibling_sid * 128
                        jtk___tmh__o = DirectoryEntry.parse(bytes(hpxwt__l_d_j), h___ve___f__)

                        ___xv_ab__p_[_q__g__a_z__.right_sibling_sid] = jtk___tmh__o
                        
                        _q__g__a_z__.parent.directory_entries.append(jtk___tmh__o)
                        jtk___tmh__o.parent = _q__g__a_z__.parent

                        j__p_r_gp_b_.append(jtk___tmh__o)
                        __k_bervcb_f.append(jtk___tmh__o)
                        _j_nssx___p_.append(jtk___tmh__o)

                        continue

                if (len(_j_nssx___p_) > 0):
                    _q__g__a_z__ = _j_nssx___p_.pop()

                    if (_q__g__a_z__.child_sid != 0xFFFFFFFF and _q__g__a_z__.child_sid not in ___xv_ab__p_):
                        h___ve___f__ = _q__g__a_z__.child_sid * 128
                        jtk___tmh__o = DirectoryEntry.parse(bytes(hpxwt__l_d_j), h___ve___f__)

                        ___xv_ab__p_[_q__g__a_z__.child_sid] = jtk___tmh__o
                        
                        _q__g__a_z__.directory_entries.append(jtk___tmh__o)
                        jtk___tmh__o.parent = _q__g__a_z__

                        j__p_r_gp_b_.append(jtk___tmh__o)
                        __k_bervcb_f.append(jtk___tmh__o)
                        _j_nssx___p_.append(jtk___tmh__o)

                        continue
           
            hqpdg_pz___p = []
            
            for f_q____r_w__ in ___xv_ab__p_.values():
                
                if (f_q____r_w__ is self.gz_l_hqialu_):
                    hqpdg_pz___p.insert(0, f_q____r_w__)
                else:
                    hqpdg_pz___p.append(f_q____r_w__)

            ____d__w_jg_ = bytearray()

            for i in range(len(hqpdg_pz___p)):
                v_s___a__dcs = hqpdg_pz___p[i]

                if(v_s___a__dcs.type is not DirectoryEntryType.STORAGE):
                    if(v_s___a__dcs.type is not DirectoryEntryType.ROOT and v_s___a__dcs.size > 0 and v_s___a__dcs.size < self.header.mini_stream_max_size):
                        __us__g_tslu = []

                        _ae___g___vb = v_s___a__dcs.start_sector
                        __us__g_tslu.append(_ae___g___vb)

                        while True:
                            _ae___g___vb = rm___j_p__kt[_ae___g___vb]

                            if (_ae___g___vb != 0xFFFFFFFC and _ae___g___vb != 0xFFFFFFFD and _ae___g___vb != 0xFFFFFFFE and _ae___g___vb != 0xFFFFFFFF and _ae___g___vb != rm___j_p__kt[_ae___g___vb]):
                                __us__g_tslu.append(_ae___g___vb)
                            else:
                                break

                        ta_gbb_fkd__ = bytearray()

                        for j in range(len(__us__g_tslu)):
                            _q__e___rtrj = __us__g_tslu[j]
                            h___ve___f__ = _q__e___rtrj * 64

                            _y__l_udjh__ = ____d__w_jg_[h___ve___f__: h___ve___f__ + 64]
                            h___ve___f__ += 64

                            ta_gbb_fkd__ += _y__l_udjh__

                        x_mh__yn__f_ = min(len(ta_gbb_fkd__), v_s___a__dcs.size)
                        v_s___a__dcs.buffer = ta_gbb_fkd__[0: x_mh__yn__f_]

                    elif (v_s___a__dcs.size > 0):
                        __us__g_tslu = []

                        _ae___g___vb = v_s___a__dcs.start_sector
                        __us__g_tslu.append(_ae___g___vb)

                        while True:
                            _ae___g___vb = __wm_kg___cj[_ae___g___vb]

                            if (_ae___g___vb != 0xFFFFFFFC and _ae___g___vb != 0xFFFFFFFD and _ae___g___vb != 0xFFFFFFFE and _ae___g___vb != 0xFFFFFFFF and _ae___g___vb != __wm_kg___cj[_ae___g___vb]):
                                __us__g_tslu.append(_ae___g___vb)
                            else:
                                break

                        ta_gbb_fkd__ = bytearray()

                        for j in range(len(__us__g_tslu)):
                            _q__e___rtrj = __us__g_tslu[j]
                            h___ve___f__ = _q__e___rtrj * self.header.sector_size + self.header.sector_size

                            _y__l_udjh__ = _s___oubc___[h___ve___f__: h___ve___f__ + self.header.sector_size]
                            h___ve___f__ += self.header.sector_size

                            ta_gbb_fkd__ += _y__l_udjh__

                        x_mh__yn__f_ = min(len(ta_gbb_fkd__), v_s___a__dcs.size)
                        v_s___a__dcs.buffer = ta_gbb_fkd__[0: x_mh__yn__f_]

                        if (v_s___a__dcs is self.gz_l_hqialu_ and self.gz_l_hqialu_.buffer is not None):
                            ____d__w_jg_ += self.gz_l_hqialu_.buffer
                        
            
    def x_mx_q__cwd_(self, _s___oubc___, __wm_kg___cj):

        ____pj_aes__ = int(self.header.sector_size / 4)
        rm___j_p__kt = [0] * self.header.mini_fat_sector_count * ____pj_aes__
        cinv___y_k__ = []

        hm_____zfstj = self.header.first_mini_fat_sector
        cinv___y_k__.append(hm_____zfstj)

        while True:
            hm_____zfstj = __wm_kg___cj[hm_____zfstj]

            if hm_____zfstj != 0xFFFFFFFE:
                cinv___y_k__.append(hm_____zfstj)
            else:
                break

        e___i_u_wg__ = 0

        for i in range(len(cinv___y_k__)):
            h___ve___f__ = cinv___y_k__[i] * self.header.sector_size + self.header.sector_size

            for _ in range(____pj_aes__):
                rm___j_p__kt[e___i_u_wg__] = int.from_bytes(_s___oubc___[h___ve___f__: h___ve___f__ + 4], "little")
                h___ve___f__ += 4
                e___i_u_wg__ += 1

        return rm___j_p__kt

    def _z_c______a_(self, _s___oubc___):

        if self.header.fat_sector_count <= 109:

            __m_rz_y__e_ = [0] * self.header.fat_sector_count
            
            for i in range(self.header.fat_sector_count):
                __m_rz_y__e_[i] = self.header.difat[i]

            return __m_rz_y__e_

        else:
            ____pj_aes__ = int(self.header.sector_size / 4)
            __xngq_f_kcp = [0] * ____pj_aes__
            __m_rz_y__e_ = [0] * self.header.fat_sector_count 

            for i in range(109):
                __m_rz_y__e_[i] = self.header.difat[i]

            h___ve___f__ = self.header.first_difat_sector * self.header.sector_size + self.header.sector_size
            e___i_u_wg__ = 109

            while True:

                for i in range(____pj_aes__):
                    __xngq_f_kcp[i] = int.from_bytes(_s___oubc___[h___ve___f__: h___ve___f__ + 4], "little")
                    h___ve___f__ += 4

                for i in range(____pj_aes__ - 1):
                    if __xngq_f_kcp[i] != 0xFFFFFFFF and e___i_u_wg__ < len(__m_rz_y__e_):
                        __m_rz_y__e_[e___i_u_wg__] = __xngq_f_kcp[i]
                        e___i_u_wg__ += 1

                if __xngq_f_kcp[____pj_aes__ - 1] != 0xFFFFFFFE and e___i_u_wg__ < len(__m_rz_y__e_):
                    h___ve___f__ = __xngq_f_kcp[____pj_aes__ - 1] * self.header.sector_size + self.header.sector_size
                else:
                    break

            return __m_rz_y__e_

    def uc_uf____zp_(self, _s___oubc___, __m_rz_y__e_):

        ____pj_aes__ = int(self.header.sector_size / 4)
        __wm_kg___cj = [0] * self.header.fat_sector_count * ____pj_aes__
        e___i_u_wg__ = 0

        for i in range(len(__m_rz_y__e_)):
            h___ve___f__ = __m_rz_y__e_[i] * self.header.sector_size + self.header.sector_size

            for _ in range(____pj_aes__):
                __wm_kg___cj[e___i_u_wg__] = int.from_bytes(_s___oubc___[h___ve___f__: h___ve___f__ + 4], "little")
                e___i_u_wg__ += 1
                h___ve___f__ += 4

        return __wm_kg___cj

    def oif____p_j__(self):

        au_b_g_zfp__ = datetime.datetime.now()

        ______w_____ = [] 
        __wm_kg___cj = [] 
        rm___j_p__kt = [] 

        a___h_____c_ = 0xFFFFFFFE
        _nx____wtm_k = 0xFFFFFFFE
        ______ojn___ = 0

        _t_w_dc_____ = bytearray()

        self.gz_l_hqialu_.color = Color.RED
        self.gz_l_hqialu_.type = DirectoryEntryType.ROOT
        self.gz_l_hqialu_.buffer = None
        self.gz_l_hqialu_.left_sibling_sid = 0xFFFFFFFF
        self.gz_l_hqialu_.right_sibling_sid = 0xFFFFFFFF           
        self.gz_l_hqialu_.created_time = datetime.datetime(1,1,1)
        self.gz_l_hqialu_.last_modified_time = datetime.datetime(1,1,1)
        self.gz_l_hqialu_.size = 0
        self.gz_l_hqialu_.start_sector = 0

        ______w_____.append(self.gz_l_hqialu_)
        self.rtp__t__oe_m(self.gz_l_hqialu_, ______w_____, au_b_g_zfp__)
                
        h_vf_ys__y_u = bytearray()
        ____d__w_jg_ = bytearray()

        for i in range(len(______w_____) - 1, -1, -1):
            v_s___a__dcs = ______w_____[i]

            if (v_s___a__dcs.buffer is not None):
                v_s___a__dcs.size = len(v_s___a__dcs.buffer)
            else:
                v_s___a__dcs.size = 0

            if (i == 0 and len(____d__w_jg_) > 0):
                v_s___a__dcs.buffer = bytes(____d__w_jg_)
                v_s___a__dcs.size = len(v_s___a__dcs.buffer)
                      

            if (i > 0 and v_s___a__dcs.size > 0 and v_s___a__dcs.size < self.header.mini_stream_max_size):
                v_s___a__dcs.start_sector = len(rm___j_p__kt)

                for __s_i___h_rk in range(0, len(v_s___a__dcs.buffer), self.header.mini_sector_size):
                    ___scqy_r_v_ = bytearray(self.header.mini_sector_size)                    
                    __y__hs__ma_ = len(___scqy_r_v_)

                    if (len(v_s___a__dcs.buffer) < __s_i___h_rk + self.header.mini_sector_size):
                        __y__hs__ma_ = len(v_s___a__dcs.buffer) - __s_i___h_rk
    
                    ___scqy_r_v_[0: __y__hs__ma_] = v_s___a__dcs.buffer[__s_i___h_rk: __s_i___h_rk + __y__hs__ma_]
                    ____d__w_jg_ += ___scqy_r_v_

                    if (__s_i___h_rk + self.header.mini_sector_size < len(v_s___a__dcs.buffer)):
                        rm___j_p__kt.append(len(rm___j_p__kt) + 1)
                    else:
                        rm___j_p__kt.append(0xFFFFFFFE)

            elif (i > 0 and v_s___a__dcs.size > 0 and v_s___a__dcs.size >= self.header.mini_stream_max_size):
                v_s___a__dcs.start_sector = len(__wm_kg___cj)

                for __s_i___h_rk in range(0, len(v_s___a__dcs.buffer), self.header.sector_size):
                    ___scqy_r_v_ = bytearray(self.header.sector_size)                    
                    __y__hs__ma_ = len(___scqy_r_v_)

                    if (len(v_s___a__dcs.buffer) < __s_i___h_rk + self.header.sector_size):
                        __y__hs__ma_ = len(v_s___a__dcs.buffer) - __s_i___h_rk

                    ___scqy_r_v_[0: __y__hs__ma_] = v_s___a__dcs.buffer[__s_i___h_rk: __s_i___h_rk + __y__hs__ma_]
                    h_vf_ys__y_u += ___scqy_r_v_

                    if (__s_i___h_rk + self.header.sector_size < len(v_s___a__dcs.buffer)):
                        __wm_kg___cj.append(len(__wm_kg___cj) + 1)
                    else:
                        __wm_kg___cj.append(0xFFFFFFFE)

        __lgf__qa___ = self.header.sector_size / self.header.mini_sector_size
        _f_kbh__vm__ = 0
        et_j_ww__dua = False

        _nx____wtm_k = len(__wm_kg___cj)

        if (len(____d__w_jg_) > 0):
            ytv_bp_p____ = bytes(____d__w_jg_)
            ___scqy_r_v_ = bytearray(self.header.sector_size)

            for __s_i___h_rk in range(0, len(ytv_bp_p____), self.header.mini_sector_size):
                __y__hs__ma_ = self.header.mini_sector_size

                if (len(ytv_bp_p____) < __s_i___h_rk + self.header.mini_sector_size):
                    __y__hs__ma_ = len(____d__w_jg_) - __s_i___h_rk

                ___scqy_r_v_[_f_kbh__vm__ * self.header.mini_sector_size: _f_kbh__vm__ * self.header.mini_sector_size + __y__hs__ma_] = ytv_bp_p____[__s_i___h_rk: __s_i___h_rk + __y__hs__ma_]
                _f_kbh__vm__ += 1

                if (__s_i___h_rk + self.header.mini_sector_size >= len(ytv_bp_p____)):
                    et_j_ww__dua = True

                if (et_j_ww__dua or _f_kbh__vm__ == __lgf__qa___):
                    _f_kbh__vm__ = 0
                    h_vf_ys__y_u += bytes(___scqy_r_v_)

                    if (not et_j_ww__dua):
                        __wm_kg___cj.append(len(__wm_kg___cj) + 1)
                    else:
                        __wm_kg___cj.append(0xFFFFFFFE)


            _ven_mm__zr_ = int(self.header.sector_size / 4)
            a___h_____c_ = len(__wm_kg___cj)

            for i in range(0, len(rm___j_p__kt), _ven_mm__zr_):
                g_z_zwxzt__c = bytearray(self.header.sector_size)

                for j in range(_ven_mm__zr_):
                    if (i + j < len(rm___j_p__kt)):
                        w_p_aj____nn = rm___j_p__kt[i + j]
                        _o___wns___n = w_p_aj____nn.to_bytes(4, "little")
                        g_z_zwxzt__c[j * 4: j * 4 + 4] = _o___wns___n[0:4]
                    else:
                        _o___wns___n = 0xFFFFFFFF.to_bytes(4, "little")
                        g_z_zwxzt__c[j * 4: j * 4 + 4] = _o___wns___n[0:4]

                h_vf_ys__y_u += bytes(g_z_zwxzt__c)
                ______ojn___ += 1

                if (i + _ven_mm__zr_ < len(rm___j_p__kt)):
                    __wm_kg___cj.append(len(__wm_kg___cj) + 1)
                else:
                    __wm_kg___cj.append(0xFFFFFFFE) 
        
        _t_w_dc_____ += bytes(h_vf_ys__y_u)

        self.header.first_directory_sector = len(__wm_kg___cj)

        ne_x_yozxx_u = 0

        _____h__jd_s = int(self.header.sector_size / 128)

        for i in range (0, len(______w_____), _____h__jd_s):

            if (______w_____[i] is self.gz_l_hqialu_ and _nx____wtm_k != 0xFFFFFFFE):
                    self.gz_l_hqialu_.start_sector = _nx____wtm_k

            s_p_o_o__e_f = bytearray(self.header.sector_size)

            for j in range(_____h__jd_s):

                if (i + j < len(______w_____)):
                    v_s___a__dcs = ______w_____[i + j]
                    s_p_o_o__e_f[j * 128: j * 128 + 128] = v_s___a__dcs.to_bytes()

            _t_w_dc_____ += bytes(s_p_o_o__e_f)
            ne_x_yozxx_u += 1

            if (i + _____h__jd_s < len(______w_____)):
                __wm_kg___cj.append(len(__wm_kg___cj) + 1)
            else:
                __wm_kg___cj.append(0xFFFFFFFE)

        if (self.header.major_version == 4):
            self.header.directory_sector_count = ne_x_yozxx_u


        _g____j_ff_r = int(self.header.sector_size / 4)
        __w______vy_ = int(len(__wm_kg___cj) / _g____j_ff_r)

        if (__w______vy_ * _g____j_ff_r < len(__wm_kg___cj)):
            __w______vy_ = __w______vy_ + 1

        __w______vy_ = int((len(__wm_kg___cj) + __w______vy_) / _g____j_ff_r)

        if (__w______vy_ * _g____j_ff_r < len(__wm_kg___cj) + __w______vy_):
            __w______vy_ = __w______vy_ + 1

        _g__of_c____ = int((__w______vy_ - 109) / (_g____j_ff_r - 1))

        if (_g__of_c____ * _g____j_ff_r < (__w______vy_ - 109)):
            _g__of_c____ = _g__of_c____ + 1

        self.header.fat_sector_count = __w______vy_
        
        h_og_ih__y_m = []
        __a__og_____ = []

        for i in range(__w______vy_):
            __wm_kg___cj.append(0xFFFFFFFD) 
            h___ve___f__ = len(__wm_kg___cj) - 1

            if (i < 109):
                h_og_ih__y_m.append(h___ve___f__)
            else:
                __a__og_____.append(h___ve___f__)
 

        for i in range(_g__of_c____):
            __wm_kg___cj.append(0xFFFFFFFC)
        
        for i in range(0, len(__wm_kg___cj), _g____j_ff_r):

            _i_____mhyq_ = bytearray(self.header.sector_size)

            for j in range(_g____j_ff_r):

                if ((i + j) < len(__wm_kg___cj)):
                    _i_____mhyq_[j * 4: j * 4 + 4] = __wm_kg___cj[i + j].to_bytes(4, "little")
                else:
                    _i_____mhyq_[j * 4: j * 4 + 4] = 0xFFFFFFFF.to_bytes(4, "little")

            _t_w_dc_____ += _i_____mhyq_

        if (_g__of_c____ > 0):
            self.header.first_difat_sector = int(len(_t_w_dc_____) / self.header.sector_size)
        else:
            self.header.first_difat_sector = 0xFFFFFFFE

        self.header.difat_sector_count = _g__of_c____

        for i in range(len(h_og_ih__y_m)):
            self.header.difat[i] = h_og_ih__y_m[i]
  
        for i in range(len(h_og_ih__y_m), 109, 1):
            self.header.difat[i] = 0xFFFFFFFF

        __b___g_o___ = 1

        for i in range(0, len(__a__og_____), _g____j_ff_r - 1):
            _i_____mhyq_ = bytearray(self.header.sector_size)

            for j in range(_g____j_ff_r - 1):

                if (i + j < len(__a__og_____)):
                    _i_____mhyq_[j * 4: j * 4 + 4] = __a__og_____[i + j].to_bytes(4, "little")
                else:
                    _i_____mhyq_[j * 4: j * 4 + 4] = 0xFFFFFFFF.to_bytes(4, "little")

            if (i + (_g____j_ff_r - 1) < len(__a__og_____)):
                _v__im__m_nm = int.to_bytes(self.header.first_difat_sector + __b___g_o___, 4, "little")
                _i_____mhyq_[(_g____j_ff_r - 1) * 4: (_g____j_ff_r - 1) * 4 + 4] = _v__im__m_nm
                __b___g_o___ += 1
            else:
                _i_____mhyq_[(_g____j_ff_r - 1) * 4: (_g____j_ff_r - 1) * 4 + 4] = 0xFFFFFFFE.to_bytes(4, "little")

            _t_w_dc_____ += _i_____mhyq_


        self.header.first_mini_fat_sector = a___h_____c_
        self.header.mini_fat_sector_count = ______ojn___

        _t_w_dc_____ = self.header.to_bytes() + _t_w_dc_____

        return bytes(_t_w_dc_____)

    def rtp__t__oe_m(self, vi_h__c____n, ______w_____, au_b_g_zfp__):
        if (len(vi_h__c____n.directory_entries) > 0):
            vi_h__c____n.directory_entries.sort()

            _w__p_hz__rm = int(len(vi_h__c____n.directory_entries) / 2)
            j_d_hmrn_n_x = vi_h__c____n.directory_entries[_w__p_hz__rm]

            if (vi_h__c____n.color == Color.BLACK):
                j_d_hmrn_n_x.color = Color.RED
            else:
                j_d_hmrn_n_x.color = Color.BLACK
                
            j_d_hmrn_n_x.created_time = j_d_hmrn_n_x.last_modified_time = au_b_g_zfp__

            if (j_d_hmrn_n_x.buffer is not None):
                j_d_hmrn_n_x.size = len(j_d_hmrn_n_x.buffer)
            else:
                j_d_hmrn_n_x.size = 0

            j_d_hmrn_n_x.start_sector = 0

            j_d_hmrn_n_x.left_sibling_sid = 0xFFFFFFFF
            j_d_hmrn_n_x.right_sibling_sid = 0xFFFFFFFF
            j_d_hmrn_n_x.child_sid = 0xFFFFFFFF

            ______w_____.append(j_d_hmrn_n_x)
            vi_h__c____n.child_sid = len(______w_____) - 1

            __a_gm____ed = j_d_hmrn_n_x

            for l in range(_w__p_hz__rm - 1, -1, -1):
                k_r_kpwooeoi = vi_h__c____n.directory_entries[l]

                if (vi_h__c____n.color == Color.BLACK):
                    k_r_kpwooeoi.color = Color.RED
                else:
                    k_r_kpwooeoi.color = Color.BLACK

                k_r_kpwooeoi.created_time = k_r_kpwooeoi.last_modified_time = au_b_g_zfp__

                if (k_r_kpwooeoi.buffer is not None):
                    k_r_kpwooeoi.size = len(k_r_kpwooeoi.buffer)
                else:
                    k_r_kpwooeoi.size = 0

                k_r_kpwooeoi.left_sibling_sid = 0xFFFFFFFF
                k_r_kpwooeoi.right_sibling_sid = 0xFFFFFFFF
                k_r_kpwooeoi.child_sid = 0xFFFFFFFF

                ______w_____.append(k_r_kpwooeoi)
                __a_gm____ed.left_sibling_sid = len(______w_____) - 1
                __a_gm____ed = k_r_kpwooeoi

                if (isinstance(k_r_kpwooeoi, Storage)):
                    self.rtp__t__oe_m(k_r_kpwooeoi, ______w_____, au_b_g_zfp__)

            __a_gm____ed = j_d_hmrn_n_x

            for r in range(_w__p_hz__rm + 1, len(vi_h__c____n.directory_entries)):
                cp_cx_kh___e = vi_h__c____n.directory_entries[r]

                if (vi_h__c____n.color == Color.BLACK):
                    cp_cx_kh___e.color = Color.RED
                else:
                    cp_cx_kh___e.color = Color.BLACK

                cp_cx_kh___e.created_time = cp_cx_kh___e.last_modified_time = au_b_g_zfp__

                if (cp_cx_kh___e.buffer is not None):
                    cp_cx_kh___e.size = len(cp_cx_kh___e.buffer)
                else:
                    cp_cx_kh___e.size = 0

                cp_cx_kh___e.left_sibling_sid = 0xFFFFFFFF
                cp_cx_kh___e.right_sibling_sid = 0xFFFFFFFF
                cp_cx_kh___e.child_sid = 0xFFFFFFFF

                ______w_____.append(cp_cx_kh___e)
                __a_gm____ed.right_sibling_sid = len(______w_____) - 1
                __a_gm____ed = cp_cx_kh___e

                if (isinstance(cp_cx_kh___e, Storage)):
                    self.rtp__t__oe_m(cp_cx_kh___e, ______w_____, au_b_g_zfp__)
           
            if (isinstance(j_d_hmrn_n_x, Storage)):
                self.rtp__t__oe_m(j_d_hmrn_n_x, ______w_____, au_b_g_zfp__)

    def to_bytes(self):
        return self.oif____p_j__()

    def save(self, file_path):

        if(file_path is not None):
            file = open(file_path, "wb")
            file.write(self.to_bytes())
            file.close

    @property
    def header(self):
        return self.___iat_p_dyf

    @property
    def root(self):
        return self.gz_l_hqialu_


class DirectoryEntry:

    def __init__(self):
        self.__name = None
        self.y__gm__x_x_i = DirectoryEntryType.INVALID
        self.___y_m_mf__r = Color.BLACK
        self.x_r_y____h_i = 0
        self._j__wpv_t__g = 0
        self._____bmtxm__ = 0
        self.___qz____xl_ = bytes(16)
        self.tj__v__ba__i = 0
        self._r_vl__mmp_z = datetime.datetime(1,1,1)
        self._o_____ldam_ = datetime.datetime(1,1,1)
        self._q_lwgn__dd_ = 0
        self.z____v_ump_z = 0
        self.vk_b_____ln_ = 0
        self.__f_am_bt_x_ = None
        self._b___v__s_oh = []
        self.___x_ln_w__f = None 

    def __eq__(self, other):
        return self._y__tx__p_f_(other)

    def __lt__(self, other):
        return self._y__tx__p_f_(other)

    def __gt__(self, other):
        return self._y__tx__p_f_(other)

    def __repr__(self):
        return "%s" % (self.name)

    def __str__(self):
        return "%s" % (self.name)

    def _y__tx__p_f_(self, other):

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
        
        ___wet_o__sx  = buffer[position: position + 64] 
        position += 64

        aceh_ssnxcg_ = int.from_bytes(buffer[position: position + 2], "little")
        position += 2

        ___k_f__l_z_ = None

        if (aceh_ssnxcg_ > 1):
            t_l____xg__t = ___wet_o__sx[0: aceh_ssnxcg_ - 2]
            ___k_f__l_z_ = t_l____xg__t.decode('utf-16-le')

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

        _lh_n_zgf__x = int.from_bytes(buffer[position: position + 4], "little")
        position += 4
        
        j___p__ne_ua = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        _cw_q_ea_r__ = datetime.datetime(1,1,1)
        _d_____t_sfe = datetime.datetime(1,1,1)

        if (j___p__ne_ua > 0):
            _fi_km_v____ = _lh_n_zgf__x + (j___p__ne_ua << 32)
            jgv__c_h___y = datetime.datetime(1601,1,1)   

            try:    
                _cw_q_ea_r__ = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                _cw_q_ea_r__ = DirectoryEntry.v_____omf__x(_cw_q_ea_r__)
            except:
                pass

        _dfv_j__m___ = int.from_bytes(buffer[position: position + 4], "little")
        position += 4
        
        ____l__fau__ = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        if (____l__fau__ > 0):
            _fi_km_v____ = _dfv_j__m___ + (____l__fau__ << 32)
            jgv__c_h___y = datetime.datetime(1601,1,1)

            try:    
                _d_____t_sfe = jgv__c_h___y + datetime.timedelta(milliseconds = _fi_km_v____ / 10000)               
                _d_____t_sfe = DirectoryEntry.v_____omf__x(last_modified_time)
            except:
                pass

        start_sector = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        size = int.from_bytes(buffer[position: position + 4], "little")
        position += 4

        if (type == DirectoryEntryType.ROOT):            
            entry = RootDirectoryEntry()
            entry.__name = ___k_f__l_z_
            entry.y__gm__x_x_i = DirectoryEntryType.ROOT
            entry.___y_m_mf__r = color
            entry.x_r_y____h_i = left_sibling_sid
            entry._j__wpv_t__g = right_sibling_sid
            entry._____bmtxm__ = child_sid
            entry.___qz____xl_ = class_id
            entry.tj__v__ba__i = user_flags
            entry._r_vl__mmp_z = _cw_q_ea_r__
            entry._o_____ldam_ = _d_____t_sfe
            entry._q_lwgn__dd_ = start_sector
            entry.z____v_ump_z = size
            entry.vk_b_____ln_ = 0
            entry.__f_am_bt_x_ = None
            entry._b___v__s_oh = []
            entry.___x_ln_w__f = None
        
            return entry
        elif (type == DirectoryEntryType.STREAM):
            entry = Stream()
            entry.__name = ___k_f__l_z_
            entry.y__gm__x_x_i = DirectoryEntryType.STREAM
            entry.___y_m_mf__r = color
            entry.x_r_y____h_i = left_sibling_sid
            entry._j__wpv_t__g = right_sibling_sid
            entry._____bmtxm__ = child_sid
            entry.___qz____xl_ = class_id
            entry.tj__v__ba__i = user_flags
            entry._r_vl__mmp_z = _cw_q_ea_r__
            entry._o_____ldam_ = _d_____t_sfe
            entry._q_lwgn__dd_ = start_sector
            entry.z____v_ump_z = size
            entry.vk_b_____ln_ = 0
            entry.__f_am_bt_x_ = None
            entry._b___v__s_oh = []
            entry.___x_ln_w__f = None
        
            return entry                        
        elif (type == DirectoryEntryType.STORAGE):
            entry = Storage()
            entry.__name = ___k_f__l_z_
            entry.y__gm__x_x_i = DirectoryEntryType.STORAGE
            entry.___y_m_mf__r = color
            entry.x_r_y____h_i = left_sibling_sid
            entry._j__wpv_t__g = right_sibling_sid
            entry._____bmtxm__ = child_sid
            entry.___qz____xl_ = class_id
            entry.tj__v__ba__i = user_flags
            entry._r_vl__mmp_z = _cw_q_ea_r__
            entry._o_____ldam_ = _d_____t_sfe
            entry._q_lwgn__dd_ = start_sector
            entry.z____v_ump_z = size
            entry.vk_b_____ln_ = 0
            entry.__f_am_bt_x_ = None
            entry._b___v__s_oh = []
            entry.___x_ln_w__f = None
        
            return entry
        else:
            entry = Storage()
            entry.__name = ___k_f__l_z_
            entry.y__gm__x_x_i = DirectoryEntryType.INVALID
            entry.___y_m_mf__r = color
            entry.x_r_y____h_i = left_sibling_sid
            entry._j__wpv_t__g = right_sibling_sid
            entry._____bmtxm__ = child_sid
            entry.___qz____xl_ = class_id
            entry.tj__v__ba__i = user_flags
            entry._r_vl__mmp_z = _cw_q_ea_r__
            entry._o_____ldam_ = _d_____t_sfe
            entry._q_lwgn__dd_ = start_sector
            entry.z____v_ump_z = size
            entry.vk_b_____ln_ = 0
            entry.__f_am_bt_x_ = None
            entry._b___v__s_oh = []
            entry.___x_ln_w__f = None
        
            return entry

    def to_bytes(self):

        buffer = bytearray(128)
        position = 0

        unicode_name_buffer = self.__name.encode('utf-16-le')

        buffer[0: len(unicode_name_buffer)] = unicode_name_buffer
        position += 64

        buffer[position: position + 2] = int.to_bytes((len(self.__name) + 1) * 2, 2, "little")
        position += 2
        
        buffer[position: position + 1] = int.to_bytes(self.y__gm__x_x_i.value, 1, "little")
        position += 1

        buffer[position: position + 1] = int.to_bytes(self.___y_m_mf__r.value, 1, "little")
        position += 1

        buffer[position: position + 4] = int.to_bytes(self.x_r_y____h_i, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self._j__wpv_t__g, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self._____bmtxm__, 4, "little")
        position += 4

        buffer[position: position + 16] = self.___qz____xl_
        position += 16

        buffer[position: position + 4] = int.to_bytes(self.tj__v__ba__i, 4, "little")
        position += 4

        if (self._r_vl__mmp_z is not None and self._r_vl__mmp_z > datetime.datetime(1601,1,1)):

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._r_vl__mmp_z - jgv__c_h___y).total_seconds()) * 10_000_000

            fj_us_k__ow_ = _fi_km_v____.to_bytes(8, "little")

            buffer[position: position + 4] = fj_us_k__ow_[0:4]
            position += 4
            buffer[position: position + 4] = fj_us_k__ow_[4:8]
            position += 4
        else:
            buffer[position: position + 4] = bytes(4)
            position += 4
            buffer[position: position + 4] = bytes(4)
            position += 4

        if (self._o_____ldam_ is not None and self._o_____ldam_ > datetime.datetime(1601,1,1)):

            jgv__c_h___y = datetime.datetime(1601,1,1)
            _fi_km_v____ = int((self._o_____ldam_ - jgv__c_h___y).total_seconds()) * 10_000_000

            fj_us_k__ow_ = _fi_km_v____.to_bytes(8, "little")

            buffer[position: position + 4] = fj_us_k__ow_[0:4]
            position += 4
            buffer[position: position + 4] = fj_us_k__ow_[4:8]
            position += 4
        else:
            buffer[position: position + 4] = bytes(4)
            position += 4
            buffer[position: position + 4] = bytes(4)
            position += 4


        buffer[position: position + 4] = int.to_bytes(self._q_lwgn__dd_, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.z____v_ump_z, 4, "little")
        position += 4

        return buffer

    def get_entry(self, name):

        for entry in self.directory_entries:            
            if entry.name == name:
                return entry

        return None

    @staticmethod    
    def v_____omf__x(utc_datetime):
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
        return self.y__gm__x_x_i

    @type.setter
    def type(self, value):
        self.y__gm__x_x_i = value

    @property
    def color(self):
        return self.___y_m_mf__r

    @color.setter
    def color(self, value):
        self.___y_m_mf__r = value

    @property
    def left_sibling_sid(self):
        return self.x_r_y____h_i

    @left_sibling_sid.setter
    def left_sibling_sid(self, value):
        self.x_r_y____h_i = value

    @property
    def right_sibling_sid(self):
        return self._j__wpv_t__g

    @right_sibling_sid.setter
    def right_sibling_sid(self, value):
        self._j__wpv_t__g = value

    @property
    def child_sid(self):
        return self._____bmtxm__

    @child_sid.setter
    def child_sid(self, value):
        self._____bmtxm__ = value

    @property
    def class_id(self):
        return self.___qz____xl_

    @class_id.setter
    def class_id(self, value):
        self.___qz____xl_ = value

    @property
    def created_time(self):
        return self._r_vl__mmp_z

    @created_time.setter
    def created_time(self, value):
        self._r_vl__mmp_z = value

    @property
    def last_modified_time(self):
        return self._o_____ldam_

    @last_modified_time.setter
    def last_modified_time(self, value):
        self._o_____ldam_ = value

    @property
    def start_sector(self):
        return self._q_lwgn__dd_

    @start_sector.setter
    def start_sector(self, value):
        self._q_lwgn__dd_ = value

    @property
    def size(self):
        return self.z____v_ump_z

    @size.setter
    def size(self, value):
        self.z____v_ump_z = value

    @property
    def buffer(self):
        return self.__f_am_bt_x_

    @buffer.setter
    def buffer(self, value):
        self.__f_am_bt_x_ = value

    @property
    def directory_entries(self):
        return self._b___v__s_oh

    @property
    def parent(self):
        return self.___x_ln_w__f

    @parent.setter
    def parent(self, value):
        self.___x_ln_w__f = value

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
    ____wx____f_ = bytes([0xd0, 0xcf, 0x11, 0xe0, 0xa1, 0xb1, 0x1a, 0xe1])

    def __init__(self, buffer = None):

        self.___qz____xl_ = bytes(16)
        self.jb_____kb___ = 0x003E
        self.zgf_t__z__p_ = 0x0003
        self.__fd__b_iu__ = 0xFFFE
        self._arsdv__lx__ = 0x0009
        self.rsuwilatwm__ = 0x0006
        self.d__vzgvr__g_ = 0x0
        self.x__lsbwb_y_g = 0x0
        self.py_a____w_b_ = 0x0
        self._wwkw__l_y__ = 0x0
        self.a____e__wo_b = 0x0
        self._l___d_x_gy_ = 0x0
        self.r_j_b____u__ = 4096
        self.w__rtdvfs_g_ = 0x0
        self._xkzchvp__kz = 0x0
        self.d____w__b___ = 0x0
        self.___l__jvz___ = 0x0
        self._c__f_a_r_r_ = []

        for i in range(109):
            self._c__f_a_r_r_.append(0)

        if buffer is not None:
           
            position = 0

            test_signature = buffer[position: position + 8]
            position += 8

            for i in range(8):
                if test_signature[i] != Header.____wx____f_[i]:
                    raise Exception("Invalid file format.")

            self.___qz____xl_ = buffer[position: position + 16]
            position += 16

            self.jb_____kb___ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.zgf_t__z__p_ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.__fd__b_iu__ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self._arsdv__lx__ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.rsuwilatwm__ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.d__vzgvr__g_ = int.from_bytes(buffer[position: position + 2], "little")
            position += 2

            self.x__lsbwb_y_g = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.py_a____w_b_ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self._wwkw__l_y__ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.a____e__wo_b = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self._l___d_x_gy_ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.r_j_b____u__ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.w__rtdvfs_g_ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self._xkzchvp__kz = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.d____w__b___ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self.___l__jvz___ = int.from_bytes(buffer[position: position + 4], "little")
            position += 4

            self._c__f_a_r_r_ = []

            for i in range(109):
                self._c__f_a_r_r_.append(int.from_bytes(buffer[position: position + 4], "little"))
                position += 4

    def to_bytes(self):

        buffer = bytearray(self.sector_size)
        position = 0

        buffer[position: position + 8] = self.____wx____f_
        position += 8

        buffer[position: position + 16] = self.___qz____xl_
        position += 16

        buffer[position: position + 2] = int.to_bytes(self.jb_____kb___, 2, "little")
        position += 2
        
        buffer[position: position + 2] = int.to_bytes(self.zgf_t__z__p_, 2, "little")
        position += 2

        buffer[position: position + 2] = int.to_bytes(self.__fd__b_iu__, 2, "little")
        position += 2
        
        buffer[position: position + 2] = int.to_bytes(self._arsdv__lx__, 2, "little")
        position += 2

        buffer[position: position + 2] = int.to_bytes(self.rsuwilatwm__, 2, "little")
        position += 2
        
        buffer[position: position + 2] = int.to_bytes(self.d__vzgvr__g_, 2, "little")
        position += 2

        buffer[position: position + 4] = int.to_bytes(self.x__lsbwb_y_g, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.py_a____w_b_, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self._wwkw__l_y__, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.a____e__wo_b, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self._l___d_x_gy_, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.r_j_b____u__, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.w__rtdvfs_g_, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self._xkzchvp__kz, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.d____w__b___, 4, "little")
        position += 4

        buffer[position: position + 4] = int.to_bytes(self.___l__jvz___, 4, "little")
        position += 4

        for i in range(109):
            buffer[position: position + 4] = int.to_bytes(self._c__f_a_r_r_[i], 4, "little")
            position += 4

        return buffer

    @property
    def class_id(self):
        return self.___qz____xl_

    @property
    def minor_version(self):
        return self.jb_____kb___

    @minor_version.setter
    def minor_version(self, value):
        self.jb_____kb___ = value

    @property
    def major_version(self):
        return self.zgf_t__z__p_

    @major_version.setter
    def major_version(self, value):
        if (value == 3):
            self.zgf_t__z__p_ = value
            self._arsdv__lx__ = 0x0009
        else:
            self.zgf_t__z__p_ = value
            self._arsdv__lx__ = 0x000C
    
    @property
    def byte_order(self):
        return self.__fd__b_iu__

    @property
    def sector_size(self):
        if self._arsdv__lx__ == 9:
            return 512
        else:
            return 4096

    @property
    def mini_sector_size(self):
        return 64

    @property
    def directory_sector_count(self):
        return self.py_a____w_b_

    @directory_sector_count.setter
    def directory_sector_count(self, value):
        self.py_a____w_b_ = value

    @property
    def fat_sector_count(self):
        return self._wwkw__l_y__

    @fat_sector_count.setter
    def fat_sector_count(self, value):
        self._wwkw__l_y__ = value

    @property
    def first_directory_sector(self):
        return self.a____e__wo_b

    @first_directory_sector.setter
    def first_directory_sector(self, value):
        self.a____e__wo_b = value

    @property
    def transaction_signature(self):
        return self._l___d_x_gy_

    @property
    def mini_stream_max_size(self):
        return self.r_j_b____u__

    @property
    def first_mini_fat_sector(self):
        return self.w__rtdvfs_g_

    @first_mini_fat_sector.setter
    def first_mini_fat_sector(self, value):
        self.w__rtdvfs_g_ = value

    @property
    def mini_fat_sector_count(self):
        return self._xkzchvp__kz

    @mini_fat_sector_count.setter
    def mini_fat_sector_count(self, value):
        self._xkzchvp__kz = value

    @property
    def first_difat_sector(self):
        return self.d____w__b___

    @first_difat_sector.setter
    def first_difat_sector(self, value):
        self.d____w__b___ = value

    @property
    def difat_sector_count(self):
        return self.___l__jvz___

    @difat_sector_count.setter
    def difat_sector_count(self, value):
        self.___l__jvz___ = value

    @property
    def difat(self):
        return self._c__f_a_r_r_