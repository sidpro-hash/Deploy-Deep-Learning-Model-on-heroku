def utilsize(height,width):
    fontthick = 1
    rectsize = 1
    fontscale = 1
    ymargin=10

    if height <= 600 or width <=600:
        fontthick = 1
        rectsize = 1
        fontscale = 1
        print("height <= 600")
        if height <=600:
            ymargin=10
    elif height <= 800 or width <=800:
        fontthick = 2
        rectsize = 2
        fontscale = 1.5
        print("height <= 800")
        if height <=800:
            ymargin=20
    elif height <=1200 or width <=1200:
        fontthick = 2
        rectsize = 2
        fontscale = 2.5
        print("height <= 1200")
        if height <= 1200:
            ymargin=30
    elif height <=2000 or width <=2000:
        fontthick = 3
        rectsize = 3
        fontscale = 3
        print("2000")
        if height <=2000:
            ymargin=40
    elif height <=4000 or width<=4000:
        fontthick = 4
        rectsize = 4
        fontscale = 5
        print("height <= 4000")
        if height <=4000:
            ymargin=50
    elif height > 4000 or width > 4000:
        fontthick = 5
        rectsize = 5
        fontscale = 6
        print("height > 4000")
        if height > 4000:
            ymargin:60
    
    return (fontthick,rectsize,fontscale,ymargin)