# AUTOGENERATED! DO NOT EDIT! File to edit: 00_docstring.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['get_annotations', 'reformat_function', 'reformat_class']

# Cell
import inspect, ast, astunparse
#nbdev_comment from __future__ import annotations
import fastcore.docments as dments
from collections import OrderedDict

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
    parsed_source = ast.parse(source)
    annos = get_annotations(source)
    for i in range(len(parsed_source.body[0].args.args)):
        parsed_source.body[0].args.args[i].annotation = None
    parsed_source.body[0].returns = None
    unparsed_source = astunparse.unparse(parsed_source).lstrip('\n').split('\n')
    has_decorator = False
    if unparsed_source[0].startswith('@'):
        has_decorator = True
    if has_decorator:
        function_definition = '\n'.join(unparsed_source[:2])
    else:
        function_definition = unparsed_source[0]
    # Check if we have a docstring
    if isinstance(parsed_source.body[0].body[0].value, ast.Str):
        if has_decorator:
            function_innards = "\n".join(unparsed_source[3:])
        else:
            function_innards = "\n".join(unparsed_source[2:])
    else:
        if has_decorator:
            function_innards = "\n".join(unparsed_source[2:])
        else:
            function_innards = "\n".join(unparsed_source[1:])
    def _get_whitespace(): return whitespace_char*num_whitespace

    if unparsed_source[2] != '':
        num_whitespace, whitespace_char = _get_leading(unparsed_source[2])
    else:
        if len(unparsed_source) < 4:
            num_whitespace, whitespace_char = _get_leading(unparsed_source[1])
        else:
            num_whitespace, whitespace_char = _get_leading(unparsed_source[3])

    docstring = f'\n{_get_whitespace()}"""'
    if isinstance(parsed_source.body[0].body[0].value, ast.Str):
        _quotes = ("'", '"')
        orig_docstring = astunparse.unparse(parsed_source.body[0].body[0]).lstrip(whitespace_char).replace(_quotes[0],'').replace(_quotes[1],'')
        orig_docstring = orig_docstring.split('\\n')
        # Check if this logic can be refactored
        for i,line in enumerate(orig_docstring):
            if len(line.strip()) > 0:
                if len(line.lstrip()) < len(line):
                    diff = len(line) - len(line.lstrip())
                    if i == 0:
                        docstring += f'{line.lstrip()}'
                    else:
                        docstring += f'\n{whitespace_char * (diff)}{line.lstrip()}'
                else:
                    if i == 0:
                        docstring += f'{line.lstrip()}'
                    else:
                        docstring += f'\n{_get_whitespace()}{line.lstrip()}'
    if len(docs.keys()) >= 1:
        if len(docs.keys()) >= 1:
            param_string = f'\n{_get_whitespace()}Parameters\n'
            param_string += f'{_get_whitespace()}----------\n'
            for i, param in enumerate(docs.keys()):
                if param != "return" and param != "self" and param != "cls":
                    param_string += f'{_get_whitespace()}{param}'
                    if annos[0][i] is not None:
                        param_string += f' : {annos[0][i]}'
                    else:
                        param_string += f' : any'
                    param_string += '\n'
                    if docs[param] is not None:
                        param_string += f'{whitespace_char * (num_whitespace+2)}{docs[param]}\n'
        if param_string != f'\n{_get_whitespace()}Parameters\n{_get_whitespace()}----------\n':
            docstring += param_string
    if (annos[-1] != inspect._empty) and ('return' in docs.keys()):
        docstring += f'\n{_get_whitespace()}Returns\n'
        docstring += f'{_get_whitespace()}-------\n'
        docstring += f'{_get_whitespace()}{annos[1]}\n'
        docstring += f'{whitespace_char * (num_whitespace+2)}{docs["return"]}\n'
    docstring += f'{_get_whitespace()}"""\n'
    return f'{function_definition}{docstring}{function_innards}'

# Cell
def reformat_class(
    source:str, # Source code of a full class
    recursion_level = 1, # Depth of recursion
):
    "Takes messy class code and refactors it into a readable PEP-8 standard style"
    whitespace_char = None
    def _format_spacing(code, num_leading):
        code = [c for c in code if len(c) > 0]
        for i, c in enumerate(code):
            curr_leading = len(c) - len(c.lstrip())
            code[i] = f'{code[i][0] * (curr_leading-num_leading)}{code[i].lstrip()}'
        return code
    body = ast.parse(source).body[0].body
    new_source = ''
    function_definition = astunparse.unparse(ast.parse(source)).lstrip('\n').split('\n')[0]
    new_source += function_definition

    def _get_whitespace(): return whitespace_char*num_whitespace
    unparsed_source = astunparse.unparse(ast.parse(source)).lstrip('\n').split('\n')
    num_whitespace, whitespace_char = _get_leading(unparsed_source[2])
    docstring = f'\n{_get_whitespace()}"""'
    docstring_len = 0
    diff = 2
    new_nodes = [function_definition]

    for i,node in enumerate(body):
        if isinstance(node, ast.ClassDef):
            beginning_lineno = node.lineno
            split_code = source.split('\n')
            if i < len(body)-1:
                ending_lineno = body[i+1].lineno
                code = split_code[beginning_lineno-1:ending_lineno-1]
                num_leading = len(code[0]) - len(code[0].lstrip())
                for i,c in enumerate(code): code[i] = code[i][num_leading:]
            new_nodes.append(reformat_class('\n'.join(code), recursion_level+1))
        elif isinstance(node, ast.FunctionDef):
            offset = node.col_offset
            beginning_lineno = node.lineno
            split_code = source.split('\n')
            if i < len(body)-1:
                ending_lineno = body[i+1].lineno
                code = split_code[beginning_lineno-1:ending_lineno-1]
                if whitespace_char is None:
                    whitespace_char = code[i][0]
                num_leading = len(code[0]) - len(code[0].lstrip())
                code = _format_spacing(code, num_leading)
                new_func = reformat_function('\n'.join(code))
            else:
                code = split_code[beginning_lineno-1:]
                if whitespace_char is None:
                    whitespace_char = code[i][0]
                num_leading = len(code[0]) - len(code[0].lstrip())
                code = _format_spacing(code, num_leading)
                new_func = reformat_function('\n'.join(code))
            new_nodes.append(f'{new_func}')
        else:
            if isinstance(node.value, ast.Str) and i == 0:
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
                docstring += f'\n{_get_whitespace()}"""'
                full_string = docstring.split('\n')
                new_string = ''
                if len(full_string) == 4:
                    for i, line in enumerate(full_string):
                        new_string += line.lstrip()
                else:
                    new_string = '\n'.join(full_string)
                docstring_len = len(new_string.split('\n'))
                new_nodes.append(new_string)
            else:
                new_nodes.append(f'{astunparse.unparse(node).strip()}')
    formatted_source = []
    num_chars = 4
    if recursion_level > 1:
        num_chars += (2*(recursion_level-1)) - 2
    else:
        num_chars = 4
    for i,line in enumerate(new_nodes):
        if i == 0:
            formatted_source.append(line)
        elif i == 1:
            if not len(line.lstrip()) < len(line):
                l = line.split('\n')
                for i,o in enumerate(l):
                    l[i] = f'{whitespace_char * num_chars}{o}'
                line = '\n'.join(l)
                formatted_source.append(line.lstrip('\n'))
            else:
                formatted_source.append(line.lstrip('\n'))
        else:
            l = line.split('\n')
            for i,o in enumerate(l):
                l[i] = f'{whitespace_char * num_chars}{o}'
            line = '\n'.join(l)
            formatted_source.append(line)
    return '\n'.join(formatted_source)