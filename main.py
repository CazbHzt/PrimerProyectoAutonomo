import json
import time

# ! Ejercicio que hice anteriormente de vuelta desde cero con metodos y clases

class Producto:
    def __init__(self,id: int,nombre:str,precio: int ,stock_actual:int ,stock_minimo:int):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        
    def venta(self,cantidad):
        if cantidad > self.stock_actual:
            return "No hay suficiente Stock"
        
        if cantidad <= 0:
            return "Ingrese una cantidad valida"
        
        self.stock_actual -= cantidad
        
        return self.stock_actual

    
    def convertir_json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo
        }
        
class Tienda:
    def __init__(self):
        self.inventario: dict[int,Producto] = {}
        
    def registrar_producto(self,id,nombre,precio,s_a,s_m):
        
        if not isinstance(id, int) or not isinstance(nombre, str) or not isinstance(precio,(int,float)) or not isinstance(s_a,int) or not isinstance(s_m,int):
            return "Valor ingresado no coincide con el tipo de dato solicitado"
        
        if id in self.inventario:
            return False, "Ya existe producto con esa ID"
        
        producto = Producto(id,nombre,precio,s_a,s_m)
        self.inventario[producto.id] = producto
        
        return True, "Producto registrado exitosamente"
    
    def alerta(self):
            alertas = []
            for producto in self.inventario.values():
                if producto.stock_actual <= producto.stock_minimo:
                    alertas.append(producto)
            return alertas
        
    def procesar_venta(self, carrito: list[tuple[int,int]]):
        
        for id_prod , cantidad in carrito:
            
            if id_prod not in self.inventario:
                return "Producto no encontrado"
            
            producto = self.inventario[id_prod]
            
            if cantidad > producto.stock_actual:
                return "Stock insuficiente"
            
        total = 0.0
        
        for id_prod, cantidad in carrito:
            
            producto = self.inventario[id_prod]
            
            producto.venta(cantidad)
            
            total += cantidad * producto.precio
            
        return True

    def modificar(self,id,n_nom,n_pre,n_s_a,n_s_m):
        
        if id not in self.inventario:
            return False, "No se encontro producto con ese id"
        
        producto = self.inventario[id]
        
        if n_nom is not None and n_nom.strip() != "":
            producto.nombre = n_nom
        if n_pre is not None and isinstance(n_pre,(int,float)):
            producto.precio = n_pre
        if n_s_a is not None:
            producto.stock_actual = n_s_a
        if n_s_m is not None:
            producto.stock_minimo = n_s_m
            
        return True, "Producto modificado exitosamente"
            
    def eliminar(self,id):
        
        if id in self.inventario:
            del self.inventario[id]
            return True, "Producto eliminado exitosamente"
        else:
            return False, "no se encontro producto con esa id"

    def guardar_archivo(self,nombre_archivo = "inventario.json"):
        
        datos_guardados = [producto.convertir_json() for producto in self.inventario.values()]
        
        with open(nombre_archivo, "w" , encoding="utf-8") as archivo:
            json.dump(datos_guardados,archivo,indent=4)
            
        print("Datos guardados con exito")
            
    def cargar_archivo(self,nombre_archivo = "inventario.json"):
        
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                
                cargados = json.load(archivo)
                
                self.inventario.clear()
                
                for items in cargados:
                    
                    producto = Producto(
                        id=items["id"],
                        nombre=items["nombre"],
                        precio=items["precio"],
                        stock_actual=items["stock_actual"],
                        stock_minimo=items["stock_minimo"]
                    )
                
                    self.inventario[producto.id] = producto
                    
                print("Archivo cargado exitosamente")
        except FileNotFoundError:
            print("Archivo no encontrado, Creando uno nuevo")
            
