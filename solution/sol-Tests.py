import unittest
import numpy as np
import subprocess as sp
import glob, os, shutil
import sol


class createIdentityTestCase(unittest.TestCase):
    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_create(self):
        sol.createIdentity("alice")
        self.assertEqual(os.path.exists("storage-alice/identities"),True,"Storage not created")
    
    def test_replace(self):
        sol.createIdentity("alice")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")
        sol.createIdentity("alice")
        self.assertEqual(sol.listRelationship("alice"),"","Identity not reinitialized")

class setRelationshipTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
    
    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_oneSimpleRelationship(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")
        self.assertEqual(sol.listRelationship("alice"),"public teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY -> action:{foo}\n","Identity not reinitialized")

    def test_severalSimpleRelationship(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY","action:{foo}")
        self.assertEqual(sol.listRelationship("alice"),"public teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY -> action:{foo}\n","Identity not reinitialized")

    def test_overwriteSimpleRelationship(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{bar}")
        self.assertEqual(sol.listRelationship("alice"),"public teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY -> action:{bar}\n","Identity not reinitialized")

    def test_oneAdvancedRelationship(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo[bar.baz.baa].boo[up].bah[down].left[right.down]}")
        self.assertEqual(sol.listRelationship("alice"),"public teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY -> action:{foo[bar.baz.baa].boo[up].bah[down].left[right.down]}\n","Identity not reinitialized")

class certCreateTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_createEmptyCert(self):
        cert = sol.certCreate("alice")
        out = sp.run(["./../target/release/trinity-certificate-pp",cert],text=True,capture_output=True)
        hilfe = out.stdout.split('\n')
        ft = open('TestYaml/Test2.txt','r')
        certCor = ft.readlines()
        ft.close()
        del hilfe[18]
        del hilfe[16]
        del hilfe[11]
        del hilfe[6]
        certCor = [s.replace('\n','') for s in certCor]
        self.assertEqual(hilfe,certCor,"Certificate incorrect format")

    def test_createSimpleCert(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")
        cert = sol.certCreate("alice")
        out = sp.run(["./../target/release/trinity-certificate-pp",cert],text=True,capture_output=True)
        hilfe = out.stdout.split('\n')
        ft = open('TestYaml/Test3.txt','r')
        certCor = ft.readlines()
        ft.close()
        del hilfe[85]
        del hilfe[83]
        del hilfe[13]
        del hilfe[8]
        certCor = [s.replace('\n','') for s in certCor]
        self.assertEqual(hilfe,certCor,"Certificate incorrect format")

    def test_createAdvancedCert(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo[bar.baz.baa].boo[up].bah[down].left[right.down]}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY","action:{foo[bar.baz.baa].boo[up].bah[down].left[right.down]}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY","action:{foo[bar.baz.baa].boo[up].bah[down].left[right.down]}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY","action:{foo[bar.baz.baa].boo[up].bah[down].left[right.down]}")
        cert = sol.certCreate("alice")
        out = sp.run(["./../target/release/trinity-certificate-pp",cert],text=True,capture_output=True)
        hilfe = out.stdout.split('\n')
        ft = open('TestYaml/Test4.txt','r')
        certCor = ft.readlines()
        ft.close()
        del hilfe[591]
        del hilfe[589]
        del hilfe[16]
        del hilfe[11]
        del hilfe[6]
        del hilfe[5]
        del hilfe[4]
        del hilfe[3]
        certCor = [s.replace('\n','') for s in certCor]
        self.assertEqual(hilfe,certCor,"Certificate incorrect format")


class certPublishTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
        sol.certCreate("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_simplePublish(self):
        sol.certPublish("alice")
        tmp1 = os.path.exists("storage-alice/local_published/lock.mdb")
        tmp2 = os.path.exists("storage-alice/local_published/data.mdb")
        self.assertEqual([tmp1,tmp2],[True,True],"Certifcate not published")


class getPubKeyTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_SimplePubKey(self):
        k = sol.getPubKey("alice")
        self.assertEqual(len(k),47,"Incorrect public key length")

class reinitializeTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_simpleReinit(self):
        sol.reinitialize("alice")
        tmp = sol.listRelationship("alice")
        self.assertEqual(tmp,"","Not correctly initialized")

class delRelationshipTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_delOneRelation(self):
        sol.delRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY")
        tmp = sol.listRelationship("alice")
        self.assertEqual(tmp,"","Relationship not deleted")

    def test_delMidRelation(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY","action:{foo}")
        sol.delRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY")
        tmp = sol.listRelationship("alice")
        cor = "public teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY -> action:{foo}\n"
        self.assertEqual(tmp,cor,"Relationship not deleted")

    def test_delManyRelations(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY","action:{foo}")
        sol.delRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY")
        sol.delRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY")
        sol.delRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY")
        sol.delRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY")
        tmp = sol.listRelationship("alice")
        self.assertEqual(tmp,"","Relationship not deleted")

class listRelationshipTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_listNoRelations(self):
        tmp = sol.listRelationship("alice")
        self.assertEqual(tmp,"","Incorrect amount of relations listed")
    
    def test_listOneRelation(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY","action:{foo}")
        tmp = sol.listRelationship("alice")
        cor = "public teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY -> action:{foo}\n"
        self.assertEqual(tmp,cor,"Incorrect amount of relations listed")

    def test_listManyRelations(self):
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY","action:{foo}")
        sol.setRelationship("alice","teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY","action:{foo}")
        tmp = sol.listRelationship("alice")
        cor = "public teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT7jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT8jeWhvD8r9oGsY -> action:{foo}\npublic teItuDBSZ9YyDSD6vKSE-l7T5ikQT9jeWhvD8r9oGsY -> action:{foo}\n"
        self.assertEqual(tmp,cor,"Incorrect amount of relations listed")

class getCertStateInfoTestCase(unittest.TestCase):
    def test_emptyCert(self):
        tmp = sol.getCertStateInfo("ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU")
        cor = ["1636949716917,", "\"mGmnv3nUG3_2bukRRbpJfXwI3CJB2RB1jj2rtsDIEPw\","]
        self.assertEqual(tmp,cor,"Incorrect date and public key")

    def test_simpleCert(self):
        tmp = sol.getCertStateInfo("ZDI6aHRkODpTSEEyXzI1NmQzMjrAdWyumqqEA3XZNykf-yczS5-x_RNsZwxVifKSauDpHDc1OmQzOmtleTM1OgAAAeASCeNjeGCqVMOknL2lcNTKug3eGHUtBoEk2ykAf2yFNTp2YWx1ZWQxOnYxNTphY3Rpb246e2ZyaWVuZH1lZWVlNTpyb290c2xkMTA6cHVibGljX2tleTM1OgAAAX40xGULrwRPMp7iqbQgGtBWNugyiHWPXJVCjlJF0ESUOTpzaWduYXR1cmUxMzQ6pqpmsPITH0HYTjsHZI6Mir--RlefreWcDcCmB-Z9mdHjfcJBZbNkVS6wKZ6yfjS3ZdYOH2daWVKYia-dpLLfBGQxOmNpMTYzNjA2NTE2Mjk1NWUxOnJkODpTSEEyXzI1NjMyOsB1bK6aqoQDddk3KR_7JzNLn7H9E2xnDFWJ8pJq4OkcZWVlZWU")
        cor = ["1636065162955,", "\"fjTEZQuvBE8ynuKptCAa0FY26DKIdY9clUKOUkXQRJQ\","]
        self.assertEqual(tmp,cor,"Incorrect date and public key")

    def test_advancedCert(self):
        tmp = sol.getCertStateInfo("ZDI6aHRkODpTSEEyXzI1NmQzMjoV2ArDejKe7cOG1T4rUTXEBgborz-58AdXnMqEJmQpaTIwMDpkMzprZXkzMjq14i24MFJn1jINIPq8pIT6XtPmKRBPyN5aG8Pyv2gaxjQ6bGVmdDMyOnf4QY16La4QZ2zb1GyDX-oVkgU2Rb3qnTEkifJ03zoVNTpyaWdodDMyOigt7-ICa1ag064A3Rp_MDPu2zBM19_wlYYIfsvATyA4NTp2YWx1ZWQxOnY2MDphY3Rpb246e2Zvb1tiYXIuYmF6LmJhYV0uYm9vW3VwXS5iYWhbZG93bl0ubGVmdFtyaWdodC5kb3duXX1lZTMyOigt7-ICa1ag064A3Rp_MDPu2zBM19_wlYYIfsvATyA4MTE3OmQzOmtleTMyOrXiLbgwUmfWMg0g-rykhPpe0-YpEE_Y3lobw_K_aBrGNTp2YWx1ZWQxOnY2MDphY3Rpb246e2Zvb1tiYXIuYmF6LmJhYV0uYm9vW3VwXS5iYWhbZG93bl0ubGVmdFtyaWdodC5kb3duXX1lZTMyOnf4QY16La4QZ2zb1GyDX-oVkgU2Rb3qnTEkifJ03zoVMTU4OmQzOmtleTMyOrXiLbgwUmfWMg0g-rykhPpe0-YpEE-43lobw_K_aBrGNDpsZWZ0MzI6u0uhEyQ14PkpHg39pIzE0DYMUdj2wMJEmdTYcIomgas1OnZhbHVlZDE6djYwOmFjdGlvbjp7Zm9vW2Jhci5iYXouYmFhXS5ib29bdXBdLmJhaFtkb3duXS5sZWZ0W3JpZ2h0LmRvd25dfWVlMzI6u0uhEyQ14PkpHg39pIzE0DYMUdj2wMJEmdTYcIomgasxMTc6ZDM6a2V5MzI6teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY1OnZhbHVlZDE6djYwOmFjdGlvbjp7Zm9vW2Jhci5iYXouYmFhXS5ib29bdXBdLmJhaFtkb3duXS5sZWZ0W3JpZ2h0LmRvd25dfWVlZWU1OnJvb3RzbGQxMDpwdWJsaWNfa2V5MzU6AAABgUHFTgj4C9uf4T94Kc-1nJLcwPOa9SGQYvQ0xzNOwIg5OnNpZ25hdHVyZTEzNDo1iTCYCXYvyQkFfOPkuLxycLQQR2sWMa8V5CSHOHgX9qwpJoPj_CrgdFH3iZ08-n7hQcGpWU_iszP4iaRi31kMZDE6Y2kxNjM4MTgxNzgxODE4ZTE6cmQ4OlNIQTJfMjU2MzI6FdgKw3oynu3DhtU-K1E1xAYG6K8_ufAHV5zKhCZkKWllZWVlZQ")
        cor = ["1638181781818,", "\"gUHFTgj4C9uf4T94Kc-1nJLcwPOa9SGQYvQ0xzNOwIg\","]
        self.assertEqual(tmp,cor,"Incorrect date and public key")

class certImportTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")
    
    def test_emptyCert(self):
        sol.certImport("alice","ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU")
        self.assertEqual(os.path.exists("storage-alice/local_published/data.mdb"),True,"Certificate not imported")
    
    def test_simpleCert(self):
        sol.certImport("alice","ZDI6aHRkODpTSEEyXzI1NmQzMjrAdWyumqqEA3XZNykf-yczS5-x_RNsZwxVifKSauDpHDc1OmQzOmtleTM1OgAAAeASCeNjeGCqVMOknL2lcNTKug3eGHUtBoEk2ykAf2yFNTp2YWx1ZWQxOnYxNTphY3Rpb246e2ZyaWVuZH1lZWVlNTpyb290c2xkMTA6cHVibGljX2tleTM1OgAAAX40xGULrwRPMp7iqbQgGtBWNugyiHWPXJVCjlJF0ESUOTpzaWduYXR1cmUxMzQ6pqpmsPITH0HYTjsHZI6Mir--RlefreWcDcCmB-Z9mdHjfcJBZbNkVS6wKZ6yfjS3ZdYOH2daWVKYia-dpLLfBGQxOmNpMTYzNjA2NTE2Mjk1NWUxOnJkODpTSEEyXzI1NjMyOsB1bK6aqoQDddk3KR_7JzNLn7H9E2xnDFWJ8pJq4OkcZWVlZWU")
        self.assertEqual(os.path.exists("storage-alice/local_published/data.mdb"),True,"Certificate not imported")

    def test_advancedCert(self):
        sol.certImport("alice","ZDI6aHRkODpTSEEyXzI1NmQzMjoV2ArDejKe7cOG1T4rUTXEBgborz-58AdXnMqEJmQpaTIwMDpkMzprZXkzMjq14i24MFJn1jINIPq8pIT6XtPmKRBPyN5aG8Pyv2gaxjQ6bGVmdDMyOnf4QY16La4QZ2zb1GyDX-oVkgU2Rb3qnTEkifJ03zoVNTpyaWdodDMyOigt7-ICa1ag064A3Rp_MDPu2zBM19_wlYYIfsvATyA4NTp2YWx1ZWQxOnY2MDphY3Rpb246e2Zvb1tiYXIuYmF6LmJhYV0uYm9vW3VwXS5iYWhbZG93bl0ubGVmdFtyaWdodC5kb3duXX1lZTMyOigt7-ICa1ag064A3Rp_MDPu2zBM19_wlYYIfsvATyA4MTE3OmQzOmtleTMyOrXiLbgwUmfWMg0g-rykhPpe0-YpEE_Y3lobw_K_aBrGNTp2YWx1ZWQxOnY2MDphY3Rpb246e2Zvb1tiYXIuYmF6LmJhYV0uYm9vW3VwXS5iYWhbZG93bl0ubGVmdFtyaWdodC5kb3duXX1lZTMyOnf4QY16La4QZ2zb1GyDX-oVkgU2Rb3qnTEkifJ03zoVMTU4OmQzOmtleTMyOrXiLbgwUmfWMg0g-rykhPpe0-YpEE-43lobw_K_aBrGNDpsZWZ0MzI6u0uhEyQ14PkpHg39pIzE0DYMUdj2wMJEmdTYcIomgas1OnZhbHVlZDE6djYwOmFjdGlvbjp7Zm9vW2Jhci5iYXouYmFhXS5ib29bdXBdLmJhaFtkb3duXS5sZWZ0W3JpZ2h0LmRvd25dfWVlMzI6u0uhEyQ14PkpHg39pIzE0DYMUdj2wMJEmdTYcIomgasxMTc6ZDM6a2V5MzI6teItuDBSZ9YyDSD6vKSE-l7T5ikQT6jeWhvD8r9oGsY1OnZhbHVlZDE6djYwOmFjdGlvbjp7Zm9vW2Jhci5iYXouYmFhXS5ib29bdXBdLmJhaFtkb3duXS5sZWZ0W3JpZ2h0LmRvd25dfWVlZWU1OnJvb3RzbGQxMDpwdWJsaWNfa2V5MzU6AAABgUHFTgj4C9uf4T94Kc-1nJLcwPOa9SGQYvQ0xzNOwIg5OnNpZ25hdHVyZTEzNDo1iTCYCXYvyQkFfOPkuLxycLQQR2sWMa8V5CSHOHgX9qwpJoPj_CrgdFH3iZ08-n7hQcGpWU_iszP4iaRi31kMZDE6Y2kxNjM4MTgxNzgxODE4ZTE6cmQ4OlNIQTJfMjU2MzI6FdgKw3oynu3DhtU-K1E1xAYG6K8_ufAHV5zKhCZkKWllZWVlZQ")
        self.assertEqual(os.path.exists("storage-alice/local_published/data.mdb"),True,"Certificate not imported")

class GetCertsFromStateTestState(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
    
    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_emptyState(self):
        shutil.copyfile("TestYaml/part3.yaml","storage-alice/state.yaml")
        tmp = sol.GetCertsFromState("alice")
        self.assertEqual(tmp,['null'],"Incorrect certificates extracted")

    def test_simpleState(self):
        shutil.copyfile("TestYaml/part2.yaml","storage-alice/state.yaml")
        tmp = sol.GetCertsFromState("alice")
        cor = ['ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU', 'ZDI6aHRkODpTSEEyXzI1NmQzMjrAdWyumqqEA3XZNykf-yczS5-x_RNsZwxVifKSauDpHDc1OmQzOmtleTM1OgAAAeASCeNjeGCqVMOknL2lcNTKug3eGHUtBoEk2ykAf2yFNTp2YWx1ZWQxOnYxNTphY3Rpb246e2ZyaWVuZH1lZWVlNTpyb290c2xkMTA6cHVibGljX2tleTM1OgAAAX40xGULrwRPMp7iqbQgGtBWNugyiHWPXJVCjlJF0ESUOTpzaWduYXR1cmUxMzQ6pqpmsPITH0HYTjsHZI6Mir--RlefreWcDcCmB-Z9mdHjfcJBZbNkVS6wKZ6yfjS3ZdYOH2daWVKYia-dpLLfBGQxOmNpMTYzNjA2NTE2Mjk1NWUxOnJkODpTSEEyXzI1NjMyOsB1bK6aqoQDddk3KR_7JzNLn7H9E2xnDFWJ8pJq4OkcZWVlZWU']
        self.assertEqual(tmp,cor,"Incorrect certificates extracted")

    def test_manyCertsState(self):
        shutil.copyfile("TestYaml/part4.yaml","storage-alice/state.yaml")
        tmp = sol.GetCertsFromState("alice")
        ft = open('TestYaml/Test5.txt','r')
        cor = ft.readlines()
        cor = [x.strip() for x in cor]
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect certificates extracted")

    def test_AdvancedCertState(self):
        shutil.copyfile("TestYaml/part5.yaml","storage-alice/state.yaml")
        tmp = sol.GetCertsFromState("alice")
        ft = open('TestYaml/Test6.txt','r')
        cor = ft.readlines()
        cor = [x.strip() for x in cor]
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect certificates extracted")

class publishTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_noStateNoCert(self):
        cert = [] 
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        self.assertEqual(tmp,[],"Incorrect state")
    
    def test_noStateSingleCert(self):
        cert = ["ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU"]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        cor = ['identities:\n', '  mGmnv3nUG3_2bukRRbpJfXwI3CJB2RB1jj2rtsDIEPw:\n', '    date: "1636949716917"\n', '    state: ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU\n']
        self.assertEqual(tmp,cor,"Incorrect state")
    
    def test_noStateManyCert(self):
        ft = open('TestYaml/Test7.txt','r')
        cert = ft.readlines()
        ft.close()
        cert = [x.strip() for x in cert]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part8.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")
    
    def test_emptyStateNoCert(self):
        shutil.copyfile("TestYaml/part6.yaml","storage-alice/state.yaml")
        cert = [] 
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        cor = []
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_emptyStateSingleCert(self):
        shutil.copyfile("TestYaml/part6.yaml","storage-alice/state.yaml")
        cert = ["ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU"]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        cor = ['identities:\n', '  mGmnv3nUG3_2bukRRbpJfXwI3CJB2RB1jj2rtsDIEPw:\n', '    date: "1636949716917"\n', '    state: ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU\n']
        self.assertEqual(tmp,cor,"Incorrect state")
    
    def test_emptyStateManyCert(self):
        shutil.copyfile("TestYaml/part6.yaml","storage-alice/state.yaml")
        ft = open('TestYaml/Test7.txt','r')
        cert = ft.readlines()
        ft.close()
        cert = [x.strip() for x in cert]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part8.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_smallStateNoCert(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        cert = [] 
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part7.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_smallStateSingleCert(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        cert = ["ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU"]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part7.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")
    
    def test_smallStateManyCert(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        ft = open('TestYaml/Test7.txt','r')
        cert = ft.readlines()
        ft.close()
        cert = [x.strip() for x in cert]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part9.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_largeStateNoCert(self):
        shutil.copyfile("TestYaml/part8.yaml","storage-alice/state.yaml")
        cert = [] 
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part8.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_largeStateSingleCert(self):
        shutil.copyfile("TestYaml/part8.yaml","storage-alice/state.yaml")
        cert = ["ZDI6aHRkODpTSEEyXzI1NmRlZTU6cm9vdHNsZDEwOnB1YmxpY19rZXkzNToAAAGYaae_edQbf_Zu6RFFukl9fAjcIkHZEHWOPau2wMgQ_Dk6c2lnbmF0dXJlODk6J8kXyJhw-vUx709AqsQ92EArx0VgFroDnpMXR8jNkB5Q5gjTQRORV_RDDxc_mmQvp66BU0739wpcY-NzDYMXBGQxOmNpMTYzNjk0OTcxNjkxN2UxOnJkZWVlZWU"]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part10.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")
    
    def test_largeStateManyCert(self):
        shutil.copyfile("TestYaml/part8.yaml","storage-alice/state.yaml")
        ft = open('TestYaml/Test7.txt','r')
        cert = ft.readlines()
        ft.close()
        cert = [x.strip() for x in cert]
        sol.publish("alice",cert)
        ft = open('storage-alice/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part8.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

class shareStateTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
        sol.createIdentity("bob")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")
        if os.path.exists("storage-bob"):
            shutil.rmtree("storage-bob")

    def test_noSource(self):
        self.assertEqual(sol.shareState("alice","bob"),"no certificates to share.","Incorrect return")
    
    def test_noTarget(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        sol.shareState("alice","bob")
        ft = open('storage-bob/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part7.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_emptyState(self):
        shutil.copyfile("TestYaml/part6.yaml","storage-alice/state.yaml")
        sol.shareState("alice","bob")
        ft = open('storage-bob/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part6.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")

    def test_mix(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        shutil.copyfile("TestYaml/part8.yaml","storage-bob/state.yaml")
        sol.shareState("alice","bob")
        ft = open('storage-bob/state.yaml','r')
        tmp = ft.readlines()
        ft.close()
        ft = open('TestYaml/part11.yaml','r')
        cor = ft.readlines()
        ft.close()
        self.assertEqual(tmp,cor,"Incorrect state")


class loadStatesTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")

    def test_noLoad(self):
        tmp = sol.loadStates("alice")
        self.assertEqual(tmp,"error, yaml file doesn't exists.","Something was incorrectly loaded")

    def test_emptyLoad(self):
        shutil.copyfile("TestYaml/part6.yaml","storage-alice/state.yaml")
        sol.loadStates("alice")
        tmp = os.path.exists("storage-alice/local_published/data.mdb")
        self.assertEqual(tmp,False,"Something was incorrectly loaded")
    
    def test_smallLoad(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        sol.loadStates("alice")
        tmp = os.path.exists("storage-alice/local_published/data.mdb")
        self.assertEqual(tmp,True,"Nothing was loaded")

class give_statesTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
        sol.createIdentity("bob")
    
    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")
        if os.path.exists("storage-bob"):
            shutil.rmtree("storage-bob")
    
    def test_noState(self):
        sol.give_states("alice","bob")
        ft = open('storage-alice/state.yaml','r')
        tmp1 = ft.readlines()
        ft.close()
        ft = open('storage-bob/state.yaml','r')
        tmp2 = ft.readlines()
        ft.close()
        tmp3 = os.path.exists("storage-bob/local_published/data.mdb")
        tmpPack = [len(tmp1),len(tmp2),tmp3]
        corPack = [4,4,True]
        self.assertEqual(tmpPack,corPack,"Incorrect give_states")

    def test_emptyState(self):
        shutil.copyfile("TestYaml/part6.yaml","storage-alice/state.yaml")
        sol.give_states("alice","bob")
        ft = open('storage-alice/state.yaml','r')
        tmp1 = ft.readlines()
        ft.close()
        ft = open('storage-bob/state.yaml','r')
        tmp2 = ft.readlines()
        ft.close()
        tmp3 = os.path.exists("storage-bob/local_published/data.mdb")
        tmpPack = [len(tmp1),len(tmp2),tmp3]
        corPack = [4,4,True]
        self.assertEqual(tmpPack,corPack,"Incorrect give_states")

    def test_simpleState(self):
        shutil.copyfile("TestYaml/part7.yaml","storage-alice/state.yaml")
        sol.give_states("alice","bob")
        ft = open('storage-alice/state.yaml','r')
        tmp1 = ft.readlines()
        ft.close()
        ft = open('storage-bob/state.yaml','r')
        tmp2 = ft.readlines()
        ft.close()
        tmp3 = os.path.exists("storage-bob/local_published/data.mdb")
        tmpPack = [len(tmp1),len(tmp2),tmp3]
        corPack = [10,10,True]
        self.assertEqual(tmpPack,corPack,"Incorrect give_states")

    def test_largeState(self):
        shutil.copyfile("TestYaml/part8.yaml","storage-alice/state.yaml")
        sol.give_states("alice","bob")
        ft = open('storage-alice/state.yaml','r')
        tmp1 = ft.readlines()
        ft.close()
        ft = open('storage-bob/state.yaml','r')
        tmp2 = ft.readlines()
        ft.close()
        tmp3 = os.path.exists("storage-bob/local_published/data.mdb")
        tmpPack = [len(tmp1),len(tmp2),tmp3]
        corPack = [130,130,True]
        self.assertEqual(tmpPack,corPack,"Incorrect give_states")

class handshakeTestCase(unittest.TestCase):
    def setUp(self):
        sol.createIdentity("alice")
        sol.createIdentity("bob")

    def tearDown(self):
        if os.path.exists("storage-alice"):
            shutil.rmtree("storage-alice")
        if os.path.exists("storage-bob"):
            shutil.rmtree("storage-bob")
        if os.path.exists("storage-craig"):
            shutil.rmtree("storage-craig")
        if os.path.exists("state-person1.bin"):
            os.remove("state-person1.bin")
        if os.path.exists("state-person2.bin"):
            os.remove("state-person2.bin")

    def test_noRelation(self):
        tmp = sol.handshake("alice","bob","action:{foo}")
        cor = "person1 >> person2: Initiate\nperson1 << person2: Respond\nperson1 >> person2: Step\n"
        self.assertEqual(tmp,cor,"Inccorect handshake result")

    def test_oneUniRelation(self):
        sol.setRelationship("alice",sol.getPubKey("bob"),"action:{foo}")
        tmp = sol.handshake("alice","bob","action:{foo}")
        cor = "person1 >> person2: Initiate\nperson1 << person2: Respond\nperson1 >> person2: Step\n"
        self.assertEqual(tmp,cor,"Inccorect handshake result")

    def test_oneUniRelationInverse(self):
        sol.setRelationship("alice",sol.getPubKey("bob"),"action:{foo}")
        tmp = sol.handshake("bob","alice","action:{foo}")
        cor = "person1 >> person2: Initiate\nperson1 << person2: Respond\nperson1 >> person2: Step\n"
        self.assertEqual(tmp,cor,"Inccorect handshake result")

    def test_oneUniRelationShared(self):
        sol.setRelationship("alice",sol.getPubKey("bob"),"action:{foo}")
        sol.give_states("alice","bob")
        tmp = len(sol.handshake("alice","bob","action:{foo}"))
        cor = 459
        self.assertEqual(tmp,cor,"Inccorect handshake result")
    
    def test_oneUniRelationSharedInverse(self):
        sol.setRelationship("alice",sol.getPubKey("bob"),"action:{foo}")
        sol.give_states("alice","bob")
        tmp = sol.handshake("bob","alice","action:{foo}")
        cor = "person1 >> person2: Initiate\nperson1 << person2: Respond\nperson1 >> person2: Step\n"
        self.assertEqual(tmp,cor,"Inccorect handshake result")

    def test_manyUniRelationShared(self):
        shutil.copyfile("TestYaml/part8.yaml","storage-alice/state.yaml")
        sol.setRelationship("alice",sol.getPubKey("bob"),"action:{foo}")
        sol.give_states("alice","bob")
        tmp = sol.handshake("alice","bob","action:{foo}")
        cor = 459
        self.assertEqual(len(tmp),cor,"Inccorect handshake result")

    def test_manyUniRelationSharedInverse(self):
        shutil.copyfile("TestYaml/part8.yaml","storage-alice/state.yaml")
        sol.setRelationship("alice",sol.getPubKey("bob"),"action:{foo}")
        sol.give_states("alice","bob")
        tmp = sol.handshake("bob","alice","action:{foo}")
        cor = "person1 >> person2: Initiate\nperson1 << person2: Respond\nperson1 >> person2: Step\n"
        self.assertEqual(tmp,cor,"Inccorect handshake result")

    def test_triWayrelationSucces(self):
        sol.createIdentity("craig")
        sol.setRelationship("alice",sol.getPubKey("craig"),"action:{foo}")
        sol.setRelationship("craig",sol.getPubKey("bob"),"action:{foo}")
        sol.give_states("alice","craig")
        sol.give_states("craig","bob")
        tmp = sol.handshake("alice","bob","action:{foo}")
        cor = 459
        self.assertEqual(len(tmp),cor,"Inccorect handshake result")

    def test_triWayrelationFail(self):
        sol.createIdentity("craig")
        sol.setRelationship("alice",sol.getPubKey("craig"),"action:{foo}")
        sol.setRelationship("craig",sol.getPubKey("bob"),"action:{foo}")
        sol.give_states("alice","craig")
        sol.give_states("craig","bob")
        tmp = sol.handshake("bob","alice","action:{foo}")
        cor = "person1 >> person2: Initiate\nperson1 << person2: Respond\nperson1 >> person2: Step\n"
        self.assertEqual(tmp,cor,"Inccorect handshake result")

def suite():
    #suite = unittest.TestSuite()

    #suite.addTest(give_statesTestCase('test_give_states'))
    #suite.addTest(createIdentityTestCase('test_create'))
    #suite.addTest(createIdentityTestCase('test_replace'))
    #suite.addTest(certImportTestCase('test_simpleCert'))
    #suite.addTest(handshakeTestCase('test_manyUniRelationShared'))
    #suite=loadTestsFromTestCase(unittest.TestCase)
    return suite

if __name__ == '__main__':
    unittest.main()
    #runner = unittest.TextTestRunner() 
    #runner.run(suite())