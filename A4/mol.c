// Dimiri Papadedes
// 113822
#define _USE_MATH_DEFINES
#include "mol.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// function to set the position of an atom
void atomset(atom *atom, char element[3], double *x, double *y, double *z) {
  atom->x = *x;
  atom->y = *y;
  atom->z = *z;
  strcpy(atom->element, element);
}

// function to get the postition of an atom
void atomget(atom *atom, char element[3], double *x, double *y, double *z) {
  *x = atom->x;
  *y = atom->y;
  *z = atom->z;
  strcpy(element, atom->element);
}

// function to set the atoms of a bond
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
  bond->a1 = *a1;
  bond->a2 = *a2;
  bond->epairs = *epairs;
  bond->atoms = *atoms;

  //call function
  compute_coords(bond);
}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
  *a1 = bond->a1;
  *a2 = bond->a2;
  *epairs = bond->epairs;
  *atoms = bond->atoms;
}

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
  // create a new struct to return at the end of the function
  struct molecule *newMol;
  newMol = malloc(sizeof(molecule));
  //error check
  if(newMol == NULL){
    return NULL;
  }

  // Tell the new molecule how many bonds and atoms it can hold at max
  newMol->atom_max = atom_max;
  newMol->bond_max = bond_max;

  // set atom_no and bond_no to 0 as a default
  newMol->atom_no = 0;
  newMol->bond_no = 0;

  // allocate memory for the atoms array by multiplying the size of an atom by
  // the length of the array
  newMol->atoms = malloc(sizeof(struct atom) * atom_max);
  //error check
  if(newMol->atoms == NULL){
    return NULL;
  }

  // allocate memory for the atoms_ptrs array by multiplying the size of an atom pointer by the length of the array
  newMol->atom_ptrs = malloc(sizeof(struct atom *) * atom_max); 
  //error check
  if(newMol->atom_ptrs == NULL){
    return NULL;
  }

  // allocate memory for the bonds array by multiplying the size of an bond by the length of the array
  newMol->bonds = malloc(sizeof(struct bond) * bond_max);
  //error check
  if(newMol->bonds == NULL){
    return NULL;
  }

  // allocate memory for the bonds_ptrs array by multiplying the size of an bond
  // pointer by the length of the array
  newMol->bond_ptrs = malloc(sizeof(struct bonds *) * bond_max);
  //error check
  if(newMol->bond_ptrs == NULL){
    return NULL;
  }

  // return the struct
  return newMol;
}

molecule *molcopy(molecule *src) {
  // create a new struct to return at the end of the function
  struct molecule *newMol;

  // malloc the new struct using molmalloc
  newMol = molmalloc(src->atom_max, src->bond_max);

  //appened all the atoms to the new array 

  for(int i = 0;i < src->atom_no; i++){
    molappend_atom(newMol, &src->atoms[i]);
  }

  //appened all the bonds to the new array 
  for(int i = 0;i < src->bond_no; i++){
    molappend_bond(newMol, &src->bonds[i]);
  }
  // return the struct
  return newMol;
}

void molfree(molecule *ptr) {
  // free the arrays first
  free(ptr->atoms);
  free(ptr->atom_ptrs);
  free(ptr->bonds);
  free(ptr->bond_ptrs);

  // then we free the struct itself
  free(ptr);
}

