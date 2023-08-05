import sys
import copy
from uuid import uuid1
from decimal import Decimal
from itertools import product

import pandas as pd
import numpy as np
import pandas.core.common as com
from pandas.io.formats.style import Styler as BaseStyler, _get_level_lengths, _is_visible, _maybe_wrap_formatter
from pandas.core.indexing import _non_reducing_slice
from pandas.api.types import is_dict_like

from reportlib.utils.templating import template_loader
from .cell import Cell
from .cell_range import CellRange


def format_attr(*args):
    if len(args) == 1:
        arg0 = args[0]
        if isinstance(arg0, dict):
            return '{key}="{value}"'.format(**arg0)
        if isinstance(arg0, (list, tuple)) and len(arg0) == 2:
            return '{}="{}"'.format(*arg0)
    if len(args) == 2:
        return '{}="{}"'.format(*args)
    return ''

  
class Styler(BaseStyler):
    template = template_loader.get_template('base/table.html')
    
    _default_options = {
        'fillna': None,
        'fillinf': None,
        'fillzero': None,
    }
    
    _options = _default_options.copy()
    
    @classmethod
    def set_option(cls, key, value):
        if key in cls._options:
            cls._options[key] = value
        elif key == 'precision':
            pd.set_option('display.precision', value)
        else:
            raise TypeError('set_option() got an unexpected key "{}"'.format(key))
            
    @classmethod
    def get_option(cls, key):
        if key in cls._options:
            return cls._options[key]
        elif key == 'precision':
            return pd.get_option('display.precision')
        else:
            raise TypeError('get_option() got an unexpected key "{}"'.format(key))
    
    @classmethod
    def reset_option(cls, key):
        if key in cls._options:
            cls._options[key] = cls._default_options[key]
        elif key == 'precision':
            pd.reset_option('display.precision')
        else:
            raise TypeError('reset_option() got an unexpected key "{}"'.format(key))
    
    def __init__(self, data, context=None,
                 fillna=None, fillinf=None, fillzero=None,
                 divisor=None, percentage=None, 
                 precision=None, caption=None, table_attributes=None):
      
        if table_attributes is None:
            table_attributes = {}
        if not isinstance(table_attributes, dict):
            raise TypeError('table_attributes must be a dict')
        table_attributes['class'] = 'rp-table rp-table-striped'
        
        self.divisor = divisor
        self.percentage = percentage
        
        super().__init__(data, precision=precision, caption=caption, table_attributes=table_attributes)
        
        if fillna is None:
            fillna = self.get_option('fillna')
        if fillinf is None:
            fillinf = self.get_option('fillinf')
        if fillzero is None:
            fillzero = self.get_option('fillzero')
        
        self.fillna = fillna
        self.fillinf = fillinf
        self.fillzero = fillzero
        
        self.cell_context = {}
        self.merged_cell_ranges = []
        self.context = context or {}
        
        self.skip_table_open_tag = False
        self.skip_table_close_tag = False
        
    def set_head(self, head):
        self.head = head
        return self
      
    def set_foot(self, foot):
        self.foot = foot
        return self
      
    def set_context(self, context=None, **kwargs):
        self.context.update(context or {})
        self.context.update(kwargs)
        return self
      
    def set_table_attributes(self, table_attributes):
        self.table_attributes.update(table_attributes)
        return self
    
    def apply(self, func, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    
    @property
    def _render_context(self):
        d = {
            **self.context,
            'skip_table_open_tag': self.skip_table_open_tag,
            'skip_table_close_tag': self.skip_table_close_tag,
        }
        
        if hasattr(self, 'head'):
            d['head'] = self.head
        if hasattr(self, 'foot'):
            d['foot'] = self.foot
        return d
      
    @staticmethod
    def _number_formatter(divisor=None, precision=None, fillna=None, fillinf=None, fillzero=None, percentage=None):
        postfix = '%' if percentage is True else ''
        precision_fmt = '.%df' % precision if precision is not None else ''
        def formatter(x):
            if isinstance(x, (int, float, complex, Decimal, np.number)):
                if divisor is not None:
                    x /= divisor
                if precision is not None:
                    x = round(x, precision)
                if fillna is not None and pd.isnull(x):
                    return fillna
                if fillinf is not None and (x == np.inf or x == -np.inf):
                    return fillinf
                if fillzero is not None and x == 0:
                    return fillzero
                return ('{:,%s}%s' % (precision_fmt, postfix)).format(x)
            else:
                return x
        return formatter
      
    def format_number(self, subset=None, divisor=None, precision=None, percentage=None,
                     fillna=None, fillinf=None, fillzero=None):          
        if divisor is None:
            divisor = self.divisor
        if precision is None:
            precision = self.precision
        if percentage is None:
            percentage = self.percentage
        if fillna is None:
            fillna = self.fillna
        if fillinf is None:
            fillinf = self.fillinf
        if fillzero is None:
            fillzero = self.fillzero
        formatter = self._number_formatter(divisor=divisor, precision=precision, percentage=percentage, fillna=fillna, fillinf=fillinf, fillzero=fillzero)
        return self.add_class('text-right', subset=subset).format(formatter, subset=subset)
      
    def format(self, formatter, subset=None):
        row_locs, col_locs = self._row_col_locs_from_subset(subset)

        if is_dict_like(formatter):
            for col, col_formatter in formatter.items():
                # formatter must be callable, so '{}' are converted to lambdas
                col_formatter = _maybe_wrap_formatter(col_formatter)
                col_num = self.data.columns.get_indexer_for([col])[0]

                for row_num in row_locs:
                    self._display_funcs[(row_num, col_num)] = col_formatter
        else:
            # single scalar to format all cells with
            locs = product(*(row_locs, col_locs))
            for i, j in locs:
                formatter = _maybe_wrap_formatter(formatter)
                self._display_funcs[(i, j)] = formatter
        return self
        
    def _add_table_class(self, table_attributes, class_name):
        table_attributes = copy.deepcopy(table_attributes)
        if isinstance(class_name, str):
            class_name = class_name.split()
        if 'class' not in table_attributes:
            table_attributes['class'] = ''
        table_attributes['class'] = ' '.join(set(table_attributes['class'].split()) | set(class_name))
        return table_attributes
        
    def add_table_class(self, class_name):
        self.table_attributes = self._add_table_class(self.table_attributes, class_name)
        return self
        
    def remove_table_class(self, class_name):
        if isinstance(class_name, str):
            class_name = class_name.split()
        if 'class' in self.table_attributes:
            self.table_attributes['class'] = ' '.join(filter(lambda x: x not in class_name, self.table_attributes['class'].split()))
            if not self.table_attributes['class']:
                del self.table_attributes['class']
        return self
        
    def _row_col_locs_from_subset(self, subset=None):
        if subset is None:
            row_locs = range(len(self.data))
            col_locs = range(len(self.data.columns))
        else:
            subset = _non_reducing_slice(subset)
            sub_df = self.data.loc[subset]
            row_locs = self.data.index.get_indexer_for(sub_df.index)
            col_locs = self.data.columns.get_indexer_for(sub_df.columns)
        return row_locs, col_locs
      
    def _subset_to_cell_range(self, subset=None):
        row_locs, col_locs = self._row_col_locs_from_subset(subset)
        
        min_row = min(row_locs)
        max_row = max(row_locs)
        min_col = min(col_locs)
        max_col = max(col_locs)
        if not (list(sorted(row_locs)) == list(range(min_row, max_row + 1)) and list(sorted(col_locs)) == list(range(min_col, max_col + 1))):
            raise ValueError('subset is not a valid cell range')
        
        return CellRange(min_row, max_row, min_col, max_col)
        
    def merge_cells(self, subset=None):
        cell_range = self._subset_to_cell_range(subset)
        for merged_cell_range in self.merged_cell_ranges:
            if cell_range.is_collision_with(merged_cell_range):
                raise ValueError('Some cells in this cell range have been merged in another cell range')
                
        self.merged_cell_ranges.append(cell_range)
        return self
      
    def unmerge_cells(self, subset=None):
        cell_range = self._subset_to_cell_range(subset)
        self.merged_cell_ranges = list(filter(lambda r: r != cell_range, self.merged_cell_ranges))
        return self
      
    def _get_merged_cell_range(self, cell):
        for merged_cell_range in self.merged_cell_ranges:
            if cell.is_in_range(merged_cell_range):
                return merged_cell_range
        return None

    def add_class(self, class_name, subset=None):
        n_rlvls = self.data.index.nlevels
        rlabels = self.data.index.tolist()

        if n_rlvls == 1:
            rlabels = [[x] for x in rlabels]
            
        row_locs, col_locs = self._row_col_locs_from_subset(subset)

        locs = product(*(row_locs, col_locs))
        for r, c in locs:
            self._add_class('data', r, c, class_name)
            
        return self

    def _add_class(self, key, r, c, class_name):
        if key not in self.cell_context:
            self.cell_context[key] = {}
        if r not in self.cell_context[key]:
            self.cell_context[key][r] = {}
        if c not in self.cell_context[key][r]:
            self.cell_context[key][r][c] = []
        self.cell_context[key][r][c].append(class_name)

    def show(self):
        if 'IPython.display' in sys.modules:
            from IPython.display import display, HTML
            display(HTML(self.render()))
            
    def render(self, **kwargs):
        self._compute()
        # TODO: namespace all the pandas keys
        d = self._translate()
        # filter out empty styles, every cell will have a class
        # but the list of props may just be [['', '']].
        # so we have the neested anys below
        trimmed = [x for x in d['cellstyle']
                   if any(any(y) for y in x['props'])]
        d['cellstyle'] = trimmed
        d.update(self._render_context)
        d.update(kwargs)
        return self.template.render(d)
      
    def _translate(self):
        table_styles = self.table_styles or []
        caption = self.caption
        ctx = self.ctx
        precision = self.precision
        hidden_index = self.hidden_index
        hidden_columns = self.hidden_columns
        uuid = self.uuid or str(uuid1()).replace("-", "_")
        ROW_HEADING_CLASS = "row_heading"
        COL_HEADING_CLASS = "col_heading"
        INDEX_NAME_CLASS = "index_name"

        DATA_CLASS = "data"
        BLANK_CLASS = "blank"
        BLANK_VALUE = ""

        # for sparsifying a MultiIndex
        idx_lengths = _get_level_lengths(self.index)
        col_lengths = _get_level_lengths(self.columns, hidden_columns)

        cell_context = self.cell_context

        n_rlvls = self.data.index.nlevels
        n_clvls = self.data.columns.nlevels
        rlabels = self.data.index.tolist()
        clabels = self.data.columns.tolist()

        if n_rlvls == 1:
            rlabels = [[x] for x in rlabels]
        if n_clvls == 1:
            clabels = [[x] for x in clabels]
        clabels = list(zip(*clabels))

        cellstyle = []
        head = []

        for r in range(n_clvls):
            # Blank for Index columns...
            row_es = [{"type": "th",
                       "value": BLANK_VALUE,
                       "display_value": BLANK_VALUE,
                       "is_visible": not hidden_index,
                       "class": " ".join([BLANK_CLASS])}] * (n_rlvls - 1)

            # ... except maybe the last for columns.names
            name = self.data.columns.names[r]
            cs = []
            name = BLANK_VALUE if name is None else name
            row_es.append({"type": "th",
                           "value": name,
                           "display_value": name,
                           "class": " ".join(cs),
                           "is_visible": not hidden_index})

            if clabels:
                for c, value in enumerate(clabels[r]):
                    cs = []
                    cs.extend(cell_context.get(
                        "col_headings", {}).get(r, {}).get(c, []))
                    es = {
                        "type": "th",
                        "value": value,
                        "display_value": value,
                        "class": " ".join(cs),
                        "is_visible": _is_visible(c, r, col_lengths),
                    }
                    colspan = col_lengths.get((r, c), 0)
                    if colspan > 1:
                        es["attributes"] = [
                            format_attr("colspan", colspan)
                        ]
                    row_es.append(es)
                head.append(row_es)

        if (self.data.index.names and
                com._any_not_none(*self.data.index.names) and
                not hidden_index):
            index_header_row = []

            for c, name in enumerate(self.data.index.names):
                cs = [INDEX_NAME_CLASS,
                      "level{lvl}".format(lvl=c)]
                name = '' if name is None else name
                index_header_row.append({"type": "th", "value": name,
                                         "class": " ".join(cs)})

            index_header_row.extend(
                [{"type": "th",
                  "value": BLANK_VALUE,
                  "class": " ".join([BLANK_CLASS])
                  }] * (len(clabels[0]) - len(hidden_columns)))

            head.append(index_header_row)

        body = []
        for r, idx in enumerate(self.data.index):
            row_es = []
            for c, value in enumerate(rlabels[r]):
                rid = []
                rid.extend(cell_context.get("row_heading", {}).get(r, {}).get(c, []))
                es = {
                    "type": "th",
                    "is_visible": (_is_visible(r, c, idx_lengths) and
                                   not hidden_index),
                    "value": value,
                    "display_value": value,
                    "id": "_".join(rid[1:]),
                    "class": " ".join(rid)
                }
                rowspan = idx_lengths.get((c, r), 0)
                if rowspan > 1:
                    es["attributes"] = [
                        format_attr("rowspan", rowspan)
                    ]
                row_es.append(es)

            for c, col in enumerate(self.data.columns):
                cs = []
                cs.extend(cell_context.get("data", {}).get(r, {}).get(c, []))
                formatter = self._display_funcs[(r, c)]
                value = self.data.iloc[r, c]
                cell = Cell(r, c)
                merged_cell_range = self._get_merged_cell_range(cell)
                row_dict = {"type": "td",
                            "value": value,
                            "class": " ".join(cs),
                            "display_value": formatter(value),
                            "is_visible": (c not in hidden_columns and not (merged_cell_range is not None and merged_cell_range.top_left != cell)),
                           }
                
                if merged_cell_range is not None and merged_cell_range.top_left == cell:
                    row_dict["attributes"] = [
                        format_attr("rowspan", merged_cell_range.rowspan),
                        format_attr("colspan", merged_cell_range.colspan),
                    ]
                
                # only add an id if the cell has a style
                if (self.cell_ids or
                        not(len(ctx[r, c]) == 1 and ctx[r, c][0] == '')):
                    row_dict["id"] = "_".join(cs[1:])
                row_es.append(row_dict)
                props = []
                for x in ctx[r, c]:
                    # have to handle empty styles like ['']
                    if x.count(":"):
                        props.append(x.split(":"))
                    else:
                        props.append(['', ''])
                cellstyle.append({'props': props,
                                  'selector': "row{row}_col{col}"
                                  .format(row=r, col=c)})
            body.append(row_es)

        table_attr = self.table_attributes
        use_mathjax = pd.get_option("display.html.use_mathjax")
        if not use_mathjax:
            table_attr = self._add_table_class(table_attr, 'tex2jax_ignore')
        table_attr_str = ' '.join(map(format_attr, table_attr.items()))

        return dict(head=head, cellstyle=cellstyle, body=body, uuid=uuid,
                    precision=precision, table_styles=table_styles,
                    caption=caption, table_attributes=table_attr_str)
