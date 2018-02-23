use <display.scad>
use <raspi.scad>
use <encoder.scad>
use <Knob.scad>
use <speaker.scad>

bix = 180;
biy = 150;
biz = 40;
or = 10;
wt = 3;

module knobEncoderAssembly(){
    encoderWithHoles();
    translate([0,0,42])
        knobAssembly();
    
}


module placeKnobEncoderAssembly(){
translate([bix+or-wt-36-22,30,-20])
    rotate([0,90,0])
        children();
}

module placeDisplay(){
    children();
}


module placeRaspi(){
    placeDisplay()
        translate([108,85+62,-17])
            rotate([0,0,-90])
                children();
}
module placeSpeakerA(){
    translate([30,-or+wt,-20])
        rotate([-90,0,0])
        children();
}

module placeSpeakerB(){
    translate([165-60,-or+wt,-20])
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
        translate([0,0,-38]){
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
                    translate([0,0,-38])
                        cube([300, 300, 300]);
            }
        } else {
            difference(){
                mainEnclosureWithHoles(mainDim, r, t);
                translate([-20, -20, 0])
                translate([0,0,-38])
                    cube([300, 300, 300]);
            }
        }
    
}

module enclosureTop(){
    mainEnclosureBody(true);
}

module enclosureBottomUntrimmed(){
    mainEnclosureBody(false);
    placeSpeakerA()
        speakerBlock();
    difference(){
        placeSpeakerB()
            speakerBlock();
        placeKnobEncoderAssembly()
        minkowski(){
            encoderWithHoles();
            sphere(7);
        }
    }
    
   placeKnobEncoderAssembly()
        encoderBrace();

}


module enclosureBottom(){
    mainDim = [bix, biy, biz];
    intersection(){
        enclosureBottomUntrimmed();
        translate([0,0,-38])
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

enclosureBottom();
//enclosureTop();
//assembledComponents();
//encoderBrace();
//encoderHoles();
//knobEncoderAssembly();

