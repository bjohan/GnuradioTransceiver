module pcbHoles(r, l){
    hr = 3.24;
    dx = 153.8+hr;
    dy = 111.8+hr;

    ox = 2.52+hr/2;
    oy = 3 +hr/2;
    translate([ox, oy, 0]){
        cylinder(l, r, r);
        translate([dx, dy, 0])
            cylinder(l, r, r);
        translate([0, dy, 0])
            cylinder(l, r, r);
        translate([dx, 0, 0])
            cylinder(l, r, r);
    }
}

module pcbBoard(){
    mx = 165;
    my = 107;
    z = 1.7;
    tx = 8;
    ty = 124;
    tl = (ty-my)/2;
    translate([0, tl, 0]){
        cube([mx, my, z]);
        translate([0, -tl, 0])
            cube([tx, ty, z]);
        translate([mx-tx, -tl, 0])
            cube([tx, ty, z]);
    }
}

module toPcbEdge(){
    translate([0,(124-107)/2,0]){
        children();
    }
}
module pcb(){
    color([0,0,1])
    difference(){
        pcbBoard();
        translate([0,0,-1])
            pcbHoles(3.24/2, 5);
    }
}

module toPcbTop(){
    translate([0,0,1.7])
        children();
}

module placeTftBezel(){
    translate([0,8,0])
        children();
}
module tftBezel(){
    color([0.5, 0.5, 0.5])
        cube([165,97, 5]);
}

module tftDisplayArea(t){
    translate([1.5,6.5, 0])
        cube([157,89,t]);
}

module tftGlass(){
    color([0.5, 0.5, 1], 0.5)
    cube([165, 100, 1.4]);
}

module flatFlexVolume(){
    translate([135, -8, 0])
        cube([30, 8, 6.4]);
}

module tft(){
    difference(){
        tftBezel();
        translate([0,0,2])
            tftDisplayArea(10);
    }
    color([0.1, 0.1, 0.1])
        tftDisplayArea(5);
    translate([0,-3,5])
        tftGlass();

    flatFlexVolume();
}





module display(){
    pcb();
    toPcbTop()
        toPcbEdge()
            placeTftBezel()
                tft();
}


display();
