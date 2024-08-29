Prism.languages.mojo = {
    'comment': {
        pattern: /(^|[^\\])#.*/,
        lookbehind: true,
        greedy: true
    },
    'string': {
        pattern: /(?:[rub]|br|rb)?("|')(?:\\.|(?!\1)[^\\\r\n])*\1/i,
        greedy: true
    },
    'function': {
        pattern: /((?:^|\s)(?:def|fn)[ \t]+)[a-zA-Z_]\w*(?=\s*\():/g,
        lookbehind: true
    },
    'class': {
        pattern: /(\bstruct\s+)\w+/i,
        lookbehind: true
    },
    'keyword': /\b(?:var|if|else|for|while|break|continue|return|import|export)\b/,
    'builtin': /\b(?:print|len|range|sum)\b/,
    'boolean': /\b(?:false|true)\b/,
    'number': /\b\d+(?:\.\d+)?\b/,
    'operator': /[-+%=]=?|!=|:=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]/,
    'punctuation': /[{}[\];(),.:]/
};

Prism.languages.mj = Prism.languages.mojo;
