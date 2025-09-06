#Jason Misael Gutierrez de Leon 1624622
#Miguel Alfonso Macario Velásquez 1597421

class RouterHash:
    def __init__(self, size=5):
        self.size = size
        self.table = [None] * size  # Tabla hash vacía

    def ip_to_int(self, ip):
        """Convierte una IP en número entero"""
        octetos = list(map(int, ip.split(".")))
        return (octetos[0] << 24) + (octetos[1] << 16) + (octetos[2] << 8) + octetos[3]

    def hash_function(self, ip):
        """Calcula el índice hash"""
        return self.ip_to_int(ip) % self.size

    def add_route(self, ip, interfaz):
        """Agrega una ruta con sondeo lineal"""
        index = self.hash_function(ip)
        for i in range(self.size):
            new_index = (index + i) % self.size
            if self.table[new_index] is None or self.table[new_index][0] == ip:
                self.table[new_index] = (ip, interfaz)
                print(f"[+] Ruta agregada: {ip} -> {interfaz} en índice {new_index}")
                return
        print("[!] Tabla llena, no se pudo agregar la ruta.")

    def search_route(self, ip):
        """Busca una ruta con sondeo lineal"""
        index = self.hash_function(ip)
        for i in range(self.size):
            new_index = (index + i) % self.size
            if self.table[new_index] is None:
                return None  # No encontrada
            if self.table[new_index][0] == ip:
                return self.table[new_index][1]
        return None

    def delete_route(self, ip):
        """Elimina una ruta"""
        index = self.hash_function(ip)
        for i in range(self.size):
            new_index = (index + i) % self.size
            if self.table[new_index] is None:
                return False
            if self.table[new_index][0] == ip:
                print(f"[-] Eliminando ruta: {ip} -> {self.table[new_index][1]}")
                self.table[new_index] = None
                return True
        return False

    def simulate_packet(self, ip):
        """Simula la llegada de un paquete"""
        interfaz = self.search_route(ip)
        if interfaz:
            print(f"Paquete con destino {ip} enviado por {interfaz}")
        else:
            print(f"No se encontró ruta para {ip}, paquete descartado")

    def show_table(self):
        """Muestra la tabla hash"""
        print("\nTabla Hash:")
        for i, entry in enumerate(self.table):
            print(f"Índice {i}: {entry}")
        print("")


# Ejemplo de uso
router = RouterHash(size=5)

router.add_route("192.168.1.1", "eth0")
router.add_route("10.0.0.2", "eth1")
router.add_route("172.16.5.10", "eth2")
router.add_route("8.8.8.8", "eth3")
router.add_route("192.168.1.99", "eth0")

router.show_table()

router.simulate_packet("192.168.1.1")
router.simulate_packet("8.8.8.8")
router.simulate_packet("1.1.1.1")  # no existe

router.delete_route("10.0.0.2")
router.show_table()
