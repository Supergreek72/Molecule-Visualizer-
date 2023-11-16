import molecule;

radius = {}
element_name = {}
header = """<svg version="1.1" width="1000" height="1000"
xmlns = "http://www.w3.org/2000/svg">""";
footer = """</svg>""";
offsetx = 500;
offsety = 500;

class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.z = c_atom.z

    def __str__(self):
        return '''x: %f' y: %f z: %f element: %c"''' % (self.c_atom.x,self.c_atom.y, self.z, self.c_atom.element)
    
    def svg(self):       
        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (self.c_atom.x * 100 + offsetx,self.c_atom.y * 100 + offsety,
                                                                      radius[self.c_atom.element],element_name[self.c_atom.element])
    
class Bond:
    def __init__(self, c_bond):
        self.c_bond = c_bond
        self.z = c_bond.z

    def __str__(self):
        return '''x1: %f' x2: %f y1: %f y2: %f z: %f len: %f dx: %f dy: %f epairs: %d"''' % (self.c_bond.x1,self.c_bond.x2,self.c_bond.y1,self.c_bond.x2,
                                                                                  self.c_bond.z,self.c_bond.len,self.c_bond.dx,self.c_bond.dy,self.c_bond.epairs)
    
    def svg(self):       
        #come back to this maybe to add ifs for when the angle changes ?
        return ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % ((self.c_bond.x1 * 100 + offsetx)  + self.c_bond.dy * 10.0, (self.c_bond.y1 * 100 + offsety ) - self.c_bond.dx * 10.0,
                                                                                                (self.c_bond.x2 * 100 + offsetx) + self.c_bond.dy * 10.0, (self.c_bond.y2 * 100 + offsety) - self.c_bond.dx * 10.0,
                                                                                                (self.c_bond.x2 * 100 + offsetx) - self.c_bond.dy * 10.0, (self.c_bond.y2 * 100 + offsety) + self.c_bond.dx * 10.0,
                                                                                                (self.c_bond.x1 * 100 + offsetx) - self.c_bond.dy * 10.0, (self.c_bond.y1 * 100 + offsety) + self.c_bond.dx * 10.0
                                                                                                
                                                                                                
                                                                                                
                                                                                                )

class Molecule(molecule.molecule):
    def __str__(self):
        outputString = ""
        #get all the atoms
        for i in range(self.atom_no):
            outputString += "atom # " + str(i) + ": " + str(self.atoms[i]) + "\n"
        outputString += "\n"

        #get all the bonds
        for i in range(self.bond_no):
            outputString += "bond # " + str(i) + ": " + str(self.bonds[i]) + "\n"

        return outputString
    
    def svg(self):
        outputString = ""
        #add header
        outputString += header
        
        newList = []

        #add atoms
        for i in range(self.atom_no):
            newList.append(Atom(self.get_atom(i)))
       
        #add bonds
        for i in range(self.bond_no):
            newList.append(Bond(self.get_bond(i)))

        #sort the list
        newList.sort(key=lambda x: x.z)
        
        #loop through and add the svg outputs 
        for i in range(len(newList)):

            outputString += newList[i].svg()
            

        #add the footer to the string
        outputString += footer

        return outputString
    

    def parse(self, f):
        #skip to actual stuff 
        f.readline()
        f.readline()
        f.readline()

        data = []
        #read the info line
        data = f.readline().split()
        
        numAtoms = int(data[0])
        numBonds = int(data[1])
        

        #new list
        atomdata = []
        x = 0.0
        y = 0.0
        z = 0.0
        el = ""

        #loop through atoms 
        for i in range(numAtoms):
            atomdata = f.readline().split()

            #take in the data for an atom
            x = float(atomdata[0])
            y = float(atomdata[1])
            z = float(atomdata[2])
            el = atomdata[3]

            #appened a new atom
            self.append_atom(el,x,y,z)
           
            

        #new list
        bonddata = []
        a1 = 0
        a2 = 0
        epairs = 0
        #loop through bonds 
        for i in range(numBonds):
            bonddata = f.readline().split()

            a1 = int(bonddata[0]) - 1
            a2 = int(bonddata[1]) - 1
            epairs = int(bonddata[2])
           

            #appened a new bond
            self.append_bond(a1,a2,epairs)


        




def main():
    mol = Molecule()
    f = open("CID_31260.sdf", "r")

    mol.parse(f) 


       
    print(mol.svg())
    f.close()

if __name__ == "__main__":
    main()

    