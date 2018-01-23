include <Knob.scad>
use <ElectronicModuleAssembly/modules/lm2596-dc-dc.scad>
use <ElectronicModuleAssembly/modules/dsn-dvm-368.scad>
insideX = 170;
insideY = 100;
insideZ = 40;
t = 3;

speakerOffset = 22;
speakerAngle = 20;

module dvmPlaced(){
    translate([15,-18,20])
        rotate([90+speakerAngle, 0, 0]){
            translate([72, -5, 0])
                dsnDvm368Module();
        }
}

module switchHolePlaced(){
    translate([0,-18,27])
        rotate([90+speakerAngle, 0, 0]){
            translate([72, -5, 0])
                cylinder(30, 5/2, 5/2);
                //dsnDvm368Module();
        }
}

module battery(){
    cube([145, 55, 17]);
}

module speaker(){
    translate([0,0,5]){
        cylinder(3, 20, 20);
        translate([0,0,3])
            cylinder(10, 37/2, 32/2);
        translate([0,0,13])
            cylinder(7,22/2, 22/2);
    }
}

module speakerHole(){
    speaker();
    translate([0,0,-5])
    cylinder(10, 18, 18);
    
}


module speakerSlot(){
    //hull(){
        minkowski(){
        speakerHole();
        cube([0.5, 100.5, 0.5]);    
        //translate([0,100, 0])
        //    speakerHole();
    }
}
//speakerWithHole();

module tube(l, ri, ro){
    difference(){
        cylinder(l, ro, ro);
        translate([0,0,-0.1])
        cylinder(l+0.2, ri, ri);
    }
}

module speakerGrill(d){
    translate([0,0,-d]){
        tube(d, 3,5);
        tube(d, 10,12);
        tube(d, 18,20);
        //translate([11, 0, 0])
        //    tube(d, 6, 8);
        translate([0, 11, 0])
            tube(d, 6, 8);
        //translate([-11, 0, 0])
        //    tube(d, 6, 8);
        translate([0, -11, 0])
            tube(d, 6, 8);
    }
}

module speakerGrillHoles(d){
    //speakerGrill(d+0.2);
    difference(){
        translate([0,0,-d])
            cylinder(d, 20, 20);
            translate([0,0,0.1])
                speakerGrill(d+0.2);
    }
}

module speakersPlaced(){
    translate([33, -speakerOffset, 19]){
        rotate([-90+speakerAngle, 0, 0])
            speaker();
    }
    translate([insideX+2*t-33, -speakerOffset, 19]){
        rotate([-90+speakerAngle, 0, 0])
            speaker();
    }
}

module speakersGrillHolesPlaced(d){
    translate([33, -speakerOffset, 19]){
        rotate([-90+speakerAngle, 0, 0])
            translate([0,0,1])
            speakerGrillHoles(d);
    }
    translate([insideX+2*t-33, -speakerOffset, 19]){
        rotate([-90+speakerAngle, 0, 0])
            translate([0,0,1])
            speakerGrillHoles(d);
    }
}

module speakerSlotsPlaced(){
    translate([33, -speakerOffset, 19]){
        rotate([-90+speakerAngle, 0, 0])
            speakerSlot();
    }
    translate([insideX+2*t-33, -speakerOffset, 19]){
        rotate([-90+speakerAngle, 0, 0])
            speakerSlot();
    }
}


//speaker();
//speakerGrillHoles(30);

module display(){
    translate([2.0, 5, -1]){
        color([0.3, 0.3, 0.3])
            cube([118, 72, 1]);
        translate([57,-6,0])
            cube([13, 6, 1]);
    }
    translate([0,0,-8]){
        color([0,0,1])
            cube([121, 78, 7]);
        translate([43, 78, -15])
            color([0,0, 1])
                cube([18, 11, 15]);
    }
}

module displayBezel(h){
    translate([2.5+3, 6+3, 0])
        cube([110,66,h]);
}

module pillar(x, y, z, r, holeOnly){
    if(holeOnly){
        translate([x/2, y/2,-1])
        cylinder(z+2, r, r); 
    } else {
        difference(){
            cube([x, y, z]);
            translate([x/2, y/2,-1])
                cylinder(z+2, r, r); 
        }
    }
}

module supportPillars(holeOnly){
    //displaySupports
    h = 31;
    ho=holeOnly;
    translate([33,10]){
        color([1,0,0]){
            pillar(15,15,h,1.5, ho);
        }
    }
    translate([33,73]){
        color([1,0,0]){
            pillar(15,15,h,1.5, ho);
        }
    }
    translate([140,90]){
        color([1,0,0]){
            pillar(15,15,h,1.5, ho);
        }
    }
    translate([140,3]){
        color([1,0,0]){
            pillar(15,6,h,1.5, ho);
        }
    }
}

module cornerPillars(holeOnly){
    h2=43;
    ho=holeOnly;
    //Corner pillars
    translate([t,t]){
        color([1,0,0]){
            pillar(15,15,h2,1.5, ho);
        }
    }
    translate([t,insideY+t-15]){
        color([1,0,0]){
            pillar(15,15,h2,1.5, ho);
        }
    }
    translate([160,90]){
        color([1,0,0]){
            pillar(15,15,h2,1.5, ho);
        }
    }
    translate([160,3]){
        color([1,0,0]){
            pillar(15,6,h2,1.5, ho);
        }
    }
}

