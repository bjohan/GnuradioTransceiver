use <display.scad>
use <raspi.scad>
use <encoder.scad>
use <Knob.scad>
use <speaker.scad>

bix = 180;
biy = 150;
biz = 44;
or = 10;
wt = 3;

module placeKnobOnEncoder(){
    translate([0,0,42])
        children();
}

module knobEncoderAssembly(){
    encoderWithHoles();
        placeKnobOnEncoder()
            knobAssembly();
    
}


module placeKnobEncoderAssembly(){
translate([bix/2-8,40+10,-30+5])
    rotate([0,90-10,-90])
        children();
}

module placeDisplay(){
    translate([0,0,0.5])
        children();
}


module placeRaspi(){
    placeDisplay()
        translate([15+0*108,0*85+62+45,-17])
            rotate([0,0,-90])
                children();
}
module placeSpeakerA(){
    translate([30,-or+wt,-20])
        rotate([-90,0,0])
        children();
}

module placeSpeakerB(){
    translate([165-60+30,-or+wt,-20])
        rotate([-90,0,0])
            children();
}

module roundedCube(size, r){
    minkowski(){
        cube(size);
        sphere(r);
    }
}


module mainEnclosure(mainDim, r, t){
        translate([0,0,-biz+2]){
       difference(){
            roundedCube(mainDim, r);
            //translate([t, t, t])
            roundedCube(mainDim, r-t);
        }
    }
}

module mainEnclosureWithHoles(mainDim, r, t){
    difference(){
        mainEnclosure(mainDim, r, t);
        placeSpeakerA()
            speakerHole();
        placeSpeakerB()
            speakerHole();
        placeKnobEncoderAssembly()
            knobOpening();
        
    }
    placeSpeakerA()
        speakerGrill(wt);
    placeSpeakerB()
        speakerGrill(wt);

}


module mainEnclosureBody(top){
    mainDim = [bix, biy, biz];
    r = or;
    t = wt;
    color([0,1,0],0.5)

        if(top){
            intersection(){
                mainEnclosureWithHoles(mainDim, r, t);
                translate([-20, -20, 0])
                    translate([0,0,-biz+2])
                        cube([300, 300, 300]);
            }
        } else {
            difference(){
                mainEnclosureWithHoles(mainDim, r, t);
                translate([-20, -20, 0])
                translate([0,0,-biz+2])
                    cube([300, 300, 300]);
            }
        }
    
}

module enclosureTop(){
    difference(){
        mainEnclosureBody(true);
        placeDisplay()
        toPcbTop()
            toPcbEdge()
                placeTftBezel()
                tftDisplayArea(100);
    }
}

module enclosureBottomUntrimmed(){
    mainEnclosureBody(false);
    placeSpeakerA()
        speakerBlock();
    difference(){
        union(){
            placeSpeakerB()
                speakerBlock();
            placeDisplay()
                displayPosts();
        }
        placeKnobEncoderAssembly()
        minkowski(){
            encoderWithHoles();
            sphere(7);
        }
        placeSpeakerA()
            speakerSlot();
        placeRaspi(){
            minkowski(){
                raspi();
                sphere(3);
            }
        }
    }

   placeRaspi()
        raspiPosts();
    
   placeKnobEncoderAssembly()
        encoderBrace();

}


module enclosureBottom(){
    mainDim = [bix, biy, biz];
    intersection(){
        enclosureBottomUntrimmed();
        translate([0,0,-biz+2])
            roundedCube(mainDim, or);
    }
}
module assembledComponents(){
    placeDisplay()
        display();
    //enclosureBottom();

    placeRaspi()
        raspi();

    placeKnobEncoderAssembly()
        knobEncoderAssembly();
    placeSpeakerA()
        speaker();

    placeSpeakerB()
        speaker();
    
}

module speakerBlock(){
    lx = 50;
    ly = 40;
    lz = 30;
    difference(){
    translate([-lx/2, -ly/2+10+10, 0])
        cube([lx, ly-10+10, lz]);
            rotate([0,0,180])
                speakerSlot();
    }
}

module encoderHoles(){
    encoderScrewHoles(3/2, 10);
    encoderShaftHole(10);
}

module encoderBraceBody(){
    w = 45;
    h = 20;
    l = 80;
    translate([-w/2+4,-w/2,-h+wt])
    difference(){
        cube([l, w, h]);
        translate([-1, wt, -wt])
            cube([l+2, w-2*wt, h]);
    }
}

module encoderBrace(){
    translate([0,0,36]){
        difference(){
            encoderBraceBody();
            translate([0, 0, -1])
                encoderHoles();
        }
    }
}

module displayPosts(){
    translate([0,0,-100])
    difference(){
        pcbHoles(8, 100);
        pcbHoles(3/2, 101);
            
    }
}

module raspiPosts(){
    difference(){
        translate([0,0,-4])
        raspiScrewHoles(8,60);
        raspiScrewHoles(2.5/2,60); 
    }
}

module knobOpening(){
    ox = 100;
    oy = 35;
    oz = 22+1;
    placeKnobOnEncoder(){
        cylinder(22+1, 63/2+1, 63/2+1);
        translate([-ox/2, -oy/2, 0])
            cube([ox, oy, oz]);
    }

}
enclosureBottom();
//translate([0,0,150])
//intersection(){
enclosureTop();
//translate([-15, -15, -70])
//cube([80, 30, 100]);}
//knobAssembly();
assembledComponents();
//encoderBrace();
//encoderHoles();
//knobEncoderAssembly();