def main():
    
    tienda = Tienda()
    
    tienda.cargar_archivo()
    while True:
        
        print("---/// Menu Principal ///---")
        print("1. Registrar producto")
        print("2. Procesar Venta")
        print("3. Modificar o Eliminar")
        print("4. Alerta Producto")
        print("5. Guardar y Salir")
        
        try:
            accion = int(input("Ingrese la accion a realizar 1-5: "))
        except ValueError:
            print("Debe ingresar un numero") 
            continue
    
        if accion == 1:
            print("Ingrese los datos del producto: [ID,NOMBRE,PRECIO,STOCK_ACTUAL,STOCK_MINIMO]")
            try:
                id = int(input("ID: "))
                nombre = str(input("Nombre: "))
                precio = float(input("Precio: "))
                st_act = int(input("Stock Actual: "))
                st_min = int(input("Stock Minimo: "))
                
            except ValueError:
                print("Dato ingresado erroneo")
            except TypeError as e:
                print(e)
                continue
            
            _,msj = tienda.registrar_producto(id,nombre,precio,st_act,st_min)
            print(msj)
                
        elif accion == 2:
            
            if not tienda.inventario:
                print("No hay inventario")
                continue
            
            carrito = []
            
            print("Ingrese -1 en ID para salir.")
            
            while True:
                try:
                    id_proc = int(input("Ingrese la ID a procesar: "))
                except ValueError:
                    print("Dato ingresado incorrecto")
                    continue
                
                if id_proc == -1:
                    break
                
                if id_proc not in tienda.inventario:
                    print("No se encontro producto con esa ID")
                    continue
                
                producto = tienda.inventario[id_proc]
                
                try:
                    cantidad = int(input("Cantidad a procesar: "))
                except ValueError:
                    print("Dato ingresado incorrecto")
                    continue
                
                if cantidad <=0:
                    print("Cantidad no valida")
                    continue
                
                if cantidad > producto.stock_actual:
                    print("No hay stock suficiente")
                    continue
                
                carrito.append((id_proc,cantidad))
                print(f"Producto procesado ({producto.nombre} x {cantidad})")
                
            resultado = tienda.procesar_venta(carrito)
            
            if isinstance(resultado,str):
                print(resultado)
            else:
                print("Venta exitosa")
                
        elif accion == 3:
            
            if not tienda.inventario:
                print("No hay inventario Regresando")
                continue
            try:
                prod_id = int(input("Ingrese el ID del producto: "))
            except ValueError:
                print("Valor ingresado erroneo")
                continue
            
            if prod_id not in tienda.inventario:
                print("No hay producto con esa ID")
                continue
            
            prod = tienda.inventario[prod_id]
            
            print(f"Producto Encontrado {prod.id} nombre: {prod.nombre}\n")    
            print("Ingrese la accion a realizar")
            print("1. Modificar Producto")
            print("2. Eliminar Producto\n")
            
            try:
                sub_opcion = int(input("Ingrese la accion a realizar: "))
            except ValueError:
                print("Valor ingresado Erroneo")
                continue
            
            if sub_opcion == 1:
                
                try:
                    nuevo_nom = str(input("Ingrese el nuevo nombre: "))
                    nuevo_prec = float(input("Ingrese el nuevo precio: "))
                    nuevo_s_a = int(input("Ingrese el nuevo stock actual: "))
                    nuevo_s_m = int(input("Ingrese el nuevo stock_minimo: "))
                except ValueError:
                    print("Valor ingresado erroneo")
                except TypeError as e:
                    print(e)
                    continue
                    
                _,msj = tienda.modificar(prod_id, nuevo_nom,nuevo_prec,nuevo_s_a,nuevo_s_m)
                
                print(msj)
                
            elif sub_opcion == 2:
                
                print("Estas seguro que deseas eliminar este producto? [s/n]")
                try:
                    resp = str(input("Ingrese su respuesta: "))
                except ValueError:
                    print("Valor ingresado erroneo")
                    continue
                
                if resp.lower() == 's':
                    _,msj= tienda.eliminar(prod_id)
                    print(msj)
                elif resp.lower() == 'n':
                    print("Accion cancelada")
                else:
                    print("No ingreso el valor correcto, cancelando operacion")
                
            else:
                print("Opcion ingresada no valida")
                continue
            
            
        elif accion == 4:
            
            alerta = tienda.alerta()
            
            if not alerta:
                print("No hay producto en riesgo de stock")
            else:
                print(" PRODUCTOS EN ALERTA DE STOCK !!!")
                for producto in alerta:
                    print(f"Producto: {producto.id} Nombre: {producto.nombre}")
                    print(f"Tiene stock: {producto.stock_actual} y el minimo es: {producto.stock_minimo}")
            
            
        elif accion == 5:       
            palabra = "Saliendo de la aplicacion, Guardando Inventario..."
            for salida in palabra:
                print(salida, end="" , flush=True)
                time.sleep(0.05)
            tienda.guardar_archivo()
            break    
        else:
            print("Valor fuera de rango 1-5")
        input("Presione [ENTER] para continuar")

if __name__ == '__main__':
    main()
