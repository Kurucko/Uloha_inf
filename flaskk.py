from flask import Flask, render_template, url_for, request, jsonify
import math
from PIL import Image, ImageColor
import os
import base64


def rasterizacia(subor: str, ww) -> Image:
    from PIL import Image, ImageColor
    import os
    #if subor:
    sprava = ""
    def linePixels(A, B):
        pixels = []
        if A[0] == B[0]:
            if A[1] > B[1]:
                A, B = B, A
            for y in range(A[1], B[1] + 1):
                pixels.append((A[0], y))
        elif A[1] == B[1]:
            if A[0] > B[0]:
                A, B = B, A
            for x in range(A[0], B[0] + 1):
                pixels.append((x, A[1]))
        else:
            if A[0] > B[0]:
                A, B = B, A
            dx = B[0] - A[0]
            dy = B[1] - A[1]
            if abs(dy / dx) > 1:
                for y in range(min(A[1], B[1]), max(A[1], B[1]) + 1):
                    x = int((y - A[1] + (dy / dx) * A[0]) * (dx / dy))
                    pixels.append((x, y))
            else:
                for x in range(min(A[0], B[0]), max(A[0], B[0]) + 1):
                    y = int((B[1] - A[1]) / (B[0] - A[0]) * (x - A[0]) + A[1])
                    pixels.append((x, y))
        return pixels

    def line(obr, AX, AY, BX, BY, color):
        A = (AX, AY)
        B = (BX, BY)
        pixels = []
        if A[0] == B[0]:  # rovna zvisla ciara
            if A[1] > B[1]:
                A, B = B, A
            for y in range(A[1], B[1] + 1):
                obr.putpixel((A[0], y), color)
        elif A[1] == B[1]:  # rovna ciara
            if A[0] > B[0]:
                A, B = B, A
            for x in range(A[0], B[0] + 1):
                obr.putpixel((x, A[1]), color)
        else:  # hocijaka ina ciara
            if A[0] > B[0]:
                A, B = B, A
            dx = B[0] - A[0]
            dy = B[1] - A[1]
            if abs(dy / dx) > 1:
                for y in range(min(A[1], B[1]), max(A[1], B[1]) + 1):
                    x = int((y - A[1] + (dy / dx) * A[0]) * (dx / dy))
                    obr.putpixel((x, y), color)
            else:
                for x in range(min(A[0], B[0]), max(A[0], B[0]) + 1):
                    y = int((B[1] - A[1]) / (B[0] - A[0]) * (x - A[0]) + A[1])
                    obr.putpixel((x, y), color)

    def circle(obr, sx, sy, r, thickness, farba, *args):
        s = (sx, sy)
        if sx > 0 and sy > 0:
            for i in range(1, r + 1):
                filled_circle(obr, int(s[0] - i), int(s[1] - ((r - i) * (r + i)) ** 0.5), thickness, farba,*args)
                filled_circle(obr, int(s[0] + i), int(s[1] - ((r - i) * (r + i)) ** 0.5), thickness, farba,*args)
                filled_circle(obr, int(s[0] + i), int(s[1] + ((r - i) * (r + i)) ** 0.5), thickness, farba,*args)
                filled_circle(obr, int(s[0] - i), int(s[1] + ((r - i) * (r + i)) ** 0.5), thickness, farba,*args)

                filled_circle(obr, int(s[0] - ((r - i) * (r + i)) ** 0.5), int(s[1] - i), thickness, farba,*args)
                filled_circle(obr, int(s[0] - ((r - i) * (r + i)) ** 0.5), int(s[1] + i), thickness, farba,*args)
                filled_circle(obr, int(s[0] + ((r - i) * (r + i)) ** 0.5), int(s[1] + i), thickness, farba,*args)
                filled_circle(obr, int(s[0] + ((r - i) * (r + i)) ** 0.5), int(s[1] - i), thickness, farba,*args)

    def filled_circle(obr, sx, sy, r, farba, *args):
        s = (sx, sy)
        if args==():
            w,h =0,0
            w2,h2 = obr.width, obr.height
        else:
            w2,h2,w,h = args
        if sx > w and sy > h and sx < w2 and sy < h2:
            for x in range(s[0] - r, s[0] + r + 1):
                for y in range(s[1] - r, s[1] + r + 1):
                    if (x - s[0]) ** 2 + (y - s[1]) ** 2 <= r ** 2:
                        if x > w and y > h and x < w2 and y < h2:
                            obr.putpixel((x, y), farba)

    def thick_line(obr, AX, AY, BX, BY, thickness, color):
        A = (AX, AY)
        B = (BX, BY)
        pixels = linePixels(A, B)
        for x, y in pixels:
            filled_circle(obr, x, y, thickness // 2, color)

    def triangle_moj(obr, A, B, C, color):
        """ Funguje, ale kus pomalé, dusan ma lepsie """
        ab = linePixels(A, B)
        bc = linePixels(B, C)
        ac = linePixels(A, C)
        for x, y in ab:
            thick_line(obr, C, (x, y), 1, color)
        for x, y in bc:
            thick_line(obr, A, (x, y), 1, color)
        for x, y in ac:
            thick_line(obr, B, (x, y), 1, color)

    def fill_triangle(im, AX, AY, BX, BY, CX, CY, color):
        # Nakrelis do obrazku im trojuhlnik s bodmi ABC a farbou color
        A = (AX, AY)
        B = (BX, BY)
        C = (CX, CY)
        V = sorted([A, B, C], key=lambda x: x[1])
        left = linePixels(V[0], V[1]) + linePixels(V[1], V[2])
        right = linePixels(V[0], V[2])

        Xmax = max(A[0], B[0], C[0])
        Xmin = min(A[0], B[0], C[0])

        if V[1][0] == Xmax:
            left, right = right, left
        for y in range(V[0][1], V[2][1] + 1):
            x1 = Xmax
            for X in left:
                if X[1] == y and X[0] < x1:
                    x1 = X[0]
            x2 = Xmin
            for X in right:
                if X[1] == y and X[0] > x2:
                    x2 = X[0]
            if x2 < 0:
                continue
            if x2 > im.width:
                x2 = im.width - 1
            if x1 < 0:
                x1 = 0
            line(im, x1, y, x2, y, color)

    def rect(obr, ax, ay, width, height, thickness, color):
        thick_line(obr, ax, ay, ax + width, ay, thickness, color)
        thick_line(obr, ax + width, ay, ax + width, ay + height, thickness, color)
        thick_line(obr, ax + width, ay + height, ax, ay + height, thickness, color)
        thick_line(obr, ax, ay + height, ax, ay, thickness, color)

    def fill_rect(obr, ax, ay, width, height, color):
        for x in range(ax, ax + width + 1):
            for y in range(ay, ay + height + 1):
                obr.putpixel((x, y), color)

    def clear(obr, color):
        for x in range(obr.size[0]):
            for y in range(obr.size[1]):
                obr.putpixel((x, y), color)

    def triangle(obr, AX, AY, BX, BY, CX, CY, THICKNESS, COLOR):
        thick_line(obr, AX, AY, BX, BY, THICKNESS, COLOR)
        thick_line(obr, AX, AY, CX, CY, THICKNESS, COLOR)
        thick_line(obr, CX, CY, BX, BY, THICKNESS, COLOR)


    def vertical_gradient(obr, AX, AY, width, height,zac_percenta, konecna_percenta,zaciatocna,konecna):
        """Percenta urcuju kde a aky prudky ma byt prechod medzi jednotlivymi farbami"""

        zaciatocna = ImageColor.getcolor("{}".format(zaciatocna), "RGB")
        konecna = ImageColor.getcolor("{}".format(konecna), "RGB")
        kolko = ((konecna[0]-zaciatocna[0] ) / ( width / 100 * abs(zac_percenta - konecna_percenta)),
                    (konecna[1]-zaciatocna[1]) / (width / 100 * abs(zac_percenta - konecna_percenta)),
                    (konecna[2]- zaciatocna[2] ) / ( width / 100 * abs(zac_percenta - konecna_percenta)))

        dalsia = (zaciatocna[0]+ kolko[0], zaciatocna[1]+ kolko[1], zaciatocna[2]+ kolko[2])
        for x in range(AX, AX+int(width/100*zac_percenta)):
            for y in range(AY, AY+height):
                obr.putpixel((x,y), zaciatocna)

        for x in range(AX+int(width/100*zac_percenta),AX+ int(width/100*konecna_percenta) ):
            for y in range(AY, AY+height ):
                obr.putpixel((x,y), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
            dalsia = (dalsia[0]+ kolko[0], dalsia[1]+ kolko[1], dalsia[2]+ kolko[2])


        for x in range(AX+int(width/100*konecna_percenta), AX+width ):
            for y in range(AY, AY+height):
                obr.putpixel((x,y), konecna)

    def linear_gradient(obr, AX, AY, width, height,zac_percenta, konecna_percenta,zaciatocna,  konecna,):
        """Percenta urcuju kde a aky prudky ma byt prechod medzi jednotlivymi farbami"""

        zaciatocna = ImageColor.getcolor("{}".format(zaciatocna), "RGB")
        konecna = ImageColor.getcolor("{}".format(konecna), "RGB")
        kolko = ((konecna[0] - zaciatocna[0]) / (height / 100 * abs(zac_percenta - konecna_percenta)),
                    (konecna[1] - zaciatocna[1]) / ( height / 100 * abs(zac_percenta - konecna_percenta)),
                    (konecna[2] - zaciatocna[2]) / ( height/ 100 * abs(zac_percenta - konecna_percenta)))

        dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])

        for y in range(AY, AY+ int(height/100*zac_percenta)):
            for x in range(AX, AX+width):
                obr.putpixel((x, y), zaciatocna)

        for y in range(AY+int(height/100*zac_percenta), AY + int(height/100*konecna_percenta) ):
            for x in range(AX, AX+width):
                obr.putpixel((x,y), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
            dalsia = (dalsia[0] + kolko[0], dalsia[1] + kolko[1], dalsia[2] + kolko[2])

        for y in range(AY+int(height/100*konecna_percenta), AY+height ):
            for x in range(AX, AX+width):
                obr.putpixel((x, y), konecna)

    def kruhovy_gradient(obr, AX, AY, width, height, sx,sy, zac_percenta, konecne_percenta, nasobitel, zaciatocna, konecna):
        zaciatocna = ImageColor.getcolor("{}".format(zaciatocna), "RGB")
        konecna = ImageColor.getcolor("{}".format(konecna), "RGB")

        r = int((width / 100 * zac_percenta))
        r2 = int((width / 100 * konecne_percenta))
        kolko = ( (konecna[0] - zaciatocna[0]) / (r2-r+nasobitel), (konecna[1] - zaciatocna[1]) / (r2-r+nasobitel), (konecna[2] - zaciatocna[2]) / (r2-r+nasobitel))

        dalsia = (round(zaciatocna[0] + kolko[0]), round(zaciatocna[1] + kolko[1]), round(zaciatocna[2] + kolko[2]))
        for x in range(AX, AX+width):
            for y in range(AY,AY+height):
                    obr.putpixel((x,y), konecna)
        filled_circle(obr, sx, sy, int(r), zaciatocna,AX + width, AY + height, AX, AY)

        for i in range(r,r2+nasobitel):
            circle(obr,sx,sy,i//2,1,(round(dalsia[0]), round(dalsia[1]), round(dalsia[2])),AX + width, AY + height, AX,AY)
            dalsia = (dalsia[0] + kolko[0], dalsia[1] + kolko[1], dalsia[2] + kolko[2])

    def kruhovy_gradient2(obr,sx,sy, *args,**kwargs:list):
        farby = [ImageColor.getcolor("{}".format(i), "RGB") for i in kwargs["farby"]]
        polomery = [int(i) for i in args]
        casti = []
        prechody = []

        for i in range(len(farby)-1)[::-1]:
            for j in range(len(farby[i])):
                casti.append(farby[i+1][j]-farby[i][j])
            prechody.append(casti)
            casti = []
        prechody = prechody[::-1]
        kolko=[]


        for i in range(len(polomery)-1):
            kolko.append(list(map(lambda x:x/(polomery[i+1]-polomery[i]),prechody[i] )))

        filled_circle(obr, sx, sy, polomery[-1]//2, farby[-1])
        filled_circle(obr, sx, sy, polomery[0]//2, farby[0])

        for i in range(1,len(polomery)):
            dalsia = (farby[i-1][0] + kolko[i-1][0], farby[i-1][1] + kolko[i-1][1], farby[i-1][2] + kolko[i-1][2])
            for j in range(polomery[i-1], polomery[i]):
                circle(obr,sx,sy,j//2,1,(round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0] + kolko[i-1][0], dalsia[1] + kolko[i-1][1], dalsia[2] + kolko[i-1][2])

    def horizontalny_gradient_v_kruhu(obr, sx,sy,r, *args, **kwargs):
        farby = [ImageColor.getcolor("{}".format(i), "RGB") for i in kwargs["farby"]]
        casti = []
        prechody = []
        dlzky = [int(2*r/100*int(i)) for i in args]
        for i in range(len(farby)-1)[::-1]:
            for j in range(len(farby[i])):
                casti.append(farby[i+1][j]-farby[i][j])
            prechody.append(casti)
            casti = []
        prechody = prechody[::-1]
        kolko = []

        for i in range(len(dlzky)-1):
            kolko.append(list(map(lambda x:x/(dlzky[i+1]-dlzky[i]),prechody[i] )))


        for y in range(sy - r, (sy -r)+dlzky[0]):
            for x in range(sx-r, sx+r):
                if (x-sx)**2+(y-sy)**2<= r**2:
                    obr.putpixel((x, y), farby[0])

        for i in range(1,len(dlzky)):
            dalsia = (
            farby[i - 1][0] + kolko[i - 1][0], farby[i - 1][1] + kolko[i - 1][1], farby[i - 1][2] + kolko[i - 1][2])
            for y in range(sy - r + dlzky[i-1], (sy - r) + dlzky[i]):
                for x in range(sx - r, sx + r):
                    if (x - sx) ** 2 + (y - sy) ** 2 <= r ** 2:
                        obr.putpixel((x, y), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0] + kolko[i - 1][0], dalsia[1] + kolko[i - 1][1], dalsia[2] + kolko[i - 1][2])


        for y in range((sy - r)+dlzky[-1], (sy +r)):
            for x in range(sx-r, sx+r):
                if (x-sx)**2+(y-sy)**2<= r**2:
                    obr.putpixel((x, y), farby[-1])

    def vertikalny_gradient_v_kruhu(obr, sx,sy,r, *args, **kwargs):
        farby = [ImageColor.getcolor("{}".format(i), "RGB") for i in kwargs["farby"]]
        casti = []
        prechody = []
        dlzky = [int(2 * r / 100 * int(i)) for i in args]
        for i in range(len(farby) - 1)[::-1]:
            for j in range(len(farby[i])):
                casti.append(farby[i + 1][j] - farby[i][j])
            prechody.append(casti)
            casti = []
        prechody = prechody[::-1]
        kolko = []

        for i in range(len(dlzky) - 1):
            kolko.append(list(map(lambda x: x / (dlzky[i + 1] - dlzky[i]), prechody[i])))

        for x in range(sx - r, (sx - r) + dlzky[0]):
            for y in range(sy - r, sy + r):
                if (x - sx) ** 2 + (y - sy) ** 2 <= r ** 2:
                    obr.putpixel((x, y), farby[0])

        for i in range(1, len(dlzky)):
            dalsia = (
                farby[i - 1][0] + kolko[i - 1][0], farby[i - 1][1] + kolko[i - 1][1],
                farby[i - 1][2] + kolko[i - 1][2])
            for x in range(sx - r + dlzky[i - 1], (sx - r) + dlzky[i]):
                for y in range(sy - r, sy + r):
                    if (x - sx) ** 2 + (y - sy) ** 2 <= r ** 2:
                        obr.putpixel((x, y), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0] + kolko[i - 1][0], dalsia[1] + kolko[i - 1][1], dalsia[2] + kolko[i - 1][2])

        for x in range((sx - r) + dlzky[-1], (sx + r)):
            for y in range(sy - r, sy + r):
                if (x - sx) ** 2 + (y - sy) ** 2 <= r ** 2:
                    obr.putpixel((x, y), farby[-1])

    def gradient_trojuholnik(obr, AX,AY, width,zac_percenta,konecna_percenta, zaciatocna, konecna):
        zaciatocna = ImageColor.getcolor("{}".format(zaciatocna), "RGB")
        konecna = ImageColor.getcolor("{}".format(konecna), "RGB")
        kolko = ((konecna[0] - zaciatocna[0]) / ((3**0.5*width/2) / 100 * abs(zac_percenta - konecna_percenta)),
                    (konecna[1] - zaciatocna[1]) / ((3**0.5*width/2) / 100 * abs(zac_percenta - konecna_percenta)),
                    (konecna[2] - zaciatocna[2]) / ((3**0.5*width/2) / 100 * abs(zac_percenta - konecna_percenta)))
        dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])




        for y in range(1, width//2):
            dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])
            for x in range(1, int(((3**0.5*y)))):
                obr.putpixel((x+AX, y+AY), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0]+ kolko[0], dalsia[1]+ kolko[1], dalsia[2]+ kolko[2])

        for y in range(width//2,width):
            dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])
            for x in range(1, int(((3 ** 0.5 * (width-y))))):
                obr.putpixel((AX + x, y + AY), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0] + kolko[0], dalsia[1] + kolko[1], dalsia[2] + kolko[2])

    def gradient_trojuholnik2(obr, AX,AY, width,zac_percenta,konecna_percenta, zaciatocna, konecna):
        zaciatocna = ImageColor.getcolor("{}".format(zaciatocna), "RGB")
        konecna = ImageColor.getcolor("{}".format(konecna), "RGB")
        kolko = (
        (konecna[0] - zaciatocna[0]) / ((3 ** 0.5 * width / 2) / 100 * abs(zac_percenta - konecna_percenta)),
        (konecna[1] - zaciatocna[1]) / ((3 ** 0.5 * width / 2) / 100 * abs(zac_percenta - konecna_percenta)),
        (konecna[2] - zaciatocna[2]) / ((3 ** 0.5 * width / 2) / 100 * abs(zac_percenta - konecna_percenta)))
        dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])

        for y in range(1, width // 2):
            dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])
            for x in range(1, int(((3 ** 0.5 * y)))):
                obr.putpixel((AX-x, y + AY), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0] + kolko[0], dalsia[1] + kolko[1], dalsia[2] + kolko[2])

        for y in range(width // 2, width):
            dalsia = (zaciatocna[0] + kolko[0], zaciatocna[1] + kolko[1], zaciatocna[2] + kolko[2])
            for x in range(1, int(((3 ** 0.5 * (width - y))))):
                obr.putpixel((AX - x, y + AY), (round(dalsia[0]), round(dalsia[1]), round(dalsia[2])))
                dalsia = (dalsia[0] + kolko[0], dalsia[1] + kolko[1], dalsia[2] + kolko[2])


    funkcie = {"CLEAR": clear, "FILL_TRIANGLE": fill_triangle, "FILL_CIRCLE": filled_circle, "FILL_RECT": fill_rect,
                "CIRCLE": circle, "RECT": rect, "LINE": thick_line, "TRIANGLE": triangle,
                }
    gradienty = {"LINEAR_GRADIENT":linear_gradient, "VERTICAL_GRADIENT":vertical_gradient, "KRUHOVY_GRADIENT":kruhovy_gradient,
                    "GRADIENT_TROJUHOLNIK":gradient_trojuholnik, "GRADIENT_TROJUHOLNIK2":gradient_trojuholnik2}
    gradienty2 = {"HORIZONTALNY_GRADIENT_V_KRUHU":horizontalny_gradient_v_kruhu, "KRUHOVY_GRADIENT2":kruhovy_gradient2,
                    "VERTIKALNY_GRADIENT_V_KRUHU":vertikalny_gradient_v_kruhu}
    
    
    daco = subor[0].strip().split(" ")
    try:
        if daco[0] != "VES":
            sprava = "WrongFormat Error: Neznámy format"
            return sprava,""
    except Exception:
        sprava = "WrongFormat Error: Nespravny format"
        quit()
    # assert daco[0] == "VES", "WrongFormat Error: Nespravny format"
    w, h = int(daco[2]), int(daco[3])
    
    obr = Image.new("RGB", (w, h), "white")
    x = 0
    for i in subor[1:]:
        x +=1
        prikaz = i.strip().split(" ")
        if prikaz == [""] or prikaz[0][0]=="#":
            continue
        else:
            try:
                if prikaz[0] in funkcie.keys():
                        funkcie[prikaz[0]](obr, *[int(i) for i in prikaz[1:-1]],
                                            ImageColor.getcolor("{}".format(prikaz[-1]), "RGB"))

                elif prikaz[0] in gradienty.keys():
                    gradienty[prikaz[0]](obr, *[int(i) for i in prikaz[1:-2]], prikaz[-2], prikaz[-1])
                elif prikaz[0] in gradienty2.keys():

                    ind = prikaz.index(list(filter(lambda x: x[0] == "#", prikaz[1:]))[0])
                    gradienty2[prikaz[0]](obr,*[int(i) for i in prikaz[1:ind]], farby=[i for i in prikaz[ind:]])

                else:
                    sprava = f'Syntax error on line  {x + 1}: Unknown command "{prikaz[0]}"'
                    print(f'Syntax error on line  {x + 1}: Unknown command "{prikaz[0]}" ')
            except Exception as e:
                sprava = f'Synatx error on line {x + 1}: Nespravne argumenty pre funkciu "{prikaz[0]}" ' 
                print(f'Synatx error on line {x + 1}: Nespravne argumenty pre funkciu "{prikaz[0]}" ')

    #rozlisenie = input("Jake rozlisenie? zadaj sirku: ").strip()
    rozlisenie = ""
    if rozlisenie == "":
        w, h = int(daco[2]), int(daco[3])
    else:
        try:
            w = int(rozlisenie)
            h = int(int(daco[3]) / int(daco[2]) * w)
            print(w,h)
        except Exception:
            sprava = "Nespravne rozlisenie"
            print("Nespravne rozlisenie")
            quit()
    ulozit="n"
    #ulozit = input("Chces aj ulozit? (y/n): ").lower()
    if ulozit == "y":
        try:
            nazov = input("nazov obrazka: ")
            formatt = input("jaky format: .").lower()
            obr.save(f"{nazov}.{formatt}")
            sprava = "Subor uspesne ulozeny"
            print("Subor uspesne ulozeny")
        except Exception:
            sprava = "neda sa ulozit, sory bratu"
            print("neda sa ulozit, sory bratu")
    #kruhovy_gradient2(obr, 100,100,20,100,150,farby=["#e3746b", "#38db28", "#5dc7e2"])
    #horizontalny_gradient_v_kruhu(obr,100,100,50,40,60,80,farby=["#e3746b", "#38db28", "#5dc7e2"])
    #obrazok_pre_dusana(obr,200,200,150,10, farby=["#693ef9","#fb0094","#fb0033","#fb73c3" , "#0000FF","#FF0000"], percenta=[20,25,30,40,45])
    #vertikalny_gradient_v_kruhu(obr,100,100,50,40,60,80,farby=["#e3746b", "#38db28", "#5dc7e2"])
    #gradient_trojuholnik(obr,100,100,60,20,80,"#38db28","#5dc7e2" )
    ww = float(ww)
    ratio = ww/w
    h = int(ratio * h)                       
    obr = obr.resize((int(ww), h))
    # obr.show()

    return sprava,obr
    # else:
    #     print("Neexistuje taky subor :(")

#rasterizacia("te.txt")



app = Flask(__name__, template_folder='template')



@app.route("/")
def hello():
    return render_template("index.html")

# @app.route("/")
@app.route("/", methods=["POST"])
def save_data():
    
    data = request.form["data"]
    w = request.form["w"]
    my_var = data
    
    
    my_var += "\n"
    my_var = my_var.split("\n")
    
    sprava, img = rasterizacia(my_var,w)
    if os.path.exists(f"static/canvas.png"):
        os.remove(f"static/canvas.png")
    if img != "":
        img.save(f"static/canvas.png")
    with open("static/canvas.png", "rb") as f:
         image_bytes = f.read()
         image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print(os.path.exists(f"static/canvas.png"))
    return jsonify(sprava, image_base64,os.path.exists(f"static/canvas.png"))
  


