// Copyright 2018 Bergmann's Lab UNIL <mattia.tomasoni@unil.ch> 
//
// This file is part of DREAM DMI Tool.
//
//    DREAM DMI Tool is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    DREAM DMI Tool is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//   along with DREAM DMI Tool. If not, see <https://www.gnu.org/licenses/>.
//
///////////////////////////////////////////////////////////////////////////////
//Mattia Tomasoni - UNIL, CBG
// 2017 DREAM challenge on Disease Module Identification
// https://www.synapse.org/modulechallenge
///////////////////////////////////////////////////////////////////////////////

#if !defined(CAST_INCLUDED)
#define CAST_INCLUDED	
	




bool cast_string_to_double (string &b, double &h) {		

// set h= the number written in b[]; 
// return false if there is an error
	
	
	h=0;
	
	
	if(b.size()==0)
		return false;
	
	int sign=1;
	
	
	 if (b[0]=='-') {
		
		b[0]='0';
		sign=-1;
	 
	 }
	
	
	
	int digits_before=0;
	for(int i=0; i<b.size(); i++)
		if(b[i]!='.')
			digits_before++;
		else
			break;
	
	
	int j=0;
	
	while (j!=digits_before) {
	
		int number=(int(b[j])-48);
		h+=number*pow(10, digits_before-j-1);
		
		
		if (number<0 || number>9)
			return false;
		
		j++;
	}
	
	
	j=digits_before+1;
	
	while (j<b.size()) {
		
		int number=(int(b[j])-48);
		h+=number*pow(10, digits_before-j);
		
		if (number<0 || number>9)
			return false;
		
		j++;
	}

		
	h=sign*h;
	
	
	return true;
	
}


int cast_int(double u) {

	int a=int(u);
	if (u - a > 0.5)
		a++;
	
	return a;
		
}


int cast_string_to_char(string &file_name, char *b) {

	for (int i=0; i<file_name.size(); i++)
		b[i]=file_name[i];
	b[file_name.size()]='\0';	

	return 0;

}

#endif
