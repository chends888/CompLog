Sub Main()
    dim x as boolean
    dim w as boolean
    dim y as integer
    dim z as integer
    x = False
    y = 0
    z = 1
    w = True
    if x then
        print z
    else
        print x
    end if
    if w then
        print y
    end if
    while y < 5
        print y
        y = y + z
    wend
End Sub
