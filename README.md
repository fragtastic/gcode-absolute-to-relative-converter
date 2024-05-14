# gcode-absolute-to-relative-converter

Converts the body of GCODE file from absolute coordinates to relative coordinates.

Processes everything between `; START OBJECT GCODE` and `; START OBJECT GCODE`.

Z0 is based on the first Z position. So if the first layer is 0.2mm thick that'll be the relative Z0. Will probably change this and include figuring out the Z position from the start.

The object is always centered in the print bed. This finds 2 opposite "corners" and centers that rectangle on the bed.

Start code blocks must end with:
```gcode
G1 Xcenter Ycenter
; START OBJECT GCODE
```

End code blocks must end with:
```gcode
; END OBJECT GCODE
G90
```
