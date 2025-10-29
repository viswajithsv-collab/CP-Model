function E = elastance(En,Emax,Emin)
    E = Emax.*En + (1-En).*Emin;
end