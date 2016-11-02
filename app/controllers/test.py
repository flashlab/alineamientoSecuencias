

    class enzima:
        hash = {}
        nombre = ""

        def init(enzima, sustrato, producto, nombre):
            self.hash = {"enzima": enzima, "sustrato": sustrato, "producto": producto}
            self.nombre = nombre




myEnzima = new enzima(123,34534, 345, "XXXXasa")


    myEnzima.hash["producto"] => 345
    myEnzima.nombre => "XXXXasa"

