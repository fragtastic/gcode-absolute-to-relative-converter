# gcode-absolute-to-relative-converter

Converts the body of GCODE file from absolute coordinates to relative coordinates.

Processes everything between `; START OBJECT GCODE` and `; START OBJECT GCODE`.

Z0 is based on the first Z position. So if the first layer is 0.2mm thick that'll be the relative Z0.

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
