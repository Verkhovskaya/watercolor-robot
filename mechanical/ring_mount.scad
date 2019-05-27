// Slip ring
small_cylinder = 8.4;
length_small = 5;
big_cylinder = 10;
length_big = 3;
min_thickness = 1;

/*
// motor
small_cylinder = 5.2;
length_small = 5;
big_cylinder = 7;
length_big = 3;
min_thickness = 1;*/

difference() {
    cylinder(h = length_big+length_small, d=big_cylinder+2*min_thickness);
    union() {
      cylinder(h=length_small, d=big_cylinder);
      translate([0,0,length_big]) cylinder(h = length_small, d=small_cylinder);
    }
}