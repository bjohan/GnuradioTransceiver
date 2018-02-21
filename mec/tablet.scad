use <display.scad>
use <raspi.scad>
use <encoder.scad>
use <Knob.scad>
use <speaker.scad>


module knobEncoderAssembly(){
    encoderWithHoles();
    translate([0,0,42])
        knobAssembly();
    
}


display();
translate([108,85+62,-17])
    rotate([0,0,-90])
        raspi();

translate([130,30,-20])
    rotate([0,90,0])
        knobEncoderAssembly();


translate([30,0,-20])
    rotate([-90,0,0])
        speaker();
translate([165-60,0,-20])
    rotate([-90,0,0])
        speaker();


module roundedCube(size, r){
    minkowski(){
        cube(size);
        sphere(r);
    }
}


module mainEnclosure(mainDim, r, t){
    difference(){
        roundedCube(mainDim, r);
        //translate([t, t, t])
        roundedCube(mainDim, r-t);
    }
}

module mainEnclosureTopBody(){
    mainDim = [180, 150, 40];
    r = 10;
    t = 3;
    difference(){
        mainEnclosure(mainDim, r, t);
        cube([200, 200, 200]);
    }
}
translate([0,0,-38])
mainEnclosureTopBody();
