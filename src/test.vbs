Sub Main()
    dim x as boolean
    dim y as integer
    dim z as integer
    x = True
    y = 0
    z = 1
    if x then
        print z
    else
        print y
    end if
    if x then
        print x
    end if
    while y < 5
        print y
        y = y + z
    wend
End Sub