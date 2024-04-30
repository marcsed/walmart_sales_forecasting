import subprocess
import importlib
import ast

def install_or_update_packages_from_code(code):
    class ImportVisitor(ast.NodeVisitor):
        def __init__(self):
            self.packages = set()
    
        def visit_Import(self, node):
            for alias in node.names:
                self.packages.add(alias.name.split('.')[0])
    
        def visit_ImportFrom(self, node):
            if node.module:  # Only add if module is not None
                self.packages.add(node.module.split('.')[0])
    
    def get_packages_from_code(code):
            tree = ast.parse(code)
            visitor = ImportVisitor()
            visitor.visit(tree)
            return list(visitor.packages)
    
    def install_or_update_package(package):
        try:
            # Try to import the package
            importlib.import_module(package)
            print(f"Checking for updates for {package}...")
            try:
                subprocess.run(["pip", "install", "--upgrade", package], check=True)
                print(f"{package} is up to date.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install or update {package}. Error: {e}")
        except ImportError:
            # If the import fails, install the package
            print(f"{package} not found, attempting to install...")
            try:
                subprocess.run(["pip", "install", "--upgrade", package], check=True)
                print(f"{package} has been installed.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}. Error: {e}")

    packages_list = get_packages_from_code(code)
    for package in packages_list:
        install_or_update_package(package)