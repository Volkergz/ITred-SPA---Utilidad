#!/usr/bin/env python3
import sys, json, os
 
CONFIG_FILE = "config.json"
TEMPLATE_FILES = {
    "php":"templates/template_PHP.php",
    "css":"templates/template_CSS.css",
    "js":"templates/template_JS.js"
}

def load_config():
    """Carga la configuración desde el archivo JSON."""
    try:
        with open(CONFIG_FILE) as configFile:
            return json.load(configFile)
    except FileNotFoundError:
        print("Error: El archivo de configuración no existe.")
        sys.exit(1)

def save_config(data):
    """Guarda la configuración en el archivo JSON."""
    with open(CONFIG_FILE, 'w') as configFile:
        json.dump(data, configFile, indent=4)

def configure():
    """Permite modificar la configuración del proyecto."""
    data = load_config()
    proyectPath = input("Ingrese el path del proyecto: ")
    data['pathProyect'] = proyectPath
    save_config(data)
    print("Configuración actualizada correctamente.")

def create_from_template():
    """Crea un archivo basado en una plantilla."""
    data = load_config()
    db_name = input("Nombre de la base de datos: ")
    file_name = input("Nombre del módulo (sin extensión): ")
    #Definimos las rutas de los archivos
    levelPath = input("Nivel de carpta del elemento: ")
    php_path = os.path.join(levelPath, file_name)
    css_path = os.path.join(levelPath.replace("php", "css"), file_name)
    js_path = os.path.join(levelPath.replace("php", "js"), file_name)

    print(f"""
php : {php_path}
 js : {js_path}
css : {css_path}
""")

    try:
        with open(TEMPLATE_FILES["css"]) as cssFile:
            template_content = cssFile.read()
        
        # Reemplazar marcadores en la plantilla
        template_content = template_content.replace("{element_name}", file_name)

        output_path = os.path.join(data["pathProyect"], css_path)
        os.makedirs(output_path, exist_ok=True)

        output_file = os.path.join(output_path, f"{file_name}.css")

        with open(output_file, 'w') as newFile:
            newFile.write(template_content)

        print(f"Archivo CSS generado exitosamente: {output_file}")

        with open(TEMPLATE_FILES["js"]) as jsFile:
            template_content = jsFile.read()
        
        # Reemplazar marcadores en la plantilla
        template_content = template_content.replace("{element_name}", file_name)

        output_path = os.path.join(data["pathProyect"], js_path)
        os.makedirs(output_path, exist_ok=True)

        output_file = os.path.join(output_path, f"{file_name}.js")

        with open(output_file, 'w') as newFile:
            newFile.write(template_content)

        print(f"Archivo CSS generado exitosamente: {output_file}")

        with open(TEMPLATE_FILES["php"]) as phpFile:
            template_content = phpFile.read()
        
        #Definimos las URLs del Js & CSS
        css_path = css_path.replace("\\", "/") + f"/{file_name}.css"
        js_path = js_path.replace("\\", "/") + f"/{file_name}.js"

        # Reemplazar marcadores en la plantilla
        template_content = template_content.replace("{db_name}", db_name)
        template_content = template_content.replace("{element_name}", file_name)
        template_content = template_content.replace("{js_url}", js_path)
        template_content = template_content.replace("{css_url}", css_path)

        output_path = os.path.join(data["pathProyect"], php_path)
        os.makedirs(output_path, exist_ok=True)

        output_file = os.path.join(output_path, f"{file_name}.php")
        with open(output_file, 'w') as newFile:
            newFile.write(template_content)

        print(f"Archivo PHP generado exitosamente: {output_file}")

    except FileNotFoundError:
        print("Error: La plantilla no fue encontrada.")
        sys.exit(1)

#Inicio del programa
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <command>")
        sys.exit(1)

    order = str(sys.argv[1])

    if order == "config":
        configure()

    elif order == "new":
        create_from_template()

    else:
        print("Comando no reconocido. Comandos válidos: config, new")