clear;
clc;

I = 11;
Q = 56;

I_char = dec2bin(0, 12);
I_binStr = dec2bin(I, 6);
I_binStr_n = dec2bin(bitxor(I, 63), 6);

for i = 1:1:6
    I_char(2*i-1) = I_binStr_n(i);
    I_char(2*i) = I_binStr(i);
end

Q_char_low = dec2bin(0, 6);
Q_char_high = dec2bin(0, 6);

Q_binStr = dec2bin(Q, 6);
Q_binStr_n = dec2bin(bitxor(Q, 63), 6);

for i = 1:1:3
    Q_char_low(2*i-1) = Q_binStr_n(i+3);
    Q_char_low(2*i) = Q_binStr(i+3);
end

Bin_char = [Q_char_high I_char Q_char_low];
Hex_char = dec2hex(bin2dec(Bin_char), 8);