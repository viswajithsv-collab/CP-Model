function dPsa = systemicArteryRC(Fin,Psa,Psp,Rsa,Csa)
   dPsa = (Fin - (Psa - Psp)/Rsa)/Csa;
end