from aplicacion.servicio_importador import ServicioImportador

ARCHIVO_EXCEL = "datos/Preanalitica_Datos_de_Prueba_Adaptado.xlsx"

if __name__ == "__main__":
    # El script solo se encarga de "disparar" la acción.
    # La lógica real vive en la capa de aplicación.
    importador = ServicioImportador(ARCHIVO_EXCEL)
    importador.ejecutar_importacion()
