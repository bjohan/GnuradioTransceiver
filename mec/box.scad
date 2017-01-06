include <Knob.scad>

insideX = 170;
insideY = 100;
insideZ = 40;
t = 3;

module display(){
    translate([2.5, 6, -1]){
        cube([117, 70, 1]);
        translate([57,-6,0])
            cube([13, 6, 1]);
    }
    translate([0,0,-8]){
        cube([121, 78, 7]);
        translate([43, 78, -15])
            cube([18, 11, 15]);
    }
}

module displayBezel(h){
    translate([2.5+3, 6+3, 0])
        cube([110,66,h]);
}

module box(){
    difference(){
        cube([insideX+2*t, insideY+2*t, insideZ+t]);
        translate([t,t,t])
            cube([insideX, insideY, insideZ+0.1]);
    }
}

module encoderScrewHoles(r,h){
    for(i=[0:2]){
        rotate([0,0,i*120])
            translate([36/2-4, 0,0])
                cylinder(h, r, r);
    }
}

module encoderShaftHole(t){
    cylinder(t,20/2, 20/2);
}

module encoderBody(){
    cylinder(36, 37/2, 37/2);
    translate([0,0,36])
        cylinder(5,20/2, 20/2);
    translate([0,0,36+5])
        cylinder(12,6/2, 6/2);
    
}

module encoderWithHoles(){
    difference(){
        encoderBody();
        translate([0,0,36-5])
            encoderScrewHoles(3/2, 6);
    }
}
module displayPlaced(drawBezel){
    translate([130, 10, 2])
    rotate([0,180,0]){
        display();
        if(drawBezel)
            displayBezel(5);
    }
}

module encoderAssembly(){
    encoderWithHoles();
    translate([0,0,42]){
        knobAssembly();
    }
}

module encoderAssemblyPlaced(holes, t){
    translate([153, 53, 36+t])
    rotate([0,180,0]){
        encoderAssembly();
        if(holes){
            minkowski(){
                sphere(0.25);
                union(){
                    translate([0,0,-0.5])
                    encoderShaftHole(t+1);
                    translate([0,0,37])
                        encoderScrewHoles(3/2, t+1);
                }
            }
        }
        
    }
}

module boxWithHoles(){
    difference(){
        box();
        encoderAssemblyPlaced(true, 5);
        displayPlaced(true);
    }
}

module boxDisplayAssembly(){
    boxWithHoles();
    encoderAssemblyPlaced(false, 1);
    displayPlaced(false);
}

boxDisplayAssembly();

//encoderAssemblyPlaced(true, 40);
//boxWithHoles();



//box();

//display();
//displayBezel(4);
