include <Knob.scad>

insideX = 170;
insideY = 100;
insideZ = 40;
t = 3;

module display(){
    translate([2.0, 6, -1]){
        color([0.3, 0.3, 0.3])
            cube([118, 70, 1]);
        translate([57,-6,0])
            cube([13, 6, 1]);
    }
    translate([0,0,-8]){
        color([0,0,1])
            cube([121, 78, 7]);
        translate([43, 78, -15])
            color([0,0l1])
                cube([18, 11, 15]);
    }
}

module displayBezel(h){
    translate([2.5+3, 6+3, 0])
        cube([110,66,h]);
}

module pillar(x, y, z, r){
    difference(){
        cube([x, y, z]);
        translate([x/2, y/2,-1])
            cylinder(z+2, r, r); 
    }
}

module box(){
    color([0.9,0.9,0.9]){
        difference(){
            cube([insideX+2*t, insideY+2*t, insideZ+t]);
            translate([t,t,t])
                cube([insideX, insideY, insideZ+0.1]);
        }
    }
    //displaySupports
    translate([33,10]){
        color([1,0,0]){
            pillar(15,15,25,1.5);
        }
    }
    translate([33,73]){
        color([1,0,0]){
            pillar(15,15,25,1.5);
        }
    }
    translate([160,90]){
        color([1,0,0]){
            pillar(15,15,25,1.5);
        }
    }
    translate([160,90]){
        color([1,0,0]){
            pillar(15,15,25,1.5);
        }
    }
    translate([160,3]){
        color([1,0,0]){
            pillar(15,6,25,1.5);
        }
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
    cylinder(t,21.5/2, 21.5/2);
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
    translate([171, 10, 2])
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
    translate([25, 53, 36+t])
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

module raspi(){
    //Base board
    
    translate([0,0,0]){
        color([0,1,0])
            cube([85, 56, 1]);
    }
    
    //usb 1
    translate([0,1.5, 1]){
        color([0.5,0.5,0.5])
            cube([10, 15, 16]);
    }
    
    //usb 2
    translate([0,19.5, 1]){
        color([0.5,0.5,0.5])
            cube([10, 15, 16]);
    }
    //ethernet
    translate([0,38, 1]){
        color([0.5,0.5,0.5])
            cube([10, 16, 14]);
    }
}


module raspiHoles(d){
    //usb 1
    translate([0-d,1.5, 1]){
        color([0.5,0.5,0.5])
            cube([10+d, 15, 16]);
    }
    
    //usb 2
    translate([0-d,19.5, 1]){
        color([0.5,0.5,0.5])
            cube([10+d, 15, 16]);
    }
    //ethernet
    translate([0-d,38, 1]){
        color([0.5,0.5,0.5])
            cube([10+d, 16, 14]);
    }
}


module raspiPlaced(holes){
    translate([171, 10, 2])
        rotate([0,180,0]){  
            translate([0,22,-27]){
                raspi();
                if(holes)
                    raspiHoles(30);
            }
        }
}


module boxWithHoles(){
    difference(){
        box();
        encoderAssemblyPlaced(true, 5);
        displayPlaced(true);
        raspiPlaced(true);
    }
}

module boxDisplayAssembly(){
    boxWithHoles();
    encoderAssemblyPlaced(false, 1);
    displayPlaced(false);
    raspiPlaced(false);
}


//display();

//raspiPlaced(true);

boxDisplayAssembly();
//raspiPlaced();
//encoderAssemblyPlaced(true, 40);
//boxWithHoles();



//box();

//display();
//displayBezel(4);
