function En = phi1(t,HR,alpha,n)
    Tc = 60./HR;
    tm = mod(t,Tc);
    x = tm./Tc;
    a1 = x./alpha(1);
    a2 = x./alpha(2);

    m = a1.^n(1);
    o = a2.^n(2);

    p = m./(1+m);
    q = 1./(1+o);

    z = p.*q;
    mEn = max(z);

    En = z./mEn;
end