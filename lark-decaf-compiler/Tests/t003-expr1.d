int main() {
    int a;
    int b;
    int c;
    int d;

    int z;
    
    a = ReadInteger();
    b = ReadInteger();
    c = ReadInteger();
    d = ReadInteger();

    z = a + (b * 5);
    a = z * d;
    z = 2 * a + ((a + b) / (c + d));
    b = z / a;
    c = b * a + z;
    d = a - b - c - d - z;

    Print(a);
    Print(b);
    Print(c);
    Print(d);

    Print(z);
}