//function to add a bond to the end of the atoms and atom_ptrs array
void molappend_atom(molecule *molecule, atom *atom) {

  // check if we are going to need to realloc for more room in the function by
  // seeing if the atom_no is less than the max
  if (molecule->atom_no < molecule->atom_max) {
    // append the sent through atom to the end of the atoms array by using the current number of atoms

    molecule->atoms[(molecule->atom_no)] = *atom;
    // put the new addition to the atoms array and add it to the ptr array
    molecule->atom_ptrs[(molecule->atom_no) ] = &molecule->atoms[(molecule->atom_no)];
    // increment the number of used spaces in the array
    molecule->atom_no++;
  }else{
    //add the other case here

    //check if the number of atoms is = to 0 if so change to 1
    if(molecule->atom_no == 0){
      
      //set the number of atoms to 1
      molecule->atom_max = 1;

      //realloc the atoms
      molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
      //error check
      if(molecule->atoms == NULL){
        exit(0);
      }
      
      //realloc the atoms pointers
      molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max);
      //error check
      if(molecule->atom_ptrs == NULL){
        exit(0);
      }
      
      //fix the pointers
      for(int i = 0; i < molecule->atom_no ;i++){
        molecule->atom_ptrs[i] = &molecule->atoms[i];      
      }
      
      
      // append the sent through atom to the end of the atoms array by using the current number of atoms
      molecule->atoms[(molecule->atom_no)] = *atom;
      // put the new addition to the atoms array and add it to the ptr array
      molecule->atom_ptrs[(molecule->atom_no) ] = &molecule->atoms[(molecule->atom_no)];
      // increment the number of used spaces in the array
      molecule->atom_no++;
      
    }else{

      //double the number the numbers 
      molecule->atom_max = molecule->atom_max * 2;

      //realloc the atoms
      molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
      //error check
      if(molecule->atoms == NULL){
        exit(0);
      }
      //realloc the atoms pointers
      molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max);
      //error check
      if(molecule->atom_ptrs == NULL){
        exit(0);
      }
      
      //fix the pointers
      for(int i = 0; i < molecule->atom_no ;i++){
        molecule->atom_ptrs[i] = &molecule->atoms[i];      
      }
      
      
      // append the sent through atom to the end of the atoms array by using the current number of atoms
      molecule->atoms[(molecule->atom_no)] = *atom;
      // put the new addition to the atoms array and add it to the ptr array
      molecule->atom_ptrs[(molecule->atom_no) ] = &molecule->atoms[(molecule->atom_no)];
      // increment the number of used spaces in the array
      molecule->atom_no++;
      
    }
  } 
}

//function to add a bond to the end of the bonds and bond_ptrs array
void molappend_bond( molecule *molecule, bond *bond ){

  // check if we are going to need to realloc for more room in the function by
  // seeing if the bond_no is less than the max
  if (molecule->bond_no < molecule->bond_max) {
    
    // append the sent through bond to the end of the bonds array by using the current number of bonds
    molecule->bonds[(molecule->bond_no)] = *bond;
    
    // put the new addition to the bonds array and add it to the ptr array
    molecule->bond_ptrs[(molecule->bond_no) ] = &molecule->bonds[(molecule->bond_no)];

    // increment the number of used spaces in the array
    molecule->bond_no++;
    

    
  }else{
    //add the other case here
    //check if the number of bonds is = to 0 if so change to 1
    if(molecule->bond_no == 0){
      //set the number of bonds to 1
      molecule->bond_max = 1;
      

       //realloc the bonds
      molecule->bonds = realloc(molecule->bonds, sizeof(struct bond ) * molecule->bond_max);
      //error check
      if(molecule->bonds == NULL){
        exit(0);
      }
      //realloc the bonds pointers
      molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max);
      //error check
      if(molecule->bond_ptrs == NULL){
        exit(0);
      }

      //printf("\n%s -- %s\n",molecule->bonds[1].a1->element,molecule->bonds[1].a2->element);
      
      //fix the pointers
      for(int i = 0; i < molecule->bond_no ;i++){
        molecule->bond_ptrs[i] = &molecule->bonds[i];      
      }

       // append the sent through bond to the end of the bonds array by using the current number of bonds
      molecule->bonds[(molecule->bond_no)] = *bond;
    
      // put the new addition to the bonds array and add it to the ptr array
      molecule->bond_ptrs[(molecule->bond_no) ] = &molecule->bonds[(molecule->bond_no)];

      // increment the number of used spaces in the array
      molecule->bond_no++;
    }else{

      //double the number the numbers 
      molecule->bond_max = molecule->bond_max * 2;
      
      //realloc the bonds
      molecule->bonds = realloc(molecule->bonds, sizeof(struct bond ) * molecule->bond_max);
      //error check
      if(molecule->bonds == NULL){
        exit(0);
      }
      //realloc the bonds pointers
      molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max);
      //error check
      if(molecule->bond_ptrs == NULL){
        exit(0);
      }

      //printf("\n%s -- %s\n",molecule->bonds[1].a1->element,molecule->bonds[1].a2->element);
      
      //fix the pointers
      for(int i = 0; i < molecule->bond_no;i++){
        molecule->bond_ptrs[i] = &molecule->bonds[i];      
      }

       // append the sent through bond to the end of the bonds array by using the current number of bonds
      molecule->bonds[(molecule->bond_no)] = *bond;
    
      // put the new addition to the bonds array and add it to the ptr array
      molecule->bond_ptrs[(molecule->bond_no) ] = &molecule->bonds[(molecule->bond_no)];

      // increment the number of used spaces in the array
      molecule->bond_no++; 
    } 
  }  
}

void molsort(molecule * molecule){
  //sort the stuff lol
  qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), sortAtoms);
  qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), bond_comp);
}

