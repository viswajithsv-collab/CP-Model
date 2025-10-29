function E = activation(gain,w,HR,alpha,n)
    u = 60/HR;
    x = mod(w,1);
    y = x/u;
    a1 = y/alpha(1);
    a2 = y/alpha(2);
    m = a1^n(1);
    o = a2^n(2);
    p = m/(1+m);
    q = 1/(1+o);
    E = gain*p*q;
end