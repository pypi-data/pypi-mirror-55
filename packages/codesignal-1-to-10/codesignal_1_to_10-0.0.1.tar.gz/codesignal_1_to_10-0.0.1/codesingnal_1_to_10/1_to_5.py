if __name__ == "__main__":
    def isLucky(n):
        m = str(n)
        s = 0
        t = 0

        for i in range(int(len(m) / 2)):
            s = s + int(m[i])
            t = t + int(m[i + int(len(m) / 2)])

        return s == t


    def sortByHeight(a):
        l = sorted([i for i in a if i > 0])
        for n, i in enumerate(a):
            if i == -1:
                l.insert(n, i)
        return l


    def reverseInParentheses(gf):
        while ')' in gf:
            A = gf.find(')')
            b = gf[:A].rfind('(')
            c = gf[b + 1:A][::-1]
            gf = gf[:b] + c + gf[A + 1:]
        return gf


    def alternatingSums(a):
        return [sum(a[::2]), sum(a[1::2])]