int sortAtoms(const void * x_void, const void * y_void) { 
  //cast the values to an atom pointer then derefrence so we can get the actual value
  atom *x = *(atom **)x_void;
  atom *y = *(atom **)y_void;
  
  return x->z - y->z;  
}

int bond_comp(const void * x_void, const void * y_void) {  
  //cast the values to an bond pointer then derefrence so we can get the actual value
  bond *x = *(bond **)x_void;
  bond *y = *(bond **)y_void;

  return x->z - y->z;
  //return ((x->a1->z + x->a2->z) / 2) - ((y->a1->z + y->a2->z) / 2);
}

void xrotation( xform_matrix xform_matrix, unsigned short deg ){

  //switch to radians
  double tempDeg =  deg * (3.14159265358979323846 / 180);

  
  xform_matrix[0][0] = 1;
  xform_matrix[0][1] = 0;
  xform_matrix[0][2] = 0;

  xform_matrix[1][0] = 0;
  xform_matrix[2][0] = 0;
  xform_matrix[1][1] = cos(tempDeg);

  xform_matrix[1][2] = (-1) * sin(tempDeg);
  xform_matrix[2][1] = sin(tempDeg);
  xform_matrix[2][2] = cos(tempDeg);

  
}

void yrotation( xform_matrix xform_matrix, unsigned short deg ){
  //switch to radians
  double tempDeg =  deg * (3.14159265358979323846 / 180);
  
  xform_matrix[0][0] = cos(tempDeg);
  xform_matrix[0][1] = 0;
  xform_matrix[0][2] = sin(tempDeg);

  xform_matrix[1][0] = 0;
  xform_matrix[2][0] = (-1) * sin(tempDeg);
  xform_matrix[1][1] = 1;

  xform_matrix[1][2] = 0;
  xform_matrix[2][1] = 0;
  xform_matrix[2][2] = cos(tempDeg);
}

void zrotation( xform_matrix xform_matrix, unsigned short deg ){

  //switch to radians
  double tempDeg = deg * (3.14159265358979323846 / 180);
  
  xform_matrix[0][0] = cos(tempDeg);
  xform_matrix[0][1] = (-1) * sin(tempDeg);
  xform_matrix[0][2] = 0;

  xform_matrix[1][0] = sin(tempDeg);
  xform_matrix[2][0] = 0;
  xform_matrix[1][1] = cos(tempDeg);

  xform_matrix[1][2] = 0;
  xform_matrix[2][1] = 0;
  xform_matrix[2][2] = 1;
  
}

void mol_xform( molecule *molecule, xform_matrix matrix ){
  double x,y,z;
  //loop through all the atoms in the molecule
  for(int i = 0; i < molecule->atom_no; i++){
    //reset variables 
    x = 0;
    y = 0;
    z = 0;

    //calculator for a matrix
    //for x values
    x = molecule->atoms[i].x * matrix[0][0];  
    x += molecule->atoms[i].y * matrix[0][1];
    x += molecule->atoms[i].z * matrix[0][2];

    //for y values
    y = molecule->atoms[i].x * matrix[1][0];  
    y += molecule->atoms[i].y * matrix[1][1];
    y += molecule->atoms[i].z * matrix[1][2];

    //for z values 
    z = molecule->atoms[i].x * matrix[2][0];  
    z += molecule->atoms[i].y * matrix[2][1];
    z += molecule->atoms[i].z * matrix[2][2];

    //set the new values that were just calculated 
    molecule->atoms[i].x = x;
    molecule->atoms[i].y = y;
    molecule->atoms[i].z = z;
  }

  for(int i = 0; i < molecule->bond_no; i++){
    //calculate the cords of the bonds
    compute_coords(&(molecule->bonds[i]));
  }
  
}

void compute_coords( bond *bond ){

  //get the x and y from the first atom
  bond->x1 = bond->atoms[bond->a1].x;
  bond->y1 = bond->atoms[bond->a1].y;
  //get the x and y from the second atom
  bond->x2 = bond->atoms[bond->a2].x;
  bond->y2 = bond->atoms[bond->a2].y;

  //set the z value of the bond
  bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;

  //calculate the distance between the two points 
  //printf("x values:     %f\n%f\n",bond->x1,bond->x2);

  //find the distance 
  bond->len = sqrt((pow(bond->x2 - bond->x1,2) + pow(bond->y2 - bond->y1,2)));
  
  bond->dx = (bond->x2 - bond->x1) / bond->len;
  bond->dy = (bond->y2 - bond->y1) / bond->len;
}

