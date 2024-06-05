from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QRect

from .mainwindow import MainWindow
from ..utils import *


class Patoc(QApplication):
    """The Patoc application"""

    def __init__(self) -> None:
        super().__init__()

        self.setApplicationName("Patoc")
        self.setDesktopFileName('Patoc')
        self.setApplicationVersion('0.1')
        self.setStyle("Fusion")
        self.main_window = MainWindow(self)
        self.main_window.setWindowTitle("Patoc")
        self.main_window.setWindowIcon(QIcon(get_data('../icons/icon.png')))
        self.setWindowIcon(self.main_window.windowIcon())
        # screenrect = self.primaryScreen().geometry()
        # self.main_window.move(screenrect.right(), screenrect.top())
        self.main_window.show()


def main() -> None:
    """Main entry point for Patoc"""
    
    print("--- Patoc: a graphical tool for quantum circuits ---")
    patoc = Patoc()
    patoc.exec()

    # from data.examples import circuit1, subcircuit1, czLHS

    # print("The big circuit is ")
    # circuit1.print()
    # print("------------------------------")
    # print("The small circuit is ")
    # subcircuit1.print()
    # print("------------------------------")
    # circuit1.matchAxiom(subcircuit1)
    # print("------------------------------")



    # from openqasm3 import parser
    # from openqasm3.ast import QuantumGate
    # from openqasm3.ast import QubitDeclaration
    # q = 'OPENQASM 3.0;include "stdgates.inc";qubit[2] q;h q[1];cx q[0], q[1];h q[1];'
    # p = "OPENQASM 3.0;qubit[2] q;"
    # s = parser.parse(q).statements
    # for x in s:
    #     print("----------------------------")
    #     print(x)
    #     print(type(x)==QuantumGate)