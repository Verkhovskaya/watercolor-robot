inner_diameter = 12;
outer_diameter = 16;
height = 6;

difference() {
    union() {
        cylinder(h=height, d=outer_diameter);
        translate([0,(-height/2),0]) cube([outer_diameter*0.5, height, height]);
    }
    cylinder(h=height, d=inner_diameter);
}