
Function Sum(x as Integer, y as Integer) as Integer
    Dim a as Integer
    a = x + y
    Sum = a
End Function

Function Subtract(x as Integer) as Integer
    Dim d as Integer
    Dim c as Integer
    d = x-1
    ' if d > 1 then
        ' c = Subtract(d)
    ' end if
    Subtract = d
End Function

Sub Main()
    Dim a as Integer
    Dim c as Integer
    a = 5
    c = Subtract(a)
    Print c
    b = Sum(a, 1)
    print b
End Sub