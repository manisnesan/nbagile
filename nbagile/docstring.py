# AUTOGENERATED! DO NOT EDIT! File to edit: 99_test.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['get_annotations', 'reformat_function', 'addition']

# Cell
import inspect, ast, astunparse
#nbdev_comment from __future__ import annotations
import fastcore.docments as dments

# Cell
def get_annotations(
    source:str # Source code of function or class
):
    "Extracts the type annotations from source code"
    parse = ast.parse(source)
    arg_annos = []
    for i,anno in enumerate(parse.body[0].args.args):
        if anno.annotation is not None:
            arg_annos.append(astunparse.unparse(anno.annotation).strip('\n'))
        else:
            arg_annos.append(anno.annotation)
        parse.body[0].args.args[i].annotation = None
    if parse.body[0].returns is not None:
        ret_anno = astunparse.unparse(parse.body[0].returns).strip('\n')
    else:
        ret_anno = None
    return arg_annos, ret_anno

# Cell
def _get_leading(o):
    return len(o) - len(o.lstrip(o[0])), o[0]

# Cell
def reformat_function(
    source:str, # Source code
):
    "Takes messy source code and refactors it into a readable PEP-8 standard style"
    docs = dments.docments(source)
    annos = get_annotations(source)
    parsed_source = ast.parse(source)
    for i in range(len(parsed_source.body[0].args.args)):
        parsed_source.body[0].args.args[i].annotation = None
    parsed_source.body[0].returns = None
    unparsed_source = astunparse.unparse(parsed_source).lstrip('\n').split('\n')
    function_definition = unparsed_source[0]
    # Check if we have a docstring
    if isinstance(parsed_source.body[0].body[0].value, ast.Str):
        function_innards = "\n".join(unparsed_source[2:])
    else:
        function_innards = "\n".join(unparsed_source[1:])
    def _get_whitespace(): return whitespace_char*num_whitespace

    num_whitespace, whitespace_char = _get_leading(unparsed_source[2])
    docstring = f'\n{_get_whitespace()}"""'
    if isinstance(parsed_source.body[0].body[0].value, ast.Str):
        _quotes = ("'", '"')
        orig_docstring = unparsed_source[1].lstrip(whitespace_char).strip(_quotes[0]).strip(_quotes[1])
        orig_docstring = orig_docstring.split('\\n')
        # Check if this logic can be refactored
        for line in orig_docstring:
            if len(line.strip()) > 0:
                if len(line.lstrip()) < len(line):
                    diff = len(line) - len(line.lstrip())
                    docstring += f'\n{whitespace_char * (diff)}{line.lstrip()}'
                else:
                    docstring += f'\n{_get_whitespace()}{line.lstrip()}'
    docstring += f'\n\n{_get_whitespace()}Parameters\n'
    docstring += f'{_get_whitespace()}----------\n'
    for i, param in enumerate(docs.keys()):
        if param != "return" and param != "self":
            docstring += f'{_get_whitespace()}{param} : {annos[0][i]}\n'
            docstring += f'{whitespace_char * (num_whitespace+2)}{docs[param]}\n'
    if (annos[-1] != inspect._empty) and ('return' in docs.keys()):
        docstring += f'\n{_get_whitespace()}Returns\n'
        docstring += f'{_get_whitespace()}-------\n'
        docstring += f'{_get_whitespace()}{annos[1]}\n'
        docstring += f'{whitespace_char * (num_whitespace+2)}{docs["return"]}\n'
    docstring += f'{_get_whitespace()}"""\n'
    return f'{function_definition}{docstring}{function_innards}'

# Cell
def addition(
    a:int, # The first number to add
    b:int, # The second number to add
) -> int: # The sum of a and b
    "Adds two numbers together"
    return a+b