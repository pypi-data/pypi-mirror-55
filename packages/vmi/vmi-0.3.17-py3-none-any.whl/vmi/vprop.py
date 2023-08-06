import copyreg
import sys
from typing import List, Optional, Union, Dict

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import vtk

import vmi
import tempfile
import pathlib
import numpy as np

tr = QObject()
tr = tr.tr


class PolyActor(QObject, vmi.Menu, vmi.Mouse):
    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False, repres: str = 'surface',
                 color: Union[QColor, List[float]] = QColor('lightgray'), opacity: float = 1.0, point_size: int = 1,
                 line_width: int = 1, shade: bool = True, always_on_top: bool = False):
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        vmi.Mouse.__init__(self)
        for b in self.mouse:
            for e in self.mouse[b]:
                if e == 'Enter':
                    self.mouse[b][e] = [self.mouseEnter]
                elif e == 'Leave':
                    self.mouse[b][e] = [self.mouseLeave]
                elif e == 'Press':
                    self.mouse[b][e] = [self.mousePress]
                elif e == 'PressMoveRelease':
                    self.mouse[b][e] = [self.mousePass if b == 'RightButton' else self.mouseRelease]
                elif e == 'PressRelease':
                    self.mouse[b][e] = [self.mousePass if b == 'RightButton' else self.mouseRelease]

        self._Mapper = vtk.vtkPolyDataMapper()
        self._Prop = vtk.vtkActor()
        self._Prop._Prop = self

        self._Property: vtk.vtkProperty = self._Prop.GetProperty()
        self._Prop.SetBackfaceProperty(self._Property)

        self._Data = vtk.vtkPolyData()
        self._Bind = self

        self._View = self._Visible = self._Pickable = self._Repres = None
        self._Color = self._Opacity = self._PointSize = self._LineWidth = self._Shade = self._AlwaysOnTop = None
        self.bind()
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.setRepres(repres)
        self.setColor(color)
        self.setOpacity(opacity)
        self.setPointSize(point_size)
        self.setLineWidth(line_width)
        self.setShade(shade)
        self.setAlwaysOnTop(always_on_top)

    def view(self) -> vmi.View:
        return self._View

    def setView(self, view) -> None:
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)

    def updateInTime(self) -> None:
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def repres(self) -> str:
        return self._Repres

    def setRepres(self, repres: str) -> None:
        self.updateInTime()
        if repres == 'points':
            self._Property.SetRepresentationToPoints()
        elif repres == 'wireframe':
            self._Property.SetRepresentationToWireframe()
        elif repres == 'surface':
            self._Property.SetRepresentationToSurface()

    def color(self) -> QColor:
        return self._Color

    def setColor(self, color: Union[QColor, List[float]]) -> None:
        self.updateInTime()
        if isinstance(color, QColor):
            self._Color = color
        else:
            self._Color = QColor.fromRgbF(color[0], color[1], color[2])
        self._Property.SetColor(self._Color.redF(), self._Color.greenF(), self._Color.blueF())

    def opacity(self) -> float:
        return self._Opacity

    def setOpacity(self, opacity: float) -> None:
        self.updateInTime()
        opacity = min(max(opacity, 0.0), 1.0)
        self._Opacity = opacity
        self._Property.SetOpacity(self._Opacity)

    def pointSize(self) -> int:
        return self._PointSize

    def setPointSize(self, point_size: int) -> None:
        point_size = min(max(point_size, 1), 100)
        self._PointSize = point_size
        self._Property.SetPointSize(self._PointSize)

    def lineWidth(self) -> int:
        return self._LineWidth

    def setLineWidth(self, point_size: int) -> None:
        point_size = min(max(point_size, 1), 100)
        self._LineWidth = point_size
        self._Property.SetLineWidth(self._LineWidth)

    def shade(self) -> bool:
        return self._Shade

    def setShade(self, shade: bool) -> None:
        self.updateInTime()
        self._Shade = shade
        self._Property.SetAmbient(0 if self._Shade else 1)
        self._Property.SetDiffuse(1 if self._Shade else 0)

    def alwaysOnTop(self) -> bool:
        return self._AlwaysOnTop

    def setAlwaysOnTop(self, always_on_top: bool) -> None:
        self.updateInTime()
        self._AlwaysOnTop = always_on_top
        if self._AlwaysOnTop:
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
        else:
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-1)

    def data(self) -> vtk.vtkPolyData:
        return self._Bind._Data

    def bind(self, other=None) -> None:
        self.updateInTime()
        if hasattr(other, '_Data'):
            self._Bind = other
        else:
            self._Bind = self
        self._Mapper.SetInputData(self.data())
        self._Prop.SetMapper(self._Mapper)

    def clone(self, other) -> None:
        self.updateInTime()
        if hasattr(other, '_Data'):
            self.data().ShallowCopy(other.data())
        elif isinstance(other, self.data().__class__):
            self.data().ShallowCopy(other)
        elif isinstance(other, vmi.TopoDS_Shape):
            other = vmi.ccPd_Sh(other)
            self.clone(other)
        elif isinstance(other, vmi.Polyhedron_3):
            other = vmi.cgPd_Ph(other)
            self.clone(other)
        else:
            self.data().ShallowCopy(self.data().__class__())

    def scalar(self, image: Optional[vtk.vtkImageData] = None,
               lookup_table: Optional[vtk.vtkScalarsToColors] = None) -> None:
        if image and lookup_table:
            self._Mapper.SetColorModeToMapScalars()
            self._Mapper.SetUseLookupTableScalarRange(1)
            self._Mapper.SetScalarVisibility(1)
            self._Mapper.SetLookupTable(lookup_table)

            probe = vtk.vtkProbeFilter()
            probe.SetInputData(self.data())
            probe.SetSourceData(image)
            probe.Update()
            self.clone(probe.GetOutput())
        else:
            self._Mapper.SetScalarVisibility(0)
            self._Mapper.SetLookupTable(None)

    def delete(self) -> None:
        self.updateInTime()
        self._Data.ReleaseData()
        self.setView(None)

    def mouseEnter(self, **kwargs) -> None:
        self.updateInTime()
        c = self._Color.lighter(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())

    def mousePress(self, **kwargs) -> None:
        self.updateInTime()
        c = self._Color.darker(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())

    def mouseRelease(self, **kwargs) -> None:
        self.updateInTime()
        self._Property.SetColor(self._Color.redF(), self._Color.greenF(), self._Color.blueF())

    def mouseLeave(self, **kwargs) -> None:
        self.updateInTime()
        self._Property.SetColor(self._Color.redF(), self._Color.greenF(), self._Color.blueF())


