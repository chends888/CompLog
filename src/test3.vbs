Sub main()
    Dim testebool as boolean
    Dim testeint as integer
    testebool = True
    testeint = 10

    if testebool then
        print testeint + 10
    end if

    while (testeint > 0) and testebool = True
        print testeint
        testeint = testeint - 1
    wend

    testeint = input
    print testeint

End Sub