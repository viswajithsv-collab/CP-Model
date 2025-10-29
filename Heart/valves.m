function F = valves(Pin,Pout,R)
    if Pin <= Pout
        F = 0;
    else
        F = (Pin - Pout)/R;
    end
end