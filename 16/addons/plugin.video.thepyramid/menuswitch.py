import sys , re , os , time
oo000 = sys . path [ 0 ]
ii = [ ]
if 51 - 51: IiI1i11I
Iii1I1 = raw_input ( 'Type 1 to encrypt a file, 2 to decrypt one, then press return\n' )
if '2' in Iii1I1 :
 OOO0O0O0ooooo = 'decrypt'
 iIIii1IIi = raw_input ( 'What is the pass key? enter and press return\n' )
elif '1' in Iii1I1 :
 OOO0O0O0ooooo = 'encrypt'
print 'What is the name of the file you wish to ' + OOO0O0O0ooooo + '?'
o0OO00 = raw_input ( 'MAKE SURE YOU include file type extension .xml .txt etc and press return\n' )
if '1' in Iii1I1 :
 oo = raw_input ( 'What type of encryption would you like today? 1/2/3/4/5 \n' )
i1iII1IiiIiI1 = oo000 . replace ( '\\' , '/' ) + '/' + o0OO00
print i1iII1IiiIiI1
iIiiiI1IiI1I1 = open ( i1iII1IiiIiI1 ) . read ( )
o0OoOoOO00 = re . compile ( '<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?<info>(.+?)</info>' , re . DOTALL ) . findall ( iIiiiI1IiI1I1 )
if 27 - 27: OOOo0 / Oo - Ooo00oOo00o . I1IiI
def o0OOO ( name , image , url5 , fanart , info ) :
 print Iii1I1
 if '1' in Iii1I1 :
  iIiiiI = oo000 . replace ( '\\' , '/' ) + '/encrypted.xml'
 elif '2' in Iii1I1 :
  iIiiiI = oo000 . replace ( '\\' , '/' ) + '/decrypted.xml'
 if not os . path . exists ( iIiiiI ) :
  Iii1ii1II11i = open ( iIiiiI , "w" )
  Iii1ii1II11i . write ( '<channels>\n' )
 else :
  Iii1ii1II11i = open ( iIiiiI , "a" )
 if name not in ii :
  Iii1ii1II11i . write ( '<channel>\n' )
  Iii1ii1II11i . write ( '<name>' + name + '</name>\n' )
  Iii1ii1II11i . write ( '<thumbnail>' + image + '</thumbnail>\n' )
  Iii1ii1II11i . write ( '<externallink>' + url5 + '</externallink>\n' )
  Iii1ii1II11i . write ( '<fanart>' + fanart + '</fanart>\n' )
  Iii1ii1II11i . write ( '<info>' + info + '</info>\n' )
  Iii1ii1II11i . write ( '</channel>\n\n' )
  ii . append ( name )
  if 10 - 10: I1iII1iiII + I1Ii111 / OOo
  if 41 - 41: I1II1
