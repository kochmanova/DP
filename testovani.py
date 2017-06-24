import rozvoj
import unittest
import sympy as sp


class ZnameHodnoty(unittest.TestCase):
    # zname hodnoty pro funkci spocitej bazi beta; ve formátu funkce, znamenko, levy kraj
    zname_hodnoty = (
        ('x**3-x**2-x-1', 1, '0', '1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3)'),
        ('x**2-x-1', 1, '0', '1/2 + sqrt(5)/2'))
    znamy_levy_kraj = (('-0.5', -0.5), ('0', 0))  # pro x**3-x**2-x-1, zápornou bázi
    zname_kraje = (('-x/(x+1)', [1, 0, 1], 1, [0, 1, 0, 1], 1), ('(x-3)/2', [1, 0, 0, 0, 1, 1], 6, [-1, 0, 1, 0], 4),
                   ('-1/x', [1, 0], 1, [-1, 0, 1, 1, 0, -1], 6))  # pro x**3-x**2-x-1, zápornou bázi

    def test_spocitej_bazi_beta_pro_zname_hodnoty(self):
        '''spocitej_bazi_beta by mela dat spravne vysledky pro zname vstupy'''
        for funkce, znamenko, levy_kraj, baze in self.zname_hodnoty:
            znamy_rozvoj = rozvoj.Soustava(funkce, znamenko, levy_kraj)
            vysledek = znamy_rozvoj.beta
            self.assertEqual(sp.sympify(baze), vysledek)

    def test_vycisleni_leveho_kraje(self):
        '''vycisleni leveho kraje by mela pro znamy levy kraj se rovnat'''
        fce = 'x**3-x**2-x-1'
        for levy_kraj, kraj in self.znamy_levy_kraj:
            znamy_rozvoj = rozvoj.Soustava(fce, 1, levy_kraj)
            vysledek = znamy_rozvoj.levy_kraj
            self.assertAlmostEqual(kraj, vysledek)

    def test_nalezeni_rozvoje(self):
        '''nalezeni rozvoje - měla by kontrolovat nalezeni rozvoje leveho i praveho kraje'''
        fce = 'x**3-x**2-x-1'
        for kraj, levy_rozvoj, leva_perioda, pravy_rozvoj, prava_perioda in self.zname_kraje:
            znamy_rozvoj = rozvoj.Soustava(fce, -1, kraj)
            self.assertEqual(levy_rozvoj, znamy_rozvoj.rozvoj_leveho_kraje.rozvoj_bodu)
            self.assertEqual(leva_perioda, znamy_rozvoj.rozvoj_leveho_kraje.perioda)
            self.assertEqual(pravy_rozvoj, znamy_rozvoj.rozvoj_praveho_kraje.rozvoj_bodu)
            self.assertEqual(prava_perioda, znamy_rozvoj.rozvoj_praveho_kraje.perioda)


class SpatneHodnoty(unittest.TestCase):
    def test_complexni_reseni(self):
        with self.assertRaises(ValueError):
            rozvoj.Soustava('x**2+1',1,'0')

    def test_baze_out(self):
        with self.assertRaises(ValueError):
            rozvoj.Soustava('x**2-1',1,'0')

    def test_baze_vice_korenu(self):
        with self.assertRaises(ValueError):
            rozvoj.Soustava('x**2+5x+6',1,'0')

    def test_levy_nuls(self):
        with self.assertRaises(ValueError):
            rozvoj.Soustava('x**2-x-1',-1,'-x')
            rozvoj.Soustava('x**2-x-1',-1,'0')

if __name__ == '__main__':
    unittest.main()
