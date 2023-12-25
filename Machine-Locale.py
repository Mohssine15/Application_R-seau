import os
import platform
from pathlib import Path

import psutil
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QPushButton, QTextEdit, QMainWindow, QFormLayout


class FenPrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coolmap")
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.setWindowIcon(QIcon('./coolmap.png'))
        self.resize(800, 800)


        #Création de GridLayout
        self.layout = QGridLayout(self.widget)
        self.widget.setLayout(self.layout)
        #Création de label détails
        self.label = QLabel("Détails", self.widget)
        self.layout.addWidget(self.label, 1, 0)
        # Création de champs texte multi lignes
        self.textEdit = QTextEdit(self.widget)
        self.textEdit.setFixedWidth(700)
        self.layout.addWidget(self.textEdit, 2, 0, 1, 3)

        # Créer un menu
        menubar = self.menuBar()

        # Créer un menu "Fichier"
        self.MachineLocalMenu = menubar.addMenu("Machine locale")
        # Ajouter une action au menu "Machine locale"
        open_action = QAction("Système", self)
        self.MachineLocalMenu.addAction(open_action)
        # Connecter l'action à une fonction
        open_action.triggered.connect(self.systeme)

        open_action = QAction("Disques", self)
        self.MachineLocalMenu.addAction(open_action)
        # Connecter l'action à une fonction
        open_action.triggered.connect(self.disques)

        open_action = QAction("Interfaces réseau", self)
        self.MachineLocalMenu.addAction(open_action)
        # Connecter l'action à une fonction
        open_action.triggered.connect(self.interfacesReseau)

        self.reseauMenu = menubar.addMenu("Réseau")
        self.open_action = QAction("Info Réseau", self)
        self.reseauMenu.addAction(self.open_action)

        self.comReseauMenu = menubar.addMenu("Commandes réseau")
        self.open_action = QAction("Info Réseau", self)
        self.comReseauMenu.addAction(self.open_action)

    def systeme(self):
        # Obtenir la vitesse du processeur en MHz
        cpu_speed = psutil.cpu_freq().current
        # Obtenir des informations sur la RAM
        ram_info = psutil.virtual_memory()
        # Extraire la capacité totale, la capacité utilisée et le pourcentage d'utilisation
        total_ram = ram_info.total / (1024 * 1024)  # Convertir de bytes à megabytes
        used_ram = ram_info.used / (1024 * 1024)
        percent_used = ram_info.percent

        processor_name = platform.processor()
        print(f"Processeur                        : {processor_name}")
        num_cores = os.cpu_count()
        print(f"Nombre de cœurs                   : {num_cores}")
        architecture = platform.architecture()[0]
        print(f"Architecture du processeur        : {architecture}")
        processor_speed = platform.processor()

        self.text = ("Système d'exploitation       : " + os.name.upper() +" " + platform.system() + " " + platform.release()+"\n"+
                     f"Type de système                : Système d’exploitation {architecture}" +"\n"
                     f"Processeur                         : {processor_name}" +"\n"
                     f"Vitesse du processeur        : {cpu_speed/1000:.2f} GHz" +"\n"
                     f"Nombre de cœurs              : {num_cores} Coeurs" +"\n"
                     f"Architecture du processeur : {architecture}" +"\n"
                     f"Mémoire vive installée        : {total_ram/1024:.2f} Go" +"\n"
                     f"Mémoire vive utilisée          : {used_ram/1024:.2f} Go" +"\n"
                     f"Pourcentage d'utilisation     : {percent_used:.2f}%" +"\n"
                     )
        replacement_text = self.text
        self.textEdit.clear()  # Efface le texte existant
        self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
        print(self.text)
    def disques(self):
        self.textEdit.clear()  # Efface le texte existant
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
                    f"Point de montage : {partition.mountpoint}" + "\n" +
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
        #Récupération des information des interfaces réseau
        interfaces = psutil.net_if_stats()
        for interface, stats in interfaces.items():
            self.text = (
                    f"Interface : {interface}" + "\n" +
                    f"  Statut : {'Actif' if stats.isup else 'Inactif'}" + "\n" +
                    f"  Vitesse : {stats.speed} Mbps\n" + "\n" +
                    "---------------------------------------------"
            )
            # print(f"Interface : {interface}")
            # print(f"  Statut : {'Actif' if stats.isup else 'Inactif'}")
            # # print(f"  Adresse MAC : {stats.address}")
            # print(f"  Vitesse : {stats.speed} Mbps\n")

            replacement_text = self.text
            self.textEdit.append(replacement_text)  # Ajoute le nouveau texte
            print(self.text)




app = QApplication([])
fen = FenPrincipale()
# app.setStyleSheet(Path('login.qss').read_text())
fen.show()
app.exec()