if '1' in Iii1I1 :
 for Ooo0OO0oOO , oooO0oo0oOOOO , O0oO , o0oO0 , oo00 in o0OoOoOO00 :
  o00 = Ooo0OO0oOO ; Oo0oO0ooo = oooO0oo0oOOOO ; o0oOoO00o = O0oO ; i1 = o0oO0 ; oOOoo00O0O = oo00
  print o0oOoO00o
  if oo == '1' :
   i1111 = o0oOoO00o . replace ( '.txt' , '[XXXX]' ) . replace ( '.m3u' , '[XXXZ]' ) . replace ( '.xml' , '[XXXV]' ) . replace ( 'http://' , '[QT]' ) . replace ( 'a' , '[PD]' ) . replace ( 'b' , '[ID]' )
   i11 = i1111 . replace ( 'c' , '[RJ]' ) . replace ( 'd' , '[LS]' ) . replace ( 'e' , '[MW]' ) . replace ( 'f' , '[LW]' ) . replace ( 'g' , '[OI]' ) . replace ( 'h' , '[KW]' ) . replace ( 'i' , '[YO]' ) . replace ( 'j' , '[HO]' ) . replace ( 'k' , '[YY]' ) . replace ( 'l' , '[JJ]' )
   I11 = i11 . replace ( 'm' , '[BU]' ) . replace ( 'n' , '[QZ]' ) . replace ( 'o' , '[XU]' ) . replace ( 'p' , '[FU]' ) . replace ( 'q' , '[WA]' ) . replace ( 'r' , '[SS]' ) . replace ( 's' , '[UP]' ) . replace ( 't' , '[WI]' ) . replace ( 'u' , '[UR]' ) . replace ( 'v' , '[FA]' )
   Oo0o0000o0o0 = I11 . replace ( 'w' , '[MO]' ) . replace ( 'x' , '[FO]' ) . replace ( 'y' , '[DE]' ) . replace ( 'z' , '[AL]' ) . replace ( '0' , '[TH]' ) . replace ( '1' , '[IT]' ) . replace ( '2' , '[XX]' ) . replace ( '3' , '[XQ]' ) . replace ( '4' , '[XW]' ) . replace ( '5' , '[XY]' )
   oOo0oooo00o = Oo0o0000o0o0 . replace ( '6' , '[XA]' ) . replace ( '7' , '[XB]' ) . replace ( '8' , '[XC]' ) . replace ( '9' , '[XZ]' ) . replace ( '.' , '[WX]' ) . replace ( '/' , '[YZ]' ) . replace ( '[XXXX]' , 'Have a nice day now' ) . replace ( '[XXXV]' , 'Hope you enjoy the view' ) . replace ( '[XXXZ]' , 'Nothing to see here' )
  elif oo == '2' :
   i1111 = o0oOoO00o . replace ( '.txt' , '[XXXX]' ) . replace ( '.m3u' , '[XXXZ]' ) . replace ( '.xml' , '[XXXV]' ) . replace ( 'http://' , '{ZZ}' ) . replace ( 'a' , '{LP}' ) . replace ( 'b' , '{MW}' )
   i11 = i1111 . replace ( 'c' , '{EO}' ) . replace ( 'd' , '{XW}' ) . replace ( 'e' , '{MS}' ) . replace ( 'f' , '{LE}' ) . replace ( 'g' , '{GO}' ) . replace ( 'h' , '{WO}' ) . replace ( 'i' , '{RL}' ) . replace ( 'j' , '{DI}' ) . replace ( 'k' , '{SA}' ) . replace ( 'l' , '{WE}' )
   I11 = i11 . replace ( 'm' , '{SO}' ) . replace ( 'n' , '{ME}' ) . replace ( 'o' , '{ID}' ) . replace ( 'p' , '{ON}' ) . replace ( 'q' , '{TC}' ) . replace ( 'r' , '{AR}' ) . replace ( 's' , '{EI}' ) . replace ( 't' , '{FI}' ) . replace ( 'u' , '{VE}' ) . replace ( 'v' , '{NE}' )
   Oo0o0000o0o0 = I11 . replace ( 'w' , '{VE}' ) . replace ( 'x' , '{RB}' ) . replace ( 'y' , '{EE}' ) . replace ( 'z' , '{HA}' ) . replace ( '0' , '{AB}' ) . replace ( '1' , '{CD}' ) . replace ( '2' , '{EF}' ) . replace ( '3' , '{GH}' ) . replace ( '4' , '{IJ}' ) . replace ( '5' , '{KL}' )
   oOo0oooo00o = Oo0o0000o0o0 . replace ( '6' , '{MN}' ) . replace ( '7' , '{OP}' ) . replace ( '8' , '{QR}' ) . replace ( '9' , '{ST}' ) . replace ( '.' , '{UV}' ) . replace ( '/' , '{WX}' ) . replace ( '[XXXX]' , 'Have a nice day now' ) . replace ( '[XXXV]' , 'Hope you enjoy the view' ) . replace ( '[XXXZ]' , 'Nothing to see here' )
  elif oo == '3' :
   i1111 = o0oOoO00o . replace ( '.txt' , '[XXXX]' ) . replace ( '.m3u' , '[XXXZ]' ) . replace ( '.xml' , '[XXXV]' ) . replace ( 'http://' , '(AA)' ) . replace ( 'a' , '(ZZ)' ) . replace ( 'b' , '(QR)' )
   i11 = i1111 . replace ( 'c' , '(PM)' ) . replace ( 'd' , '(ML)' ) . replace ( 'e' , '(PZ)' ) . replace ( 'f' , '(AA)' ) . replace ( 'g' , '(YO)' ) . replace ( 'h' , '(UW)' ) . replace ( 'i' , '(HA)' ) . replace ( 'j' , '(TC)' ) . replace ( 'k' , '(AL)' ) . replace ( 'l' , '(MD)' )
   I11 = i11 . replace ( 'm' , '(OW)' ) . replace ( 'n' , '(NM)' ) . replace ( 'o' , '(AN)' ) . replace ( 'p' , '(HO)' ) . replace ( 'q' , '(TH)' ) . replace ( 'r' , '(TE)' ) . replace ( 's' , '(EF)' ) . replace ( 't' , '(UC)' ) . replace ( 'u' , '(KD)' ) . replace ( 'v' , '(OY)' )
   Oo0o0000o0o0 = I11 . replace ( 'w' , '(OU)' ) . replace ( 'x' , '(IN)' ) . replace ( 'y' , '(TE)' ) . replace ( 'z' , '(ND)' ) . replace ( '0' , '(ON)' ) . replace ( '1' , '(RI)' ) . replace ( '2' , '(PP)' ) . replace ( '3' , '(IN)' ) . replace ( '4' , '(GT)' ) . replace ( '5' , '(HI)' )
   oOo0oooo00o = Oo0o0000o0o0 . replace ( '6' , '(SO)' ) . replace ( '7' , '(FF)' ) . replace ( '8' , '(MO)' ) . replace ( '9' , '(FO)' ) . replace ( '.' , '(CY)' ) . replace ( '/' , '(AZ)' ) . replace ( '[XXXX]' , 'Have a nice day now' ) . replace ( '[XXXV]' , 'Hope you enjoy the view' ) . replace ( '[XXXZ]' , 'Nothing to see here' )
  elif oo == '4' :
   i1111 = o0oOoO00o . replace ( '.txt' , '[XXXX]' ) . replace ( '.m3u' , '[XXXZ]' ) . replace ( '.xml' , '[XXXV]' ) . replace ( 'http://' , '~PP~' ) . replace ( 'a' , '~EZ~' ) . replace ( 'b' , '~PZ~' )
   i11 = i1111 . replace ( 'c' , '~LE~' ) . replace ( 'd' , '~MO~' ) . replace ( 'e' , '~NS~' ) . replace ( 'f' , '~QU~' ) . replace ( 'g' , '~EE~' ) . replace ( 'h' , '~MD~' ) . replace ( 'i' , '~TH~' ) . replace ( 'j' , '~EQ~' ) . replace ( 'k' , '~UI~' ) . replace ( 'l' , '~CK~' )
   I11 = i11 . replace ( 'm' , '~BR~' ) . replace ( 'n' , '~OW~' ) . replace ( 'o' , '~NF~' ) . replace ( 'p' , '~OX~' ) . replace ( 'q' , '~JU~' ) . replace ( 'r' , '~MP~' ) . replace ( 's' , '~SO~' ) . replace ( 't' , '~VE~' ) . replace ( 'u' , '~RT~' ) . replace ( 'v' , '~HE~' )
   Oo0o0000o0o0 = I11 . replace ( 'w' , '~LA~' ) . replace ( 'x' , '~ZY~' ) . replace ( 'y' , '~DO~' ) . replace ( 'z' , '~GT~' ) . replace ( '0' , '~HE~' ) . replace ( '1' , '~ID~' ) . replace ( '2' , '~LE~' ) . replace ( '3' , '~BA~' ) . replace ( '4' , '~ST~' ) . replace ( '5' , '~AR~' )
   oOo0oooo00o = Oo0o0000o0o0 . replace ( '6' , '~DH~' ) . replace ( '7' , '~IM~' ) . replace ( '8' , '~FK~' ) . replace ( '9' , '~IN~' ) . replace ( '.' , '~YA~' ) . replace ( '/' , '~NK~' ) . replace ( '[XXXX]' , 'Have a nice day now' ) . replace ( '[XXXV]' , 'Hope you enjoy the view' ) . replace ( '[XXXZ]' , 'Nothing to see here' )
  elif oo == '5' :
   i1111 = o0oOoO00o . replace ( '.txt' , '[XXXX]' ) . replace ( '.m3u' , '[XXXZ]' ) . replace ( '.xml' , '[XXXV]' ) . replace ( 'http://' , '@WI@' ) . replace ( 'a' , '@SE@' ) . replace ( 'b' , '@ME@' )
   i11 = i1111 . replace ( 'c' , '@NS@' ) . replace ( 'd' , '@AY@' ) . replace ( 'e' , '@ON@' ) . replace ( 'f' , '@NL@' ) . replace ( 'g' , '@YF@' ) . replace ( 'h' , '@OO@' ) . replace ( 'i' , '@LS@' ) . replace ( 'j' , '@RI@' ) . replace ( 'k' , '@PE@' ) . replace ( 'l' , '@OP@' )
   I11 = i11 . replace ( 'm' , '@LE@' ) . replace ( 'n' , '@OF@' ) . replace ( 'o' , '@FS@' ) . replace ( 'p' , '@OG@' ) . replace ( 'q' , '@OF@' ) . replace ( 'r' , '@UQ@' ) . replace ( 's' , '@KY@' ) . replace ( 't' , '@OU@' ) . replace ( 'u' , '@RS@' ) . replace ( 'v' , '@EL@' )
   Oo0o0000o0o0 = I11 . replace ( 'w' , '@FO@' ) . replace ( 'x' , '@KM@' ) . replace ( 'y' , '@OT@' ) . replace ( 'z' , '@HE@' ) . replace ( '0' , '@RF@' ) . replace ( '1' , '@UC@' ) . replace ( '2' , '@KE@' ) . replace ( '3' , '@RH' ) . replace ( '4' , '@AV@' ) . replace ( '5' , '@EA@' )
   oOo0oooo00o = Oo0o0000o0o0 . replace ( '6' , '@NI@' ) . replace ( '7' , '@CE@' ) . replace ( '8' , '@DA@' ) . replace ( '9' , '@YN@' ) . replace ( '.' , '@OW@' ) . replace ( '/' , '@PC@' ) . replace ( '[XXXX]' , 'Have a nice day now' ) . replace ( '[XXXV]' , 'Hope you enjoy the view' ) . replace ( '[XXXZ]' , 'Nothing to see here' )
  print oOo0oooo00o
  o0OOO ( o00 , Oo0oO0ooo , oOo0oooo00o , i1 , oOOoo00O0O )
  if 65 - 65: O0o * i1iIIII * I1
  if 54 - 54: oO % IiiIIiiI11 / oooOOOOO * IiiIII111ii / i1iIIi1
  if 50 - 50: IiIi1Iii1I1 - O00O0O0O0
