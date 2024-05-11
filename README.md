# gcode-absolute-to-relative-converter

Converts the body of GCODE file from absolute coordinates to relative coordinates.

Processes everything between `; START OBJECT GCODE` and `; START OBJECT GCODE`.

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