module slope(x, y, z){
    difference(){
    cube([x, y, z]);
    
    
    rotate([-atan2(y,z),0,0])
        translate([-0.1,-2*y,0])
            cube([x+0.2, 2*y, 2*z]);
    }
}
module loudspeakerBoxPartBody(){
    px = insideX+2*t;
        pz = insideZ+t;
        py = sin(speakerAngle)*pz;
        //rotate([0,90,0])
        difference(){
            translate([0,-speakerOffset-8-3,pz])
                mirror([0,0,1]){
                    slope(px, py, pz);
                    translate([0,py,0])
                    cube([px, t, pz]);
                }
            translate([t,-speakerOffset-8-3+t,pz+0.1])
                mirror([0,0,1])
                    slope(px-2*t, py+0.1, pz+0.1);
        }
        translate([0,-speakerOffset+3.7,0]){
            difference(){
                cube([px, speakerOffset, pz]);
                translate([t,-00.1,t]){
                    cube([px-2*t, speakerOffset+0.2, pz]);
                }
        }
    }
        //rotate([0,90,0])
        //    prism(px, py, pz);
}

module loudspeakerBoxPart(){
    difference(){
        loudspeakerBoxPartBody();
        speakersGrillHolesPlaced(5);
    }
}

module box(){
    color([0.9,0.9,0.9]){
        difference(){
            cube([insideX+2*t, insideY+2*t, insideZ+t]);
            translate([t,0*t-0.1,t])
                cube([insideX, t+insideY+0.1, insideZ+0.1]);
        }
        loudspeakerBoxPart();        
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
                    translate([0,0,37])
                    encoderShaftHole(t+1);
                    translate([0,0,37])
                        encoderScrewHoles(4/2, t+1);
                }
            }
        }
        
    }
}

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
    translate([22.2+r,2.2+r,-1-d])
        cylinder(5+d,r,r);
    translate([22.2+r,51+r,-1-d])
        cylinder(5+d,r,r);
    translate([80+r,2.2+r,-1-d])
        cylinder(5+d,r,r);
    translate([80+r,51+r,-1-d])
        cylinder(5+d,r,r);
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

module boxWithPillars(){
    box();
    supportPillars(false);
    cornerPillars(false);
}

module boxWithHoles(){
    difference(){
        //box();
        boxWithPillars();
        encoderAssemblyPlaced(true, 5);
        displayPlaced(true);
        raspiPlaced(true);
        dvmPlaced();
        switchHolePlaced();
    }
}

module boxDisplayAssembly(){
    boxWithHoles();
    encoderAssemblyPlaced(false, 1);
    displayPlaced(false);
    raspiPlaced(false);
}

module lid(){
    e = 33;
    color([1,0.9,1]){
        difference(){
            translate([0, -e, 0]){
                difference(){
                    cube([insideX+2*t, insideY+2*t+e, 20 + 0*t*2]);
                    translate([15, 15, -9])
                    cube([insideX+2*t-30, insideY+2*t+e-30, 26]);
                }
            }
            translate([0,0,-1])
                cornerPillars(true);
                //cube([insideX, insideY, insideZ+0.1]);
        }
    }
    //translate([15,0,0])
    //battery();
}


module lidPlaced(){
    translate([0,0,43])
        lid();
}

module electronicsConsoleBody(){
    difference(){
        translate([19-16, 3.5-25, 31]){
            cube([153+16, 99+25, 3]);
            difference(){
                union(){
                    translate([10-5+3, 8, -25])
                        rotate([speakerAngle, 0, 0])
                            cube([45, 24, 30]);
                    
                    translate([10-5-3+insideX+2*t-60, 8, -25])
                        rotate([speakerAngle, 0, 0])
                            cube([45, 24, 30]);
                }
                
                translate([0,-1,3])
                    cube([200, 200, 15]);
            }
        }
        translate([25, 53, 36+t])
            rotate([0,180,0])
                minkowski(){
                    encoderBody();
                    translate([-1, -1, -1])
                        cube([2,2,2]);
                }
         minkowski(){
            cornerPillars();
            translate([-1, -1, -1])
                cube([2,2,2]);
         }
         translate([0,0,5])
            supportPillars(true);
    }
    
}

module electronicsConsole(){
    difference(){
        electronicsConsoleBody();
        raspiPlaced(true);
        speakerSlotsPlaced();
    }
}

//raspi();
//raspiHoles(50);
//electronicsConsole();
//raspiPlaced(false);
//displayPlaced();

//raspiPlaced(true);

//boxDisplayAssembly();
//speakersPlaced();
//translate([-50, -50, 43])
//cube([100, 100, 1]);

//raspiPlaced();
//encoderAssemblyPlaced(true, 40);
//boxWithHoles();
//lidPlaced();
lid();

//box();
//dvmPlaced();
//switchHolePlaced();
/*translate([0,-15,20])
rotate([90+speakerAngle, 0, 0]){
    translate([72, -5, 0])
    dsnDvm368Module();
}*/
//display();
//displayBezel(4);
