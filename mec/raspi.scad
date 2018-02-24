
module raspi(){
    //Base board
    translate([0,0,0]){
        color([0,1,0]){
            difference(){
                cube([85, 56, 1]);
                    r=2.65/2;
                    translate([22.2+r,2.2+r,-1])
                        cylinder(5,r,r);
                    translate([22.2+r,51+r,-1])
                        cylinder(5,r,r);
                    translate([80+r,2.2+r,-1])
                        cylinder(5,r,r);
                    translate([80+r,51+r,-1])
                        cylinder(5,r,r);
            }
        }
    }
    
    //usb 1
    translate([0,1.5, 1]){
        color([0.5,0.5,0.5])
            cube([17, 15, 16]);
    }
    
    //usb 2
    translate([0,19.5, 1]){
        color([0.5,0.5,0.5])
            cube([17, 15, 16]);
    }
    //ethernet
    translate([0,38, 1]){
        color([0.5,0.5,0.5])
            cube([21, 16, 14]);
    }
    
    //micro usb
    translate([70, 50, 1]){
        color([0.5,0.5,0.5])
            cube([9, 8, 3]);
    }
    
    //headphone
    translate([28, 50, 1]){
        color([0,0,0])
            cube([7, 8, 7]);
    }
    
    //microsd
    translate([72, 21, -2]){
        color([0.5,0.5,0.5])
            cube([18, 14, 2]);
    }
}


module raspiHoles(d){
    //usb 1
    translate([0-d,1.0, 1]){
        color([0.5,0.5,0.5]){
            cube([10+d, 16, 16]);
            
        }
    }
    
    //usb 2
    translate([0-d,19.0, 1]){
        color([0.5,0.5,0.5])
            cube([10+d, 16, 16]);
    }
    //ethernet
    translate([0-d,38, 1]){
        color([0.5,0.5,0.5])
            cube([10+d, 16, 14]);
    }
    //micro usb
    translate([70-5, 50, 1-4]){
        color([0.5,0.5,0.5])
            cube([9+10, 8+d, 3+8]);
    }
    
    //headphone
    translate([28-2, 50, 1-4]){
        color([0,0,0])
            cube([7+4, 8+13, 7+8]);
    }
    
    //microsd
    translate([72, 21, -2]){
        color([0.5,0.5,0.5])
            cube([18+10, 14, 2]);
    }
    r=2.65/2;
    raspiScrewHoles(r, d);
}

module raspiScrewHoles(hr, d){
    r=2.65/2;
    translate([22.2+r,2.2+r,-1-d])
        cylinder(5+d,hr,hr);
    translate([22.2+r,51+r,-1-d])
        cylinder(5+d,hr,hr);
    translate([80+r,2.2+r,-1-d])
        cylinder(5+d,hr,hr);
    translate([80+r,51+r,-1-d])
        cylinder(5+d,hr,hr);
}

//raspi();
raspiHoles(50);
