from MolDisplay import Molecule
import MolDisplay
import os
import sqlite3




#database class
class Database():

    def __init__(self, reset):
        #check for reset key
        if(reset == True):
            os.remove( 'molecules.db' )
            self.conn = sqlite3.connect( 'molecules.db' )
        else:
            self.conn = sqlite3.connect( 'molecules.db' )
    
    def create_tables(self):

        # Create a cursor object
        cursor = self.conn.cursor()

        # Check if the table exists
        table_name = 'Elements'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        # Print the result
        if table_exists == False:
          #come back to make sure i am not remaking the tables 
          #create elements table
          self.conn.execute( """CREATE TABLE Elements 
                  ( ELEMENT_NO     INTEGER     NOT NULL,
                    ELEMENT_CODE   VARCHAR(3)  NOT NULL,
                    ELEMENT_NAME   VARCHAR(32) NOT NULL,
                    COLOUR1        CHAR(6)     NOT NULL,
                    COLOUR2        CHAR(6)     NOT NULL,
                    COLOUR3        CHAR(6)     NOT NULL,
                    RADIUS         DECIMAL(3)  NOT NULL,
                    PRIMARY KEY (ELEMENT_CODE) );""" )
        
        # Check if the table exists
        table_name = 'Atoms'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        # Print the result
        if table_exists == False:
          #create atoms table 
          self.conn.execute( """CREATE TABLE Atoms 
                  ( ATOM_ID        INTEGER      NOT NULL   PRIMARY KEY   AUTOINCREMENT,
                    ELEMENT_CODE   VARCHAR(3)   NOT NULL,
                    x              DECIMAL(7,4) NOT NULL,
                    y              DECIMAL(7,4) NOT NULL,
                    z              DECIMAL(7,4) NOT NULL,
                    FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements);""" )
          
        # Check if the table exists
        table_name = 'Bonds'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        # Print the result
        if table_exists == False:
          #create bonds table 
          self.conn.execute( """CREATE TABLE Bonds 
                  ( BOND_ID        INTEGER   NOT NULL PRIMARY KEY  AUTOINCREMENT,
                    A1             INTEGER   NOT NULL,
                    A2             INTEGER   NOT NULL,
                    EPAIRS         INTEGER   NOT NULL);""" )
          
        # Check if the table exists
        table_name = 'Molecules'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        # Print the result
        if table_exists == False:
          #create molecules table 
          self.conn.execute( """CREATE TABLE Molecules 
                  ( MOLECULE_ID    INTEGER   NOT NULL       PRIMARY KEY     AUTOINCREMENT ,
                    NAME           TEXT      NOT NULL       UNIQUE);""" )

        # Check if the table exists
        table_name = 'MoleculeAtom'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        # Print the result
        if table_exists == False:
          #create MoleculeAtom table 
          self.conn.execute( """CREATE TABLE MoleculeAtom 
                  ( MOLECULE_ID    INTEGER    NOT NULL,
                    ATOM_ID        INTEGER    NOT NULL,
                    PRIMARY KEY (MOLECULE_ID,ATOM_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                    FOREIGN KEY (ATOM_ID)     REFERENCES Atoms);""" )

        # Check if the table exists
        table_name = 'MoleculeBond'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        # Print the result
        if table_exists == False:  
          #create MoleculeBond table 
          self.conn.execute( """CREATE TABLE MoleculeBond
                  ( MOLECULE_ID    INTEGER      NOT NULL,
                    BOND_ID        INTEGER      NOT NULL,
                    PRIMARY KEY (MOLECULE_ID,BOND_ID)
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                    FOREIGN KEY (BOND_ID)     REFERENCES Bonds);""" )

        cursor.close()


    def __setitem__( self, table, values ):
      
      #check the table and insert values
      if(table == "Elements"):
        self.conn.execute("INSERT INTO Elements (ELEMENT_NO,ELEMENT_CODE,ELEMENT_NAME,COLOUR1,COLOUR2,COLOUR3,RADIUS) VALUES (?, ?, ?, ?, ?, ?, ?);", (values[0],values[1],values[2],values[3],values[4],values[5],values[6]))
      elif(table == "Atoms"):
        self.conn.execute("INSERT INTO Atoms (ATOM_ID,ELEMENT_CODE,x,y,z) VALUES (?, ?, ?, ?, ?);", (values[0],values[1],values[2],values[3],values[4]))
      elif(table == "Bonds"):
        self.conn.execute("INSERT INTO Bonds (BOND_ID,A1,A2,EPAIRS) VALUES (?, ?, ?, ?);", (values[0],values[1],values[2],values[3]))
      elif(table == "Molecules"):
        self.conn.execute(f"""INSERT INTO Molecules (NAME) VALUES ('{values[0]}');""")
      elif(table == "MoleculeAtom"):
        self.conn.execute("INSERT INTO MoleculeAtom (BOND_ID) VALUES (?);", (values[0]))
      elif(table == "MoleculeBond"):
        self.conn.execute("INSERT INTO MoleculeBond (BOND_ID) VALUES (?);", (values[0]))
      #commit the changes
      self.conn.commit()

    def add_atom( self, molname, atom ):
       
      #add the atom to the database 
      #self.conn['Atoms'] = (atom.element,atom.x,atom.y,atom.z)
      self.conn.execute("""INSERT INTO Atoms (ELEMENT_CODE,x,y,z) VALUES (?, ?, ?, ?);""", (atom.element,atom.x,atom.y,atom.z))
      #commit the changes
      self.conn.commit()
      

      #find the atom id 
      c = self.conn.cursor()
      c.execute("""SELECT ATOM_ID FROM Atoms ORDER BY ATOM_ID DESC LIMIT 1;""")
      atomid = c.fetchone()
      

      #find the molecule id
      c.execute("""SELECT MOLECULE_ID FROM Molecules ORDER BY MOLECULE_ID DESC LIMIT 1;""")
      moleculeid = c.fetchone()
      

      #self.conn['MoleculeAtom'] = (atomid,moleculeid)
      self.conn.execute("""INSERT INTO MoleculeAtom (MOLECULE_ID,ATOM_ID) VALUES (?, ?);""", (*moleculeid,*atomid))
      #commit the changes
      self.conn.commit()
      #close cursor 
      c.close()


    def add_bond( self, molname, bond ):
       
      #add the bonds to the database 
      self.conn.execute("""INSERT INTO Bonds (A1,A2,EPAIRS) VALUES (?, ?, ?);""", (bond.a1,bond.a2,bond.epairs))
      #commit the changes
      self.conn.commit()

      #find the bond id 
      c = self.conn.cursor()
      c.execute("""SELECT BOND_ID FROM Bonds ORDER BY BOND_ID DESC LIMIT 1;""")
      bondid = c.fetchone()

      #find the molecule id
      c.execute("""SELECT MOLECULE_ID FROM Molecules ORDER BY MOLECULE_ID DESC LIMIT 1;""")
      moleculeid = c.fetchone()

      self.conn.execute("""INSERT INTO MoleculeBond (MOLECULE_ID,BOND_ID) VALUES (?, ?);""", (*moleculeid,*bondid))
      #commit the changes
      self.conn.commit()
      #close cursor 
      c.close()
       
    def add_molecule( self, name, fp ):

      #create the molecule 
      mol = Molecule()

      #parse the file
      mol.parse(fp)

      #add the molecule table the database
      self.conn.execute(f"""INSERT INTO Molecules(NAME) VALUES ('{name}');""")
      #commit the changes
      self.conn.commit()


      #add the atoms to the database
      for i in range(mol.atom_no):
        self.add_atom(name,mol.get_atom(i))

      #add the bonds to the database
      for i in range(mol.bond_no):
        self.add_bond(name,mol.get_bond(i))
      
      

    def load_mol( self, name ):
      #create a mol
      mol = Molecule()

      #find the atoms 
      c = self.conn.cursor()
      #print(self.conn.execute("""SELECT NAME FROM Molecules WHERE Molecules.NAME = 'Water'""").fetchall())
      c.execute(f"""SELECT Atoms.*
      FROM Atoms
      JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
      JOIN Molecules ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
      WHERE Molecules.NAME = ('{name}');""" )
      atoms = c.fetchall()
      #print(atoms)

      #add the atoms 
      for i in range(len(atoms)):
        mol.append_atom(atoms[i][1],atoms[i][2],atoms[i][3],atoms[i][4])
        
      

      #find the bonds
      c.execute(f"""SELECT Bonds.*
      FROM Bonds
      JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.Bond_ID
      JOIN Molecules ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
      WHERE Molecules.NAME = ('{name}');""")
      bonds = c.fetchall()
      
      

      #add the bonds 
      for i in range(len(bonds)):
        mol.append_bond(bonds[i][1],bonds[i][2],bonds[i][3])
        #mol.append_bond(bonds[i][4],bonds[i][5],bonds[i][6])
        #print(bonds[i][2],bonds[i][3],bonds[i][4],bonds[i][5])
      #("Bonds:\n" + str(bonds[0][2]) + str(bonds[0][3]) + "\n" + str(bonds[0][4]) + str(bonds[0][5]) + "\nEpairs:" + str(bonds[0][6]))
      
      
      c.close()
      return mol   
    
    def radius( self ):
      dict = {}

      #find the codes 
      c = self.conn.cursor()
      c.execute("""SELECT RADIUS,ELEMENT_CODE 
                  FROM Elements;""")
      values = c.fetchall()

      #add them to the dict
      for i in range(len(values)):
        dict[values[i][1]] = values[i][0]

      return dict

    def element_name( self ):
      dict = {}

      #find the codes 
      c = self.conn.cursor()
      c.execute("""SELECT ELEMENT_NAME,ELEMENT_CODE 
                  FROM Elements;""")
      values = c.fetchall()

      #add them to the dict
      for i in range(len(values)):
        dict[values[i][1]] = values[i][0]
      
      c.close()
      return dict
    
    def radial_gradients( self ):

      #find the codes 
      c = self.conn.cursor()
      c.execute("""SELECT ELEMENT_NAME,COLOUR1,COLOUR2,COLOUR3 
                  FROM Elements;""")
      values = c.fetchall()
      radialGradientSVG = ""
      #create the svg offset
      for i in range(len(values)):
        radialGradientSVG += """
        <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
        <stop offset="0%%" stop-color="#%s"/>
        <stop offset="50%%" stop-color="#%s"/>
        <stop offset="100%%" stop-color="#%s"/>
        </radialGradient>""" % (values[i][0],values[i][1],values[i][2],values[i][3])
      
      c.close()
      return radialGradientSVG


    def getMolecules(self):
      list = ()

      #get the names of molecules in db
      c = self.conn.cursor()
      c.execute("""SELECT NAME FROM Molecules;""")
      list = c.fetchall()

      c.close()
      return list

    def getAtoms(self, name):
      a = 0

      #get the names of molecules in db
      c = self.conn.cursor()
      c.execute(f"""SELECT COUNT(*) FROM Atoms join MoleculeAtom JOIN Molecules WHERE atoms.atom_id = MoleculeAtom.molecule_id 
                   AND MoleculeAtom.molecule_id = Molecules.MOLECULE_ID AND Molecules.name = ('{name}');""")
      a = c.fetchall()

      c.close()
      return a
    
    def getBonds(self, name):
      b = 0

      #get the names of molecules in db
      c = self.conn.cursor()
      c.execute(f"""SELECT COUNT(*) FROM Bonds join MoleculeBond JOIN Molecules WHERE Bonds.bond_id = MoleculeBond.molecule_id 
                    AND MoleculeBond.molecule_id = Molecules.MOLECULE_ID AND Molecules.name = ('{name}');""")
      b = c.fetchall()

      c.close()
      return b
    
    def getElements(self):
      list = ()

      #get all the elements 
      c = self.conn.cursor()
      c.execute("""SELECT * FROM Elements;""")
      list = c.fetchall()

      c.close()
      return list
    
    def reset(self):
      #remove databasefile
      os.remove( 'molecules.db' )
      self.conn = sqlite3.connect( 'molecules.db' )
      #create tables again
      self.create_tables()

    def getElementNames(self):
      list = ()

      #get the names of elements in db
      c = self.conn.cursor()
      c.execute("""SELECT ELEMENT_NAME FROM Elements;""")
      list = c.fetchall()

      c.close()
      return list
    
    def deleteElement(self, name):

      c = self.conn.cursor()
      # execute the DELETE statement
      c.execute(f"""DELETE FROM Elements WHERE ELEMENT_NAME = ('{name}');""")
      c.close()


      
if __name__ == "__main__":
  db = Database(reset=False); # or use default
  MolDisplay.radius = db.radius();
  MolDisplay.element_name = db.element_name();
  MolDisplay.header += db.radial_gradients();
  for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
    mol = db.load_mol( molecule );
    mol.sort();
    fp = open( molecule + ".svg", "w" );
    fp.write( mol.svg() );
    fp.close();

