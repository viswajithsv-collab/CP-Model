function dPsa = systemicArtery(Qin,Psa,Psp,Rsa,Csa)
   dPsa = (Qin - (Psa - Psp)/Rsa)/Csa;
end