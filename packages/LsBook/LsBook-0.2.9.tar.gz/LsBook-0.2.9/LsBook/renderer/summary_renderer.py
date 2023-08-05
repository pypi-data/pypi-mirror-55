import logging
import os

import mistletoe

from ..utils.path import get_pure_path, get_filename_not_ext


class SummaryRenderer(mistletoe.HTMLRenderer):
    def __init__(self, *extras, book_output=None, current_path=None, current_data_level=None, index=None):
        """目录生成器

        :param extras:
        :param book_output: 书籍输出目录
        :param current_path: 当前文件路径
        :param current_data_level: 当前文件级别
        :param index: 本页所处索引位置
        """
        super().__init__(*extras)
        self._data_level = []
        self._heading_count = 0
        self._iter_count = {}
        self._iter_index = 0
        # 目录结构
        self.summary = {}
        self._count = 0
        # 当前文件路径
        self._current_path = current_path
        # 输出路径
        self._book_output = book_output
        # 当前页面级别
        self._current_data_level = current_data_level
        # 本页所处索引位置
        self._index = index
        # 目录字典：记录整个目录信息，包括上下页
        self.summary_dict = {}
        # 上一页标题
        self.prev_title = ""
        # 上一页相对路径：相对本页面
        self.prev_relative_path = ""
        # 下一页标题
        self.next_title = ""
        # 下一页相对路径：相对本页面
        self.next_relative_path = ""
        # 本页面相对于根的相对路径
        self.basePath = "."
        self._target = []

    @property
    def data_level(self):
        tmp = [str(x) for x in self._data_level]
        return ".".join(tmp)

    def render_link(self, token):
        template = '<a href="{target}"><b>{data_level}.</b>{inner}</a>'
        inner = self.render_inner(token)

        target = token.target
        if token.target[-2:].lower() == "md":
            self._count += 1
            if self._current_path:
                # 计算相对路径
                target = token.target
                target = get_relpath(book_output=self._book_output, ref=target,
                                     current_ref=self._current_path) + ".html"
                # 通过当前页码计数记录前后页
                if self._index == self._count:
                    self.basePath = get_relative_path(self._book_output, self._current_path)
                elif self._index - 1 == self._count:
                    self.prev_title = inner
                    self.prev_relative_path = target
                elif self._index + 1 == self._count:
                    self.next_title = inner
                    self.next_relative_path = target
                pass
            else:
                self.summary[self._count] = {"data_level": self.data_level, "target": target, "title": inner}
                pass
        self._target.append(target)
        logging.info(f"{inner}\t{self.data_level}")
        return template.format(data_level=self.data_level, inner=inner, target=target)

    def render_heading(self, token):
        self._heading_count += 1
        self._data_level = [self._heading_count]
        self._iter_index = 0

        self._iter_count = {}

        template = '<li class="header">{inner}</li>'
        inner = self.render_inner(token)
        return template.format(inner=inner)

    def render_list(self, token):
        self._iter_index += 1
        if self._iter_index in self._iter_count:
            self._iter_count[self._iter_index] += 1
        else:
            self._iter_count[self._iter_index] = 0

        template = '<{tag} {attr}>{inner}</{tag}>'
        tag = 'ul'
        attr = 'class="articles"'

        self._suppress_ptag_stack.append(not token.loose)

        self._data_level.append(self._iter_count.get(self._iter_index))

        _inner = []
        for child in token.children:
            _inner.append(self.render(child))

        inner = "\n".join(_inner)
        self._data_level = self._data_level[:self._iter_index]
        self._iter_index -= 1
        self._suppress_ptag_stack.pop()

        return template.format(tag=tag, attr=attr, inner=inner)

    def render_list_item(self, token):
        if len(token.children) == 0:
            return '<li></li>'
        self._data_level[-1] += 1
        inner = '\n'.join([self.render(child) for child in token.children])

        if self.data_level == self._current_data_level:
            template = '<li class="chapter active" data-level="{data_level}" data-path="{target}">{inner}</li>' \
                .format(data_level=self.data_level, inner=inner, target=self._target.pop())
        else:
            template = '<li class="chapter" data-level="{data_level}" data-path="{target}">{inner}</li>' \
                .format(data_level=self.data_level, inner=inner, target=self._target.pop())

        return template

    def render_paragraph(self, token):
        return '{}'.format(self.render_inner(token))

    def render_document(self, token):
        self.footnotes.update(token.footnotes)
        inner = '\n'.join([self.render(child) for child in token.children])
        return '{}'.format(inner) if inner else ''

    @staticmethod
    def render_thematic_break(token):
        return '<hr />'

    pass


def renderer_summary(book_output, _item, _index, page):
    with SummaryRenderer(book_output=book_output, current_path=_item.get("target", ""),
                         current_data_level=_item.get("data_level"), index=_index) as renderer:
        summary = renderer.render(mistletoe.Document(page))
    summary_classify = {
        'title': _item.get("title", ""),
        'level': _item.get("data_level", ""),
        'prev_title': renderer.prev_title,
        'prev_relative_path': renderer.prev_relative_path,
        'next_title': renderer.next_title,
        'next_relative_path': renderer.next_relative_path,
        'summary': summary,
        'href': _item.get("target", ""),
        'basePath': renderer.basePath
    }
    return summary_classify


def get_relpath(book_output, ref: str, current_ref: str):
    """转换为相对路径

    :param book_output: 书籍目录
    :param ref: 要转换的路径
    :param current_ref: 当前路径
    :return:
    """
    _ref = ref
    if os.path.basename(_ref).lower() == "readme.md":
        if os.path.dirname(ref):
            _ref = get_pure_path(os.path.relpath(os.path.dirname(ref)), "index.md")
        else:
            _ref = "index.md"
    return get_pure_path(get_filename_not_ext(
        os.path.relpath(
            get_pure_path(book_output, _ref),
            os.path.dirname(get_pure_path(book_output, current_ref))
        )
    ))


def get_relative_path(book_output, ref: str):
    """转换本页面相对于根的相对路径"""
    return get_pure_path(os.path.relpath(book_output, os.path.dirname(get_pure_path(book_output, ref))))
