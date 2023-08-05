# -*- coding: utf-8 -*-
# author: Ethosa

from ..eMath import *
from ..utils import Thread_VK
from .EColor import ecolor
import asyncio
import math
import struct
import zlib

class EImage:
    def __init__(self, width=256, height=256, color=b"\xFF\xFF\xFF\xFF"):
        self.width = width
        self.height = height
        self.colors = [[0 for x in range(self.height)] for y in range(self.width)]
        self.fill = lambda color=b"\xFF\xFF\xFF\xFF": asyncio.run(self.fillA(color))
        self.save = lambda file, mode="bmp": asyncio.run(self.saveA(file, mode))
        self.flip = lambda: asyncio.run(self.flipA())
        self.getAt = lambda x, y: asyncio.run(self.getAtA(x, y))
        self.drawRect = lambda x, y, width, height, color=b"\xFF\xFF\xFF\xFF": asyncio.run(self.drawRectA(x, y, width, height, color))
        self.fill(color)

    async def fillA(self, color=b"\xFF\xFF\xFF\xFF"):
        color = ecolor(color)
        for x in range(self.width):
            for y in range(self.height):
                self.colors[x][y] = color

    async def flipA(self):
        obj = []
        for x in range(self.width):
            obj.append(self.colors[x][:])
            self.colors[x] = self.colors[x][::-1]
        self.colors = self.colors[::-1]

    def transpose(self):
        width = self.height
        height = self.width
        self.colors = [[self.colors[x][y] for x in range(self.height)] for y in range(self.width)]
        self.width = width
        self.height = height

    async def getAtA(self, x, y):
        return self.colors[x][y]

    def setAt(self, x, y, color=b"\xFF\xFF\xFF\xFF"):
        self.colors[x][y] = ecolor(color)

    async def drawRectA(self, x, y, width, height, color=b"\xFF\xFF\xFF\xFF"):
        color = ecolor(color)
        for i in range(x, width+x):
            for j in range(y, height+y):
                self.colors[i][j] = color

    def drawLine(self, x1, y1, x2, y2, color=b"\xFF\xFF\xFF\xFF", width=1):
        nb_points = x1+x2 if x1+x2 > y1+y2 else y1+y2
        x_spacing = (x2 - x1) / (nb_points + 1)
        y_spacing = (y2 - y1) / (nb_points + 1)
        color = ecolor(color)
        if width > 1:
            for i in range(1, nb_points+1):
                self.drawCircle((int(x1 + i * x_spacing)+width)//2, (int(y1 + i * y_spacing)+width)//2, width, color)
        else:
            for i in range(1, nb_points+1):
                self.colors[int(x1 + i * x_spacing)][int(y1 + i * y_spacing)] = color


    def drawCircle(self, x, y, r, color=b"\xFF\xFF\xFF\xFF", width=1):
        color = ecolor(color)
        #The lower this value the higher quality the circle is with more points generated
        stepSize = r/r/100

        #Generated vertices
        positions = []

        t = 0
        while t < 2 * math.pi:
            positions.append([int(r * math.cos(t) + x), int(r * math.sin(t) + y)])
            t += stepSize
        for p in positions:
            x = p[0] if p[0] > 0 else p[0]*-2
            y = p[1] if p[1] > 0 else p[1]*-2
            self.colors[x][y] = color

    def drawPath(self, path, color=b"\xFF\xFF\xFF\xFF", width=1):
        color = ecolor(color)
        for p in range(len(path.path)):
            if p+1 < len(path.path):
                self.drawLine(path.path[p].points[0], path.path[p].points[1],
                    path.path[p+1].points[0], path.path[p+1].points[1], color, width)

    def drawTriangle(self, x, y, width, height, color=b"\xFF\xFF\xFF\xFF", lineWidth=1):
        pnt1 = [x, y+height]
        pnt2 = [x+width, y+height]
        pnt3 = [x+(width//2), y]
        self.drawLine(pnt1[0], pnt1[1], pnt2[0], pnt2[1], color, lineWidth)
        self.drawLine(pnt3[0], pnt3[1], pnt2[0], pnt2[1], color, lineWidth)
        self.drawLine(pnt3[0], pnt3[1], pnt1[0], pnt1[1], color, lineWidth)

    def I1(self, value):
        return struct.pack("!B", value & (2**8-1))
    def I1INT(self, value):
        return struct.pack("!B", value)
    def I4(self, value):
        return struct.pack("!I", value)

    async def saveA(self, file, mode="bmp"):
        if mode == "bmp":
            with open(file, "wb") as f:
                f.write(b'BM') # ID field (42h, 4Dh)
                f.write(b'\x9a\x00\x00\x00') # 154 bytes (122+32) Size of the BMP file
                f.write(b'\x00\x00') # Unused
                f.write(b'\x00\x00') # Unused
                f.write(b'z\x00\x00\x00') # 122 bytes (14+108) Offset where the pixel array (bitmap data) can be found
                f.write(b'l\x00\x00\x00') # 108 bytes Number of bytes in the DIB header (from this point)
                f.write((self.width).to_bytes(4,byteorder="little")) # self.width pixels (left to right order) Width of the bitmap in pixels
                f.write((self.height).to_bytes(4,byteorder="little")) # self.height pixels (bottom to top order) Height of the bitmap in pixels
                f.write(b'\x01\x00') # 1 plane Number of color planes being used
                f.write(b' \x00') # 32 bits Number of bits per pixel
                f.write(b'\x03\x00\x00\x00') # 3 BI_BITFIELDS, no pixel array compression used
                f.write(b' \x00\x00\x00') # 32 bytes Size of the raw bitmap data (including padding)
                f.write(b'\x13\x0b\x00\x00') # 2835 pixels/metre horizontal Print resolution of the image,
                f.write(b'\x13\x0b\x00\x00') # 2835 pixels/metre vertical   72 DPI × 39.3701 inches per metre yields 2834.6472
                f.write(b'\x00\x00\x00\x00') # 0 colors Number of colors in the palette
                f.write(b'\x00\x00\x00\x00') # 0 important colors 0 means all colors are important
                f.write(b'\x00\x00\xFF\x00') # 00FF0000 in big-endian Red channel bit mask (valid because BI_BITFIELDS is specified)
                f.write(b'\x00\xFF\x00\x00') # 0000FF00 in big-endian Green channel bit mask (valid because BI_BITFIELDS is specified)
                f.write(b'\xFF\x00\x00\x00') # 000000FF in big-endian Blue channel bit mask (valid because BI_BITFIELDS is specified)
                f.write(b'\x00\x00\x00\xFF') # FF000000 in big-endian Alpha channel bit mask
                f.write(b' niW') # little-endian "Win " LCS_WINDOWS_COLOR_SPACE
                f.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') # CIEXYZTRIPLE Color Space endpoints Unused for LCS "Win " or "sRGB"
                f.write(b'\x00\x00\x00\x00') # 0 Red Gamma Unused for LCS "Win " or "sRGB"
                f.write(b'\x00\x00\x00\x00') # 0 Green Gamma Unused for LCS "Win " or "sRGB"
                f.write(b'\x00\x00\x00\x00') # 0 Blue Gamma Unused for LCS "Win " or "sRGB"
                for x in range(self.width):
                    self.colors[x] = self.colors[x][::-1]
                for x in range(self.height):
                    for y in range(self.width):
                        f.write(self.colors[y][x])
        elif mode == "graypng":
            # generate these chunks depending on image type
            png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')
            # IHDR`
            colortype = 0 # true gray image (no palette)
            bitdepth = 8 # with one byte per pixel (0..255)
            compression = 0 # zlib (no choice here)
            filtertype = 0 # adaptive (each scanline seperately)
            interlaced = 0 # no
            IHDR = self.I4(self.width) + self.I4(self.height) + self.I1INT(bitdepth)
            IHDR += self.I1INT(colortype) + self.I1INT(compression)
            IHDR += self.I1INT(filtertype) + self.I1INT(interlaced)
            block = "IHDR".encode('ascii') + IHDR
            png += self.I4(len(IHDR)) + block + self.I4(zlib.crc32(block))

            # IDAT
            raw = b""
            self.transpose()
            for y in range(self.height):
                raw += b"\0" # no filter for this scanline
                for x in range(self.width):
                    c = self.I1(int.from_bytes(self.colors[y][x], "little"))
                    raw += c
            compressor = zlib.compressobj()
            compressed = compressor.compress(raw)
            compressed += compressor.flush() #!!
            block = "IDAT".encode('ascii') + compressed
            png += self.I4(len(compressed)) + block + self.I4(zlib.crc32(block))

            # IEND
            block = "IEND".encode('ascii')
            png += self.I4(0) + block + self.I4(zlib.crc32(block))
            with open(file,"wb") as f:
                f.write(png)
