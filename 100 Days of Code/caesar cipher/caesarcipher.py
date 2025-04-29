request = "yes"
print( """           
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88   
            88             88                                 
           ""             88                                 
                          88                                 
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b         88 88       d8 88       88 8PP""""""" 88          
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88          
              88                                             
              88           
""")
while request == "yes":
  

  alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

  
  direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
  if direction == "encode" or direction == "decode":
    text = input("Type your message:\n").lower()
    shift_check = True
    while shift_check is True:
      try:
        shift = int(input("Type the shift number:\n"))
        shift_check = False
      except Exception:
        print(f'Sorry, "{shift}" is an invalid input. Please input an integer number.')
  else:
    print(f'Sorry, "{direction}" is an invalid input. Please try again.')

  def ceasar(algo=direction, text1=text, shift1=shift):  
    #encryption
    if algo == "encode":
      wi = []
      fl = []
      cl = []

      for i in text1:
        if i in alphabet:
          wi.append(alphabet.index(i))
          cl.append(alphabet.index(i))
        else:
          wi.append(i)

      print(wi)
      sl = alphabet
      check = 0
      while check != shift1:
          sl.append(sl[0])
          sl.remove(sl[0])
          check += 1

      for i in wi:
        if i in cl:
          fl.append(sl[i])
        else:
          fl.append(i)
      
      dec1 = ''.join(fl)
      print(f"Your encoded message is {dec1}.")
    elif algo == "decode":
    #decryption
      tl = text1
      nl = []
      cl1 = []

      for i in tl:
        if i in alphabet:
          nl.append(alphabet.index(i))
          cl1.append(alphabet.index(i))
        else:
          nl.append(i)
          
      ac = alphabet
      el = []
      
      for i in range(0, shift1):
        el.insert(0, ac[-1])
        ac.remove(ac[-1])
        ac.insert(0, el[0])

      fel = []
      for i in nl:
        if i in cl1:
          fel.append(ac[i])
        else:
          fel.append(i)

      dec = ''.join(fel)

      print(f"The decoded text is {dec}.")

  ceasar(algo=direction, text1=text, shift1=shift)
  
  b = "q"
  if request == "yes":
    while b == "q":
      b = input("Do you want to use Ceasar's Cipher again?\n")
      if b == "yes":
        request = "yes"
      elif b == "no":
        request = "no"
        print("Thank you for using Ceasar's Cipher.")
      else:
        print(f"Sorry {b} is an invalid input")
        b = "q"    
  else:
    request == "no"
    print("Thank you for using Ceasar's Cipher.")
  