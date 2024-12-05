import os
import sys


class GenerateAst:
    @staticmethod
    def main(args):
        if len(args) != 1:
            print("Usage: generate_ast <output directory>", file=sys.stderr)
            sys.exit(64)

        output_dir = args[0]
        GenerateAst.define_ast(output_dir, "Expr", [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Object value",
            "Unary    : Token operator, Expr right"
        ])

    @staticmethod
    def define_ast(output_dir, base_name, types):
        """Generate the AST classes and its subclasses"""
        try:
            path = os.path.join(output_dir, f"{base_name.lower()}.py")
            with open(path, "w") as file:
                file.write(f"class {base_name}:\n")
                # Base class
                file.write("    def accept(self, visitor):\n")
                file.write("        raise NotImplementedError()\n\n")
                
                
                # define visitor interface
                GenerateAst.define_visitor(file, base_name, types)
                
                

                # Generate AST classes
                for type_definition in types:
                    class_name, fields = map(str.strip, type_definition.split(":"))
                    GenerateAst.define_type(file, base_name, class_name, fields)
                print(f"AST classes generated in {path}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
            
            
    
    @staticmethod
    def define_visitor(writer, base_name, types):
        writer.write(f"class {base_name}Visitor:\n")
        for type_definition in types:
            class_name = type_definition.split(":")[0].strip()
            # print(class_name)
            writer.write(f"    def visit_{class_name.lower()}(self, {class_name.lower()}):\n")
            writer.write(f"        raise NotImplementedError()\n\n")
            
    
    
            

    @staticmethod
    def define_type(file, base_name, class_name, field_list):
        """Generate code for a specific type of AST node"""
        file.write(f"class {class_name}({base_name}):\n")
        fields = [f.strip() for f in field_list.split(",")]
        # print(fields)
        # Constructor
        file.write(f"    def __init__(self, {', '.join([field.split()[1] for field in fields])}):\n")
        for field in fields:
            field_type, field_name = field.split()
            file.write(f"        self.{field_name} = {field_name}\n")
        file.write("\n")
        
        
        # implement the accept method
        file.write(f"    def accept(self, visitor):\n")
        file.write(f"        return visitor.visit_{class_name.lower()}(self)\n\n")


if __name__ == "__main__":
    GenerateAst.main(sys.argv[1:])