from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWinExtras import QtWin
import project_cust_38.Cust_Qt as CQT

CQT.conver_ui_v_py()
from Setup_gui import Ui_MainWindow
import project_cust_38.Cust_Functions as F
import os
import sys
import platform


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.PUT_PO_UMOLCH = F.put_po_umolch() + F.sep() + 'MES' + F.sep()

        if F.nalich_file(self.PUT_PO_UMOLCH) == False:
            F.sozd_dir(self.PUT_PO_UMOLCH)
        self.ui.le_putust.setText(self.PUT_PO_UMOLCH)

        self.ui.btn_tool.clicked.connect(self.vibor_papki)
        self.ui.btn_setup.clicked.connect(self.load_gui)
        self.ui.btn_info.clicked.connect(self.load_info)
        # =======================================

        self.DICT_PROG = self.load_prog()
        self.DICT_LOCAL_PROG = self.load_local_prog()
        # self.ui.rbtn_reload.setEnabled(False)
        print(platform.win32_ver())
        CQT.load_css(self)
        self.load_gui()
        CQT.load_icons(self)


    @CQT.onerror
    def vibor_papki(self,*args):
        rez = CQT.getDirectory(self, self.ui.le_putust.text())
        if rez == '.' or rez == None:
            return
        self.ui.le_putust.setText(rez + F.sep())

    @CQT.onerror
    def load_local_prog(self):
        file_list_prog = self.PUT_PO_UMOLCH + 'cache.txt'
        if F.nalich_file(file_list_prog) == False:
            F.zap_f(self.PUT_PO_UMOLCH + 'cache.txt', [], '|', utf8=True)
        # ========================Таблица
        old_spis_prog = F.otkr_f(self.PUT_PO_UMOLCH + 'cache.txt', True, '|')
        list_for_del = []
        for item in old_spis_prog:
            prog = item[0]
            if prog not in self.DICT_PROG:
                list_for_del.append(prog)
        new_spis_prog = self.del_prog_fix_cache(old_spis_prog, list_for_del)
        dict_local_prog = dict(new_spis_prog)
        return dict_local_prog

    @CQT.onerror
    def del_prog_fix_cache(self, old_spis_prog, list_for_del):
        new_spis_prog = []
        for item in old_spis_prog:
            if item[0] not in list_for_del:
                new_spis_prog.append(item)
            else:
                F.udal_papky(item[1])
        F.zap_f(self.PUT_PO_UMOLCH + 'cache.txt', new_spis_prog, '|', utf8=True)
        return new_spis_prog

    @CQT.onerror
    def load_prog(self):
        list_prog = F.scfg('dir_list_prog').split(';')
        file_list_prog = ''
        for dir in list_prog:
            if F.nalich_file(dir + F.sep() + 'list.txt'):
                file_list_prog = dir + F.sep() + 'list.txt'
                path = dir
        if file_list_prog == '':
            CQT.msgbox(f'Не обнаружен список')
            sys.exit(app.exec())
        # ========================Таблица
        spis_prog_setup = F.otkr_f(file_list_prog, utf8=True, separ='|')
        zachin = F.sep().join(path.split(F.sep())[:-1]) + F.sep()
        goal = 'Z:\\ProdSoft\\'
        self.setWindowTitle(zachin)
        self.GLOBAL_PATH = zachin
        for i in range(len(spis_prog_setup)):
            spis_prog_setup[i][1] = spis_prog_setup[i][1].replace(goal, zachin)
        spis_prog_setup.insert(0, ['Имя', 'Путь', 'Название'])
        dict_rez = F.list_to_dict(spis_prog_setup, 'Имя')
        return dict_rez

    @CQT.onerror
    def load_gui(self,*args):
        if self.ui.fr_setup.isHidden():
            self.ui.fr_setup.setHidden(False)
            self.ui.fr_update.setHidden(True)
            self.load_setup()


        else:
            self.ui.fr_setup.setHidden(True)
            self.ui.fr_update.setHidden(False)
            self.load_upadate()

    @CQT.onerror
    def load_info(self,*args):
        file = "И-ОП6-1.5 инструкция «Порядок взаимодействия цехов и служб при работе с автоматизированной системой управления производством»..docx"
        full_path = os.path.join(self.GLOBAL_PATH, 'MES_setup', "info", file)
        F.zapyst_file(full_path, True)

    @CQT.onerror
    def load_upadate(self):
        if F.nalich_file(self.PUT_PO_UMOLCH + 'cache.txt'):
            self.ui.groupBox_2.setTitle('Обновление')
            tbl = self.ui.tbl_spis_prog_update
            CQT.clear_tbl(tbl)

            spis_prog = [[k, self.DICT_LOCAL_PROG[k]] for k in self.DICT_LOCAL_PROG.keys()]
            spis_prog.insert(0, ["Исп.", 'Имя', "Путь", 'Удалить', "Обновить", 'Запустить', 'Открыть_папку'])
            for i in range(1, len(spis_prog)):
                spis_prog[i].insert(0, '')
                spis_prog[i].append('')
                spis_prog[i].append('')
                spis_prog[i].append('')
                spis_prog[i].append('')
            CQT.zapoln_wtabl(self, spis_prog, tbl, separ='', isp_shapka=True)
            nk_ima = CQT.nom_kol_po_imen(tbl, 'Имя')
            nk_put = CQT.nom_kol_po_imen(tbl, 'Путь')
            nk_isp_f = CQT.nom_kol_po_imen(tbl, 'Исп.')
            nk_stat = CQT.nom_kol_po_imen(tbl, 'Обновить')
            nk_zap = CQT.nom_kol_po_imen(tbl, 'Запустить')
            nk_del = CQT.nom_kol_po_imen(tbl, 'Удалить')
            nk_open_dir = CQT.nom_kol_po_imen(tbl, 'Открыть_папку')
            tbl.setColumnHidden(nk_put, True)
            local_name_emb = 'embed'
            if platform.win32_ver()[0] == '7':
                local_name_emb = 'embed_win7'
            for i in range(tbl.rowCount()):
                ima = tbl.item(i, nk_ima).text()
                enable = self.check_version(self.DICT_LOCAL_PROG[ima], self.DICT_PROG[ima]['Путь'])
                CQT.add_btn(tbl, i, nk_stat, 'Обновить', not enable,
                            self.update_prog, img_path=F.sep().join(('icons', '127.png')), height=tbl.rowHeight(i), fontsize = 14)
                CQT.add_btn(tbl, i, nk_zap, 'Запуск', enable,
                            self.zapusk_prog, img_path=F.sep().join(('icons', '130.png')), height=tbl.rowHeight(i), fontsize = 14)
                CQT.add_btn(tbl, i, nk_del, 'Удалить', True,
                            self.del_prog, img_path=F.sep().join(('icons', '126.png')), height=tbl.rowHeight(i), fontsize = 14)
                CQT.add_btn(tbl, i, nk_open_dir, 'Папка', True,
                            self.open_dir, img_path=F.sep().join(('icons', '119.png')), height=tbl.rowHeight(i), fontsize = 14)
                
                path = F.sep().join((self.DICT_LOCAL_PROG[ima], local_name_emb, 'icons', '1.ico'))
                if F.nalich_file(path):
                    CQT.add_image(tbl, i, nk_isp_f, path, w=tbl.rowHeight(i), h=tbl.rowHeight(i))
            self.click_reload()
            tbl.horizontalHeader().hide()
            tbl.resizeColumnsToContents()
        else:
            self.load_gui()

    @CQT.onerror
    def open_dir(self, r, c):
        tbl = self.ui.tbl_spis_prog_update
        nk_name = CQT.nom_kol_po_imen(tbl, 'Имя')
        name = tbl.item(r, nk_name).text()
        path_local = self.DICT_LOCAL_PROG[name]
        F.otkr_papky(path_local)

    @CQT.onerror
    def del_prog(self, r, c):
        tbl = self.ui.tbl_spis_prog_update
        nk_name = CQT.nom_kol_po_imen(tbl, 'Имя')
        name = tbl.item(r, nk_name).text()
        if not CQT.msgboxgYN(f'Точно УДАЛИТЬ {name}?', icon=QtWidgets.QMessageBox.Critical):
            return
        self.del_prog_fix_cache([[k, self.DICT_LOCAL_PROG[k]] for k in self.DICT_LOCAL_PROG.keys()], [name])
        self.DICT_LOCAL_PROG = self.load_local_prog()
        self.load_upadate()
        pass

    @CQT.onerror
    def check_version(self, path, path_setup):
        local_name_emb = 'embed'
        if platform.win32_ver()[0] == '7':
            local_name_emb = 'embed_win7'
        try:
            ver_setup = F.otkr_f(path_setup + F.sep() + 'embed' + F.sep() + 'ver.txt')
            ver = F.otkr_f(path + F.sep() + local_name_emb + F.sep() + 'ver.txt')
            if ver == ver_setup:
                return True
            else:
                print(path_setup + F.sep() + 'embed' + F.sep() + 'ver.txt')
                print(ver_setup)
                print(path + F.sep() + local_name_emb + F.sep() + 'ver.txt')
                print(ver)
        except:
            print(path_setup + F.sep() + 'embed' + F.sep() + 'ver.txt')
            print(path + F.sep() + local_name_emb + F.sep() + 'ver.txt')
            return False
        return False

    @CQT.onerror
    def update_prog(self, r, c, tbl=''):
        if tbl == '':
            tbl = self.ui.tbl_spis_prog_update
        nk_name = CQT.nom_kol_po_imen(tbl, 'Имя')
        name = tbl.item(r, nk_name).text()
        path_local = self.DICT_LOCAL_PROG[name]
        put_ishod_dir = self.DICT_PROG[name]['Путь']
        if not F.nalich_file(path_local):
            CQT.msgbox('Не обнаружен каталог')
            return
        put_new_embed = path_local + F.sep() + 'embed'
        if platform.win32_ver()[0] == '7':
            spis_ishod_dir = put_ishod_dir.split(F.sep())
            spis_ishod_dir.insert(-1, 'win7')
            put_ishod_dir = F.sep().join(spis_ishod_dir)
            put_new_embed = path_local + F.sep() + 'embed_win7'
        print(f' use local put_new_embed : {put_new_embed}')

        if F.nalich_file(put_ishod_dir) == False:
            CQT.msgbox('Не найден исходный каталог.')
            return
        if F.nalich_file(put_new_embed + F.sep() + 'mydesign.py'):
            F.udal_file(put_new_embed + F.sep() + 'mydesign.py')

        if tbl == self.ui.tbl_spis_prog_update:
            CQT.statusbar_text(self, f'Обновление {name}...')
        else:
            CQT.statusbar_text(self, f'Установка {name}...')
        F.copytree(put_ishod_dir, path_local)
        spis_files = F.spis_files(path_local)
        for block in spis_files:
            for file in block[2]:
                if F.ostavit_rasshir(file) == '.ui':
                    F.udal_file(block[0] + F.sep() + file)

        spis_run = [['@echo off'], [f'python {self.DICT_PROG[name]["Название"]}']]
        print(f"try to create run.bat in dir {put_new_embed + F.sep() + 'run.bat'}")
        F.zap_f(put_new_embed + F.sep() + 'run.bat', spis_run, separ='|', utf8=True)
        try:
            F.skopir_file(put_ishod_dir  + F.sep() +  'embed' + F.sep() + 'ver.txt', put_new_embed + F.sep() + 'ver.txt')
        except:
            CQT.msgbox(f'ОШибка копирования версий')
            return
        # ==========================================FREE===============
        self.create_labels('window_free.vbs', put_new_embed, path_local, self.DICT_PROG[name]["Имя"], free=True)
        self.create_labels('window.vbs', put_new_embed, path_local, self.DICT_PROG[name]["Имя"] + '_win')
        # ====================================================
        self.cache_add(name, path_local)  # обновить список установленных мес программ
        if tbl == self.ui.tbl_spis_prog_update:
            self.load_upadate()
            CQT.msgbox(f'{name} успешно обновлено')
        else:
            self.load_setup()
            CQT.msgbox(f'{name} успешно установлено')
        CQT.statusbar_text(self, f'')

    @CQT.onerror
    def create_labels(self, vbs_name, put_new_embed, path_local, name, free=False):
        file_zapysk = put_new_embed + F.sep() + vbs_name
        F.udal_file(file_zapysk)
        if free:
            spis = ['Set WshShell = CreateObject("WScript.Shell")',
                    rf'WshShell.Run chr(34) & "{put_new_embed}\run.bat" & Chr(34), 0',
                    'Set WshShell = Nothing']
        else:
            spis = ['Set WshShell = CreateObject("WScript.Shell")',
                    rf'WshShell.Run chr(34) & "{put_new_embed}\run.bat" & Chr(34)']
        F.zap_f(file_zapysk, spis, separ='', utf8=True)
        put_ico = put_new_embed + F.sep() + r'icons\1.ico'
        ico = ''
        if F.nalich_file(put_ico):
            ico = put_ico
        F.sozd_yarlik(file_zapysk, path_local, name, ico)


    @CQT.onerror
    def load_setup(self):
        tbl = self.ui.tbl_spis_prog
        self.ui.groupBox_2.setTitle('Установка')
        CQT.clear_tbl(tbl)

        spis_prog_ust = []
        if F.nalich_file(self.PUT_PO_UMOLCH + 'cache.txt'):
            spis_prog_ust = [_[0] for _ in F.otkr_f(self.PUT_PO_UMOLCH + 'cache.txt', True, '|')]
        spis_prog = []
        for key in self.DICT_PROG:
            if key not in spis_prog_ust:
                spis_prog.append(
                    [self.DICT_PROG[key]['Имя'], self.DICT_PROG[key]['Путь'], self.DICT_PROG[key]['Название']])
        spis_prog.insert(0, ['img', 'Имя', "Путь", 'Установить'])
        for i in range(1, len(spis_prog)):
            spis_prog[i].insert(0, '')
            spis_prog[i].append('')
        CQT.zapoln_wtabl(self, spis_prog, tbl, separ='', isp_shapka=True)
        nk_ima = CQT.nom_kol_po_imen(tbl, 'Имя')
        nk_put = CQT.nom_kol_po_imen(tbl, 'Путь')
        nk_isp_f = CQT.nom_kol_po_imen(tbl, 'img')
        nk_zap = CQT.nom_kol_po_imen(tbl, 'Установить')

        tbl.setColumnHidden(nk_put, True)
        for i in range(tbl.rowCount()):
            ima = tbl.item(i, nk_ima).text()
            path = F.sep().join((self.DICT_PROG[ima]['Путь'], 'embed', 'icons', '1.ico'))
            if F.nalich_file(path):
                CQT.add_image(tbl, i, nk_isp_f, path, w=tbl.rowHeight(i), h=tbl.rowHeight(i))
            CQT.add_btn(tbl, i, nk_zap, 'Установить', True, self.setup_prog,
                        img_path=F.sep().join(('icons', '41.png')), height=tbl.rowHeight(i), fontsize = 14)
        # =======================================
        self.click_setup()
        tbl.horizontalHeader().hide()
        tbl.resizeColumnsToContents()

    @CQT.onerror
    def setup_prog(self, r, c):
        tbl = self.ui.tbl_spis_prog
        rez = self.check_put()
        if rez != True:
            CQT.msgbox(rez)
            return
        nk_name = CQT.nom_kol_po_imen(tbl, 'Имя')
        name = tbl.item(r, nk_name).text()
        dir_mes = self.ui.le_putust.text()
        ima_new_papki = F.clear_pod_ima_faila(F.transliteration(self.DICT_PROG[name]['Имя']))
        put_new = dir_mes + ima_new_papki
        if F.nalich_file(put_new):
            try:
                F.udal_papky(put_new)
            except:
                CQT.msgbox('Целевая папка занята, необходимо закрыть все используемые файлы '
                           'или перезагрузить компьютер')
                return
        try:
            F.sozd_dir(put_new)
        except:
            pass
        spis_cache = [[k, self.DICT_LOCAL_PROG[k]] for k in self.DICT_LOCAL_PROG.keys()]
        fl = True
        for item in spis_cache:
            if item[0] == name:
                fl = False
                break
        if fl:
            spis_cache.append([name, put_new])
            F.zap_f(self.PUT_PO_UMOLCH + 'cache.txt', spis_cache, '|', utf8=True)
            self.DICT_LOCAL_PROG = self.load_local_prog()
        self.update_prog(r, c, self.ui.tbl_spis_prog)

    @CQT.onerror
    def zapusk_prog(self, row, col):
        tbl = self.ui.tbl_spis_prog_update
        nk_name = CQT.nom_kol_po_imen(tbl, 'Имя')
        name = tbl.item(row, nk_name).text()
        path = self.DICT_LOCAL_PROG[name]
        local_name_emb = 'embed'
        if platform.win32_ver()[0] == '7':
            local_name_emb = 'embed_win7'
        if F.nalich_file(path + F.sep() + local_name_emb + F.sep() + 'window_free.vbs'):
            F.zapyst_file(path + F.sep() + name + '.lnk')
            sys.exit()
        else:
            CQT.msgbox('Не найден файл запуска')

    @CQT.onerror
    def click_reload(self):
        self.ui.le_putust.setText('')
        self.ui.le_putust.setEnabled(False)

    @CQT.onerror
    def click_setup(self):
        self.ui.le_putust.setText(self.PUT_PO_UMOLCH)
        self.ui.le_putust.setEnabled(True)

    @CQT.onerror
    def cache_load(self, ima):
        if F.nalich_file(self.PUT_PO_UMOLCH + 'cache.txt'):
            spis_cache = F.otkr_f(self.PUT_PO_UMOLCH + 'cache.txt', True, '|')
            for i in range(len(spis_cache)):
                if spis_cache[i][0] == ima:
                    return spis_cache[i][1]

    @CQT.onerror
    def cache_add(self, ima, path):
        if F.nalich_file(self.PUT_PO_UMOLCH + 'cache.txt'):
            spis_cache = F.otkr_f(self.PUT_PO_UMOLCH + 'cache.txt', True, '|')
        else:
            spis_cache = []
        put_old = ''
        for i in range(len(spis_cache)):
            if spis_cache[i][0] == ima:
                put_old = spis_cache[i][1]
                spis_cache[i][1] = path
                break
        if put_old == '':
            spis_cache.append([ima, path])
        F.zap_f(self.PUT_PO_UMOLCH + 'cache.txt', spis_cache, '|', utf8=True)

    @CQT.onerror
    def check_put(self):
        if F.check_for_russian(self.ui.le_putust.text()) == True:
            return f'Не допустима киррилица в пути к папке'
        if F.nalich_file(self.ui.le_putust.text()) == False:
            return f'Путь установки не существует'
        return True

app = QtWidgets.QApplication(sys.argv)

args = sys.argv[1:]

myappid = 'Powerz.BAG.SustControlWork.0.0.0'  # !!!
QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
app.setWindowIcon(QtGui.QIcon(os.path.join("icons", "icon.png")))
print(QtWidgets.QStyleFactory.keys())
S = F.scfg('Stile').split(",")
if len(S) > 1:
    app.setStyle(S[1])

application = mywindow()
application.show()

sys.exit(app.exec())

# pyinstaller.exe --onefile --icon=1.ico --noconsole Setup.py