ooO0O = 'u'
ooiii11iII = 'a'
i1I111I = 'p'
i11I1IIiiIi = 's'
IiIiIi = 'o'
II = 'q'
iI = 'y'
iI11iiiI1II = 'm'
O0oooo0Oo00 = 'f'
Ii11iii11I = 'a'
oOo00Oo00O = 'w'
iI11i1I1 = 'b'
o0o0OOO0o0 = 'o'
ooOOOo0oo0O0 = 'n'
if 71 - 71: oO00OO0oo0 . I1Ii111
oO0o0ooo = Ii11iii11I + ooOOOo0oo0O0 + o0o0OOO0o0 + iI11i1I1 + iI + iI11iiiI1II + IiIiIi + ooO0O + i11I1IIiiIi
if 20 - 20: i1iIIII
if 77 - 77: O0o / oooOOOOO
if '2' in Iii1I1 :
 if iIIii1IIi == oO0o0ooo :
  for Ooo0OO0oOO , oooO0oo0oOOOO , O0oO , o0oO0 , oo00 in o0OoOoOO00 :
   o00 = Ooo0OO0oOO ; Oo0oO0ooo = oooO0oo0oOOOO ; o0oOoO00o = O0oO ; i1 = o0oO0 ; oOOoo00O0O = oo00
   if '[QT]' in o0oOoO00o :
    oo = '1'
   elif '{ZZ}' in o0oOoO00o :
    oo = '2'
   elif '(AA)' in o0oOoO00o :
    oo = '3'
   elif '~PP~' in o0oOoO00o :
    oo = '4'
   elif '@WI@' in o0oOoO00o :
    oo = '5'
   else :
    oo = '6'
   if oo == '1' :
    i1111 = o0oOoO00o . replace ( 'Have a nice day now' , '.txt' ) . replace ( 'Hope you enjoy the view' , '.xml' ) . replace ( 'Nothing to see here' , '.m3u' ) . replace ( '[QT]' , 'http://' ) . replace ( '[PD]' , 'a' ) . replace ( '[ID]' , 'b' )
    i11 = i1111 . replace ( '[RJ]' , 'c' ) . replace ( '[LS]' , 'd' ) . replace ( '[MW]' , 'e' ) . replace ( '[LW]' , 'f' ) . replace ( '[OI]' , 'g' ) . replace ( '[KW]' , 'h' ) . replace ( '[YO]' , 'i' ) . replace ( '[HO]' , 'j' ) . replace ( '[YY]' , 'k' ) . replace ( '[JJ]' , 'l' )
    I11 = i11 . replace ( '[BU]' , 'm' ) . replace ( '[QZ]' , 'n' ) . replace ( '[XU]' , 'o' ) . replace ( '[FU]' , 'p' ) . replace ( '[WA]' , 'q' ) . replace ( '[SS]' , 'r' ) . replace ( '[UP]' , 's' ) . replace ( '[WI]' , 't' ) . replace ( '[UR]' , 'u' ) . replace ( '[FA]' , 'v' )
    Oo0o0000o0o0 = I11 . replace ( '[MO]' , 'w' ) . replace ( '[FO]' , 'x' ) . replace ( '[DE]' , 'y' ) . replace ( '[AL]' , 'z' ) . replace ( '[TH]' , '0' ) . replace ( '[IT]' , '1' ) . replace ( '[XX]' , '2' ) . replace ( '[XQ]' , '3' ) . replace ( '[XW]' , '4' ) . replace ( '[XY]' , '5' )
    oOo0oooo00o = Oo0o0000o0o0 . replace ( '[XA]' , '6' ) . replace ( '[XB]' , '7' ) . replace ( '[XC]' , '8' ) . replace ( '[XZ]' , '9' ) . replace ( '[WX]' , '.' ) . replace ( '[YZ]' , '/' )
   elif oo == '2' :
    i1111 = o0oOoO00o . replace ( 'Have a nice day now' , '.txt' ) . replace ( 'Hope you enjoy the view' , '.xml' ) . replace ( 'Nothing to see here' , ',m3u' ) . replace ( '{ZZ}' , 'http://' ) . replace ( '{LP}' , 'a' ) . replace ( '{MW}' , 'b' )
    i11 = i1111 . replace ( '{EO}' , 'c' ) . replace ( '{XW}' , 'd' ) . replace ( '{MS}' , 'e' ) . replace ( '{LE}' , 'f' ) . replace ( '{GO}' , 'g' ) . replace ( '{WO}' , 'h' ) . replace ( '{RL}' , 'i' ) . replace ( '{DI}' , 'j' ) . replace ( '{SA}' , 'k' ) . replace ( '{WE}' , 'l' )
    I11 = i11 . replace ( '{SO}' , 'm' ) . replace ( '{ME}' , 'n' ) . replace ( '{ID}' , 'o' ) . replace ( '{ON}' , 'p' ) . replace ( '{TC}' , 'q' ) . replace ( '{AR}' , 'r' ) . replace ( '{EI}' , 's' ) . replace ( '{FI}' , 't' ) . replace ( '{VE}' , 'u' ) . replace ( '{NE}' , 'v' )
    Oo0o0000o0o0 = I11 . replace ( '{VE}' , 'w' ) . replace ( '{RB}' , 'x' ) . replace ( '{EE}' , 'y' ) . replace ( '{HA}' , 'z' ) . replace ( '{AB}' , '0' ) . replace ( '{CD}' , '1' ) . replace ( '{EF}' , '2' ) . replace ( '{GH}' , '3' ) . replace ( '{IJ}' , '4' ) . replace ( '{KL}' , '5' )
    oOo0oooo00o = Oo0o0000o0o0 . replace ( '{MN}' , '6' ) . replace ( '{OP}' , '7' ) . replace ( '{QR}' , '8' ) . replace ( '{ST}' , '9' ) . replace ( '{UV}' , '.' ) . replace ( '{WX}' , '/' )
   elif oo == '3' :
    i1111 = o0oOoO00o . replace ( 'Have a nice day now' , '.txt' ) . replace ( 'Hope you enjoy the view' , '.xml' ) . replace ( 'Nothing to see here' , '.m3u' ) . replace ( '(AA)' , 'http://' ) . replace ( '(ZZ)' , 'a' ) . replace ( '(QR)' , 'b' )
    i11 = i1111 . replace ( '(PM)' , 'c' ) . replace ( '(ML)' , 'd' ) . replace ( '(PZ)' , 'e' ) . replace ( '(AA)' , 'f' ) . replace ( '(YO)' , 'g' ) . replace ( '(UW)' , 'h' ) . replace ( '(HA)' , 'i' ) . replace ( '(TC)' , 'j' ) . replace ( '(AL)' , 'k' ) . replace ( '(MD)' , 'l' )
    I11 = i11 . replace ( '(OW)' , 'm' ) . replace ( '(NM)' , 'n' ) . replace ( '(AN)' , 'o' ) . replace ( '(HO)' , 'p' ) . replace ( '(TH)' , 'q' ) . replace ( '(TE)' , 'r' ) . replace ( '(EF)' , 's' ) . replace ( '(UC)' , 't' ) . replace ( '(KD)' , 'u' ) . replace ( '(OY)' , 'v' )
    Oo0o0000o0o0 = I11 . replace ( '(OU)' , 'w' ) . replace ( '(IN)' , 'x' ) . replace ( '(TE)' , 'y' ) . replace ( '(ND)' , 'z' ) . replace ( '(ON)' , '0' ) . replace ( '(RI)' , '1' ) . replace ( '(PP)' , '2' ) . replace ( '(IN)' , '3' ) . replace ( '(GT)' , '4' ) . replace ( '(HI)' , '5' )
    oOo0oooo00o = Oo0o0000o0o0 . replace ( '(SO)' , '6' ) . replace ( '(FF)' , '7' ) . replace ( '(MO)' , '8' ) . replace ( '(FO)' , '9' ) . replace ( '(CY)' , '.' ) . replace ( '(AZ)' , '/' )
   elif oo == '4' :
    i1111 = o0oOoO00o . replace ( 'Have a nice day now' , '.txt' ) . replace ( 'Hope you enjoy the view' , '.xml' ) . replace ( 'Nothing to see here' , '.m3u' ) . replace ( '~PP~' , 'http://' ) . replace ( '~EZ~' , 'a' ) . replace ( '~PZ~' , 'b' )
    i11 = i1111 . replace ( '~LE~' , 'c' ) . replace ( '~MO~' , 'd' ) . replace ( '~NS~' , 'e' ) . replace ( '~QU~' , 'f' ) . replace ( '~EE~' , 'g' ) . replace ( '~MD~' , 'h' ) . replace ( '~TH~' , 'i' ) . replace ( '~EQ~' , 'j' ) . replace ( '~UI~' , 'k' ) . replace ( '~CK~' , 'l' )
    I11 = i11 . replace ( '~BR~' , 'm' ) . replace ( '~OW~' , 'n' ) . replace ( '~NF~' , 'o' ) . replace ( '~OX~' , 'p' ) . replace ( '~JU~' , 'q' ) . replace ( '~MP~' , 'r' ) . replace ( '~SO~' , 's' ) . replace ( '~VE~' , 't' ) . replace ( '~RT~' , 'u' ) . replace ( '~HE~' , 'v' )
    Oo0o0000o0o0 = I11 . replace ( '~LA~' , 'w' ) . replace ( '~ZY~' , 'x' ) . replace ( '~DO~' , 'y' ) . replace ( '~GT~' , 'z' ) . replace ( '~HE~' , '0' ) . replace ( '~ID~' , '1' ) . replace ( '~LE~' , '2' ) . replace ( '~BA~' , '3' ) . replace ( '~ST~' , '4' ) . replace ( '~AR~' , '5' )
    oOo0oooo00o = Oo0o0000o0o0 . replace ( '~DH~' , '6' ) . replace ( '~IM~' , '7' ) . replace ( '~FK~' , '8' ) . replace ( '~IN~' , '9' ) . replace ( '~YA~' , '.' ) . replace ( '~NK~' , '/' )
   elif oo == '5' :
    i1111 = o0oOoO00o . replace ( 'Have a nice day now' , '.txt' ) . replace ( 'Hope you enjoy the view' , '.xml' ) . replace ( 'Nothing to see here' , '.m3u' ) . replace ( '@WI@' , 'http://' ) . replace ( '@SE@' , 'a' ) . replace ( '@ME@' , 'b' )
    i11 = i1111 . replace ( '@NS@' , 'c' ) . replace ( '@AY@' , 'd' ) . replace ( '@ON@' , 'e' ) . replace ( '@NL@' , 'f' ) . replace ( '@YF@' , 'g' ) . replace ( '@OO@' , 'h' ) . replace ( '@LS@' , 'i' ) . replace ( '@RI@' , 'j' ) . replace ( '@PE@' , 'k' ) . replace ( '@OP@' , 'l' )
    I11 = i11 . replace ( '@LE@' , 'm' ) . replace ( '@OF@' , 'n' ) . replace ( '@FS@' , 'o' ) . replace ( '@OG@' , 'p' ) . replace ( '@OF@' , 'q' ) . replace ( '@UQ@' , 'r' ) . replace ( '@KY@' , 's' ) . replace ( '@OU@' , 't' ) . replace ( '@RS@' , 'u' ) . replace ( '@EL@' , 'v' )
    Oo0o0000o0o0 = I11 . replace ( '@FO@' , 'w' ) . replace ( '@KM@' , 'x' ) . replace ( '@OT@' , 'y' ) . replace ( '@HE@' , 'z' ) . replace ( '@RF@' , '0' ) . replace ( '@UC@' , '1' ) . replace ( '@KE@' , '2' ) . replace ( '@RH' , '3' ) . replace ( '@AV@' , '4' ) . replace ( '@EA@' , '5' )
    oOo0oooo00o = Oo0o0000o0o0 . replace ( '@NI@' , '6' ) . replace ( '@CE@' , '7' ) . replace ( '@DA@' , '8' ) . replace ( '@YN@' , '9' ) . replace ( '@OW@' , '.' ) . replace ( '@PC@' , '/' )
   elif oo == '6' :
    print 'Sorry this type on encryption is not recognised'
    time . sleep ( 2 )
    print 'The program will now close'
   o0OOO ( o00 , Oo0oO0ooo , oOo0oooo00o , i1 , oOOoo00O0O )
   if 98 - 98: Oo / I1IiI / IiI1i11I / i1iIIII
I1i1I1II = raw_input ( 'All done, press return to close' )
