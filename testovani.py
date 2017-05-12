import rozvoj
import unittest
import math

class Zname_hodnoty(unittest.TestCase):
    #zname hodnoty pro funkci spocitej bazi beta; ve formátu funkce, znamenko, levy kraj
    zname_hodnoty=(('x**3-x**2-x-1',1,'0','1/3 + 4/(9*(math.sqrt(33)/9 + 19/27)**(1/3)) + (math.sqrt(33)/9 + 19/27)**(1/3)'),
                   ('x**2-x-1',1,'0','1/2 + math.sqrt(5)/2'))

    def test_spocitej_bazi_beta_pro_zname_hodnoty(self):
        '''spocitej_bazi_beta by mela dat spravne vysledky pro zname vstupy'''
        #fce=(('x**3-x**2-x-1','1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3)'),'x**2-x-1')
        for funkce,znamenko,levy_kraj,baze in self.zname_hodnoty:
            znamy_rozvoj = rozvoj.Soustava(funkce,znamenko,levy_kraj)
            vysledek = znamy_rozvoj.beta
            #self.assertAlmostEqual(baze,vysledek)
            self.assertEqual(baze,vysledek)

if __name__=='__main__':
    unittest.main()