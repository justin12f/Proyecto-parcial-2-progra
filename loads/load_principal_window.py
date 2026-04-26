from PyQt5 import QtWidgets, uic
from loads.load_regresion_lineal import LoadRegresionLineal
from loads.load_integracion import LoadIntegracion
from loads.load_integracion_inversa import LoadIntegracionInversa
from loads.load_significancia import LoadSignificancia

# Importamos nuestra nueva calculadora de álgebra
from loads.load_algebra_lineal import LoadAlgebraLineal


class LoadPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/main_window.ui", self)
        self.show()

        # --- CONEXIONES DEL MENÚ SUPERIOR (ACTIONS) ---
        # (Corregí el cruce que había entre Regresión e Integración)
        self.actionRegresion.triggered.connect(self.regresion)
        self.actionIntegracion.triggered.connect(self.integracion)
        self.actionIntegracionInversa.triggered.connect(self.integracion_inversa)
        self.actionSignificancia.triggered.connect(self.significancia)

        # Conexión para el nuevo action de Álgebra
        self.actionAlgebraLineal.triggered.connect(self.algebra_lineal)

        # --- CONEXIONES DE LOS BOTONES EN PANTALLA ---
        self.btnRegresion.clicked.connect(self.regresion)
        self.btnIntegracion.clicked.connect(self.integracion)
        self.btnIntegracionInversa.clicked.connect(self.integracion_inversa)
        self.btnSignificancia.clicked.connect(self.significancia)

        # Conexión para el nuevo botón de Álgebra
        self.btnAlgebraLineal.clicked.connect(self.algebra_lineal)

    # --- MÉTODOS PARA ABRIR LAS VENTANAS ---
    def regresion(self):
        self.loadregresion = LoadRegresionLineal()

    def integracion(self):
        self.loadintegracion = LoadIntegracion()

    def integracion_inversa(self):
        self.loadintegracioninversa = LoadIntegracionInversa()

    def significancia(self):
        self.loadsignificancia = LoadSignificancia()

    # Nuevo método para abrir la herramienta de Álgebra Lineal
    def algebra_lineal(self):
        self.loadalgebra = LoadAlgebraLineal()
