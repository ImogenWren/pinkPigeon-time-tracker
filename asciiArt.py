'''
ASCII Art


'''

import prettyCLI

dft = prettyCLI.pcli["df"]                # default all

pnk = prettyCLI.pcli["fg"]["pink"]
wht = prettyCLI.pcli["fg"]["white"]
blu = prettyCLI.pcli["fg"]["cyan"]
ylw = prettyCLI.pcli["fg"]["yellow"]
blk = prettyCLI.pcli["fg"]["black"]
gry = prettyCLI.pcli["fg"]["grey"]

bgbwht =  prettyCLI.pcli["bg"]["white"]

pigeonArt = f"{pnk} " + r"""           
                         -
    \                  /   @ )
      \             _/_   |~ \)
        \     ( ( (     \ \
         ( ( ( ( (       | \
_ _=(_(_(_(_(_(_(_  _ _ /  )
                -  _ _ _  /
                      _\___
                     `    "'                                                                 
""" + f"{dft}"

#print(pigeonArt)