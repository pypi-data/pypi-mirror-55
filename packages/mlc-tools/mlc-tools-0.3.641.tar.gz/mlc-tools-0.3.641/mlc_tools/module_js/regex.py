import re


class RegexPatternJs(object):

    FUNCTION = (
        (re.compile(r'\((.+?)\s*==\s*(.+?)([\),])'), r'(compare(\1, \2)\3', ['==']),
        (re.compile(r'\((.+?)\s*!=\s*(.+?)([\),])'), r'(!compare(\1, \2)\3', ['!=']),
        # (re.compile(r'(\w+[\.>-]+\w+)\.add\((\w+),\s*&(\w+)::(\w+)'), r'\1.add(\2, "\4"', ['.add(']),
        # (re.compile(r'catch\((\w+)\s*(\w*)\)'), r'catch__\1__\2', ['catch']),
        (re.compile(r'DataStorage::shared\(\).get<(\w+)>'), r'DataStorage.shared().get\1', ['DataStorage::shared']),
        # (re.compile(r'Factory::(.+)<\w+>'), r'Factory::\1', ['Factory:']),
        # (re.compile(r'\.str\(\)'), r'', ['str()']),
        (re.compile(r'for\s*\([\w_]+ (.+?)\s*:\s*(.+)\s*\)'), r'for(let \1 in \2)', ['for']),
        (re.compile(r'for\s*\([\w_]+& (.+?)\s*:\s*(.+)\s*\)'), r'for(let \1 in \2)', ['for']),
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)\s*{'),
         r'for (let \1 in \3)\n{\nlet \2 = \3[\1];\n ', ['for']),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+<([\.\->\w]+?);\s*\+\+\w+\s*\)'),
         r'for(let \1 = \2; \1 < \3; \1++)', ['for']),
        (re.compile(r'(\w+)\s+(\w+);'), r'let \2 = new \1();'),
        (re.compile(r'\w+\* (\w+)\s*=\s*new (.+);'), r'let \1 = new \2;', ['new']),
        (re.compile(r'std::let (\w+) = new string\(\)'), r'let \1 = ""', ['std::let']),
        (re.compile(r'\bauto (\w+)'), r'let \1', ['auto']),
        (re.compile(r'\bauto& (\w+)'), r'let \1', ['auto']),
        (re.compile(r'\bvoid (\w+)'), r'let \1', ['void']),
        (re.compile(r'\bint (\w+)'), r'let \1', ['int']),
        (re.compile(r'\bbool (\w+)'), r'let \1', ['bool']),
        (re.compile(r'std::string (\w+)'), r'let \1', ['std::string']),
        (re.compile(r'\b\w+ (\w+)\s+=\s+(.+);'), r'let \1 = \2;', ['=']),

        (re.compile(r'\((\w+) (\w+)\)'), r'(\2)'),
        # (re.compile(r'\(const (\w+)\& (\w+)\)'), r'($\2)', ['const']),
        # (re.compile(r'\(const (\w+)\* (\w+)\)'), r'($\2)', ['const']),
        # (re.compile(r'\((\w+)\* (\w+)\)'), r'($\2)'),
        # (re.compile(r'(\w+)\ (\w+),'), r'$\2,'),
        # (re.compile(r'(\w+)\& (\w+),'), r'$\2,', ['&']),
        # (re.compile(r'(\w+)\* (\w+),'), r'$\2,', ['*']),
        # (re.compile(r'const (\w+)\* (\w+)'), r'$\2', ['const ']),
        # (re.compile(r'const (\w+)\& (\w+)'), r'$\2', ['const ']),
        # (re.compile(r'float (\w+)'), r'$\1', ['float ']),
        # (re.compile(r'\bthis\b'), r'$this', ['this']),
        # (re.compile(r':const'), r'', ['const']),
        # (re.compile(r'(\w+)::(\w+)'), r'\1::$\2', ['::']),
        # (re.compile(r'(\w+)::(\w+)\)'), r'\1::$\2)', ['::']),
        # (re.compile(r'(\w+)::(\w+)\.'), r'\1::$\2.', ['::']),
        # (re.compile(r'(\w+)::(\w+)->'), r'\1::$\2.', ['::']),
        # (re.compile(r'(\w+)::(\w+)\]'), r'\1::$\2]', ['::']),
        # (re.compile(r'(\w+)::\$(\w+)\('), r'\1::\2(', ['::']),
        # (re.compile(r'(\w+)::\$(\w+)\((\w*)\)'), r'\1::\2(\3)', ['::']),
        # (re.compile(r'function \$(\w+)'), r'function \1', ['function ']),
        (re.compile(r'\.at\((.*?)\)'), r'[\1]', ['.at']),
        # (re.compile(r'(\w+)\.'), r'\1.'),
        # (re.compile(r'(\w+)\(\)\.'), r'\1().'),
        # (re.compile(r'(\w+)\]\.'), r'\1].'),
        (re.compile(r'&(\w+)'), r'\1', ['&']),
        # (re.compile(r'\$if\('), r'if(', ['if']),
        # (re.compile(r'delete \$(\w+);'), r'', ['delete']),
        # (re.compile(r'([-0-9])->([-0-9])f\b'), r'\1.\2', ['']),
        # (re.compile(r'assert\(.+\);'), r'', ['assert']),
        (re.compile(r'make_intrusive<(\w+)>\(\s*\)'), r'new \1()', ['make_intrusive']),
        (re.compile(r'dynamic_pointer_cast_intrusive<.+>\((.+?)\)'), r'\1', ['dynamic_pointer_cast_intrusive']),
        # (re.compile(r'(.+?)\->push_back\((.+)\);'), r'array_push(\1, \2);', ['push_back']),
        (re.compile(r'let (\w+) = new return\(\);'), r'return \1;', ['new return']),
        (re.compile(r'std::vector<.+?>\s+(\w+)'), r'let \1 = []', ['std::vector']),
        (re.compile(r'\blist<.+>\s+(\w+)'), r'let \1 = []', ['list<']),
        (re.compile(r'\bmap<([<:>\w\s\*&\$]+),\s*([<:>\w\s\*&\$]+)>\s*(\w+)'), r'let \3 = {}', ['map<']),
        # (re.compile(r'\bstrTo<(\w+)>'), r'(\1)', ['strTo']),
        (re.compile(r'toStr\s*\((\s*(.+?)\s*)\)'), r'(\1).toString()', ['toStr']),
        # (re.compile(r'(@{__string_\d+__})\s*\+'), r'\1.', ['@{__string_']),
        # (re.compile(r'\+\s*(@{__string_\d+__})'), r'.\1', ['@{__string_']),
        (re.compile(r'(\b[-0-9]+)\.f\b'), r'\1.0'),
        (re.compile(r'(\b[-0-9]+)\.([-0-9]*)f\b'), r'\1.\2'),

        (re.compile(r'map_size\s*\((\s*(.+?)\s*)\)'), r'length_of(Object.keys(\1))', ['map_size']),

        (re.compile(r'list_size\s*\((\s*(.+?)\s*)\)'), r'length_of(\1)', ['list_size']),
        (re.compile(r'list_push\s*\(\s*(.+?),\s*(.+)\s*\)'), r'\1.push(\2)', ['list_push']),
        (re.compile(r'list_insert\s*\(\s*(.+?),\s*(.+)\s*,\s*(.+)\s*\)'), r'\1.splice(\2, 0, \3)', ['list_insert']),
        (re.compile(r'list_remove\s*\(\s*(.+),\s*(.+)\s*\)'), r'\1.splice(\1.indexOf(\2), 1)', ['list_remove']),
        (re.compile(r'list_erase\s*\(\s*(.+),\s*(.+)\s*\)'), r'\1.splice(\2, 1)', ['list_erase']),
        (re.compile(r'list_clear\s*\(\s*(.+)\s*\)'), r'\1 = []', ['list_clear']),
        (re.compile(r'list_resize\s*\(\s*(.+),\s*(.+)\s*\)'), r'\1.length = \2', ['list_resize']),
        (re.compile(r'in_map\s*\(\s*(.+?),\s*(.+?)\s*\)'), r'(\1 in \2)', ['in_map']),
        (re.compile(r'in_list\s*\(\s*(.+),\s*(.+)\s*\)'), r'(\2.indexOf(\1) != 1)', ['in_list']),

        (re.compile(r'map_clear\s*\(\s*(.+)\s*\)'), r'\1 = {}', ['map_clear']),
        (re.compile(r'map_remove\s*\(\s*(.+),\s*(.+)\s*\)'), r'delete (\1[\2])', ['map_remove']),

        # (re.compile(r'->\$(\w+)\('), r'.\1(', ['.']),
        # (re.compile(r'([-0-9]*)->([-0-9]*)f\b'), r'\1.\2'),
        # (re.compile(r'([-0-9]*)->f\\b'), r'\1.0'),
        # (re.compile(r'\$return\s'), r'return', ['$return']),

        # add listener to Observable
        (re.compile(r'(\w+\.\w+)\.add\((\w+), \w+::(\w+)(.+)\);'), r'\1.add(\2, \2.\3\4);', ['']),
        (re.compile(r',\s*std::placeholders::_\d'), r'', ['std::placeholders']),

        # (re.compile(r'list_remove\((\$.+?),\s*([\$.\w]+?)\);'), r'array_splice(\1, array_search(\2, \1), 1);',
        #  ['list_remove']),
        # (re.compile(r'list_erase\((\$.+?),\s*([\$.\w]+?)\);'), r'array_splice(\1, \2, 1);',
        #  ['list_erase']),
        # (re.compile(r'list_clear\((.+?)\);'), r'\1 = array();', ['list_clear']),
        # (re.compile(r'list_resize\s*\(\s*(.+),\s*(.+)\s*\)'), r'\1 = array_fill(0, \2, NULL);', ['list_resize']),
        (re.compile(r'string_empty\((.+?)\)'), r'(length_of(\1) == 0)', ['string_empty']),
        # (re.compile(r'random_float\(\)'), r'(mt_rand() * 1.0 / mt_getrandmax())', ['random_float']),
        # (re.compile(r'random_int\((.+?),\s*(.+)\)'), r'mt_rand(\1, \2-1)', ['random_int']),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'((\1)+(\2))', ['std::strcat']),
        # (re.compile(r'list_push\s*\((.+)\)'), r'array_push(\1)', ['list_push']),
        # (re.compile(r'list_insert\s*\((\$.+?),\s*([\$.\w]+?),\s*([\$.\w]+?)\)'), r'array_splice(\1, \2, 0, \3);',
        #  ['list_insert']),
        #
        # # Exception with try/catch block (one catch)
        # (re.compile(r'try\n\s*{([\s\S.]+?)}\n\s*catch__((\w+)__(\w*))\n\s+{([\s\S.]+?)}'),
        #  r'try\n{\1}\ncatch(\3 $\4)\n{\5}', ['try'])
    )

    INITIALIZE = (re.compile(r'(\w+)::(\w+)'), r'\1::\2')

    REPLACES = (
        ('->', '.'),
        ('::', '.'),
        # ('($int)', '(int)'),
        # ('time(nullptr)', 'time()'),
        # ('$$', '$'),
        # ('std::max', 'max'),
        # ('std::$max<int>', 'max'),
        # ('std::$max<float>', 'max'),
        # ('std::min', 'min'),
        # ('std::$min<int>', 'min'),
        # ('std::$min<float>', 'min'),
        # ('std::round', 'round'),
        # ('std::floor', 'floor'),
        # ('std::fabs', 'abs'),
        # ('std::ceil', 'ceil'),
        # ('std::sqrt', 'sqrt'),
        # ('in_map', 'array_key_exists'),
    )
