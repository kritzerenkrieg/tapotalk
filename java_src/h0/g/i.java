package h0.g;

public class i {
    private int a;
    private int b;
    private int c;
    private int d;
    private int e;
    private int f;
    private int g;

    public int getB() {
        return b;
    }

    public int getD() {
        return d;
    }

    public int getF() {
        return f;
    }

    public int a() {
        return this.a & 15;
    }

    public int b() {
        return this.b & 7;
    }

    public int c() {
        return this.d & 32767;
    }

    public int d() {
        return this.f & 32767;
    }

    public int e() {
        return this.c & 1;
    }

    public int f() {
        return this.e & 1;
    }

    public int g() {
        return this.g & 1;
    }

    public void h(int var1) {
        this.a = var1 & 15;
    }

    public void i(int var1) {
        this.b = var1 & 7;
    }

    public void j(int var1) {
        this.d = var1 & 32767;
    }

    public void k(int var1) {
        this.f = var1 & 32767;
    }

    public void l(int var1) {
        this.c = var1 & 1;
    }

    public void m(int var1) {
        this.e = var1 & 1;
    }

    public void n(int var1) {
        this.g = var1 & 1;
    }
}