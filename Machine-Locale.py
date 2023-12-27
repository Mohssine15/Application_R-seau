import os
import platform
import socket
import psutil
import nmap
import subprocess

from getmac import get_mac_address as gmac
from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QPushButton, QTextEdit, QMainWindow, QFormLayout, QCompleter, QStyle


class FenPrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Coolmap')
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.setWindowIcon(QIcon('./pic/coolmap.png'))
        self.resize(800, 800)

        #Création de GridLayout
        self.layout = QGridLayout(self.widget)
        self.widget.setLayout(self.layout)
        #Création de label détails
        self.label = QLabel("Détails", self.widget)
        self.layout.addWidget(self.label, 1, 0)
        # Création de champs texte multi lignes
        self.textEdit = QTextEdit(self.widget)
        self.textEdit.setReadOnly(True)  # Désactivez la modification
        self.textEdit.setFixedWidth(850)
        self.layout.addWidget(self.textEdit, 2, 0, 1, 5)

        # Créer un menu
        menubar = self.menuBar()

        # Menu Machine locale
        self.MachineLocalMenu = menubar.addMenu('&Machine locale')

        #Menu Machine Locale =====> Système
        open_action = QAction(QIcon("./pic/systeme.jpg"), '&Système', self)
        self.MachineLocalMenu.addAction(open_action)
        # open_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        open_action.setShortcut('Ctrl+S')
        open_action.triggered.connect(self.systeme)

        #Menu Machine Locale =====> Disques
        open_action = QAction(QIcon("./pic/hdd.jpg"),'&Disques', self)
        self.MachineLocalMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+D')
        open_action.triggered.connect(self.disques)

        #Menu Machine Locale =====> Interfaces réseau
        open_action = QAction(QIcon("./pic/nic.png"),'&Interfaces réseau', self)
        self.MachineLocalMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+I')
        open_action.triggered.connect(self.interfacesReseau)

        # Menu Réseau
        self.reseauMenu = menubar.addMenu("Réseau")

        # Menu Réseau =====> Infos
        open_action = QAction(QIcon("./pic/localhost.jpg"),'&Localhost', self)
        self.reseauMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+L')
        open_action.triggered.connect(self.localhost)

        # Menu Réseau =====> Ipconfig
        open_action = QAction(QIcon("./pic/ip.png"), 'I&pconfig', self)
        self.reseauMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+P')
        open_action.triggered.connect(self.ipconfig)

        # Menu Commandes
        self.comReseauMenu = menubar.addMenu("Commandes")

        # Menu Commandes =====> Scan
        open_action = QAction(QIcon("./pic/scan.png"),"Sca&n", self)
        self.comReseauMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+N')
        open_action.triggered.connect(self.btnScanClicked)

        # Menu Commandes=====> Ping
        open_action = QAction(QIcon("./pic/coolmap.png"),"Pin&g", self)
        self.comReseauMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+G')
        open_action.triggered.connect(self.btnPingClicked)

        # Menu Commandes=====> Tracert
        open_action = QAction(QIcon("./pic/tracert.png"),"&Tracert", self)
        self.comReseauMenu.addAction(open_action)
        open_action.setShortcut('Ctrl+T')
        open_action.triggered.connect(self.btnPingClicked)

        # Menu Help
        self.comReseauMenu = menubar.addMenu("&Help")

        # Menu Help=====> À propos
        open_action = QAction(QIcon("./pic/about.png"), "À propos", self)
        self.comReseauMenu.addAction(open_action)
        open_action.triggered.connect(self.btnPingClicked)

        #label Target
        self.label = QLabel("Target :", self.widget)
        self.layout.addWidget(self.label, 0, 0)
        self.label.setFixedSize(50, 25)
        #Line texte
        self.lineEdit = QLineEdit(self.widget, placeholderText='Entrer une adresse IP ou un nom de domaine', clearButtonEnabled=True)
        self.layout.addWidget(self.lineEdit, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.lineEdit.setFixedSize(400, 34)
        self.liste = QCompleter(['localhost', '10.0.0.219', 'Moi', 'Toi', '127.0.0.1'])
        self.lineEdit.setCompleter(self.liste)
        #Bouton scan
        self.btnScan = QPushButton("   Scan", self.widget)
        self.layout.addWidget(self.btnScan, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.btnScan.setIcon(QIcon('./pic/scan.png'))
        self.btnScan.setFixedSize(120, 34)
        self.btnScan.clicked.connect(self.btnScanClicked)
        #bouton ping
        self.btnPing = QPushButton("   Ping", self.widget)
        self.layout.addWidget(self.btnPing, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.btnPing.setIcon(QIcon('./pic/coolmap.png'))
        self.btnPing.setFixedSize(120, 34)
        self.btnPing.clicked.connect(self.btnPingClicked)
        # bouton tracert
        self.btnTracert = QPushButton("   Tracert", self.widget)
        self.layout.addWidget(self.btnTracert, 0, 4, alignment=Qt.AlignmentFlag.AlignLeft)
        self.btnTracert.setIcon(QIcon('./pic/tracert.png'))
        self.btnTracert.setFixedSize(120, 34)
        self.btnTracert.clicked.connect(self.btnTracertClicked)
    def systeme(self):
        self.textEdit.clear()  # Efface le texte existant
        self.textEdit.append("============= Localhost détails =============")  # Ajoute le nouveau texte
        # Obtenir la vitesse du processeur en MHz
        cpu_speed = psutil.cpu_freq().current
        # Obtenir des informations sur la RAM
        ram_info = psutil.virtual_memory()
        # Extraire la capacité totale, la capacité utilisée et le pourcentage d'utilisation
        total_ram = ram_info.total / (1024 * 1024)  # Convertir de bytes à megabytes
        used_ram = ram_info.used / (1024 * 1024)
        percent_used = ram_info.percent

        processor_name = platform.processor()
        # print(f"Processeur                        : {processor_name}")
        num_cores = os.cpu_count()
        # print(f"Nombre de cœurs                   : {num_cores}")
        architecture = platform.architecture()[0]
        # print(f"Architecture du processeur        : {architecture}")
        processor_speed = platform.processor()
        #recuperation de hostname
        hostname = socket.gethostname()
        # print(f"Nom d'hôte : {hostname}")
        self.text = (f"Nom d'hôte                              : {hostname}" +"\n"
                     "Système d'exploitation           : " + os.name.upper() +" " + platform.system() + " " + platform.release()+"\n"+
                     f"Type de système                     : Système d’exploitation {architecture}" +"\n"
                     f"Processeur                              : {processor_name}" +"\n"
                     f"Vitesse du processeur           : {cpu_speed/1000:.2f} GHz" +"\n"
                     f"Nombre de cœurs                   : {num_cores} Coeurs" +"\n"
                     f"Architecture du processeur    : {architecture}" +"\n"
                     f"Mémoire vive installée            : {total_ram/1024:.2f} Go" +"\n"
                     f"Mémoire vive utilisée              : {used_ram/1024:.2f} Go" +"\n"
                     f"Pourcentage d'utilisation        : {percent_used:.2f}%" +"\n"
                     )
        replacement_text = self.text
        self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
    def disques(self):
        self.textEdit.clear()  # Efface le texte existant
        self.textEdit.append("========= Les disques installés ============")  # Ajoute le nouveau texte
        #recupération des disques installés
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(partition)
            # print(f"Nom du disque : {partition.device}")
            # print(f"Point de montage : {partition.mountpoint}")
            # print(f"Système de fichiers : {partition.fstype}")
            disk_usage = psutil.disk_usage(partition.mountpoint)
            # print(f"Taille totale : {disk_usage.total / (1024 ** 3):.2f} Go")
            # print(f"Espace libre : {disk_usage.free / (1024 ** 3):.2f} Go")
            # print(f"Espace utilisé : {disk_usage.used / (1024 ** 3):.2f} Go")
            # print(f"Taux d'utilisation : {disk_usage.percent}%\n")
            self.text = (
                    f"Nom du disque : {partition.device}" + "\n" +
                    f"Système de fichiers : {partition.fstype}" + "\n" +
                    f"Taille totale : {disk_usage.total / (1024 ** 3):.2f} Go" + "\n" +
                    f"Espace libre : {disk_usage.free / (1024 ** 3):.2f} Go" + "\n" +
                    f"Espace utilisé : {disk_usage.used / (1024 ** 3):.2f} Go" + "\n" +
                    f"Taux d'utilisation : {disk_usage.percent}%\n"
                    "---------------------------------------------"
            )
            # print(self.text)
            replacement_text = self.text
            self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
            print(self.text)
    def interfacesReseau(self):
        self.textEdit.clear()  # Efface le texte existant
        self.textEdit.append("============= Interfaces réseau =============")  # Ajoute le nouveau texte
        #Récupération des information des interfaces réseau
        interfaces = psutil.net_if_stats()
        for interface, stats in interfaces.items():
            self.text = (
                    f"Interface : {interface}" + "\n" +
                    f"  Statut : {'Actif' if stats.isup else 'Inactif'}" + "\n" +
                    f"  Vitesse : {stats.speed} Mbps\n" 
                    "---------------------------------------------"
            )
            replacement_text = self.text
            self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
    def localhost(self):
        self.textEdit.clear()  # Efface le texte existant
        self.textEdit.append("============= Localhost : Informations réseau =============")  # Ajoute le nouveau texte
        # Exécutez la commande PowerShell pour obtenir le nom du domaine ou du groupe de travail
        domain = subprocess.run(["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"],
                                stdout=subprocess.PIPE, text=True).stdout.strip()
        # recupération d'adresse IP
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        #recupération d'adresse MAC
        win_mac = gmac(interface="Ethernet")  # Remplacez par le nom de l'interface souhaitée
        self.text = (
                f"Hostname                                                  : {hostname}" + "\n" +
                f"L'adresse IP                                              : {ip}" + "\n" +
                f"L'adresse MAC                                        : {win_mac}" + "\n"
                f"Nom de domain ou groupe de travail     : {domain}"
        )
        replacement_text = self.text
        self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
    def ipconfig(self):
        self.textEdit.clear()  # Efface le texte existant
        # récupération de ipconfig
        # Exécutez la commande 'ipconfig' (Windows)
        result = os.popen('ipconfig').read()
        # Recherchez la ligne contenant le masque de sous-réseau
        for line in result.splitlines():
            if 'Carte Ethernet Ethernet ' in line:
                subnet_mask = line.split(':')[-1].strip()
                print(f"Le masque de sous-réseau est : {subnet_mask}")
                break
        # Recherchez la ligne contenant la passerelle par défaut
        for line in result.splitlines():
            if 'Passerelle par défaut' in line:
                gateway = line.split(':')[-1].strip()
                print(f"La passerelle par défaut est : {gateway}")
                break

        self.text = (
                f" {result}"
        )
        replacement_text = self.text
        self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
    def btnPingClicked(self):
        self.textEdit.clear()  # Efface le texte existant
        # récupération de ipconfig
        # Exécutez la commande 'ipconfig' (Windows)
        result = os.popen("ping " + self.lineEdit.text()).read()
        self.text = (
                f" {result}"
        )
        replacement_text = self.text
        self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
    def btnScanClicked(self):
        self.textEdit.clear()  # Efface le texte existant
        remote_host = self.lineEdit.text()
        # print(remote_host)
        try:
            remote_hostname = socket.gethostbyaddr(remote_host)[0]
            self.textEdit.append("======= Information sur l'hôte =======")
            self.textEdit.append("L'adresse IP: " + remote_host)
            self.textEdit.append(f"Hostname: {remote_hostname}")
            # print("======= Information sur l'hôte =======")
            # print("L'adresse IP: " + remote_host)
            # print(f"Hostname: {remote_hostname}")
        except socket.herror:
            print("Impossible de résoudre le nom d'hôte pour l'adresse IP spécifiée.")

        # self.textEdit.clear()  # Efface le texte existant
        # Créez un objet Nmap PortScanner
        nmScan = nmap.PortScanner()
        # Scannez l'adresse IP spécifiée pour les ports de 21 à 65000
        nmScan.scan(self.lineEdit.text(), '10-65000')
        resultat = []
        # Récupérez les détails de l'analyse
        for host in nmScan.all_hosts():
            # print(f"Host : {host} ({nmScan[host].hostname()})")
            # print(f"State : {nmScan[host].state()}")
            for port in nmScan[host]['tcp']:
                print(
                    f"Port : {port} | State : {nmScan[host]['tcp'][port]['state']} | Service : {nmScan[host]['tcp'][port]['name']}")
                resultat.append( f" {port}  |  {nmScan[host]['tcp'][port]['state']}  |  {nmScan[host]['tcp'][port]['name']}")
        print("============================================")
        print(resultat)
        self.textEdit.append("========= Résultats du scan ========")
        self.textEdit.append(f"Host : {host} ({nmScan[host].hostname()})")
        self.textEdit.append(f"State : {nmScan[host].state()}")
        self.textEdit.append("PORT | STATE  |  SERVICE")
        print("PORT | STATE  |  SERVICE")
        for x in resultat:
            print(x)
            replacement_text = x
            self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
            # print(self.text.encode(encoding="UTF-8"))
    def btnTracertClicked(self):
        self.textEdit.clear()  # Efface le texte existant
        #
        # # Récupérez l'argument de ligne de commande (adresse IP ou nom de domaine)
        # target = self.lineEdit.text()
        # # Exécutez la commande tracert
        # print(target)
        # os.system(f"tracert {target}")
        # print(f"tracert {target}")
        # result = os.system(f"tracert {target}")
        # # for x in result:
        # #     print("x = " + x)
        # self.text = (
        #     f" {result}"
        # )
        # replacement_text = self.text
        # self.textEdit.append(replacement_text)  # Ajoute le nouveau texte

app = QApplication([])
fen = FenPrincipale()
app.setStyleSheet(Path('style.qss').read_text())
fen.show()
app.exec()