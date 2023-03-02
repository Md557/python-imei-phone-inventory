class ImeiValidator:
    """
    Borrowed and lightly-modified from https://www.geeksforgeeks.org/program-check-valid-imei-number/
    """
    @staticmethod
    def sumDig(n):
        a = 0
        while n > 0:
            a = a + n % 10
            n = int(n / 10)

        return a


    # Returns True if n is valid EMEI
    def isValidIMEI(self, n):

        # Converting the number into
        # String for finding length
        s = str(n)
        l = len(s)

        # If length is not 15 then IMEI is Invalid
        if l != 15:
            return False

        d = 0
        sum = 0
        for i in range(15, 0, -1):
            d = (int)(n % 10)
            if i % 2 == 0:
                # Doubling every alternate digit
                d = 2 * d

            # Finding sum of the digits
            sum = sum + self.sumDig(d)
            n = n / 10
        return (sum % 10 == 0)


    def validate_IMEI(self, imei):
        return self.isValidIMEI(int(imei))
