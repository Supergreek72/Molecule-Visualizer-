from os import environ
import os
import re
from MolDisplay import Molecule
import molecule
from molsql import Database
import MolDisplay
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import sys
import io
import json
import cgi
import urllib;





class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            page = open("home.html").read()
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( page, "utf-8" ))
            self.wfile.write(page.encode())

        elif self.path == '/table-values':
            list = db.getElements()
            
            # Set the response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Convert the data to JSON and return it
            json_data = json.dumps(list)
            self.wfile.write(json_data.encode())

        elif self.path == '/upload.html':
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            page = open("upload.html").read()
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( page, "utf-8" ))
            self.wfile.write(page.encode())

        elif self.path == '/home.html':
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            page = open("home.html").read()
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( page, "utf-8" ))
            self.wfile.write(page.encode())
        
        elif self.path == '/elements.html':
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            page = open("elements.html").read()
            self.send_header( "Content-length", len(page) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( page, "utf-8" ))
            self.wfile.write(page.encode())

        elif self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            css = open("style.css").read()
            self.send_header( "Content-length", len(css) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( css, "utf-8" ))
            self.wfile.write(css.encode())

        elif self.path == '/script.js': 
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            js = open("script.js").read()
            self.send_header( "Content-length", len(js) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( js, "utf-8" ))
            self.wfile.write(js.encode())

        elif self.path == '/element.js':
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            js = open("element.js").read()
            self.send_header( "Content-length", len(js) )
            self.end_headers()

            #write the page
            self.wfile.write( bytes( js, "utf-8" ))
            self.wfile.write(js.encode())
        
        elif self.path == '/get-values':

            values = db.getMolecules()

            # Convert the data to a JSON string
            data_json = json.dumps(values)
            
            # Set the content type header
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Send the data to the client
            self.wfile.write(data_json.encode())

        elif self.path == '/get-element-names':
            values = db.getElementNames()

            # Convert the data to a JSON string
            data_json = json.dumps(values)
            
            # Set the content type header
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Send the data to the client
            self.wfile.write(data_json.encode())
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

  

    def do_POST(self):
        if self.path == "/upload.html":

           # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
        
            molName = postvars['molName'][0]
            fileStuff = postvars['fileStuff'][0]
            f = io.TextIOWrapper(io.BytesIO(bytes(fileStuff, 'UTF-8')))
            db.add_molecule(molName, f)
            

            message = "sdf file uploaded to database";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        elif self.path == '/get-atoms.html':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_post_data = urllib.parse.parse_qs(post_data)
            name = parsed_post_data['molName'][0]

            result = db.getAtoms(name)
            # Send the result back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(result[0][0]).encode())

        elif self.path == '/get-bonds.html':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_post_data = urllib.parse.parse_qs(post_data)
            name = parsed_post_data['molName'][0]

            result = db.getBonds(name)
            # Send the result back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(result[0][0]).encode())

        elif self.path == '/displayMol.html':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_post_data = urllib.parse.parse_qs(post_data)
            name = parsed_post_data['molName'][0]

            mol = db.load_mol(name)
            mol.sort()
            # Send the result back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(mol.svg().encode())

        elif self.path == '/RotateMol.html':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_post_data = urllib.parse.parse_qs(post_data)
            name = parsed_post_data['molName'][0]
            axis = parsed_post_data['axis'][0]
            temp = parsed_post_data['degrees'][0]

            if(temp == ""):
                degrees = 90
            else:
                degrees = (int)(temp)

            mol = db.load_mol(name)
            
            #rotate the molecule
            if(axis == 'x'):
                mx = molecule.mx_wrapper(degrees,0,0)
            elif(axis == 'y'):
                mx = molecule.mx_wrapper(0,degrees,0)
            else:
                mx = molecule.mx_wrapper(0,0,degrees)
            
            mol.xform(mx.xform_matrix)

            mol.sort()
            # Send the result back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(mol.svg().encode())

        elif self.path == '/create-element.html':
            # Parse the form data posted
            form_data = self.rfile.read(int(self.headers['Content-Length']))
            form_data = urllib.parse.parse_qs(form_data.decode('utf-8'))

            # Get the values of the form fields
            element_num = form_data.get('elementNum', [''])[0]
            element_code = form_data.get('elementCode', [''])[0]
            element_name = form_data.get('elementName', [''])[0]
            colour1 = form_data.get('colour1', [''])[0]
            colour2 = form_data.get('colour2', [''])[0]
            colour3 = form_data.get('colour3', [''])[0]
            radius = form_data.get('radius', [''])[0]
            print(radius)
            #default values
            if(colour1 == ""):
                colour1 = "1f005c"
            if(colour2 == ""):
                colour2 = "ffb56b"
            if(colour3 == ""):
                colour3 = "000000"
            if(radius == ""):
                radius = 35


            #add to database
            db['Elements'] = ( element_num, element_code, element_name, colour1, colour2, colour3, radius);
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()

            # Send the response
            message = "Element Uploaded to Database";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        elif self.path == '/clear-db.html':

            #reset the database
            db.reset()
            # Send the response
            message = "Database Reset";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        elif self.path == '/delete-element.html':

            #get the stuf
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_post_data = urllib.parse.parse_qs(post_data)
            name = parsed_post_data['elName'][0]

            #delete the element
            db.deleteElement(name)


            # Send the response
            message = "Element Deleted From Database";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

#load the tables from database
db = Database(reset=False) # or use default
MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()


def main():
    #create the website
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    httpd.serve_forever()
    
if __name__ == "__main__":
    main()