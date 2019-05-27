cylinder_diameter = 8;
min_height = 3;
thickness = 2;
cylinder_length = 10;

difference() {
    cube([cylinder_diameter+2*thickness, cylinder_length, cylinder_diameter/2 + min_height]);
    translate([cylinder_diameter/2+thickness, 0, 0]) rotate([-90,0,0]) cylinder(h=cylinder_length, d=cylinder_diameter);
}