def pickle_PolyActor(instance: PolyActor):
    data_attr = ['_AlwaysOnTop', '_Color', '_LineWidth', '_Opacity', '_Pickable', '_PointSize', '_Repres', '_Shade',
                 '_Visible']
    data_attr = {kw: getattr(instance, kw) for kw in data_attr}

    data_vtk = ['_Data', '_Mapper', '_Prop', '_Property']
    data_vtk = {kw: vmi.vtkInstance_gets(getattr(instance, kw)) for kw in data_vtk}
    data = {'data_attr': data_attr, 'data_vtk': data_vtk}
    return unpickle_PolyActor, (data,)


def unpickle_PolyActor(data):
    data_attr = data['data_attr']
    data_vtk = data['data_vtk']
    instance = PolyActor()
    for kw in data_vtk:
        vmi.vtkInstance_sets(getattr(instance, kw), data_vtk[kw])
    for kw in data_attr:
        getattr(instance, kw.replace('_', 'set', 1))(data_attr[kw])
    return instance


copyreg.pickle(PolyActor, pickle_PolyActor)


class ImageBox(QObject, vmi.Menu, vmi.Mouse):
    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 image: QImage = QImage(1, 1, QImage.Format.Format_RGB32),
                 size: List[float] = (0.5, 0.5), pos: List[float] = (0.5, 0.5), anchor: List[float] = (0.5, 0.5)):
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        vmi.Mouse.__init__(self)
        for b in self.mouse:
            for e in self.mouse[b]:
                if e == 'Enter':
                    self.mouse[b][e] = [self.mouseEnter]
                elif e == 'Leave':
                    self.mouse[b][e] = [self.mouseLeave]
                elif e == 'Press':
                    self.mouse[b][e] = [self.mousePress]
                elif e == 'PressMoveRelease':
                    self.mouse[b][e] = [self.mousePass if b == 'RightButton' else self.mouseRelease]
                elif e == 'PressRelease':
                    self.mouse[b][e] = [self.mousePass if b == 'RightButton' else self.mouseRelease]

        self._Mapper = vtk.vtkImageMapper()
        self._Mapper.SetColorLevel(128)
        self._Mapper.SetColorWindow(256)

        self._Prop = vtk.vtkActor2D()
        self._Prop._Prop = self
        self._Property: vtk.vtkProperty = self._Prop.GetProperty()
        self._Data = vtk.vtkImageData()
        self._Bind = self

        self._View = self._Visible = self._Pickable = None
        self._Image = QImage(1, 1, QImage.Format.Format_RGB32)
        self._Size = [0.5, 0.5]
        self._Pos = [0.5, 0.5]
        self._Anchor = [0.5, 0.5]
        self.bind()
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.draw(image=image, size=size, pos=pos, anchor=anchor)

    def resize(self) -> None:
        self.draw()

    def data(self) -> vtk.vtkImageData:
        return self._Bind._Data

    def bind(self, other=None) -> None:
        self.updateInTime()
        if hasattr(other, '_Data'):
            self._Bind = other
        self._Mapper.SetInputData(self.data())
        self._Prop.SetMapper(self._Mapper)

    def draw(self, image: QImage = None, size: List[float] = None, pos: List[float] = None,
             anchor: List[float] = None) -> None:
        self.updateInTime()

        if image is not None:
            self._Image = image

        if size is not None:
            self._Size = [min(max(size[0], 0), 1), min(max(size[1], 0), 1)]

        if pos is not None:
            self._Pos = [min(max(pos[0], 0), 1), min(max(pos[1], 0), 1)]

        if anchor is not None:
            self._Anchor = [min(max(anchor[0], 0), 1), min(max(anchor[1], 0), 1)]

        if self.view():
            # 图像缩放
            size = [round(self._Size[0] * self.view().width()), round(self._Size[1] * self.view().height())]
            image = self._Image.scaled(size[0], size[1], Qt.AspectRatioMode.KeepAspectRatio)

            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '.png'
                image.save(str(p), 'PNG')

                r = vtk.vtkPNGReader()
                r.SetFileName(str(p))
                r.Update()
                self.data().ShallowCopy(r.GetOutput())

            # 图像定位
            pos = [round(self._Pos[0] * self.view().width()), round(self._Pos[1] * self.view().height())]
            anchor = [round(self._Anchor[0] * image.width()), round((1 - self._Anchor[1]) * image.height())]

            self._Prop.SetPosition(pos[0] - anchor[0], self.view().height() - pos[1] - anchor[1])

    def view(self) -> vmi.View:
        return self._View

    def setView(self, view) -> None:
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)

    def updateInTime(self) -> None:
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def image(self) -> QImage:
        return self._Image

    def size(self) -> List[float]:
        return self._Size

    def pos(self) -> List[float]:
        return self._Pos

    def anchor(self) -> List[float]:
        return self._Anchor

    def mouseEnter(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(96)
        self._Mapper.SetColorWindow(256)

    def mousePress(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(160)
        self._Mapper.SetColorWindow(256)

    def mouseRelease(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(128)
        self._Mapper.SetColorWindow(256)

    def mouseLeave(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(128)
        self._Mapper.SetColorWindow(256)


def pickle_ImageBox(instance: ImageBox):
    data_attr = ['_Pickable', '_Visible']
    data_attr = {kw: getattr(instance, kw) for kw in data_attr}

    data_draw = ['_Anchor', '_Image', '_Pos', '_Size']
    data_draw = {kw: getattr(instance, kw) for kw in data_draw}

    data_vtk = ['_Data', '_Mapper', '_Prop', '_Property']
    data_vtk = {kw: vmi.vtkInstance_gets(getattr(instance, kw)) for kw in data_vtk}

    data = {'data_attr': data_attr, 'data_draw': data_draw, 'data_vtk': data_vtk}
    return unpickle_ImageBox, (data,)


def unpickle_ImageBox(data):
    data_attr = data['data_attr']
    data_draw = data['data_draw']
    data_vtk = data['data_vtk']
    instance = ImageBox()
    for kw in data_vtk:
        vmi.vtkInstance_sets(getattr(instance, kw), data_vtk[kw])
    for kw in data_attr:
        getattr(instance, kw.replace('_', 'set', 1))(data_attr[kw])

    instance.draw(image=data_draw['_Image'], size=data_draw['_Size'], pos=data_draw['_Pos'],
                  anchor=data_draw['_Anchor'])
    return instance


copyreg.pickle(ImageBox, pickle_ImageBox)


class TextBox(ImageBox):
    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 text: str = str(), text_font: str = '等线', text_align: str = 'AlignCenter',
                 fore_color: QColor = QColor('black'), back_color: QColor = QColor('whitesmoke'),
                 bold: bool = False, italic: bool = False, underline: bool = False,
                 size: List[float] = (0.5, 0.5), pos: List[float] = (0.5, 0.5), anchor: List[float] = (0.5, 0.5)):
        ImageBox.__init__(self, view=view, visible=visible, size=size, pos=pos, anchor=anchor, pickable=pickable)

        self._Text = str()
        self._TextFont = '等线'
        self._TextAlign = 'AlignCenter'
        self._ForeColor = QColor('black')
        self._BackColor = QColor('whitesmoke')
        self._Bold = False
        self._Italic = False
        self._Underline = False
        self.draw_text(text=text, text_font=text_font, text_align=text_align,
                       fore_color=fore_color, back_color=back_color,
                       bold=bold, italic=italic, underline=underline,
                       size=size, pos=pos, anchor=anchor)

    def font(self) -> str:
        return self._TextFont

    def text(self) -> str:
        return self._Text

    def text_align(self) -> str:
        return self._TextAlign

    def fore_color(self) -> QColor:
        return self._ForeColor

    def back_color(self) -> QColor:
        return self._BackColor

    def bold(self) -> bool:
        return self._Bold

    def italic(self) -> bool:
        return self._Italic

    def underline(self) -> bool:
        return self._Underline

    def draw_text(self, text: str = None, text_font: str = None, text_align: str = None,
                  fore_color: QColor = None, back_color: QColor = None,
                  bold: bool = None, italic: bool = None, underline: bool = None,
                  size: List[float] = None, pos: List[float] = None, anchor: List[float] = None) -> None:
        if text is not None:
            self._Text = text
        if text_font is not None:
            self._TextFont = text_font
        if text_align is not None:
            self._TextAlign = text_align
        if fore_color is not None:
            self._ForeColor = fore_color
        if back_color is not None:
            self._BackColor = back_color
        if bold is not None:
            self._Bold = bold
        if italic is not None:
            self._Italic = italic
        if underline is not None:
            self._Underline = underline

        if self.view():
            w = round(self._Size[0] * self.view().width())
            h = round(self._Size[1] * self.view().height())

            pa = QPainter()

            # 字体
            font_size = 16
            font = QFont(self._TextFont, font_size)
            font.setPointSizeF(font_size)
            font.setBold(self._Bold)
            font.setItalic(self._Italic)
            font.setUnderline(self._Underline)

            # 计算字体大小
            image = QImage(w, h, QImage.Format.Format_RGB32)

            pa.begin(image)
            pa.setPen(self._ForeColor)
            # for s in range(2,18):
            pa.setFont(font)
            rect = pa.drawText(0, 0, w, h, getattr(Qt, self._TextAlign), self._Text)
            if rect.width() > 0 and rect.height() > 0:
                if 0.5 * h / rect.height() < (w - 20) / rect.width():
                    font_size *= 0.5 * h / rect.height()
                else:
                    font_size *= (w - 20) / rect.width()
                font.setPointSizeF(font_size)
            pa.end()

            # 绘制文本
            image = QImage(w, h, QImage.Format.Format_RGB32)
            pa.begin(image)
            pa.setFont(font)
            pa.setPen(self._ForeColor)
            pa.fillRect(0, 0, w, h, self._BackColor)
            pa.drawText(0, 0, w, h, getattr(Qt, self._TextAlign), self._Text)
            pa.end()

            self.draw(image=image, size=size, pos=pos, anchor=anchor)

    def setView(self, view) -> None:
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)

    def resize(self) -> None:
        self.draw_text()


def pickle_TextBox(instance: TextBox):
    data_attr = ['_Pickable', '_Visible']
    data_attr = {kw: getattr(instance, kw) for kw in data_attr}

    data_draw = ['_Anchor', '_BackColor', '_Bold', '_ForeColor', '_Italic', '_Pos', '_Size', '_Text', '_TextAlign',
                 '_TextFont', '_Underline']
    data_draw = {kw: getattr(instance, kw) for kw in data_draw}

    data_vtk = ['_Data', '_Mapper', '_Prop', '_Property']
    data_vtk = {kw: vmi.vtkInstance_gets(getattr(instance, kw)) for kw in data_vtk}

    data = {'data_attr': data_attr, 'data_draw': data_draw, 'data_vtk': data_vtk}
    return unpickle_TextBox, (data,)


def unpickle_TextBox(data):
    data_attr = data['data_attr']
    data_draw = data['data_draw']
    data_vtk = data['data_vtk']
    instance = TextBox()
    for kw in data_vtk:
        vmi.vtkInstance_sets(getattr(instance, kw), data_vtk[kw])
    for kw in data_attr:
        getattr(instance, kw.replace('_', 'set', 1))(data_attr[kw])
    instance.draw_text(text=data_draw['_Text'], text_font=data_draw['_TextFont'], text_align=data_draw['_TextAlign'],
                       fore_color=data_draw['_ForeColor'], back_color=data_draw['_BackColor'],
                       bold=data_draw['_Bold'], italic=data_draw['_Italic'], underline=data_draw['_Underline'],
                       size=data_draw['_Size'], pos=data_draw['_Pos'], anchor=data_draw['_Anchor'])
    return instance


copyreg.pickle(TextBox, pickle_TextBox)


class ImageSlice(QObject, vmi.Menu, vmi.Mouse):
    """场景表示，图像数据的断层表示
    vtk.vtkImageData -> vtk.vtkImageSlice"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = True,
                 colorWindow: List[int] = (350, 50)):
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        self.actions = {'SlicePlaneValueNormal': QAction(''),
                        'SlicePlaneAxial': QAction(tr('横断位 (Axial)')),
                        'SlicePlaneSagittal': QAction(tr('矢状位 (Sagittal)')),
                        'SlicePlaneCoronal': QAction(tr('冠状位 (Coronal)')),
                        'WindowValue': QAction(''),
                        'WindowAuto': QAction(tr('自动 (Auto)')),
                        'WindowBone': QAction(tr('骨骼 (Bone)')),
                        'WindowSoft': QAction(tr('组织 (Soft)'))}

        self.actions['SlicePlaneAxial'].triggered.connect(self.setSlicePlane_Axial)
        self.actions['SlicePlaneSagittal'].triggered.connect(self.setSlicePlane_Sagittal)
        self.actions['SlicePlaneCoronal'].triggered.connect(self.setSlicePlane_Coronal)
        self.actions['WindowAuto'].triggered.connect(self.setColorWindow_Auto)
        self.actions['WindowBone'].triggered.connect(self.setColorWindow_Bone)
        self.actions['WindowSoft'].triggered.connect(self.setColorWindow_Soft)

        def aboutToShow():
            self.actions['SlicePlaneValueNormal'].setText(
                tr('法向 (Normal)') + ' = ' + repr(self._BindSlicePlane._SlicePlane.GetNormal()))
            self.actions['WindowValue'].setText(
                tr('宽/位 (W/L)') + ' = ' + (repr(tuple(self._ColorWindow))))

            self.menu.clear()

            menu = QMenu(tr('切面 (Slice plane)'))
            menu.addAction(self.actions['SlicePlaneValueNormal'])
            menu.addSeparator()
            menu.addAction(self.actions['SlicePlaneAxial'])
            menu.addAction(self.actions['SlicePlaneSagittal'])
            menu.addAction(self.actions['SlicePlaneCoronal'])
            self.menu.addMenu(menu)

            menu = QMenu(tr('窗 (Window)'))
            menu.addAction(self.actions['WindowValue'])
            menu.addSeparator()
            menu.addAction(self.actions['WindowAuto'])
            menu.addAction(self.actions['WindowBone'])
            menu.addAction(self.actions['WindowSoft'])
            self.menu.addMenu(menu)

        self.menu.aboutToShow.connect(aboutToShow)

        vmi.Mouse.__init__(self, menu=self)
        self.mouse['NoButton']['Wheel'] = [self.slice]
        self.mouse['LeftButton']['PressMove'] = [self.windowMove]

        self._Mapper = vtk.vtkImageResliceMapper()
        self._Prop = vtk.vtkImageSlice()
        self._Prop._Prop = self

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToCubic()
        self._Property.SetUseLookupTableScalarRange(1)

        self._Data = vtk.vtkImageData()
        self._Bind = self

        self._SlicePlane = vtk.vtkPlane()
        self._BindSlicePlane = self

        self._LookupTable = vtk.vtkLookupTable()
        self._BindLookupTable = self

        self._View = self._Visible = self._Pickable = None
        self._ColorWindow = [350, 50]
        self.bind()
        self.bindSlicePlane()
        self.bindLookupTable()
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.setColorWindow(colorWindow)

    def view(self) -> vmi.View:
        return self._View

    def setView(self, view) -> None:
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)

    def updateInTime(self) -> None:
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def data(self) -> vtk.vtkImageData:
        return self._Bind._Data

    def slicePlane(self) -> vtk.vtkPlane:
        return self._BindSlicePlane._SlicePlane

    def lookupTable(self) -> vtk.vtkLookupTable:
        return self._BindLookupTable._LookupTable

    def bind(self, other=None) -> None:
        self.updateInTime()
        if hasattr(other, '_Data'):
            self._Bind = other
        elif other is not None:
            raise AttributeError(other)
        self._Mapper.SetInputData(self.data())
        self._Prop.SetMapper(self._Mapper)

    def bindSlicePlane(self, other=None) -> None:
        if hasattr(other, '_SlicePlane'):
            self._BindSlicePlane = other
        self._Mapper.SetSlicePlane(self.slicePlane())
        self.updateInTime()

    def bindLookupTable(self, other=None) -> None:
        if hasattr(other, '_LookupTable'):
            self._BindLookupTable = other
        self._Property.SetLookupTable(self.lookupTable())
        self.updateInTime()

    def setLookupTable(self, lookup_table) -> None:
        self._LookupTable = lookup_table
        self.bind(self._BindLookupTable)
        self.updateInTime()

    def clone(self, other) -> None:
        self.updateInTime()
        if hasattr(other, '_Data'):
            self.data().ShallowCopy(other.data())
        elif isinstance(other, self.data().__class__):
            self.data().ShallowCopy(other)
        else:
            self.data().ShallowCopy(self.data().__class__())

    def delete(self) -> None:
        self.updateInTime()
        self._Data.ReleaseData()
        self.setView(None)

    def setSlicePlane(self, origin: Union[np.ndarray, List[float]], normal: Union[np.ndarray, List[float]]) -> None:
        self.updateInTime()
        self.slicePlane().SetOrigin(origin)
        self.slicePlane().SetNormal(normal)

    def setSlicePlaneOrigin(self, origin: Union[np.ndarray, List[float]]) -> None:
        self.updateInTime()
        self.slicePlane().SetOrigin(origin)

    def setSlicePlaneNormal(self, normal: Union[np.ndarray, List[float]]) -> None:
        self.updateInTime()
        self.slicePlane().SetNormal(normal)

    def setSlicePlaneOrigin_Center(self) -> None:
        self.setSlicePlaneOrigin(self.data().GetCenter())

    def setSlicePlane_Axial(self) -> None:
        self.slicePlane().SetNormal(0, 0, 1)

    def setSlicePlane_Sagittal(self) -> None:
        self.slicePlane().SetNormal(-1, 0, 0)

    def setSlicePlane_Coronal(self) -> None:
        self.slicePlane().SetNormal(0, -1, 0)

    def setInterpolationType_Nearest(self) -> None:
        self._Property.SetInterpolationTypeToNearest()
        self.updateInTime()

    def setInterpolationType_Linear(self) -> None:
        self._Property.SetInterpolationTypeToLinear()
        self.updateInTime()

    def setInterpolationType_Cubic(self) -> None:
        self._Property.SetInterpolationTypeToCubic()
        self.updateInTime()

    def setColorWindow(self, color_window: List[int]) -> None:
        width = min(max(round(color_window[0]), 0), 20000)
        level = min(max(round(color_window[1]), -10000), 10000)

        self._ColorWindow[0] = int(width)
        self._ColorWindow[1] = int(level)

        r = [self._ColorWindow[1] - 0.5 * self._ColorWindow[0],
             self._ColorWindow[1] + 0.5 * self._ColorWindow[0]]

        t = self.lookupTable()
        t.SetNumberOfTableValues(self._ColorWindow[0])
        t.SetTableRange(r)
        t.SetBelowRangeColor(0, 0, 0, 1.0)
        t.SetAboveRangeColor(1, 1, 1, 1.0)
        t.SetUseBelowRangeColor(1)
        t.SetUseAboveRangeColor(1)

        for i in range(self._ColorWindow[0]):
            v = i / self._ColorWindow[0]
            t.SetTableValue(i, (v, v, v, 1.0))
        self.updateInTime()

    def setColorWindowWidth(self, width: int) -> None:
        width = min(max(width, 0), 20000)
        self.setColorWindow([width, self._ColorWindow[1]])

    def setColorWindowLevel(self, level: int) -> None:
        level = min(max(level, -10000), 10000)
        self.setColorWindow([self._ColorWindow[0], level])

    def setColorWindow_Auto(self) -> None:
        r = vtk.vtkImageHistogramStatistics()
        r.SetInputData(self.data())
        r.SetAutoRangePercentiles(1, 99)
        r.SetGenerateHistogramImage(0)
        r.Update()
        r = r.GetAutoRange()
        self.setColorWindow([round(r[1] - r[0]), round(0.5 * (r[0] + r[1]))])

    def setColorWindow_Bone(self) -> None:
        self.setColorWindow([1000, 400])

    def setColorWindow_Soft(self) -> None:
        self.setColorWindow([350, 50])

    def slice(self, **kwargs) -> Optional[bool]:
        o = list(self.slicePlane().GetOrigin())
        n = self.slicePlane().GetNormal()
        dim = self.data().GetDimensions()
        dxyz = self.data().GetSpacing()

        n = [abs(_) / (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5 for _ in n]
        dn = n[0] * dxyz[0] + n[1] * dxyz[1] + n[2] * dxyz[2]

        for i in range(3):
            if dim[i] > 1:
                o[i] += kwargs['delta'] * dn * n[i]

        if vtk.vtkMath.PlaneIntersectsAABB(self.data().GetBounds(), n, o) == 0:
            self.setSlicePlaneOrigin(o)
        return True

    def windowMove(self, **kwargs) -> Optional[bool]:
        if self.view():
            dx, dy = self.view().pickVt_Display()

            r = self.data().GetScalarRange()
            t = (r[1] - r[0]) / 2048

            width = self._ColorWindow[0] + t * dx
            level = self._ColorWindow[1] - t * dy

            width = round(min(max(width, 0), r[1] - r[0]))
            level = round(min(max(level, r[0]), r[1]))
            self.setColorWindow([width, level])
            return True


def pickle_ImageSlice(instance: ImageSlice):
    data_attr = ['_Pickable', '_Visible', '_ColorWindow']
    data_attr = {kw: getattr(instance, kw) for kw in data_attr}

    data_vtk = ['_Data', '_Mapper', '_Prop', '_Property', '_LookupTable', '_SlicePlane']
    data_vtk = {kw: vmi.vtkInstance_gets(getattr(instance, kw)) for kw in data_vtk}
    data = {'data_attr': data_attr, 'data_vtk': data_vtk}
    return unpickle_ImageSlice, (data,)


def unpickle_ImageSlice(data):
    data_attr = data['data_attr']
    data_vtk = data['data_vtk']
    instance = ImageSlice()
    for kw in data_vtk:
        vmi.vtkInstance_sets(getattr(instance, kw), data_vtk[kw])
    for kw in data_attr:
        getattr(instance, kw.replace('_', 'set', 1))(data_attr[kw])
    return instance


copyreg.pickle(ImageSlice, pickle_ImageSlice)


class ImageVolume(QObject, vmi.Menu, vmi.Mouse):
    """场景表示，图像数据的立体表示
    vtk.vtkImageData -> vtk.vtkVolume"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 color: Dict[int, List[float]] = None, opacityScalar: Dict[int, float] = None,
                 opacityGradient: Dict[int, float] = None):
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        self.actions = {'Threshold': QAction(tr('阈值 (Threshold)'))}
        self.actions['Threshold'].triggered.connect(self.setColor_Threshold)

        def aboutToShow():
            self.menu.clear()

            menu = QMenu(tr('风格 (Style)'))
            menu.addAction(self.actions['Threshold'])
            self.menu.addMenu(menu)

        self.menu.aboutToShow.connect(aboutToShow)

        vmi.Mouse.__init__(self)

        self._Mapper = vtk.vtkGPUVolumeRayCastMapper()
        self._Prop = vtk.vtkVolume()
        self._Prop._Prop = self

        self._Mapper.SetBlendModeToComposite()
        self._Mapper.SetMaxMemoryInBytes(4096)
        self._Mapper.SetMaxMemoryFraction(1)
        self._Mapper.SetAutoAdjustSampleDistances(0)
        self._Mapper.SetLockSampleDistanceToInputSpacing(1)
        self._Mapper.SetUseJittering(1)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToLinear()
        self._Property.SetAmbient(0)
        self._Property.SetDiffuse(1)
        self._Property.SetShade(1)

        self._Data = vtk.vtkImageData()
        self._Bind = self

        self._View = self._Visible = self._Pickable = None
        self._Color = self._OpacityScalar = self._OpacityGradient = None

        self.bind()
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.setColor(color if color else {0: [1, 1, 1]})
        self.setOpacityScalar(opacityScalar if opacityScalar else {0: 0, 400: 1})
        self.setOpacityGradient(opacityGradient if opacityGradient else {})

    def view(self) -> vmi.View:
        return self._View

    def setView(self, view) -> None:
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)

    def updateInTime(self) -> None:
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def data(self) -> vtk.vtkImageData:
        return self._Bind._Data

    def delete(self) -> None:
        self.updateInTime()
        image = vtk.vtkImageData()
        image.SetExtent(0, 0, 0, 0, 0, 0)
        image.AllocateScalars(vtk.VTK_SHORT, 1)
        self.clone(image)
        self.setView(None)

    def bind(self, other=None) -> None:
        if hasattr(other, '_Data'):
            self._Bind = other
        elif other is not None:
            raise AttributeError(other)
        self._Mapper.SetInputData(self.data())
        self._Prop.SetMapper(self._Mapper)
        self.updateInTime()

    def clone(self, other) -> None:
        self.updateInTime()
        if hasattr(other, 'data'):
            self.data().ShallowCopy(other.data())
        elif isinstance(other, self.data().__class__):
            self.data().ShallowCopy(other)
        else:
            self.data().ShallowCopy(self.data().__class__())

    def setColor(self, color: Dict[int, List[float]]) -> None:
        self.updateInTime()
        self._Color = color
        f = vtk.vtkColorTransferFunction()
        for x in self._Color:
            r, g, b = self._Color[x]
            f.AddRGBPoint(x, r, g, b)
        self._Property.SetColor(f)

    def setColor_Threshold(self, threshold: int = None):
        self.setOpacityScalar({threshold - 1: 0, threshold: 1})

    def setOpacityScalar(self, opacity_scalar: Dict[int, float]) -> None:
        self.updateInTime()
        self._OpacityScalar = opacity_scalar
        f = vtk.vtkPiecewiseFunction()
        for x in self._OpacityScalar:
            f.AddPoint(x, self._OpacityScalar[x])
        self._Property.SetScalarOpacity(f)

    def setOpacityGradient(self, opacity_gradient: Dict[int, float]) -> None:
        self.updateInTime()
        self._OpacityGradient = opacity_gradient
        f = vtk.vtkPiecewiseFunction()
        for x in self._OpacityGradient:
            f.AddPoint(x, self._OpacityGradient[x])
        self._Property.SetGradientOpacity(f)


def pickle_ImageVolume(instance: ImageVolume):
    data_attr = ['_Pickable', '_Visible']
    data_attr = {kw: getattr(instance, kw) for kw in data_attr}

    data_vtk = ['_Data', '_Mapper', '_Prop', '_Property', '_Color', '_OpacityScalar', '_OpacityGradient']
    data_vtk = {kw: vmi.vtkInstance_gets(getattr(instance, kw)) for kw in data_vtk}
    data = {'data_attr': data_attr, 'data_vtk': data_vtk}
    return unpickle_ImageVolume, (data,)


def unpickle_ImageVolume(data):
    data_attr = data['data_attr']
    data_vtk = data['data_vtk']
    instance = ImageVolume()
    for kw in data_vtk:
        vmi.vtkInstance_sets(getattr(instance, kw), data_vtk[kw])
    for kw in data_attr:
        getattr(instance, kw.replace('_', 'set', 1))(data_attr[kw])
    return instance


copyreg.pickle(ImageVolume, pickle_ImageVolume)
