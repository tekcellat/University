def m(n):
    x2, y2 = 1, 0
    x, y = 0, 0
    s = [[None] * n for _ in range(n)]
    for i in range(1, n**2+1):
        s[x][y] = i
        nx, ny = x+x2, y+y2
        if 0 <= nx < n and 0 <= ny < n and not s[nx][ny]:
            x, y = nx, ny
        else:
            x2, y2 = -y2, x2
            x, y = x+x2, y+y2
    for x in list(zip(*s)):
        print(*x)
m(int(input('Введите количество элеметнов')))