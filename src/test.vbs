
Function Sum(x as Integer, y as Integer) as Integer
    Dim a as Integer
    a = x + y
     Print a
    Sum = a
End Function

Function Subtract(x as Integer, y as Integer) as Integer
    Dim d as Integer
    d = x - y
    Subtract = d
End Function

Sub Main()
    Dim a as Integer
    Dim b as Integer
    Dim w as Integer
    a = 5
    w = 2
    ' b = y - a
    c = Subtract(w, 1)
    ' Print b
    print c
    b = Sum(a, 1)
End Sub